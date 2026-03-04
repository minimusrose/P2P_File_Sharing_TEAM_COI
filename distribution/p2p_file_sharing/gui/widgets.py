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