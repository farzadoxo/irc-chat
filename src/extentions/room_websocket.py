from fastapi.websockets import WebSocket


class RoomWebsocket(WebSocket):
    def __init__(self,room):
        super().__init__()
        self.room = room

        
