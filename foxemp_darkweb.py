#!/usr/bin/env python3
"""
FoXEmp + SpiderFoot Darkweb OSINT Integration
"""

import subprocess
import json
import os
import sys

class FoXEmpDarkweb:
    def __init__(self):
        self.results = {}
        
    def fox_log(self, msg, level='info'):
        icons = {'info': '🦊', 'success': '✅', 'attack': '⚔️', 'found': '🔥', 'darkweb': '🕵️'}
        print(f"{icons.get(level, '🦊')} {msg}")
        
    def check_tor(self):
        """Check if Tor is running"""
        result = subprocess.run(["systemctl", "is-active", "tor"], 
                              capture_output=True, text=True)
        return result.returncode == 0
        
    def start_tor(self):
        """Start Tor service"""
        self.fox_log("Starting Tor service...", 'info')
        subprocess.run(["sudo", "systemctl", "start", "tor"], check=False)
        
    def scan_darkweb_url(self, url):
        """Scan darkweb URL with SpiderFoot"""
        self.fox_log(f"DARKWEB OSINT: Analyzing {url}", 'attack')
        
        # Ensure Tor is running
        if not self.check_tor():
            self.start_tor()
            
        # Clean URL
        target = url.replace('http://', '').replace('https://', '').rstrip('/')
        
        # SpiderFoot modules for darkweb
        modules = [
            "sfp_ahmia",
            "sfp_darksearch",
            "sfp_onioncity",
            "sfp_onionsearchengine",
            "sfp_torch",
            "sfp_torexits",
            "sfp_spider",
            "sfp_email",
            "sfp_bitcoin",
            "sfp_interesting_file",
            "sfp_crossref"
        ]
        
        cmd = [
            "spiderfoot",
            "-s", target,
            "-t", "DOMAIN_NAME",
            "-u", "investigate",
            "-o", "json"
        ]
        
        self.fox_log(f"Target: {target}", 'darkweb')
        self.fox_log("Running SpiderFoot scan...", 'attack')
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.stdout:
            try:
                # Parse SpiderFoot output
                lines = result.stdout.strip().split('\n')
                findings = []
                for line in lines:
                    if line.strip():
                        try:
                            data = json.loads(line)
                            findings.append(data)
                        except:
                            pass
                
                self.results['spiderfoot_findings'] = findings
                self.fox_log(f"Found {len(findings)} intelligence items", 'found')
                
                # Categorize findings
                emails = []
                bitcoin = []
                links = []
                mentions = []
                
                for finding in findings:
                    ftype = finding.get('type', '')
                    data = finding.get('data', '')
                    
                    if 'EMAIL' in ftype:
                        emails.append(data)
                    elif 'BITCOIN' in ftype:
                        bitcoin.append(data)
                    elif 'URL' in ftype or 'LINK' in ftype:
                        links.append(data)
                    elif 'DARKNET_MENTION' in ftype:
                        mentions.append(data)
                
                self.results['categorized'] = {
                    'emails': list(set(emails)),
                    'bitcoin_addresses': list(set(bitcoin)),
                    'links': list(set(links)),
                    'darknet_mentions': list(set(mentions))
                }
                
                if emails:
                    self.fox_log(f"Emails: {len(emails)}", 'found')
                if bitcoin:
                    self.fox_log(f"Bitcoin addresses: {len(bitcoin)}", 'found')
                if links:
                    self.fox_log(f"Links: {len(links)}", 'found')
                    
            except Exception as e:
                self.fox_log(f"Parse error: {e}", 'info')
                
        if result.stderr and "ERROR" in result.stderr:
            self.fox_log(f"Error: {result.stderr}", 'info')
            
        return self.results
        
    def display_results(self):
        """Display formatted results"""
        print(f"\n{'='*70}")
        print("🕵️  DARKWEB OSINT RESULTS")
        print(f"{'='*70}\n")
        
        cat = self.results.get('categorized', {})
        
        if cat.get('emails'):
            print("📧 EMAIL ADDRESSES FOUND:")
            for email in cat['emails'][:10]:
                print(f"   • {email}")
            if len(cat['emails']) > 10:
                print(f"   ... and {len(cat['emails']) - 10} more")
                
        if cat.get('bitcoin_addresses'):
            print("\n₿ BITCOIN ADDRESSES:")
            for btc in cat['bitcoin_addresses'][:5]:
                print(f"   • {btc}")
                
        if cat.get('links'):
            print(f"\n🔗 LINKS DISCOVERED: {len(cat['links'])}")
            for link in cat['links'][:5]:
                print(f"   • {link}")
                
        if cat.get('darknet_mentions'):
            print(f"\n🌐 DARKNET MENTIONS: {len(cat['darknet_mentions'])}")
            
        print(f"\n{'='*70}")
        
    def save_report(self, url):
        """Save report"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        os.makedirs('FOXEMP_DARKWEB_REPORTS', exist_ok=True)
        
        domain = url.split('/')[-1] if '/' in url else url
        domain = domain.replace('.onion', '').replace('http://', '').replace('https://', '')
        
        json_file = f"FOXEMP_DARKWEB_REPORTS/darkweb_{domain}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
            
        self.fox_log(f"Report saved: {json_file}", 'success')
        return json_file

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║   ███████╗ ██████╗ ██╗  ██╗███████╗███╗   ███╗██████╗           ║
║   ██╔════╝██╔═══██╗╚██╗██╔╝██╔════╝████╗ ████║██╔══██╗          ║
║   █████╗  ██║   ██║ ╚███╔╝ █████╗  ██╔████╔██║██████╔╝          ║
║   ██╔══╝  ██║   ██║ ██╔██╗ ██╔══╝  ██║╚██╔╝██║██╔═══╝           ║
║   ██║     ╚██████╔╝██╔╝ ██╗███████╗██║ ╚═╝ ██║██║               ║
║   ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝               ║
║              DARKWEB OSINT + SPIDERFOOT                           ║
╚═══════════════════════════════════════════════════════════════════╝
""")
    
    if len(sys.argv) < 2:
        print("Usage: python3 foxemp_darkweb.py <onion-url>")
        print("Example: python3 foxemp_darkweb.py http://example.onion")
        sys.exit(1)
        
    url = sys.argv[1]
    
    fox = FoXEmpDarkweb()
    fox.scan_darkweb_url(url)
    fox.display_results()
    fox.save_report(url)
    
    print("\n🦊 FoXEmp Darkweb OSINT Complete! 🦊\n")
