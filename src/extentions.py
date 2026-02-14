from typing import List
from fastapi import WebSocket


async def broadcast(connections:List[WebSocket],message):
    dead_connection = List[WebSocket] = []
    for conn in connections:
        try:
            await conn.send_json(data=message)
        except:
            dead_connection.append(conn)

    for dead in dead_connection:
        connections.remove(dead)

    return connections


