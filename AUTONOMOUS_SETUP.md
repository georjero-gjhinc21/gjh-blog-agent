# Autonomous Blog Setup Guide

This guide explains how to set up the GJH Consulting Blog to run autonomously from GitHub Actions.

## Overview

The autonomous blog system will:
- 🤖 **Auto-generate posts**: 2-3 times per week (Tuesday & Friday at 10 AM UTC)
- 🔍 **Discover trending topics**: Automatically research government contracting trends
- 💰 **Match affiliate products**: Integrate PartnerStack products into posts
- 📝 **Generate content**: Use Ollama LLM to write 800-1500 word blog posts
- 🚀 **Deploy automatically**: Push to Vercel when posts are ready
- 📊 **Track metrics**: Monitor performance and revenue

## Secret Management with Bitwarden

This project uses **Bitwarden** for centralized secret management. All API keys and credentials are stored in a Bitwarden vault and fetched during workflow execution.

### Quick Setup (3 GitHub Secrets Only!)

Configure these in your GitHub repository settings (`Settings > Secrets and variables > Actions`):

```
BW_CLIENT_ID
```
- Your Bitwarden API client ID
- Get from: Bitwarden web vault → Settings → Security → API Key

```
BW_CLIENT_SECRET
```
- Your Bitwarden API client secret
- Get from: Same location as client ID

```
BW_PASSWORD
```
- Your Bitwarden master password
- Use a strong, unique password

### Bitwarden Vault Setup

Create these items in your Bitwarden vault:

1. **GJH Blog - PostgreSQL** (Login item)
   - Password: Your PostgreSQL password

2. **GJH Blog - PartnerStack** (Login item)
   - Password: Your PartnerStack API key

3. **GJH Blog - Vercel** (Login item with custom fields)
   - Custom field `token`: Vercel API token
   - Custom field `org_id`: Vercel organization ID
   - Custom field `project_id`: Vercel project ID
   - Custom field `deploy_hook`: Deploy hook URL

**📖 Complete Bitwarden setup guide**: See [BITWARDEN_SETUP.md](BITWARDEN_SETUP.md)

### GitHub (Automatic)

```
GITHUB_TOKEN
```
- Automatically provided by GitHub Actions
- No configuration needed

## Workflows

### 1. Autonomous Blog Generation (`.github/workflows/autonomous-blog.yml`)

**Schedule**: Tuesday and Friday at 10 AM UTC

**Steps**:
1. Set up infrastructure (PostgreSQL, Redis)
2. Install Python dependencies
3. Download and run Ollama LLM
4. Discover 10 trending topics
5. Generate a blog post
6. Copy post to frontend
7. Commit and push changes
8. Trigger Vercel deployment

**Manual trigger**: Can be triggered manually via GitHub Actions UI

### 2. Frontend Deployment (`.github/workflows/deploy-frontend.yml`)

**Trigger**: Automatically on push to `main` branch when frontend files change

**Steps**:
1. Build Next.js frontend
2. Deploy to Vercel production

## Setup Instructions

### Step 1: Set Up Bitwarden Vault

**Complete guide**: [BITWARDEN_SETUP.md](BITWARDEN_SETUP.md)

Quick steps:
1. Create Bitwarden account at https://vault.bitwarden.com
2. Generate API credentials (Settings → Security → API Key)
3. Create secret items in vault (PostgreSQL, PartnerStack, Vercel)
4. Configure custom fields for Vercel item

### Step 2: Configure GitHub Secrets

1. Go to your repository on GitHub
2. Click `Settings > Secrets and variables > Actions`
3. Click `New repository secret`
4. Add these 3 secrets:
   - `BW_CLIENT_ID`
   - `BW_CLIENT_SECRET`
   - `BW_PASSWORD`

### Step 3: Link Vercel Project

```bash
cd frontend
npm install -g vercel
vercel link
```

This creates `.vercel/project.json` with your project and org IDs.

### Step 4: Enable Workflows

The workflows are already committed. GitHub Actions will automatically:
- Run autonomous blog generation on schedule
- Deploy frontend when changes are pushed

### Step 5: Test Manual Run

1. Go to `Actions` tab in GitHub
2. Select `Autonomous Blog Generation`
3. Click `Run workflow`
4. Monitor the execution

## Monitoring

### Check Workflow Status

- Go to `Actions` tab in GitHub
- View recent workflow runs
- Check logs for any errors

### View Generated Posts

- Check `frontend/posts/` directory
- New posts are automatically committed by the bot
- Posts are deployed to https://gjhconsulting.net

### Statistics

Each workflow run includes statistics output showing:
- Topics discovered
- Posts generated
- Affiliate revenue potential
- Database metrics

## Troubleshooting

### Workflow Fails on Database Init

**Solution**: Database may already be initialized. This is expected and won't stop the workflow.

### No Topics Found

**Solution**: 
- Check PartnerStack API key is valid
- Topics may already be in use
- Try manual trigger to generate more topics

### Ollama Model Download Fails

**Solution**: 
- Workflow may need more time
- Check GitHub Actions runner has sufficient resources
- Model downloads automatically on first run

### Vercel Deployment Fails

**Solution**:
- Verify all Vercel secrets are set correctly
- Check Vercel token has deployment permissions
- Ensure project is properly linked

## Cost Considerations

- **GitHub Actions**: Free for public repos, 2000 minutes/month for private
- **Ollama**: Runs locally in the workflow, no API costs
- **Vercel**: Free tier supports hobby projects, upgrade for production
- **PartnerStack**: Free to join, earn commissions on referrals

## Security Notes

1. **Never commit secrets**: All sensitive data is in GitHub Secrets
2. **Database password**: Use strong password, rotate regularly
3. **API keys**: Monitor usage, revoke if compromised
4. **Vercel token**: Limit permissions to deployment only

## Customization

### Change Schedule

Edit `.github/workflows/autonomous-blog.yml`:

```yaml
on:
  schedule:
    # Daily at noon UTC
    - cron: '0 12 * * *'
    # Or weekly on Monday
    - cron: '0 10 * * 1'
```

### Adjust Post Frequency

Modify the `discover --max-topics` parameter to generate more or fewer topics.

### Change LLM Model

Edit the workflow to use a different Ollama model:

```bash
# nvidia-api pull (removed - using NVIDIA API) llama3.1:70b  # Larger, better quality
# nvidia-api pull (removed - using NVIDIA API) llama3.1:8b   # Faster, lower quality
```

## Next Steps

1. ✅ Configure GitHub Secrets
2. ✅ Link Vercel project
3. ✅ Test manual workflow run
4. 📊 Monitor first automated run
5. 🎯 Optimize based on performance metrics

## Support

For issues or questions:
- Check workflow logs in GitHub Actions
- Review error messages in the statistics output
- Ensure all secrets are configured correctly
