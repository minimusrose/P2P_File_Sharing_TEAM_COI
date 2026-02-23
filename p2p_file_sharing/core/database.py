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