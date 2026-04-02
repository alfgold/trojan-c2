#!/usr/bin/env python3
"""Quick Telegram Message Analyzer for t.me/tafsiria/5358"""

import requests
import re

def analyze_telegram_link():
    url = "https://t.me/tafsiria/5358"
    
    print(f"🔍 Analyzing: {url}")
    print("="*50)
    
    try:
        # Try to get public preview
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        if response.status_code == 200:
            content = response.text
            
            # Extract basic info
            title_match = re.search(r'<title>(.*?)</title>', content)
            if title_match:
                print(f"📢 Title: {title_match.group(1)}")
            
            # Look for coordinates in meta tags or content
            coords = re.findall(r'[-+]?[0-9]*\.?[0-9]+,\s*[-+]?[0-9]*\.?[0-9]+', content)
            if coords:
                print(f"🌍 Potential coordinates found: {coords}")
                for coord in coords:
                    lat, lon = coord.split(',')
                    lat, lon = lat.strip(), lon.strip()
                    print(f"📍 Google Maps: https://www.google.com/maps?q={lat},{lon}")
                    print(f"📍 Yandex Maps: https://yandex.ru/maps/?ll={lon},{lat}&z=17")
            
            # Look for location mentions
            location_keywords = ['location', 'coordinates', 'latitude', 'longitude', 'geo', 'map']
            for keyword in location_keywords:
                if keyword.lower() in content.lower():
                    print(f"🔍 Found location keyword: {keyword}")
            
            print(f"\n📝 Channel: tafsiria")
            print(f"📝 Message ID: 5358")
            print(f"🔗 Direct link: {url}")
            
        else:
            print(f"❌ Cannot access public preview (Status: {response.status_code})")
            print("⚠️  This message may be:")
            print("   • Private/restricted")
            print("   • Deleted")
            print("   • Requires Telegram app access")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*50)
    print("🦊 For full analysis, use Telegram API with credentials")
    print("   Run: python3 telegram_geolocation.py")

if __name__ == "__main__":
    analyze_telegram_link()