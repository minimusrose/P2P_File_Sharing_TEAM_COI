#!/bin/bash

echo "============================================"
echo "   Installation P2P File Sharing"
echo "============================================"
echo

# 1. Verifier Python 3
if ! command -v python3 &> /dev/null; then
    echo "[ERREUR] Python 3 n'est pas installe"
    echo
    echo "Sur Ubuntu/Debian:"
    echo "  sudo apt update"
    echo "  sudo apt install python3 python3-pip python3-tk"
    echo
    echo "Sur Fedora:"
    echo "  sudo dnf install python3 python3-pip python3-tkinter"
    echo
    exit 1
fi

echo "[OK] Python detecte"
python3 --version

# 2. Verifier version Python (3.9+)
python3 -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)"
if [ $? -ne 0 ]; then
    echo "[ERREUR] Python 3.9+ requis"
    exit 1
fi

echo "[OK] Version Python compatible"
echo

# 3. Verifier tkinter
python3 -c "import tkinter" &> /dev/null
if [ $? -ne 0 ]; then
    echo "[AVERTISSEMENT] tkinter non disponible"
    echo "Installez avec:"
    echo "  Ubuntu/Debian: sudo apt install python3-tk"
    echo "  Fedora: sudo dnf install python3-tkinter"
    read -p "Continuer quand meme? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "[OK] tkinter disponible"
fi

echo

# 4. Installer dependances (si necessaire)
if [ -f "requirements.txt" ]; then
    echo "[INFO] Installation des dependances..."
    python3 -m pip install --upgrade pip --user
    python3 -m pip install -r requirements.txt --user
    echo "[OK] Dependances installees"
else
    echo "[INFO] Pas de requirements.txt - stdlib uniquement"
fi

echo

# 5. Creer dossiers
mkdir -p data shared_files downloads
echo "[OK] Dossiers crees (data, shared_files, downloads)"

# 6. Rendre run.sh executable
chmod +x run.sh

echo
echo "============================================"
echo "   Installation terminee !"
echo "============================================"
echo
echo "Pour lancer l'application:"
echo "  - Tapez: ./run.sh"
echo "  - Ou: python3 main.py"
echo
