from p2p_file_sharing.core.database import Database

print("=== Test Database ===\n")

# DB en mémoire pour test
db = Database(':memory:')

# Test 1: Peers
print("Test 1: Gestion peers...")
db.add_peer('peer1', '192.168.1.10', 5001)
db.add_peer('peer2', '192.168.1.11', 5001)
peers = db.get_active_peers()
print(f"✓ Peers ajoutés: {len(peers)}")
for p in peers:
    print(f"  - {p['peer_id']} @ {p['ip']}:{p['port']}")
print()

# Test 2: Files
print("Test 2: Gestion fichiers...")
db.add_file('file1', 'test.txt', 1024, 'abc123hash', 'peer1', 4)
db.add_file('file2', 'video.mp4', 10485760, 'def456hash', 'peer2', 40)
files = db.get_all_files()
print(f"✓ Fichiers ajoutés: {len(files)}")
for f in files:
    size_mb = f['size'] / 1024 / 1024
    print(f"  - {f['filename']} ({size_mb:.2f} MB, {f['chunks_total']} chunks)")
print()

# Test 3: Chunks
print("Test 3: Gestion chunks...")
db.add_chunk('chunk1', 'file1', 0, 'chunk0hash', ['peer1', 'peer2'])
db.add_chunk('chunk2', 'file1', 1, 'chunk1hash', ['peer1'])
chunks = db.get_chunks_for_file('file1')
print(f"✓ Chunks ajoutés: {len(chunks)}")
for c in chunks:
    print(f"  - Chunk {c['chunk_index']}: {len(c['peer_ids'])} peer(s)")
print()

# Test 4: Local shared
print("Test 4: Fichiers locaux...")
db.add_local_shared('file1', '/path/to/file1.txt')
local = db.get_local_shared_files()
print(f"✓ Fichiers partagés localement: {len(local)}")
print()

db.close()
print("=== Tests terminés avec succès ===")