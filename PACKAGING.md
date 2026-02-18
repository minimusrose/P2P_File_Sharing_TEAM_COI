# 📦 PACKAGING.md - Jour 10+ Déploiement

**Phase finale: Scripts d'installation et distribution**

Vous avez un système fonctionnel. Il faut maintenant le packager pour:
- Distribution facile aux utilisateurs
- Installation simple sans compétences techniques
- Portabilité Windows + Linux

---

## 🎯 Objectifs Packaging

### Ce qu'on veut

```
Utilisateur reçoit: p2p_file_sharing.zip
  ↓
Extrait l'archive
  ↓
Double-clic: install.bat (Windows) ou install.sh (Linux)
  ↓
Installe Python + dépendances automatiquement
  ↓
Double-clic: run.bat ou run.sh pour lancer l'app
  ↓
GUI s'ouvre → Ready !
```

### Ce qu'on NE fait PAS

- ❌ Pas de .exe compilé (complexe, OS-specific)
- ❌ Pas de setup.msi ou .deb (overkill pour projet étudiant)
- ✅ Simple: Scripts + Python source

---

## 📁 Structure Finale Archive

```
p2p_file_sharing/
├── install.bat              ← Installation Windows
├── install.sh               ← Installation Linux
├── run.bat                  ← Lancer app Windows
├── run.sh                   ← Lancer app Linux
├── README.md                ← Guide utilisateur
├── requirements.txt         ← Dépendances (si besoin)
├── p2p_file_sharing/        ← Code source
│   ├── __init__.py
│   ├── main.py
│   ├── network/
│   ├── core/
│   ├── gui/
│   └── utils/
├── data/                    ← Créé auto (DB, logs)
└── shared_files/            ← Créé auto
```

---

## 🪟 Windows: install.bat

**But:** Vérifier Python, installer dépendances, préparer dossiers

**Créer `install.bat` à la racine:**

```batch
@echo off
echo ============================================
echo    Installation P2P File Sharing
echo ============================================
echo.

REM 1. Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans PATH
    echo.
    echo Telechargez Python 3.9+ depuis: https://www.python.org/downloads/
    echo Cochez "Add Python to PATH" pendant l'installation !
    echo.
    pause
    exit /b 1
)

echo [OK] Python detecte
python --version

REM 2. Vérifier version Python (3.9+)
python -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)"
if errorlevel 1 (
    echo [ERREUR] Python 3.9+ requis
    pause
    exit /b 1
)

echo [OK] Version Python compatible
echo.

REM 3. Installer dépendances (si requirements.txt existe)
if exist requirements.txt (
    echo [INFO] Installation des dependances...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [AVERTISSEMENT] Certaines dependances ont echoue
        echo Continuez quand meme, tkinter est inclus avec Python
    ) else (
        echo [OK] Dependances installees
    )
) else (
    echo [INFO] Pas de requirements.txt - stdlib uniquement
)

echo.

REM 4. Créer dossiers nécessaires
if not exist "data" mkdir data
if not exist "shared_files" mkdir shared_files
echo [OK] Dossiers crees

echo.
echo ============================================
echo    Installation terminee !
echo ============================================
echo.
echo Pour lancer l'application:
echo   - Double-cliquez sur run.bat
echo   - Ou tapez: python -m p2p_file_sharing.main
echo.
pause
```

### Test install.bat

```powershell
# Tester le script
.\install.bat

# Résultat attendu:
# [OK] Python détecté
# [OK] Version compatible
# [OK] Dépendances installées
# [OK] Dossiers créés
```

---

## 🐧 Linux: install.sh

**Créer `install.sh` à la racine:**

```bash
#!/bin/bash

echo "============================================"
echo "   Installation P2P File Sharing"
echo "============================================"
echo

# 1. Vérifier Python 3
if ! command -v python3 &> /dev/null; then
    echo "[ERREUR] Python 3 n'est pas installé"
    echo
    echo "Sur Ubuntu/Debian:"
    echo "  sudo apt update"
    echo "  sudo apt install python3 python3-pip python3-tk"
    echo
    exit 1
fi

echo "[OK] Python détecté"
python3 --version

# 2. Vérifier version Python (3.9+)
python3 -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)"
if [ $? -ne 0 ]; then
    echo "[ERREUR] Python 3.9+ requis"
    exit 1
fi

echo "[OK] Version Python compatible"
echo

# 3. Vérifier tkinter
python3 -c "import tkinter" &> /dev/null
if [ $? -ne 0 ]; then
    echo "[AVERTISSEMENT] tkinter non disponible"
    echo "Installez avec: sudo apt install python3-tk"
    read -p "Continuer quand même? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "[OK] tkinter disponible"
fi

echo

# 4. Installer dépendances (si nécessaire)
if [ -f "requirements.txt" ]; then
    echo "[INFO] Installation des dépendances..."
    python3 -m pip install --upgrade pip --user
    python3 -m pip install -r requirements.txt --user
    echo "[OK] Dépendances installées"
else
    echo "[INFO] Pas de requirements.txt - stdlib uniquement"
fi

echo

# 5. Créer dossiers
mkdir -p data shared_files
echo "[OK] Dossiers créés"

# 6. Rendre run.sh exécutable
chmod +x run.sh

echo
echo "============================================"
echo "   Installation terminée !"
echo "============================================"
echo
echo "Pour lancer l'application:"
echo "  - Tapez: ./run.sh"
echo "  - Ou: python3 -m p2p_file_sharing.main"
echo
```

**Rendre exécutable:**

```bash
chmod +x install.sh
./install.sh
```

---

## 🚀 Windows: run.bat

**But:** Lancer l'app sans fenêtre console (pythonw)

**Créer `run.bat`:**

```batch
@echo off

REM Vérifier que installation a été faite
if not exist "data" (
    echo [ERREUR] Dossier 'data' absent
    echo Lancez install.bat d'abord !
    pause
    exit /b 1
)

REM Lancer avec pythonw (pas de console) si disponible
where pythonw >nul 2>&1
if %errorlevel% equ 0 (
    start pythonw -m p2p_file_sharing.main
) else (
    REM Fallback sur python normal
    start python -m p2p_file_sharing.main
)

REM Note: start détache le processus
```

### Alternative: run.bat avec console visible (debug)

**Créer aussi `run_debug.bat`:**

```batch
@echo off
echo Lancement P2P File Sharing...
python -m p2p_file_sharing.main
pause
```

---

## 🐧 Linux: run.sh

**Créer `run.sh`:**

```bash
#!/bin/bash

# Vérifier installation
if [ ! -d "data" ]; then
    echo "[ERREUR] Dossier 'data' absent"
    echo "Lancez ./install.sh d'abord !"
    exit 1
fi

# Lancer l'app
python3 -m p2p_file_sharing.main
```

**Rendre exécutable:**

```bash
chmod +x run.sh
./run.sh
```

---

## 📄 requirements.txt (Optionnel)

**Si vous aviez ajouté des dépendances externes:**

```
# Aucune dépendance externe pour version de base
# Tout est dans la stdlib Python

# Si vous aviez ajouté cryptography:
# cryptography>=41.0.0

# Si vous aviez ajouté requests:
# requests>=2.31.0
```

**Note:** Projet de base n'a PAS besoin de requirements.txt (stdlib uniquement)

---

## 📖 README.md Utilisateur

**Créer `README.md` final (différent du README_PROJET.md dev):**

```markdown
# 🌐 P2P File Sharing

**Système de partage de fichiers décentralisé peer-to-peer**

---

## ✨ Fonctionnalités

- 🔍 Découverte automatique des peers sur le réseau local
- 📁 Partage de fichiers entre utilisateurs
- ⬇️ Téléchargement sécurisé avec vérification d'intégrité (SHA256)
- 🖥️ Interface graphique simple
- 🌐 Compatible Windows + Linux

---

## 📋 Prérequis

- **Python 3.9 ou supérieur**
- **Connexion réseau local** (même WiFi/Ethernet)

---

## 🚀 Installation

### Windows

1. Extraire l'archive `p2p_file_sharing.zip`
2. Double-cliquer sur `install.bat`
3. Attendre fin de l'installation

### Linux

1. Extraire l'archive
2. Ouvrir terminal dans le dossier
3. Taper: `chmod +x install.sh && ./install.sh`

---

## ▶️ Utilisation

### Lancer l'application

**Windows:** Double-cliquer `run.bat`

**Linux:** Terminal → `./run.sh`

### Partager un fichier

1. Cliquer bouton **"Partager fichier"**
2. Sélectionner le fichier sur votre disque
3. Le fichier apparaît dans la liste des fichiers partagés
4. Les autres peers le verront automatiquement

### Télécharger un fichier

1. Regarder la liste des fichiers disponibles
2. Sélectionner un fichier
3. Cliquer **"Télécharger"**
4. Choisir où enregistrer
5. Attendre la barre de progression

---

## 🔧 Dépannage

### Problème: Peers ne se voient pas

**Cause:** Firewall bloque les ports

**Solution:**
- **Windows:** Autoriser Python dans Pare-feu Windows
  - Panneau de configuration → Pare-feu → Autoriser une app
  - Ajouter Python (python.exe et pythonw.exe)
- **Linux:** 
  ```bash
  sudo ufw allow 5000/udp
  sudo ufw allow 5001/tcp
  ```

### Problème: "Python n'est pas installé"

**Solution:**
- Télécharger Python 3.9+ depuis [python.org](https://www.python.org/downloads/)
- **IMPORTANT:** Cocher "Add Python to PATH" pendant l'installation

### Problème: "tkinter non disponible" (Linux)

**Solution:**
```bash
sudo apt update
sudo apt install python3-tk
```

### Problème: GUI ne s'ouvre pas

**Solution:**
- Lancer `run_debug.bat` (Windows) pour voir les erreurs
- Ou terminal: `python -m p2p_file_sharing.main`
- Vérifier logs dans `data/p2p.log`

### Problème: Téléchargement échoue

**Causes possibles:**
1. Peer émetteur déconnecté → Réessayer
2. Fichier trop volumineux → Patience
3. Réseau instable → Vérifier connexion WiFi

---

## 📂 Structure Dossiers

```
p2p_file_sharing/
├── data/           ← Base de données et logs
├── shared_files/   ← Fichiers que vous partagez
└── downloads/      ← Fichiers téléchargés
```

---

## ⚠️ Limitations

- Fonctionne uniquement sur réseau local (pas Internet)
- Maximum ~100 MB par fichier (selon réseau)
- Pas de chiffrement des données (réseau privé uniquement)

---

## 📞 Support

En cas de problème, vérifier:
1. Logs dans `data/p2p.log`
2. Firewall autorise Python
3. Tous sur le même réseau WiFi

---

## 👥 Développeurs

Projet P2P File Sharing - 2024

Licence: MIT
```

---

## 📦 Créer Archive de Distribution

### Windows (PowerShell)

```powershell
# 1. Nettoyer fichiers inutiles
Remove-Item -Recurse -Force data, shared_files, __pycache__ -ErrorAction SilentlyContinue

# Nettoyer aussi dans sous-dossiers
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
Get-ChildItem -Recurse -Filter ".coverage" | Remove-Item -Force

# 2. Créer archive ZIP
Compress-Archive -Path .\p2p_file_sharing, .\install.bat, .\install.sh, .\run.bat, .\run.sh, .\run_debug.bat, .\README.md -DestinationPath p2p_file_sharing_v1.0.zip -Force

Write-Host "Archive créée: p2p_file_sharing_v1.0.zip" -ForegroundColor Green
```

### Linux

```bash
# 1. Nettoyer
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
rm -rf data shared_files

# 2. Créer archive
tar -czf p2p_file_sharing_v1.0.tar.gz \
    p2p_file_sharing/ \
    install.bat install.sh \
    run.bat run.sh \
    README.md

echo "Archive créée: p2p_file_sharing_v1.0.tar.gz"
```

---

## ✅ Checklist Distribution

### Avant archivage

- [ ] `install.bat` et `install.sh` testés
- [ ] `run.bat` et `run.sh` fonctionnent
- [ ] `README.md` utilisateur rédigé
- [ ] Tous les `__pycache__` supprimés
- [ ] Pas de fichiers `.db` ou `.log` inclus
- [ ] Pas de données sensibles

### Test sur machine vierge

**Machine Windows:**
- [ ] Python non installé → install.bat donne bon message
- [ ] Python installé → install.bat réussit
- [ ] run.bat lance l'app
- [ ] GUI s'affiche correctement

**Machine Linux:**
- [ ] ./install.sh fonctionne
- [ ] tkinter détecté ou bon message erreur
- [ ] ./run.sh lance l'app

### Test fonctionnel

- [ ] 2 machines extraient l'archive
- [ ] Les 2 installent et lancent
- [ ] Se découvrent mutuellement
- [ ] Partage fichier fonctionne
- [ ] Téléchargement fonctionne

---

## 🎓 Scripts Avancés (Bonus)

### Auto-update script

**`update.bat` (Windows):**

```batch
@echo off
echo Mise a jour P2P File Sharing...
git pull origin main
python -m pip install -r requirements.txt --upgrade
echo Mise a jour terminee !
pause
```

### Uninstall script

**`uninstall.bat`:**

```batch
@echo off
echo Suppression des donnees P2P File Sharing...
rmdir /S /Q data shared_files downloads
echo Donnees supprimees. Les fichiers source restent.
pause
```

---

## 📊 Métriques Archive

**Taille attendue:**
- Source code: ~50-100 KB
- Scripts: ~10 KB
- Archive totale: **~50-150 KB**

**Très léger car:**
- Pas de dépendances externes
- Pas de binaires
- Python interprété

---

## 💡 Conseils Finaux

### Pour distribution publique

1. **Tester sur machines propres** (VMs recommandées)
2. **Documenter toutes les erreurs possibles**
3. **Fournir vidéo démo** (1-2 min)
4. **Indiquer limitations clairement**

### Pour professeurs

**Inclure avec l'archive:**
- `RAPPORT.pdf` (architecture, choix techniques)
- `DEMO_SCRIPT.md` (scénario démonstration)
- **Ce dossier de documentation** (README_PROJET.md, SETUP.md, etc.)

### Pour futurs mainteneurs

**Si vous continuez le projet:**
- Ajouter tests unitaires
- CI/CD avec GitHub Actions
- Versioning sémantique (v1.0.0)
- Changelog

---

**Prochaine étape:** [GIT_COMMANDS.md](GIT_COMMANDS.md) - Référence Git complète
