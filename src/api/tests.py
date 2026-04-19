import requests
from src.core.models import Room , Message
from requests.exceptions import ConnectionError
import json


_IP = '127.0.0.1'
_PORT = 8000
BASE_URL = f'http://{_IP}:{_PORT}/api'


""" ROOM """
def create_room(room:Room) -> dict:
    data = json.dumps({"name":room.name,"user_limit":room.user_limit,"visable":room.visable})
    r = requests.post(f"{BASE_URL}/rooms",data=data)

    return json.loads(r.content)



def get_rooms():
    r = requests.get(f"{BASE_URL}/rooms")

    print(json.loads(r.content))




def get_room(id:str):
    r = requests.get(f'{BASE_URL}/room/{id}')

    print(json.loads(r.content))



def delete_room(id):
    r = requests.delete(f'{BASE_URL}/room/{id}')

    print(json.loads(r.content))



""" MESSAGE """
def get_messages():
    r = requests.get(f"{BASE_URL}/messages")

    print(json.loads(r.content))


def get_message(id):
    r = requests.get(f"{BASE_URL}/message/{id}")

    print(json.loads(r.content))


def send_message(msg:Message):
    data = json.dumps({'content':msg.content})
    r = requests.post(f"{BASE_URL}/message",data=data)

    return json.loads(r.content)


def delete_message(id:int):
    r = requests.delete(f'{BASE_URL}/message/{id}')

    print(json.loads(r.content))


def delete_all_message():
    r = requests.delete(f"{BASE_URL}/messages")

    print(r.content)


if __name__ == "__main__":
    try:
        # room test
        print("Start testing api endpoints ...")
        print('*'*30)

        room = create_room(room=Room(name="chattt",user_limit=3,visable=True))
        print(room)
        print("1) Passed.")
        print('-'*30)

        get_rooms()
        print("2) Passed.")
        print('-'*30)

        get_room(id=room[8:16])
        print("3) Passed.")
        print('-'*30)

        # delete_room(id=room[8:16])
        # print("4) Passed.")
        # print('-'*30)

        # message test
        message = send_message(msg=Message(content="Hello World!",username='test'))
        print(message)
        print("5) Passed.")
        print('-'*30)

        get_messages()
        print("6) Passed.")
        print('-'*30)

        # get_message(id=message[8:16])
        # print("7) Passed.")
        # print('-'*30)

        # delete_message(id=message[8:16])
        # print("8) Passed.")
        # print('-'*30)

        delete_all_message()
        print("9) Passed.")
        print('-'*30)



    except ConnectionError:
        print(">>> ERR: Connection unstablished!")