# Info.plist and Build Settings

## Philosophy

Keep Info.plist minimal. Configure most settings via Xcode build settings in `project.pbxproj`.

## Minimal Info.plist

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.org/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict/>
</plist>
```

## Build Settings

In `project.pbxproj`:

```
GENERATE_INFOPLIST_FILE = YES
INFOPLIST_FILE = ProjectName/Info.plist

// App Store encryption compliance
INFOPLIST_KEY_ITSAppUsesNonExemptEncryption = NO

// Version info
MARKETING_VERSION = 1.5
CURRENT_PROJECT_VERSION = 1

// App metadata
INFOPLIST_KEY_CFBundleDisplayName = "App Name"
INFOPLIST_KEY_UISupportedInterfaceOrientations = "UIInterfaceOrientationPortrait"
INFOPLIST_KEY_UILaunchScreen_Generation = YES
```

## ITSAppUsesNonExemptEncryption

**Always set to NO** unless using encryption beyond:
- Standard HTTPS/TLS
- Apple's built-in encryption APIs

Setting to NO avoids annual export compliance questionnaire.

## Permission Descriptions

```
// Location
INFOPLIST_KEY_NSLocationWhenInUseUsageDescription = "App needs your location to..."

// Bluetooth
INFOPLIST_KEY_NSBluetoothAlwaysUsageDescription = "App needs Bluetooth to..."
INFOPLIST_KEY_NSBluetoothPeripheralUsageDescription = "App needs Bluetooth peripheral access to..."

// Local Network
INFOPLIST_KEY_NSLocalNetworkUsageDescription = "App needs local network for multiplayer..."
```

## Background Modes

```
UIBackgroundModes[sdk=iphoneos*] = "bluetooth-central"
// Or multiple:
UIBackgroundModes = "audio bluetooth-central location"
```

## When to Use Info.plist Directly

Some settings must be in the plist file:
- Bonjour service types
- URL schemes
- App Transport Security exceptions

Example with Bonjour:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.org/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSBonjourServices</key>
    <array>
        <string>_my-service._tcp</string>
    </array>
</dict>
</plist>
```
