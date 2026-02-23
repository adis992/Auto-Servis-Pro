#!/bin/bash
# iOS Build Script for Auto Servis Application
# Builds iOS application using Kivy-iOS (requires macOS)

set -e

echo "========================================"
echo "Building Auto Servis for iOS"
echo "========================================"

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "ERROR: iOS builds require macOS"
    echo "Current OS: $OSTYPE"
    exit 1
fi

# Check if Xcode is installed
if ! command -v xcodebuild &> /dev/null; then
    echo "ERROR: Xcode is not installed"
    echo "Install Xcode from the App Store"
    exit 1
fi

# Check Xcode version
XCODE_VERSION=$(xcodebuild -version | head -n 1 | awk '{print $2}')
echo "Xcode version: $XCODE_VERSION"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Install Python 3 using Homebrew: brew install python3"
    exit 1
fi

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "WARNING: Homebrew not found"
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install dependencies
echo "Installing dependencies..."
brew install autoconf automake libtool pkg-config || true
brew install openssl || true

# Install Kivy-iOS
if ! command -v toolchain &> /dev/null; then
    echo "Installing Kivy-iOS toolchain..."
    pip3 install kivy-ios
fi

# Create output directory
mkdir -p output
mkdir -p ios-build

cd ios-build

echo ""
echo "Building iOS dependencies..."
echo "This will take a long time on first run..."
echo ""

# Build required recipes
toolchain build python3 || true
toolchain build kivy || true
toolchain build flask || true
toolchain build pillow || true

# Create Xcode project
echo ""
echo "Creating Xcode project..."
echo ""

toolchain create AutoServis ../narudzbe

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Project creation failed"
    cd ..
    exit 1
fi

# Customize Info.plist
cat > AutoServis-ios/Info.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleDisplayName</key>
    <string>Auto Servis</string>
    <key>CFBundleExecutable</key>
    <string>AutoServis</string>
    <key>CFBundleIdentifier</key>
    <string>com.autoservis.app</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>AutoServis</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSRequiresIPhoneOS</key>
    <true/>
    <key>UIRequiredDeviceCapabilities</key>
    <array>
        <string>arm64</string>
    </array>
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
        <string>UIInterfaceOrientationLandscapeLeft</string>
        <string>UIInterfaceOrientationLandscapeRight</string>
    </array>
    <key>UIRequiresFullScreen</key>
    <false/>
</dict>
</plist>
EOF

echo ""
echo "Building Xcode project..."
echo ""

# Build for device
cd AutoServis-ios
xcodebuild -configuration Release -scheme AutoServis -destination generic/platform=iOS

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Xcode build failed"
    cd ../..
    exit 1
fi

# Create IPA (requires proper code signing)
echo ""
echo "Creating IPA archive..."
echo ""

xcodebuild archive \
    -scheme AutoServis \
    -archivePath ../AutoServis.xcarchive \
    -configuration Release

xcodebuild -exportArchive \
    -archivePath ../AutoServis.xcarchive \
    -exportPath ../output \
    -exportOptionsPlist exportOptions.plist || true

cd ../..

# Copy archive to output
if [ -f "ios-build/AutoServis.xcarchive" ]; then
    cp -r ios-build/AutoServis.xcarchive output/
fi

# Create README for distribution
cat > output/README-iOS.txt << EOF
Auto Servis - iOS Distribution
===============================

Requirements:
- macOS with Xcode installed
- Apple Developer account for code signing
- iOS device or simulator

Build Steps:
1. Open AutoServis.xcarchive in Xcode
2. Configure code signing with your Apple Developer account
3. Archive the app (Product > Archive)
4. Distribute to App Store or TestFlight

Installation (TestFlight):
1. Submit build to TestFlight
2. Add beta testers
3. Testers install via TestFlight app

Installation (Ad Hoc):
1. Export IPA with Ad Hoc provisioning profile
2. Install via Xcode or Apple Configurator

Features:
- Full appointment management
- Customer database
- PDF generation
- Native iOS interface

Support: auto-servis@example.com

Note: Code signing and provisioning must be configured in Xcode
EOF

echo ""
echo "========================================"
echo "Build completed!"
echo "========================================"
echo "Xcode project: ios-build/AutoServis-ios/"
echo "Archive: output/AutoServis.xcarchive"
echo ""
echo "Next steps:"
echo "1. Open the Xcode project"
echo "2. Configure code signing"
echo "3. Build and archive for distribution"
echo ""
