#!/usr/bin/env python3
"""
Script pour supprimer uniquement les fichiers de la base de données
(conserve les peers)
"""
import sqlite3
from p2p_file_sharing.utils.config import DATABASE_PATH

def clear_files_only():
    """Supprime uniquement les fichiers, chunks et local_shared"""
    try:
        conn = sqlite3.connect(str(DATABASE_PATH))
        cursor = conn.cursor()
        
        # Supprimer les données des tables liées aux fichiers
        cursor.execute('DELETE FROM local_shared')
        cursor.execute('DELETE FROM chunks')
        cursor.execute('DELETE FROM files')
        
        conn.commit()
        
        # Afficher le résultat
        cursor.execute('SELECT COUNT(*) FROM files')
        files_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM peers')
        peers_count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"✅ Fichiers supprimés!")
        print(f"   - Fichiers restants: {files_count}")
        print(f"   - Peers conservés: {peers_count}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("⚠️  Cette action va supprimer TOUS les fichiers de la base de données")
    print("   (les peers seront conservés)")
    confirmation = input("\nContinuer? (oui/non): ")
    
    if confirmation.lower() in ['oui', 'o', 'yes', 'y']:
        clear_files_only()
    else:
        print("❌ Annulé")
