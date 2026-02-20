# 📝 Contrats d'Interface - Jour 1 Après-midi

**⚠️ OBLIGATOIRE avant de commencer à coder !**

**Qui:** Tous les 3 ensemble  
**Durée:** 1-2 heures  
**Objectif:** Définir les signatures de fonctions pour que chacun puisse développer en parallèle

---

## 🎯 Pourquoi c'est important

- ✅ Permet développement en parallèle sans attendre
- ✅ Évite incompatibilités lors de l'intégration
- ✅ Chacun sait exactement ce que font les autres modules
- ✅ Réduit drastiquement les conflits Git

---

## 📋 Fichiers à créer ensemble

### 1. `p2p_file_sharing/utils/config.py` (Personne 3 écrit, tous valident)

**PowerShell:**
```powershell
New-Item -ItemType File -Path "p2p_file_sharing\utils\config.py"
code p2p_file_sharing\utils\config.py
```

**Contenu:**
```python
"""Configuration globale du système P2P"""
import os
from pathlib import Path
import platform

# === Chemins cross-platform ===
HOME = Path.home()
APP_DATA_DIR = HOME / ".p2p_fileshare"
APP_DATA_DIR.mkdir(exist_ok=True)

DOWNLOAD_DIR = APP_DATA_DIR / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)

SHARED_FILES_DIR = APP_DATA_DIR / "shared"
SHARED_FILES_DIR.mkdir(exist_ok=True)

DATABASE_PATH = APP_DATA_DIR / "p2p.db"
LOG_FILE = APP_DATA_DIR / "p2p.log"

# === Réseau ===
DISCOVERY_PORT = 5000
TRANSFER_PORT_START = 5001
UDP_BROADCAST_INTERVAL = 10  # secondes
PEER_TIMEOUT = 30  # secondes sans heartbeat

# === Fichiers ===
CHUNK_SIZE = 256 * 1024  # 256 KB
MAX_PARALLEL_DOWNLOADS = 5

# === Système ===
OS_TYPE = platform.system()  # 'Windows', 'Linux', 'Darwin'
```

---

### 2. `p2p_file_sharing/utils/logger.py` (Personne 3)

**PowerShell:**
```powershell
New-Item -ItemType File -Path "p2p_file_sharing\utils\logger.py"
code p2p_file_sharing\utils\logger.py
```

**Contenu:**
```python
"""Configuration du système de logs"""
import logging
from .config import LOG_FILE

def setup_logger(name='P2P'):
    """Configure le logger pour l'application"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Console handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console)
    logger.addHandler(file_handler)
    
    return logger
```

---

### 3. `p2p_file_sharing/network/protocol.py` (Personne 1 écrit, tous valident)

**PowerShell:**
```powershell
New-Item -ItemType File -Path "p2p_file_sharing\network\protocol.py"
code p2p_file_sharing\network\protocol.py
```

**Contenu:**
```python
"""Protocole de communication entre peers"""
import json
from typing import Dict, Any

class MessageType:
    """Types de messages échangés"""
    ANNOUNCE = "ANNOUNCE"
    FILE_LIST_REQUEST = "FILE_LIST_REQUEST"
    FILE_LIST_RESPONSE = "FILE_LIST_RESPONSE"
    CHUNK_REQUEST = "CHUNK_REQUEST"
    CHUNK_DATA = "CHUNK_DATA"
    GOODBYE = "GOODBYE"

def create_message(msg_type: str, peer_id: str, data: Dict[str, Any]) -> bytes:
    """
    Crée un message JSON encodé en bytes
    
    Args:
        msg_type: Type de message (voir MessageType)
        peer_id: ID du peer émetteur
        data: Données du message (dict)
    
    Returns:
        bytes: Message encodé prêt à envoyer
    """
    message = {
        "type": msg_type,
        "peer_id": peer_id,
        "data": data
    }
    return json.dumps(message).encode('utf-8')

def parse_message(raw_data: bytes) -> Dict[str, Any]:
    """
    Parse un message reçu
    
    Args:
        raw_data: Bytes reçus du réseau
    
    Returns:
        dict: Message parsé avec 'type', 'peer_id', 'data'
    """
    return json.loads(raw_data.decode('utf-8'))
```

---

### 4. `p2p_file_sharing/core/peer_manager.py` (Personne 2 écrit, tous valident)

**PowerShell:**
```powershell
New-Item -ItemType File -Path "p2p_file_sharing\core\peer_manager.py"
code p2p_file_sharing\core\peer_manager.py
```

**Contenu:**
```python
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
```

---

### 5. `p2p_file_sharing/core/file_manager.py` (Personne 2)

**PowerShell:**
```powershell
New-Item -ItemType File -Path "p2p_file_sharing\core\file_manager.py"
code p2p_file_sharing\core\file_manager.py
```

**Contenu:**
```python
"""Gestionnaire de fichiers et chunks"""
from pathlib import Path
from typing import Callable, List, Dict
from ..utils.config import CHUNK_SIZE
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class FileManager:
    """Gère le chunking et l'assemblage de fichiers"""
    
    def __init__(self, database):
        """
        Initialise le gestionnaire de fichiers
        
        Args:
            database: Instance de Database
        """
        self.db = database
    
    def add_shared_file(self, filepath: str) -> str:
        """
        Ajoute un fichier à partager
        
        Args:
            filepath: Chemin complet du fichier
        
        Returns:
            str: file_id unique généré
        """
        return ""  # À implémenter
    
    def get_shared_files(self) -> List[Dict]:
        """
        Retourne la liste des fichiers partagés localement
        
        Returns:
            List de dicts avec file_id, filename, size, hash
        """
        return []
    
    def chunk_file(self, filepath: str) -> List[Dict]:
        """
        Découpe un fichier en chunks
        
        Args:
            filepath: Chemin du fichier
        
        Returns:
            List de dicts: [
                {'chunk_index': 0, 'data': bytes, 'hash': 'sha256...'},
                ...
            ]
        """
        return []
    
    def download_file(self, file_id: str, save_path: str, 
                      progress_callback: Callable[[int], None]) -> None:
        """
        Télécharge un fichier depuis les peers
        
        Args:
            file_id: ID du fichier à télécharger
            save_path: Où sauvegarder le fichier
            progress_callback: Fonction appelée avec pourcentage (0-100)
        """
        pass
    
    def assemble_chunks(self, chunks: List[Dict], output_path: str) -> bool:
        """
        Réassemble les chunks en fichier
        
        Args:
            chunks: Liste de chunks avec 'chunk_index', 'data', 'hash'
            output_path: Chemin du fichier de sortie
        
        Returns:
            bool: True si succès
        """
        return False
```

---

### 6. `p2p_file_sharing/gui/main_window.py` (Personne 3)

**PowerShell:**
```powershell
New-Item -ItemType File -Path "p2p_file_sharing\gui\main_window.py"
code p2p_file_sharing\gui\main_window.py
```

**Contenu:**
```python
"""Fenêtre principale de l'application"""
import tkinter as tk
from tkinter import ttk
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class MainWindow:
    """Interface graphique principale"""
    
    def __init__(self, peer_manager=None, file_manager=None, network_handler=None):
        """
        Initialise la fenêtre principale
        
        Args:
            peer_manager: Instance de PeerManager
            file_manager: Instance de FileManager
            network_handler: Instance du gestionnaire réseau
        """
        self.peer_manager = peer_manager
        self.file_manager = file_manager
        self.network = network_handler
        
        self.root = tk.Tk()
        self.root.title("P2P File Sharing")
        self.root.geometry("800x600")
        
        self._build_ui()
    
    def _build_ui(self):
        """Construit l'interface"""
        pass  # À implémenter
    
    def run(self):
        """Lance la boucle d'événements tkinter"""
        logger.info("Starting GUI main loop")
        self.root.mainloop()
```

---

## 📤 Commit et distribution (Personne 3)

**Tous ces fichiers vont sur la branche `main` pour que tout le monde les ait:**

**PowerShell:**
```powershell
# Retour sur main
git checkout main

# Ajouter tous les fichiers
git add p2p_file_sharing/utils/
git add p2p_file_sharing/network/protocol.py
git add p2p_file_sharing/core/peer_manager.py
git add p2p_file_sharing/core/file_manager.py
git add p2p_file_sharing/gui/main_window.py

# Commit
git commit -m "Add interface contracts and base classes"

# Push
git push origin main
```

---

## 🔄 Récupération par chaque personne

**Personne 1 et 2 font:**

**PowerShell:**
```powershell
# Update main local
git checkout main
git pull origin main

# Merge dans votre branche
git checkout feature/VOTRE_BRANCHE
git merge main

# Vérifier que vous avez les fichiers
ls p2p_file_sharing\utils\
ls p2p_file_sharing\network\
ls p2p_file_sharing\core\
ls p2p_file_sharing\gui\
```

---

## ✅ Validation des contrats

**Test que tout compile:**

**PowerShell:**
```powershell
# Chacun teste sur sa branche
python -c "from p2p_file_sharing.utils.config import CHUNK_SIZE; print(f'Chunk size: {CHUNK_SIZE}')"
# Doit afficher: Chunk size: 262144

python -c "from p2p_file_sharing.utils.logger import setup_logger; logger = setup_logger(); logger.info('Test OK')"
# Doit afficher un log

python -c "from p2p_file_sharing.network.protocol import MessageType; print(MessageType.ANNOUNCE)"
# Doit afficher: ANNOUNCE

python -c "from p2p_file_sharing.core.peer_manager import PeerManager; print('PeerManager OK')"
# Doit afficher: PeerManager OK

python -c "from p2p_file_sharing.core.file_manager import FileManager; print('FileManager OK')"
# Doit afficher: FileManager OK

python -c "from p2p_file_sharing.gui.main_window import MainWindow; print('MainWindow OK')"
# Doit afficher: MainWindow OK
```

Si tous ces tests passent ✅ → Les contrats sont validés !

---

## 📋 Résumé des interfaces

### Network → Core

**Personne 1 appellera:**
```python
peer_manager.handle_peer_announce(peer_id, ip, port)
```

**Quand:** Un peer est découvert via UDP

---

### Core → Network

**Personne 2 utilisera:**
```python
# Protocole messages
from network.protocol import create_message, MessageType

message = create_message(MessageType.FILE_LIST_REQUEST, my_peer_id, {})
# Puis envoyer via TCP
```

---

### GUI → Core

**Personne 3 appellera:**
```python
# Liste des peers
peers = peer_manager.get_online_peers()

# Partager fichier
file_id = file_manager.add_shared_file(filepath)

# Télécharger
def progress(percent):
    # Update progress bar
    pass

file_manager.download_file(file_id, save_path, progress)
```

---

### Core → GUI

**Personne 2 fournira:**
```python
# Callbacks possibles (à discuter si besoin)
# Par exemple: on_file_added, on_peer_connected, etc.
```

---

## 🎯 Checklist finale

**Avant de commencer le développement:**

- [ ] Tous les fichiers d'interface créés
- [ ] Committés sur `main`
- [ ] Chaque personne a pullé et mergé dans sa branche
- [ ] Tests d'import passent (voir section Validation)
- [ ] Tout le monde comprend les signatures
- [ ] Questions clarifiées

**Si une question se pose:**  
→ Ne pas hésiter, il vaut mieux clarifier maintenant que découvrir un problème jour 4 !

---

## 💡 Conseils

- **Respecter les signatures:** Ne pas changer sans prévenir les autres
- **Ajouter des paramètres:** OK, mais avec valeurs par défaut
- **Documentez:** Docstrings claires (déjà faites ci-dessus)
- **Types hints:** Utiliser typing (List, Dict, etc.)
- **Exceptions:** Discuter des exceptions possibles

---

## 🚀 Prochaines étapes

**Maintenant que les contrats sont définis, chacun peut travailler en parallèle:**

- **Personne 1:** Lire [TACHES_PERSONNE1.md](TACHES_PERSONNE1.md)
- **Personne 2:** Lire [TACHES_PERSONNE2.md](TACHES_PERSONNE2.md)
- **Personne 3:** Lire [TACHES_PERSONNE3.md](TACHES_PERSONNE3.md)

**Durée développement parallèle:** Jours 1-3

**Rendez-vous:** Fin jour 3 pour le premier merge !

---

**Contrats validés ✅ → Commencer le développement !**
