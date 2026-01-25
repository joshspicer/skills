# Code Organization Patterns

## Core Principles

1. **One class/struct/enum per file** (with exceptions for closely related types)
2. **Maximum 400 lines per file** (target 200-300)
3. **Use extensions to split large classes**
4. **Subdirectories** for related components

## File Naming

| Pattern | Use Case | Example |
|---------|----------|---------|
| `ClassName.swift` | Main class | `BluetoothManager.swift` |
| `ClassName+Feature.swift` | Extension | `GameScene+Touches.swift` |
| `ClassNameProtocol.swift` | Protocol | `MapToolProtocol.swift` |
| `ClassName+Codable.swift` | Conformance | `CLLocationCoordinate2D+Codable.swift` |

## Directory Structure

Organize by feature or layer - whatever makes sense for the project. Use subdirectories to group related files.

Example subdirectory for a complex view:
```
Views/
└── DeviceDetail/
    ├── DeviceDetailView.swift
    ├── BatteryStatusView.swift
    └── DeviceActionsView.swift
```

## Extension Files Pattern

When a class grows large, split with extensions:

### Main: `GameScene.swift`
```swift
import SpriteKit

class GameScene: SKScene {
    var players: [Player] = []
    var gameState: GameState = .waiting

    override func didMove(to view: SKView) {
        setupScene()
    }
}
```

### Extension: `GameScene+Touches.swift`
```swift
import SpriteKit

extension GameScene {
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        // Touch handling
    }
}
```

### Extension: `GameScene+Multiplayer.swift`
```swift
extension GameScene {
    func handlePeerMessage(_ data: Data) {
        // Network handling
    }
}
```

## View Splitting

### Before (500-line monolith):
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
        }
    }
}
```

**DeviceDetail/BatteryStatusView.swift** (~100 lines):
```swift
struct BatteryStatusView: View {
    let device: Device
    var body: some View { /* Battery UI */ }
}
```

## Size Guidelines

| File Type | Target | Max |
|-----------|--------|-----|
| Views | 100-200 | 300 |
| Models | 50-100 | 200 |
| Managers | 200-300 | 400 |
| Extensions | 50-150 | 200 |

## Multi-Platform Shared Code

Put cross-platform code in a `Shared/` folder. Use target membership in Xcode to include files in multiple targets (iOS, macOS, tvOS, watchOS).

See [custom-libraries.md](custom-libraries.md) for details on the Shared folder pattern.
