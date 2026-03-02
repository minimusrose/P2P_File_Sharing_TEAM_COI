"""Protocole de communication entre peers"""
import json
from typing import Dict, Any

class MessageType:
    """Types de messages échangés"""

    ANNOUNCE = "ANNOUNCE"
    FILE_LIST_REQUEST = "FILE_LIST_REQUEST"
    FILE_LIST_RESPONSE = "FILE_LIST_RESPONSE"
    CHUNK_REQUEST = "CHUNK_REQUEST"
    CHUNK_DATA = "CHUNK_DATA"
    GOODBYE = "GOODBYE"


def create_message(msg_type: str, peer_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Crée un message au format dict prêt pour l'envoi.

    NOTE IMPORTANTE:
    - Le sérialisation JSON est gérée par TCPClient.send_message() et
      TCPServer.send_to_peer(), donc cette fonction retourne un dict,
      pas des bytes.

    Args:
        msg_type: Type de message (voir MessageType)
        peer_id: ID du peer émetteur
        data: Données du message (dict)

    Returns:
        dict: Message sérialisable en JSON
    """
    return {
        "type": msg_type,
        "peer_id": peer_id,
        "data": data,
    }

def parse_message(raw_data: bytes) -> Dict[str, Any]:
    """
    Parse un message reçu
    
    Args:
        raw_data: Bytes reçus du réseau
    
    Returns:
        dict: Message parsé avec 'type', 'peer_id', 'data'
    """
    return json.loads(raw_data.decode('utf-8'))
