from fastapi import FastAPI , WebSocket , status
from fastapi.responses import Response , JSONResponse
from db.database import redis_client , key
from api.models import Message

import datetime
import json
import random


app = FastAPI()

@app.websocket('/ws')
async def websocket_endpoint(ws:WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        await ws.send_text(f"I got your message! : {data}")



@app.post('/api/message')
def new_message(msg:Message):
    if msg.content:
        guid = random.randint(10000,345345345)
        redis_client.rpush(key,json.dumps({
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
    all_messages = [json.loads(msg) for msg in redis_client.lrange(key,0,-1)]
    for i in all_messages:
        if i['id'] == id:
            return JSONResponse({'id':i['id'],'message':id['content'],'created_at':i['created_at']},
                                status_code=status.HTTP_200_OK)
        else:
            return Response("Message not found!",status_code=status.HTTP_404_NOT_FOUND)
    



@app.get('/api/messages')
def get_all_messages():
    messages = [json.loads(msg) for msg in redis_client.lrange(key,0,-1)]
    if len(messages) != 0:
        msgs = {'messages':[]}
        for msg in messages:
            msgs['messages'].append({'id':msg['id'],'message':msg['content'],'created_at':msg['created_at']})
        
        return JSONResponse(msgs,status_code=status.HTTP_200_OK)
    



@app.delete('/api/message')
def delete_message(id:int):
        messages = [json.loads(msg) for msg in redis_client.lrange(key,0,-1)]
        for message in messages:
            if int(message['id']) == id:
                
