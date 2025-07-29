#!/bin/bash

echo "🔔 Starting Python Alarm Clock..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.6 or higher"
    exit 1
fi

# Check if requirements are installed
echo "Checking dependencies..."
if ! python3 -c "import pygame" &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

# Run the alarm clock
echo "Starting alarm clock application..."
python3 alarm_clock.py

# If the application exits with an error
if [ $? -ne 0 ]; then
    echo
    echo "The application encountered an error."
    echo "Please check the error message above."
fi 