# Custom Libraries

Shared Swift libraries and patterns for iOS projects.

**Important:** This skills document is the definitive source of truth for custom library patterns. Keep this updated when making changes to library integration strategies.


## Local Development vs CI/Distribution

Use the **workspace strategy** to enable local package development while maintaining CI compatibility:

### Strategy Overview

| Scenario | Open | Package Source |
|----------|------|----------------|
| **Local development** | `Project.xcworkspace` | Local package (editable) |
| **CI / App Store** | `Project.xcodeproj` | Remote GitHub URL |

### Setup Steps

1. **Reference remote URL in project** (for CI):
   ```
   # In project.pbxproj, use XCRemoteSwiftPackageReference:
   repositoryURL = "https://github.com/joshspicer/MultiPlayKit.git";
   requirement = { kind = upToNextMajorVersion; minimumVersion = 1.0.0; };
   ```

2. **Create workspace with local package** (for development):
   ```xml
   <!-- Project.xcworkspace/contents.xcworkspacedata -->
   <?xml version="1.0" encoding="UTF-8"?>
   <Workspace version="1.0">
      <FileRef location="container:Project.xcodeproj"/>
      <FileRef location="group:../MultiPlayKit"/>
   </Workspace>
   ```

3. **Commit both** - The workspace enables local dev, project enables CI

### How It Works

- Xcode prefers local packages over remote when both are available
- Opening the workspace: Xcode sees local `../MultiPlayKit` and uses it
- Opening the project (CI): Xcode fetches from GitHub URL
- Changes to local package are immediately reflected when rebuilding

### LLM Tool Usage

When running apps locally via Claude Code or other LLM tools:

```bash
# CORRECT: Use workspace for local development
xcodebuild -workspace Project.xcworkspace -scheme "Project iOS" ...

# For XcodeBuildMCP: specify workspace path
mcp__xcodebuild__build_run_sim with workspace: "Project.xcworkspace"
```

**Never use `.xcodeproj` directly when developing locally** - it will fetch the remote package and miss local changes.

## Shared Folder Pattern

Put shareable Swift code in a shared folder for easy multi-platform support (macOS, tvOS, watchOS).

**Naming:** Either `Shared/` or `ProjectName Shared/` (Xcode default when adding targets).

```
ProjectName/
├── ProjectName/              # iOS-specific code
├── ProjectName Shared/       # Cross-platform code (Xcode default naming)
├── ProjectName macOS/        # macOS-specific (if needed)
└── ProjectName tvOS/         # tvOS-specific (if needed)
```

Or with simple `Shared/` folder:
```
ProjectName/
├── ProjectName/
├── Shared/
└── ...
```

**Setup:**
- Create the `Shared/` folder and add files to it
- In Xcode, set target membership for shared files to include all platforms
- Platform-specific code stays in platform folders
- Schemes for each platform are automatically set up by Xcode

**What goes in Shared:**
- Data models (Codable structs)
- Business logic and services
- Networking code
- Extensions on Foundation/Swift types
- Utilities and helpers

**What stays platform-specific:**
- Views (SwiftUI views may differ per platform)
- Platform-specific APIs (HealthKit, WatchKit, etc.)
- App entry points and delegates

## MultiPlayKit

**GitHub:** https://github.com/joshspicer/MultiPlayKit

Peer-to-peer local multiplayer library for iOS/tvOS/macOS. Supports both real-time action games and turn-based games with automatic peer discovery, authority election, and state synchronization.

**Used in:**
- [Tank Game](https://joshspicer.com/tankgame) - Real-time multiplayer
- [Bunny Bunch](https://joshspicer.com/bunnybunch) - Turn-based multiplayer

### Key Architecture

**Elder Pattern** (not host/client):
- Peer with lowest UUID automatically becomes "elder" (authority)
- Elder broadcasts periodic full state for eventual consistency
- On elder disconnect, next-lowest UUID becomes elder
- No explicit host selection needed

**Peer Discovery:**
- All peers simultaneously advertise AND browse
- Deterministic invitation: lower UUID invites higher UUID (prevents duplicates)
- Auto-accept invitations by default

**State Synchronization:**
- Full sync: On new peer join + periodic broadcasts from elder
- Incremental sync: Individual actions broadcast as they happen

### Core Types

| Type | Purpose |
|------|---------|
| `PeerSession` | Main entry point, wraps MCSession |
| `PeerIdentity` | Persistent UUID-based peer identity |
| `PeerMessage` | Protocol for custom game messages |
| `SyncableState` | Protocol for syncable game state |
| `TurnCoordinator` | Distributed turn management |
| `RealtimeSyncManager` | Periodic sync for action games |

### Quick Usage

```swift
import MultiPlayKit

// Create session
let config = SessionConfiguration(serviceType: "mygame")
let session = PeerSession(configuration: config)
session.delegate = self

// Start peer discovery
session.start()

// Send messages
session.broadcast(MyGameMessage(...))

// Check authority status
if session.isElder {
    session.broadcastState(gameState)
}
```

### Custom Messages

```swift
enum GameMessage: Codable, PeerMessage, @unchecked Sendable {
    static var messageType: String { "GameMessage" }

    case move(playerId: String, x: Int, y: Int)
    case action(playerId: String, actionType: String)
    case sync(state: GameState)
}
```

## inner-loop-swift (TODO)

**GitHub:** https://github.com/joshspicer/inner-loop-swift

Logging and error tracking library. **Not yet production ready.**

**Planned capabilities:**
- Structured logging with levels
- Remote log aggregation
- Shake-to-report for TestFlight feedback
- Error tracking and batching
