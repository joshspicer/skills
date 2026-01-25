# MCP Server Configuration for iOS Development

Two MCP servers are standard for iOS projects, configured in both VSCode and Claude Code.

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

### XcodeBuildMCP

Provides Claude with Xcode build capabilities:
- Build and run apps in simulator
- Start/stop simulator log capture
- Take simulator screenshots
- List schemes and build settings
- Discover Xcode projects

### apple-developer-docs

Provides access to Apple Developer Documentation:
- Search API docs (`mcp__appledocs__search_apple_docs`)
- Get doc content (`mcp__appledocs__get_apple_doc_content`)

## Claude Code Permissions

Create `.claude/settings.local.json` with granular permissions:

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

## VSCode Settings for Terminal Approval

Create `.vscode/settings.json` to auto-approve xcrun commands:

```json
{
  "chat.tools.terminal": {
    "autoApprove": ["xcrun"]
  }
}
```

## GitHub Instructions for AI Agents

Create `.github/instructions/apple-docs.instructions.md`:

```markdown
---
applyTo: '**/*.swift'
---
Use the apple-developer-docs MCP to look up modern Apple API patterns when uncertain.
```

## Install MCP Servers Globally

For Claude Code desktop app, install the MCP servers:

```bash
# These are installed via npx automatically when configured in mcp.json
# No manual installation needed - npx pulls latest on each use
```

## Usage Notes

- SENTRY_DISABLED=true prevents xcodebuildmcp from sending telemetry
- Use `npx -y` to auto-confirm installation without prompts
- Both servers work with tools: ["*"] to enable all capabilities
- WebFetch permissions should include relevant domains (github.com, your domain)
