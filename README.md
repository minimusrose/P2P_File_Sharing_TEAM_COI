# 🌐 P2P File Sharing

**Système de partage de fichiers décentralisé peer-to-peer**

---

## ✨ Fonctionnalités

- 🔍 Découverte automatique des peers sur le réseau local
- 📁 Partage de fichiers entre utilisateurs
- ⬇️ Téléchargement sécurisé avec vérification d'intégrité (SHA256)
- 🖥️ Interface graphique simple et intuitive
- 🌐 Compatible Windows + Linux

---

## 📋 Prérequis

- **Python 3.9 ou supérieur**
- **Connexion réseau local** (même WiFi/Ethernet)
- **Système d'exploitation:** Windows 10+ ou Linux (Ubuntu, Fedora, etc.)

---

## 🚀 Installation

### Windows

1. Extraire l'archive `p2p_file_sharing.zip`
2. Double-cliquer sur **`install.bat`**
3. Attendre la fin de l'installation
4. Une fois terminé, appuyer sur Entrée

### Linux

1. Extraire l'archive
2. Ouvrir un terminal dans le dossier
3. Rendre le script exécutable et l'exécuter:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

---

## ▶️ Utilisation

### Lancer l'application

**Windows:** 
- Double-cliquer sur **`run.bat`** (mode normal)
- Ou **`run_debug.bat`** (mode debug avec console)

**Linux:** 
```bash
./run.sh
```

### Partager un fichier

1. Cliquer sur le bouton **"Partager fichier"**
2. Sélectionner le fichier sur votre disque
3. Le fichier apparaît dans la liste des fichiers partagés
4. Les autres peers le verront automatiquement après quelques secondes

### Télécharger un fichier

1. Attendre que les fichiers des autres peers apparaissent dans la liste
2. Sélectionner un fichier dans la liste
3. Cliquer sur **"Télécharger"**
4. Choisir où enregistrer le fichier
5. Attendre la barre de progression (peut prendre du temps pour les gros fichiers)

### Voir les peers connectés

- La liste des peers connectés s'affiche dans l'interface
- Elle se met à jour automatiquement toutes les ~30 secondes
- Un peer qui se déconnecte disparaît après quelques minutes

---

## 🔧 Dépannage

### Problème: Les peers ne se voient pas

**Cause:** Le firewall bloque les ports UDP/TCP

**Solution:**

**Windows:**
1. Ouvrir "Pare-feu Windows Defender"
2. Cliquer sur "Autoriser une application"
3. Ajouter Python (python.exe et pythonw.exe)
4. Autoriser pour les réseaux privés

**Linux:**
```bash
sudo ufw allow 5000/udp
sudo ufw allow 5001/tcp
```

### Problème: "Python n'est pas installé"

**Solution:**
- Télécharger Python 3.9+ depuis [python.org](https://www.python.org/downloads/)
- **IMPORTANT:** Cocher **"Add Python to PATH"** pendant l'installation
- Redémarrer le terminal après installation

### Problème: "tkinter non disponible" (Linux)

**Solution:**

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

### Problème: La GUI ne s'ouvre pas

**Solution:**
- Lancer **`run_debug.bat`** (Windows) pour voir les erreurs
- Ou en terminal: `python main.py`
- Vérifier les logs dans `data/p2p.log`
- S'assurer que tkinter est installé

### Problème: Le téléchargement échoue

**Causes possibles:**
1. **Peer émetteur déconnecté** → Réessayer dans quelques secondes
2. **Fichier trop volumineux** → Patience (peut prendre plusieurs minutes)
3. **Réseau instable** → Vérifier la connexion WiFi
4. **Port occupé** → Redémarrer l'application

### Problème: "Port already in use"

**Solution:**
- Fermer toutes les instances de l'application
- Attendre 30 secondes
- Relancer l'application
- Si le problème persiste, redémarrer l'ordinateur

---

## 📂 Structure des Dossiers

```
p2p_file_sharing/
├── data/           ← Base de données et logs
├── shared_files/   ← Fichiers que vous partagez
└── downloads/      ← Fichiers téléchargés (créé automatiquement)
```

**Note:** Ne supprimez pas le dossier `data` pendant que l'application tourne.

---

## ⚠️ Limitations

- ✅ Fonctionne uniquement sur **réseau local** (pas Internet)
- ✅ Testé jusqu'à ~100 MB par fichier
- ✅ Maximum 10-20 peers simultanés recommandés
- ⚠️ Pas de chiffrement des données (à utiliser sur réseau privé uniquement)
- ⚠️ Pas de reprise de téléchargement en cas d'interruption

---

## 🔒 Sécurité

- **Vérification d'intégrité:** Tous les fichiers sont vérifiés avec SHA256
- **Réseau local uniquement:** L'application ne se connecte pas à Internet
- **Pas de serveur central:** Architecture décentralisée
- **Attention:** N'utilisez pas sur un réseau public (café, bibliothèque, etc.)

---

## 📊 Performance

### Vitesse de transfert

- **LAN (Ethernet):** ~50-100 MB/s
- **WiFi 5GHz:** ~20-50 MB/s
- **WiFi 2.4GHz:** ~5-20 MB/s

### Temps de découverte

- **Premier peer:** ~5-10 secondes
- **Peers suivants:** ~30 secondes (rafraîchissement automatique)

---

## 📞 Support

En cas de problème persistant:

1. **Vérifier les logs:** `data/p2p.log`
2. **Tester le firewall:** Désactiver temporairement pour tester
3. **Vérifier le réseau:** Tous les peers sur le même WiFi/LAN
4. **Redémarrer:** Fermer et relancer l'application

### Logs

Les logs se trouvent dans `data/p2p.log` et contiennent:
- Les connexions/déconnexions des peers
- Les transferts de fichiers
- Les erreurs éventuelles

---

## 🎓 À propos

**Projet:** P2P File Sharing  
**Version:** 1.0  
**Année:** 2026  
**Équipe:** COI Team

### Technologies utilisées

- Python 3.9+
- Tkinter (interface graphique)
- Socket (communication réseau)
- SQLite (base de données)
- Threading (concurrence)

---

## 📜 Licence

MIT License - Libre d'utilisation et de modification

---

## 🤝 Contribution

Pour les développeurs souhaitant contribuer, voir:
- [README_PROJET.md](README_PROJET.md) - Documentation technique
- [SETUP.md](SETUP.md) - Guide de développement
- [INTEGRATION.md](INTEGRATION.md) - Architecture du système

---

**Bon partage de fichiers ! 🚀**