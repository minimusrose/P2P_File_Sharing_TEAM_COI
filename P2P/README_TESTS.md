# Tests réseau et exécution rapide

Ce guide explique comment lancer rapidement les tests fournis pour la couche réseau.

1) Test TCP (serveur + client)

```bash
python3 test_tcp_full.py
```

2) Test UDP discovery

Par défaut le test tente d'utiliser le broadcast réseau. Si votre environnement bloque le broadcast
ou si vous voulez tester localement sur la machine, lancez les deux instances avec `--localhost`.

Terminal A (background):

```bash
# Lance en arrière-plan (ou ouvrir un autre terminal)
python3 test_discovery.py --localhost &
```

Terminal B:

```bash
python3 test_discovery.py --localhost
```

Vous devriez voir les deux instances se découvrir via `127.0.0.1`.

---

Notes:
- Les scripts utilisent `p2p_file_sharing/utils/config.py` pour les ports.
- Les logs sont écrits dans `~/.p2p_fileshare/p2p.log`.