Ollama and Milvus healthchecks

Recommended Docker Compose healthchecks to ensure Ollama and Milvus are ready before the agent calls them.

Ollama:
- Check HTTP endpoint: GET http://localhost:11434/api/tags (200 OK)
- Example docker-compose healthcheck (service: ollama):
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
    interval: 10s
    timeout: 5s
    retries: 5

Milvus (standalone):
- Use grpc/port probe or milvus health endpoint if available; alternatively check TCP port 19530.
- Example docker-compose healthcheck (service: milvus-standalone):
  healthcheck:
    test: ["CMD", "bash", "-c", "</dev/tcp/localhost/19530" ]
    interval: 10s
    timeout: 5s
    retries: 5

Notes:
- Keep healthchecks conservative to avoid flapping (retries >= 3).
- In CI, mock or skip external services; use unit tests that don't require running Milvus or Ollama.
