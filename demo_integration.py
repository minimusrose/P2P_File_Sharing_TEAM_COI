#!/usr/bin/env python3
"""
SCRIPT DE DÉMONSTRATION : Différence Jours 1-3 vs Jour 5
==========================================================

Ce script simule les deux états du système pour montrer la différence.

Usage:
    python demo_integration.py mode1    # Simule jours 1-3 (modules isolés)
    python demo_integration.py mode2    # Simule jour 5 (intégration complète)
"""

import sys
import time
from datetime import datetime

# ========================================================================
# SIMULATION JOURS 1-3 : Modules isolés
# ========================================================================

class Mode1_IsolatedModules:
    """Simule le comportement jours 1-3 où modules ne communiquent pas"""
    
    def __init__(self):
        print("\n" + "="*60)
        print("MODE 1 : JOURS 1-3 - Modules Isolés")
        print("="*60 + "\n")
        
        # Initialisation modules
        self.network = Mode1_Network()
        self.core = Mode1_Core()
        self.gui = Mode1_GUI()
        
        print("✓ Modules initialisés séparément\n")
    
    def run_scenario(self):
        """Scénario : Découverte peer + partage fichier"""
        
        print("─── Scénario 1 : Découverte de peer ───\n")
        
        # Network découvre un peer
        peer_info = self.network.discover_peer()
        print(f"Network: Peer découvert → {peer_info}")
        print("❌ Mais... callback ne fait rien !")
        print("❌ PeerManager non connecté")
        print("❌ Database pas mise à jour")
        print("❌ GUI ne voit pas le peer\n")
        
        time.sleep(1)
        
        print("─── Scénario 2 : Partage de fichier ───\n")
        
        # User veut partager fichier
        file_id = self.core.share_file("document.pdf")
        print(f"Core: Fichier chunké → file_id={file_id}")
        print("❌ Mais... aucun broadcast réseau !")
        print("❌ Autres peers pas notifiés")
        print("❌ Fichier reste invisible\n")
        
        time.sleep(1)
        
        print("─── Scénario 3 : Tentative téléchargement ───\n")
        
        # User clique download
        self.gui.download_file("file_123")
        print("❌ Fonctionnalité mockée, ne fait rien !\n")
        
        time.sleep(1)
        
        print("─── RÉSUMÉ MODE 1 ───")
        print("✓ Chaque module fonctionne individuellement")
        print("✓ Tests unitaires OK")
        print("❌ MAIS : Pas de communication inter-modules")
        print("❌ Système non fonctionnel end-to-end\n")


class Mode1_Network:
    """Simulation Network Layer - Jours 1-3"""
    def discover_peer(self):
        return {"peer_id": "peer_abc", "ip": "192.168.1.10", "port": 5001}


class Mode1_Core:
    """Simulation Core Layer - Jours 1-3"""
    def share_file(self, filepath):
        print(f"  1. Calcul hash... {filepath}")
        print(f"  2. Découpe en 4 chunks...")
        print(f"  3. Stockage DB local... OK")
        return "file_abc123"


class Mode1_GUI:
    """Simulation GUI - Jours 1-3"""
    def download_file(self, file_id):
        print(f"  User clique 'Télécharger' sur {file_id}")
        print("  → Messagebox: 'Fonctionnalité après intégration'")


# ========================================================================
# SIMULATION JOUR 5 : Intégration complète
# ========================================================================

class Mode2_IntegratedSystem:
    """Simule le comportement jour 5 avec modules connectés"""
    
    def __init__(self):
        print("\n" + "="*60)
        print("MODE 2 : JOUR 5 - Système Intégré")
        print("="*60 + "\n")
        
        # Database hub central
        self.db = Mode2_Database()
        
        # Modules avec références partagées
        self.peer_manager = Mode2_PeerManager(self.db)
        self.file_manager = Mode2_FileManager(self.db)
        self.network = Mode2_Network(self.peer_manager)
        self.gui = Mode2_GUI(self.peer_manager, self.file_manager, self.network)
        
        print("✓ Modules initialisés avec connexions\n")
        print("   Database ←→ PeerManager")
        print("   Database ←→ FileManager")
        print("   Network  ←→ PeerManager (callback)")
        print("   GUI      ←→ Tous les modules\n")
    
    def run_scenario(self):
        """Scénario : Découverte peer + partage + download"""
        
        print("─── Scénario 1 : Découverte de peer (INTÉGRÉ) ───\n")
        
        # Network découvre peer
        peer_info = self.network.discover_peer()
        print(f"Network: Peer découvert → {peer_info}")
        print("✅ Callback appelé automatiquement !")
        # Le callback déclenche la chaîne suivante automatiquement
        time.sleep(0.5)
        
        # Vérifier résultat
        peers = self.peer_manager.get_online_peers()
        print(f"✅ PeerManager: {len(peers)} peer(s) en ligne")
        gui_peers = self.gui.refresh_peers()
        print(f"✅ GUI actualisée: affiche {len(gui_peers)} peer(s)\n")
        
        time.sleep(1)
        
        print("─── Scénario 2 : Partage fichier (BROADCAST) ───\n")
        
        # User partage fichier
        file_id = self.file_manager.share_file("document.pdf")
        print(f"FileManager: Fichier partagé → file_id={file_id}")
        
        # Broadcast automatique via network
        print("✅ Broadcast FILE_LIST_RESPONSE via TCP")
        self.network.broadcast_file_list([file_id])
        
        # Peer distant reçoit (simulation)
        print("✅ Peer distant: Fichier ajouté à sa liste\n")
        
        time.sleep(1)
        
        print("─── Scénario 3 : Téléchargement RÉEL ───\n")
        
        # User télécharge
        print("User: Clique 'Télécharger' sur document.pdf")
        success = self.gui.download_file(file_id)
        
        if success:
            print("✅ Fichier téléchargé avec succès !")
            print("✅ Hash vérifié : OK")
            print("✅ Fichier créé sur disque\n")
        
        time.sleep(1)
        
        print("─── RÉSUMÉ MODE 2 ───")
        print("✅ Modules communiquent via callbacks et DB")
        print("✅ Découverte UDP → PeerManager → DB → GUI (automatique)")
        print("✅ Partage → Broadcast réseau → Peers notifiés")
        print("✅ Download → Requêtes TCP → Chunks reçus → Fichier assemblé")
        print("✅ Système P2P FONCTIONNEL end-to-end 🎉\n")


class Mode2_Database:
    """Simulation Database avec données"""
    def __init__(self):
        self.peers = []
        self.files = []
    
    def add_peer(self, peer_id, ip, port):
        self.peers.append({"peer_id": peer_id, "ip": ip, "port": port})
        print(f"  → DB: Peer ajouté [{peer_id}]")
    
    def add_file(self, file_id, filename, owner):
        self.files.append({
            "file_id": file_id,
            "filename": filename,
            "owner": owner
        })
        print(f"  → DB: Fichier ajouté [{filename}]")
    
    def get_peers(self):
        return self.peers
    
    def get_files(self):
        return self.files


class Mode2_PeerManager:
    """Simulation PeerManager connecté"""
    def __init__(self, database):
        self.db = database
    
    def handle_peer_announce(self, peer_id, ip, port):
        """Callback appelé par network lors découverte"""
        print(f"  → PeerManager: handle_peer_announce({peer_id})")
        self.db.add_peer(peer_id, ip, port)
    
    def get_online_peers(self):
        return self.db.get_peers()


class Mode2_FileManager:
    """Simulation FileManager connecté"""
    def __init__(self, database):
        self.db = database
    
    def share_file(self, filepath):
        print(f"  1. Calcul hash... {filepath}")
        print(f"  2. Découpe en 4 chunks...")
        file_id = "file_abc123"
        self.db.add_file(file_id, filepath, "local")
        return file_id
    
    def download_file(self, file_id, progress_callback):
        """Téléchargement réel avec chunks"""
        print(f"  1. Récupération infos fichier {file_id}...")
        print(f"  2. Recherche peers ayant le fichier...")
        print(f"  3. Connexion TCP au peer...")
        
        # Simulation download chunks
        for i in range(4):
            print(f"  4. Chunk {i+1}/4 téléchargé... ", end="")
            time.sleep(0.3)
            progress_callback((i+1) * 25)
            print(f"{(i+1)*25}%")
        
        print(f"  5. Assemblage chunks...")
        print(f"  6. Vérification hash... OK")
        return True


class Mode2_Network:
    """Simulation Network Layer connecté"""
    def __init__(self, peer_manager):
        self.peer_manager = peer_manager
        print("  → Network: Callback connecté à PeerManager")
    
    def discover_peer(self):
        """Discovery avec callback automatique"""
        peer_info = {"peer_id": "peer_abc", "ip": "192.168.1.10", "port": 5001}
        
        # ✅ CALLBACK AUTOMATIQUE
        self.peer_manager.handle_peer_announce(
            peer_info["peer_id"],
            peer_info["ip"],
            peer_info["port"]
        )
        
        return peer_info
    
    def broadcast_file_list(self, file_ids):
        print(f"  → Network: Envoi FILE_LIST_RESPONSE à tous peers")
        print(f"     Fichiers: {file_ids}")


class Mode2_GUI:
    """Simulation GUI connectée"""
    def __init__(self, peer_manager, file_manager, network):
        self.peer_manager = peer_manager
        self.file_manager = file_manager
        self.network = network
    
    def refresh_peers(self):
        """Auto-refresh des peers"""
        peers = self.peer_manager.get_online_peers()
        print(f"  → GUI: Liste peers actualisée ({len(peers)} peers)")
        for p in peers:
            print(f"     • {p['peer_id']} @ {p['ip']}")
        return peers
    
    def download_file(self, file_id):
        """Téléchargement avec barre progression"""
        print(f"  → GUI: Lancement download thread...")
        
        def progress_callback(percent):
            print(f"  → GUI: Barre progression = {percent}%")
        
        success = self.file_manager.download_file(file_id, progress_callback)
        return success


# ========================================================================
# MAIN
# ========================================================================

def print_header():
    print("\n" + "="*60)
    print(" DÉMONSTRATION : Différence Jours 1-3 vs Jour 5")
    print("="*60)
    print("\nCe script montre la différence entre :")
    print("  • MODE 1 : Modules isolés (Jours 1-3)")
    print("  • MODE 2 : Système intégré (Jour 5)")
    print("")


def main():
    print_header()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python demo_integration.py mode1    # Modules isolés")
        print("  python demo_integration.py mode2    # Système intégré")
        print("")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == "mode1":
        simulator = Mode1_IsolatedModules()
        simulator.run_scenario()
    
    elif mode == "mode2":
        simulator = Mode2_IntegratedSystem()
        simulator.run_scenario()
    
    else:
        print(f"❌ Mode inconnu: {mode}")
        print("Utilisez 'mode1' ou 'mode2'\n")
        sys.exit(1)
    
    print("="*60)
    print(f"Simulation terminée - {datetime.now().strftime('%H:%M:%S')}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
