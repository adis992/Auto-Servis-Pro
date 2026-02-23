#!/bin/bash
# Android Build Script for Auto Servis Application
# Builds Android APK using Buildozer

set -e

echo "========================================"
echo "Building Auto Servis for Android"
echo "========================================"

# Check if running on Linux (required for Buildozer)
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "ERROR: Android builds require Linux"
    echo "Use WSL2 on Windows or a Linux VM"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

# Install Buildozer dependencies
echo "Checking Buildozer dependencies..."
DEPS_MISSING=0

for cmd in git zip unzip java; do
    if ! command -v $cmd &> /dev/null; then
        echo "Missing dependency: $cmd"
        DEPS_MISSING=1
    fi
done

if [ $DEPS_MISSING -eq 1 ]; then
    echo ""
    echo "Installing dependencies..."
    sudo apt-get update
    sudo apt-get install -y git zip unzip openjdk-11-jdk python3-pip \
        build-essential libssl-dev libffi-dev python3-dev \
        autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
        libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
fi

# Install Buildozer
if ! command -v buildozer &> /dev/null; then
    echo "Installing Buildozer..."
    pip3 install --user buildozer
    pip3 install --user cython
fi

# Install Android SDK/NDK (handled by Buildozer on first run)
echo "Buildozer will download Android SDK/NDK on first run"

# Create output directory
mkdir -p output

# Create or update buildozer.spec
if [ ! -f "buildozer.spec" ]; then
    echo "Creating buildozer.spec..."
    cat > buildozer.spec << 'EOF'
[app]

# Application title
title = Auto Servis

# Package name
package.name = autoservis

# Package domain
package.domain = com.autoservis

# Source code directory
source.dir = .

# Main entry point
source.include_exts = py,png,jpg,kv,atlas,db,ico

# Version
version = 1.0.0

# Application requirements
requirements = python3,kivy,flask,flask-cors,sqlite3,reportlab,pillow

# Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Orientation
orientation = portrait

# Android API level
android.api = 31
android.minapi = 21
android.ndk = 23b

# Architecture
android.archs = arm64-v8a,armeabi-v7a

# Full screen
fullscreen = 0

# Android icon
#icon.filename = icon.png

# Presplash
#presplash.filename = presplash.png

[buildozer]

# Log level
log_level = 2

# Build directory
build_dir = ./.buildozer

# Warn on root
warn_on_root = 1
EOF
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf .buildozer/android/platform/build

echo ""
echo "Building Android APK..."
echo "This may take a while on first run (downloading SDK/NDK)..."
echo ""

# Build APK
buildozer android debug

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Build failed"
    exit 1
fi

# Copy APK to output
echo ""
echo "Copying APK to output folder..."
find bin -name "*.apk" -exec cp {} output/AutoServis-Android.apk \;

# Create README for distribution
cat > output/README-Android.txt << EOF
Auto Servis - Android Distribution
===================================

Installation:
1. Enable "Install from Unknown Sources" in Android settings
2. Copy AutoServis-Android.apk to your device
3. Tap the APK file to install
4. Launch the Auto Servis app

Requirements:
- Android 5.0 (API 21) or later
- 50 MB free space
- Internet permission for web interface

Features:
- Full appointment management
- Customer database
- PDF generation
- Works offline after initial setup

Support: auto-servis@example.com

Note: This is a debug build. For production, use 'buildozer android release'
EOF

echo ""
echo "========================================"
echo "Build completed successfully!"
echo "========================================"
echo "APK: output/AutoServis-Android.apk"
echo ""
echo "To install on device:"
echo "  adb install output/AutoServis-Android.apk"
echo ""
