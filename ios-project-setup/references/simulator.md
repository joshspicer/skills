# Simulator Instructions

**Always prefer XcodeBuildMCP tools over raw xcodebuild/xcrun commands.** The MCP tools handle build paths, simulator selection, and app installation automatically.

## XcodeBuildMCP Tools (Preferred)

```
mcp__xcodebuild__build_run_sim            # Build and run on default simulator
mcp__xcodebuild__build_run_sim_name_proj  # Specify simulator name and project
mcp__xcodebuild__build_sim                # Build only
mcp__xcodebuild__build_sim_name_proj      # Build for specific simulator
mcp__xcodebuild__screenshot               # Take simulator screenshot
mcp__xcodebuild__start_sim_log_cap        # Start capturing logs
mcp__xcodebuild__stop_sim_log_cap         # Stop capture and retrieve logs
mcp__xcodebuild__launch_app_logs_sim      # Launch app with log streaming
mcp__xcodebuild__discover_projs           # Find Xcode projects in directory
mcp__xcodebuild__list_schemes             # List available build schemes
mcp__xcodebuild__show_build_set_proj      # Show build settings
```

## Fallback: Command Line

Only use these when MCP tools are unavailable.

### List Simulators
```bash
xcrun simctl list devices available
```

### Build
```bash
xcodebuild -list -project ProjectName.xcodeproj

xcodebuild -project ProjectName.xcodeproj \
  -scheme "ProjectName" \
  -destination "platform=iOS Simulator,name=iPhone 15 Pro" \
  -configuration Debug \
  build
```

### Install and Launch
```bash
xcrun simctl boot "iPhone 15 Pro"
xcrun simctl install booted /path/to/App.app
xcrun simctl launch booted com.example.appname
```

## Multi-Simulator Testing

For multiplayer testing with two simulators:

```bash
# Create second device if needed
xcrun simctl create "iPhone 15 Pro (2)" "iPhone 15 Pro"

# Boot both
xcrun simctl boot "iPhone 15 Pro"
xcrun simctl boot "iPhone 15 Pro (2)"

# Install on both
xcrun simctl install "iPhone 15 Pro" /path/to/App.app
xcrun simctl install "iPhone 15 Pro (2)" /path/to/App.app

# Launch both
xcrun simctl launch "iPhone 15 Pro" com.example.appname
xcrun simctl launch "iPhone 15 Pro (2)" com.example.appname
```

## Log Capture (Fallback)

```bash
# Stream logs
xcrun simctl spawn booted log stream \
  --predicate 'subsystem == "com.example.appname"' \
  --level debug

# Recent logs
xcrun simctl spawn booted log show \
  --predicate 'subsystem == "com.example.appname"' \
  --last 5m --style compact
```

## Screenshots and Recording (Fallback)

```bash
xcrun simctl io booted screenshot ~/Desktop/screenshot.png
xcrun simctl io booted recordVideo ~/Desktop/recording.mov  # Ctrl+C to stop
```

## Troubleshooting

```bash
xcrun simctl erase "iPhone 15 Pro"      # Reset simulator
xcrun simctl shutdown all                # Kill all simulators
xcrun simctl list devices booted         # Check running simulators
xcodebuild clean -project ProjectName.xcodeproj -scheme "ProjectName"
```

## Platform Destinations

```
platform=iOS Simulator,name=iPhone 15 Pro
platform=iOS Simulator,name=iPhone 15 Pro Max
platform=iOS Simulator,name=iPad Pro (12.9-inch) (6th generation)
platform=watchOS Simulator,name=Apple Watch Series 9 (45mm)
platform=tvOS Simulator,name=Apple TV 4K (3rd generation)
```
