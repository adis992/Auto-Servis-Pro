@echo off
echo.
echo ======================================================
echo  🚗 Auto Servis Pro - Web Panel
echo ======================================================
echo.
echo Pokretanje API servera na http://localhost:7000
echo Web panel: http://localhost:7000/index.html
echo.
echo Pritisnite CTRL+C da zaustavite server
echo.
echo ======================================================
echo.

cd /d "%~dp0"
python narudzbe/api_server.py
pause
