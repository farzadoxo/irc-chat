# Database Documentation 

### Database info
```json
Type: "Redis(Valkey)"
Host: "for docker:'redis' for local:'127.0.0.1'"
Port: "6379"
```

## Stracture 
We have a redis-list for public chats.KEY of this list is "messages".
All public messages will stored in the list with following stracture:

### Public messages
--> messages: 
1) "{"id":"5345345", "content":"Hi there.", "created_at":"2026-02-07", "username":"test"}"
2) "{"id":"4534534","content":"sup money?","created_at":"2025-01-12", "username":"test2"}"

### Room messages
-->:
1) "{"id":"5345345", "room_id":"c43r5r", "content":"Hi there.", "created_at":"2026-02-07", "username":"test"}"
2) "{"id":"4534534", "room_id":"453ggt", "content":"sup money?","created_at":"2025-01-12", "username":"test2"}"