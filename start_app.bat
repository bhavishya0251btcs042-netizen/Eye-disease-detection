@echo off
title VisionGuard AI - Desktop
color 0A
setlocal

echo ===================================================
echo      VisionGuard AI - Desktop Application
echo ===================================================
echo.

:: Get the directory of this script
set "SCRIPT_DIR=%~dp0"

:: Check for virtual environment and activate if present
if exist "%SCRIPT_DIR%.venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "%SCRIPT_DIR%.venv\Scripts\activate.bat"
) else (
    echo No virtual environment found, using system Python.
)

:: Navigate to the web_app directory
cd /d "%SCRIPT_DIR%web_app"

:: Check if python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in PATH. Please install Python.
    pause
    exit /b
)

:: Install specific dependencies
echo Checking and installing dependencies...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies.
    echo Please make sure you have internet access.
    pause
    exit /b
)

echo.
echo Launching Application...
echo.

:: Start the Desktop application
python desktop_app.py

pause
