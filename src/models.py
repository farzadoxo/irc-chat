from pydantic import BaseModel

class Room(BaseModel):
    name : str
    user_limit : int

    
class Message(BaseModel):
    content : str
