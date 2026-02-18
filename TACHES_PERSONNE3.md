# 🟣 Tâches Personne 3 - GUI & Intégration

**Branche:** `feature/gui`  
**Responsabilité:** Interface graphique, intégration modules, lead du projet

**Rôle spécial:** Integration Lead - Vous coordonnez les merges

---

## 📂 Vos fichiers

- `p2p_file_sharing/gui/main_window.py` - Fenêtre principale
- `p2p_file_sharing/gui/widgets.py` - Composants personnalisés
- `main.py` - Point d'entrée application
- `install.bat` / `install.sh` - Scripts installation (jour 9-10)
- `run.bat` / `run.sh` - Scripts lancement (jour 9-10)

---

## 📅 Jour 1: GUI Layout

### Objectif
Créer l'interface graphique de base avec tkinter

### Compléter `main_window.py`

**Ouvrir:**
```powershell
code p2p_file_sharing\gui\main_window.py
```

**Code complet:**
```python
"""Fenêtre principale de l'application"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class MainWindow:
    """Interface graphique principale"""
    
    def __init__(self, peer_manager=None, file_manager=None, network_handler=None):
        self.peer_manager = peer_manager
        self.file_manager = file_manager
        self.network = network_handler
        
        self.root = tk.Tk()
        self.root.title("P2P File Sharing")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Thème moderne
        
        self._build_ui()
        
        # Auto-refresh
        if self.peer_manager:
            self.root.after(2000, self.update_peer_list)
        if self.file_manager:
            self.root.after(3000, self.update_file_list)
    
    def _build_ui(self):
        """Construit l'interface"""
        
        # === Frame principal ===
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # === Top: Peers connectés ===
        peer_frame = ttk.LabelFrame(
            main_frame, 
            text="🌐 Peers connectés", 
            padding="10"
        )
        peer_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        # Listbox + Scrollbar
        peer_scroll_frame = ttk.Frame(peer_frame)
        peer_scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        self.peer_listbox = tk.Listbox(
            peer_scroll_frame, 
            height=4, 
            font=('Arial', 10)
        )
        self.peer_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        peer_scrollbar = ttk.Scrollbar(
            peer_scroll_frame, 
            orient=tk.VERTICAL,
            command=self.peer_listbox.yview
        )
        peer_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.peer_listbox.config(yscrollcommand=peer_scrollbar.set)
        
        # === Middle: Fichiers disponibles ===
        files_frame = ttk.LabelFrame(
            main_frame, 
            text="📁 Fichiers disponibles", 
            padding="10"
        )
        files_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # TreeView
        columns = ("Nom", "Taille", "Propriétaire", "Chunks", "Statut")
        self.files_tree = ttk.Treeview(
            files_frame, 
            columns=columns,
            show="headings", 
            height=10
        )
        
        # Headers
        self.files_tree.heading("Nom", text="Nom du fichier")
        self.files_tree.heading("Taille", text="Taille")
        self.files_tree.heading("Propriétaire", text="Propriétaire")
        self.files_tree.heading("Chunks", text="Chunks")
        self.files_tree.heading("Statut", text="Statut")
        
        # Colonnes width
        self.files_tree.column("Nom", width=300)
        self.files_tree.column("Taille", width=100)
        self.files_tree.column("Propriétaire", width=120)
        self.files_tree.column("Chunks", width=80)
        self.files_tree.column("Statut", width=120)
        
        self.files_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        files_scrollbar = ttk.Scrollbar(
            files_frame,
            orient=tk.VERTICAL,
            command=self.files_tree.yview
        )
        files_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.files_tree.config(yscrollcommand=files_scrollbar.set)
        
        # === Buttons ===
        btn_frame = ttk.Frame(main_frame, padding="5")
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.btn_share = ttk.Button(
            btn_frame,
            text="📤 Partager un fichier",
            command=self.share_file
        )
        self.btn_share.pack(side=tk.LEFT, padx=5)
        
        self.btn_download = ttk.Button(
            btn_frame,
            text="📥 Télécharger",
            command=self.download_file
        )
        self.btn_download.pack(side=tk.LEFT, padx=5)
        
        self.btn_refresh = ttk.Button(
            btn_frame,
            text="🔄 Actualiser",
            command=self.refresh_all
        )
        self.btn_refresh.pack(side=tk.LEFT, padx=5)
        
        # === Bottom: Downloads ===
        dl_frame = ttk.LabelFrame(
            main_frame,
            text="⬇️ Téléchargements en cours",
            padding="10"
        )
        dl_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        self.dl_label = ttk.Label(
            dl_frame,
            text="Aucun téléchargement en cours",
            font=('Arial', 9)
        )
        self.dl_label.pack(anchor=tk.W, pady=2)
        
        self.progress_bar = ttk.Progressbar(
            dl_frame,
            mode='determinate',
            length=300
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # === Status Bar ===
        self.status_var = tk.StringVar(value="Prêt")
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding="2"
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        logger.info("GUI built successfully")
    
    def share_file(self):
        """Partage un fichier local"""
        filepath = filedialog.askopenfilename(
            title="Sélectionner un fichier à partager",
            filetypes=[
                ("Tous les fichiers", "*.*"),
                ("Documents", "*.pdf *.doc *.docx *.txt"),
                ("Images", "*.jpg *.png *.gif *.bmp"),
                ("Vidéos", "*.mp4 *.avi *.mkv"),
            ]
        )
        
        if not filepath:
            return
        
        logger.info(f"Sharing file: {filepath}")
        
        try:
            if self.file_manager:
                file_id = self.file_manager.add_shared_file(filepath)
                if file_id:
                    self.status_var.set(f"Fichier partagé: {filepath}")
                    messagebox.showinfo(
                        "Succès", 
                        f"Fichier partagé avec succès!\nID: {file_id}"
                    )
                    self.update_file_list()
                else:
                    messagebox.showerror("Erreur", "Échec du partage")
            else:
                messagebox.showwarning("Erreur", "File manager non disponible")
        except Exception as e:
            logger.error(f"Share error: {e}", exc_info=True)
            messagebox.showerror("Erreur", f"Erreur lors du partage: {e}")
    
    def download_file(self):
        """Télécharge le fichier sélectionné"""
        selection = self.files_tree.selection()
        
        if not selection:
            messagebox.showwarning(
                "Attention", 
                "Veuillez sélectionner un fichier à télécharger"
            )
            return
        
        # Récupérer infos fichier
        item = self.files_tree.item(selection[0])
        filename = item['values'][0]
        file_id = item.get('tags', [''])[0] if item.get('tags') else None
        
        if not file_id:
            messagebox.showerror("Erreur", "ID fichier introuvable")
            return
        
        # Demander où sauvegarder
        save_path = filedialog.asksaveasfilename(
            title="Enregistrer sous",
            initialfile=filename,
            defaultextension=".*"
        )
        
        if not save_path:
            return
        
        logger.info(f"Downloading: {filename} (ID: {file_id}) -> {save_path}")
        self.dl_label.config(text=f"Téléchargement: {filename}")
        self.progress_bar['value'] = 0
        
        # TODO: Implémenter téléchargement réel après intégration
        messagebox.showinfo(
            "Info", 
            "Téléchargement démarré!\n(Fonctionnalité complète après intégration)"
        )
    
    def update_peer_list(self):
        """Rafraîchit la liste des peers"""
        if not self.peer_manager:
            self.root.after(2000, self.update_peer_list)
            return
        
        self.peer_listbox.delete(0, tk.END)
        
        try:
            peers = self.peer_manager.get_online_peers()
            
            if not peers:
                self.peer_listbox.insert(tk.END, "Aucun peer connecté")
                self.peer_listbox.config(fg='gray')
            else:
                self.peer_listbox.config(fg='black')
                for peer in peers:
                    self.peer_listbox.insert(
                        tk.END,
                        f"🟢 {peer['peer_id']} - {peer['ip']}:{peer['port']}"
                    )
            
            self.status_var.set(f"Prêt - {len(peers)} peer(s) connecté(s)")
            
        except Exception as e:
            logger.error(f"Update peer list error: {e}")
        
        # Re-schedule
        self.root.after(2000, self.update_peer_list)
    
    def update_file_list(self):
        """Rafraîchit la liste des fichiers"""
        if not self.file_manager:
            self.root.after(3000, self.update_file_list)
            return
        
        # Clear tree
        for item in self.files_tree.get_children():
            self.files_tree.delete(item)
        
        try:
            # Récupérer fichiers de la DB
            if hasattr(self.file_manager, 'db') and self.file_manager.db:
                files = self.file_manager.db.get_all_files()
                
                for file in files:
                    size_mb = file['size'] / (1024 * 1024)
                    size_str = f"{size_mb:.2f} MB" if size_mb >= 1 else f"{file['size']/1024:.0f} KB"
                    
                    # Insérer avec file_id en tag
                    self.files_tree.insert(
                        "", 
                        tk.END,
                        values=(
                            file['filename'],
                            size_str,
                            file['owner_peer_id'][:12] + "..." if len(file['owner_peer_id']) > 12 else file['owner_peer_id'],
                            f"{file['chunks_total']} chunks",
                            "Disponible"
                        ),
                        tags=(file['file_id'],)
                    )
            else:
                # Données de test si pas de DB
                test_files = [
                    ("example.pdf", "2.5 MB", "peer_abc", "10 chunks", "Disponible"),
                    ("music.mp3", "4.1 MB", "peer_xyz", "16 chunks", "Partiel 60%"),
                ]
                for file_data in test_files:
                    self.files_tree.insert("", tk.END, values=file_data)
                
        except Exception as e:
            logger.error(f"Update file list error: {e}")
        
        # Re-schedule
        self.root.after(3000, self.update_file_list)
    
    def refresh_all(self):
        """Force le rafraîchissement de tout"""
        logger.info("Manual refresh triggered")
        self.update_peer_list()
        self.update_file_list()
    
    def run(self):
        """Lance la boucle d'événements tkinter"""
        logger.info("Starting GUI main loop")
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            logger.info("GUI interrupted")
        finally:
            logger.info("GUI closed")
```

### Test Jour 1

**PowerShell:**
```powershell
python -c "from p2p_file_sharing.gui.main_window import MainWindow; win = MainWindow(); win.run()"
```

Devrait afficher une fenêtre avec:
- Zone peers (vide)
- Zone fichiers (avec exemples)
- Boutons fonctionnels
- Barre de progression

### Commit Jour 1

```powershell
git add p2p_file_sharing/gui/main_window.py
git commit -m "Create main GUI layout with all components"
git push origin feature/gui
```

---

## 📅 Jour 2: Widgets + main.py

### Objectif
Créer widgets personnalisés et point d'entrée

### Créer `widgets.py`

**PowerShell:**
```powershell
New-Item -ItemType File -Path "p2p_file_sharing\gui\widgets.py"
code p2p_file_sharing\gui\widgets.py
```

**Code:**
```python
"""Widgets personnalisés pour la GUI"""
import tkinter as tk
from tkinter import ttk

class DownloadProgressWidget(ttk.Frame):
    """Widget affichant la progression d'un téléchargement"""
    
    def __init__(self, parent, filename, on_cancel=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.filename = filename
        self.on_cancel = on_cancel
        
        # Nom fichier
        self.label = ttk.Label(
            self, 
            text=f"📥 {filename}", 
            font=('Arial', 10, 'bold')
        )
        self.label.pack(anchor=tk.W, pady=2)
        
        # Progress bar + pourcentage
        progress_frame = ttk.Frame(self)
        progress_frame.pack(fill=tk.X, pady=2)
        
        self.progress = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=300
        )
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.percent_label = ttk.Label(
            progress_frame,
            text="0%",
            width=5
        )
        self.percent_label.pack(side=tk.LEFT)
        
        # Détails (vitesse, temps restant)
        self.details_label = ttk.Label(
            self,
            text="Démarrage...",
            font=('Arial', 8),
            foreground='gray'
        )
        self.details_label.pack(anchor=tk.W)
        
        # Bouton annuler
        if on_cancel:
            self.btn_cancel = ttk.Button(
                self,
                text="❌ Annuler",
                width=10,
                command=self._cancel
            )
            self.btn_cancel.pack(anchor=tk.E, pady=2)
    
    def update_progress(self, percent: int, speed_kbps: float = None, eta_seconds: int = None):
        """
        Met à jour la progression
        
        Args:
            percent: Pourcentage (0-100)
            speed_kbps: Vitesse en KB/s (optionnel)
            eta_seconds: Temps restant en secondes (optionnel)
        """
        self.progress['value'] = percent
        self.percent_label.config(text=f"{percent}%")
        
        # Détails
        details = []
        if speed_kbps is not None:
            details.append(f"{speed_kbps:.1f} KB/s")
        if eta_seconds is not None:
            minutes = eta_seconds // 60
            seconds = eta_seconds % 60
            details.append(f"Temps restant: {minutes}m {seconds}s")
        
        if details:
            self.details_label.config(text=" - ".join(details))
        
        self.update_idletasks()
    
    def _cancel(self):
        """Annule le téléchargement"""
        if self.on_cancel:
            self.on_cancel()
        self.destroy()
    
    def complete(self):
        """Marque comme terminé"""
        self.progress['value'] = 100
        self.percent_label.config(text="100%")
        self.details_label.config(text="✓ Terminé!", foreground='green')
        
        # Désactiver bouton annuler
        if hasattr(self, 'btn_cancel'):
            self.btn_cancel.config(state='disabled')


class PeerInfoWidget(ttk.Frame):
    """Widget affichant des infos sur un peer"""
    
    def __init__(self, parent, peer_id, ip, port, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Status indicator
        self.status_indicator = tk.Canvas(self, width=10, height=10)
        self.status_indicator.pack(side=tk.LEFT, padx=5)
        self._draw_status(True)
        
        # Peer info
        info_frame = ttk.Frame(self)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(
            info_frame,
            text=peer_id,
            font=('Arial', 10, 'bold')
        ).pack(anchor=tk.W)
        
        ttk.Label(
            info_frame,
            text=f"{ip}:{port}",
            font=('Arial', 8),
            foreground='gray'
        ).pack(anchor=tk.W)
    
    def _draw_status(self, online: bool):
        """Dessine l'indicateur de statut"""
        color = 'green' if online else 'red'
        self.status_indicator.create_oval(2, 2, 8, 8, fill=color, outline=color)
    
    def set_online(self, online: bool):
        """Met à jour le statut"""
        self.status_indicator.delete('all')
        self._draw_status(online)
```

### Créer `main.py` (racine du projet)

**PowerShell:**
```powershell
# Fichier déjà créé, le compléter
code main.py
```

**Code complet:**
```python
#!/usr/bin/env python3
"""
P2P File Sharing System - Point d'entrée
Système de partage de fichiers peer-to-peer décentralisé
"""

import sys
import socket
import random
import signal
from pathlib import Path

# Ajouter au path
sys.path.insert(0, str(Path(__file__).parent))

from p2p_file_sharing.utils.logger import setup_logger
from p2p_file_sharing.utils.config import (
    DISCOVERY_PORT, 
    DATABASE_PATH,
    TRANSFER_PORT_START
)
from p2p_file_sharing.gui.main_window import MainWindow

# Imports conditionnels (graceful si modules pas encore mergés)
try:
    from p2p_file_sharing.network.discovery import UDPDiscovery
    from p2p_file_sharing.network.connection import TCPServer
    NETWORK_AVAILABLE = True
except ImportError:
    NETWORK_AVAILABLE = False
    print("⚠️  Network modules not available - running in offline mode")

try:
    from p2p_file_sharing.core.database import Database
    from p2p_file_sharing.core.peer_manager import PeerManager
    from p2p_file_sharing.core.file_manager import FileManager
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    print("⚠️  Core modules not available - running in GUI-only mode")

logger = setup_logger()

def generate_peer_id() -> str:
    """Génère un ID unique pour ce peer"""
    hostname = socket.gethostname()
    random_id = random.randint(1000, 9999)
    return f"{hostname}_{random_id}"

def signal_handler(sig, frame):
    """Gère Ctrl+C proprement"""
    logger.info("Shutdown signal received")
    sys.exit(0)

def main():
    """Point d'entrée principal"""
    print("=" * 60)
    print("         P2P FILE SHARING SYSTEM")
    print("=" * 60)
    logger.info("Application starting...")
    
    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Générer peer ID
    peer_id = generate_peer_id()
    logger.info(f"Local Peer ID: {peer_id}")
    print(f"Peer ID: {peer_id}")
    
    # === Initialize components ===
    
    peer_manager = None
    file_manager = None
    discovery = None
    tcp_server = None
    
    if CORE_AVAILABLE:
        logger.info("Initializing core modules...")
        print("✓ Core modules loaded")
        
        db = Database(DATABASE_PATH)
        peer_manager = PeerManager(db)
        peer_manager.set_local_peer_id(peer_id)
        file_manager = FileManager(db)
    else:
        logger.warning("Core modules not available")
        print("✗ Core modules unavailable")
    
    if NETWORK_AVAILABLE and peer_manager:
        logger.info("Initializing network modules...")
        print("✓ Network modules loaded")
        
        # UDP Discovery
        discovery = UDPDiscovery(peer_id, DISCOVERY_PORT)
        discovery.start_listening(peer_manager.handle_peer_announce)
        discovery.start_broadcasting()
        print(f"  - UDP discovery on port {DISCOVERY_PORT}")
        
        # TCP Server
        def on_message(sender_peer_id, message):
            logger.info(f"Message from {sender_peer_id}: {message['type']}")
            # TODO: Router messages to handlers
        
        tcp_server = TCPServer(TRANSFER_PORT_START)
        tcp_server.start(on_message)
        print(f"  - TCP server on port {TRANSFER_PORT_START}")
    else:
        logger.warning("Network modules not available")
        print("✗ Network modules unavailable (offline mode)")
    
    # === Launch GUI ===
    logger.info("Launching GUI...")
    print("\n🖥️  Launching GUI...")
    print("=" * 60)
    
    gui = MainWindow(peer_manager, file_manager, None)
    
    try:
        gui.run()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Erreur fatale: {e}")
    finally:
        # Cleanup
        logger.info("Shutting down...")
        print("\nShutting down...")
        
        if discovery:
            discovery.stop()
            print("  - Discovery stopped")
        
        if tcp_server:
            tcp_server.stop()
            print("  - TCP server stopped")
        
        if CORE_AVAILABLE:
            db.close()
            print("  - Database closed")
        
        logger.info("Application closed")
        print("Goodbye!")

if __name__ == "__main__":
    main()
```

### Test Jour 2

**PowerShell:**
```powershell
python main.py
```

Devrait lancer la GUI même si modules network/core pas encore mergés.

### Commit Jour 2

```powershell
git add p2p_file_sharing/gui/widgets.py main.py
git commit -m "Add custom widgets and main entry point"
git push origin feature/gui
```

---

## 📅 Jour 3: Documentation + Préparation Merge

### Objectif
Préparer intégration, documenter, tester

### Créer tests d'intégration

**Créer `test_gui_integration.py`:**
```python
"""Test d'intégration GUI avec mocks"""
from p2p_file_sharing.gui.main_window import MainWindow
import tkinter as tk

# Mock managers
class MockPeerManager:
    def get_online_peers(self):
        return [
            {'peer_id': 'test_peer_1', 'ip': '192.168.1.10', 'port': 5001},
            {'peer_id': 'test_peer_2', 'ip': '192.168.1.11', 'port': 5001}
        ]

class MockFileManager:
    def __init__(self):
        self.db = MockDB()
    
    def add_shared_file(self, filepath):
        print(f"Mock: Sharing {filepath}")
        return "mock_file_id_123"

class MockDB:
    def get_all_files(self):
        return [
            {
                'file_id': 'file1',
                'filename': 'test_document.pdf',
                'size': 2500000,
                'owner_peer_id': 'peer_abc',
                'chunks_total': 10
            },
            {
                'file_id': 'file2',
                'filename': 'vacation_photo.jpg',
                'size': 1500000,
                'owner_peer_id': 'peer_xyz',
                'chunks_total': 6
            }
        ]

print("=== Test GUI avec mocks ===\n")
print("Lancement GUI avec données de test...")
print("Fermez la fenêtre pour terminer le test.\n")

# Lancer GUI
pm = MockPeerManager()
fm = MockFileManager()

gui = MainWindow(pm, fm, None)
gui.run()

print("\n✓ Test terminé")
```

### Documentation du code

**Ajouter docstrings manquantes, vérifier:**
- Toutes les classes ont docstrings
- Toutes les méthodes publiques documentées
- Types hints présents
- Commentaires sur parties complexes

### Commit Jour 3

```powershell
git add .
git commit -m "Add widgets, improve documentation, prepare integration"
git push origin feature/gui
```

---

## 🔀 Fin Jour 3: Coordination du Merge

**Votre rôle de Integration Lead:**

### 1. Vérifier que tous ont fini

**Contacter Personne 1 et 2:**
```
"Avez-vous pushé votre PR ? 
Tous les tests passent ?"
```

### 2. Créer votre PR

**Sur GitHub:**
```
Title: "GUI layer and main application entry point"
Description:
- Complete tkinter GUI with all components
- Custom widgets for downloads
- Main entry point with graceful module loading
- Tests with mocks included
```

### 3. Review les autres PRs

**Pour chaque PR (network, core):**
- Lire le code
- Vérifier tests inclus
- Tester checkout leur branche
- Approuver si OK

### 4. Merger dans l'ordre

**Sur GitHub (ordre important!):**
1. Merger `feature/core` d'abord (pas de dépendances)
2. Merger `feature/network` 
3. Merger `feature/gui` en dernier

### 5. Test intégration

**PowerShell:**
```powershell
git checkout main
git pull origin main

# Test
python main.py

# Devrait:
# ✓ Lancer sans erreur
# ✓ GUI s'affiche
# ✓ Si 2 instances: se découvrent
```

### 6. Communiquer résultats

**Sur le chat équipe:**
```
"✓ Merge terminé !
Tout le monde: git pull origin main

Test: python main.py dans 2 terminaux
Les 2 instances doivent se voir après ~10 sec"
```

---

## 📊 Checklist Jours 1-3

- [ ] GUI complète avec tous composants
- [ ] Widgets personnalisés créés
- [ ] main.py avec imports graceful
- [ ] Tests avec mocks fonctionnent
- [ ] Documentation complète
- [ ] Code committé et pushé
- [ ] PR créée
- [ ] PRs autres membres reviewées
- [ ] Merge coordonné (ordre correct)
- [ ] Test intégration réussi

---

## 💡 Conseils Integration Lead

- **Communication:** Sync daily avec équipe
- **Review rapide:** Pas perfectionniste, juste fonctionnel
- **Ordre merge:** Core → Network → GUI
- **Conflits:** Appeler les personnes concernées
- **Tests:** Tester TOUT après chaque merge
- **Rollback:** Si gros problème, `git revert`

---

## 🆘 Problèmes courants

### Conflits Git lors du merge

**Solution:**
```powershell
# Identifier fichiers en conflit
git status

# Éditer fichier, chercher:
#  <<<<<<< HEAD
#  =======
#  >>>>>>> feature/xxx

# Choisir bon code, supprimer marqueurs
# Puis:
git add fichier_resolu.py
git commit
git push
```

### GUI freeze

- Utiliser threads pour opérations longues
- `root.after()` pour updates GUI
- Jamais bloquer dans callbacks

### Import errors après merge

- Vérifier que tous `__init__.py` existent
- Tester imports: `python -c "from p2p_file_sharing.core import *"`
- Refaire `git pull` si nécessaire

---

**Prochaines étapes:** Voir [INTEGRATION.md](INTEGRATION.md) pour jours 4-9
