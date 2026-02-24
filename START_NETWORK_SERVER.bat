@echo off
title AUTO SERVIS PRO - NETWORK SERVER
color 0B

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║     🌐 AUTO SERVIS PRO - NETWORK WEB PANEL SERVER          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Pokretanje servera sa mreznim pristupom...
echo.

cd /d "%~dp0"

REM Get local IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set IP=%%a
    goto :found
)
:found
set IP=%IP:~1%

echo ╔══════════════════════════════════════════════════════════════╗
echo ║  ✅ SERVER POKRENUT                                         ║
echo ╠══════════════════════════════════════════════════════════════╣
echo ║                                                              ║
echo ║  📍 LOKALNI PRISTUP:                                        ║
echo ║     http://localhost:7000                                    ║
echo ║                                                              ║
echo ║  🌐 MREZNI PRISTUP (sa drugih PC):                         ║
echo ║     http://%IP%:7000                             ║
echo ║                                                              ║
echo ║  👤 DEMO NALOZI:                                            ║
echo ║     Admin: admin / admin123                                 ║
echo ║     User:  user / user123                                   ║
echo ║                                                              ║
echo ║  💡 TIP: Daj drugima IP adresu da pristupe panelu!         ║
echo ║                                                              ║
echo ║  🛑 Pritisnite Ctrl+C za zaustavljanje servera              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Start network server
python network_server.py

pause
