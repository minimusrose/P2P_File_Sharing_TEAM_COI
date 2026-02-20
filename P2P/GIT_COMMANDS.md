# 🔀 GIT_COMMANDS.md - Référence Git Complète

**Manuel Git pour le projet P2P File Sharing**

Commandes essentielles et workflows Git pour vos 10 jours de développement.

---

## 📚 Table des Matières

1. [Configuration Initiale](#configuration-initiale)
2. [Workflow Quotidien](#workflow-quotidien)
3. [Branches](#branches)
4. [Commits](#commits)
5. [Synchronisation](#synchronisation)
6. [Résolution Conflits](#résolution-conflits)
7. [Historique & Diagnostic](#historique--diagnostic)
8. [Commandes d'Urgence](#commandes-durgence)
9. [Scénarios Courants](#scénarios-courants)

---

## ⚙️ Configuration Initiale

### Première fois avec Git

```powershell
# Configurer identité (pour les commits)
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"

# Vérifier config
git config --list

# Affichage couleur (plus lisible)
git config --global color.ui auto

# Éditeur par défaut (VS Code)
git config --global core.editor "code --wait"
```

### Cloner le repository

```powershell
# Cloner depuis GitHub
git clone https://github.com/VOTRE_COMPTE/p2p_file_sharing.git

# Entrer dans le dossier
cd p2p_file_sharing

# Vérifier remotes
git remote -v
# Devrait afficher:
# origin  https://github.com/VOTRE_COMPTE/p2p_file_sharing.git (fetch)
# origin  https://github.com/VOTRE_COMPTE/p2p_file_sharing.git (push)
```

### Checkout votre branche de travail

```powershell
# Personne 1
git checkout feature/network

# Personne 2
git checkout feature/core

# Personne 3
git checkout feature/gui
```

---

## 📆 Workflow Quotidien

### Matin (début de journée)

```powershell
# 1. Vérifier sur quelle branche vous êtes
git branch
# L'étoile * indique votre branche actuelle

# 2. Récupérer dernières modifications du remote
git fetch origin

# 3. Vérifier si votre branche est à jour
git status

# 4. (Optionnel) Mettre à jour depuis main si nécessaire
# SEULEMENT après jour 3 !
git merge origin/main

# 5. Voir ce qui a changé
git log --oneline -5   # 5 derniers commits
```

### Pendant la journée (après modifications)

```powershell
# 1. Voir fichiers modifiés
git status

# Résultat exemple:
# modified:   p2p_file_sharing/network/discovery.py
# new file:   tests/test_discovery.py

# 2. Voir les changements ligne par ligne
git diff

# 3. Ajouter fichiers au staging
git add p2p_file_sharing/network/discovery.py
git add tests/test_discovery.py

# Ou tout ajouter d'un coup
git add .

# 4. Vérifier ce qui est staged
git status

# 5. Commit avec message descriptif
git commit -m "Implement UDP discovery broadcast and listen"

# 6. Push vers GitHub
git push origin feature/network  # Remplacer par votre branche
```

### Soir (fin de journée)

```powershell
# 1. Commit tout ce qui reste
git add .
git commit -m "End of day X - [résumé travail]"

# 2. Push
git push origin feature/network

# 3. (Optionnel) Créer tag pour marquer jalon
git tag jour-1-complet
git push origin jour-1-complet
```

---

## 🌿 Branches

### Voir branches

```powershell
# Branches locales
git branch

# Toutes les branches (remote inclus)
git branch -a

# Branches avec dernier commit
git branch -v
```

### Créer et changer de branche

```powershell
# Créer branche
git branch feature/nouvelle-feature

# Changer de branche
git checkout feature/nouvelle-feature

# Créer ET changer en 1 commande
git checkout -b feature/nouvelle-feature

# Retourner à main
git checkout main
```

### Supprimer branche

```powershell
# Supprimer branche locale (après merge)
git branch -d feature/network

# Forcer suppression (si pas merge)
git branch -D feature/network

# Supprimer branche remote
git push origin --delete feature/network
```

### Renommer branche

```powershell
# Renommer branche actuelle
git branch -m nouveau-nom

# Renommer autre branche
git branch -m ancien-nom nouveau-nom
```

---

## 📝 Commits

### Commit simple

```powershell
# Ajouter ET commit en 1 commande (fichiers déjà trackés)
git commit -am "Message de commit"

# Commit standard (2 étapes)
git add fichier.py
git commit -m "Message"
```

### Messages de commit

**Format recommandé:**

```
<type>: <description courte>

<description longue optionnelle>
```

**Types courants:**
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction bug
- `docs:` Documentation
- `test:` Ajout tests
- `refactor:` Refactorisation code

**Exemples:**

```powershell
git commit -m "feat: Add UDP broadcast discovery"

git commit -m "fix: Handle timeout in TCP connection"

git commit -m "test: Add unit tests for file chunking"

git commit -m "docs: Update README with installation instructions"
```

### Modifier dernier commit

```powershell
# Oublié un fichier dans le dernier commit
git add fichier_oublie.py
git commit --amend --no-edit

# Changer message du dernier commit
git commit --amend -m "Nouveau message"

# ⚠️ Ne JAMAIS amend un commit déjà pushé !
```

### Annuler commit

```powershell
# Annuler dernier commit (garder changements)
git reset --soft HEAD~1

# Annuler ET supprimer changements (DANGER !)
git reset --hard HEAD~1

# Annuler les 2 derniers commits
git reset --soft HEAD~2
```

---

## 🔄 Synchronisation

### Pull (récupérer et fusionner)

```powershell
# Pull = fetch + merge
git pull origin main

# Pull votre branche
git pull origin feature/network
```

### Push (envoyer)

```powershell
# Push vers votre branche
git push origin feature/network

# Push toutes les branches
git push --all origin

# Push avec tags
git push --tags
```

### Fetch (récupérer sans fusionner)

```powershell
# Récupérer infos de toutes les branches
git fetch origin

# Voir ce qui a changé
git log HEAD..origin/main --oneline

# Fusionner manuellement après
git merge origin/main
```

---

## ⚔️ Résolution Conflits

### Détecter conflits

```powershell
# Merger main dans votre branche
git merge main

# Si conflits:
# Auto-merging p2p_file_sharing/utils/config.py
# CONFLICT (content): Merge conflict in p2p_file_sharing/utils/config.py
# Automatic merge failed; fix conflicts and then commit the result.

# Voir fichiers en conflit
git status
# Both modified:   p2p_file_sharing/utils/config.py
```

### Résoudre conflits

**1. Ouvrir le fichier en conflit:**

```python
# Fichier contient des marqueurs:
<<<<<<< HEAD
# Votre version
DISCOVERY_PORT = 5000
=======
# Version de main
DISCOVERY_PORT = 5050
>>>>>>> main
```

**2. Éditer manuellement:**

```python
# Choisir la bonne valeur ou combiner
DISCOVERY_PORT = 5000
```

**3. Marquer comme résolu:**

```powershell
git add p2p_file_sharing/utils/config.py
```

**4. Commit le merge:**

```powershell
git commit -m "Merge main into feature/network - resolve config conflict"
```

### Outils visuels

```powershell
# Lancer merge tool (VS Code)
git mergetool

# VS Code montre:
# - Incoming (version main)
# - Current (votre version)
# - Résultat

# Choisir "Accept Current" ou "Accept Incoming" ou éditer
```

### Abandonner le merge

```powershell
# Si trop de conflits, annuler tout
git merge --abort
```

---

## 📜 Historique & Diagnostic

### Log (historique commits)

```powershell
# Log simple
git log

# Log compact (1 ligne par commit)
git log --oneline

# Log avec graphe branches
git log --oneline --graph --all

# 5 derniers commits
git log -5

# Commits d'un auteur
git log --author="Nom"

# Commits entre dates
git log --since="2024-01-01" --until="2024-01-31"

# Commits touchant un fichier
git log -- p2p_file_sharing/network/discovery.py
```

### Diff (différences)

```powershell
# Changements non staged
git diff

# Changements staged
git diff --staged

# Différence entre branches
git diff main feature/network

# Différence entre commits
git diff abc123 def456

# Différence sur 1 fichier
git diff main -- config.py
```

### Blame (qui a écrit quelle ligne)

```powershell
# Voir qui a modifié chaque ligne
git blame p2p_file_sharing/network/discovery.py

# Format compact
git blame -L 10,20 discovery.py  # Lignes 10 à 20
```

### Show (voir détails commit)

```powershell
# Voir dernier commit
git show

# Voir commit précis
git show abc123

# Voir fichier d'un commit
git show abc123:p2p_file_sharing/main.py
```

### Status détaillé

```powershell
# Status normal
git status

# Status court
git status -s

# M  = modified
# A  = added
# D  = deleted
# ?? = untracked
```

---

## 🚨 Commandes d'Urgence

### Stash (mettre de côté)

```powershell
# Situation: Changements en cours mais besoin changer de branche
git stash

# Lister stashes
git stash list

# Réappliquer dernier stash
git stash pop

# Appliquer stash précis
git stash apply stash@{1}

# Supprimer stash
git stash drop

# Stash avec message
git stash save "Work in progress sur discovery"
```

### Reset (annuler)

```powershell
# Annuler changements non staged
git checkout -- fichier.py

# Annuler tout (DANGEREUX)
git reset --hard HEAD

# Revenir à un commit précis (garder changements)
git reset --soft abc123

# Revenir et SUPPRIMER changements (TRÈS DANGEREUX)
git reset --hard abc123
```

### Revert (annuler proprement)

```powershell
# Créer commit qui annule un commit précédent
git revert abc123

# Annuler plusieurs commits
git revert abc123..def456
```

### Restore (nouvelle commande Git 2.23+)

```powershell
# Restaurer fichier depuis dernier commit
git restore fichier.py

# Unstage fichier
git restore --staged fichier.py

# Restaurer depuis autre commit
git restore --source=abc123 fichier.py
```

### Clean (supprimer fichiers non trackés)

```powershell
# Voir ce qui serait supprimé (dry-run)
git clean -n

# Supprimer fichiers non trackés
git clean -f

# Supprimer aussi dossiers
git clean -fd

# Supprimer aussi fichiers ignorés
git clean -fdx
```

---

## 🎯 Scénarios Courants

### Scénario 1: Oublié de commit avant de change branch

```powershell
# Vous avez changements non commités
git status
# modified: discovery.py

# Essayez changer branche
git checkout main
# error: Your local changes would be overwritten

# SOLUTION: Stash
git stash
git checkout main
# ... faire ce que vous devez faire
git checkout feature/network
git stash pop
```

### Scénario 2: Commit sur mauvaise branche

```powershell
# Vous êtes sur main, vouliez être sur feature/network
git log --oneline -1
# abc123 Add discovery (← commit à déplacer)

# SOLUTION
# 1. Noter le hash du commit (abc123)
# 2. Annuler le commit sur main
git reset --hard HEAD~1

# 3. Aller sur bonne branche
git checkout feature/network

# 4. Cherry-pick le commit
git cherry-pick abc123
```

### Scénario 3: Besoin une feature de main avant merge officiel

```powershell
# Vous êtes sur feature/network
# Personne 2 a pushé une fonction utile sur main

# SOLUTION: Cherry-pick OU merge partiel
# Option A: Merge main (prend tout)
git merge main

# Option B: Cherry-pick 1 commit précis
git cherry-pick def456  # Hash du commit voulu
```

### Scénario 4: Push refusé (not fast-forward)

```powershell
git push origin feature/network
# error: failed to push some refs
# hint: Updates were rejected because the tip of your current branch is behind

# CAUSE: Quelqu'un a pushé avant vous

# SOLUTION
# 1. Pull (fetch + merge)
git pull origin feature/network

# 2. Résoudre conflits si nécessaire
# 3. Push
git push origin feature/network
```

### Scénario 5: Accidentellement supprimé fichier

```powershell
# Fichier supprimé mais pas encore commité
git status
# deleted: important.py

# SOLUTION: Restore
git restore important.py

# Fichier supprimé ET commité
git log --oneline -- important.py  # Trouver dernier commit où il existait
git restore --source=abc123 important.py
git add important.py
git commit -m "Restore important.py"
```

### Scénario 6: Merger feature branches ensemble

```powershell
# Fin jour 3: Merger tout dans main

# Personne 3 (Integration Lead):
git checkout main
git pull origin main

# Merger Core d'abord
git merge feature/core
git push origin main

# Puis Network
git merge feature/network
# Résoudre conflits si nécessaire
git push origin main

# Enfin GUI
git merge feature/gui
git push origin main

# Tout le monde pull
git pull origin main
```

---

## 📊 Commandes Utiles Avancées

### Logs avancés

```powershell
# Log avec stats fichiers modifiés
git log --stat

# Log avec diff inclus
git log -p

# Log joliment formaté
git log --pretty=format:"%h - %an, %ar : %s"

# Graphe ASCII
git log --graph --oneline --decorate --all
```

### Recherche dans historique

```powershell
# Trouver commits contenant "bug"
git log --grep="bug"

# Trouver commits modifiant code contenant "DISCOVERY_PORT"
git log -S"DISCOVERY_PORT"

# Quand une ligne a été ajoutée
git log -G"def broadcast" -- discovery.py
```

### Comparer branches

```powershell
# Commits dans feature/network pas encore dans main
git log main..feature/network

# Fichiers différents entre branches
git diff --name-only main feature/network

# Combien de commits d'avance/retard
git rev-list --left-right --count main...feature/network
```

### Tags

```powershell
# Créer tag léger
git tag v1.0

# Créer tag annoté (recommandé)
git tag -a v1.0 -m "Version 1.0 - Première release"

# Lister tags
git tag

# Voir détails tag
git show v1.0

# Pusher tags
git push origin v1.0
git push --tags  # Tous les tags

# Supprimer tag
git tag -d v1.0
git push origin :refs/tags/v1.0  # Remote
```

---

## 🔑 Alias Git (Raccourcis)

**Configurer des raccourcis:**

```powershell
# Status court
git config --global alias.st "status -s"

# Log joli
git config --global alias.lg "log --oneline --graph --all"

# Dernier commit
git config --global alias.last "log -1 HEAD"

# Unstage fichier
git config --global alias.unstage "reset HEAD --"

# Usage:
git st       # Au lieu de git status
git lg       # Au lieu de git log --oneline...
git last     # Au lieu de git log -1 HEAD
```

---

## 📖 Glossaire

- **Repository (repo):** Dossier Git contenant tout l'historique
- **Commit:** Snapshot du projet à un moment donné
- **Branch:** Ligne de développement parallèle
- **Remote:** Version du repo sur serveur (GitHub)
- **Origin:** Nom par défaut du remote principal
- **HEAD:** Pointeur vers le commit actuel
- **Staging area (index):** Zone intermédiaire avant commit
- **Working directory:** Vos fichiers actuels
- **Merge:** Fusionner deux branches
- **Conflict:** Git ne peut pas merger automatiquement
- **Fast-forward:** Merge simple sans commit de merge
- **Cherry-pick:** Copier un commit vers autre branche
- **Stash:** Mettre changements de côté temporairement
- **Tag:** Marquer un commit important (release)

---

## 🎓 Bonnes Pratiques

### Commits

✅ **Faire:**
- Commits atomiques (1 fonctionnalité = 1 commit)
- Messages clairs et descriptifs
- Commit souvent (plusieurs par jour)
- Tester avant de commit

❌ **Éviter:**
- Commits énormes (100+ fichiers)
- Messages vagues ("fix", "update")
- Commit code qui ne compile pas
- Commit fichiers sensibles (.env, credentials)

### Branches

✅ **Faire:**
- 1 branche = 1 feature
- Noms descriptifs (`feature/network`, pas `branch1`)
- Merge régulièrement depuis main
- Supprimer branches mergées

❌ **Éviter:**
- Tout développer sur main
- Branches qui vivent des semaines
- Oublier de pull avant push

### Messages

**Format:**
```
Type: Description courte (50 chars max)

- Détail 1
- Détail 2
- Détail 3
```

**Exemples:**

✅ Bon:
```
feat: Implement UDP peer discovery

- Add UDPDiscovery class with broadcast/listen
- Use threading for non-blocking operation
- Add tests for discovery protocol
```

❌ Mauvais:
```
stuff

did some work
```

---

## 🆘 Aide

```powershell
# Aide commande
git help <commande>
git help commit

# Aide courte
git <commande> --help
git commit --help

# Version Git
git --version
```

---

## 📌 Commandes Essentielles (Récap)

**Quotidien (80% du temps):**
```powershell
git status          # Voir état
git add .           # Ajouter changements
git commit -m "..."  # Commit
git push            # Envoyer
git pull            # Récupérer
```

**Branches:**
```powershell
git branch          # Voir branches
git checkout -b XXX # Créer et aller sur branche
git merge XXX       # Fusionner
```

**Urgence:**
```powershell
git stash           # Mettre de côté
git reset --hard    # Annuler tout (DANGER)
git log             # Voir historique
```

---

**Prochaine étape:** [CHECKLIST.md](CHECKLIST.md) - Liste de vérification finale
