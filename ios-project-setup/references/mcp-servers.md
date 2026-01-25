# MCP Server Configuration

## VSCode Configuration

Create `.vscode/mcp.json`:

```json
{
  "servers": {
    "XcodeBuildMCP": {
      "command": "npx",
      "args": ["-y", "xcodebuildmcp@latest"],
      "tools": ["*"],
      "env": {
        "SENTRY_DISABLED": "true"
      }
    },
    "apple-developer-docs": {
      "command": "npx",
      "args": ["apple-developer-docs-mcp"],
      "tools": ["*"]
    }
  }
}
```

### XcodeBuildMCP Tools

- Build and run apps in simulator
- Start/stop simulator log capture
- Take simulator screenshots
- List schemes and build settings
- Discover Xcode projects

### apple-developer-docs Tools

- `mcp__appledocs__search_apple_docs` - Search API docs
- `mcp__appledocs__get_apple_doc_content` - Get doc content

## Claude Code Permissions

Create `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(xcodebuild:*)",
      "Bash(grep:*)",
      "Bash(swift:*)",
      "Bash(find:*)",
      "Bash(rg:*)",
      "Bash(python3:*)",
      "Bash(git add:*)",
      "Bash(git stash:*)",
      "Bash(git checkout:*)",
      "Bash(curl:*)",
      "Bash(docker-compose up:*)",
      "Bash(timeout 60 xcodebuild:*)",
      "mcp__xcodebuild__build_run_sim_name_proj",
      "mcp__xcodebuild__build_sim_name_proj",
      "mcp__xcodebuild__build_sim_id_proj",
      "mcp__xcodebuild__build_run_sim",
      "mcp__xcodebuild__build_sim",
      "mcp__xcodebuild__start_sim_log_cap",
      "mcp__xcodebuild__stop_sim_log_cap",
      "mcp__xcodebuild__launch_app_logs_sim",
      "mcp__xcodebuild__screenshot",
      "mcp__xcodebuild__discover_projs",
      "mcp__xcodebuild__list_schemes",
      "mcp__xcodebuild__show_build_set_proj",
      "mcp__xcodebuild__session-set-defaults",
      "mcp__xcodebuild__get_mac_app_path_proj",
      "mcp__xcodebuild__build_mac_proj",
      "mcp__appledocs__search_apple_docs",
      "mcp__appledocs__get_apple_doc_content",
      "WebFetch(domain:github.com)"
    ],
    "deny": []
  }
}
```

## VSCode Terminal Settings

Create `.vscode/settings.json`:

```json
{
  "chat.tools.terminal": {
    "autoApprove": ["xcrun"]
  }
}
```

## GitHub Instructions

Create `.github/instructions/apple-docs.instructions.md`:

```markdown
---
applyTo: '**/*.swift'
---
Use the apple-developer-docs MCP to look up modern Apple API patterns when uncertain.
```

## Notes

- `SENTRY_DISABLED=true` prevents xcodebuildmcp telemetry
- `npx -y` auto-confirms installation
- Add relevant domains to WebFetch permissions
