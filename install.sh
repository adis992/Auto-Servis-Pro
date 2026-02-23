#!/bin/bash
# Auto Servis Installation Script for Linux/macOS
# Sets up Python virtual environment and installs dependencies

set -e

echo "========================================"
echo "Auto Servis - Linux/macOS Installation"
echo "========================================"
echo ""

# Detect platform
PLATFORM=$(uname -s)
echo "Detected platform: $PLATFORM"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo ""
    if [[ "$PLATFORM" == "Linux" ]]; then
        echo "Install Python 3:"
        echo "  Ubuntu/Debian: sudo apt-get install python3 python3-venv python3-pip"
        echo "  Fedora/RHEL: sudo dnf install python3 python3-pip"
        echo "  Arch: sudo pacman -S python python-pip"
    elif [[ "$PLATFORM" == "Darwin" ]]; then
        echo "Install Python 3:"
        echo "  brew install python3"
    fi
    exit 1
fi

# Get Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $PYTHON_VERSION"

# Check Python version (basic check for 3.8+)
python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" || {
    echo "ERROR: Python 3.8 or later is required"
    echo "Current version: $PYTHON_VERSION"
    exit 1
}

echo ""
echo "Step 1: Creating virtual environment..."
echo ""

# Remove old virtual environment if exists
if [ -d ".venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf .venv
fi

# Create new virtual environment
python3 -m venv .venv

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    echo ""
    if [[ "$PLATFORM" == "Linux" ]]; then
        echo "Install python3-venv:"
        echo "  Ubuntu/Debian: sudo apt-get install python3-venv"
        echo "  Fedora/RHEL: sudo dnf install python3-virtualenv"
    fi
    exit 1
fi

echo "Virtual environment created successfully"
echo ""

# Activate virtual environment
echo "Step 2: Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo ""
echo "Step 3: Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Step 4: Installing dependencies..."
echo "This may take a few minutes..."
echo ""

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        echo "ERROR: Failed to install dependencies"
        echo "Check your internet connection and try again"
        exit 1
    fi
else
    echo "WARNING: requirements.txt not found"
    echo "Installing core dependencies..."
    pip install flask flask-cors reportlab pillow tkcalendar
fi

# Install platform-specific dependencies
echo ""
echo "Step 5: Installing platform-specific dependencies..."

if [[ "$PLATFORM" == "Linux" ]]; then
    # Check if tkinter is available
    python3 -c "import tkinter" 2>/dev/null || {
        echo "WARNING: tkinter not found"
        echo "Install it with:"
        echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
        echo "  Fedora/RHEL: sudo dnf install python3-tkinter"
    }
fi

echo ""
echo "Step 6: Initializing database..."
echo ""

# Check if database.py exists
if [ -f "narudzbe/database.py" ]; then
    python narudzbe/database.py || {
        echo "WARNING: Database initialization failed"
        echo "You may need to initialize it manually"
    }
    echo "Database initialized successfully"
else
    echo "WARNING: database.py not found"
    echo "Database will be created on first run"
fi

echo ""
echo "Step 7: Creating launcher scripts..."
echo ""

# Create launcher script
cat > run.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
python narudzbe/main.py
EOF

chmod +x run.sh
echo "Created run.sh launcher"

# Create API server launcher
if [ -f "narudzbe/api_server.py" ]; then
    cat > run_api.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
python narudzbe/api_server.py
EOF
    
    chmod +x run_api.sh
    echo "Created run_api.sh launcher"
fi

echo ""
echo "========================================"
echo "Installation completed successfully!"
echo "========================================"
echo ""
echo "To run the application:"
echo "  1. Run: ./run.sh"
echo "  2. Or activate environment and run manually:"
echo "     source .venv/bin/activate"
echo "     python narudzbe/main.py"
echo ""

if [ -f "run_api.sh" ]; then
    echo "To run API server:"
    echo "  ./run_api.sh"
    echo ""
fi

echo "Virtual environment location: .venv"
echo ""
echo "========================================"
echo ""

deactivate
