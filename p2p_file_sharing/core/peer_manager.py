"""Gestionnaire de peers"""
from typing import List, Dict
from datetime import datetime
from ..utils.logger import setup_logger
from ..utils.config import PEER_TIMEOUT

logger = setup_logger(__name__)

class PeerManager:
    """Gère la liste des peers et leur état"""
    
    def __init__(self, database):
        self.db = database
        self.local_peer_id = None
    
    def set_local_peer_id(self, peer_id: str):
        """Définit l'ID du peer local"""
        self.local_peer_id = peer_id
        logger.info(f"Local peer ID set: {peer_id}")
    
    def handle_peer_announce(self, peer_id: str, ip: str, port: int):
        """
        Callback appelé par network layer lors découverte peer
        """
        if peer_id == self.local_peer_id:
            return  # C'est nous, ignorer
        
        logger.info(f"Peer announced: {peer_id} at {ip}:{port}")
        self.add_peer(peer_id, ip, port)
    
    def add_peer(self, peer_id: str, ip: str, port: int) -> None:
        """Ajoute ou met à jour un peer"""
        if not self.db:
            logger.warning("Database not available")
            return
        
        self.db.add_peer(peer_id, ip, port)
        logger.debug(f"Peer {peer_id} added/updated in database")
    
    def remove_peer(self, peer_id: str) -> None:
        """Supprime un peer déconnecté"""
        if not self.db:
            return
        
        self.db.remove_peer(peer_id)
        logger.info(f"Peer removed: {peer_id}")
    
    def get_online_peers(self, timeout: int = PEER_TIMEOUT) -> List[Dict]:
        """
        Retourne la liste des peers en ligne
        
        Args:
            timeout: Secondes max depuis dernier heartbeat
        
        Returns:
            List de dicts avec peer_id, ip, port, last_seen
        """
        if not self.db:
            return []
        
        return self.db.get_active_peers(timeout)
    
    def update_peer_files(self, peer_id: str, file_list: List[Dict]) -> None:
        """
        Met à jour la liste des fichiers d'un peer
        
        Args:
            peer_id: ID du peer
            file_list: Liste de dicts avec file_id, filename, size, etc.
        """
        if not self.db:
            return
        
        for file_info in file_list:
            try:
                self.db.add_file(
                    file_id=file_info['file_id'],
                    filename=file_info['filename'],
                    size=file_info['size'],
                    hash=file_info['hash'],
                    owner_peer_id=peer_id,
                    chunks_total=file_info['chunks_total']
                )
            except Exception as e:
                logger.error(f"Error adding file from peer {peer_id}: {e}")
        
        logger.info(f"Updated {len(file_list)} files for peer {peer_id}")
    
    def get_peers_for_file(self, file_id: str) -> List[Dict]:
        """
        Retourne liste peers ayant ce fichier
        
        Args:
            file_id: ID du fichier
        
        Returns:
            List de dicts avec infos peers
        """
        if not self.db:
            return []
        
        # Récupérer chunks du fichier
        chunks = self.db.get_chunks_for_file(file_id)
        
        # Extraire peer_ids uniques
        peer_ids = set()
        for chunk in chunks:
            if 'peer_ids' in chunk:
                peer_ids.update(chunk['peer_ids'])
        
        # Get peer info
        online_peers = self.get_online_peers()
        return [p for p in online_peers if p['peer_id'] in peer_ids]