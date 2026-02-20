"""Module de découverte de peers via UDP broadcast"""
import socket
import threading
import time
import json
from ..utils.config import DISCOVERY_PORT, UDP_BROADCAST_INTERVAL
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class UDPDiscovery:
    """Gère la découverte de peers via UDP broadcast

    Parameters
    - peer_id: identifiant local
    - port: port UDP pour discovery
    - broadcast_addr: adresse de broadcast à utiliser (par défaut '<broadcast>')
    """

    def __init__(self, peer_id: str, port: int = DISCOVERY_PORT, broadcast_addr: str = '<broadcast>'):
        self.peer_id = peer_id
        self.port = port
        self.broadcast_addr = broadcast_addr
        self.running = False
        self.broadcast_thread = None
        self.listen_thread = None
        
    def start_broadcasting(self):
        """Lance l'envoi périodique d'annonces"""
        self.running = True
        self.broadcast_thread = threading.Thread(target=self._broadcast_loop)
        self.broadcast_thread.daemon = True
        self.broadcast_thread.start()
        logger.info(f"Broadcasting started on port {self.port}")
        
    def _broadcast_loop(self):
        """Boucle d'envoi d'annonces ANNOUNCE"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        while self.running:
            message = {
                "type": "ANNOUNCE",
                "peer_id": self.peer_id,
                "port": self.port + 1  # TCP port = UDP port + 1
            }
            try:
                target = self.broadcast_addr
                sock.sendto(
                    json.dumps(message).encode('utf-8'),
                    (target, self.port)
                )
                logger.debug(f"Broadcast sent: {self.peer_id}")
            except Exception as e:
                logger.error(f"Broadcast error: {e}")
            
            time.sleep(UDP_BROADCAST_INTERVAL)
        
        sock.close()
        logger.info("Broadcasting stopped")
    
    def start_listening(self, callback):
        """
        Lance l'écoute d'annonces
        
        Args:
            callback: fonction(peer_id, ip, port) appelée quand peer découvert
        """
        self.running = True
        self.listen_thread = threading.Thread(
            target=self._listen_loop,
            args=(callback,)
        )
        self.listen_thread.daemon = True
        self.listen_thread.start()
        logger.info(f"Listening for peers on port {self.port}")
    
    def _listen_loop(self, callback):
        """Boucle d'écoute UDP"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(('', self.port))
        except Exception:
            # Fallback: try binding to localhost
            sock.bind(('127.0.0.1', self.port))
        
        while self.running:
            try:
                data, addr = sock.recvfrom(1024)
                message = json.loads(data.decode('utf-8'))
                
                if message['type'] == 'ANNOUNCE':
                    peer_id = message['peer_id']
                    if peer_id != self.peer_id:  # Pas nous-mêmes
                        callback(peer_id, addr[0], message['port'])
                        logger.info(f"Peer discovered: {peer_id} at {addr[0]}")
                        
            except Exception as e:
                if self.running:  # Ignorer erreurs si on s'arrête
                    logger.error(f"Listen error: {e}")
        
        sock.close()
        logger.info("Listening stopped")
    
    def stop(self):
        """Arrête discovery (broadcast + listening)"""
        logger.info("Stopping discovery...")
        self.running = False
        
        # Attendre arrêt threads
        if self.broadcast_thread:
            self.broadcast_thread.join(timeout=2)
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
