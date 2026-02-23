@echo off
REM Auto Servis Installation Script for Windows
REM Sets up Python virtual environment and installs dependencies

echo ========================================
echo Auto Servis - Windows Installation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    echo.
    echo Please install Python 3.8 or later from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%a in ('python --version 2^>^&1') do set PYTHON_VERSION=%%a
echo Found Python %PYTHON_VERSION%

REM Check Python version (basic check)
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"
if errorlevel 1 (
    echo ERROR: Python 3.8 or later is required
    echo Current version: %PYTHON_VERSION%
    pause
    exit /b 1
)

echo.
echo Step 1: Creating virtual environment...
echo.

REM Remove old virtual environment if exists
if exist ".venv\" (
    echo Removing old virtual environment...
    rmdir /s /q .venv
)

REM Create new virtual environment
python -m venv .venv

if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Make sure python3-venv is installed
    pause
    exit /b 1
)

echo Virtual environment created successfully
echo.

REM Activate virtual environment
echo Step 2: Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Step 3: Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Step 4: Installing dependencies...
echo This may take a few minutes...
echo.

if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies
        echo Check your internet connection and try again
        pause
        exit /b 1
    )
) else (
    echo WARNING: requirements.txt not found
    echo Installing core dependencies...
    pip install flask flask-cors reportlab pillow tkcalendar pywin32
)

echo.
echo Step 5: Initializing database...
echo.

REM Check if database.py exists
if exist "narudzbe\database.py" (
    python narudzbe\database.py
    if errorlevel 1 (
        echo WARNING: Database initialization failed
        echo You may need to initialize it manually
    ) else (
        echo Database initialized successfully
    )
) else (
    echo WARNING: database.py not found
    echo Database will be created on first run
)

echo.
echo Step 6: Creating launcher scripts...
echo.

REM Create Windows launcher script
(
echo @echo off
echo call .venv\Scripts\activate.bat
echo python narudzbe\main.py
echo pause
) > run.bat

echo Created run.bat launcher

REM Create API server launcher
if exist "narudzbe\api_server.py" (
    (
    echo @echo off
    echo call .venv\Scripts\activate.bat
    echo python narudzbe\api_server.py
    echo pause
    ) > run_api.bat
    echo Created run_api.bat launcher
)

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo To run the application:
echo   1. Run: run.bat
echo   2. Or activate environment and run manually:
echo      .venv\Scripts\activate.bat
echo      python narudzbe\main.py
echo.
echo To run API server (if available):
echo   run_api.bat
echo.
echo Virtual environment location: .venv
echo.
echo ========================================

REM Deactivate virtual environment
deactivate

pause
