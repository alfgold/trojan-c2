#!/bin/bash

echo "[+] Setting up iCloud Hunt Tool..."

# Check if virtual environment exists
if [ ! -d "icloud_env" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv icloud_env
fi

# Install dependencies
echo "[*] Installing dependencies..."
./icloud_env/bin/pip install pyicloud requests beautifulsoup4

# Create reports directory
mkdir -p FOXEMP_REPORTS

echo "[+] Setup complete!"
echo "[*] Usage: ./icloud_hunt.py <icloud_email>"
echo "[*] Example: ./icloud_hunt.py user@icloud.com"
