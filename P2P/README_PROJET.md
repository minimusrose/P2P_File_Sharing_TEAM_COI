# 🌐 Projet P2P File Sharing - Guide Principal

**Système de partage de fichiers peer-to-peer décentralisé en Python**

## 📋 Vue d'ensemble

- **Durée:** 10 jours
- **Équipe:** 3 personnes
- **Technologies:** Python 3.9+, tkinter, SQLite, UDP/TCP
- **Plateformes:** Windows + Linux

## 🎯 Objectif

Créer un système P2P permettant:
- ✅ Découverte automatique des peers (UDP broadcast)
- ✅ Partage de fichiers de toute taille
- ✅ Téléchargement depuis plusieurs peers simultanément
- ✅ Fragmentation automatique (chunks 256KB)
- ✅ Interface graphique simple (tkinter)
- ✅ Distribution via scripts d'installation

## 👥 Répartition des équipes

### 🔵 Personne 1: Couche Réseau
- **Branche:** `feature/network`
- **Responsabilité:** UDP discovery + TCP communication
- **Fichiers:** `network/discovery.py`, `network/connection.py`, `network/protocol.py`
- **Doc:** [TACHES_PERSONNE1.md](TACHES_PERSONNE1.md)

### 🟢 Personne 2: Logique Métier
- **Branche:** `feature/core`
- **Responsabilité:** File chunking, database, peer management
- **Fichiers:** `core/file_manager.py`, `core/peer_manager.py`, `core/database.py`
- **Doc:** [TACHES_PERSONNE2.md](TACHES_PERSONNE2.md)

### 🟣 Personne 3: GUI & Intégration
- **Branche:** `feature/gui`
- **Responsabilité:** Interface graphique, intégration, lead
- **Fichiers:** `gui/main_window.py`, `gui/widgets.py`, `main.py`
- **Doc:** [TACHES_PERSONNE3.md](TACHES_PERSONNE3.md)
- **Rôle spécial:** Integration Lead (gère les merges)

## 📅 Timeline

### Jour 1 matin (Tous ensemble)
- ⚙️ [Configuration initiale](SETUP.md)
- 📝 [Créer les contrats d'interface](CONTRATS_INTERFACES.md)

### Jours 1-3 (Développement parallèle)
- Chacun travaille sur sa branche
- Voir fichiers TACHES_PERSONNE*.md

### Fin Jour 3 (Premier merge)
- Créer Pull Requests
- Merger vers `main`
- **Test critique:** 2 peers se découvrent

### Jours 4-6 (Intégration)
- ✅ [Guide d'intégration](INTEGRATION.md)
- Jour 4: Network ↔ Core
- Jour 5: Partage de fichiers
- Jour 6: Premier téléchargement ⭐

### Jours 7-9 (Features avancées)
- Jour 7: Multi-peer download
- Jour 8: Téléchargements partiels + polish
- Jour 9: Tests complets avec 3 machines

### Jour 10+ (Packaging)
- 📦 [Guide packaging](PACKAGING.md)
- Scripts install.bat / install.sh
- README final
- Archive de distribution

## 📚 Documentation

| Fichier | Contenu |
|---------|---------|
| [SETUP.md](SETUP.md) | Configuration GitHub, VS Code, structure projet |
| [CONTRATS_INTERFACES.md](CONTRATS_INTERFACES.md) | Interfaces à créer ensemble (Jour 1) |
| [TACHES_PERSONNE1.md](TACHES_PERSONNE1.md) | Détails réseau (UDP/TCP) |
| [TACHES_PERSONNE2.md](TACHES_PERSONNE2.md) | Détails core (chunking/DB) |
| [TACHES_PERSONNE3.md](TACHES_PERSONNE3.md) | Détails GUI + intégration |
| [INTEGRATION.md](INTEGRATION.md) | Jours 4-9 intégration |
| [PACKAGING.md](PACKAGING.md) | Scripts installation + distribution |
| [GIT_COMMANDS.md](GIT_COMMANDS.md) | Référence Git complète |
| [CHECKLIST.md](CHECKLIST.md) | Checklist finale avant livraison |

## 🚀 Démarrage rapide

### 1. Setup initial (Personne 3 fait en premier)
```bash
# Voir SETUP.md pour détails complets
git clone https://github.com/VOTRE_EQUIPE/P2P-File-Sharing.git
cd P2P-File-Sharing
# Créer structure + branches
```

### 2. Chaque personne clone et checkout sa branche
```bash
git clone https://github.com/VOTRE_EQUIPE/P2P-File-Sharing.git
cd P2P-File-Sharing
git checkout feature/VOTRE_MODULE
code .
```

### 3. Créer les contrats d'interface ensemble
Voir [CONTRATS_INTERFACES.md](CONTRATS_INTERFACES.md) - **OBLIGATOIRE Jour 1**

### 4. Développer sur votre branche
Suivre votre fichier TACHES_PERSONNE*.md

### 5. Daily workflow
```bash
# Matin
git checkout main
git pull origin main
git checkout feature/VOTRE_BRANCHE
git merge main

# Pendant dev
git add .
git commit -m "Description"
git push origin feature/VOTRE_BRANCHE

# Soir (après jour 3)
git checkout main
git merge feature/VOTRE_BRANCHE
git push origin main
```

Voir [GIT_COMMANDS.md](GIT_COMMANDS.md) pour tous les détails.

## 🏗️ Architecture finale

```
P2P-File-Sharing/
├── p2p_file_sharing/
│   ├── network/          # Personne 1
│   │   ├── discovery.py
│   │   ├── connection.py
│   │   └── protocol.py
│   ├── core/             # Personne 2
│   │   ├── file_manager.py
│   │   ├── peer_manager.py
│   │   └── database.py
│   ├── gui/              # Personne 3
│   │   ├── main_window.py
│   │   └── widgets.py
│   └── utils/            # Partagé
│       ├── config.py
│       └── logger.py
├── main.py               # Point d'entrée
├── requirements.txt
├── install.bat / .sh     # Scripts installation
├── run.bat / .sh         # Scripts lancement
└── README.md             # Doc utilisateur

Documentation projet/
├── README_PROJET.md      # Ce fichier
├── SETUP.md
├── CONTRATS_INTERFACES.md
├── TACHES_PERSONNE1.md
├── TACHES_PERSONNE2.md
├── TACHES_PERSONNE3.md
├── INTEGRATION.md
├── PACKAGING.md
├── GIT_COMMANDS.md
└── CHECKLIST.md
```

## ⚠️ Points critiques de succès

1. **Jour 1 après-midi:** Créer les contrats d'interface ENSEMBLE
2. **Fin jour 3:** Premier merge - peers se découvrent
3. **Jour 6:** Premier téléchargement complet fonctionne
4. **Jour 9:** Test avec 3 vraies machines
5. **Communication:** Daily standup 5min chaque matin

## 🆘 En cas de problème

### Retard sur timeline
- **Jour 5:** ❌ Cut partial downloads
- **Jour 7:** ❌ Cut multi-peer (1 seul peer OK)
- **Jour 9:** ❌ Skip installer, distribuer Python

### Conflits Git
Voir [GIT_COMMANDS.md](GIT_COMMANDS.md) section "Résolution conflits"

### Bugs réseau
- Vérifier firewall (ports 5000-5010)
- Consulter logs: `~/.p2p_fileshare/p2p.log`
- Tester avec `nc` (netcat)

### GUI freeze
- Utiliser threads pour downloads
- `root.after()` pour updates GUI

## 📞 Communication quotidienne

**Daily Standup (5min call chaque matin):**
```
Chacun répond:
- Hier: Ce que j'ai terminé
- Aujourd'hui: Ce que je vais faire
- Bloqué: Problèmes rencontrés
```

## 🎯 Définition de "Terminé"

Pour dire qu'une feature est terminée:
- ✅ Code committé et pushé
- ✅ Testé localement
- ✅ Docstrings ajoutées
- ✅ Logs en place
- ✅ Pas de print() debug
- ✅ Gestion erreurs (try/except)

## 📊 Indicateurs de progression

### Jour 3
- [ ] 3 PRs créées et mergées
- [ ] `python main.py` lance sans erreur
- [ ] 2 instances se découvrent

### Jour 6
- [ ] Fichier partagé visible sur autres peers
- [ ] Téléchargement complet fonctionne
- [ ] Hash vérifié après download

### Jour 9
- [ ] Test 3 machines réussi
- [ ] Multi-peer download OK
- [ ] Gestion déconnexions

### Jour 10+
- [ ] Scripts install.bat/.sh fonctionnent
- [ ] Archive .zip testée
- [ ] README complet

## 💡 Conseils

- **Commits fréquents:** Minimum 3-4 par jour
- **Tests tôt:** Dès jour 4, tester intégrations
- **Code simple:** Préférer clarté à optimisation
- **Logger partout:** Debug distribué = difficile
- **Communiquer:** Bloquer >2h = demander aide

## 🎓 Ressources

- **Python docs:** https://docs.python.org/3/
- **Socket programming:** https://realpython.com/python-sockets/
- **tkinter:** https://tkdocs.com/
- **Git:** https://git-scm.com/book/fr/v2

---

**Prochaine étape:** Lire [SETUP.md](SETUP.md) pour la configuration initiale

**Bon courage ! 🚀**
