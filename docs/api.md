# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All endpoints require `X-API-Key` header:

```bash
curl -H "X-API-Key: your-api-key-here" http://localhost:8000/api/v1/...
```

## Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "components": {
    "neo4j": true,
    "weaviate": true,
    "llm": true
  }
}
```

## Authentication Endpoints

### Create API Key

```http
POST /auth/keys
Content-Type: application/json

{
  "name": "My API Key",
  "description": "For development"
}
```

Response:

```json
{
  "id": "uuid",
  "name": "My API Key",
  "key": "key-value-keep-safe",
  "status": "active",
  "org_id": "org-uuid",
  "created_at": "2024-01-01T00:00:00",
  "expires_at": "2024-04-01T00:00:00"
}
```

### Revoke API Key

```http
DELETE /auth/keys/{key_id}
```

## Chat Endpoints

### Start Conversation

```http
POST /chat/start
```

Response:

```json
{
  "conversation_id": "conv-uuid"
}
```

### Send Message

```http
POST /chat/message
Content-Type: application/json

{
  "conversation_id": "conv-uuid",
  "content": "How do I fix my AWS EC2 instance?",
  "context_resources": ["resource-id-1", "resource-id-2"]
}
```

Response:

```json
{
  "message_id": "msg-uuid",
  "conversation_id": "conv-uuid",
  "content": "Step-by-step resolution...",
  "confidence": 0.95
}
```

### WebSocket (Streaming)

```
WS /chat/ws/{conversation_id}
```

Send:

```
{"content": "Your question"}
```

Receive:

```
{"content": "Streaming response..."}
```

## Resource Endpoints

### List Resources

```http
GET /resources?skip=0&limit=100
```

Response:

```json
[
  {
    "id": "resource-uuid",
    "name": "my-instance",
    "resource_type": "ec2",
    "provider": "aws",
    "account_id": "123456789",
    "metadata": {
      "state": "running",
      "instance_type": "t3.medium"
    },
    "org_id": "org-uuid",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

### Get Resource Details

```http
GET /resources/{resource_id}
```

## Admin Endpoints

### Get Organization

```http
GET /admin/organization
```

Response:

```json
{
  "id": "org-uuid",
  "name": "My Company",
  "description": "Cloud infrastructure",
  "created_at": "2024-01-01T00:00:00"
}
```

### List API Keys

```http
GET /admin/keys
```

Response:

```json
[
  {
    "id": "key-uuid",
    "name": "API Key 1",
    "status": "active",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {}
  }
}
```

### HTTP Status Codes

- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Validation Error
- `500`: Internal Server Error
- `502`: Bad Gateway (Cloud API error)
- `503`: Service Unavailable (LLM error)
