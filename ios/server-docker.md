# Server Components and Docker Workflows

iOS apps often have companion server components for sync, multiplayer, or API services.

## Server Architecture Pattern

```
collab_server/
├── app.py                    # Main Flask/Express server
├── requirements.txt          # Python deps (or package.json)
├── Dockerfile
├── docker-compose.yml
├── healthcheck.sh
└── config/
    └── config.json           # Runtime configuration
```

## Dockerfile Pattern

Multi-stage build with health checks:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create data directories
RUN mkdir -p /app/sessions /app/config

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:6001/health || exit 1

# Inject git commit at build time
ARG GIT_COMMIT=unknown
ENV GIT_COMMIT=${GIT_COMMIT}

EXPOSE 6001

CMD ["gunicorn", "--bind", "0.0.0.0:6001", "--workers", "2", "--threads", "4", "app:app"]
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
      - "6001:6001"
    volumes:
      - ./sessions:/app/sessions
      - ./config:/app/config:ro
    environment:
      - FLASK_DEBUG=${FLASK_DEBUG:-0}
      - SECRET_KEY=${SECRET_KEY:-}
      - ADMIN_PASSWORD=${ADMIN_PASSWORD:-}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6001/health"]
      interval: 30s
      timeout: 3s
      start_period: 5s
      retries: 3
```

## GitHub Actions: Build and Push Docker

`.github/workflows/docker-publish.yml`:

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [main]
    paths:
      - 'collab_server/**'
  pull_request:
    branches: [main]
    paths:
      - 'collab_server/**'
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository_owner }}/projectname

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata for Docker
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          # Note: 'latest' tag is managed by appstore-release.yml
          tags: |
            type=sha,format=short
            type=ref,event=branch
            type=ref,event=pr

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: ./collab_server
          build-args: |
            GIT_COMMIT=${{ github.sha }}
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## GitHub Actions: Tag on App Store Release

`.github/workflows/appstore-release.yml` - Syncs Docker tags with iOS releases:

```yaml
name: Tag Docker Image on App Store Release

on:
  schedule:
    - cron: '0 */3 * * *'  # Every 3 hours
  workflow_dispatch:
    inputs:
      force_version:
        description: 'Force tag a specific version'
        required: false
        type: string

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: username/projectname

jobs:
  check-and-tag:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      packages: write
      pull-requests: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install PyJWT cryptography requests

      - name: Check App Store version
        id: appstore
        env:
          ASC_KEY_ID: ${{ secrets.ASC_KEY_ID }}
          ASC_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
          ASC_PRIVATE_KEY: ${{ secrets.ASC_PRIVATE_KEY }}
          APP_APPLE_ID: ${{ secrets.APP_APPLE_ID }}
          FORCE_VERSION: ${{ inputs.force_version }}
        run: python .github/scripts/check_appstore_version.py

      - name: Tag and push with version
        if: steps.appstore.outputs.new_release == 'true'
        run: |
          VERSION="${{ steps.appstore.outputs.version }}"

          docker pull ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:main

          # Tag with marketing version
          docker tag ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:main \
                     ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${VERSION}
          docker push ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${VERSION}

          # Update latest tag
          docker tag ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:main \
                     ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
          docker push ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest

      # Bump version for next development cycle
      - name: Bump version and create PR
        if: steps.appstore.outputs.new_release == 'true'
        run: |
          python3 .github/scripts/bump_version.py ProjectName.xcodeproj/project.pbxproj
        # ... then use peter-evans/create-pull-request@v6
```

## Required Secrets for App Store Connect

```
ASC_KEY_ID        - App Store Connect API Key ID
ASC_ISSUER_ID     - API Key Issuer ID
ASC_PRIVATE_KEY   - The .p8 private key contents
APP_APPLE_ID      - Your app's Apple ID (numeric)
```

Generate these at https://appstoreconnect.apple.com/access/api

## Tagging Strategy

| Trigger | Docker Tags |
|---------|-------------|
| Push to main | `main`, `sha-abc1234` |
| Pull request | `pr-123` |
| App Store release | `1.5`, `latest` |

The `latest` tag tracks App Store releases, not the latest commit. This ensures production servers run the same version as the App Store app.

## Running Locally

```bash
# Build and run
cd collab_server
docker-compose up --build

# Or without Docker
pip install -r requirements.txt
python app.py
```
