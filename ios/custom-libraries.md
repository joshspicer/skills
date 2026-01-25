# Custom Libraries (TODO)

This document outlines the plan for creating shared Swift libraries across iOS projects.

## Future Goal

Create reusable Swift packages for common functionality:

- **Logging/Error Tracking** - InnerLoop-style log aggregation
- **Networking** - Common API client patterns
- **Persistence** - UserDefaults wrappers, file management
- **UI Components** - Shared SwiftUI views and modifiers
- **Utilities** - Extensions, helpers

## Current State

Each project currently has its own implementations of common patterns:

| Functionality | MapCalipers | Bunny Bunch | hybrid-hr-bridge |
|---------------|-------------|-------------|------------------|
| Logging | Custom LogManager | Console | InnerLoop integration |
| Settings | Settings singleton | In-scene state | @AppStorage |
| Networking | SessionSync | P2P Bluetooth | REST + BLE |

## Proposed Package Structure

```
SwiftPackages/
├── JoshCore/
│   ├── Package.swift
│   └── Sources/
│       ├── Logging/
│       │   ├── LogLevel.swift
│       │   ├── LogDestination.swift
│       │   └── Logger.swift
│       ├── Storage/
│       │   ├── PersistentStore.swift
│       │   └── SecureStorage.swift
│       └── Extensions/
│           └── Foundation+Extensions.swift
├── JoshUI/
│   ├── Package.swift
│   └── Sources/
│       ├── Components/
│       └── Modifiers/
└── JoshNetworking/
    └── Package.swift
```

## Integration Plan

1. Create packages as local Swift packages first
2. Gradually extract common code from existing projects
3. Eventually publish to a private repository
4. Use Swift Package Manager for integration

## Adding Local Package to Xcode Project

```
Project/
├── ProjectName.xcodeproj
├── ProjectName/
└── Packages/              # Local packages here
    └── JoshCore/
        ├── Package.swift
        └── Sources/
```

In Xcode: File > Add Package Dependencies > Add Local > select the package folder

## Example Package.swift

```swift
// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "JoshCore",
    platforms: [
        .iOS(.v17),
        .watchOS(.v10),
        .tvOS(.v17)
    ],
    products: [
        .library(name: "JoshCore", targets: ["JoshCore"])
    ],
    targets: [
        .target(name: "JoshCore", dependencies: []),
        .testTarget(name: "JoshCoreTests", dependencies: ["JoshCore"])
    ]
)
```

## Notes

- Keep packages minimal and focused
- Avoid dependencies where possible
- Document public APIs clearly
- Include unit tests
- Support all target platforms (iOS, watchOS, tvOS, macOS)
