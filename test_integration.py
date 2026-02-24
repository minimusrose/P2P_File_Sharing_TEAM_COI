"""Test d'intégration GUI avec mocks"""
from p2p_file_sharing.gui.main_window import MainWindow
import tkinter as tk

# Mock managers
class MockPeerManager:
    def get_online_peers(self):
        return [
            {'peer_id': 'test_peer_1', 'ip': '192.168.1.10', 'port': 5001},
            {'peer_id': 'test_peer_2', 'ip': '192.168.1.11', 'port': 5001}
        ]

class MockFileManager:
    def __init__(self):
        self.db = MockDB()
    
    def add_shared_file(self, filepath):
        print(f"Mock: Sharing {filepath}")
        return "mock_file_id_123"

class MockDB:
    def get_all_files(self):
        return [
            {
                'file_id': 'file1',
                'filename': 'test_document.pdf',
                'size': 2500000,
                'owner_peer_id': 'peer_abc',
                'chunks_total': 10
            },
            {
                'file_id': 'file2',
                'filename': 'vacation_photo.jpg',
                'size': 1500000,
                'owner_peer_id': 'peer_xyz',
                'chunks_total': 6
            }
        ]

print("=== Test GUI avec mocks ===\n")
print("Lancement GUI avec données de test...")
print("Fermez la fenêtre pour terminer le test.\n")

# Lancer GUI
pm = MockPeerManager()
fm = MockFileManager()

gui = MainWindow(pm, fm, None)
gui.run()

print("\n✓ Test terminé")