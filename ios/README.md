# iOS Project Setup Skills

Standard patterns and configurations used when setting up iOS projects.

## Quick Reference

| Topic | File |
|-------|------|
| MCP Server Setup | [mcp-servers.md](mcp-servers.md) |
| Info.plist & Encryption | [info-plist.md](info-plist.md) |
| Version & Commit Embedding | [version-embedding.md](version-embedding.md) |
| Server Components & Docker | [server-docker.md](server-docker.md) |
| Code Organization | [code-organization.md](code-organization.md) |
| Simulator Instructions | [simulator.md](simulator.md) |
| Custom Libraries (TODO) | [custom-libraries.md](custom-libraries.md) |

## Example Projects

- **MapCalipers** (`~/git/MapCalipers`) - Primary reference, includes iOS + watchOS + Python server
- **Bunny Bunch** (`~/git/Bunny Bunch`) - SpriteKit game with iOS + tvOS, P2P multiplayer
- **hybrid-hr-bridge** (`~/git/hybrid-hr-bridge`) - BLE protocol app with Node.js service

## Project Structure Overview

```
ProjectName/
├── .vscode/
│   └── mcp.json                    # MCP server configuration
├── .claude/
│   └── settings.local.json         # Claude Code permissions
├── .github/
│   ├── instructions/               # AI context instructions
│   ├── workflows/                  # CI/CD (Docker, version bumping)
│   └── scripts/                    # Automation scripts
├── ci_scripts/
│   └── ci_post_clone.sh           # Xcode Cloud commit embedding
├── ProjectName/
│   ├── Info.plist                  # Minimal, checked into git
│   ├── GitCommit.swift             # Auto-generated commit hash
│   ├── Models/                     # Data models
│   ├── Views/                      # SwiftUI views
│   ├── Services/                   # Business logic managers
│   └── Extensions/                 # Class+Feature.swift files
├── ProjectName.xcodeproj/
│   └── project.pbxproj             # Version and encryption flags here
├── collab_server/                  # Optional server component
│   ├── Dockerfile
│   └── docker-compose.yml
├── CLAUDE.md                       # AI development guidance
└── AGENTS.md                       # Alternative agent guidance
```
