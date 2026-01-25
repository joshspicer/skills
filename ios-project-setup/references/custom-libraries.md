# Custom Libraries

Shared Swift libraries and patterns for iOS projects.

## App Catalog

- [MapCalipers](https://joshspicer.com/mapcalipers)
- [HabitBridge](https://joshspicer.com/HabitBridge)
- [Tank Game](https://joshspicer.com/tankgame)
- [Bunny Bunch](https://joshspicer.com/bunnybunch)

## Shared Folder Pattern

Always put shareable Swift code in a `Shared/` folder. This makes it easy to release macOS, tvOS, or watchOS versions later.

```
ProjectName/
├── ProjectName/           # iOS-specific code
├── ProjectName macOS/     # macOS-specific code (if needed)
├── ProjectName tvOS/      # tvOS-specific code (if needed)
└── Shared/                # Cross-platform code
    ├── Models/
    ├── Services/
    ├── Extensions/
    └── Utilities/
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

Real-time or turn-based local multiplayer via Bonjour/Bluetooth. Use for any peer-to-peer multiplayer functionality.

**Used in:**
- [Tank Game](https://joshspicer.com/tankgame)
- [Bunny Bunch](https://joshspicer.com/bunnybunch)

**Capabilities:**
- Bonjour service discovery
- Bluetooth peer connections
- Turn-based and real-time game state sync
- Host/client architecture

## inner-loop-swift (TODO)

**GitHub:** https://github.com/joshspicer/inner-loop-swift

Logging and error tracking library. **Not yet production ready.**

**Planned capabilities:**
- Structured logging with levels
- Remote log aggregation
- Shake-to-report for TestFlight feedback
- Error tracking and batching
