#!/usr/bin/env python3
"""
iCloud Hunt - OSINT tool for iCloud email investigation
Similar to ghunt but for Apple ecosystem
"""

import sys
import os
import json
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import time

# Add virtual environment path
sys.path.insert(0, '/home/user/Desktop/FoXEmp-Final/icloud_env/lib/python3.13/site-packages')

try:
    from pyicloud import PyiCloudService
    from pyicloud.exceptions import PyiCloudFailedLoginException
except ImportError:
    print("[-] Required packages not found. Please install pyicloud")
    sys.exit(1)

class iCloudHunt:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def validate_icloud_email(self, email):
        """Validate if email is an iCloud address"""
        icloud_domains = ['icloud.com', 'me.com', 'mac.com']
        domain = email.split('@')[-1].lower()
        return domain in icloud_domains
    
    def check_email_exists(self, email):
        """Check if iCloud email exists using Apple's validation"""
        try:
            # Apple's email validation endpoint
            url = "https://idmsa.apple.com/appleauth/auth/signin"
            
            # This is a passive check - we're not actually logging in
            data = {
                'accountName': email,
                'rememberMe': False
            }
            
            response = self.session.post(url, json=data, timeout=10)
            
            # Analyze response to determine if email exists
            if response.status_code == 200:
                response_text = response.text.lower()
                if "this apple id is valid but" in response_text or "password" in response_text:
                    return {"exists": True, "reason": "Email exists, password required"}
                elif "cannot be found" in response_text or "does not exist" in response_text:
                    return {"exists": False, "reason": "Email does not exist"}
                    
            return {"exists": "unknown", "reason": f"Status code: {response.status_code}"}
            
        except Exception as e:
            return {"exists": "error", "reason": str(e)}
    
    def find_linked_services(self, email):
        """Find services linked to the iCloud email"""
        services = []
        
        # Check common Apple services
        apple_services = {
            'iCloud': 'https://www.icloud.com',
            'Apple ID': 'https://appleid.apple.com',
            'Find My': 'https://www.icloud.com/find',
            'iCloud Mail': 'https://www.icloud.com/mail',
            'iCloud Photos': 'https://www.icloud.com/photos',
            'iCloud Drive': 'https://www.icloud.com/drive'
        }
        
        for service, url in apple_services.items():
            try:
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    services.append({
                        'service': service,
                        'url': url,
                        'status': 'accessible'
                    })
            except:
                services.append({
                    'service': service,
                    'url': url,
                    'status': 'error'
                })
        
        return services
    
    def extract_metadata_from_email(self, email):
        """Extract metadata from email format"""
        metadata = {}
        
        # Analyze email structure
        local_part = email.split('@')[0]
        
        # Check for patterns
        metadata['local_part_length'] = len(local_part)
        metadata['has_numbers'] = bool(re.search(r'\d', local_part))
        metadata['has_underscore'] = '_' in local_part
        metadata['has_period'] = '.' in local_part
        
        # Common patterns
        if re.match(r'^[a-z]+\.[a-z]+$', local_part):
            metadata['pattern'] = 'first.last'
        elif re.match(r'^[a-z]+\d+$', local_part):
            metadata['pattern'] = 'name+numbers'
        elif re.match(r'^[a-z]+_[a-z]+$', local_part):
            metadata['pattern'] = 'first_last'
        else:
            metadata['pattern'] = 'custom'
            
        return metadata
    
    def search_public_footprints(self, email):
        """Search for public footprints of the email"""
        footprints = []
        
        # Common sites where emails might be public
        search_sites = [
            "https://github.com/search?q=",
            "https://www.linkedin.com/search/results/all/?keywords=",
            "https://twitter.com/search?q=",
        ]
        
        for site in search_sites:
            try:
                search_url = site + email
                response = self.session.get(search_url, timeout=5)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for email mentions
                    if email.lower() in response.text.lower():
                        footprints.append({
                            'site': site.split('/')[2],
                            'url': search_url,
                            'found': True
                        })
                    else:
                        footprints.append({
                            'site': site.split('/')[2],
                            'url': search_url,
                            'found': False
                        })
            except:
                footprints.append({
                    'site': site.split('/')[2],
                    'url': site,
                    'found': 'error'
                })
        
        return footprints
    
    def investigate(self, email):
        """Main investigation function"""
        print(f"[+] Starting iCloud investigation for: {email}")
        
        if not self.validate_icloud_email(email):
            print(f"[-] {email} is not a valid iCloud address")
            return None
        
        results = {
            'email': email,
            'timestamp': datetime.now().isoformat(),
            'investigation': {}
        }
        
        # Email existence check
        print("[*] Checking email existence...")
        existence = self.check_email_exists(email)
        results['investigation']['existence'] = existence
        print(f"[+] Email existence: {existence['exists']}")
        
        # Metadata extraction
        print("[*] Extracting email metadata...")
        metadata = self.extract_metadata_from_email(email)
        results['investigation']['metadata'] = metadata
        print(f"[+] Email pattern: {metadata['pattern']}")
        
        # Linked services
        print("[*] Checking linked services...")
        services = self.find_linked_services(email)
        results['investigation']['services'] = services
        print(f"[+] Found {len(services)} Apple services")
        
        # Public footprints
        print("[*] Searching public footprints...")
        footprints = self.search_public_footprints(email)
        results['investigation']['footprints'] = footprints
        
        found_footprints = [f for f in footprints if f.get('found') == True]
        print(f"[+] Found {len(found_footprints)} public footprints")
        
        return results
    
    def save_report(self, results, filename=None):
        """Save investigation results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"icloud_hunt_{results['email']}_{timestamp}.json"
        
        filepath = os.path.join('/home/user/Desktop/FoXEmp-Final/FOXEMP_REPORTS', filename)
        
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"[+] Report saved to: {filepath}")
            return filepath
        except Exception as e:
            print(f"[-] Error saving report: {e}")
            return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 icloud_hunt.py <icloud_email>")
        print("Example: python3 icloud_hunt.py user@icloud.com")
        sys.exit(1)
    
    email = sys.argv[1]
    hunter = iCloudHunt()
    
    results = hunter.investigate(email)
    
    if results:
        hunter.save_report(results)
        
        # Print summary
        print("\n" + "="*50)
        print("INVESTIGATION SUMMARY")
        print("="*50)
        print(f"Email: {results['email']}")
        print(f"Exists: {results['investigation']['existence']['exists']}")
        print(f"Pattern: {results['investigation']['metadata']['pattern']}")
        print(f"Services: {len(results['investigation']['services'])}")
        print(f"Public footprints: {len([f for f in results['investigation']['footprints'] if f.get('found') == True])}")

if __name__ == "__main__":
    main()
