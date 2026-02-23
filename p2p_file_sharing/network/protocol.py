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

def create_message(msg_type: str, peer_id: str, data: Dict[str, Any]) -> bytes:
    """
    Crée un message JSON encodé en bytes
    
    Args:
        msg_type: Type de message (voir MessageType)
        peer_id: ID du peer émetteur
        data: Données du message (dict)
    
    Returns:
        bytes: Message encodé prêt à envoyer
    """
    message = {
        "type": msg_type,
        "peer_id": peer_id,
        "data": data
    }
    return json.dumps(message).encode('utf-8')

def parse_message(raw_data: bytes) -> Dict[str, Any]:
    """
    Parse un message reçu
    
    Args:
        raw_data: Bytes reçus du réseau
    
    Returns:
        dict: Message parsé avec 'type', 'peer_id', 'data'
    """
    return json.loads(raw_data.decode('utf-8'))
