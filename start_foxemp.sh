#!/bin/bash
# FoXEmp Startup Script for Kali Linux

echo "🦊 Starting FoXEmp Professional Phone Geolocation System"
echo "=========================================================="

# Check if virtual environment exists
if [ ! -d "foxemp_env" ]; then
    echo "❌ Virtual environment not found. Creating..."
    python3 -m venv foxemp_env
    source foxemp_env/bin/activate
    pip install requests phonenumbers telethon
    echo "✅ Virtual environment created and dependencies installed"
else
    echo "✅ Virtual environment found"
fi

# Activate virtual environment
source foxemp_env/bin/activate

# Check if phone number provided
if [ $# -eq 0 ]; then
    echo ""
    echo "Usage: ./start_foxemp.sh <phone_number>"
    echo "Example: ./start_foxemp.sh +79187644740"
    echo ""
    echo "🦊 FoXEmp Ready - Phone Number Geolocation System"
    exit 1
fi

# Run FoXEmp
echo ""
echo "🚀 Launching FoXEmp with target: $1"
echo ""
python3 FoXEmp.py "$1"
