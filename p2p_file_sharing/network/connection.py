"""Module de connexion TCP entre peers"""
import socket
import threading
import json
from ..utils.config import TRANSFER_PORT_START
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class TCPServer:
    """Serveur TCP acceptant connexions de peers"""
    
    def __init__(self, port: int = TRANSFER_PORT_START):
        self.port = port
        self.running = False
        self.server_thread = None
        self.clients = {}  # peer_id -> socket
        self.message_callback = None
        
    def start(self, message_callback):
        """
        D├®marre le serveur
        
        Args:
            message_callback: fonction(peer_id, message_dict) pour g├®rer messages
        """
        self.running = True
        self.message_callback = message_callback
        self.server_thread = threading.Thread(target=self._accept_loop)
        self.server_thread.daemon = True
        self.server_thread.start()
        logger.info(f"TCP Server started on port {self.port}")
    
    def _accept_loop(self):
        """Accepte les connexions entrantes"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            sock.bind(('0.0.0.0', self.port))
            sock.listen(5)
            logger.info(f"TCP Server listening on 0.0.0.0:{self.port}")
        except Exception as e:
            logger.error(f"Failed to start TCP server: {e}")
            return
        
        while self.running:
            try:
                sock.settimeout(1.0)  # Timeout pour v├®rifier self.running
                try:
                    client_sock, addr = sock.accept()
                except socket.timeout:
                    continue
                
                logger.info(f"Connection from {addr}")
                
                # Lancer thread pour g├®rer ce client
                t = threading.Thread(
                    target=self._handle_client,
                    args=(client_sock, addr)
                )
                t.daemon = True
                t.start()
                
            except Exception as e:
                if self.running:
                    logger.error(f"Accept error: {e}")
        
        sock.close()
        logger.info("TCP Server stopped")
    
    def _handle_client(self, sock, addr):
        """G├¿re les messages d'un client"""
        peer_id = None
        
        try:
            while self.running:
                # Recevoir taille du message (4 bytes)
                size_data = sock.recv(4)
                if not size_data:
                    break
                
                msg_size = int.from_bytes(size_data, 'big')
                
                # Recevoir message complet
                data = b''
                while len(data) < msg_size:
                    chunk = sock.recv(min(msg_size - len(data), 4096))
                    if not chunk:
                        break
                    data += chunk
                
                if len(data) < msg_size:
                    break
                
                # Parser message
                message = json.loads(data.decode('utf-8'))
                peer_id = message.get('peer_id')
                
                if peer_id:
                    self.clients[peer_id] = sock
                    if self.message_callback:
                        self.message_callback(peer_id, message)
                    
        except Exception as e:
            logger.error(f"Client handler error: {e}")
        finally:
            if peer_id and peer_id in self.clients:
                del self.clients[peer_id]
            sock.close()
            logger.info(f"Client disconnected: {addr}")
    
    def send_to_peer(self, peer_id: str, message: dict) -> bool:
        """
        Envoie un message ├á un peer connect├®
        
        Args:
            peer_id: ID du peer destination
            message: Dict ├á envoyer
        
        Returns:
            bool: True si envoy├® avec succ├¿s
        """
        if peer_id not in self.clients:
            logger.warning(f"Peer {peer_id} not connected")
            return False
        
        try:
            data = json.dumps(message).encode('utf-8')
            size = len(data).to_bytes(4, 'big')
            
            sock = self.clients[peer_id]
            sock.sendall(size + data)
            logger.debug(f"Message sent to {peer_id}: {message['type']}")
            return True
        except Exception as e:
            logger.error(f"Send error to {peer_id}: {e}")
            if peer_id in self.clients:
                del self.clients[peer_id]
            return False
    
    def stop(self):
        """Arr├¬te le serveur"""
        logger.info("Stopping TCP Server...")
        self.running = False
        
        # Fermer toutes les connexions
        for sock in list(self.clients.values()):
            try:
                sock.close()
            except:
                pass
        self.clients.clear()
        
        if self.server_thread:
            self.server_thread.join(timeout=2)


class TCPClient:
    """Client TCP pour se connecter à un peer"""
    
    def __init__(self):
        self.sock = None
        self.connected = False
        self.peer_id = None
        
    def connect(self, ip: str, port: int) -> bool:
        """
        Connecte à un peer
        
        Args:
            ip: Adresse IP du peer
            port: Port TCP

        Returns:
            bool: True si connexion réussie
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ip, port))
            self.connected = True
            logger.info(f"Connected to {ip}:{port}")
            return True
        except Exception as e:
            logger.error(f"Connection failed to {ip}:{port}: {e}")
            return False
    
    def send_message(self, message) -> bool:
        """
        Envoie un message
        
        Args:
            message: Dict ou bytes à envoyer
        
        Returns:
            bool: True si envoyé
        """
        if not self.connected:
            logger.warning("Not connected")
            return False
        
        try:
            # Accepte dict ou bytes
            if isinstance(message, bytes):
                data = message
                msg_type = "bytes"
            else:
                data = json.dumps(message).encode('utf-8')
                msg_type = message.get('type', 'unknown')
            
            size = len(data).to_bytes(4, 'big')
            self.sock.sendall(size + data)
            logger.debug(f"Message sent: {msg_type}")
            return True
        except Exception as e:
            logger.error(f"Send error: {e}")
            self.connected = False
            return False
    
    def receive_message(self, timeout=None) -> dict:
        """
        Reçoit un message (bloquant avec timeout optionnel)
        
        Args:
            timeout: Secondes max (None = infini)
        
        Returns:
            dict: Message reçu ou None si erreur/timeout
        """
        if not self.connected:
            return None
        
        try:
            if timeout:
                self.sock.settimeout(timeout)
            
            # Recevoir taille
            size_data = self.sock.recv(4)
            if not size_data:
                return None
            
            msg_size = int.from_bytes(size_data, 'big')
            
            # Recevoir message
            data = b''
            while len(data) < msg_size:
                chunk = self.sock.recv(min(msg_size - len(data), 4096))
                if not chunk:
                    break
                data += chunk
            
            if len(data) < msg_size:
                return None
            
            return json.loads(data.decode('utf-8'))
            
        except socket.timeout:
            logger.debug("Receive timeout")
            return None
        except Exception as e:
            logger.error(f"Receive error: {e}")
            self.connected = False
            return None
    
    def close(self):
        """Ferme la connexion"""
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
            self.connected = False
            logger.info("Connection closed")