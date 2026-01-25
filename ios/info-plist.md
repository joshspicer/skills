# Info.plist and Build Settings

## Philosophy

Keep Info.plist minimal and checked into git. Configure most settings via Xcode build settings in `project.pbxproj`, which auto-generates the Info.plist at build time.

## Minimal Info.plist

For most apps, the Info.plist can be nearly empty:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.org/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict/>
</plist>
```

## Build Settings for Info.plist Keys

In `project.pbxproj`, set these in the build configuration:

```
GENERATE_INFOPLIST_FILE = YES
INFOPLIST_FILE = ProjectName/Info.plist

// App Store encryption compliance - ALWAYS SET THIS
INFOPLIST_KEY_ITSAppUsesNonExemptEncryption = NO

// Version info (managed in pbxproj, not Info.plist)
MARKETING_VERSION = 1.5
CURRENT_PROJECT_VERSION = 1

// App metadata
INFOPLIST_KEY_CFBundleDisplayName = "App Name"
INFOPLIST_KEY_UISupportedInterfaceOrientations = "UIInterfaceOrientationPortrait"
INFOPLIST_KEY_UILaunchScreen_Generation = YES
```

## ITSAppUsesNonExemptEncryption Flag

**Always set to NO** unless your app uses encryption for purposes beyond:
- Standard HTTPS/TLS
- Apple's built-in encryption APIs for standard use

```
INFOPLIST_KEY_ITSAppUsesNonExemptEncryption = NO
```

This avoids the annual export compliance questionnaire on App Store Connect.

If your app DOES use non-exempt encryption:
- Set to YES
- Prepare export compliance documentation

## Permission Descriptions

Add permission strings directly in build settings:

```
// Location
INFOPLIST_KEY_NSLocationWhenInUseUsageDescription = "App needs your location to..."
INFOPLIST_KEY_NSLocationTemporaryUsageDescriptionDictionary = "MapUsage"

// Bluetooth
INFOPLIST_KEY_NSBluetoothAlwaysUsageDescription = "App needs Bluetooth to..."
INFOPLIST_KEY_NSBluetoothPeripheralUsageDescription = "App needs Bluetooth peripheral access to..."

// Local Network
INFOPLIST_KEY_NSLocalNetworkUsageDescription = "App needs local network for multiplayer..."
```

## Background Modes

Set in build settings:

```
UIBackgroundModes[sdk=iphoneos*] = "bluetooth-central"
// Or for multiple modes:
UIBackgroundModes = "audio bluetooth-central location"
```

## When to Use Info.plist Directly

Some settings must be in Info.plist file:
- Bonjour service types
- URL schemes
- Custom iOS/watchOS specific configurations
- App Transport Security exceptions

Example Info.plist with Bonjour services:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.org/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSBonjourServices</key>
    <array>
        <string>_my-service._tcp</string>
        <string>_my-service._udp</string>
    </array>
</dict>
</plist>
```

## Checking Settings

View effective Info.plist after build:
```bash
# Find the built .app
xcodebuild -showBuildSettings | grep BUILT_PRODUCTS_DIR
# Then examine Info.plist in the .app bundle
```
