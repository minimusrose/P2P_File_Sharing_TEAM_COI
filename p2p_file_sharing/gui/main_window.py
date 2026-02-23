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
