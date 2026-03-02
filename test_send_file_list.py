#!/usr/bin/env python3
"""
Test TCP simple: envoie un FILE_LIST_RESPONSE à un peer.

Usage:
  python test_send_file_list.py <target_ip> <target_port> <my_peer_id>

Exemple:
  python test_send_file_list.py 10.57.223.181 5001 CALEBSAMA_4321
"""

import sys

from p2p_file_sharing.network.connection import TCPClient
from p2p_file_sharing.network.protocol import create_message, MessageType


def main() -> int:
    if len(sys.argv) != 4:
        print(
            "Usage: python test_send_file_list.py <target_ip> <target_port> <my_peer_id>"
        )
        return 2

    target_ip = sys.argv[1]
    try:
        target_port = int(sys.argv[2])
    except ValueError:
        print("target_port must be an int")
        return 2

    my_peer_id = sys.argv[3]

    # Liste de fichiers factice: si le peer distant la reçoit, il doit l'afficher en GUI.
    fake_files = [
        {
            "file_id": "test_file_001",
            "filename": "tcp_smoke_test.txt",
            "size": 1234,
            "hash": "deadbeef",
            "chunks_total": 1,
        }
    ]

    msg = create_message(
        MessageType.FILE_LIST_RESPONSE,
        my_peer_id,
        {"files": fake_files},
    )

    client = TCPClient()
    if not client.connect(target_ip, target_port):
        print(f"❌ Connexion TCP impossible vers {target_ip}:{target_port}")
        return 1

    try:
        ok = client.send_message(msg)
        if ok:
            print(f"✅ Message envoyé à {target_ip}:{target_port}")
            print("   Attends 2-3s puis clique 'Actualiser' sur le peer distant.")
            return 0
        else:
            print("❌ send_message() a échoué")
            return 1
    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(main())

