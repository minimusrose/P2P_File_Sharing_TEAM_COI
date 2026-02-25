from p2p_file_sharing.network.discovery import UDPDiscovery
import time

def on_peer_found(peer_id, ip, port):
    print(f"✓ Peer trouvé: {peer_id} @ {ip}:{port}")

# Test
discovery = UDPDiscovery("test_peer_1")
discovery.start_listening(on_peer_found)
discovery.start_broadcasting()

print("En attente de peers... (Ctrl+C pour arrêter)")
print("Lancez une 2ème instance dans un autre terminal!")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nArrêt...")
    discovery.stop()