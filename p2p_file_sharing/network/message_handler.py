"""Gestion des messages reçus"""
from .protocol import MessageType
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class MessageHandler:
    """Route les messages vers les handlers appropriés"""

    def __init__(self, peer_manager, file_manager):
        """
        Args:
            peer_manager: Gestionnaire de peers
            file_manager: Gestionnaire de fichiers
        """
        self.peer_manager = peer_manager
        self.file_manager = file_manager
        self.tcp_server = None  # sera injecté par main.py une fois créé

    def handle_message(self, sender_peer_id, message):
        """
        Route un message vers le bon handler

        Args:
            sender_peer_id: ID du peer émetteur
            message: Dict avec 'type', 'peer_id', 'data'
        """
        msg_type = message.get("type")

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

        if not hasattr(self.file_manager, "get_my_file_list"):
            logger.error("FileManager does not support get_my_file_list()")
            return

        # Récupérer nos fichiers via le file_manager
        my_files = self.file_manager.get_my_file_list()

        # Créer le message de réponse
        from .protocol import create_message, MessageType as _MessageType

        response = create_message(
            _MessageType.FILE_LIST_RESPONSE,
            self.peer_manager.local_peer_id,
            {"files": my_files},
        )

        # Renvoyer spécifiquement au demandeur via le TCPServer si disponible
        if self.tcp_server:
            self.tcp_server.send_to_peer(sender_peer_id, response)
        else:
            logger.warning("No TCP server set on MessageHandler; cannot reply")

    def _handle_file_list_response(self, sender_peer_id, message):
        """Peer envoie sa liste de fichiers"""
        file_list = message['data'].get('files', [])
        logger.info(f"Received FILE_LIST_RESPONSE: {len(file_list)} files from {sender_peer_id}")
        
        if not file_list:
            logger.warning(f"Peer {sender_peer_id} sent empty file list")
        else:
            logger.debug(f"Files from {sender_peer_id}: {[f.get('filename', 'unknown') for f in file_list]}")
        
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
            tcp_server: Instance TCPServer (peut être None)
            my_peer_id: Notre ID
            file_list: Liste fichiers à envoyer
        """
        from .protocol import create_message, MessageType
        from .connection import TCPClient
        
        message = create_message(
            MessageType.FILE_LIST_RESPONSE,
            my_peer_id,
            {"files": file_list},
        )
        
        # Récupérer tous les peers actifs de la base de données
        if not self.peer_manager or not hasattr(self.peer_manager, 'get_online_peers'):
            logger.warning("Cannot broadcast: peer_manager not available")
            return
        
        online_peers = self.peer_manager.get_online_peers()
        sent_count = 0
        
        for peer_data in online_peers:
            peer_id = peer_data['peer_id']
            ip = peer_data['ip']
            port = peer_data['port']
            
            # Option 1: Utiliser connexion existante si disponible
            if tcp_server and peer_id in tcp_server.clients:
                try:
                    tcp_server.send_to_peer(peer_id, message)
                    sent_count += 1
                    logger.debug(f"Sent via persistent connection to {peer_id}")
                    continue
                except Exception as e:
                    logger.warning(f"Failed to send via persistent connection: {e}")
            
            # Option 2: Créer connexion temporaire pour envoyer
            client = TCPClient()
            try:
                if client.connect(ip, port):
                    if client.send_message(message):
                        sent_count += 1
                        logger.debug(f"Sent via new connection to {peer_id} at {ip}:{port}")
                    client.close()
            except Exception as e:
                logger.error(f"Failed to broadcast to {peer_id} at {ip}:{port}: {e}")
        
        logger.info(f"Broadcasted {len(file_list)} files to {sent_count}/{len(online_peers)} peers")