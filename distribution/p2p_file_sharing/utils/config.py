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
