from fastapi import FastAPI , WebSocket , status , WebSocketDisconnect
from fastapi.responses import Response , JSONResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import redis_client , KEY
from models import Message

import datetime
import json
import random


app = FastAPI()
app.mount('/statics',StaticFiles(directory='statics'),name='statics')
app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_methods=['*'],
                   allow_headers=['*'],
                   allow_credentials=True
                   )


connections : list[WebSocket] = []
dead_connections : list[WebSocket] = []
templates = Jinja2Templates(directory='statics/templates')

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
                'created_at':str(datetime.datetime.now())
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




@app.get('/')
def root(request:Request):
    return templates.TemplateResponse(request=request,
                                      name="index.html",
                                      context={'messages':[json.loads(msg) for msg in redis_client.lrange(KEY,0,-1)]})



@app.post('/api/message')
def new_message(msg:Message):
    if msg.content:
        guid = random.randint(10000,345345345)
        redis_client.rpush(KEY,json.dumps({
            'id':guid,
            'content':msg.content,
            'created_at':str(datetime.datetime.now())
        }))
        

        return Response("Message send successfully!",status_code=status.HTTP_201_CREATED)
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
    msgs = {'messages':[]}

    for msg in messages:
        msgs['messages'].append({'id':msg['id'],
                                    'message':msg['content'],
                                    'created_at':msg['created_at']})
    
    return JSONResponse(content=msgs,status_code=status.HTTP_200_OK)
    

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
                
