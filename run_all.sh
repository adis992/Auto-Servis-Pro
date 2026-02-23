#!/bin/bash
# Auto Servis - Complete Application Launcher
# Starts both API backend and Desktop frontend

set -e

cd "$(dirname "$0")"

echo "========================================"
echo "Auto Servis - Application Launcher"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
API_PORT=5000
API_HOST="localhost"
API_URL="http://${API_HOST}:${API_PORT}"
API_SCRIPT="narudzbe/api_server.py"
MAIN_SCRIPT="narudzbe/main.py"
LOG_DIR="logs"
API_LOG="${LOG_DIR}/api_server.log"
APP_LOG="${LOG_DIR}/app.log"

# Create logs directory
mkdir -p "$LOG_DIR"

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        return 0
    else
        return 1
    fi
}

# Function to kill processes on port
kill_port() {
    local port=$1
    print_info "Checking for processes on port $port..."
    
    if check_port $port; then
        print_warning "Port $port is in use, killing processes..."
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
        sleep 2
        
        if check_port $port; then
            print_error "Failed to free port $port"
            return 1
        else
            print_success "Port $port freed"
        fi
    else
        print_info "Port $port is available"
    fi
    return 0
}

# Function to cleanup on exit
cleanup() {
    echo ""
    print_info "Shutting down services..."
    
    if [ ! -z "$API_PID" ]; then
        print_info "Stopping API server (PID: $API_PID)..."
        kill $API_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$APP_PID" ]; then
        print_info "Stopping Desktop app (PID: $APP_PID)..."
        kill $APP_PID 2>/dev/null || true
    fi
    
    # Kill any remaining processes on API port
    kill_port $API_PORT
    
    print_success "Cleanup completed"
    exit 0
}

# Set trap for cleanup
trap cleanup EXIT INT TERM

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    print_error "Virtual environment not found"
    print_info "Run install.sh first"
    exit 1
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source .venv/bin/activate

# Check if required scripts exist
if [ ! -f "$API_SCRIPT" ]; then
    print_error "API server script not found: $API_SCRIPT"
    exit 1
fi

if [ ! -f "$MAIN_SCRIPT" ]; then
    print_error "Main application script not found: $MAIN_SCRIPT"
    exit 1
fi

# Kill any existing processes
print_info "Cleaning up existing processes..."
kill_port $API_PORT

# Kill any Python processes running our scripts
pkill -f "$API_SCRIPT" 2>/dev/null || true
pkill -f "$MAIN_SCRIPT" 2>/dev/null || true
sleep 1

echo ""
echo "========================================"
echo "Starting Services"
echo "========================================"
echo ""

# Start API server in background
print_info "Starting API server..."
python "$API_SCRIPT" > "$API_LOG" 2>&1 &
API_PID=$!

print_success "API server started (PID: $API_PID)"
print_info "API log: $API_LOG"

# Wait for API to be ready
print_info "Waiting for API server to be ready..."
MAX_WAIT=30
WAIT_COUNT=0

while ! check_port $API_PORT; do
    sleep 1
    WAIT_COUNT=$((WAIT_COUNT + 1))
    
    if [ $WAIT_COUNT -ge $MAX_WAIT ]; then
        print_error "API server failed to start within ${MAX_WAIT} seconds"
        print_info "Check log file: $API_LOG"
        tail -n 20 "$API_LOG"
        exit 1
    fi
    
    # Check if API process is still running
    if ! kill -0 $API_PID 2>/dev/null; then
        print_error "API server process died"
        print_info "Check log file: $API_LOG"
        tail -n 20 "$API_LOG"
        exit 1
    fi
done

print_success "API server is ready on $API_URL"

# Test API connection
print_info "Testing API connection..."
if curl -s -f "$API_URL" > /dev/null 2>&1 || curl -s -f "${API_URL}/api/health" > /dev/null 2>&1; then
    print_success "API is responding"
else
    print_warning "API test failed, but continuing anyway..."
fi

echo ""
print_info "Starting Desktop application..."

# Start main application in foreground
python "$MAIN_SCRIPT" > "$APP_LOG" 2>&1 &
APP_PID=$!

print_success "Desktop application started (PID: $APP_PID)"
print_info "Application log: $APP_LOG"

# Open browser (optional)
sleep 2
print_info "Opening web interface in browser..."

if command -v xdg-open &> /dev/null; then
    xdg-open "$API_URL" 2>/dev/null &
elif command -v open &> /dev/null; then
    open "$API_URL" 2>/dev/null &
elif command -v start &> /dev/null; then
    start "$API_URL" 2>/dev/null &
else
    print_warning "Could not open browser automatically"
    print_info "Please open: $API_URL"
fi

echo ""
echo "========================================"
echo "Services Running"
echo "========================================"
echo ""
echo "API Server:"
echo "  PID: $API_PID"
echo "  URL: $API_URL"
echo "  Log: $API_LOG"
echo ""
echo "Desktop App:"
echo "  PID: $APP_PID"
echo "  Log: $APP_LOG"
echo ""
echo "========================================"
echo ""
print_info "Press Ctrl+C to stop all services"
echo ""

# Wait for main application process
wait $APP_PID

echo ""
print_info "Desktop application exited"
