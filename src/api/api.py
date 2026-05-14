from pathlib import Path
from fastapi import FastAPI, WebSocket, status, WebSocketDisconnect
from fastapi.responses import Response, JSONResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from core.database import redis_client , KEY
from core.models import Message,Room
from extentions.room_websocket import RoomWebsocket

import colorama
import datetime
import json
import random
import os


# env
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "front-end"
TEMPLATES_DIR = STATIC_DIR / "templates"


app = FastAPI()
app.mount("/front-end", StaticFiles(directory=str(STATIC_DIR)), name="statics")
templates = Jinja2Templates(directory=str(STATIC_DIR))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)



# Public messageing websocket
connections : list[WebSocket] = []
dead_connections : list[WebSocket] = []
@app.websocket('/ws')
async def websocket_endpoint(ws:WebSocket):
    await ws.accept()
    connections.append(ws)
    try:
        while True:
            data = await ws.receive_json()
            guid = random.randint(10000,345345345)
            redis_client.rpush(KEY,json.dumps({
                'id':guid,
                'content':data['content'],
                'created_at':str(datetime.datetime.now()),
                'username':data['username']
            }))

            # broadcasting and removing dead connected websockets from connection list
            for connection in connections:
                try:
                    await connection.send_json(data)
                except:
                    dead_connections.append(connection)
            for dead in dead_connections:
                connections.remove(dead)

    except WebSocketDisconnect:
        if ws in connections:
            connections.remove(ws)  






# Room messaging websocket
connected_rooms : list[Room] = []
room_sessions : list[WebSocket] = []
@app.websocket('/rws/{room_id}')
async def websocket_endpoint(rws: WebSocket, room_id: str):

    rooms = [json.loads(room) for room in redis_client.lrange('rooms',0,-1)]
    matched = None
    for room in rooms:
        if room['id'] == room_id:
            matched = room
            break
    
    if matched is None:
        print("Room not found")
        await rws.close()
        return

    await rws.accept()
    rws.room = room_id
    room_sessions.append(rws)

    try:
        while True:
            data = await rws.receive_json()

            guid = random.randint(10000,345345345)
            redis_client.rpush(
                f'room:{room_id}',
                json.dumps({
                    'id': guid,
                    'room_id': room_id,
                    'content': data['content'],
                    'created_at': str(datetime.datetime.now()),
                    'username': data['username']
                })
            )

            dead = []
            for connection in room_sessions:
                if getattr(connection, "room", None) == room_id:
                    try:
                        await connection.send_json(data)
                    except:
                        dead.append(connection)

            for d in dead:
                room_sessions.remove(d)

    except WebSocketDisconnect:
        if rws in room_sessions:
            room_sessions.remove(rws)


                




@app.get('/')
def root(request:Request):
    return templates.TemplateResponse(request=request,
                                      name="index.html",
                                      context={'messages':[json.loads(msg) for msg in redis_client.lrange(KEY,0,-1)]})



@app.post('/api/message')
def new_message(msg:Message):
    if msg.content:
        guid = os.urandom(4).hex()
        message = json.dumps({
            'id':guid,
            'content':msg.content,
            'created_at':str(datetime.datetime.now()),
            'username':msg.username
        })
        redis_client.rpush(KEY,message)
        
        return JSONResponse(message,status_code=status.HTTP_201_CREATED)
    
    else:
        return Response("You can not send empty message!",status_code=status.HTTP_400_BAD_REQUEST)
    


# NOTE: not recommended 
@app.get('/api/message')
def get_message(id:int):
    all_messages = [json.loads(msg) for msg in redis_client.lrange(KEY,0,-1)]
    for msg in all_messages:
        if msg['id'] == id:
            return JSONResponse(content=msg,
                                status_code=status.HTTP_200_OK)
    else:
        return Response("Message not found!",status_code=status.HTTP_404_NOT_FOUND)
            
    



@app.get('/api/messages')
def get_all_messages():
    messages = [json.loads(msg) for msg in redis_client.lrange(KEY,0,-1)]
    data = {'message_count':len(messages),'messages':[]}

    for msg in messages:
        data['messages'].append({'id':msg['id'],
                                    'message':msg['content'],
                                    'created_at':msg['created_at'],
                                    'username':msg['username']})
    
    return JSONResponse(content=data,status_code=status.HTTP_200_OK)
    

# NOTE: Not so recommended
@app.delete('/api/message')
def delete_message(id:int):
        messages = [json.loads(msg) for msg in redis_client.lrange(KEY,0,-1)]
        for message in messages:
            if int(message['id']) == id: 
                redis_client.lrem(KEY,0,json.dumps(message))
                return Response('Message Deleted successfully!',status_code=status.HTTP_200_OK)
        else:
            return Response("Message not found!",status_code=status.HTTP_404_NOT_FOUND)



@app.delete('/api/messages')
def delete_all_messages():
    redis_client.ltrim('messages',1,0)
    return Response('Ok',status_code=status.HTTP_200_OK)


"""ROOM"""

@app.post('/api/rooms')
def new_room(room:Room):
    key='rooms'
    guid = os.urandom(4).hex()
    new_room = f"room:{guid}"
    
    try:
        redis_client.rpush(new_room,json.dumps({
            "id":f"{random.randint(435333,3456622)}",
            "room_id":guid,
            "content":"------- MESSAGES -------- ",
            "created_at":str(datetime.datetime.now())
            }))

        room = json.dumps({
            "id":guid,
            "name":room.name,
            "user_limit":room.user_limit,
            "visable":str(room.visable)})
        redis_client.rpush(key,room)
        
        return JSONResponse(room,status_code=status.HTTP_201_CREATED)
    
    except Exception as error:
        return Response(f"Somthing went wrong: {error}")
    



@app.get('/api/rooms')
def get_all_rooms():
    rooms = [json.loads(room) for room in redis_client.lrange('rooms',0,-1)]
    rms = {"rooms":[]}

    for room in rooms:
        if room['visable'] == "True":
            rms['rooms'].append({"id":room['id'],
                                "name":room['name'],
                                "user_limit":room['user_limit'],
                                "visable":room['visable']})
        
    return JSONResponse(rms,status_code=status.HTTP_200_OK)



@app.get('/api/room/{room_id}')
def get_room(room_id):
    rooms = [json.loads(room) for room in redis_client.lrange('rooms',0,-1)]
    for room in rooms:
        if room['id'] == room_id:
                messages = [json.loads(msg) for msg in redis_client.lrange(f"room:{room_id}",0,-1)]
                response = {"info":{},"messages":[]}
                response['info'] = {"id":room['id'],"name":room['name'],"user_limit":room['user_limit'],"visable":room['visable']}
                for message in messages:
                    response['messages'].append({"id":message['id'],
                                            "content":message['content'],
                                            "created_at":message['created_at']})
                
                return JSONResponse(response,status_code=status.HTTP_200_OK)



@app.delete('/api/room')
def delete_room(room_id:str):
    rooms = [json.loads(room) for room in redis_client.lrange('rooms',0,-1)]
    for room in rooms:
        if room['id'] == room_id:
            redis_client.lrem('rooms',0,json.dumps(room))
            redis_client.delete(f'room:{room_id}')

            return JSONResponse(room,status_code=status.HTTP_200_OK)
    
    else:
        return Response("Room not found!",status_code=status.HTTP_404_NOT_FOUND)
