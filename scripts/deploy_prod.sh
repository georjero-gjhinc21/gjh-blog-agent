#!/usr/bin/env bash
set -euo pipefail

# Simple deploy script (local) - requires docker and kubectl configured with access to the cluster
IMAGE=${IMAGE:-ghcr.io/yourorg/gjh-blog-agent:latest}

if [ -z "$IMAGE" ]; then
  echo "IMAGE environment variable must be set"
  exit 1
fi

echo "Building image $IMAGE"
docker build -t "$IMAGE" .

echo "Pushing image $IMAGE"
docker push "$IMAGE"

echo "Applying Kubernetes manifests"
kubectl apply -f k8s/celery_workers.yaml
kubectl apply -f k8s/hpa.yaml || true
kubectl apply -f k8s/keda_scaledobject.yaml || true

# Optional: update deployments' images
kubectl set image deployment/celery-research-worker celery-research=$IMAGE --namespace default || true
kubectl set image deployment/celery-generator-worker celery-generator=$IMAGE --namespace default || true

# Wait for rollouts
kubectl rollout status deployment/celery-research-worker --timeout=120s || true
kubectl rollout status deployment/celery-generator-worker --timeout=120s || true

echo "Deploy complete. Verify logs and healthchecks."