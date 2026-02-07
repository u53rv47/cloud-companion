# Architecture & Design

## System Overview

Cloud Companion is a multi-tenant, cloud-agnostic AI chatbot for cloud resource analysis and troubleshooting.

```
┌─────────────────┐
│  Customer UIs   │ (Web, Mobile, Chat Apps)
└────────┬────────┘
         │ HTTP/WebSocket
         ▼
┌─────────────────────────────────────────┐
│      FastAPI Application (v1)           │
│  ├─ /auth      (API Key Management)     │
│  ├─ /chat      (Conversation + WebSocket)
│  ├─ /resources (Cloud Resource CRUD)    │
│  └─ /admin     (Organization Management)│
└────────┬────────┬────────┬──────────────┘
         │        │        │
         ▼        ▼        ▼
    ┌────────┐┌─────────┐┌──────────┐
    │ Neo4j  ││Weaviate ││ Ollama   │
    │(Graph) ││(Vector) ││(LLM)     │
    └────────┘└─────────┘└──────────┘
         │        │        │
         ▼        ▼        ▼
    ┌──────────────────────────────┐
    │  Cloud Crawlers              │
    │  ├─ AWS Crawler              │
    │  ├─ Azure Crawler            │
    │  └─ GCP Crawler              │
    └──────────────────────────────┘
         │
         ▼
    ┌──────────────────────┐
    │ Customer Cloud       │
    │ Accounts             │
    └──────────────────────┘
```

## Database Design

### Neo4j Graph

**Nodes:**

- `Organization`: Company/entity
- `CloudAccount`: AWS/Azure/GCP accounts
- `APIKey`: API keys for authentication
- `CloudResource`: EC2 instances, databases, etc.
- `Conversation`: Chat conversations
- `Message`: Chat messages

**Relationships:**

- `Organization -> HAS_ACCOUNT -> CloudAccount`
- `CloudAccount -> HAS_RESOURCE -> CloudResource`
- `Organization -> HAS_KEY -> APIKey`
- `Conversation -> HAS_MESSAGE -> Message`

### Weaviate (Vector DB)

Stores embeddings of:

- Cloud resources (descriptions, metadata)
- Cloud documentation
- Common issues and solutions

Enables semantic search for contextual information.

## Authentication

**API Key Flow:**

1. Organization creates API key via `/auth/keys`
2. Key is hashed and stored in Neo4j
3. Client includes key in `X-API-Key` header
4. Middleware verifies and extracts org context
5. All queries scoped to organization

## Multi-Tenancy

Every request includes `RequestContext`:

- `org_id`: Organization identifier
- `api_key_id`: Key identifier
- `account_ids`: Accessible cloud accounts

All database queries filtered by `org_id`.

## Data Privacy

- **No credential storage**: Cloud credentials passed temporarily, never persisted
- **No data export**: Raw resource data stays in customer's graph DB
- **Encrypted configs**: Account configurations encrypted at rest
- **Local LLM**: Option to run LLM locally, no external calls
