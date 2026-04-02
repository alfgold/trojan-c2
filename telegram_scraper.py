#!/usr/bin/env python3
"""
FoXEmp Telegram OSINT Scraper
"""

from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import GetFullChannelRequest
import json
import os
from datetime import datetime

# API credentials (get from https://my.telegram.org)
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
PHONE = 'YOUR_PHONE'

class TelegramScraper:
    def __init__(self):
        self.client = None
        self.results = {}
        
    def connect(self):
        """Connect to Telegram"""
        self.client = TelegramClient('foxemp_session', API_ID, API_HASH)
        self.client.connect()
        if not self.client.is_user_authorized():
            self.client.send_code_request(PHONE)
            self.client.sign_in(PHONE, input('Enter code: '))
        print("✅ Connected to Telegram")
        
    def scrape_user(self, username):
        """Scrape user profile"""
        print(f"🔍 Scraping user: @{username}")
        try:
            user = self.client.get_entity(username)
            full = self.client(GetFullUserRequest(user))
            
            data = {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'bio': full.full_user.about,
                'verified': user.verified,
                'bot': user.bot,
                'scam': user.scam,
                'fake': user.fake,
                'premium': user.premium if hasattr(user, 'premium') else False
            }
            
            self.results['user'] = data
            print(f"✅ User: {user.first_name} (@{user.username})")
            return data
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
            
    def scrape_channel(self, username, limit=100):
        """Scrape channel/group"""
        print(f"🔍 Scraping channel: @{username}")
        try:
            channel = self.client.get_entity(username)
            full = self.client(GetFullChannelRequest(channel))
            
            data = {
                'id': channel.id,
                'title': channel.title,
                'username': channel.username,
                'members': full.full_chat.participants_count,
                'description': full.full_chat.about,
                'verified': channel.verified,
                'scam': channel.scam,
                'fake': channel.fake,
                'messages': []
            }
            
            # Get messages
            print(f"📥 Downloading {limit} messages...")
            for msg in self.client.iter_messages(channel, limit=limit):
                data['messages'].append({
                    'id': msg.id,
                    'date': str(msg.date),
                    'text': msg.text,
                    'views': msg.views,
                    'forwards': msg.forwards,
                    'sender_id': msg.sender_id
                })
                
            self.results['channel'] = data
            print(f"✅ Channel: {channel.title} ({data['members']} members)")
            return data
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
            
    def scrape_phone(self, phone):
        """Search by phone number"""
        print(f"🔍 Searching phone: {phone}")
        try:
            from telethon.tl.functions.contacts import ImportContactsRequest
            from telethon.tl.types import InputPhoneContact
            
            contact = InputPhoneContact(client_id=0, phone=phone, first_name="", last_name="")
            result = self.client(ImportContactsRequest([contact]))
            
            if result.users:
                user = result.users[0]
                data = {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'phone': phone
                }
                self.results['phone_search'] = data
                print(f"✅ Found: {user.first_name} (@{user.username})")
                return data
            else:
                print("❌ No user found")
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
            
    def save_report(self, target):
        """Save report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        os.makedirs('TELEGRAM_REPORTS', exist_ok=True)
        
        filename = f"TELEGRAM_REPORTS/telegram_{target}_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"💾 Report: {filename}")
        
    def disconnect(self):
        """Disconnect"""
        if self.client:
            self.client.disconnect()

if __name__ == "__main__":
    import sys
    
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                  FoXEmp Telegram OSINT Scraper                    ║
╚═══════════════════════════════════════════════════════════════════╝
""")
    
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python3 telegram_scraper.py user <username>")
        print("  python3 telegram_scraper.py channel <username> [limit]")
        print("  python3 telegram_scraper.py phone <phone_number>")
        sys.exit(1)
        
    mode = sys.argv[1]
    target = sys.argv[2]
    
    scraper = TelegramScraper()
    scraper.connect()
    
    if mode == 'user':
        scraper.scrape_user(target)
    elif mode == 'channel':
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 100
        scraper.scrape_channel(target, limit)
    elif mode == 'phone':
        scraper.scrape_phone(target)
    else:
        print("❌ Invalid mode")
        
    scraper.save_report(target)
    scraper.disconnect()
    print("\n🦊 Complete!\n")
