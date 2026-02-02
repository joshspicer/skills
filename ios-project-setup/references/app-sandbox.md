# App Sandbox Configuration

In cases where you need to disable the sandbox on macOS (e.g., spawning external CLIs like `copilot`, accessing arbitrary file paths), use xcconfig files to swap between sandboxed and non-sandboxed builds.

**Only add this when you determine you need it** - most apps work fine with the default sandbox. It's nice to keep the sandbox enabled for security and, most importantly, App Store distribution.

## Configuration Files

When needed, create two xcconfig files at the project root:

**sandbox.xcconfig** (for App Store distribution):
```
ENABLE_APP_SANDBOX = YES
SWIFT_ACTIVE_COMPILATION_CONDITIONS = $(inherited) SANDBOX
```

**nosandbox.xcconfig** (for development with external CLIs like Copilot):
```
ENABLE_APP_SANDBOX = NO
// SANDBOX flag NOT set - use #if !SANDBOX in code
```

## Xcode Setup

In Xcode: Project → Info → Configurations → set the xcconfig for each build configuration:
- Debug → `nosandbox.xcconfig`
- Release → `sandbox.xcconfig` (or `nosandbox.xcconfig` if not targeting App Store)

## Checking Sandbox in Code

The xcconfig sets a `SANDBOX` compilation condition. Use it to conditionally enable features:

```swift
#if SANDBOX
    // Running sandboxed (App Store build)
    // External CLI features disabled
#else
    // Running without sandbox
    // Can spawn external processes like `copilot` CLI
#endif
```

## When to Disable Sandbox

- Spawning external CLI processes (like `copilot` CLI)
- Accessing arbitrary file system paths
- Inter-process communication

**Note:** Apps without sandbox cannot be distributed on the Mac App Store.
