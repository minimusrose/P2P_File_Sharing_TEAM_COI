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
                      progress_callback: Callable[[int], None]) -> None:
        """
        Télécharge un fichier (sera complété lors de l'intégration)
        
        Args:
            file_id: ID du fichier
            save_path: Où sauvegarder
            progress_callback: Fonction(percent) pour progression
        """
        # TODO: Implémenter lors de l'intégration avec network layer
        logger.info(f"Download requested: {file_id} -> {save_path}")
        pass

    