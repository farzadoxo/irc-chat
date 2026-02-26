# Database Documentation 

### Database info
```json
Type: "Redis(Valkey)"
Host: "redis"
Port: "6379"
```

### Stracture 
We have a redis-list for public chats.KEY of this list is "messages".
All public messages will stored in the list with following stracture:

--> messages: 
1) "{"id":"5345345", "content":"Hi there.", "created_at":"2026-02-07"}"
2) "{"id":"4534534","content":"sup money?","created_at":"2025-01-12"}"

`This stracture is for public message`
