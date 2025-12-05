Thank you for contributing! Please follow these steps to get started:

1. Read README.md for setup and architecture details.
2. Copy .env.example to .env and fill in values (do not commit .env).
3. Run tests locally: python -m pip install -r requirements.txt && pytest -q
4. Open a PR with a clear description and link to any related issue.

CI: This repository runs a lightweight CI that installs deps, runs tests, and performs a dependency audit via pip-audit.

Required repository secrets (add in GitHub: Settings → Secrets → Actions):
- KUBECONFIG: kubeconfig content for cluster deployments
- GHCR_PAT: GitHub Container Registry PAT for pushing images (or use repository-specific tokens)
- PARTNERSTACK_API_KEY: (optional) PartnerStack API key for affiliate syncs
- VERCEL_TOKEN: (optional) Vercel token for deployments
- CLOUD_PROVIDER_CREDENTIALS: (optional) any cloud provider credentials needed for deployment

Validate secrets locally: ./scripts/validate_secrets.sh
Validate secrets in GitHub: run the "Validate Secrets" workflow from Actions tab.
