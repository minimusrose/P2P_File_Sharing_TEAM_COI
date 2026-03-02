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
        self._initial_file_request_done = False
        
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
            if not self.file_manager:
                messagebox.showwarning("Erreur", "File manager non disponible")
                return

            # 1. Ajouter le fichier côté core
            file_id = self.file_manager.add_shared_file(filepath)
            if not file_id:
                messagebox.showerror("Erreur", "Échec du partage")
                return

            # 2. Notifier la couche réseau pour broadcast (si disponible)
            #    On s'attend à ce que network_handler expose une méthode
            #    pour déclencher le broadcast (par exemple: broadcast_my_files)
            if self.network and hasattr(self.network, "broadcast_my_files"):
                try:
                    # Récupérer la liste de nos fichiers formatée pour le réseau
                    if hasattr(self.file_manager, "get_my_file_list"):
                        file_list = self.file_manager.get_my_file_list()
                    else:
                        file_list = []

                    # Récupérer notre peer_id local via le peer_manager, si dispo
                    my_peer_id = None
                    if self.peer_manager and hasattr(
                        self.peer_manager, "local_peer_id"
                    ):
                        my_peer_id = self.peer_manager.local_peer_id

                    # L'objet network_handler devrait savoir accéder au tcp_server
                    # et utiliser message_handler.broadcast_my_files en interne.
                    self.network.broadcast_my_files(
                        my_peer_id=my_peer_id,
                        file_list=file_list,
                    )
                    logger.info(
                        "Broadcast request for shared files sent to network layer"
                    )
                except Exception as e:
                    logger.error(
                        f"Error while broadcasting file list: {e}", exc_info=True
                    )

            # 3. Feedback GUI
            self.status_var.set(f"Fichier partagé: {filepath}")
            messagebox.showinfo(
                "Succès",
                f"Fichier partagé!\nID: {file_id}",
            )
            self.update_file_list()

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

        # Lors du premier rafraîchissement, si on a un réseau et un peer_id local,
        # demander automatiquement la liste des fichiers aux autres peers.
        if (
            not self._initial_file_request_done
            and self.network
            and hasattr(self.network, "request_file_lists")
            and self.peer_manager
            and hasattr(self.peer_manager, "local_peer_id")
            and self.peer_manager.local_peer_id is not None
        ):
            try:
                self.network.request_file_lists(self.peer_manager.local_peer_id)
                logger.info("Initial FILE_LIST_REQUEST sent to peers")
                self._initial_file_request_done = True  # Marquer comme fait seulement si succès
            except Exception as e:
                logger.error(f"Error sending initial FILE_LIST_REQUEST: {e}", exc_info=True)
        
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
        # En cas de refresh manuel, on redemande aussi les listes de fichiers
        if (
            self.network
            and hasattr(self.network, "request_file_lists")
            and self.peer_manager
            and hasattr(self.peer_manager, "local_peer_id")
        ):
            try:
                self.network.request_file_lists(self.peer_manager.local_peer_id)
            except Exception as e:
                logger.error(f"Error requesting file lists on refresh: {e}")

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