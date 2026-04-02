#!/usr/bin/env python3
"""
Telegram Group Members Scraper
"""

from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import json
import csv

API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
PHONE = 'YOUR_PHONE'

client = TelegramClient('session', API_ID, API_HASH)

async def scrape_members(group_username):
    """Scrape all members from group"""
    await client.connect()
    
    if not await client.is_user_authorized():
        await client.send_code_request(PHONE)
        await client.sign_in(PHONE, input('Code: '))
    
    group = await client.get_entity(group_username)
    print(f"📥 Scraping: {group.title}")
    
    members = []
    offset = 0
    limit = 100
    
    while True:
        participants = await client(GetParticipantsRequest(
            group, ChannelParticipantsSearch(''), offset, limit, hash=0
        ))
        
        if not participants.users:
            break
            
        for user in participants.users:
            members.append({
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'bot': user.bot
            })
            
        offset += len(participants.users)
        print(f"✅ Scraped: {len(members)} members")
        
    # Save JSON
    with open(f'{group_username}_members.json', 'w') as f:
        json.dump(members, f, indent=2)
        
    # Save CSV
    with open(f'{group_username}_members.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id','username','first_name','last_name','phone','bot'])
        writer.writeheader()
        writer.writerows(members)
        
    print(f"💾 Saved: {len(members)} members")
    await client.disconnect()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 telegram_members.py <group_username>")
        sys.exit(1)
        
    import asyncio
    asyncio.run(scrape_members(sys.argv[1]))
