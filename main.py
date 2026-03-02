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
from p2p_file_sharing.network.message_handler import MessageHandler
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


class NetworkHandler:
    """
    Contrôleur réseau utilisé par la GUI.

    - broadcast_my_files: envoie notre liste de fichiers à tous les peers.
    - request_file_lists: demande la liste de fichiers à tous les peers.
    """

    def __init__(self, peer_manager):
        self.peer_manager = peer_manager

    def _get_online_peers(self):
        if not self.peer_manager or not hasattr(self.peer_manager, "get_online_peers"):
            return []
        return self.peer_manager.get_online_peers()

    def broadcast_my_files(self, my_peer_id, file_list):
        """Broadcast FILE_LIST_RESPONSE à tous les peers connus."""
        from p2p_file_sharing.network.connection import TCPClient
        from p2p_file_sharing.network.protocol import create_message, MessageType

        peers = self._get_online_peers()
        if not peers:
            logger.info("No peers online to broadcast file list")
            return

        message = create_message(
            MessageType.FILE_LIST_RESPONSE,
            my_peer_id,
            {"files": file_list},
        )

        for peer in peers:
            if peer["peer_id"] == my_peer_id:
                continue

            client = TCPClient()
            if not client.connect(peer["ip"], peer["port"]):
                logger.warning(
                    f"Could not connect to peer {peer['peer_id']} "
                    f"at {peer['ip']}:{peer['port']}"
                )
                continue

            try:
                client.send_message(message)
                logger.info(
                    f"Broadcasted {len(file_list)} files to "
                    f"{peer['peer_id']} ({peer['ip']}:{peer['port']})"
                )
            finally:
                client.close()

    def request_file_lists(self, my_peer_id):
        """
        Envoie un FILE_LIST_REQUEST à tous les peers connus.
        Utilisé notamment quand un nouveau peer rejoint le réseau.
        """
        from p2p_file_sharing.network.connection import TCPClient
        from p2p_file_sharing.network.protocol import create_message, MessageType

        logger.info(f"Requesting file lists from all peers (my_peer_id={my_peer_id})")
        
        peers = self._get_online_peers()
        if not peers:
            logger.info("No peers online to request file lists from")
            return
        
        logger.info(f"Found {len(peers)} online peers")

        message = create_message(
            MessageType.FILE_LIST_REQUEST,
            my_peer_id,
            {},
        )

        sent_count = 0
        for peer in peers:
            if peer["peer_id"] == my_peer_id:
                continue

            client = TCPClient()
            if not client.connect(peer["ip"], peer["port"]):
                logger.warning(
                    f"Could not connect to peer {peer['peer_id']} "
                    f"at {peer['ip']}:{peer['port']}"
                )
                continue

            try:
                client.send_message(message)
                sent_count += 1
                logger.info(f"FILE_LIST_REQUEST sent to {peer['peer_id']}")
            except Exception as e:
                logger.error(f"Error sending FILE_LIST_REQUEST to {peer['peer_id']}: {e}")
            finally:
                client.close()
        
        logger.info(f"FILE_LIST_REQUEST sent to {sent_count}/{len(peers)} peers")

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
    network_handler = None
    
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
        # UDP Discovery avec callback peer_manager
        discovery = UDPDiscovery(peer_id, DISCOVERY_PORT)
        discovery.start_listening(peer_manager.handle_peer_announce)
        discovery.start_broadcasting()

        # Créer NetworkHandler pour la GUI (pull/push de listes de fichiers)
        network_handler = NetworkHandler(peer_manager)
        
        # Callback: quand un nouveau peer est découvert, lui demander sa liste de fichiers
        def on_new_peer_discovered(peer_id_discovered, ip, port):
            logger.info(f"New peer discovered: {peer_id_discovered}, requesting file list")
            try:
                from p2p_file_sharing.network.connection import TCPClient
                from p2p_file_sharing.network.protocol import create_message, MessageType
                
                message = create_message(
                    MessageType.FILE_LIST_REQUEST,
                    peer_id,
                    {},
                )
                
                client = TCPClient()
                if client.connect(ip, port):
                    client.send_message(message)
                    logger.info(f"FILE_LIST_REQUEST sent to new peer {peer_id_discovered}")
                    client.close()
            except Exception as e:
                logger.error(f"Error requesting files from new peer: {e}")
        
        peer_manager.on_new_peer_callback = on_new_peer_discovered

        # Création d'une instance de MessageHandler pour router les messages TCP
        message_handler = MessageHandler(peer_manager, file_manager)

        # TCP Server avec handler messages
        def on_tcp_message(sender_peer_id, message):
            logger.info(f"TCP message from {sender_peer_id}: {message['type']}")
            # Router selon type
            message_handler.handle_message(sender_peer_id, message)

        tcp_server = TCPServer(TRANSFER_PORT_START)
        tcp_server.start(on_tcp_message)
        message_handler.tcp_server = tcp_server

        # Créer NetworkHandler pour la GUI (pull/push de listes de fichiers)
        network_handler = NetworkHandler(peer_manager)
        
    # === Launch GUI ===
    logger.info("Launching GUI...")
    print("\n🖥️  Launching GUI...")
    print("=" * 60)
    
    gui = MainWindow(peer_manager, file_manager, network_handler)
    
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