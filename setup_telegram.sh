#!/bin/bash
# FoXEmp Telegram OSINT Setup

echo "🦊 FoXEmp Telegram OSINT Setup"
echo "================================"

# Install Telethon
pip3 install telethon

echo ""
echo "✅ Installation complete!"
echo ""
echo "📝 SETUP INSTRUCTIONS:"
echo ""
echo "1. Get API credentials from: https://my.telegram.org/apps"
echo "   - Login with your phone number"
echo "   - Create new application"
echo "   - Copy API_ID and API_HASH"
echo ""
echo "2. Edit the scripts and add your credentials:"
echo "   API_ID = 'your_api_id'"
echo "   API_HASH = 'your_api_hash'"
echo "   PHONE = '+your_phone'"
echo ""
echo "3. Usage examples:"
echo "   python3 telegram_scraper.py user username"
echo "   python3 telegram_scraper.py channel channelname 500"
echo "   python3 telegram_scraper.py phone +79123456789"
echo "   python3 telegram_members.py groupname"
echo "   python3 telegram_messages.py username 1000 --media"
echo ""
echo "🦊 Ready to scrape!"
