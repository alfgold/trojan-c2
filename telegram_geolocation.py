#!/usr/bin/env python3
"""Telegram Geolocation Extractor"""

from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaGeo, MessageMediaVenue, MessageMediaGeoLive
import json

API_ID = input("API_ID: ").strip()
API_HASH = input("API_HASH: ").strip()
PHONE = input("Phone: ").strip()

client = TelegramClient('geo_session', API_ID, API_HASH)
client.start(PHONE)

channel = 'tafsiria'
msg_id = 5358

print(f"\n🌍 Extracting geolocation from t.me/{channel}/{msg_id}\n")

try:
    entity = client.get_entity(channel)
    msg = client.get_messages(entity, ids=msg_id)
    
    print(f"📢 Channel: {entity.title}")
    print(f"📅 Date: {msg.date}")
    print(f"📝 Text: {msg.text}\n")
    
    # Check for geolocation
    if isinstance(msg.media, (MessageMediaGeo, MessageMediaVenue, MessageMediaGeoLive)):
        geo = msg.media.geo
        lat = geo.lat
        lon = geo.long
        
        print(f"{'='*70}")
        print(f"🎯 GEOLOCATION FOUND!")
        print(f"{'='*70}")
        print(f"📍 Latitude:  {lat}")
        print(f"📍 Longitude: {lon}")
        print(f"\n🗺️  MAPS:")
        print(f"   Google: https://www.google.com/maps?q={lat},{lon}")
        print(f"   Yandex: https://yandex.ru/maps/?ll={lon},{lat}&z=17")
        print(f"   OSM:    https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=17")
        
        if isinstance(msg.media, MessageMediaVenue):
            print(f"\n📍 Venue: {msg.media.title}")
            print(f"📍 Address: {msg.media.address}")
        
        # Save
        data = {
            'channel': channel,
            'message_id': msg_id,
            'latitude': lat,
            'longitude': lon,
            'date': str(msg.date),
            'text': msg.text,
            'google_maps': f"https://www.google.com/maps?q={lat},{lon}"
        }
        
        with open(f'geo_{channel}_{msg_id}.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n💾 Saved: geo_{channel}_{msg_id}.json")
        print(f"{'='*70}\n")
    else:
        print("❌ No geolocation data in this message")
        print(f"📎 Media type: {type(msg.media).__name__ if msg.media else 'None'}")
        
        # Download media if exists
        if msg.media:
            print("\n📥 Downloading media for manual analysis...")
            path = client.download_media(msg, 'telegram_media/')
            print(f"💾 Saved: {path}")
            
except Exception as e:
    print(f"❌ Error: {e}")

client.disconnect()
