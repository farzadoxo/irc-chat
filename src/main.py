from api.api import app
import uvicorn
import dotenv
import os


dotenv.load_dotenv('')    
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

print(HOST)
print(PORT)


if __name__ == "__main__":
    import core.database
    uvicorn.run(app,host=HOST,port=int(PORT))

# you can run project without this sentence! run:
#       python3 -m uvicorn main:app --host 'ip' --port 'port'