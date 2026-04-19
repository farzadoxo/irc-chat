# Database Documentation 

### Database info
```json
Type: "Redis(Valkey)"
Host: "for docker:'redis' for local:'127.0.0.1'"
Port: "6379"
```

### Stracture 
We have a redis-list for public chats.KEY of this list is "messages".
All public messages will stored in the list with following stracture:

--> messages: 
1) "{"id":"5345345", "content":"Hi there.", "created_at":"2026-02-07", "username":"test"}"
2) "{"id":"4534534","content":"sup money?","created_at":"2025-01-12", "username":"test2"}"

`This stracture is for public message`
