#!/usr/bin/env python3
"""Quick Telegram Message Analyzer"""

from telethon.sync import TelegramClient
import json
from datetime import datetime

# Add your credentials here
API_ID = input("API_ID: ").strip() or '12345678'
API_HASH = input("API_HASH: ").strip() or 'your_hash_here'
PHONE = input("Phone (+7...): ").strip() or '+79999999999'

client = TelegramClient('foxemp_tg', API_ID, API_HASH)
client.start(PHONE)

# Parse t.me/tafsiria/5358
channel = 'tafsiria'
msg_id = 5358

print(f"\n🔍 Analyzing: t.me/{channel}/{msg_id}\n")

try:
    entity = client.get_entity(channel)
    msg = client.get_messages(entity, ids=msg_id)
    
    print(f"{'='*70}")
    print(f"📢 CHANNEL: {entity.title}")
    print(f"👥 Members: {entity.participants_count if hasattr(entity, 'participants_count') else 'N/A'}")
    print(f"🔗 Username: @{entity.username}")
    print(f"{'='*70}\n")
    
    print(f"📅 Date: {msg.date}")
    print(f"👁️  Views: {msg.views}")
    print(f"🔄 Forwards: {msg.forwards}")
    print(f"💬 Replies: {msg.replies.replies if msg.replies else 0}")
    print(f"\n📝 TEXT:\n{msg.text}\n")
    
    if msg.media:
        print(f"📎 Media: {type(msg.media).__name__}")
        path = client.download_media(msg, 'telegram_media/')
        print(f"💾 Downloaded: {path}")
    
    # Get sender info
    if msg.sender:
        print(f"\n👤 SENDER:")
        print(f"   ID: {msg.sender_id}")
        print(f"   Name: {msg.sender.first_name}")
        if msg.sender.username:
            print(f"   Username: @{msg.sender.username}")
    
    # Get replies
    print(f"\n💬 REPLIES:")
    for reply in client.iter_messages(entity, reply_to=msg_id, limit=10):
        print(f"   • {reply.sender.first_name}: {reply.text[:50]}...")
    
    # Save report
    data = {
        'channel': entity.title,
        'username': entity.username,
        'message_id': msg_id,
        'date': str(msg.date),
        'text': msg.text,
        'views': msg.views,
        'forwards': msg.forwards,
        'sender_id': msg.sender_id,
        'has_media': msg.media is not None
    }
    
    filename = f"telegram_analysis_{channel}_{msg_id}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Report: {filename}")
    print(f"{'='*70}\n")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n⚠️  Make sure you:")
    print("   1. Have valid API credentials from https://my.telegram.org")
    print("   2. Are a member of the channel")
    print("   3. Have authorized the session")

client.disconnect()
