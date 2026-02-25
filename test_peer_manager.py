from p2p_file_sharing.core.database import Database
from p2p_file_sharing.core.peer_manager import PeerManager

print("=== Test Peer Manager ===\n")

# Setup
db = Database(':memory:')
pm = PeerManager(db)
pm.set_local_peer_id('local_peer')

# Test 1: Announce handling
print("Test 1: Handle peer announce...")
pm.handle_peer_announce('peer1', '192.168.1.10', 5001)
pm.handle_peer_announce('peer2', '192.168.1.11', 5001)
pm.handle_peer_announce('local_peer', '192.168.1.5', 5001)  # Devrait être ignoré

peers = pm.get_online_peers()
print(f"✓ Peers en ligne: {len(peers)} (devrait être 2)")
for p in peers:
    print(f"  - {p['peer_id']}")
print()

# Test 2: Update peer files
print("Test 2: Update peer files...")
files = [
    {
        'file_id': 'file1',
        'filename': 'document.pdf',
        'size': 1024000,
        'hash': 'hash123',
        'chunks_total': 4
    },
    {
        'file_id': 'file2',
        'filename': 'image.jpg',
        'size': 512000,
        'hash': 'hash456',
        'chunks_total': 2
    }
]
pm.update_peer_files('peer1', files)

all_files = db.get_all_files()
print(f"✓ Fichiers ajoutés: {len(all_files)}")
for f in all_files:
    print(f"  - {f['filename']} (owner: {f['owner_peer_id']})")
print()

db.close()
print("=== Tests terminés avec succès ===")