# GJH Consulting Autonomous Blog Agent

Complete autonomous blog generation system that creates 2-3 SEO-optimized blog posts per week with integrated affiliate marketing.

## Features

- **Research Agent**: Discovers trending topics in government contracting
- **Affiliate Agent**: Matches PartnerStack products to content
- **Content Agent**: Generates 800-1500 word blog posts using local Ollama LLM
- **Publishing Agent**: Deploys to Vercel (gjhconsulting.net)
- **Monitoring Agent**: Tracks performance and revenue metrics

## Architecture

```
┌─────────────────┐
│  Research Agent │──> Discovers Topics
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Affiliate Agent │──> Matches Products
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Content Agent  │──> Generates Posts
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Publishing Agent │──> Deploys to Vercel
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Monitoring Agent │──> Tracks Metrics
└─────────────────┘
```

## Infrastructure

- **PostgreSQL**: Blog posts, topics, affiliate products, metrics
- **Redis**: Task queue and caching
- **Milvus**: Vector database for semantic search
- **Celery**: Automated task scheduling
- **Ollama**: Local LLM (llama3.1:8b) - NO API calls

## Quick Start

### 1. Start Infrastructure

```bash
docker compose up -d
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize Database

```bash
python main.py init
```

### 4. Run Complete Workflow

```bash
python main.py workflow
```

## CLI Commands

### Core Workflow

```bash
# Discover trending topics
python main.py discover --max-topics 10

# Generate a blog post
python main.py generate

# Publish a post
python main.py publish <post_id>

# Run complete workflow (discover → generate → publish)
python main.py workflow
```

### Management

```bash
# List posts
python main.py list-posts --status published --limit 20

# View statistics
python main.py stats

# Add affiliate product
python main.py add-product "Product Name" "Description" "Category" "https://affiliate-link" --commission-rate 20.0

# Show version info
python main.py version
```

## Automated Scheduling

The system automatically generates posts using Celery Beat:

- **Monday, 8 AM**: Generate and publish blog post
- **Wednesday, 8 AM**: Generate and publish blog post
- **Friday, 8 AM**: Generate and publish blog post
- **Daily, 6 AM**: Discover new trending topics
- **Daily, 11 PM**: Update performance metrics

### Start Celery Workers

```bash
# Start worker
celery -A tasks.celery_app worker --loglevel=info

# Start beat scheduler
celery -A tasks.celery_app beat --loglevel=info
```

Or use Docker Compose (workers already configured):

```bash
docker compose up celery-worker celery-beat
```

## Configuration

Edit `.env` file:

```env
# Database
DATABASE_URL=postgresql://gjh_admin:gjh_secure_password_2024@localhost:5432/gjh_blog

# Redis
REDIS_URL=redis://localhost:6379/0

# Milvus
MILVUS_HOST=localhost
MILVUS_PORT=19530

# Ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# Blog
BLOG_DOMAIN=gjhconsulting.net
POSTS_PER_WEEK=3
MIN_WORDS=800
MAX_WORDS=1500

# PartnerStack (optional)
PARTNERSTACK_API_KEY=your_key_here

# Vercel (optional)
VERCEL_TOKEN=your_token_here
VERCEL_PROJECT_ID=your_project_id
```

## Focus Topics

The system generates content around:

- Government contracting
- Federal procurement
- GSA schedules
- SBIR/STTR grants
- Technology consulting
- Data analytics
- Cybersecurity compliance

## Development

### Project Structure

```
gjh-blog-agent/
├── agents/              # AI agents
│   ├── research_agent.py
│   ├── affiliate_agent.py
│   ├── content_agent.py
│   ├── publishing_agent.py
│   └── monitoring_agent.py
├── models/              # Database models
│   └── blog.py
├── database/            # Database connection
│   ├── connection.py
│   └── init.sql
├── tasks/               # Celery tasks
│   ├── celery_app.py
│   └── blog_tasks.py
├── utils/               # Utilities
│   ├── ollama_client.py
│   └── vector_store.py
├── config/              # Configuration
│   └── settings.py
├── data/                # Generated content
│   └── posts/
├── docker-compose.yml   # Infrastructure
├── requirements.txt     # Python dependencies
└── main.py             # CLI interface
```

### Testing

The system includes built-in test data and simulation:

```bash
# Initialize with sample affiliate products
python main.py init

# Generate test traffic metrics
# (automatically happens during stats command)
python main.py stats
```

## Production Deployment

### 1. Set Environment Variables

Set real values in `.env`:
- `VERCEL_TOKEN`
- `VERCEL_PROJECT_ID`
- `PARTNERSTACK_API_KEY`

### 2. Start All Services

```bash
docker compose up -d
```

### 3. Monitor Logs

```bash
docker compose logs -f celery-worker
docker compose logs -f celery-beat
```

### 4. Check Status

```bash
python main.py stats
python main.py list-posts --status published
```

## Performance

- **Topic Discovery**: ~30 seconds
- **Content Generation**: 2-5 minutes (using local LLM)
- **Publishing**: ~10 seconds
- **Total Workflow**: 3-6 minutes per post

## Troubleshooting

### Ollama Connection Issues

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve
```

### Database Connection Issues

```bash
# Check PostgreSQL
docker compose ps postgres

# View logs
docker compose logs postgres
```

### Milvus Issues

```bash
# Restart Milvus stack
docker compose restart milvus-standalone milvus-etcd milvus-minio
```

## License

Proprietary - GJH Consulting

## Support

For issues or questions, contact the GJH Consulting team.
