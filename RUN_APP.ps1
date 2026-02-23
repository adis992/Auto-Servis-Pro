# AUTO SERVIS PRO - Quick Launcher
# Pokrece Desktop + API Server odjednom

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   AUTO SERVIS PRO - QUICK START" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$rootPath = "C:\Users\admin11\Desktop\obd_full-scanner-repair"
$pythonExe = "$rootPath\.venv\bin\python.exe"
$apiScript = "$rootPath\narudzbe\api_server.py"
$desktopScript = "$rootPath\narudzbe\main.py"

# Provjeri da li Python postoji
if (-not (Test-Path $pythonExe)) {
    Write-Host "[ERROR] Python nije pronađen!" -ForegroundColor Red
    Write-Host "Putanja: $pythonExe" -ForegroundColor Yellow
    Write-Host "Pokrenite install.bat prvo!" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "[1/3] Pokretanje API servera na port 7000..." -ForegroundColor Yellow
$apiProcess = Start-Process -FilePath $pythonExe -ArgumentList $apiScript -WindowStyle Minimized -PassThru
Write-Host "  API Server PID: $($apiProcess.Id)" -ForegroundColor Green
Start-Sleep -Seconds 3

Write-Host "[2/3] Pokretanje Desktop aplikacije..." -ForegroundColor Yellow
$desktopProcess = Start-Process -FilePath $pythonExe -ArgumentList $desktopScript -PassThru
Write-Host "  Desktop App PID: $($desktopProcess.Id)" -ForegroundColor Green
Start-Sleep -Seconds 2

Write-Host "[3/3] Otvaranje web interfacea..." -ForegroundColor Yellow
Start-Process "http://localhost:7000"
Write-Host "  Web: http://localhost:7000" -ForegroundColor Green

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   SISTEM POKRENUT!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Desktop App: Prozor otvoren" -ForegroundColor White
Write-Host "API Server:  http://localhost:7000 (PID: $($apiProcess.Id))" -ForegroundColor White
Write-Host "Web Access:  Provjeri browser" -ForegroundColor White
Write-Host ""
Write-Host "Za zatvaranje:" -ForegroundColor Yellow
Write-Host "  - Zatvori Desktop App prozor" -ForegroundColor Gray
Write-Host "  - Ili: Stop-Process -Id $($apiProcess.Id)" -ForegroundColor Gray
Write-Host ""
Write-Host "API Endpoints:" -ForegroundColor Cyan
Write-Host "  http://localhost:7000/api/health" -ForegroundColor Gray
Write-Host "  http://localhost:7000/api/services" -ForegroundColor Gray
Write-Host "  http://localhost:7000/api/appointments" -ForegroundColor Gray
Write-Host ""

pause
