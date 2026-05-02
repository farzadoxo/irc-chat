# Api Documentation
This file will help frontend developers and peoples that want to know how this project API work!
## Public messaging:

### Websocket
```json
URL: "ws://localhost/ws"
Protocol: WebSocket
Content-Type: Json
```

### Get All Messages
```json
URL: "/api/messages"
Method: ["GET"]
------------------------------
Response : 
[
    {
        "id":"111",
        "content":"Hello World!",
        "created_at":"2026.3.2",
        "user":"John"
    }, ...
]
```


### Delete All messages
```json
URL: "/api/messages"
Method: ["DELETE"]
```

### Delete a Specific message
`⚠️ This endpoint is not so optimize and its not recommended!`
```json
URL: "/api/message"
Method: ["DELETE"]
```

### Get a Specific Message
`⚠️ This endpoint is not so optimize and its not recommended!`
```json
URL: "/api/message"
Method: ["GET"]
```

### New Message
`🛑 This endpoint is not in use by api!`
```json 
URL: "/api/message"
Method: ["POST"]
------------------------------
Request:
{
    "content" : "Hello World!"
    // 'id' and 'created_at' field will generate automaticly!
} 
```

## Room messaging:

### Websocket
```json 
URL: "ws://localhost/rws"
Protocol: WebSocket
Content-Type: Json
```

### Get All Rooms 
```json
URL: "/api/rooms"
Method: ["GET"]
------------------------------
Response:
{
    "rooms":
        [
            {
                "id":"cc4er3",
                "name":"Meet",
                "user_limit":5,
                "visable":True
            },
            {
                "id":"2c4rrh",
                "name":"Friends",
                "user_limit":15,
                "visable":False                
            }
        ]

}
```

### Get A Room
```json
URL: "/api/room/{room_id}"
Method: ["GET"]
------------------------------
Response:
{
    "info":
            {
                "id":"cc4er3",
                "name":"Meet",
                "user_limit":"5",
                "visable":True
            },
    "messages":
            [
                {
                    "id":"111",
                    "content":"Hey sup man?",
                    "created_at":"2026.3.2",
                    "user":"John"
                },
                {
                    "id":"1232",
                    "content:"Im good n!",
                    "created_at":"2026.3.2",
                    "user":"Bob"
                }
            ]
}
```
### Delete a Room
```json
URL: "/api/room"
Method: ["DELETE"]
------------------------------
```

### New room
`🛑 This endpoint is not in use by api!`
```json
URL: "/api/rooms"
Method: ["POST"]
------------------------------
Request:
{
    "content" : "Hello World!",
    "room_id" : "cc44rwd"
    // 'id' and 'created_at' field will generate automaticly!
} 
```

