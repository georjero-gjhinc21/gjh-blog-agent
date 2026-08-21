# Bitwarden Secret Management Setup

This guide shows how to configure Bitwarden to manage all secrets for the GJH Blog Agent autonomous operation.

## Why Bitwarden?

- **Centralized Management**: All secrets in one secure vault
- **Team Sharing**: Easy to share with team members
- **Audit Trail**: Track who accessed what and when
- **Version Control**: Keep history of secret changes
- **Free for Personal Use**: No cost for individual developers

## Prerequisites

1. **Bitwarden Account**: Sign up at https://vault.bitwarden.com
2. **Bitwarden Organization** (Optional): For team access
3. **GitHub Repository**: Admin access to configure secrets

## Step 1: Create Bitwarden API Credentials

### 1.1 Login to Bitwarden Web Vault

Visit https://vault.bitwarden.com and login

### 1.2 Create API Key

1. Go to **Settings** → **Security** → **API Key**
2. Click **View API Key**
3. Enter your master password
4. Copy both:
   - `client_id` (starts with "user." or "organization.")
   - `client_secret` (long alphanumeric string)

**⚠️ Important**: Save these credentials securely. You'll need them for GitHub Secrets.

## Step 2: Create Secret Items in Bitwarden

Create the following items in your Bitwarden vault:

### 2.1 PostgreSQL Database

**Item Name**: `GJH Blog - PostgreSQL`
**Type**: Login
**Password**: Your PostgreSQL password (e.g., `gjh_secure_password_2024`)

**Notes**:
```
PostgreSQL database for GJH Blog Agent
Database: gjh_blog
User: gjh_admin
```

### 2.2 PartnerStack API

**Item Name**: `GJH Blog - PartnerStack`
**Type**: Login
**Password**: Your PartnerStack API key

**How to get**:
1. Login to https://app.partnerstack.com
2. Go to **Settings** → **API Keys**
3. Create a new API key
4. Copy the key

**Notes**:
```
PartnerStack API for affiliate product matching
Used for: Topic discovery and content generation
```

### 2.3 Vercel Deployment

**Item Name**: `GJH Blog - Vercel`
**Type**: Login
**Username**: (optional) your Vercel email
**Password**: (leave empty or use dummy value)

**Custom Fields** (click "New Custom Field"):

| Field Name | Type | Value |
|------------|------|-------|
| `token` | Hidden | Your Vercel token |
| `org_id` | Text | Your Vercel organization ID |
| `project_id` | Text | Your Vercel project ID |
| `deploy_hook` | Text | Your Vercel deploy hook URL |

**How to get Vercel credentials**:

1. **Token**:
   - Go to https://vercel.com/account/tokens
   - Click **Create Token**
   - Name: "GJH Blog Agent"
   - Scope: Full Account
   - Copy the token

2. **Organization ID & Project ID**:
   ```bash
   cd frontend
   npm install -g vercel
   vercel link
   cat .vercel/project.json
   ```
   Copy `orgId` and `projectId` from the JSON output

3. **Deploy Hook**:
   - Go to your Vercel project settings
   - Click **Git** → **Deploy Hooks**
   - Create a new hook for `main` branch
   - Copy the URL

**Notes**:
```
Vercel deployment credentials
Project: gjhconsulting.net
Used for: Automated frontend deployment
```

## Step 3: Configure GitHub Secrets

Only 3 secrets needed in GitHub (Settings → Secrets and variables → Actions):

### 3.1 BW_CLIENT_ID

**Value**: Your Bitwarden API client ID (from Step 1.2)
**Example**: `user.abc123-def456-ghi789`

### 3.2 BW_CLIENT_SECRET

**Value**: Your Bitwarden API client secret (from Step 1.2)
**Example**: `AbCdEf123456...`

### 3.3 BW_PASSWORD

**Value**: Your Bitwarden master password
**⚠️ Security**: Use a strong, unique password

## Step 4: Verify Setup

### 4.1 Test Bitwarden CLI Locally

```bash
# Install Bitwarden CLI
wget https://vault.bitwarden.com/download/?app=cli&platform=linux -O bw.zip
unzip bw.zip
sudo mv bw /usr/local/bin/
bw --version

# Login with API credentials
export BW_CLIENTID="user.your-client-id"
export BW_CLIENTSECRET="your-client-secret"
bw login --apikey

# Unlock vault
export BW_SESSION=$(bw unlock "your-master-password" --raw)

# Test fetching secrets
bw get password "GJH Blog - PostgreSQL" --session $BW_SESSION
bw get password "GJH Blog - PartnerStack" --session $BW_SESSION
bw get item "GJH Blog - Vercel" --session $BW_SESSION | jq -r '.fields[] | select(.name=="token") | .value'

# Lock vault
bw lock
```

### 4.2 Test GitHub Actions Workflow

1. Go to your GitHub repository
2. Navigate to **Actions** tab
3. Select **Autonomous Blog Generation**
4. Click **Run workflow**
5. Monitor the execution
6. Check "Load secrets from Bitwarden" step succeeds

## Step 5: Organization Setup (Optional)

For team collaboration, use a Bitwarden Organization:

### 5.1 Create Organization

1. Login to Bitwarden web vault
2. Click **New** → **Organization**
3. Name: "GJH Consulting"
4. Plan: Free (2 users) or paid for more features

### 5.2 Share Secrets

1. Create a Collection: "GJH Blog Agent"
2. Move all secret items to the collection
3. Share collection with team members
4. Set permissions (read-only for most users)

### 5.3 Use Organization API Credentials

Update GitHub secrets to use organization credentials:
- `BW_CLIENT_ID`: Organization client ID (starts with "organization.")
- `BW_CLIENT_SECRET`: Organization client secret

## Security Best Practices

### ✅ Do's

- **Use strong master password**: 20+ characters, unique
- **Enable 2FA**: Add two-factor authentication to Bitwarden
- **Rotate secrets regularly**: Update API keys quarterly
- **Use organization**: Share secrets securely with team
- **Audit access**: Review Bitwarden event logs monthly
- **Backup vault**: Export encrypted backup regularly

### ❌ Don'ts

- **Don't share master password**: Each person should have their own account
- **Don't commit secrets**: Never put secrets in code or git
- **Don't use weak passwords**: Avoid common or reused passwords
- **Don't skip 2FA**: Always enable two-factor authentication
- **Don't leave sessions unlocked**: Lock vault when done

## Troubleshooting

### Error: "Invalid client_id or client_secret"

**Solution**: Verify your API credentials in Bitwarden settings. They may have been regenerated.

### Error: "Failed to unlock vault"

**Solution**: Check your master password. Ensure no extra spaces or characters.

### Error: "Item not found"

**Solution**: Verify item names exactly match:
- `GJH Blog - PostgreSQL`
- `GJH Blog - PartnerStack`
- `GJH Blog - Vercel`

Case-sensitive, spaces matter!

### Error: "Session expired"

**Solution**: The BW_SESSION token expires. Re-run the unlock command:
```bash
export BW_SESSION=$(bw unlock "your-password" --raw)
```

### Custom Fields Not Found

**Solution**: Ensure custom fields in "GJH Blog - Vercel" are named exactly:
- `token` (not "Token" or "ACCESS_TOKEN")
- `org_id` (not "orgId" or "organization_id")
- `project_id` (not "projectId" or "project")
- `deploy_hook` (not "deployHook" or "webhook")

## Maintenance

### Monthly Tasks

1. **Review Access Logs**: Check who accessed secrets
2. **Update Expiring Secrets**: Rotate API keys before expiration
3. **Audit Team Access**: Remove departed team members
4. **Test Recovery**: Verify backup can restore vault

### Quarterly Tasks

1. **Rotate All Secrets**: Generate new API keys
2. **Update Master Password**: Change to new strong password
3. **Review Workflows**: Ensure automation still works
4. **Update Documentation**: Keep this guide current

## Migration from GitHub Secrets

If you already have secrets in GitHub:

1. **Copy to Bitwarden**: Create items in vault with current values
2. **Test Workflows**: Run a test workflow to verify Bitwarden integration
3. **Remove GitHub Secrets**: Delete old secrets from GitHub (keep only BW_* secrets)

## Advanced: Multiple Environments

To support dev/staging/production:

### Create Environment-Specific Items

- `GJH Blog - PostgreSQL - Dev`
- `GJH Blog - PostgreSQL - Staging`
- `GJH Blog - PostgreSQL - Production`

### Use Workflow Inputs

```yaml
workflow_dispatch:
  inputs:
    environment:
      description: 'Environment'
      required: true
      default: 'production'
      type: choice
      options:
        - development
        - staging
        - production
```

### Update Secret Loading

Modify `.github/actions/bitwarden-secrets/action.yml` to include environment suffix:
```bash
get_secret "GJH Blog - PostgreSQL - ${{ inputs.environment }}"
```

## Support

For issues with:
- **Bitwarden**: https://bitwarden.com/help/
- **GitHub Actions**: https://docs.github.com/actions
- **This Setup**: Create an issue in the repository

## Resources

- [Bitwarden CLI Documentation](https://bitwarden.com/help/cli/)
- [GitHub Actions Secrets](https://docs.github.com/actions/security-guides/encrypted-secrets)
- [Bitwarden Best Practices](https://bitwarden.com/help/bitwarden-security-white-paper/)
