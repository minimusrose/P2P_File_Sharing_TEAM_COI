# 🔵 Tâches Personne 1 - Couche Réseau

**Branche:** `feature/network`  
**Responsabilité:** Communication entre peers (UDP discovery + TCP transfer)

---

## 📂 Vos fichiers

- `p2p_file_sharing/network/discovery.py` - Découverte UDP
- `p2p_file_sharing/network/connection.py` - Serveur/Client TCP
- `p2p_file_sharing/network/protocol.py` - Déjà créé (contrats)

---

## 📅 Jour 1: UDP Discovery

### Objectif
Implémenter la découverte de peers via broadcast UDP

### Fichier: `discovery.py`

**Créer le fichier:**
```powershell
New-Item -ItemType File -Path "p2p_file_sharing\network\discovery.py"
code p2p_file_sharing\network\discovery.py
```

**Code complet:**
```python
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
                sock.sendto(
                    json.dumps(message).encode('utf-8'),
                    ('<broadcast>', self.port)
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
```

### Test Jour 1

**Créer `test_discovery.py` à la racine:**
```python
from p2p_file_sharing.network.discovery import UDPDiscovery
import time

def on_peer_found(peer_id, ip, port):
    print(f"✓ Peer trouvé: {peer_id} @ {ip}:{port}")

# Test
discovery = UDPDiscovery("test_peer_1")
discovery.start_listening(on_peer_found)
discovery.start_broadcasting()

print("En attente de peers... (Ctrl+C pour arrêter)")
print("Lancez une 2ème instance dans un autre terminal!")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nArrêt...")
    discovery.stop()
```

**Exécuter:**
```powershell
# Terminal 1
python test_discovery.py

# Terminal 2
python test_discovery.py

# Les deux devraient se découvrir en ~10 secondes
```

### Commit Jour 1

```powershell
git add p2p_file_sharing/network/discovery.py
git commit -m "Implement UDP peer discovery with broadcast"
git push origin feature/network
```

---

## 📅 Jour 2: TCP Server

### Objectif
Créer serveur TCP acceptant connexions multiples

### Fichier: `connection.py` (partie serveur)

**Créer:**
```powershell
New-Item -ItemType File -Path "p2p_file_sharing\network\connection.py"
code p2p_file_sharing\network\connection.py
```

**Code:**
```python
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
        Démarre le serveur
        
        Args:
            message_callback: fonction(peer_id, message_dict) pour gérer messages
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
                sock.settimeout(1.0)  # Timeout pour vérifier self.running
                try:
                    client_sock, addr = sock.accept()
                except socket.timeout:
                    continue
                
                logger.info(f"Connection from {addr}")
                
                # Lancer thread pour gérer ce client
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
        """Gère les messages d'un client"""
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
        Envoie un message à un peer connecté
        
        Args:
            peer_id: ID du peer destination
            message: Dict à envoyer
        
        Returns:
            bool: True si envoyé avec succès
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
        """Arrête le serveur"""
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
```

### Test Jour 2

**Test avec netcat (optionnel):**
```powershell
# Terminal 1: Lancer serveur
python -c "from p2p_file_sharing.network.connection import TCPServer; import time; s = TCPServer(5001); s.start(lambda pid, msg: print(f'Msg: {msg}')); time.sleep(60)"

# Terminal 2: Tester avec telnet ou netcat
# (ou créer un test_tcp_server.py)
```

### Commit Jour 2

```powershell
git add p2p_file_sharing/network/connection.py
git commit -m "Add TCP server for peer connections"
git push origin feature/network
```

---

## 📅 Jour 3: TCP Client

### Objectif
Client TCP pour connexions sortantes

### Compléter `connection.py`

**Ajouter à la fin de connection.py:**
```python
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
    
    def send_message(self, message: dict) -> bool:
        """
        Envoie un message
        
        Args:
            message: Dict à envoyer (doit avoir 'type', 'peer_id', 'data')
        
        Returns:
            bool: True si envoyé
        """
        if not self.connected:
            logger.warning("Not connected")
            return False
        
        try:
            data = json.dumps(message).encode('utf-8')
            size = len(data).to_bytes(4, 'big')
            self.sock.sendall(size + data)
            logger.debug(f"Message sent: {message['type']}")
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
```

### Test Jour 3 - Test intégration complet

**Créer `test_tcp_full.py`:**
```python
from p2p_file_sharing.network.connection import TCPServer, TCPClient
from p2p_file_sharing.network.protocol import create_message, MessageType
import time
import threading

def test_server():
    """Fonction pour le serveur"""
    def on_message(peer_id, message):
        print(f"✓ Serveur reçu de {peer_id}: {message['type']}")
    
    server = TCPServer(5001)
    server.start(on_message)
    
    print("Serveur démarré, en attente...")
    time.sleep(20)
    server.stop()

def test_client():
    """Fonction pour le client"""
    time.sleep(2)  # Attendre que serveur démarre
    
    client = TCPClient()
    if client.connect('127.0.0.1', 5001):
        print("✓ Client connecté")
        
        # Envoyer message
        msg = {
            "type": MessageType.ANNOUNCE,
            "peer_id": "test_client",
            "data": {"message": "Hello from client!"}
        }
        client.send_message(msg)
        print("✓ Message envoyé")
        
        time.sleep(1)
        client.close()
    else:
        print("✗ Échec connexion")

# Lancer les deux
print("Test TCP Server + Client")
print("-" * 40)

server_thread = threading.Thread(target=test_server)
client_thread = threading.Thread(target=test_client)

server_thread.start()
client_thread.start()

server_thread.join()
client_thread.join()

print("-" * 40)
print("Test terminé!")
```

**Exécuter:**
```powershell
python test_tcp_full.py
# Devrait afficher:
# ✓ Client connecté
# ✓ Message envoyé
# ✓ Serveur reçu de test_client: ANNOUNCE
```

### Commit Jour 3

```powershell
git add p2p_file_sharing/network/connection.py
git commit -m "Add TCP client and complete network layer"
git push origin feature/network
```

---

## 🔀 Fin Jour 3: Créer Pull Request

**Sur GitHub.com:**
```
1. Aller sur le repository
2. Cliquer "Pull requests" → "New pull request"
3. Base: main ← Compare: feature/network
4. Titre: "Network layer: UDP discovery + TCP communication"
5. Description:
   
   Implémente la couche réseau complète:
   - UDP broadcast pour découverte de peers
   - TCP serveur multi-client
   - TCP client pour connexions sortantes
   - Tests inclus et fonctionnels
   
6. Create pull request
7. Attendre review de Personne 3 (Integration Lead)
```

---

## 📊 Checklist Jours 1-3

- [ ] `discovery.py` implémenté et testé
- [ ] `connection.py` TCPServer fonctionnel
- [ ] `connection.py` TCPClient fonctionnel
- [ ] Tests passent (discovery + TCP)
- [ ] Code committé et pushé
- [ ] Pull Request créée
- [ ] Pas de print() debug (logger uniquement)
- [ ] Docstrings présentes
- [ ] Gestion erreurs avec try/except

---

## 💡 Conseils

- **Logger partout:** Facilite debug pendant intégration
- **Threads daemon:** Permet arrêt propre avec Ctrl+C
- **Ports:** UDP 5000, TCP 5001 (configurable)
- **Messages:** Toujours format: taille (4 bytes) + JSON
- **Tests:** Tester avec 2 instances en parallèle
- **Git:** Commit au moins 2-3 fois par jour

---

## 🆘 Problèmes courants

### "Address already in use"

**Solution:**
```powershell
# Tuer processus utilisant le port
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Firewall bloque

**Windows Firewall:**
```powershell
# Autoriser Python
New-NetFirewallRule -DisplayName "Python P2P" -Direction Inbound -Program "C:\Path\To\python.exe" -Action Allow
```

### Broadcast ne fonctionne pas

- Vérifier réseau local (même subnet)
- Tester avec IP directe d'abord
- Logs avec `logger.debug()`

---

**Prochaine étape:** Attendre fin jour 3, puis voir [INTEGRATION.md](INTEGRATION.md)
