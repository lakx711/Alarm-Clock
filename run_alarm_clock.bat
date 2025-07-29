@echo off
echo 🔔 Starting Python Alarm Clock...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.6 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show pygame >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Run the alarm clock
echo Starting alarm clock application...
python alarm_clock.py

REM If the application exits with an error
if errorlevel 1 (
    echo.
    echo The application encountered an error.
    echo Please check the error message above.
    pause
) 