# i will use redis version but you can use sqlite version if you want!

# """ SQLITE VERSION """
# import sqlite3 

# conn = sqlite3.connect("db.db",check_same_thread=False)
# cur = conn.cursor()

# cur.execute(f"""
#                 CREATE TABLE IF NOT EXISTS messages (
#                 id INT PRIMARY KEY ,
#                 content TEXT NOT NULL ,
#                 created_at DATETIME NOT NULL)
#             """) 



""" REDIS VERSION """
from redis import Redis
import datetime
import json


redis_client = Redis(
    host='127.0.0.1',
    port=6379,
    decode_responses=True
)

KEY = 'messages'

# init 
redis_client.delete(KEY)
redis_client.expire(KEY, 10)
redis_client.rpush(KEY,json.dumps({'id':0,'content':'🔽 ------ MESSAGES ------ 🔽','created_at':str(datetime.datetime.now())}))