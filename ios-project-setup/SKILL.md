---
name: ios-project-setup
description: Standard patterns for setting up iOS projects including MCP server configuration, Info.plist handling, version/commit embedding, server components with Docker workflows, code organization, and simulator instructions. Use when creating new iOS projects or configuring existing ones.
metadata:
  author: joshspicer
  version: "1.0"
compatibility: Requires Xcode, npx for MCP servers, and optionally Docker for server components.
---

# iOS Project Setup

Standard patterns and configurations for iOS projects.

## Project Structure

```
ProjectName/
├── .vscode/
│   └── mcp.json                    # MCP server configuration
├── .github/
│   ├── instructions/               # AI context instructions
│   ├── workflows/                  # Optional: CI/CD (Docker, version bumping)
│   └── scripts/                    # Automation scripts
├── ci_scripts/                     # Optional: Xcode Cloud scripts
│   └── ci_post_clone.sh
├── ProjectName/                    # iOS-specific code
│   ├── Info.plist
│   └── GitCommit.swift             # Optional: auto-generated commit hash
├── Shared/ (or "ProjectName Shared/")  # Cross-platform code
├── ProjectName.xcodeproj/
│   └── project.pbxproj             # Version and encryption flags
├── server/                         # Optional: server component
│   ├── Dockerfile
│   └── docker-compose.yml
└── CLAUDE.md                       # AI development guidance
```

## Quick Setup Checklist

1. **MCP Servers** - Configure XcodeBuildMCP and apple-developer-docs in `.vscode/mcp.json`
2. **Encryption Flag** - Set `INFOPLIST_KEY_ITSAppUsesNonExemptEncryption = NO` in project.pbxproj
3. **Code Organization** - Split files at 400 lines max, use `Class+Feature.swift` extensions
4. **Shared Folder** - Put cross-platform code in `Shared/` or `ProjectName Shared/`
5. **Version Embedding (optional)** - Create `GitCommit.swift` and `ci_scripts/ci_post_clone.sh`
6. **Server (optional)** - Docker setup with health checks and GitHub Actions workflows

## MCP Server Configuration

Create `.vscode/mcp.json`:

```json
{
  "servers": {
    "XcodeBuildMCP": {
      "command": "npx",
      "args": ["-y", "xcodebuildmcp@latest"],
      "tools": ["*"],
      "env": { "SENTRY_DISABLED": "true" }
    },
    "apple-developer-docs": {
      "command": "npx",
      "args": ["apple-developer-docs-mcp"],
      "tools": ["*"]
    }
  }
}
```

See [references/mcp-servers.md](references/mcp-servers.md) for Claude Code permissions setup.

## Info.plist and Encryption

Keep Info.plist minimal. Configure in build settings:

```
GENERATE_INFOPLIST_FILE = YES
INFOPLIST_KEY_ITSAppUsesNonExemptEncryption = NO
MARKETING_VERSION = 1.0
CURRENT_PROJECT_VERSION = 1
```

**Always set `ITSAppUsesNonExemptEncryption = NO`** unless using non-exempt encryption. This avoids the annual export compliance questionnaire.

See [references/info-plist.md](references/info-plist.md) for permission strings and background modes.

## Version and Commit Embedding (Optional)

Embed git commit hash into the app for debugging. Useful for correlating user-reported issues with specific builds.

### GitCommit.swift (placeholder)

```swift
import Foundation

struct GitCommit {
    static let hash: String = "n/a"
}
```

### ci_scripts/ci_post_clone.sh

```bash
#!/bin/sh
set -e
GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

if [ -n "$CI_WORKSPACE" ]; then
    OUTPUT_FILE="${CI_WORKSPACE}/ProjectName/GitCommit.swift"
else
    OUTPUT_FILE="$(dirname "$(pwd)")/ProjectName/GitCommit.swift"
fi

cat > "$OUTPUT_FILE" << EOF
import Foundation

struct GitCommit {
    static let hash: String = "$GIT_COMMIT"
}
EOF
```

Display in settings alongside version and build number.

See [references/version-embedding.md](references/version-embedding.md) for auto-bumping workflows.

## Code Organization

### File Naming

| Pattern | Use Case |
|---------|----------|
| `ClassName.swift` | Main class |
| `ClassName+Feature.swift` | Extension file |
| `ClassNameProtocol.swift` | Protocol definition |

### Size Guidelines

- **Target**: 200-300 lines
- **Maximum**: 400 lines
- Split large classes with extension files
- Put cross-platform code in `Shared/` folder

See [references/code-organization.md](references/code-organization.md) for detailed patterns.

## Server Components

For apps with server components, use Docker with health checks:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

ARG GIT_COMMIT=unknown
ENV GIT_COMMIT=${GIT_COMMIT}
```

GitHub Actions workflows:
- **docker-publish.yml** - Build and push on server changes
- **appstore-release.yml** - Tag Docker images with App Store version

See [references/server-docker.md](references/server-docker.md) for complete workflow examples.

## Simulator Instructions

**Always prefer XcodeBuildMCP tools over raw xcodebuild/xcrun commands.**

### XcodeBuildMCP Tools (Preferred)

```
mcp__xcodebuild__build_run_sim        # Build and run in one step
mcp__xcodebuild__build_sim            # Build only
mcp__xcodebuild__screenshot           # Take screenshot
mcp__xcodebuild__start_sim_log_cap    # Start log capture
mcp__xcodebuild__stop_sim_log_cap     # Stop and retrieve logs
mcp__xcodebuild__list_schemes         # List available schemes
mcp__xcodebuild__discover_projs       # Find Xcode projects
```

See [references/simulator.md](references/simulator.md) for fallback commands when MCP is unavailable.

## References

- [MCP Servers](references/mcp-servers.md) - Detailed MCP and permissions setup
- [Info.plist](references/info-plist.md) - Build settings and permissions
- [Version Embedding](references/version-embedding.md) - Commit hashing and auto-bumping
- [Server & Docker](references/server-docker.md) - Docker workflows and App Store sync
- [Code Organization](references/code-organization.md) - File splitting patterns
- [Simulator](references/simulator.md) - Build, run, and test commands
- [Custom Libraries](references/custom-libraries.md) - Future shared packages (TODO)
