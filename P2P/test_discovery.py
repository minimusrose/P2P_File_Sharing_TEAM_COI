from p2p_file_sharing.network.discovery import UDPDiscovery
import time
import sys

def on_peer_found(peer_id, ip, port):
    print(f"✓ Peer trouvé: {peer_id} @ {ip}:{port}")


use_local = '--localhost' in sys.argv

# Test
if use_local:
    discovery = UDPDiscovery("test_peer_1", broadcast_addr='127.0.0.1')
else:
    discovery = UDPDiscovery("test_peer_1")

discovery.start_listening(on_peer_found)
discovery.start_broadcasting()

print("En attente de peers... (Ctrl+C pour arrêter)")
print("Lancez une 2ème instance dans un autre terminal! (ajoutez --localhost si besoin)")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nArrêt...")
    discovery.stop()
