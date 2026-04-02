#!/usr/bin/env python3
"""
RUN THIS SCRIPT TO ANALYZE t.me/tafsiria/5358

BEFORE RUNNING:
1. Go to: https://my.telegram.org/apps
2. Login with your phone number
3. Create new application
4. Copy API_ID and API_HASH below
"""

# PASTE YOUR CREDENTIALS HERE:
API_ID = ''  # Example: 12345678
API_HASH = ''  # Example: '0123456789abcdef0123456789abcdef'
PHONE = ''  # Example: '+79123456789'

# ============================================

from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaGeo, MessageMediaVenue, MessageMediaGeoLive
import json

if not API_ID or not API_HASH or not PHONE:
    print("❌ ERROR: Add your credentials at the top of this script!")
    print("Get them from: https://my.telegram.org/apps")
    exit(1)

client = TelegramClient('session', API_ID, API_HASH)
client.start(PHONE)

print("\n🔍 Analyzing t.me/tafsiria/5358\n")

try:
    msg = client.get_messages('tafsiria', ids=5358)
    
    print(f"📅 Date: {msg.date}")
    print(f"👁️  Views: {msg.views}")
    print(f"📝 Text: {msg.text}\n")
    
    if isinstance(msg.media, (MessageMediaGeo, MessageMediaVenue, MessageMediaGeoLive)):
        lat = msg.media.geo.lat
        lon = msg.media.geo.long
        
        print("="*60)
        print("🎯 GEOLOCATION FOUND!")
        print("="*60)
        print(f"📍 Latitude:  {lat}")
        print(f"📍 Longitude: {lon}")
        print(f"\n🗺️  Google Maps: https://www.google.com/maps?q={lat},{lon}")
        print(f"🗺️  Yandex Maps: https://yandex.ru/maps/?ll={lon},{lat}&z=17")
        print("="*60)
        
        with open('geolocation_result.json', 'w') as f:
            json.dump({'lat': lat, 'lon': lon, 'text': msg.text}, f, indent=2)
        print("\n💾 Saved: geolocation_result.json")
    else:
        print("❌ No geolocation in this message")
        if msg.media:
            path = client.download_media(msg)
            print(f"📥 Downloaded media: {path}")
            
except Exception as e:
    print(f"❌ Error: {e}")

client.disconnect()
