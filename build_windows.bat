@echo off
REM Windows Build Script for Auto Servis Application
REM Builds standalone Windows EXE using PyInstaller

echo ========================================
echo Building Auto Servis for Windows
echo ========================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv\" (
    echo ERROR: Virtual environment not found
    echo Run install.bat first
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install PyInstaller if not present
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Clean previous builds
echo Cleaning previous builds...
if exist "build\" rmdir /s /q build
if exist "dist\" rmdir /s /q dist
if exist "*.spec" del /q *.spec

REM Create output directory
if not exist "output\" mkdir output

echo.
echo Building Windows executable...
echo.

REM Build with PyInstaller
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "AutoServis" ^
    --icon=icon.ico ^
    --add-data "narudzbe;narudzbe" ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --hidden-import=reportlab ^
    --hidden-import=reportlab.pdfgen ^
    --hidden-import=reportlab.lib ^
    --hidden-import=flask ^
    --hidden-import=flask_cors ^
    --hidden-import=win32print ^
    --hidden-import=win32api ^
    --hidden-import=sqlite3 ^
    --hidden-import=tkinter ^
    --hidden-import=tkcalendar ^
    --hidden-import=PIL ^
    --hidden-import=PIL._tkinter_finder ^
    --collect-all reportlab ^
    --collect-all flask ^
    --collect-all flask_cors ^
    --exclude-module=matplotlib ^
    --exclude-module=numpy ^
    --exclude-module=pandas ^
    narudzbe/main.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed
    exit /b 1
)

REM Copy executable to output
echo.
echo Copying executable to output folder...
copy "dist\AutoServis.exe" "output\AutoServis-Windows.exe"

REM Copy database initialization
if exist "narudzbe\database.py" (
    copy "narudzbe\database.py" "output\database.py"
)

REM Create README for distribution
echo Creating distribution README...
(
echo Auto Servis - Windows Distribution
echo ==================================
echo.
echo Installation:
echo 1. Run AutoServis-Windows.exe
echo 2. The application will create a database on first run
echo 3. Access the web interface at http://localhost:5000
echo.
echo Requirements:
echo - Windows 10 or later
echo - No additional software required
echo.
echo Support: auto-servis@example.com
) > "output\README-Windows.txt"

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo Executable: output\AutoServis-Windows.exe
echo.

REM Deactivate virtual environment
deactivate

pause
