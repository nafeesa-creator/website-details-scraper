@echo off
echo =========================================
echo Website Details Scraper
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Install requirements
echo Installing dependencies...
pip install -q -r requirements.txt

REM Run the scraper
echo.
echo Starting scraper...
python website_scraper.py

pause