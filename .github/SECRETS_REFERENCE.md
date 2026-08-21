# Secrets Quick Reference

## Bitwarden Vault Items

### Item 1: GJH Blog - PostgreSQL
```
Type: Login
Password: [PostgreSQL database password]

Usage: Database connection for blog posts storage
```

### Item 2: GJH Blog - PartnerStack
```
Type: Login
Password: [PartnerStack API key]

Usage: Affiliate product matching and link generation
Get from: https://app.partnerstack.com/settings/api
```

### Item 3: GJH Blog - Vercel
```
Type: Login
Custom Fields:
  - token: [Vercel API token]
  - org_id: [Vercel organization ID]
  - project_id: [Vercel project ID]
  - deploy_hook: [Deploy hook URL]

Get credentials:
  - Token: https://vercel.com/account/tokens
  - IDs: Run 'vercel link' in frontend/ directory
  - Hook: Project settings → Git → Deploy Hooks
```

## GitHub Repository Secrets

Only 3 secrets needed:

```
BW_CLIENT_ID       = user.xxxxx-xxxxx-xxxxx
BW_CLIENT_SECRET   = xxxxxxxxxxxxxxxxxxxxxxx
BW_PASSWORD        = [Your Bitwarden master password]
```

Get from: Bitwarden web vault → Settings → Security → API Key

## Verification Checklist

- [ ] Bitwarden vault has all 3 items created
- [ ] Custom fields added to "GJH Blog - Vercel" item
- [ ] GitHub secrets configured (BW_CLIENT_ID, BW_CLIENT_SECRET, BW_PASSWORD)
- [ ] Vercel project linked (vercel link in frontend/)
- [ ] Test workflow run succeeded

## Environment Variables (Loaded Automatically)

These are fetched from Bitwarden during workflow execution:

```bash
POSTGRES_PASSWORD       # From: GJH Blog - PostgreSQL
PARTNERSTACK_API_KEY    # From: GJH Blog - PartnerStack
VERCEL_TOKEN           # From: GJH Blog - Vercel → field 'token'
VERCEL_ORG_ID          # From: GJH Blog - Vercel → field 'org_id'
VERCEL_PROJECT_ID      # From: GJH Blog - Vercel → field 'project_id'
VERCEL_DEPLOY_HOOK     # From: GJH Blog - Vercel → field 'deploy_hook'
```

## Troubleshooting

**Workflow fails on "Load secrets from Bitwarden"**
- Verify BW_CLIENT_ID, BW_CLIENT_SECRET, BW_PASSWORD in GitHub secrets
- Check item names in Bitwarden match exactly (case-sensitive)
- Ensure custom fields in Vercel item use correct names

**Secret value is empty**
- Verify item exists in Bitwarden vault
- Check custom field names (lowercase with underscores)
- Sync vault: `bw sync`

**More help**: See [BITWARDEN_SETUP.md](../BITWARDEN_SETUP.md)
