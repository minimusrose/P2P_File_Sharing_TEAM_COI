# 🟢 Tâches Personne 2 - Logique Métier

**Branche:** `feature/core`  
**Responsabilité:** Gestion fichiers (chunking), base de données, gestion peers

---

## 📂 Vos fichiers

- `p2p_file_sharing/core/file_manager.py` - Chunking & assemblage
- `p2p_file_sharing/core/database.py` - SQLite
- `p2p_file_sharing/core/peer_manager.py` - Déjà créé (contrats)

---

## 📅 Jour 1: File Chunking

### Objectif
Implémenter la fragmentation et réassemblage de fichiers avec vérification hash

### Compléter `file_manager.py`

**Ouvrir:**
```powershell
code p2p_file_sharing\core\file_manager.py
```

**Compléter le code:**
```python
"""Gestionnaire de fichiers et chunks"""
from pathlib import Path
import hashlib
from typing import List, Dict, Callable
from ..utils.config import CHUNK_SIZE, SHARED_FILES_DIR
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class FileManager:
    """Gère le chunking et l'assemblage de fichiers"""
    
    def __init__(self, database=None):
        self.db = database
        self.shared_files = {}  # file_id -> filepath
    
    def calculate_file_hash(self, filepath: str) -> str:
        """
        Calcule hash SHA256 du fichier complet
        
        Args:
            filepath: Chemin du fichier
        
        Returns:
            str: Hash hexadécimal
        """
        sha256 = hashlib.sha256()
        
        try:
            with open(filepath, 'rb') as f:
                while True:
                    data = f.read(8192)
                    if not data:
                        break
                    sha256.update(data)
            
            return sha256.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {filepath}: {e}")
            return ""
    
    def chunk_file(self, filepath: str) -> List[Dict]:
        """
        Découpe fichier en chunks de CHUNK_SIZE
        
        Args:
            filepath: Chemin du fichier à chunker
        
        Returns:
            List de dicts: [
                {'chunk_index': 0, 'data': bytes, 'hash': 'sha256...'},
                ...
            ]
        """
        chunks = []
        chunk_index = 0
        
        try:
            with open(filepath, 'rb') as f:
                while True:
                    data = f.read(CHUNK_SIZE)
                    if not data:
                        break
                    
                    chunk_hash = hashlib.sha256(data).hexdigest()
                    chunks.append({
                        'chunk_index': chunk_index,
                        'data': data,
                        'hash': chunk_hash,
                        'size': len(data)
                    })
                    chunk_index += 1
            
            logger.info(f"File chunked: {filepath} -> {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Error chunking file {filepath}: {e}")
            return []
    
    def assemble_chunks(self, chunks: List[Dict], output_path: str) -> bool:
        """
        Réassemble les chunks en fichier
        
        Args:
            chunks: Liste de chunks avec 'chunk_index', 'data', 'hash'
            output_path: Chemin du fichier de sortie
        
        Returns:
            bool: True si succès
        """
        try:
            # Trier par index
            sorted_chunks = sorted(chunks, key=lambda x: x['chunk_index'])
            
            # Vérifier continuité
            for i, chunk in enumerate(sorted_chunks):
                if chunk['chunk_index'] != i:
                    logger.error(f"Missing chunk {i}")
                    return False
            
            # Écrire fichier
            with open(output_path, 'wb') as f:
                for chunk in sorted_chunks:
                    # Vérifier hash si présent
                    if 'hash' in chunk and chunk['hash']:
                        calculated = hashlib.sha256(chunk['data']).hexdigest()
                        if calculated != chunk['hash']:
                            logger.error(f"Chunk {chunk['chunk_index']} hash mismatch!")
                            return False
                    
                    f.write(chunk['data'])
            
            logger.info(f"File reassembled: {output_path} ({len(sorted_chunks)} chunks)")
            return True
            
        except Exception as e:
            logger.error(f"Error assembling chunks: {e}")
            return False
    
    def add_shared_file(self, filepath: str) -> str:
        """
        Ajoute un fichier à partager
        
        Args:
            filepath: Chemin complet du fichier
        
        Returns:
            str: file_id unique
        """
        try:
            path = Path(filepath)
            if not path.exists():
                logger.error(f"File not found: {filepath}")
                return ""
            
            # Générer file_id
            file_id = hashlib.md5(filepath.encode()).hexdigest()[:16]
            
            # Calculer infos
            file_hash = self.calculate_file_hash(filepath)
            file_size = path.stat().st_size
            chunks_total = (file_size // CHUNK_SIZE) + (1 if file_size % CHUNK_SIZE else 0)
            
            # Stocker localement
            self.shared_files[file_id] = filepath
            
            # Ajouter à DB si disponible
            if self.db:
                self.db.add_file(
                    file_id=file_id,
                    filename=path.name,
                    size=file_size,
                    hash=file_hash,
                    owner_peer_id="local",  # Sera mis à jour
                    chunks_total=chunks_total
                )
                self.db.add_local_shared(file_id, filepath)
            
            logger.info(f"Shared file added: {path.name} (ID: {file_id})")
            return file_id
            
        except Exception as e:
            logger.error(f"Error adding shared file: {e}")
            return ""
    
    def get_shared_files(self) -> List[Dict]:
        """Retourne la liste des fichiers partagés localement"""
        if not self.db:
            return []
        
        return self.db.get_local_shared_files()
    
    def download_file(self, file_id: str, save_path: str, 
                      progress_callback: Callable[[int], None]) -> None:
        """
        Télécharge un fichier (sera complété lors de l'intégration)
        
        Args:
            file_id: ID du fichier
            save_path: Où sauvegarder
            progress_callback: Fonction(percent) pour progression
        """
        # TODO: Implémenter lors de l'intégration avec network layer
        logger.info(f"Download requested: {file_id} -> {save_path}")
        pass
```

### Test Jour 1

**Créer `test_chunking.py`:**
```python
from p2p_file_sharing.core.file_manager import FileManager
from pathlib import Path
import os

print("=== Test File Chunking ===\n")

# Créer fichier test 1MB
test_file = "test_1mb.dat"
print(f"Création fichier test: {test_file}...")
with open(test_file, 'wb') as f:
    f.write(os.urandom(1024 * 1024))  # 1MB random
print(f"✓ Fichier créé: 1 MB\n")

fm = FileManager()

# Test 1: Chunking
print("Test 1: Chunking...")
chunks = fm.chunk_file(test_file)
print(f"✓ Chunks créés: {len(chunks)}")
print(f"  Taille attendue: 4 chunks (256KB chacun)")
print(f"  Premier chunk: {len(chunks[0]['data'])} bytes")
print(f"  Hash premier chunk: {chunks[0]['hash'][:16]}...\n")

# Test 2: Hash fichier
print("Test 2: Hash fichier complet...")
hash1 = fm.calculate_file_hash(test_file)
print(f"✓ Hash: {hash1[:32]}...\n")

# Test 3: Réassemblage
print("Test 3: Réassemblage...")
output = "test_reassembled.dat"
success = fm.assemble_chunks(chunks, output)
print(f"✓ Réassemblage: {'OK' if success else 'FAIL'}")

# Vérifier hash
hash2 = fm.calculate_file_hash(output)
print(f"✓ Hash après réassemblage: {hash2[:32]}...")
match = hash1 == hash2
print(f"✓ Hash match: {'OUI ✓' if match else 'NON ✗'}\n")

# Cleanup
Path(test_file).unlink()
Path(output).unlink()

print("=== Tests terminés ===")
print(f"Résultat: {'SUCCÈS ✓' if match else 'ÉCHEC ✗'}")
```

**Exécuter:**
```powershell
python test_chunking.py
# Doit afficher: SUCCÈS ✓
```

### Commit Jour 1

```powershell
git add p2p_file_sharing/core/file_manager.py
git commit -m "Implement file chunking with SHA256 verification"
git push origin feature/core
```

---

## 📅 Jour 2: Database SQLite

### Objectif
Créer schéma de base de données et opérations CRUD

### Créer `database.py`

**PowerShell:**
```powershell
New-Item -ItemType File -Path "p2p_file_sharing\core\database.py"
code p2p_file_sharing\core\database.py
```

**Code complet (fichier long):**
```python
"""Gestion de la base de données SQLite"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
from ..utils.config import DATABASE_PATH
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class Database:
    """Gestion de la base de données locale"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or DATABASE_PATH
        self.conn = sqlite3.connect(
            str(self.db_path), 
            check_same_thread=False
        )
        self.conn.row_factory = sqlite3.Row
        self._create_schema()
        logger.info(f"Database initialized: {self.db_path}")
    
    def _create_schema(self):
        """Crée le schéma de la base"""
        cursor = self.conn.cursor()
        
        # Table peers
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS peers (
                peer_id TEXT PRIMARY KEY,
                ip TEXT NOT NULL,
                port INTEGER NOT NULL,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table files
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                file_id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                size INTEGER NOT NULL,
                hash TEXT NOT NULL,
                owner_peer_id TEXT,
                chunks_total INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table chunks
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chunks (
                chunk_id TEXT PRIMARY KEY,
                file_id TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                hash TEXT,
                peer_ids TEXT,
                FOREIGN KEY (file_id) REFERENCES files(file_id)
            )
        ''')
        
        # Table local_shared
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS local_shared (
                file_id TEXT PRIMARY KEY,
                filepath TEXT NOT NULL,
                FOREIGN KEY (file_id) REFERENCES files(file_id)
            )
        ''')
        
        self.conn.commit()
        logger.info("Database schema created/verified")
    
    # === PEERS ===
    
    def add_peer(self, peer_id: str, ip: str, port: int):
        """Ajoute ou met à jour un peer"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO peers (peer_id, ip, port, last_seen)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ''', (peer_id, ip, port))
        self.conn.commit()
        logger.debug(f"Peer added/updated: {peer_id}")
    
    def get_active_peers(self, timeout_seconds: int = 30) -> List[Dict]:
        """Retourne peers actifs"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT peer_id, ip, port, last_seen
            FROM peers
            WHERE datetime(last_seen) > datetime('now', '-' || ? || ' seconds')
        ''', (timeout_seconds,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def remove_peer(self, peer_id: str):
        """Supprime un peer"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM peers WHERE peer_id = ?', (peer_id,))
        self.conn.commit()
        logger.debug(f"Peer removed: {peer_id}")
    
    # === FILES ===
    
    def add_file(self, file_id: str, filename: str, size: int, 
                 hash: str, owner_peer_id: str, chunks_total: int):
        """Ajoute un fichier au catalogue"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO files 
            (file_id, filename, size, hash, owner_peer_id, chunks_total)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (file_id, filename, size, hash, owner_peer_id, chunks_total))
        self.conn.commit()
        logger.debug(f"File added: {filename} ({file_id})")
    
    def get_file_by_id(self, file_id: str) -> Optional[Dict]:
        """Récupère un fichier par ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM files WHERE file_id = ?', (file_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_files_by_peer(self, peer_id: str) -> List[Dict]:
        """Récupère les fichiers d'un peer"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM files WHERE owner_peer_id = ?
        ''', (peer_id,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_all_files(self) -> List[Dict]:
        """Récupère tous les fichiers disponibles"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM files ORDER BY created_at DESC')
        return [dict(row) for row in cursor.fetchall()]
    
    # === CHUNKS ===
    
    def add_chunk(self, chunk_id: str, file_id: str, chunk_index: int,
                  hash: str, peer_ids: List[str]):
        """Ajoute info sur un chunk"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO chunks 
            (chunk_id, file_id, chunk_index, hash, peer_ids)
            VALUES (?, ?, ?, ?, ?)
        ''', (chunk_id, file_id, chunk_index, hash, json.dumps(peer_ids)))
        self.conn.commit()
    
    def get_chunks_for_file(self, file_id: str) -> List[Dict]:
        """Récupère les chunks d'un fichier"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT chunk_id, chunk_index, hash, peer_ids 
            FROM chunks WHERE file_id = ?
            ORDER BY chunk_index
        ''', (file_id,))
        
        chunks = []
        for row in cursor.fetchall():
            chunk = dict(row)
            chunk['peer_ids'] = json.loads(chunk['peer_ids']) if chunk['peer_ids'] else []
            chunks.append(chunk)
        
        return chunks
    
    # === LOCAL SHARED ===
    
    def add_local_shared(self, file_id: str, filepath: str):
        """Ajoute un fichier partagé localement"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO local_shared (file_id, filepath)
            VALUES (?, ?)
        ''', (file_id, filepath))
        self.conn.commit()
    
    def get_local_shared_files(self) -> List[Dict]:
        """Récupère fichiers partagés localement"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT f.*, ls.filepath
            FROM files f
            JOIN local_shared ls ON f.file_id = ls.file_id
        ''')
        return [dict(row) for row in cursor.fetchall()]
    
    def close(self):
        """Ferme la connexion"""
        self.conn.close()
        logger.info("Database closed")
```

### Test Jour 2

**Créer `test_database.py`:**
```python
from p2p_file_sharing.core.database import Database

print("=== Test Database ===\n")

# DB en mémoire pour test
db = Database(':memory:')

# Test 1: Peers
print("Test 1: Gestion peers...")
db.add_peer('peer1', '192.168.1.10', 5001)
db.add_peer('peer2', '192.168.1.11', 5001)
peers = db.get_active_peers()
print(f"✓ Peers ajoutés: {len(peers)}")
for p in peers:
    print(f"  - {p['peer_id']} @ {p['ip']}:{p['port']}")
print()

# Test 2: Files
print("Test 2: Gestion fichiers...")
db.add_file('file1', 'test.txt', 1024, 'abc123hash', 'peer1', 4)
db.add_file('file2', 'video.mp4', 10485760, 'def456hash', 'peer2', 40)
files = db.get_all_files()
print(f"✓ Fichiers ajoutés: {len(files)}")
for f in files:
    size_mb = f['size'] / 1024 / 1024
    print(f"  - {f['filename']} ({size_mb:.2f} MB, {f['chunks_total']} chunks)")
print()

# Test 3: Chunks
print("Test 3: Gestion chunks...")
db.add_chunk('chunk1', 'file1', 0, 'chunk0hash', ['peer1', 'peer2'])
db.add_chunk('chunk2', 'file1', 1, 'chunk1hash', ['peer1'])
chunks = db.get_chunks_for_file('file1')
print(f"✓ Chunks ajoutés: {len(chunks)}")
for c in chunks:
    print(f"  - Chunk {c['chunk_index']}: {len(c['peer_ids'])} peer(s)")
print()

# Test 4: Local shared
print("Test 4: Fichiers locaux...")
db.add_local_shared('file1', '/path/to/file1.txt')
local = db.get_local_shared_files()
print(f"✓ Fichiers partagés localement: {len(local)}")
print()

db.close()
print("=== Tests terminés avec succès ===")
```

**Exécuter:**
```powershell
python test_database.py
```

### Commit Jour 2

```powershell
git add p2p_file_sharing/core/database.py
git commit -m "Add SQLite database with peers/files/chunks tables"
git push origin feature/core
```

---

## 📅 Jour 3: Peer Manager

### Objectif
Compléter la gestion de l'état des peers

### Compléter `peer_manager.py`

**Ouvrir:**
```powershell
code p2p_file_sharing\core\peer_manager.py
```

**Compléter le code:**
```python
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
```

### Test Jour 3

**Créer `test_peer_manager.py`:**
```python
from p2p_file_sharing.core.database import Database
from p2p_file_sharing.core.peer_manager import PeerManager

print("=== Test Peer Manager ===\n")

# Setup
db = Database(':memory:')
pm = PeerManager(db)
pm.set_local_peer_id('local_peer')

# Test 1: Announce handling
print("Test 1: Handle peer announce...")
pm.handle_peer_announce('peer1', '192.168.1.10', 5001)
pm.handle_peer_announce('peer2', '192.168.1.11', 5001)
pm.handle_peer_announce('local_peer', '192.168.1.5', 5001)  # Devrait être ignoré

peers = pm.get_online_peers()
print(f"✓ Peers en ligne: {len(peers)} (devrait être 2)")
for p in peers:
    print(f"  - {p['peer_id']}")
print()

# Test 2: Update peer files
print("Test 2: Update peer files...")
files = [
    {
        'file_id': 'file1',
        'filename': 'document.pdf',
        'size': 1024000,
        'hash': 'hash123',
        'chunks_total': 4
    },
    {
        'file_id': 'file2',
        'filename': 'image.jpg',
        'size': 512000,
        'hash': 'hash456',
        'chunks_total': 2
    }
]
pm.update_peer_files('peer1', files)

all_files = db.get_all_files()
print(f"✓ Fichiers ajoutés: {len(all_files)}")
for f in all_files:
    print(f"  - {f['filename']} (owner: {f['owner_peer_id']})")
print()

db.close()
print("=== Tests terminés avec succès ===")
```

**Exécuter:**
```powershell
python test_peer_manager.py
```

### Commit Jour 3

```powershell
git add p2p_file_sharing/core/peer_manager.py
git commit -m "Complete peer manager with database integration"
git push origin feature/core
```

---

## 🔀 Fin Jour 3: Créer Pull Request

**Sur GitHub.com:**
```
1. Pull requests → New pull request
2. Base: main ← Compare: feature/core
3. Titre: "Core layer: File management, database, peer tracking"
4. Description:
   
   Implémente la logique métier:
   - File chunking avec SHA256
   - Database SQLite (peers, files, chunks)
   - Peer manager avec tracking état
   - Tests inclus et fonctionnels
   
5. Create pull request
```

---

## 📊 Checklist Jours 1-3

- [ ] `file_manager.py` chunking/assemblage fonctionnel
- [ ] `database.py` avec toutes les tables
- [ ] `peer_manager.py` complet
- [ ] Tests passent (chunking, DB, peer manager)
- [ ] Code committé et pushé
- [ ] Pull Request créée
- [ ] Pas de print() debug
- [ ] Docstrings présentes
- [ ] Gestion erreurs

---

## 💡 Conseils

- **Hash partout:** Vérifier intégrité des chunks
- **SQLite thread-safe:** `check_same_thread=False`
- **Cleanup:** Supprimer vieux peers automatiquement
- **Tests:** Fichiers de différentes tailles
- **Git:** Commits réguliers

---

## 🆘 Problèmes courants

### Base de données verrouillée

**Solution:**
```python
# Utiliser timeout
conn = sqlite3.connect(db_path, timeout=10.0)
```

### Chunks incohérents

- Vérifier que chunk_index démarre à 0
- Trier avant assemblage
- Vérifier hash de chaque chunk

### Mémoire insuffisante

- Ne pas charger fichier complet en mémoire
- Streamer chunk par chunk
- Limiter taille max fichier si nécessaire

---

**Prochaine étape:** Attendre fin jour 3, puis voir [INTEGRATION.md](INTEGRATION.md)
