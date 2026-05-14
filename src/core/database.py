
import os
import dotenv

""" REDIS VERSION """
from redis import Redis
# import datetime
# import json

dotenv.load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')


redis_client = Redis(
    host= DB_HOST,
    port= DB_PORT,
    decode_responses=True
)

KEY = 'messages'
KEY2 = 'rooms'

# init 
redis_client.delete(KEY)
redis_client.delete(KEY2)
redis_client.expire(KEY, 10)
# redis_client.rpush(KEY,json.dumps({'id':0,'content':'🔽 ------ MESSAGES ------ 🔽','created_at':str(datetime.datetime.now())}))
# redis_client.rpush('rooms',json.dumps({'id':'000000','name':"init",'user_limit':0,'visable':False}))
