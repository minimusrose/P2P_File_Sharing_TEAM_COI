"""Module de découverte de peers via UDP broadcast"""
import socket
import threading
import time
import json
from ..utils.config import DISCOVERY_PORT, UDP_BROADCAST_INTERVAL
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class UDPDiscovery:
    """Gère la découverte de peers via UDP broadcast"""
    
    def __init__(self, peer_id: str, port: int = DISCOVERY_PORT):
        self.peer_id = peer_id
        self.port = port
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
        
    def _get_broadcast_address(self):
        """Calcule l'adresse broadcast du réseau local actif"""
        try:
            # Obtenir l'IP locale (celle qui serait utilisée pour connexion externe)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            
            # Calculer l'adresse broadcast du sous-réseau (assume /24)
            ip_parts = local_ip.split('.')
            broadcast = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.255"
            
            logger.info(f"Using local IP: {local_ip}, broadcast: {broadcast}")
            return broadcast
        except Exception as e:
            logger.warning(f"Could not determine broadcast address: {e}, using default")
            return '<broadcast>'  # Fallback
    
    def _broadcast_loop(self):
        """Boucle d'envoi d'annonces ANNOUNCE"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Utiliser '<broadcast>' pour compatibilité maximale
        # Note: '<broadcast>' est plus fiable que de calculer l'adresse broadcast spécifique
        # car il fonctionne sur tous les réseaux sans dépendre du masque de sous-réseau
        broadcast_addr = '<broadcast>'
        logger.info(f"Broadcasting to: {broadcast_addr}:{self.port}")
        
        while self.running:
            message = {
                "type": "ANNOUNCE",
                "peer_id": self.peer_id,
                "port": self.port + 1  # TCP port = UDP port + 1
            }
            try:
                sock.sendto(
                    json.dumps(message).encode('utf-8'),
                    (broadcast_addr, self.port)
                )
                logger.debug(f"Broadcast sent to {broadcast_addr}: {self.peer_id}")
            except Exception as e:
                logger.error(f"Broadcast error to {broadcast_addr}: {e}")
            
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
        sock.bind(('', self.port))
        
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