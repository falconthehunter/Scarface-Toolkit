@echo off
setlocal enabledelayedexpansion

:: Colors using ANSI escape codes
for /F %%a in ('echo prompt $E^| cmd') do set "ESC=%%a"
set "BLUE=%ESC%[34m"
set "GREEN=%ESC%[32m"
set "RED=%ESC%[31m"
set "YELLOW=%ESC%[33m"
set "CYAN=%ESC%[36m"
set "RESET=%ESC%[0m"

echo %BLUE%▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
echo █ Scarface Environment Setup v3.0 █
echo ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀%RESET%

:check_python
echo %YELLOW%[1/5] Checking Python installation...%RESET%
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%✗ Python not found! Install Python 3 first%RESET%
    exit /b 1
)
echo %GREEN%✓ Python detected%RESET%
timeout /t 3 >nul

:create_links
echo %YELLOW%[2/5] Creating system links...%RESET%
set "BIN_DIR=%APPDATA%\scarface\bin"
mkdir "%BIN_DIR%" 2>nul
mklink "%BIN_DIR%\scarface.bat" "%~dp0scarface.bat" >nul
echo %GREEN%✓ Shortcuts created%RESET%
timeout /t 3 >nul

:set_permissions
echo %YELLOW%[3/5] Setting permissions...%RESET%
icacls "%~dp0scarface.bat" /grant Everyone:F >nul
echo %GREEN%✓ Permissions configured%RESET%
timeout /t 3 >nul

:install_deps
echo %YELLOW%[4/5] Installing dependencies...%RESET%
pip install flask requests termcolor bs4 >nul
echo %GREEN%✓ Dependencies installed%RESET%
timeout /t 3 >nul

:finalize
echo %YELLOW%[5/5] Finalizing...%RESET%
timeout /t 3 >nul
echo %GREEN%✓ Installation complete%RESET%

echo %CYAN%Run 'scarface' from any command prompt%RESET%
endlocal
