# Deployment Guide

## Local Development

### Prerequisites

- Docker & Docker Compose
- Python 3.10+
- Git

### Quick Start

1. Clone and setup:

   ```bash
   git clone <repo-url>
   cd cloud-companion
   ```

2. Start all services:

   ```bash
   docker-compose up -d
   ```

3. Wait for services to be healthy:

   ```bash
   docker-compose ps
   ```

4. Test the API:

   ```bash
   curl http://localhost:8000/health
   ```

5. Access services:
   - API: http://localhost:8000
   - Neo4j Browser: http://localhost:7474 (neo4j/changeme)
   - Weaviate Console: http://localhost:8080
   - Ollama: http://localhost:11434

## Production Deployment

### Docker

Build image:

```bash
docker build -t cloud-companion:latest .
```

Run with environment variables:

```bash
docker run -d \
  -e NEO4J_PASSWORD=your-strong-password \
  -e ENCRYPTION_KEY=your-strong-key \
  -e DEBUG=false \
  -p 8000:8000 \
  cloud-companion:latest
```

### Docker Compose (Self-Hosted)

Modify `docker-compose.yml`:

1. Change default passwords
2. Set production encryption key
3. Configure resource limits
4. Use persistent volumes
5. Configure backups for Neo4j

### Kubernetes

Create `k8s/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cloud-companion
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cloud-companion
  template:
    metadata:
      labels:
        app: cloud-companion
    spec:
      containers:
        - name: api
          image: cloud-companion:latest
          ports:
            - containerPort: 8000
          env:
            - name: NEO4J_URI
              valueFrom:
                configMapKeyRef:
                  name: config
                  key: neo4j_uri
            - name: ENCRYPTION_KEY
              valueFrom:
                secretKeyRef:
                  name: secrets
                  key: encryption_key
```

Deploy:

```bash
kubectl apply -f k8s/
```

## Scaling

### API Server

- Horizontal scaling with load balancer
- Multiple replicas behind reverse proxy (Nginx/HAProxy)

### Neo4j

- Use Neo4j Enterprise for clustering
- Set `NEO4J_dbms_memory_heap_maxSize` based on resources

### Weaviate

- Clustering for HA (Weaviate Enterprise)
- Configure backups

### Ollama

- Run on separate GPU machines
- Use load balancer for multiple instances

## Monitoring

### Logs

```bash
docker logs cloud-companion-api
```

### Health Check

```bash
curl http://localhost:8000/health
```

### Metrics

- Monitor Neo4j queries: http://localhost:7474
- Monitor Weaviate: http://localhost:8080/v1/meta

## Backup & Recovery

### Neo4j Backup

```bash
docker exec cloud-companion-neo4j neo4j-admin database backup neo4j
```

### Restore

```bash
docker exec cloud-companion-neo4j neo4j-admin database restore neo4j
```

## Troubleshooting

### Services not starting

```bash
docker-compose logs neo4j
docker-compose logs weaviate
docker-compose logs app
```

### Connection issues

```bash
docker-compose exec app ping neo4j
docker-compose exec app ping weaviate
```

### Memory issues

Adjust in `docker-compose.yml`:

```yaml
services:
  neo4j:
    environment:
      NEO4J_dbms_memory_heap_maxSize: 4G
```
