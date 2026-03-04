#!/usr/bin/env python3
"""
Script de diagnostic UDP - À lancer sur CALEBSAMA pour tester la réception
"""
import socket
import json
import time
import sys

DISCOVERY_PORT = 5000

def test_udp_receive():
    """Test de réception UDP sur le port 5000"""
    print("=" * 70)
    print("TEST DE RÉCEPTION UDP - DIAGNOSTIC")
    print("=" * 70)
    print(f"\nCe script va écouter sur le port {DISCOVERY_PORT} UDP")
    print("Lancez l'application P2P sur l'autre peer (LAPTOP)")
    print("Attendez 30 secondes pour voir si des broadcasts arrivent...")
    print("\n" + "-" * 70 + "\n")
    
    try:
        # Créer socket UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Important sur Windows!
        
        # Bind sur toutes les interfaces
        sock.bind(('', DISCOVERY_PORT))
        sock.settimeout(1.0)  # Timeout de 1 seconde
        
        print(f"✓ Socket créé et lié à 0.0.0.0:{DISCOVERY_PORT}")
        print(f"✓ SO_BROADCAST activé")
        print(f"✓ SO_REUSEADDR activé")
        print("\nÉcoute en cours... (30 secondes)\n")
        
        packets_received = 0
        start_time = time.time()
        
        while time.time() - start_time < 30:
            try:
                data, addr = sock.recvfrom(1024)
                packets_received += 1
                
                print(f"\n[{packets_received}] ✓ PACKET REÇU!")
                print(f"    De: {addr[0]}:{addr[1]}")
                print(f"    Taille: {len(data)} bytes")
                
                try:
                    message = json.loads(data.decode('utf-8'))
                    print(f"    Type: {message.get('type', 'unknown')}")
                    print(f"    Peer ID: {message.get('peer_id', 'unknown')}")
                    print(f"    Port TCP: {message.get('port', 'unknown')}")
                except Exception as e:
                    print(f"    Erreur JSON: {e}")
                    print(f"    Données brutes: {data[:100]}")
                
            except socket.timeout:
                # Timeout normal, continuer
                elapsed = int(time.time() - start_time)
                remaining = 30 - elapsed
                sys.stdout.write(f"\r  Écoute... {elapsed}s / 30s ({packets_received} packets reçus)    ")
                sys.stdout.flush()
                continue
        
        sock.close()
        
        print("\n\n" + "=" * 70)
        print("RÉSULTAT DU TEST")
        print("=" * 70)
        
        if packets_received > 0:
            print(f"✓ SUCCÈS: {packets_received} packets UDP reçus")
            print("  → La réception UDP fonctionne!")
            print("  → Le problème est ailleurs (vérifier le code)")
        else:
            print("✗ ÉCHEC: Aucun packet UDP reçu")
            print("\n  CAUSES POSSIBLES:")
            print("  1. Firewall Windows bloque le port 5000 UDP")
            print("  2. L'autre peer n'envoie pas de broadcasts")
            print("  3. Problème réseau (switch/routeur bloque broadcasts)")
            print("\n  SOLUTIONS:")
            print("  → Désactiver temporairement le firewall Windows")
            print("  → Vérifier que les deux machines sont sur le MÊME réseau")
            print("  → Autoriser Python dans le firewall:")
            print("     netsh advfirewall firewall add rule name=\"P2P UDP\" dir=in action=allow protocol=UDP localport=5000")
        
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ ERREUR: {e}")
        print(f"\nLe port {DISCOVERY_PORT} est peut-être déjà utilisé?")
        print("Fermez l'application P2P avant de lancer ce test.")

if __name__ == "__main__":
    test_udp_receive()
