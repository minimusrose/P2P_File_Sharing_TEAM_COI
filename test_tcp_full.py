from p2p_file_sharing.network.connection import TCPServer, TCPClient
from p2p_file_sharing.network.protocol import create_message, MessageType
import time
import threading

def test_server():
    """Fonction pour le serveur"""
    def on_message(peer_id, message):
        print(f"✓ Serveur reçu de {peer_id}: {message['type']}")
    
    server = TCPServer(5001)
    server.start(on_message)
    
    print("Serveur démarré, en attente...")
    time.sleep(20)
    server.stop()

def test_client():
    """Fonction pour le client"""
    time.sleep(2)  # Attendre que serveur démarre
    
    client = TCPClient()
    if client.connect('127.0.0.1', 5001):
        print("✓ Client connecté")
        
        # Envoyer message
        msg = {
            "type": MessageType.ANNOUNCE,
            "peer_id": "test_client",
            "data": {"message": "Hello from client!"}
        }
        client.send_message(msg)
        print("✓ Message envoyé")
        
        time.sleep(1)
        client.close()
    else:
        print("✗ Échec connexion")

# Lancer les deux
print("Test TCP Server + Client")
print("-" * 40)

server_thread = threading.Thread(target=test_server)
client_thread = threading.Thread(target=test_client)

server_thread.start()
client_thread.start()

server_thread.join()
client_thread.join()

print("-" * 40)
print("Test terminé!")