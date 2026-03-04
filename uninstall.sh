#!/bin/bash

echo "============================================"
echo "   Désinstallation P2P File Sharing"
echo "============================================"
echo
echo "ATTENTION: Cette opération va supprimer:"
echo "  - Le dossier 'data' (base de données et logs)"
echo "  - Le dossier 'shared_files' (fichiers partagés)"
echo "  - Le dossier 'downloads' (fichiers téléchargés)"
echo
echo "Les fichiers source du programme seront conservés."
echo

read -p "Continuer? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Désinstallation annulée."
    exit 0
fi

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

echo
echo "============================================"
echo "   Désinstallation terminée !"
echo "============================================"
echo
echo "Pour réinstaller, lancez: ./install.sh"
echo
