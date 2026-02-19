"""Test Jour 1: File chunking, hash, assemblage"""
from p2p_file_sharing.core.file_manager import FileManager
from pathlib import Path
import os

print("=== Test File Chunking ===\n")

# Créer fichier test 1MB
test_file = "test_1mb.dat"
print(f"Creation fichier test: {test_file}...")
with open(test_file, 'wb') as f:
    f.write(os.urandom(1024 * 1024))  # 1MB random
print("OK Fichier cree: 1 MB\n")

fm = FileManager()

# Test 1: Chunking
print("Test 1: Chunking...")
chunks = fm.chunk_file(test_file)
print(f"OK Chunks crees: {len(chunks)}")
print(f"  Taille attendue: 4 chunks (256KB chacun)")
print(f"  Premier chunk: {len(chunks[0]['data'])} bytes")
print(f"  Hash premier chunk: {chunks[0]['hash'][:16]}...\n")

# Test 2: Hash fichier
print("Test 2: Hash fichier complet...")
hash1 = fm.calculate_file_hash(test_file)
print(f"OK Hash: {hash1[:32]}...\n")

# Test 3: Réassemblage
print("Test 3: Reassemblage...")
output = "test_reassembled.dat"
success = fm.assemble_chunks(chunks, output)
print(f"OK Reassemblage: {'OK' if success else 'FAIL'}")

# Vérifier hash
hash2 = fm.calculate_file_hash(output)
print(f"OK Hash apres reassemblage: {hash2[:32]}...")
match = hash1 == hash2
print(f"OK Hash match: {'OUI' if match else 'NON'}\n")

# Cleanup
Path(test_file).unlink()
Path(output).unlink()

print("=== Tests termines ===")
print(f"Resultat: {'SUCCES' if match else 'ECHEC'}")
