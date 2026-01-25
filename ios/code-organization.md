# Code Organization Patterns

Split code into as many small files as possible for easy AI editing and maintainability.

## Core Principles

1. **One class/struct/enum per file** (with exceptions for closely related types)
2. **Maximum 400 lines per file** (target 200-300)
3. **Use extensions to split large classes**
4. **Feature subdirectories** for related components

## File Naming Conventions

| Pattern | Use Case | Example |
|---------|----------|---------|
| `ClassName.swift` | Main class definition | `BluetoothManager.swift` |
| `ClassName+Feature.swift` | Extension file | `GameScene+Touches.swift` |
| `ClassNameProtocol.swift` | Protocol definition | `MapToolProtocol.swift` |
| `ClassName+Codable.swift` | Conformance extension | `CLLocationCoordinate2D+Codable.swift` |

## Directory Structure

```
ProjectName/
├── Models/                      # Data structures
│   ├── User.swift
│   ├── Game.swift
│   └── Settings.swift
├── Views/                       # SwiftUI views
│   ├── ContentView.swift
│   ├── SettingsView.swift
│   └── DeviceDetail/           # Sub-view components
│       ├── ActivitySummaryView.swift
│       ├── BatteryStatusView.swift
│       └── DeviceActionsView.swift
├── Services/                    # Business logic
│   ├── WatchManager.swift
│   └── ActivityDataManager.swift
├── Managers/                    # State and coordination
│   ├── TimelineManager.swift
│   ├── OverlayManager.swift
│   └── PersistentOverlayManager.swift
├── Protocol/                    # Protocol layer (for BLE/network apps)
│   ├── AuthenticationManager.swift
│   ├── FileTransferManager.swift
│   └── FileTransfer/           # Sub-feature
│       ├── EncryptedFileReader.swift
│       └── EncryptedReadState.swift
├── Tools/                       # Tool implementations
│   ├── RadarTool.swift
│   ├── RadarToolUIOverlay.swift
│   ├── DistanceTool.swift
│   └── MapToolProtocol.swift
├── Extensions/                  # Type extensions
│   ├── CLLocationCoordinate2D+Codable.swift
│   └── MKPolygon+Coordinates.swift
├── Utilities/                   # Helper functions
│   ├── LogManager.swift
│   ├── AESCrypto.swift
│   └── ByteBuffer.swift
└── Root/
    ├── AppDelegate.swift       # (if not using SwiftUI lifecycle)
    └── ProjectNameApp.swift    # Entry point
```

## Extension Files Pattern

When a class grows large, split it with extension files:

### Main file: `GameScene.swift`
```swift
import SpriteKit

class GameScene: SKScene {
    // Core properties
    var players: [Player] = []
    var gameState: GameState = .waiting

    // Core initialization
    override func didMove(to view: SKView) {
        setupScene()
    }

    // Primary logic only
}
```

### Extension: `GameScene+Touches.swift`
```swift
import SpriteKit

extension GameScene {
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        // Touch handling logic
    }

    override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent?) {
        // Touch move logic
    }
}
```

### Extension: `GameScene+Multiplayer.swift`
```swift
extension GameScene {
    func handlePeerMessage(_ data: Data) {
        // Network message handling
    }

    func sendGameState() {
        // State sync
    }
}
```

## Protocol-Based Design

Define protocols for tool/component interfaces:

```swift
// MapToolProtocol.swift
protocol MapToolProtocol {
    var region: MKCoordinateRegion? { get set }
    var mapView: MKMapView? { get set }

    func activate()
    func deactivate()
    func handleTap(at coordinate: CLLocationCoordinate2D)

    var stateDescription: String { get }
}
```

Each tool implements the protocol in its own file:
- `RadarTool.swift`
- `DistanceTool.swift`
- `InspectTool.swift`

## View Splitting Guidelines

Large views should be split into sub-components:

### Before (one 500-line file):
```swift
struct DeviceDetailView: View {
    var body: some View {
        ScrollView {
            // 500 lines of mixed concerns
        }
    }
}
```

### After (multiple focused files):

**DeviceDetailView.swift** (~100 lines):
```swift
struct DeviceDetailView: View {
    let device: Device

    var body: some View {
        ScrollView {
            BatteryStatusView(device: device)
            ActivitySummaryView(device: device)
            DeviceActionsView(device: device)
            LogExportView(device: device)
        }
    }
}
```

**DeviceDetail/BatteryStatusView.swift** (~100 lines):
```swift
struct BatteryStatusView: View {
    let device: Device

    var body: some View {
        // Battery-specific UI
    }
}
```

## Model Files

One model per file with Codable conformance:

```swift
// Models/ActivityEntry.swift
import Foundation

struct ActivityEntry: Codable, Identifiable {
    let id: UUID
    let timestamp: Date
    let steps: Int
    let heartRate: Int?
}
```

## Manager Pattern

Managers coordinate state and business logic:

```swift
// Services/TimelineManager.swift
import Foundation
import Combine

@MainActor
class TimelineManager: ObservableObject {
    @Published var steps: [GameStep] = []
    @Published var currentIndex: Int = 0

    func addStep(_ step: GameStep) { ... }
    func undo() { ... }
    func redo() { ... }
}
```

## File Size Guidelines

| File Type | Target Lines | Max Lines |
|-----------|--------------|-----------|
| Views | 100-200 | 300 |
| Models | 50-100 | 200 |
| Managers | 200-300 | 400 |
| Extensions | 50-150 | 200 |
| Utilities | 50-100 | 200 |

## Shared Code

For multi-platform projects (iOS + watchOS + tvOS):

```
Shared/
├── Models/          # Shared data models
├── Extensions/      # Shared type extensions
└── Settings.swift   # Shared configuration
```

Use target membership in Xcode to include files in multiple targets, or use a Shared folder with universal code.
