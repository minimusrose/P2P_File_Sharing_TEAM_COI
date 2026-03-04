#!/usr/bin/env python3
"""
Test UDP Broadcast - Version simple
Lancez ce script sur les DEUX peers simultanément pour tester
"""
import socket
import json
import threading
import time
import sys

DISCOVERY_PORT = 5000

def broadcast_thread():
    """Thread qui envoie des broadcasts"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    peer_id = f"TEST_PEER_{socket.gethostname()}"
    
    print(f"[BROADCAST] Démarrage broadcasts avec ID: {peer_id}")
    
    for i in range(30):  # 30 broadcasts sur 30 secondes
        message = {
            "type": "ANNOUNCE",
            "peer_id": peer_id,
            "port": 5001
        }
        
        try:
            sock.sendto(
                json.dumps(message).encode('utf-8'),
                ('<broadcast>', DISCOVERY_PORT)
            )
            print(f"[BROADCAST] #{i+1} envoyé: {peer_id}")
        except Exception as e:
            print(f"[BROADCAST] ERREUR: {e}")
        
        time.sleep(1)
    
    sock.close()
    print("[BROADCAST] Fin des broadcasts")

def listen_thread():
    """Thread qui écoute les broadcasts"""
    print(f"[LISTEN] Démarrage écoute sur port {DISCOVERY_PORT}")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', DISCOVERY_PORT))
        sock.settimeout(35)  # Timeout un peu plus long que les broadcasts
        
        print(f"[LISTEN] En écoute sur 0.0.0.0:{DISCOVERY_PORT}")
        print("[LISTEN] Attendez 30 secondes...")
        print()
        
        local_peer_id = f"TEST_PEER_{socket.gethostname()}"
        
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                message = json.loads(data.decode('utf-8'))
                
                if message.get('type') == 'ANNOUNCE':
                    peer_id = message.get('peer_id')
                    
                    if peer_id == local_peer_id:
                        print(f"[LISTEN] Ignoré (broadcast de nous-mêmes)")
                    else:
                        print(f"[LISTEN] ✓ PEER DÉCOUVERT: {peer_id} depuis {addr[0]}")
                        print(f"         Port TCP: {message.get('port')}")
                        print()
                        
            except socket.timeout:
                break
            except Exception as e:
                print(f"[LISTEN] Erreur réception: {e}")
        
        sock.close()
        print("[LISTEN] Fin de l'écoute")
        
    except Exception as e:
        print(f"[LISTEN] ERREUR CRITIQUE: {e}")
        print(f"[LISTEN] Le port {DISCOVERY_PORT} est peut-être déjà utilisé?")

def main():
    print("=" * 70)
    print("TEST UDP BROADCAST - DÉCOUVERTE DE PEERS")
    print("=" * 70)
    print()
    print("Ce script doit être lancé sur LES DEUX peers simultanément.")
    print(f"Hostname: {socket.gethostname()}")
    print()
    
    # Obtenir l'IP locale
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"IP locale: {local_ip}")
    except:
        print("Impossible d'obtenir l'IP locale")
    
    print()
    print("-" * 70)
    print()
    
    # Lancer les threads
    t1 = threading.Thread(target=listen_thread, daemon=False)
    t2 = threading.Thread(target=broadcast_thread, daemon=False)
    
    t1.start()
    time.sleep(0.5)  # Démarrer l'écoute avant de broadcaster
    t2.start()
    
    # Attendre la fin
    t1.join()
    t2.join()
    
    print()
    print("=" * 70)
    print("TEST TERMINÉ")
    print("=" * 70)
    print()
    print("RÉSULTATS:")
    print("- Si vous avez vu 'PEER DÉCOUVERT' → La découverte fonctionne!")
    print("- Si aucun peer découvert → Problème firewall/réseau")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrompu.")
    except Exception as e:
        print(f"\n\nErreur fatale: {e}")
