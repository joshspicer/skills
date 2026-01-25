# Server Components and Docker Workflows

## Key Patterns

1. **Commit embedding** - Pass git commit into container at build time
2. **Health checks** - Always include for container orchestration
3. **App Store version sync** - Tag Docker images when iOS app releases

## Dockerfile Essentials

The important parts, regardless of language/framework:

```dockerfile
# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Inject git commit at build time
ARG GIT_COMMIT=unknown
ENV GIT_COMMIT=${GIT_COMMIT}

EXPOSE 8080
```

## docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      args:
        GIT_COMMIT: ${GIT_COMMIT:-unknown}
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
      - ./config:/app/config:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 3s
      start_period: 5s
      retries: 3
```

## GitHub Actions: Build and Push

`.github/workflows/docker-publish.yml`:

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [main]
    paths:
      - 'server/**'
  pull_request:
    branches: [main]
    paths:
      - 'server/**'
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository_owner }}/${{ github.event.repository.name }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,format=short
            type=ref,event=branch
            type=ref,event=pr

      - uses: docker/build-push-action@v5
        with:
          context: ./server
          build-args: |
            GIT_COMMIT=${{ github.sha }}
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## GitHub Actions: App Store Release Sync

Tags Docker image with App Store version when iOS app releases. This ensures server version matches the iOS app in production.

`.github/workflows/appstore-release.yml`:

```yaml
name: Tag Docker Image on App Store Release

on:
  schedule:
    - cron: '0 */3 * * *'  # Check every 3 hours
  workflow_dispatch:
    inputs:
      force_version:
        description: 'Force tag a specific version'
        required: false

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository_owner }}/${{ github.event.repository.name }}

jobs:
  check-and-tag:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      packages: write

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - run: pip install PyJWT cryptography requests

      - id: appstore
        env:
          ASC_KEY_ID: ${{ secrets.ASC_KEY_ID }}
          ASC_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
          ASC_PRIVATE_KEY: ${{ secrets.ASC_PRIVATE_KEY }}
          APP_APPLE_ID: ${{ secrets.APP_APPLE_ID }}
        run: python .github/scripts/check_appstore_version.py

      - if: steps.appstore.outputs.new_release == 'true'
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - if: steps.appstore.outputs.new_release == 'true'
        run: |
          VERSION="${{ steps.appstore.outputs.version }}"
          docker pull ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:main

          # Tag with app version (e.g., 1.5)
          docker tag ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:main \
                     ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${VERSION}
          docker push ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${VERSION}

          # Update latest tag
          docker tag ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:main \
                     ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
          docker push ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
```

## Required Secrets for App Store Connect

Generate API key at https://appstoreconnect.apple.com/access/api

```
ASC_KEY_ID        - API Key ID
ASC_ISSUER_ID     - Issuer ID
ASC_PRIVATE_KEY   - Contents of .p8 file
APP_APPLE_ID      - Your app's Apple ID (numeric)
```

## Tagging Strategy

| Trigger | Docker Tags |
|---------|-------------|
| Push to main | `main`, `sha-abc1234` |
| Pull request | `pr-123` |
| App Store release | `1.5`, `latest` |

The `latest` tag tracks App Store releases, ensuring production servers match the iOS app version.
