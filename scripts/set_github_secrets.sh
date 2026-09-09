#!/usr/bin/env bash
set -euo pipefail

# Usage: run this script from your local machine where required secret values/files exist.
# It auto-detects the repo from git remote if REPO env var is not provided.

REPO=${REPO:-}
if [ -z "$REPO" ]; then
  REMOTE_URL=$(git config --get remote.origin.url || true)
  if [ -n "$REMOTE_URL" ] && echo "$REMOTE_URL" | grep -q "github.com"; then
    REPO=$(echo "$REMOTE_URL" | sed -E 's#.*github.com[:/]+([^/]+/[^/.]+)(\.git)?#\1#')
    REPO=${REPO%.git}
  fi
fi

if [ -z "$REPO" ]; then
  echo "ERROR: Could not detect repository. Set REPO=owner/repo or ensure git remote origin is set." >&2
  exit 1
fi

echo "Target repository: $REPO"

if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: gh CLI not found. Install and authenticate (https://cli.github.com/)." >&2
  exit 1
fi

# KUBECONFIG (needed for deploy; skipped with warning if absent so that
# affiliate-only setups, e.g. a DGX/Coder box holding API keys, can still
# provision workflow secrets without a cluster config).
KUBECONFIG_BODY=""
if [ -f "$HOME/.kube/config" ]; then
  KUBECONFIG_BODY=$(cat "$HOME/.kube/config")
elif [ -n "${KUBECONFIG_CONTENT-}" ]; then
  KUBECONFIG_BODY="$KUBECONFIG_CONTENT"
fi
if [ -z "$KUBECONFIG_BODY" ]; then
  echo "KUBECONFIG not found locally; skipping (only needed for deploy)."
else
  echo "Setting KUBECONFIG..."
  printf "%s" "$KUBECONFIG_BODY" | gh secret set KUBECONFIG -R "$REPO" --body - >/dev/null
fi

echo "Checking GHCR_PAT..."
if [ -z "${GHCR_PAT-}" ]; then
  echo "GHCR_PAT environment variable not set; skipping (only needed for deploy)."
else
  echo "Setting GHCR_PAT..."
  gh secret set GHCR_PAT --body "$GHCR_PAT" -R "$REPO"
fi

# Optional secrets: set them if provided
if [ -n "${PARTNERSTACK_API_KEY-}" ]; then
  echo "Setting PARTNERSTACK_API_KEY..."
  gh secret set PARTNERSTACK_API_KEY --body "$PARTNERSTACK_API_KEY" -R "$REPO"
else
  echo "PARTNERSTACK_API_KEY not provided; skipping (optional)."
fi

if [ -n "${PARTNERSTACK_PARTNER_KEY-}" ]; then
  echo "Setting PARTNERSTACK_PARTNER_KEY..."
  gh secret set PARTNERSTACK_PARTNER_KEY --body "$PARTNERSTACK_PARTNER_KEY" -R "$REPO"
else
  echo "PARTNERSTACK_PARTNER_KEY not provided; skipping (optional)."
fi

if [ -n "${IMPACT_ACCOUNT_SID-}" ]; then
  echo "Setting IMPACT_ACCOUNT_SID..."
  gh secret set IMPACT_ACCOUNT_SID --body "$IMPACT_ACCOUNT_SID" -R "$REPO"
else
  echo "IMPACT_ACCOUNT_SID not provided; skipping (optional)."
fi

if [ -n "${IMPACT_AUTH_TOKEN-}" ]; then
  echo "Setting IMPACT_AUTH_TOKEN..."
  gh secret set IMPACT_AUTH_TOKEN --body "$IMPACT_AUTH_TOKEN" -R "$REPO"
else
  echo "IMPACT_AUTH_TOKEN not provided; skipping (optional)."
fi

if [ -n "${VERCEL_TOKEN-}" ]; then
  echo "Setting VERCEL_TOKEN..."
  gh secret set VERCEL_TOKEN --body "$VERCEL_TOKEN" -R "$REPO"
else
  echo "VERCEL_TOKEN not provided; skipping (optional)."
fi

if [ -n "${CLOUD_PROVIDER_CREDENTIALS-}" ]; then
  echo "Setting CLOUD_PROVIDER_CREDENTIALS..."
  gh secret set CLOUD_PROVIDER_CREDENTIALS --body "$CLOUD_PROVIDER_CREDENTIALS" -R "$REPO"
else
  echo "CLOUD_PROVIDER_CREDENTIALS not provided; skipping (optional)."
fi

echo "All requested secrets processed for $REPO."