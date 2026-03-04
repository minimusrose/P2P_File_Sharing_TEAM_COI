#!/bin/bash

# Verifier installation
if [ ! -d "data" ]; then
    echo "[ERREUR] Dossier 'data' absent"
    echo "Lancez ./install.sh d'abord !"
    exit 1
fi

# Lancer l'app
python3 main.py
