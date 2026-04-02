#!/usr/bin/env python3
"""
Telegram Message & Media Scraper
"""

from telethon.sync import TelegramClient
import os

API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
PHONE = 'YOUR_PHONE'

def scrape_messages(target, limit=1000, download_media=False):
    """Scrape messages and optionally download media"""
    client = TelegramClient('session', API_ID, API_HASH)
    client.start(PHONE)
    
    entity = client.get_entity(target)
    print(f"📥 Scraping: {getattr(entity, 'title', entity.first_name)}")
    
    if download_media:
        os.makedirs(f'media_{target}', exist_ok=True)
    
    messages = []
    for msg in client.iter_messages(entity, limit=limit):
        data = {
            'id': msg.id,
            'date': str(msg.date),
            'text': msg.text,
            'views': msg.views,
            'forwards': msg.forwards,
            'sender_id': msg.sender_id,
            'has_media': msg.media is not None
        }
        
        if download_media and msg.media:
            path = client.download_media(msg, f'media_{target}/')
            data['media_path'] = path
            print(f"📥 Downloaded: {path}")
            
        messages.append(data)
        
    import json
    with open(f'{target}_messages.json', 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Saved {len(messages)} messages")
    client.disconnect()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 telegram_messages.py <username> [limit] [--media]")
        sys.exit(1)
        
    target = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 1000
    download_media = '--media' in sys.argv
    
    scrape_messages(target, limit, download_media)
