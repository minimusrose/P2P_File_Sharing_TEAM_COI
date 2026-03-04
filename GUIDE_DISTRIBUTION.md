# 📦 GUIDE DE DISTRIBUTION

**Comment préparer et distribuer P2P File Sharing**

---

## 🎯 Objectif

Ce guide explique comment créer l'archive finale pour distribuer votre application aux utilisateurs.

---

## ✅ Checklist Avant Distribution

### 1. Vérifier Fonctionnalités

- [ ] Découverte des peers fonctionne
- [ ] Partage de fichiers fonctionne
- [ ] Téléchargement fonctionne
- [ ] Interface graphique s'affiche correctement
- [ ] Pas d'erreurs dans les logs

### 2. Tester sur Machines Propres

**Windows:**
- [ ] Test sur Windows 10
- [ ] Test sur Windows 11
- [ ] Python déjà installé → install.bat fonctionne
- [ ] Python pas installé → message d'erreur clair

**Linux:**
- [ ] Test sur Ubuntu/Debian
- [ ] Test sur Fedora (si possible)
- [ ] ./install.sh fonctionne

### 3. Documentation Complète

- [ ] README.md clair et complet
- [ ] Section dépannage à jour
- [ ] Capture d'écran de l'interface (optionnel)
- [ ] Tutoriel vidéo (optionnel)

---

## 🧹 Étape 1: Nettoyage

### Windows

```powershell
# Lancer le script de nettoyage
.\clean_for_release.bat
```

### Linux

```bash
chmod +x clean_for_release.sh
./clean_for_release.sh
```

**Ce qui est supprimé:**
- Dossiers `data/`, `shared_files/`, `downloads/`
- Tous les `__pycache__/` et `*.pyc`
- Fichiers de test (`.coverage`, `.pytest_cache`)

**Ce qui est conservé:**
- Code source (`p2p_file_sharing/`)
- Scripts d'installation et d'exécution
- Documentation (`README.md`, etc.)

---

## 📦 Étape 2: Créer l'Archive

### Option 1: Archive Complète (Recommandé)

**Contenu:**
```
p2p_file_sharing_v1.0/
├── p2p_file_sharing/     # Code source
├── main.py               # Point d'entrée
├── install.bat           # Installation Windows
├── install.sh            # Installation Linux
├── run.bat               # Lancer Windows
├── run.sh                # Lancer Linux
├── run_debug.bat         # Debug Windows
├── uninstall.bat         # Désinstallation Windows
├── uninstall.sh          # Désinstallation Linux
├── README.md             # Guide utilisateur
└── requirements.txt      # Dépendances (vide)
```

**Windows - Créer ZIP:**

```powershell
# Méthode 1: PowerShell
Compress-Archive -Path `
    p2p_file_sharing, main.py, `
    install.bat, install.sh, `
    run.bat, run.sh, run_debug.bat, `
    uninstall.bat, uninstall.sh, `
    README.md, requirements.txt `
    -DestinationPath p2p_file_sharing_v1.0.zip -Force

# Méthode 2: Interface graphique
# 1. Sélectionner tous les fichiers listés ci-dessus
# 2. Clic droit > Envoyer vers > Dossier compressé
# 3. Renommer en: p2p_file_sharing_v1.0.zip
```

**Linux - Créer TAR.GZ:**

```bash
tar -czf p2p_file_sharing_v1.0.tar.gz \
    p2p_file_sharing/ \
    main.py \
    install.bat install.sh \
    run.bat run.sh run_debug.bat \
    uninstall.bat uninstall.sh \
    README.md requirements.txt
```

### Option 2: Archive Développeur (Avec Documentation)

**Inclut en plus:**
- `README_PROJET.md` - Documentation technique
- `SETUP.md` - Guide développement
- `INTEGRATION.md` - Architecture
- `PACKAGING.md` - Ce guide
- Tous les fichiers de test (`test_*.py`)

```powershell
# Windows
Compress-Archive -Path * -DestinationPath p2p_file_sharing_dev_v1.0.zip -Force

# Linux
tar -czf p2p_file_sharing_dev_v1.0.tar.gz *
```

---

## 📏 Taille Archive

**Attendu:**
- Archive utilisateur: ~100-200 KB
- Archive développeur: ~500 KB - 1 MB

**Si plus gros:**
- Vérifier que `data/` est bien supprimé
- Vérifier absence de gros fichiers de test

---

## 🧪 Étape 3: Test de l'Archive

### Test Complet

1. **Extraire l'archive** dans un nouveau dossier
2. **Tester installation:**
   ```powershell
   # Windows
   .\install.bat
   
   # Linux
   ./install.sh
   ```
3. **Tester exécution:**
   ```powershell
   # Windows
   .\run.bat
   
   # Linux
   ./run.sh
   ```
4. **Tester fonctionnalités:**
   - Découverte de peers
   - Partage de fichier
   - Téléchargement

### Test sur Machine Vierge

**Idéal:** Machine virtuelle (VirtualBox, VMware)

**Windows:**
- VM Windows 10/11
- Python pas installé au départ
- Tester message d'erreur clair

**Linux:**
- VM Ubuntu 22.04 ou Fedora 38
- Python 3.9+ installé

---

## 📤 Étape 4: Distribution

### Plateformes de Partage

**Pour projet étudiant:**
- Email aux professeurs
- Plateforme de cours (Moodle, etc.)
- Google Drive / OneDrive (lien de partage)

**Pour distribution publique:**
- GitHub Releases
- GitLab Releases
- SourceForge

### Exemple GitHub Release

```markdown
## P2P File Sharing v1.0

Système de partage de fichiers peer-to-peer décentralisé.

### 📥 Téléchargement

- **Windows/Linux:** [p2p_file_sharing_v1.0.zip](...)

### ✨ Fonctionnalités

- Découverte automatique des peers
- Partage de fichiers sécurisé
- Interface graphique intuitive

### 📋 Installation

1. Extraire l'archive
2. Lancer `install.bat` (Windows) ou `./install.sh` (Linux)
3. Lancer `run.bat` ou `./run.sh`

### 📖 Documentation

Voir [README.md](README.md) dans l'archive.
```

---

## 📝 Fichiers Accompagnateurs

### Pour Professeurs

**Créer `RAPPORT_RENDU.md`:**

```markdown
# Rapport de Projet - P2P File Sharing

**Équipe:** COI Team  
**Date:** [Date]

## Contenu du Rendu

1. **p2p_file_sharing_v1.0.zip** - Application utilisateur
2. **RAPPORT.pdf** - Rapport technique détaillé
3. **DEMO_VIDEO.mp4** - Vidéo démonstration (optionnel)

## Installation et Test

Voir instructions dans README.md inclus dans l'archive.

## Architecture

Voir INTEGRATION.md pour détails techniques.

## Choix Techniques

- Python 3.9+ (stdlib uniquement)
- Architecture décentralisée
- Protocol UDP (découverte) + TCP (transfert)
- SQLite (base de données)
- Tkinter (interface)

## Difficultés Rencontrées

[À compléter]

## Améliorations Futures

[À compléter]
```

### Vidéo Démo (Optionnel)

**Scénario simple (2-3 minutes):**

1. **Introduction** (15s)
   - "Système P2P de partage de fichiers"
   
2. **Installation** (30s)
   - Extraire archive
   - Lancer install.bat
   
3. **Utilisation** (90s)
   - Lancer application sur 2 machines
   - Partager un fichier
   - Télécharger depuis autre machine
   
4. **Conclusion** (15s)
   - Récapitulatif fonctionnalités

**Outils recommandés:**
- OBS Studio (gratuit, enregistrement écran)
- Windows Game Bar (Win+G)
- SimpleScreenRecorder (Linux)

---

## 🔒 Sécurité Distribution

### Vérifications

- [ ] Pas de mots de passe hardcodés
- [ ] Pas de données personnelles
- [ ] Pas de clés API
- [ ] Code commenté de façon professionnelle

### Checksum (Optionnel)

**Fournir SHA256 de l'archive:**

```powershell
# Windows
Get-FileHash p2p_file_sharing_v1.0.zip -Algorithm SHA256

# Linux
sha256sum p2p_file_sharing_v1.0.tar.gz
```

**Inclure dans RAPPORT.md:**
```
SHA256: abc123...
```

---

## 📊 Métriques Qualité

### Code

- **Lignes de code:** ~1500-2000
- **Fichiers:** ~15
- **Modules:** network, core, gui, utils
- **Tests:** test_*.py (optionnel pour rendu)

### Documentation

- **README.md:** Guide utilisateur complet
- **README_PROJET.md:** Documentation développeur
- **Commentaires:** Code bien commenté

---

## ✅ Checklist Finale

### Avant de Soumettre

- [ ] Archive créée et testée
- [ ] README.md complet et clair
- [ ] Installation testée Windows + Linux
- [ ] Fonctionnalités principales testées
- [ ] Pas de fichiers temporaires dans l'archive
- [ ] Taille archive raisonnable (<5 MB)
- [ ] Scripts d'installation fonctionnent
- [ ] Scripts d'exécution fonctionnent

### Documents Additionnels

- [ ] RAPPORT.pdf (si requis)
- [ ] Vidéo démo (si requis)
- [ ] Présentation PowerPoint (si requis)

### Communication

- [ ] Email de soumission rédigé
- [ ] Instructions claires pour tester
- [ ] Contact pour questions

---

## 📧 Template Email Soumission

```
Objet: [Projet P2P] Rendu Final - Équipe COI

Bonjour,

Veuillez trouver ci-joint notre projet de système P2P de partage de fichiers.

**Contenu:**
- p2p_file_sharing_v1.0.zip (application complète)
- RAPPORT.pdf (documentation technique)

**Installation:**
1. Extraire l'archive
2. Lancer install.bat (Windows) ou ./install.sh (Linux)
3. Lancer run.bat ou ./run.sh

**Test rapide:**
- Lancer sur 2 machines sur même réseau
- Les peers se découvrent automatiquement
- Partager et télécharger un fichier

**Technologies:**
Python 3.9+, Tkinter, Socket, SQLite, Threading

N'hésitez pas si vous avez des questions.

Cordialement,
[Noms équipe]
```

---

## 🎓 Conseils Finaux

### Pour Bonne Impression

1. **Documentation claire** - Pas de jargon inutile
2. **Tests approfondis** - Zéro bug évident
3. **Code propre** - Bien formaté et commenté
4. **Installation facile** - Doit marcher du premier coup

### Erreurs à Éviter

- ❌ Archive avec dossier `__pycache__`
- ❌ Chemins hardcodés absolu (C:\Users\...)
- ❌ Installation qui demande compétences techniques
- ❌ Documentation incomplète ou fausse

### Points Bonus

- ✅ Vidéo démo professionnelle
- ✅ Interface graphique soignée
- ✅ Gestion d'erreurs robuste
- ✅ Documentation exhaustive

---

**Prochaine étape:** Créer l'archive et tester !

**Bon courage pour le rendu ! 🚀**
