#!/usr/bin/env python3
"""
Script pour nettoyer la base de données P2P
"""
from pathlib import Path
from p2p_file_sharing.utils.config import DATABASE_PATH

def clear_database():
    """Supprime le fichier de base de données"""
    db_path = Path(DATABASE_PATH)
    
    if db_path.exists():
        db_path.unlink()
        print(f"✅ Base de données supprimée: {db_path}")
    else:
        print(f"ℹ️  Aucune base de données trouvée à: {db_path}")
    
    print("\nLa base sera recréée automatiquement au prochain lancement.")

if __name__ == "__main__":
    confirmation = input("⚠️  Voulez-vous vraiment supprimer TOUTE la base de données? (oui/non): ")
    if confirmation.lower() in ['oui', 'o', 'yes', 'y']:
        clear_database()
    else:
        print("❌ Annulé")
