# Simulator Instructions

Using XcodeBuildMCP and command line tools for simulator development.

## Using XcodeBuildMCP

The XcodeBuildMCP provides Claude with simulator control:

### Build and Run
```
mcp__xcodebuild__build_run_sim        # Build and run on default sim
mcp__xcodebuild__build_run_sim_name_proj  # Specify simulator name and project
```

### Build Only
```
mcp__xcodebuild__build_sim            # Build for default sim
mcp__xcodebuild__build_sim_name_proj  # Specify simulator name
mcp__xcodebuild__build_sim_id_proj    # Specify simulator by ID
```

### Log Capture
```
mcp__xcodebuild__start_sim_log_cap    # Start capturing logs
mcp__xcodebuild__stop_sim_log_cap     # Stop and retrieve logs
mcp__xcodebuild__launch_app_logs_sim  # Launch with log streaming
```

### Screenshots
```
mcp__xcodebuild__screenshot           # Take simulator screenshot
```

### Discovery
```
mcp__xcodebuild__discover_projs       # Find Xcode projects
mcp__xcodebuild__list_schemes         # List available schemes
mcp__xcodebuild__show_build_set_proj  # Show build settings
```

## Command Line Build and Run

### List Simulators
```bash
xcrun simctl list devices available
```

### Build for Simulator
```bash
# Find the scheme name first
xcodebuild -list -project ProjectName.xcodeproj

# Build for iOS Simulator
xcodebuild -project ProjectName.xcodeproj \
  -scheme "ProjectName" \
  -destination "platform=iOS Simulator,name=iPhone 15 Pro" \
  -configuration Debug \
  build
```

### Install and Launch
```bash
# Boot simulator if needed
xcrun simctl boot "iPhone 15 Pro"

# Install the app
xcrun simctl install booted /path/to/App.app

# Launch the app
xcrun simctl launch booted com.example.appname
```

### Combined Build + Run
```bash
xcodebuild -project ProjectName.xcodeproj \
  -scheme "ProjectName" \
  -destination "platform=iOS Simulator,name=iPhone 15 Pro" \
  -configuration Debug \
  build

xcrun simctl install booted "$(xcodebuild -project ProjectName.xcodeproj -scheme ProjectName -showBuildSettings | grep -m 1 'BUILT_PRODUCTS_DIR' | awk '{print $3}')/ProjectName.app"

xcrun simctl launch booted com.joshspicer.ProjectName
```

## Multi-Simulator Setup

For multiplayer testing, launch two simulators:

```bash
# List available device types
xcrun simctl list devicetypes

# Create a second device if needed
xcrun simctl create "iPhone 15 Pro (2)" "iPhone 15 Pro"

# Boot both
xcrun simctl boot "iPhone 15 Pro"
xcrun simctl boot "iPhone 15 Pro (2)"

# Install on both
xcrun simctl install "iPhone 15 Pro" /path/to/App.app
xcrun simctl install "iPhone 15 Pro (2)" /path/to/App.app

# Launch on both
xcrun simctl launch "iPhone 15 Pro" com.example.appname
xcrun simctl launch "iPhone 15 Pro (2)" com.example.appname
```

## Simulator Log Capture

### Stream Logs
```bash
xcrun simctl spawn booted log stream --predicate 'subsystem == "com.example.appname"' --level debug
```

### View Recent Logs
```bash
xcrun simctl spawn booted log show --predicate 'subsystem == "com.example.appname"' --last 5m --style compact
```

## Screenshots

### Take Screenshot
```bash
xcrun simctl io booted screenshot ~/Desktop/screenshot.png
```

### Record Video
```bash
xcrun simctl io booted recordVideo ~/Desktop/recording.mov
# Press Ctrl+C to stop
```

## Troubleshooting

### Reset Simulator
```bash
xcrun simctl erase "iPhone 15 Pro"
```

### Kill All Simulators
```bash
xcrun simctl shutdown all
```

### Clean Build
```bash
xcodebuild clean -project ProjectName.xcodeproj -scheme "ProjectName"
```

### Check Simulator Status
```bash
xcrun simctl list devices booted
```

## watchOS Simulator

```bash
# Build for watchOS
xcodebuild -project ProjectName.xcodeproj \
  -scheme "ProjectNameWatch" \
  -destination "platform=watchOS Simulator,name=Apple Watch Series 9 (45mm)"

# Install watch app
xcrun simctl install "Apple Watch Series 9 (45mm)" /path/to/WatchApp.app
```

## tvOS Simulator

```bash
# Build for tvOS
xcodebuild -project ProjectName.xcodeproj \
  -scheme "ProjectName tvOS" \
  -destination "platform=tvOS Simulator,name=Apple TV 4K (3rd generation)"
```

## GitHub Instructions File

Create `.github/instructions/launch-two-simulators.instructions.md`:

```markdown
---
applyTo: '**'
---
When testing multiplayer functionality:
1. Use xcrun simctl to boot two iPhone simulators
2. Install the app on both
3. Launch the app on both
4. Test the multiplayer flow
```

## Common Destination Strings

```
platform=iOS Simulator,name=iPhone 15 Pro
platform=iOS Simulator,name=iPhone 15 Pro Max
platform=iOS Simulator,name=iPad Pro (12.9-inch) (6th generation)
platform=watchOS Simulator,name=Apple Watch Series 9 (45mm)
platform=tvOS Simulator,name=Apple TV 4K (3rd generation)
```
