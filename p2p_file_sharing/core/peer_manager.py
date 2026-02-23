"""Gestionnaire de peers"""
from typing import List, Dict, Callable
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class PeerManager:
    """Gère la liste des peers et leur état"""
    
    def __init__(self, database):
        """
        Initialise le gestionnaire de peers
        
        Args:
            database: Instance de Database pour persistance
        """
        self.db = database
        self.local_peer_id = None
        self.peers = {}  # peer_id -> {ip, port, last_seen, files}
    
    def set_local_peer_id(self, peer_id: str):
        """Définit l'ID du peer local"""
        self.local_peer_id = peer_id
        logger.info(f"Local peer ID set: {peer_id}")
    
    def add_peer(self, peer_id: str, ip: str, port: int) -> None:
        """
        Ajoute ou met à jour un peer
        
        Args:
            peer_id: ID unique du peer
            ip: Adresse IP
            port: Port TCP
        """
        pass  # À implémenter par Personne 2
    
    def remove_peer(self, peer_id: str) -> None:
        """Supprime un peer déconnecté"""
        pass
    
    def get_online_peers(self, timeout: int = 30) -> List[Dict]:
        """
        Retourne la liste des peers en ligne
        
        Args:
            timeout: Secondes max depuis dernier heartbeat
        
        Returns:
            List de dicts: [{'peer_id': ..., 'ip': ..., 'port': ...}, ...]
        """
        return []
    
    def update_peer_files(self, peer_id: str, file_list: List[Dict]) -> None:
        """
        Met à jour la liste des fichiers d'un peer
        
        Args:
            peer_id: ID du peer
            file_list: Liste de dicts avec file_id, filename, size, etc.
        """
        pass
    
    def handle_peer_announce(self, peer_id: str, ip: str, port: int) -> None:
        """
        Callback appelé par network layer lors découverte peer
        
        Args:
            peer_id: ID du peer découvert
            ip: Son IP
            port: Son port
        """
        if peer_id == self.local_peer_id:
            return  # C'est nous, ignorer
        
        logger.info(f"Peer announced: {peer_id} at {ip}:{port}")
        self.add_peer(peer_id, ip, port)
