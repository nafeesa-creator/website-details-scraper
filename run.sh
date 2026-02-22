#!/bin/bash

echo "========================================="
echo "Website Details Scraper"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed"
    echo "Install from: https://www.python.org/downloads/"
    exit 1
fi

# Install requirements
echo "Installing dependencies..."
pip3 install -q -r requirements.txt

# Run the scraper
echo ""
echo "Starting scraper..."
python3 website_scraper.py