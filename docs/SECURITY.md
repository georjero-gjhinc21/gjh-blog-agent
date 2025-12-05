Secrets management

Do not store secrets in the repository. Use `.env.example` as a template and a secrets manager (GitHub Secrets, AWS Secrets Manager, HashiCorp Vault) for production and CI.

CI configuration:
- Add required secrets to your repository's settings (VERCEL_TOKEN, PARTNERSTACK_API_KEY, DATABASE_URL, etc.)
- The CI workflow will use these secrets during deployment steps.
