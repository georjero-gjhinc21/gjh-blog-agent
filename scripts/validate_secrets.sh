#!/usr/bin/env bash
set -euo pipefail

# Local environment secret validator. Use this before running deploy scripts.
MISSING=0
check() {
  name=$1
  val="${!name:-}"
  if [ -z "$val" ]; then
    echo "[MISSING] $name"
    MISSING=1
  else
    echo "[OK] $name"
  fi
}

check KUBECONFIG
check GHCR_PAT
check PARTNERSTACK_API_KEY
check VERCEL_TOKEN
check CLOUD_PROVIDER_CREDENTIALS

if [ "$MISSING" -eq 1 ]; then
  echo "One or more required secrets are missing. Add them to your environment or GitHub Secrets."
  echo "See CONTRIBUTING.md for instructions."
  exit 1
fi

echo "All required secrets appear to be set (local env)."