from pydantic import BaseModel

class Room(BaseModel):
    name : str
    user_limit : int
    visable : bool
    
class Message(BaseModel):
    content : str
    username : str


class RoomMessage(BaseModel):
    room_id : str
    content: str
