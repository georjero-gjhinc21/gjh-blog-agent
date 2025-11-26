# GJH Blog Agent - Quick Start Guide

## Initial Setup (One-Time)

### 1. Start Infrastructure

```bash
./start.sh
```

This will:
- Check Ollama is running
- Start PostgreSQL and Redis
- Verify all services are ready

### 2. Initialize Database

```bash
./venv/bin/python main.py init
```

This creates database tables and seeds sample affiliate products.

## Generate Your First Blog Post

### Manual Mode

```bash
./venv/bin/python main.py workflow
```

This will:
1. Discover trending topics in government contracting
2. Select the best topic
3. Match an affiliate product
4. Generate an 800-1500 word blog post using Ollama
5. "Publish" the post (creates markdown file)

### Check Results

```bash
# List all posts
./venv/bin/python main.py list-posts

# View the generated file
ls -lh data/posts/

# See the content
cat data/posts/*.md
```

## Automated Mode (2-3 Posts per Week)

### Option 1: Docker Compose (Recommended)

Start Celery workers and scheduler:

```bash
docker compose up -d celery-worker celery-beat
```

Check logs:

```bash
docker compose logs -f celery-worker celery-beat
```

The system will automatically:
- **Monday, 8 AM**: Generate and publish blog post
- **Wednesday, 8 AM**: Generate and publish blog post
- **Friday, 8 AM**: Generate and publish blog post
- **Daily, 6 AM**: Discover new trending topics
- **Daily, 11 PM**: Update metrics

### Option 2: Manual Celery (Development)

Terminal 1 - Worker:
```bash
source venv/bin/activate
celery -A tasks.celery_app worker --loglevel=info
```

Terminal 2 - Beat Scheduler:
```bash
source venv/bin/activate
celery -A tasks.celery_app beat --loglevel=info
```

### Option 3: Cron Jobs

Add to crontab (`crontab -e`):

```cron
# Generate blog posts
0 8 * * 1 cd /opt/gjh-blog-agent && ./venv/bin/python main.py workflow >> /var/log/gjh-blog.log 2>&1
0 8 * * 3 cd /opt/gjh-blog-agent && ./venv/bin/python main.py workflow >> /var/log/gjh-blog.log 2>&1
0 8 * * 5 cd /opt/gjh-blog-agent && ./venv/bin/python main.py workflow >> /var/log/gjh-blog.log 2>&1

# Discover topics daily
0 6 * * * cd /opt/gjh-blog-agent && ./venv/bin/python main.py discover >> /var/log/gjh-blog.log 2>&1
```

## Available Commands

### Core Workflow

```bash
# Complete workflow (discover → generate → publish)
./venv/bin/python main.py workflow

# Individual steps
./venv/bin/python main.py discover           # Find new topics
./venv/bin/python main.py generate           # Generate blog post
./venv/bin/python main.py publish <post_id>  # Publish specific post
```

### Management

```bash
# List posts
./venv/bin/python main.py list-posts
./venv/bin/python main.py list-posts --status published
./venv/bin/python main.py list-posts --status draft

# View statistics
./venv/bin/python main.py stats

# Add affiliate product
./venv/bin/python main.py add-product \
  "Product Name" \
  "Description" \
  "Category" \
  "https://affiliate-link" \
  --commission-rate 20.0
```

## Monitoring

### Check System Status

```bash
# Infrastructure
docker compose ps

# Logs
docker compose logs postgres
docker compose logs redis
docker compose logs celery-worker
docker compose logs celery-beat

# Generated posts
ls -lh data/posts/
```

### View Performance

```bash
./venv/bin/python main.py stats
```

Shows:
- Total posts published
- Page views and traffic
- Affiliate clicks and conversions
- Revenue generated
- Top performing posts

## Troubleshooting

### Ollama Not Running

```bash
# Check Ollama
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve
```

### Database Connection Issues

```bash
# Restart PostgreSQL
docker compose restart postgres

# Check logs
docker compose logs postgres
```

### Redis Issues

```bash
# Restart Redis
docker compose restart redis

# Test connection
docker compose exec redis redis-cli ping
```

### Generate Test Post Manually

```bash
# Skip automation, generate one post now
./venv/bin/python main.py workflow
```

## Production Deployment

### 1. Update .env with Real Values

```bash
# Vercel (for actual deployment)
VERCEL_TOKEN=your_vercel_token
VERCEL_PROJECT_ID=your_project_id

# PartnerStack (for real affiliate links)
PARTNERSTACK_API_KEY=your_api_key
```

### 2. Enable Milvus (Optional - Vector Search)

Install system dependency:
```bash
sudo apt-get install python3-dev
```

Uncomment in requirements.txt:
```
pymilvus==2.3.4
```

Reinstall:
```bash
./venv/bin/pip install -r requirements.txt
```

Start Milvus:
```bash
docker compose up -d milvus-standalone milvus-etcd milvus-minio
```

### 3. Start All Services

```bash
docker compose up -d
```

### 4. Monitor

```bash
# View all logs
docker compose logs -f

# Check specific service
docker compose logs -f celery-beat
```

## Stopping the System

```bash
./stop.sh
```

Or manually:

```bash
# Stop all containers
docker compose down

# Stop and remove all data (WARNING!)
docker compose down -v
```

## Next Steps

1. ✅ System is running and generating posts
2. Configure real Vercel deployment credentials
3. Add real PartnerStack affiliate products
4. Set up analytics tracking (Google Analytics, etc.)
5. Monitor and optimize content quality
6. Adjust posting schedule as needed

## Support

For issues or questions:
- Check logs: `docker compose logs`
- Review README.md for detailed documentation
- Verify Ollama is running with llama3.1:8b model
