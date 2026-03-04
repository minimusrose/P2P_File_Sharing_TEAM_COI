#!/bin/bash
# Script pour préparer l'archive de distribution
# Nettoie tous les fichiers temporaires et de développement

echo "============================================"
echo "   Préparation Archive Distribution"
echo "============================================"
echo

# 1. Nettoyer les données utilisateur
if [ -d "data" ]; then
    rm -rf data
    echo "[OK] Dossier 'data' supprimé"
fi

if [ -d "shared_files" ]; then
    rm -rf shared_files
    echo "[OK] Dossier 'shared_files' supprimé"
fi

if [ -d "downloads" ]; then
    rm -rf downloads
    echo "[OK] Dossier 'downloads' supprimé"
fi

# 2. Nettoyer __pycache__
echo
echo "Nettoyage des fichiers Python..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
echo "[OK] Fichiers __pycache__ et .pyc supprimés"

# 3. Nettoyer fichiers de test
rm -f .coverage 2>/dev/null
rm -rf .pytest_cache 2>/dev/null
echo "[OK] Fichiers de test nettoyés"

# 4. Nettoyer fichiers Git (optionnel)
# Si vous voulez exclure .git de l'archive, décommentez:
# rm -rf .git
# echo "[OK] Dossier .git supprimé"

echo
echo "============================================"
echo "   Nettoyage terminé !"
echo "============================================"
echo
echo "Pour créer l'archive:"
echo "  tar -czf p2p_file_sharing_v1.0.tar.gz \\"
echo "    p2p_file_sharing/ \\"
echo "    *.bat *.sh \\"
echo "    README.md requirements.txt"
echo
