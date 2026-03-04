"""Handler réseau simplifié pour la GUI"""
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class NetworkHandler:
    """
    Wrapper qui simplifie l'accès aux fonctionnalités réseau pour la GUI.
    Coordonne TCPServer et MessageHandler.
    """
    
    def __init__(self, tcp_server, message_handler):
        """
        Args:
            tcp_server: Instance TCPServer
            message_handler: Instance MessageHandler
        """
        self.tcp_server = tcp_server
        self.message_handler = message_handler
    
    def broadcast_my_files(self, my_peer_id, file_list):
        """
        Broadcast notre liste de fichiers à tous les peers connectés.
        Méthode simplifiée pour la GUI.
        
        Args:
            my_peer_id: Notre peer ID
            file_list: Liste de fichiers à broadcaster
        """
        if not self.tcp_server or not self.message_handler:
            logger.warning("Network components not available for broadcast")
            return
        
        try:
            # Déléguer au message_handler qui connaît le protocole
            self.message_handler.broadcast_my_files(
                self.tcp_server,
                my_peer_id,
                file_list
            )
            logger.info(f"Broadcast initiated: {len(file_list)} files")
        except Exception as e:
            logger.error(f"Error during broadcast: {e}", exc_info=True)
    
    def request_file_list(self, peer_id):
        """
        Demande la liste de fichiers d'un peer spécifique (TODO pour plus tard)
        
        Args:
            peer_id: ID du peer à interroger
        """
        # TODO: Implémenter si besoin
        pass
