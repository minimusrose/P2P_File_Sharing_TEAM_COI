# ⚙️ Configuration Initiale - Jour 1 Matin

**Durée estimée:** 1 heure

## 🎯 Objectif

Mettre en place:
- Repository GitHub avec 3 branches
- Structure de fichiers du projet
- Configuration VS Code
- Chaque personne sur sa branche

---

## Étape 1: Création du repository GitHub (Personne 3)

### 1.1 Créer le repo sur GitHub.com

```
1. Aller sur github.com
2. Cliquer "New Repository" (bouton vert)
3. Remplir:
   - Repository name: P2P-File-Sharing
   - Description: "Système de partage de fichiers peer-to-peer décentralisé"
   - Public ou Private (au choix)
   - ☑️ Add a README file
   - Add .gitignore: Python
   - Choose a license: MIT
4. Cliquer "Create repository"
```

### 1.2 Inviter les membres

```
1. Sur la page du repo: Settings → Collaborators
2. Cliquer "Add people"
3. Ajouter Personne 1 et Personne 2 par username/email
4. Ils recevront une invitation par email
```

### 1.3 Cloner localement

**PowerShell:**
```powershell
cd ~\Documents  # ou votre dossier préféré
git clone https://github.com/VOTRE_USERNAME/P2P-File-Sharing.git
cd P2P-File-Sharing
```

---

## Étape 2: Créer les branches (Personne 3)

**PowerShell:**
```powershell
# Créer et push les 3 branches feature
git checkout -b feature/network
git push -u origin feature/network

git checkout main
git checkout -b feature/core
git push -u origin feature/core

git checkout main
git checkout -b feature/gui
git push -u origin feature/gui

git checkout main
```

**Vérifier:**
```powershell
git branch -a
# Doit afficher:
#   main
#   remotes/origin/feature/core
#   remotes/origin/feature/gui
#   remotes/origin/feature/network
```

---

## Étape 3: Protéger la branche main (Personne 3)

**Sur GitHub.com:**
```
1. Repo → Settings → Branches
2. Cliquer "Add rule"
3. Branch name pattern: main
4. Cocher: ☑️ Require a pull request before merging
5. Cocher: ☑️ Require approvals (1)
6. Cliquer "Create"
```

Cela force les Pull Requests avant merge (bonne pratique).

---

## Étape 4: Créer la structure du projet (Personne 3)

### 4.1 Créer l'arborescence

**PowerShell:**
```powershell
# Créer dossiers
New-Item -ItemType Directory -Path "p2p_file_sharing\network" -Force
New-Item -ItemType Directory -Path "p2p_file_sharing\core" -Force
New-Item -ItemType Directory -Path "p2p_file_sharing\gui" -Force
New-Item -ItemType Directory -Path "p2p_file_sharing\utils" -Force

# Créer fichiers __init__.py
New-Item -ItemType File -Path "p2p_file_sharing\__init__.py"
New-Item -ItemType File -Path "p2p_file_sharing\network\__init__.py"
New-Item -ItemType File -Path "p2p_file_sharing\core\__init__.py"
New-Item -ItemType File -Path "p2p_file_sharing\gui\__init__.py"
New-Item -ItemType File -Path "p2p_file_sharing\utils\__init__.py"

# Créer main.py
New-Item -ItemType File -Path "main.py"
```

### 4.2 Créer .gitignore

**PowerShell:**
```powershell
@"
# Python
__pycache__/
*.py[cod]
*`$py.class
*.so
.Python
env/
venv/
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp

# Project specific
*.db
*.log
downloads/
shared/
.p2p_fileshare/

# OS
.DS_Store
Thumbs.db
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
```

### 4.3 Créer requirements.txt

**PowerShell:**
```powershell
@"
# Pas de dépendances externes nécessaires
# Bibliothèques standard Python suffisent:
# - socket, threading, tkinter, sqlite3, hashlib, json

# Optionnel pour développement:
pytest==7.4.0
black==23.7.0
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8
```

### 4.4 Créer README.md initial

**PowerShell:**
```powershell
@"
# P2P File Sharing System

Système de partage de fichiers peer-to-peer décentralisé en Python.

## Équipe

- **Personne 1:** Couche réseau (UDP/TCP)
- **Personne 2:** Logique métier (chunking, database)
- **Personne 3:** Interface graphique & intégration

## Installation

### Windows
``````
install.bat
run.bat
``````

### Linux
``````
chmod +x install.sh run.sh
./install.sh
./run.sh
``````

## Architecture

``````
p2p_file_sharing/
├── network/    # Discovery UDP + Transfer TCP
├── core/       # File manager, peer manager, database
├── gui/        # Interface tkinter
└── utils/      # Config, logging
``````

## Développement

Voir documentation dans le dossier racine:
- README_PROJET.md
- SETUP.md
- TACHES_PERSONNE*.md
"@ | Out-File -FilePath "README.md" -Encoding UTF8
```

### 4.5 Commit et push

**PowerShell:**
```powershell
git add .
git commit -m "Initial project structure"
git push origin main
```

---

## Étape 5: Configuration VS Code (Tous)

### 5.1 Installer VS Code

Si pas encore installé: https://code.visualstudio.com/

### 5.2 Installer extensions recommandées

Dans VS Code:
```
1. Ctrl+Shift+X (ouvrir Extensions)
2. Installer:
   - Python (Microsoft) 
   - Python Debugger
   - GitLens
   - Error Lens
   - Better Comments (optionnel)
```

### 5.3 Créer .vscode/settings.json (Personne 3)

**PowerShell:**
```powershell
New-Item -ItemType Directory -Path ".vscode" -Force

@"
{
  "python.defaultInterpreterPath": "python",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.rulers": [88],
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  },
  "python.testing.pytestEnabled": true
}
"@ | Out-File -FilePath ".vscode\settings.json" -Encoding UTF8
```

### 5.4 Créer .vscode/launch.json (Personne 3)

**PowerShell:**
```powershell
@"
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Main",
      "type": "python",
      "request": "launch",
      "program": "`${workspaceFolder}/main.py",
      "console": "integratedTerminal"
    }
  ]
}
"@ | Out-File -FilePath ".vscode\launch.json" -Encoding UTF8
```

### 5.5 Commit config VS Code

**PowerShell:**
```powershell
git add .vscode/
git commit -m "Add VS Code configuration"
git push origin main
```

---

## Étape 6: Chaque personne clone et checkout (Personne 1, 2, 3)

### Personne 1 (Réseau)

**PowerShell:**
```powershell
cd ~\Documents
git clone https://github.com/VOTRE_USERNAME/P2P-File-Sharing.git
cd P2P-File-Sharing

# Checkout branche network
git checkout feature/network

# Ouvrir VS Code
code .
```

### Personne 2 (Core)

**PowerShell:**
```powershell
cd ~\Documents
git clone https://github.com/VOTRE_USERNAME/P2P-File-Sharing.git
cd P2P-File-Sharing

# Checkout branche core
git checkout feature/core

# Ouvrir VS Code
code .
```

### Personne 3 (GUI)

**PowerShell:**
```powershell
# Déjà dans le repo
cd P2P-File-Sharing

# Checkout branche gui
git checkout feature/gui

# Ouvrir VS Code
code .
```

---

## Étape 7: Configuration Git identité (Tous)

**Si pas encore configuré globalement:**

**PowerShell:**
```powershell
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"
```

**Vérifier:**
```powershell
git config user.name
git config user.email
```

---

## Étape 8: Test de l'environnement (Tous)

### 8.1 Vérifier Python

**PowerShell:**
```powershell
python --version
# Doit afficher: Python 3.9+ ou supérieur
```

**Si pas installé:**
1. Télécharger depuis https://www.python.org/downloads/
2. ⚠️ **IMPORTANT:** Cocher "Add Python to PATH" lors de l'installation

### 8.2 Vérifier tkinter

**PowerShell:**
```powershell
python -c "import tkinter; print('tkinter OK')"
# Doit afficher: tkinter OK
```

**Si erreur sur Linux:**
```bash
sudo apt install python3-tk
```

### 8.3 Vérifier Git

**PowerShell:**
```powershell
git --version
# Doit afficher: git version 2.x.x
```

### 8.4 Test VS Code Python

1. Ouvrir VS Code
2. Créer fichier test.py
3. Écrire: `print("Hello P2P")`
4. F5 (ou Run → Start Debugging)
5. Doit afficher "Hello P2P" dans terminal
6. Supprimer test.py

---

## ✅ Checklist de fin de setup

**Personne 3 vérifie:**
- [ ] Repository GitHub créé et accessible
- [ ] 3 branches (feature/network, feature/core, feature/gui) existent
- [ ] Branche main protégée
- [ ] Structure de fichiers créée
- [ ] .gitignore, requirements.txt, README.md committés
- [ ] Config VS Code (.vscode/) committée
- [ ] Personne 1 et 2 invitées comme collaborators

**Chaque personne vérifie:**
- [ ] Repo cloné localement
- [ ] Sur la bonne branche (feature/VOTRE_MODULE)
- [ ] VS Code ouvert avec extensions installées
- [ ] Python 3.9+ installé et dans PATH
- [ ] tkinter fonctionne
- [ ] Git configuré (name, email)
- [ ] Peut commit et push

**Test final (tous ensemble):**
```powershell
# Chacun sur sa branche
git status
# Doit afficher: On branch feature/VOTRE_MODULE

# Créer fichier test
"Test Personne X" | Out-File -FilePath "test_$env:USERNAME.txt"
git add .
git commit -m "Test commit personne X"
git push origin feature/VOTRE_MODULE

# Vérifier sur GitHub que le commit est visible
```

---

## 📋 Structure finale attendue

```
P2P-File-Sharing/
├── .git/
├── .vscode/
│   ├── settings.json
│   └── launch.json
├── p2p_file_sharing/
│   ├── __init__.py
│   ├── network/
│   │   └── __init__.py
│   ├── core/
│   │   └── __init__.py
│   ├── gui/
│   │   └── __init__.py
│   └── utils/
│       └── __init__.py
├── .gitignore
├── main.py (vide pour l'instant)
├── requirements.txt
└── README.md
```

---

## 🚀 Prochaines étapes

1. **Tous ensemble:** Lire [CONTRATS_INTERFACES.md](CONTRATS_INTERFACES.md)
2. **Créer les interfaces** (Jour 1 après-midi)
3. **Commencer le développement** selon TACHES_PERSONNE*.md

---

## 🆘 Problèmes courants

### Python not found (Windows)

**Solution:**
```powershell
# Ajouter Python au PATH manuellement
$env:Path += ";C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python39"
```

Ou réinstaller Python en cochant "Add to PATH".

### Git push rejected

**Erreur:** "Updates were rejected because the remote contains work..."

**Solution:**
```powershell
git pull origin VOTRE_BRANCHE
# Résoudre conflits si nécessaire
git push origin VOTRE_BRANCHE
```

### VS Code n'ouvre pas le terminal

**Solution:**
```
File → Preferences → Settings
Chercher: terminal.integrated.shell.windows
Vérifier que c'est: powershell.exe
```

### Permission denied (Linux)

**Solution:**
```bash
chmod +x script.sh
```

---

## 📞 Support

Si bloquer >30 minutes sur le setup:
- Vérifier les logs d'erreur
- Chercher l'erreur sur Google
- Demander à l'équipe
- Poser question sur le chat du groupe

**Le setup doit être terminé avant midi du Jour 1 !**

---

**Setup terminé ! → Passer à [CONTRATS_INTERFACES.md](CONTRATS_INTERFACES.md)**
