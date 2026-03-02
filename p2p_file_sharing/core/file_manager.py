"""Gestionnaire de fichiers et chunks"""
from pathlib import Path
import hashlib
from typing import List, Dict, Callable
from ..utils.config import CHUNK_SIZE, SHARED_FILES_DIR
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class FileManager:
    """Gère le chunking et l'assemblage de fichiers"""
    
    def __init__(self, database=None):
        self.db = database
        self.shared_files = {}  # file_id -> filepath
    
    def calculate_file_hash(self, filepath: str) -> str:
        """
        Calcule hash SHA256 du fichier complet
        
        Args:
            filepath: Chemin du fichier
        
        Returns:
            str: Hash hexadécimal
        """
        sha256 = hashlib.sha256()
        
        try:
            with open(filepath, 'rb') as f:
                while True:
                    data = f.read(8192)
                    if not data:
                        break
                    sha256.update(data)
            
            return sha256.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {filepath}: {e}")
            return ""
    
    def chunk_file(self, filepath: str) -> List[Dict]:
        """
        Découpe fichier en chunks de CHUNK_SIZE
        
        Args:
            filepath: Chemin du fichier à chunker
        
        Returns:
            List de dicts: [
                {'chunk_index': 0, 'data': bytes, 'hash': 'sha256...'},
                ...
            ]
        """
        chunks = []
        chunk_index = 0
        
        try:
            with open(filepath, 'rb') as f:
                while True:
                    data = f.read(CHUNK_SIZE)
                    if not data:
                        break
                    
                    chunk_hash = hashlib.sha256(data).hexdigest()
                    chunks.append({
                        'chunk_index': chunk_index,
                        'data': data,
                        'hash': chunk_hash,
                        'size': len(data)
                    })
                    chunk_index += 1
            
            logger.info(f"File chunked: {filepath} -> {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Error chunking file {filepath}: {e}")
            return []
    
    def assemble_chunks(self, chunks: List[Dict], output_path: str) -> bool:
        """
        Réassemble les chunks en fichier
        
        Args:
            chunks: Liste de chunks avec 'chunk_index', 'data', 'hash'
            output_path: Chemin du fichier de sortie
        
        Returns:
            bool: True si succès
        """
        try:
            # Trier par index
            sorted_chunks = sorted(chunks, key=lambda x: x['chunk_index'])
            
            # Vérifier continuité
            for i, chunk in enumerate(sorted_chunks):
                if chunk['chunk_index'] != i:
                    logger.error(f"Missing chunk {i}")
                    return False
            
            # Écrire fichier
            with open(output_path, 'wb') as f:
                for chunk in sorted_chunks:
                    # Vérifier hash si présent
                    if 'hash' in chunk and chunk['hash']:
                        calculated = hashlib.sha256(chunk['data']).hexdigest()
                        if calculated != chunk['hash']:
                            logger.error(f"Chunk {chunk['chunk_index']} hash mismatch!")
                            return False
                    
                    f.write(chunk['data'])
            
            logger.info(f"File reassembled: {output_path} ({len(sorted_chunks)} chunks)")
            return True
            
        except Exception as e:
            logger.error(f"Error assembling chunks: {e}")
            return False
    
    def add_shared_file(self, filepath: str) -> str:
        """
        Ajoute un fichier à partager
        
        Args:
            filepath: Chemin complet du fichier
        
        Returns:
            str: file_id unique
        """
        try:
            path = Path(filepath)
            if not path.exists():
                logger.error(f"File not found: {filepath}")
                return ""
            
            # Générer file_id
            file_id = hashlib.md5(filepath.encode()).hexdigest()[:16]
            
            # Calculer infos
            file_hash = self.calculate_file_hash(filepath)
            file_size = path.stat().st_size
            chunks_total = (file_size // CHUNK_SIZE) + (1 if file_size % CHUNK_SIZE else 0)
            
            # Stocker localement
            self.shared_files[file_id] = filepath
            
            # Ajouter à DB si disponible
            if self.db:
                self.db.add_file(
                    file_id=file_id,
                    filename=path.name,
                    size=file_size,
                    hash=file_hash,
                    owner_peer_id="local",  # Sera mis à jour
                    chunks_total=chunks_total
                )
                self.db.add_local_shared(file_id, filepath)
            
            logger.info(f"Shared file added: {path.name} (ID: {file_id})")
            logger.info(f"File shared: {file_id} - Ready to broadcast")
    
            return file_id
            
        except Exception as e:
            logger.error(f"Error adding shared file: {e}")
            return ""
    
    def get_shared_files(self) -> List[Dict]:
        """Retourne la liste des fichiers partagés localement"""
        if not self.db:
            return []
        
        return self.db.get_local_shared_files()

    def get_my_file_list(self) -> List[Dict]:
        """Retourne liste de nos fichiers pour l'envoyer aux peers"""
        files = self.get_shared_files()
    
        # Format pour envoi réseau
        file_list = []
        for f in files:
            file_list.append({
            'file_id': f['file_id'],
            'filename': f['filename'],
            'size': f['size'],
            'hash': f['hash'],
            'chunks_total': f['chunks_total']
        })
    
        return file_list
    

    def download_file(self, file_id: str, save_path: str, 
                      progress_callback: Callable[[int], None],
                      peer_manager) -> bool:
        """
        Télécharge un fichier depuis le réseau
        
        Args:
            file_id: ID du fichier
            save_path: Où sauvegarder
            progress_callback: Fonction(percent) pour progression
            peer_manager: PeerManager pour accéder aux peers
        
        Returns:
            bool: True si succès
        """
        try:
            logger.info(f"Starting download: {file_id} -> {save_path}")
            
            # 1. Récupérer infos fichier
            file_info = self.db.get_file_by_id(file_id)
            if not file_info:
                logger.error(f"File {file_id} not found in database")
                return False
            
            chunks_total = file_info['chunks_total']
            expected_hash = file_info['hash']
            logger.info(f"Downloading {file_info['filename']}: {chunks_total} chunks")
            
            # 2. Trouver le peer qui a le fichier (owner)
            owner_peer_id = file_info['owner_peer_id']
            peers = peer_manager.get_online_peers()
            owner_peer = next((p for p in peers if p['peer_id'] == owner_peer_id), None)
            
            if not owner_peer:
                logger.error(f"Owner peer {owner_peer_id} not online")
                return False
            
            logger.info(f"Downloading from {owner_peer_id} at {owner_peer['ip']}:{owner_peer['port']}")
            
            # 3. Télécharger chaque chunk
            chunks_data = []
            for i in range(chunks_total):
                logger.info(f"Requesting chunk {i+1}/{chunks_total}")
                
                chunk_data = self._request_chunk(
                    owner_peer['ip'],
                    owner_peer['port'],
                    file_id,
                    i,
                    peer_manager.local_peer_id
                )
                
                if not chunk_data:
                    logger.error(f"Failed to download chunk {i}")
                    return False
                
                chunks_data.append(chunk_data)
                
                # Mise à jour progression
                percent = int((i + 1) / chunks_total * 100)
                if progress_callback:
                    progress_callback(percent)
            
            # 4. Assembler les chunks
            logger.info(f"Assembling {len(chunks_data)} chunks...")
            with open(save_path, 'wb') as f:
                for chunk_data in chunks_data:
                    f.write(chunk_data)
            
            # 5. Vérifier hash final
            final_hash = self.calculate_file_hash(save_path)
            
            if final_hash == expected_hash:
                logger.info(f"✓ File downloaded successfully: {save_path}")
                logger.info(f"  Hash verified: {final_hash}")
                return True
            else:
                logger.error(f"Hash mismatch!")
                logger.error(f"  Expected: {expected_hash}")
                logger.error(f"  Got:      {final_hash}")
                return False
                
        except Exception as e:
            logger.error(f"Download error: {e}", exc_info=True)
            return False
    
    def _request_chunk(self, peer_ip: str, peer_port: int, file_id: str,
                      chunk_index: int, my_peer_id: str) -> bytes:
        """
        Demande un chunk à un peer
        
        Returns:
            bytes: Données du chunk ou None si erreur
        """
        from ..network.connection import TCPClient
        from ..network.protocol import create_message, MessageType
        
        client = TCPClient()
        try:
            if not client.connect(peer_ip, peer_port):
                logger.error(f"Cannot connect to {peer_ip}:{peer_port}")
                return None
            
            # Envoyer requête
            request = create_message(
                MessageType.CHUNK_REQUEST,
                my_peer_id,
                {
                    'file_id': file_id,
                    'chunk_index': chunk_index
                }
            )
            client.send_message(request)
            logger.debug(f"CHUNK_REQUEST sent for chunk {chunk_index}")
            
            # Recevoir réponse
            response = client.receive_message(timeout=30)
            
            if response and response['type'] == MessageType.CHUNK_DATA:
                import base64
                chunk_data = base64.b64decode(response['data']['chunk_data'])
                chunk_hash = response['data']['hash']
                
                # Vérifier hash
                import hashlib
                actual_hash = hashlib.sha256(chunk_data).hexdigest()
                
                if actual_hash == chunk_hash:
                    logger.debug(f"Chunk {chunk_index} received and verified")
                    return chunk_data
                else:
                    logger.error(f"Chunk {chunk_index} hash mismatch")
                    return None
            else:
                logger.error(f"Invalid response for chunk {chunk_index}")
                return None
                
        except Exception as e:
            logger.error(f"Error requesting chunk {chunk_index}: {e}")
            return None
        finally:
            client.close()

    