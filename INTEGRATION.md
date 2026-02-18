# 🔗 INTEGRATION.md - Jours 4-9

**Phase d'intégration et développement des features complètes**

Une fois les 3 modules mergés dans `main` (fin jour 3), vous travaillez tous ensemble sur les fonctionnalités complètes.

---

## 📅 Jour 4: Connexion Network ↔ Core

**Objectif:** Les peers découverts sont ajoutés à la base de données

### Workflow attendu

```
Peer A découvert via UDP
  ↓
UDPDiscovery appelle callback
  ↓
PeerManager.handle_peer_announce()
  ↓
Database.add_peer()
  ↓
GUI affiche peer dans liste
```

### Tâches

**Tous ensemble, pair programming recommandé:**

#### Personne 3: Intégration dans main.py

**Compléter la fonction `main()` dans `main.py`:**

```python
# Après initialisation des modules...

if NETWORK_AVAILABLE and peer_manager:
    # UDP Discovery avec callback peer_manager
    discovery = UDPDiscovery(peer_id, DISCOVERY_PORT)
    discovery.start_listening(peer_manager.handle_peer_announce)
    discovery.start_broadcasting()
    
    # TCP Server avec handler messages
    def on_tcp_message(sender_peer_id, message):
        logger.info(f"TCP message from {sender_peer_id}: {message['type']}")
        # Router selon type
        handle_message(sender_peer_id, message)
    
    tcp_server = TCPServer(TRANSFER_PORT_START)
    tcp_server.start(on_tcp_message)
```

#### Personne 1: Handler de messages

**Créer `p2p_file_sharing/network/message_handler.py`:**

```python
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
```

### Test Jour 4

**Terminal 1:**
```powershell
python main.py
```

**Terminal 2:**
```powershell
python main.py
```

**Résultat attendu:**
- Les 2 instances se découvrent en ~10 secondes
- Chaque GUI affiche l'autre peer dans la liste
- Logs montrent découverte UDP + ajout DB

**Si ça marche → 🎉 Premier milestone atteint !**

### Commit Jour 4

```powershell
git add .
git commit -m "Integrate network discovery with peer manager"
git push origin main
```

---

## 📅 Jour 5: Partage de Fichiers

**Objectif:** Bouton "Partager" → fichier visible chez autres peers

### Workflow complet

```
User clique "Partager fichier"
  ↓
FileManager.add_shared_file() → chunk, store DB
  ↓
Broadcast FILE_LIST update à tous les peers
  ↓
Autres peers reçoivent, affichent fichier
```

### Tâches

#### Personne 2: Compléter partage

**Dans `file_manager.py`, améliorer `add_shared_file()`:**

```python
def add_shared_file(self, filepath: str) -> str:
    """Ajoute fichier + notifie network pour broadcast"""
    # ... code existant ...
    
    # Notifier qu'on a un nouveau fichier
    # (sera géré par main.py pour broadcaster)
    logger.info(f"File shared: {file_id} - Ready to broadcast")
    
    return file_id

def get_my_file_list(self) -> List[Dict]:
    """Retourne liste de nos fichiers pour l'envoyer aux peers"""
    files = self.get_shared_files()
    
    # Format pour envoi réseau
    file_list = []
    for f in files:
        file_list.append({
            'file_id': f['file_id'],
            'filename': f['filename'],
            'size': f['size'],
            'hash': f['hash'],
            'chunks_total': f['chunks_total']
        })
    
    return file_list
```

#### Personne 1: Broadcast file list

**Dans `message_handler.py`:**

```python
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
        {'files': file_list}
    )
    
    # Envoyer à tous les peers connectés
    for peer_id in tcp_server.clients.keys():
        tcp_server.send_to_peer(peer_id, message)
    
    logger.info(f"Broadcasted {len(file_list)} files to peers")
```

#### Personne 3: Connecter GUI

**Dans `main_window.py`, méthode `share_file()`:**

```python
def share_file(self):
    """Partage un fichier local"""
    filepath = filedialog.askopenfilename(...)
    if not filepath:
        return
    
    try:
        if self.file_manager:
            file_id = self.file_manager.add_shared_file(filepath)
            if file_id:
                # Notifier network pour broadcast (via callback ou event)
                # TODO: Implémenter mechanism de notification
                
                self.status_var.set(f"Fichier partagé: {filepath}")
                messagebox.showinfo("Succès", f"Fichier partagé!\nID: {file_id}")
                self.update_file_list()
```

### Test Jour 5

```
1. Peer A: Partager fichier test.pdf
2. Attendre 2-3 secondes
3. Peer B: Devrait voir test.pdf dans liste des fichiers
4. Vérifier DB de B: fichier doit être présent
```

### Commit Jour 5

```powershell
git add .
git commit -m "Implement file sharing with broadcast"
git push origin main
```

---

## 📅 Jour 6: Premier Téléchargement ⭐

**Objectif critique:** Télécharger fichier complet depuis 1 peer

### Workflow

```
User clique "Télécharger"
  ↓
GUI → FileManager.download_file()
  ↓
FileManager récupère infos fichier (chunks_total, peers)
  ↓
Pour chaque chunk:
  - Envoyer CHUNK_REQUEST via TCP
  - Recevoir CHUNK_DATA
  - Vérifier hash
  - Callback progress
  ↓
Assembler tous les chunks
  ↓
Vérifier hash final
  ↓
Succès !
```

### Tâches (GROSSE JOURNÉE - Tous ensemble)

#### Personne 1: Protocole chunks

**Dans `connection.py`, ajouter méthodes:**

```python
def request_chunk(self, peer_ip: str, peer_port: int, file_id: str, 
                  chunk_index: int, my_peer_id: str) -> bytes:
    """
    Demande un chunk à un peer
    
    Returns:
        bytes: Données du chunk ou None si erreur
    """
    from .protocol import create_message, MessageType
    
    client = TCPClient()
    if not client.connect(peer_ip, peer_port):
        return None
    
    # Envoyer requête
    request = create_message(
        MessageType.CHUNK_REQUEST,
        my_peer_id,
        {
            'file_id': file_id,
            'chunk_index': chunk_index
        }
    )
    client.send_message(request)
    
    # Recevoir réponse
    response = client.receive_message(timeout=30)
    client.close()
    
    if response and response['type'] == MessageType.CHUNK_DATA:
        import base64
        chunk_data = base64.b64decode(response['data']['chunk_data'])
        return chunk_data
    
    return None
```

**Handler côté serveur (message_handler.py):**

```python
def _handle_chunk_request(self, sender_peer_id, message):
    """Peer demande un chunk"""
    file_id = message['data']['file_id']
    chunk_index = message['data']['chunk_index']
    
    logger.info(f"Chunk {chunk_index} of {file_id} requested by {sender_peer_id}")
    
    # Récupérer le fichier local
    local_files = self.file_manager.db.get_local_shared_files()
    local_file = None
    for f in local_files:
        if f['file_id'] == file_id:
            local_file = f
            break
    
    if not local_file:
        logger.error(f"File {file_id} not found locally")
        return
    
    # Charger et envoyer chunk
    chunks = self.file_manager.chunk_file(local_file['filepath'])
    if chunk_index < len(chunks):
        chunk = chunks[chunk_index]
        
        import base64
        chunk_data_b64 = base64.b64encode(chunk['data']).decode('utf-8')
        
        from .protocol import create_message, MessageType
        response = create_message(
            MessageType.CHUNK_DATA,
            self.peer_manager.local_peer_id,
            {
                'file_id': file_id,
                'chunk_index': chunk_index,
                'chunk_data': chunk_data_b64,
                'hash': chunk['hash']
            }
        )
        
        # Envoyer via TCP (TODO: gérer connexion)
        logger.info(f"Sending chunk {chunk_index} to {sender_peer_id}")
```

#### Personne 2: Download logic

**Dans `file_manager.py`, compléter `download_file()`:**

```python
def download_file(self, file_id: str, save_path: str, 
                  progress_callback: Callable[[int], None],
                  network_requester) -> bool:
    """
    Télécharge un fichier
    
    Args:
        file_id: ID du fichier
        save_path: Où sauvegarder
        progress_callback: Fonction(percent) pour GUI
        network_requester: Objet pour faire requêtes réseau
    
    Returns:
        bool: True si succès
    """
    try:
        # 1. Get file info
        file_info = self.db.get_file_by_id(file_id)
        if not file_info:
            logger.error(f"File {file_id} not found")
            return False
        
        chunks_total = file_info['chunks_total']
        logger.info(f"Downloading {file_info['filename']} ({chunks_total} chunks)")
        
        # 2. Get peers qui ont le fichier
        # Pour l'instant: on suppose que owner_peer_id a tout
        owner_peer_id = file_info['owner_peer_id']
        peers = self.db.get_active_peers()
        owner_peer = None
        for p in peers:
            if p['peer_id'] == owner_peer_id:
                owner_peer = p
                break
        
        if not owner_peer:
            logger.error(f"Owner peer {owner_peer_id} not online")
            return False
        
        # 3. Télécharger chaque chunk
        chunks = []
        for i in range(chunks_total):
            logger.info(f"Requesting chunk {i}/{chunks_total}")
            
            chunk_data = network_requester.request_chunk(
                owner_peer['ip'],
                owner_peer['port'],
                file_id,
                i,
                self.db  # Passer local peer ID via contexte
            )
            
            if not chunk_data:
                logger.error(f"Failed to download chunk {i}")
                return False
            
            chunks.append({
                'chunk_index': i,
                'data': chunk_data,
                'hash': ''  # TODO: vérifier
            })
            
            # Update progress
            percent = int((i + 1) / chunks_total * 100)
            progress_callback(percent)
        
        # 4. Assembler
        success = self.assemble_chunks(chunks, save_path)
        
        if success:
            # Vérifier hash final
            final_hash = self.calculate_file_hash(save_path)
            expected_hash = file_info['hash']
            
            if final_hash == expected_hash:
                logger.info(f"✓ File downloaded successfully: {save_path}")
                return True
            else:
                logger.error("Hash mismatch after download!")
                return False
        
        return False
        
    except Exception as e:
        logger.error(f"Download error: {e}", exc_info=True)
        return False
```

#### Personne 3: GUI threading

**Dans `main_window.py`:**

```python
def download_file(self):
    """Télécharge le fichier sélectionné (avec thread)"""
    selection = self.files_tree.selection()
    if not selection:
        messagebox.showwarning("Attention", "Sélectionnez un fichier")
        return
    
    # Get file info
    item = self.files_tree.item(selection[0])
    filename = item['values'][0]
    file_id = item.get('tags', [''])[0]
    
    if not file_id:
        messagebox.showerror("Erreur", "ID fichier introuvable")
        return
    
    # Demander destination
    save_path = filedialog.asksaveasfilename(
        title="Enregistrer sous",
        initialfile=filename
    )
    if not save_path:
        return
    
    logger.info(f"Starting download: {filename} -> {save_path}")
    self.dl_label.config(text=f"Téléchargement: {filename}")
    self.progress_bar['value'] = 0
    
    # Progress callback
    def update_progress(percent):
        self.progress_bar['value'] = percent
        self.root.update_idletasks()
    
    # Download dans thread séparé
    import threading
    def download_thread():
        try:
            # TODO: Passer network_requester
            success = self.file_manager.download_file(
                file_id,
                save_path,
                update_progress,
                None  # network requester
            )
            
            if success:
                self.root.after(0, lambda: messagebox.showinfo(
                    "Succès",
                    f"Fichier téléchargé:\n{save_path}"
                ))
            else:
                self.root.after(0, lambda: messagebox.showerror(
                    "Erreur",
                    "Échec du téléchargement"
                ))
        except Exception as e:
            logger.error(f"Download thread error: {e}")
            self.root.after(0, lambda: messagebox.showerror(
                "Erreur",
                f"Erreur: {e}"
            ))
        finally:
            self.dl_label.config(text="Téléchargement terminé")
    
    t = threading.Thread(target=download_thread, daemon=True)
    t.start()
```

### Test Jour 6 - TEST CRITIQUE ⭐

**Ce test valide que votre système fonctionne end-to-end:**

```
1. Peer A: Partager fichier image.jpg (5 MB)
2. Attendre que B le voie
3. Peer B: Télécharger image.jpg
4. Vérifier:
   - Barre de progression bouge
   - Fichier téléchargé existe
   - Taille correcte
   - Hash identique à l'original
```

**Vérifier hash:**
```powershell
# Sur Peer A
python -c "from p2p_file_sharing.core.file_manager import FileManager; fm = FileManager(); print(fm.calculate_file_hash('image.jpg'))"

# Sur Peer B
python -c "from p2p_file_sharing.core.file_manager import FileManager; fm = FileManager(); print(fm.calculate_file_hash('downloaded_image.jpg'))"

# Les deux doivent être identiques !
```

**Si ça marche → 🚀 ÉNORME MILESTONE ! Célébrez !**

### Commit Jour 6

```powershell
git add .
git commit -m "✨ Implement complete file download from single peer"
git push origin main
```

---

## 📅 Jour 7: Téléchargement Multi-Peer

**Objectif:** Télécharger chunks depuis plusieurs peers en parallèle

*Note: Si en retard, SKIP cette feature - mono-peer suffit*

### Concept

```
Fichier 10 chunks:
- Peer A a chunks 0-4
- Peer B a chunks 5-9

Télécharger 0-4 depuis A et 5-9 depuis B simultanément
→ 2x plus rapide !
```

### Implémentation (Personne 2 lead)

**Modifier `download_file()` pour gérer multi-peer:**

```python
import threading
from queue import Queue

def download_file_multi_peer(self, file_id: str, save_path: str, 
                              progress_callback, network_requester):
    """Télécharge depuis plusieurs peers"""
    
    # 1. Map chunks → peers
    chunks_info = self.db.get_chunks_for_file(file_id)
    
    # 2. Queue de travail
    work_queue = Queue()
    for chunk in chunks_info:
        work_queue.put(chunk)
    
    # 3. Résultats (thread-safe)
    results = {}
    results_lock = threading.Lock()
    
    # 4. Worker
    def worker():
        while not work_queue.empty():
            try:
                chunk_info = work_queue.get(timeout=1)
            except:
                break
            
            # Try each peer qui a ce chunk
            for peer_id in chunk_info['peer_ids']:
                peer = self._get_peer_info(peer_id)
                if not peer:
                    continue
                
                data = network_requester.request_chunk(
                    peer['ip'], peer['port'],
                    file_id, chunk_info['chunk_index']
                )
                
                if data:
                    with results_lock:
                        results[chunk_info['chunk_index']] = data
                    break
            
            # Progress
            with results_lock:
                percent = int(len(results) / len(chunks_info) * 100)
                progress_callback(percent)
    
    # 5. Lancer 3 workers
    workers = []
    for _ in range(3):
        t = threading.Thread(target=worker)
        t.start()
        workers.append(t)
    
    # 6. Attendre
    for t in workers:
        t.join()
    
    # 7. Assembler
    sorted_chunks = [
        {'chunk_index': i, 'data': results[i]} 
        for i in sorted(results.keys())
    ]
    return self.assemble_chunks(sorted_chunks, save_path)
```

### Test Jour 7

Nécessite 3 machines ou configs avancées. Skip si manque de temps.

---

## 📅 Jour 8: Polish & Partial Downloads

### Matin: Téléchargements partiels

**Permettre download même si pas tous les peers disponibles:**

```python
# Si chunk manquant, continuer avec les autres
# Marquer fichier comme "partiel"
# Permettre reprise plus tard
```

### Après-midi: Polish GUI

**Personne 3:**
- Meilleurs messages d'erreur
- About dialog
- Tooltips
- Icônes/couleurs
- Gestion exceptions robuste

### Commit Jour 8

```powershell
git add .
git commit -m "Add partial downloads and GUI improvements"
git push origin main
```

---

## 📅 Jour 9: Tests Complets & Bugfixes

### Testing avec 3 machines réelles

**Scénarios à tester:**

1. **Découverte:**
   - 3 peers se découvrent mutuellement
   - Déconnecter 1 peer → disparaît des listes
   - Reconnecter → réapparaît

2. **Partage:**
   - A partage fichier → B et C le voient
   - Vérifier DB de B et C

3. **Download mono-peer:**
   - C télécharge depuis A
   - Vérifier hash identique

4. **Download multi-peer:**
   - Fichier fragmenté sur A et B
   - C télécharge depuis les deux
   - Vérifier assemblage correct

5. **Résilience:**
   - Pendant download, A se déconnecte
   - C continue avec B (ou fail gracefully)

6. **Edge cases:**
   - Fichier 0 byte
   - Fichier énorme (>100MB)
   - Caractères spéciaux dans nom
   - Réseau lent

### Checklist bugs courants

- [ ] GUI freeze → threads OK ?
- [ ] Chunks corrompus → hash vérifiés ?
- [ ] Ports occupés → gestion erreurs ?
- [ ] Firewall bloque → doc utilisateur ?
- [ ] Memory leaks → fermer connexions ?
- [ ] Deadlocks → minimiser locks ?
- [ ] Crashes sur déconnexion → try/except ?

### Commit Jour 9

```powershell
git add .
git commit -m "Fix bugs from integration testing"
git push origin main
```

---

## ✅ Checklist Intégration (Jours 4-9)

### Jour 4
- [ ] Peers découverts ajoutés en DB
- [ ] GUI affiche peers réels
- [ ] Test 2 instances réussi

### Jour 6 ⭐
- [ ] Fichier partagé visible sur autres peers
- [ ] Téléchargement complet fonctionne
- [ ] Hash vérifié après download
- [ ] Barre de progression active

### Jour 9
- [ ] Tests avec 3 machines réels
- [ ] Tous scénarios passent
- [ ] Bugs principaux fixés
- [ ] Logs clairs

---

## 💡 Conseils

- **Daily standup:** 10min chaque matin
- **Pair programming:** Jours 5-6 critiques
- **Commits fréquents:** Au moins 2-3 par jour
- **Tests précoces:** Dès jour 4
- **Communication:** Signaler blocages immédiatement

---

**Prochaine étape:** [PACKAGING.md](PACKAGING.md) pour jour 10+
