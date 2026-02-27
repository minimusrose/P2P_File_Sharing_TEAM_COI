"""Gestion des messages reçus"""
from .protocol import MessageType
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class MessageHandler:
    """Route les messages vers les handlers appropriés"""
    
    def __init__(self, peer_manager, file_manager):
        self.peer_manager = peer_manager
        self.file_manager = file_manager
    
    def handle_message(self, sender_peer_id, message):
        """
        Route un message vers le bon handler
        
        Args:
            sender_peer_id: ID du peer émetteur
            message: Dict avec 'type', 'peer_id', 'data'
        """
        msg_type = message.get('type')
        
        if msg_type == MessageType.FILE_LIST_REQUEST:
            return self._handle_file_list_request(sender_peer_id, message)
        elif msg_type == MessageType.FILE_LIST_RESPONSE:
            return self._handle_file_list_response(sender_peer_id, message)
        elif msg_type == MessageType.CHUNK_REQUEST:
            return self._handle_chunk_request(sender_peer_id, message)
        elif msg_type == MessageType.CHUNK_DATA:
            return self._handle_chunk_data(sender_peer_id, message)
        else:
            logger.warning(f"Unknown message type: {msg_type}")
    
    def _handle_file_list_request(self, sender_peer_id, message):
        """Peer demande notre liste de fichiers"""
        logger.info(f"File list requested by {sender_peer_id}")
        # TODO: Envoyer notre liste
    
    def _handle_file_list_response(self, sender_peer_id, message):
        """Peer envoie sa liste de fichiers"""
        file_list = message['data'].get('files', [])
        logger.info(f"Received {len(file_list)} files from {sender_peer_id}")
        self.peer_manager.update_peer_files(sender_peer_id, file_list)
    
    def _handle_chunk_request(self, sender_peer_id, message):
        """Peer demande un chunk"""
        logger.info(f"Chunk requested by {sender_peer_id}")
        # TODO: Envoyer chunk
    
    def _handle_chunk_data(self, sender_peer_id, message):
        """Peer envoie un chunk"""
        logger.info(f"Chunk received from {sender_peer_id}")
        # TODO: Stocker chunk

    def broadcast_my_files(self, tcp_server, my_peer_id, file_list):
        """
        Broadcast notre liste de fichiers à tous les peers
        
        Args:
            tcp_server: Instance TCPServer
            my_peer_id: Notre ID
            file_list: Liste fichiers à envoyer
        """
        from .protocol import create_message, MessageType
        
        message = create_message(
            MessageType.FILE_LIST_RESPONSE,
            my_peer_id,
            {"files": file_list},
        )
        # Envoyer à tous les peers connectés
        for peer_id in list(tcp_server.clients.keys()):
            tcp_server.send_to_peer(peer_id, message)
        
        logger.info(f"Broadcasted {len(file_list)} files to peers")