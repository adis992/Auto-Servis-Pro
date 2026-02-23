#!/bin/bash
# Master Build Script for Auto Servis Application
# Builds for all platforms and organizes output

set -e

echo "========================================"
echo "Auto Servis - Master Build Script"
echo "========================================"
echo ""

# Detect platform
PLATFORM=$(uname -s)
echo "Detected platform: $PLATFORM"
echo ""

# Create output directory with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="output/build_${TIMESTAMP}"
mkdir -p "$OUTPUT_DIR"

# Track build results
BUILD_LOG="$OUTPUT_DIR/build.log"
touch "$BUILD_LOG"

echo "Build started at: $(date)" | tee -a "$BUILD_LOG"
echo "Output directory: $OUTPUT_DIR" | tee -a "$BUILD_LOG"
echo "" | tee -a "$BUILD_LOG"

# Function to run build and log results
run_build() {
    local name=$1
    local script=$2
    local platform=$3
    
    echo "========================================" | tee -a "$BUILD_LOG"
    echo "Building for $name..." | tee -a "$BUILD_LOG"
    echo "========================================" | tee -a "$BUILD_LOG"
    echo "" | tee -a "$BUILD_LOG"
    
    if [ -f "$script" ]; then
        if bash "$script" 2>&1 | tee -a "$BUILD_LOG"; then
            echo "✓ $name build SUCCESS" | tee -a "$BUILD_LOG"
            return 0
        else
            echo "✗ $name build FAILED" | tee -a "$BUILD_LOG"
            return 1
        fi
    else
        echo "✗ $name build SKIPPED (script not found: $script)" | tee -a "$BUILD_LOG"
        return 1
    fi
    echo "" | tee -a "$BUILD_LOG"
}

# Build counters
BUILDS_SUCCESS=0
BUILDS_FAILED=0
BUILDS_SKIPPED=0

# Windows build (only on Windows/WSL)
if [ -f "build_windows.bat" ]; then
    if [[ "$PLATFORM" == "MINGW"* ]] || [[ "$PLATFORM" == "MSYS"* ]]; then
        echo "Running Windows build..." | tee -a "$BUILD_LOG"
        if cmd.exe /c build_windows.bat 2>&1 | tee -a "$BUILD_LOG"; then
            echo "✓ Windows build SUCCESS" | tee -a "$BUILD_LOG"
            BUILDS_SUCCESS=$((BUILDS_SUCCESS + 1))
        else
            echo "✗ Windows build FAILED" | tee -a "$BUILD_LOG"
            BUILDS_FAILED=$((BUILDS_FAILED + 1))
        fi
    else
        echo "✗ Windows build SKIPPED (not on Windows)" | tee -a "$BUILD_LOG"
        BUILDS_SKIPPED=$((BUILDS_SKIPPED + 1))
    fi
    echo "" | tee -a "$BUILD_LOG"
fi

# Linux build
if run_build "Linux" "build_linux.sh" "Linux"; then
    BUILDS_SUCCESS=$((BUILDS_SUCCESS + 1))
else
    BUILDS_FAILED=$((BUILDS_FAILED + 1))
fi

# Android build (Linux only)
if [[ "$PLATFORM" == "Linux" ]]; then
    if run_build "Android" "build_android.sh" "Android"; then
        BUILDS_SUCCESS=$((BUILDS_SUCCESS + 1))
    else
        BUILDS_FAILED=$((BUILDS_FAILED + 1))
    fi
else
    echo "✗ Android build SKIPPED (requires Linux)" | tee -a "$BUILD_LOG"
    BUILDS_SKIPPED=$((BUILDS_SKIPPED + 1))
fi

# iOS build (macOS only)
if [[ "$PLATFORM" == "Darwin" ]]; then
    if run_build "iOS" "build_ios.sh" "iOS"; then
        BUILDS_SUCCESS=$((BUILDS_SUCCESS + 1))
    else
        BUILDS_FAILED=$((BUILDS_FAILED + 1))
    fi
else
    echo "✗ iOS build SKIPPED (requires macOS)" | tee -a "$BUILD_LOG"
    BUILDS_SKIPPED=$((BUILDS_SKIPPED + 1))
fi

# Organize output files
echo "" | tee -a "$BUILD_LOG"
echo "========================================" | tee -a "$BUILD_LOG"
echo "Organizing build artifacts..." | tee -a "$BUILD_LOG"
echo "========================================" | tee -a "$BUILD_LOG"
echo "" | tee -a "$BUILD_LOG"

# Copy all builds to timestamped directory
if [ -d "output" ]; then
    find output -maxdepth 1 -type f -name "*.exe" -o -name "*.AppImage" -o -name "*.apk" -o -name "*.ipa" 2>/dev/null | while read file; do
        if [ -f "$file" ]; then
            echo "Copying: $(basename $file)" | tee -a "$BUILD_LOG"
            cp "$file" "$OUTPUT_DIR/"
        fi
    done
    
    # Copy README files
    find output -maxdepth 1 -type f -name "README-*.txt" 2>/dev/null | while read file; do
        if [ -f "$file" ]; then
            cp "$file" "$OUTPUT_DIR/"
        fi
    done
fi

# Create master README
cat > "$OUTPUT_DIR/README.txt" << EOF
Auto Servis - Multi-Platform Build
===================================

Build Date: $(date)
Platform: $PLATFORM

Build Results:
- Successful: $BUILDS_SUCCESS
- Failed: $BUILDS_FAILED
- Skipped: $BUILDS_SKIPPED

Contents:
---------
EOF

# List all files in output
ls -1 "$OUTPUT_DIR" | grep -v "README.txt" | grep -v "build.log" >> "$OUTPUT_DIR/README.txt" 2>/dev/null || true

cat >> "$OUTPUT_DIR/README.txt" << EOF

Installation Instructions:
--------------------------

Windows:
  - Run AutoServis-Windows.exe
  - No installation required

Linux:
  - chmod +x AutoServis-Linux-x86_64.AppImage
  - ./AutoServis-Linux-x86_64.AppImage

Android:
  - Enable "Install from Unknown Sources"
  - Install AutoServis-Android.apk

iOS:
  - Requires Xcode for code signing
  - See README-iOS.txt for details

Support:
--------
Email: auto-servis@example.com
Web: http://localhost:5000 (when running)

For detailed build logs, see build.log
EOF

# Calculate sizes
echo "" | tee -a "$BUILD_LOG"
echo "Build artifacts:" | tee -a "$BUILD_LOG"
du -h "$OUTPUT_DIR"/* 2>/dev/null | tee -a "$BUILD_LOG" || true

# Final summary
echo "" | tee -a "$BUILD_LOG"
echo "========================================" | tee -a "$BUILD_LOG"
echo "BUILD SUMMARY" | tee -a "$BUILD_LOG"
echo "========================================" | tee -a "$BUILD_LOG"
echo "Successful builds: $BUILDS_SUCCESS" | tee -a "$BUILD_LOG"
echo "Failed builds: $BUILDS_FAILED" | tee -a "$BUILD_LOG"
echo "Skipped builds: $BUILDS_SKIPPED" | tee -a "$BUILD_LOG"
echo "" | tee -a "$BUILD_LOG"
echo "Output directory: $OUTPUT_DIR" | tee -a "$BUILD_LOG"
echo "Build log: $BUILD_LOG" | tee -a "$BUILD_LOG"
echo "" | tee -a "$BUILD_LOG"
echo "Build completed at: $(date)" | tee -a "$BUILD_LOG"
echo "========================================" | tee -a "$BUILD_LOG"

# Create symlink to latest build
rm -f output/latest
ln -sf "build_${TIMESTAMP}" output/latest

echo ""
echo "Latest build linked at: output/latest"
echo ""

# Return appropriate exit code
if [ $BUILDS_FAILED -gt 0 ]; then
    exit 1
else
    exit 0
fi
