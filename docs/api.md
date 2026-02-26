# Api Documentation

### Websocket
```json
URL: "ws://localhost/"
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
        "created_at":"2026.3.2"
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
`🛑 This endpoint is not in use with api!`
```json 
URL: "/api/message"
Method: ["POST"]
------------------------------
Request:
{
    "content" : "Hello World!"
    // 'id' and 'created_at' field will generate automaticly!
} 
