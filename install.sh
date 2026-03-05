#!/bin/bash

echo "============================================"
echo "   INSTALLATEUR AUTOMATIQUE"
echo "   P2P File Sharing"
echo "============================================"
echo
echo "Cet installateur va automatiquement:"
echo " - Detecter/installer Python"
echo " - Configurer l'environnement"
echo " - Installer les dependances"
echo
echo "Vous devrez juste repondre Oui (y) ou Non (n)"
echo
read -p "Appuyez sur Entree pour continuer..."
echo

# ============================================
# ETAPE 1: DETECTION PYTHON
# ============================================
echo "[1/5] Detection de Python..."
echo

if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 n'est pas installe"
    echo
    echo "Voulez-vous l'installer automatiquement? (y/n)"
    read -p "> " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation annulee"
        exit 1
    fi
    
    echo
    echo "Detection de votre distribution..."
    
    if command -v apt &> /dev/null; then
        echo "Distribution: Debian/Ubuntu detectee"
        echo "Installation de Python..."
        sudo apt update
        sudo apt install -y python3 python3-pip python3-tk python3-venv
    elif command -v dnf &> /dev/null; then
        echo "Distribution: Fedora detectee"
        echo "Installation de Python..."
        sudo dnf install -y python3 python3-pip python3-tkinter
    elif command -v yum &> /dev/null; then
        echo "Distribution: RHEL/CentOS detectee"
        echo "Installation de Python..."
        sudo yum install -y python3 python3-pip python3-tkinter
    elif command -v pacman &> /dev/null; then
        echo "Distribution: Arch detectee"
        echo "Installation de Python..."
        sudo pacman -S --noconfirm python python-pip tk
    else
        echo "[ERREUR] Distribution non supportee automatiquement"
        echo "Installez Python 3.9+ manuellement"
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        echo "[ERREUR] L'installation a echoue"
        exit 1
    fi
fi

echo "[OK] Python detecte"
python3 --version
echo

# ============================================
# ETAPE 2: VERIFICATION VERSION
# ============================================
echo "[2/5] Verification de la version Python..."
python3 -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)"
if [ $? -ne 0 ]; then
    echo "[AVERTISSEMENT] Python 3.9+ recommande"
    echo "Version actuelle: $(python3 --version)"
    echo
    read -p "Continuer quand meme? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "[OK] Version compatible (3.9+)"
fi

echo

# ============================================
# ETAPE 3: VERIFICATION TKINTER
# ============================================
echo "[3/5] Verification de tkinter (interface graphique)..."
python3 -c "import tkinter" &> /dev/null
if [ $? -ne 0 ]; then
    echo "[AVERTISSEMENT] tkinter non disponible"
    echo
    echo "tkinter est necessaire pour l'interface graphique."
    echo "Voulez-vous l'installer maintenant? (y/n)"
    read -p "> " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v apt &> /dev/null; then
            sudo apt install -y python3-tk
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3-tkinter
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3-tkinter
        fi
    else
        echo "Voulez-vous continuer sans interface graphique?"
        read -p "(y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
else
    echo "[OK] tkinter disponible"
fi

echo

# ============================================
# ETAPE 4: INSTALLATION DEPENDANCES
# ============================================
echo "[4/5] Installation des dependances Python..."
echo

if [ -f "requirements.txt" ]; then
    echo "Les dependances vont etre installees."
    echo "Cela peut prendre quelques minutes..."
    echo
    read -p "Continuer? (y/n) " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo
        
        # Detecter si l'environnement est gere par le systeme (Debian/Ubuntu)
        if python3 -m pip install --help &> /dev/null; then
            # Essayer d'abord avec --user
            echo "Installation avec pip (mode utilisateur)..."
            python3 -m pip install --user -r requirements.txt 2>/dev/null
            
            if [ $? -ne 0 ]; then
                echo
                echo "[INFO] Installation classique impossible (environnement gere)"
                echo
                echo "Voulez-vous utiliser un environnement virtuel (venv)?"
                echo "C'est la methode recommandee sur les systemes modernes."
                read -p "(y/n) " -n 1 -r
                echo
                
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    echo
                    echo "Creation d'un environnement virtuel..."
                    python3 -m venv venv
                    
                    echo "Activation de l'environnement virtuel..."
                    source venv/bin/activate
                    
                    echo "Installation des dependances dans venv..."
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    
                    if [ $? -eq 0 ]; then
                        echo "[OK] Dependances installees dans l'environnement virtuel"
                        echo
                        echo "[INFO] Pour utiliser l'application:"
                        echo "  1. Activez venv: source venv/bin/activate"
                        echo "  2. Lancez: python3 main.py"
                        echo "  OU utilisez simplement: ./run.sh"
                        
                        # Mettre a jour run.sh pour activer venv automatiquement
                        if [ -f "run.sh" ]; then
                            if ! grep -q "venv/bin/activate" run.sh; then
                                echo
                                echo "Mise a jour de run.sh pour auto-activer venv..."
                                sed -i '2i\# Activer environnement virtuel si present\nif [ -d "venv" ]; then\n    source venv/bin/activate\nfi\n' run.sh
                            fi
                        fi
                    else
                        echo "[AVERTISSEMENT] Installation dans venv echouee"
                    fi
                else
                    echo
                    echo "[INFO] L'application fonctionnera avec les modules standards"
                    echo "(tkinter uniquement)"
                fi
            else
                echo "[OK] Dependances installees (mode utilisateur)"
            fi
        else
            echo "[INFO] pip non disponible - utilisation modules standards"
        fi
    else
        echo "Installation des dependances ignoree"
    fi
else
    echo "[INFO] Pas de requirements.txt trouve"
    echo "L'application utilisera uniquement les modules standards"
fi

echo

# ============================================
# ETAPE 5: CREATION DOSSIERS
# ============================================
echo "[5/5] Creation des dossiers necessaires..."

# Creer dossiers avec gestion des permissions
mkdir -p data 2>/dev/null || {
    echo "[AVERTISSEMENT] Impossible de creer 'data' ici"
    echo "Creation dans le dossier personnel..."
    mkdir -p "$HOME/.p2p_file_sharing/data"
    ln -sf "$HOME/.p2p_file_sharing/data" data 2>/dev/null
}

mkdir -p shared_files 2>/dev/null || {
    echo "[AVERTISSEMENT] Impossible de creer 'shared_files' ici"
    mkdir -p "$HOME/.p2p_file_sharing/shared_files"
    ln -sf "$HOME/.p2p_file_sharing/shared_files" shared_files 2>/dev/null
}

mkdir -p downloads 2>/dev/null || {
    echo "[AVERTISSEMENT] Impossible de creer 'downloads' ici"
    mkdir -p "$HOME/.p2p_file_sharing/downloads"
    ln -sf "$HOME/.p2p_file_sharing/downloads" downloads 2>/dev/null
}

echo "[OK] Dossiers crees:"
echo "     - data/         (base de donnees)"
echo "     - shared_files/ (fichiers partages)"
echo "     - downloads/    (telechargements)"

# Rendre run.sh executable si present
if [ -f "run.sh" ]; then
    chmod +x run.sh 2>/dev/null
fi

echo
echo "============================================"
echo "   Installation REUSSIE !"
echo "============================================"
echo
echo "L'application est prete a etre utilisee!"
echo
echo "Pour lancer l'application:"
if [ -f "venv/bin/activate" ]; then
    echo "  - Lancez: ./run.sh (active venv automatiquement)"
    echo "  - Ou manuellement:"
    echo "      source venv/bin/activate"
    echo "      python3 main.py"
else
    echo "  - Lancez: ./run.sh"
    echo "  - Ou: python3 main.py"
fi
echo
read -p "Appuyez sur Entree pour terminer..."
