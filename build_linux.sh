#!/bin/bash
# Linux Build Script for Auto Servis Application
# Builds AppImage using PyInstaller

set -e

echo "========================================"
echo "Building Auto Servis for Linux"
echo "========================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "ERROR: Virtual environment not found"
    echo "Run install.sh first"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Install PyInstaller if not present
if ! pip show pyinstaller &> /dev/null; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

# Install AppImage tools if not present
if ! command -v appimagetool &> /dev/null; then
    echo "Installing AppImage tools..."
    wget -c https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage -O appimagetool
    chmod +x appimagetool
    sudo mv appimagetool /usr/local/bin/
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist *.spec AppDir

# Create output directory
mkdir -p output

echo ""
echo "Building Linux executable..."
echo ""

# Build with PyInstaller
pyinstaller \
    --onefile \
    --name "AutoServis" \
    --add-data "narudzbe:narudzbe" \
    --add-data "templates:templates" \
    --add-data "static:static" \
    --hidden-import=reportlab \
    --hidden-import=reportlab.pdfgen \
    --hidden-import=reportlab.lib \
    --hidden-import=flask \
    --hidden-import=flask_cors \
    --hidden-import=sqlite3 \
    --hidden-import=tkinter \
    --hidden-import=tkcalendar \
    --hidden-import=PIL \
    --collect-all reportlab \
    --collect-all flask \
    --collect-all flask_cors \
    --exclude-module=matplotlib \
    --exclude-module=numpy \
    --exclude-module=pandas \
    narudzbe/main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Build failed"
    exit 1
fi

# Create AppImage structure
echo ""
echo "Creating AppImage..."
mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/256x256/apps

# Copy executable
cp dist/AutoServis AppDir/usr/bin/

# Create desktop entry
cat > AppDir/usr/share/applications/autoservis.desktop << EOF
[Desktop Entry]
Type=Application
Name=Auto Servis
Comment=Auto Service Management System
Exec=AutoServis
Icon=autoservis
Categories=Office;Database;
Terminal=false
EOF

# Create icon (if available)
if [ -f "icon.png" ]; then
    cp icon.png AppDir/usr/share/icons/hicolor/256x256/apps/autoservis.png
else
    # Create a simple placeholder icon
    echo "Creating placeholder icon..."
    convert -size 256x256 xc:blue -pointsize 72 -fill white -gravity center \
        -annotate +0+0 "AS" AppDir/usr/share/icons/hicolor/256x256/apps/autoservis.png 2>/dev/null || true
fi

# Create AppRun script
cat > AppDir/AppRun << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin/:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib/:${LD_LIBRARY_PATH}"
cd "${HERE}/usr/bin"
exec "${HERE}/usr/bin/AutoServis" "$@"
EOF

chmod +x AppDir/AppRun

# Build AppImage
if command -v appimagetool &> /dev/null; then
    appimagetool AppDir output/AutoServis-Linux-x86_64.AppImage
    chmod +x output/AutoServis-Linux-x86_64.AppImage
else
    echo "WARNING: appimagetool not found, copying executable only"
    cp dist/AutoServis output/AutoServis-Linux
    chmod +x output/AutoServis-Linux
fi

# Copy database initialization
if [ -f "narudzbe/database.py" ]; then
    cp narudzbe/database.py output/database.py
fi

# Create README for distribution
cat > output/README-Linux.txt << EOF
Auto Servis - Linux Distribution
=================================

Installation:
1. Make the AppImage executable: chmod +x AutoServis-Linux-x86_64.AppImage
2. Run: ./AutoServis-Linux-x86_64.AppImage
3. The application will create a database on first run
4. Access the web interface at http://localhost:5000

Requirements:
- Linux with glibc 2.17 or later
- X11 display server
- No additional dependencies required

Support: auto-servis@example.com
EOF

echo ""
echo "========================================"
echo "Build completed successfully!"
echo "========================================"
if [ -f "output/AutoServis-Linux-x86_64.AppImage" ]; then
    echo "AppImage: output/AutoServis-Linux-x86_64.AppImage"
else
    echo "Executable: output/AutoServis-Linux"
fi
echo ""

deactivate
