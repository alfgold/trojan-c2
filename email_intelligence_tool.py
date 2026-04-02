#!/usr/bin/env python3
"""
Advanced Email Intelligence Tool - Extract maximum information from email addresses
"""

import sys
import os
import json
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import hashlib
import base64
import time

# Add virtual environment path
sys.path.insert(0, '/home/user/Desktop/FoXEmp-Final/icloud_env/lib/python3.13/site-packages')

class EmailIntelligenceTool:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Common data breach APIs and databases
        self.breach_apis = [
            'https://haveibeenpwned.com/api/v3/breachedaccount/',
            'https://breachdirectory.org/api/v1/lookup?email=',
            'https://api.xposedornot.com/v1/check/email/'
        ]
        
        # Email validation services
        self.validation_services = [
            'https://api.hunter.io/v2/email-verifier?email=',
            'https://api.kickbox.com/v2/verify?email='
        ]
    
    def analyze_email_structure(self, email):
        """Deep analysis of email structure and patterns"""
        print("[*] Analyzing email structure...")
        
        local_part = email.split('@')[0]
        domain = email.split('@')[1].lower()
        
        analysis = {
            'full_email': email,
            'local_part': local_part,
            'domain': domain,
            'length': len(local_part),
            'character_analysis': {},
            'pattern_analysis': {},
            'name_extraction': {},
            'cultural_indicators': {}
        }
        
        # Character analysis
        analysis['character_analysis'] = {
            'has_numbers': bool(re.search(r'\d', local_part)),
            'has_underscore': '_' in local_part,
            'has_period': '.' in local_part,
            'has_hyphen': '-' in local_part,
            'uppercase_ratio': sum(1 for c in local_part if c.isupper()) / len(local_part) if local_part else 0,
            'numeric_ratio': sum(1 for c in local_part if c.isdigit()) / len(local_part) if local_part else 0
        }
        
        # Pattern analysis
        patterns = {
            'first_last': re.match(r'^[a-z]+\.[a-z]+$', local_part.lower()),
            'firstlast': re.match(r'^[a-z]+[a-z]+$', local_part.lower()),
            'first_last_num': re.match(r'^[a-z]+\.[a-z]+\d+$', local_part.lower()),
            'first_num': re.match(r'^[a-z]+\d+$', local_part.lower()),
            'name_initial': re.match(r'^[a-z]\d*$', local_part.lower()),
            'full_name': re.match(r'^[a-z]+$', local_part.lower()),
            'custom': True
        }
        
        for pattern_name, pattern_match in patterns.items():
            if pattern_match and pattern_name != 'custom':
                analysis['pattern_analysis']['detected_pattern'] = pattern_name
                analysis['pattern_analysis']['custom'] = False
                break
        
        # Name extraction attempts
        possible_names = []
        
        # Split by common separators
        if '.' in local_part:
            parts = local_part.split('.')
            if len(parts) == 2 and all(len(part) > 1 for part in parts):
                possible_names.append({
                    'first_name': parts[0].title(),
                    'last_name': parts[1].title(),
                    'confidence': 'high'
                })
        
        if '_' in local_part:
            parts = local_part.split('_')
            if len(parts) == 2 and all(len(part) > 1 for part in parts):
                possible_names.append({
                    'first_name': parts[0].title(),
                    'last_name': parts[1].title(),
                    'confidence': 'medium'
                })
        
        # CamelCase detection
        camelcase_parts = re.findall(r'[A-Z][a-z]*', local_part)
        if len(camelcase_parts) >= 2:
            possible_names.append({
                'first_name': camelcase_parts[0],
                'last_name': ''.join(camelcase_parts[1:]),
                'confidence': 'medium'
            })
        
        analysis['name_extraction'] = possible_names
        
        # Cultural and linguistic indicators
        cultural_analysis = {
            'cyrillic_chars': bool(re.search(r'[а-яё]', local_part, re.IGNORECASE)),
            'nordic_chars': bool(re.search(r'[åäöø]', local_part, re.IGNORECASE)),
            'germanic_chars': bool(re.search(r'[äöüß]', local_part, re.IGNORECASE)),
            'romance_chars': bool(re.search(r'[àáâãäåæçèéêëìíîïñòóôõöùúûüýÿ]', local_part, re.IGNORECASE)),
            'estimated_origin': 'unknown'
        }
        
        # Estimate origin based on patterns
        if cultural_analysis['cyrillic_chars']:
            cultural_analysis['estimated_origin'] = 'slavic'
        elif cultural_analysis['nordic_chars']:
            cultural_analysis['estimated_origin'] = 'nordic'
        elif cultural_analysis['germanic_chars']:
            cultural_analysis['estimated_origin'] = 'germanic'
        elif cultural_analysis['romance_chars']:
            cultural_analysis['estimated_origin'] = 'romance'
        
        analysis['cultural_indicators'] = cultural_analysis
        
        return analysis
    
    def check_breach_databases(self, email):
        """Check email against known breach databases"""
        print("[*] Checking breach databases...")
        
        breach_results = {
            'email': email,
            'breaches_found': [],
            'total_breaches': 0,
            'risk_score': 'low'
        }
        
        # Note: These APIs typically require API keys, so we'll simulate the structure
        # In a real scenario, you'd need proper API keys
        
        # Simulated breach check (replace with actual API calls)
        try:
            # This is a placeholder - actual implementation would need API keys
            breach_results['note'] = 'Breach database checks require API keys for real implementation'
            breach_results['services_checked'] = [
                'HaveIBeenPwned',
                'BreachDirectory', 
                'XposedOrNot'
            ]
            
            # Generate email hash for correlation
            email_hash = hashlib.sha256(email.encode()).hexdigest()[:16]
            breach_results['email_hash'] = email_hash
            
        except Exception as e:
            breach_results['error'] = str(e)
        
        return breach_results
    
    def analyze_domain_intelligence(self, domain):
        """Gather intelligence about the email domain"""
        print(f"[*] Analyzing domain: {domain}")
        
        domain_analysis = {
            'domain': domain,
            'domain_type': 'unknown',
            'registration_info': {},
            'security_features': {},
            'reputation_indicators': {}
        }
        
        # Determine domain type
        free_providers = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com']
        corporate_domains = ['apple.com', 'microsoft.com', 'google.com', 'amazon.com']
        privacy_domains = ['protonmail.com', 'tutanota.com', 'mailfence.com']
        
        if domain in free_providers:
            domain_analysis['domain_type'] = 'free_provider'
        elif domain in corporate_domains:
            domain_analysis['domain_type'] = 'corporate'
        elif domain in privacy_domains:
            domain_analysis['domain_type'] = 'privacy_focused'
        elif 'icloud.com' in domain or 'me.com' in domain or 'mac.com' in domain:
            domain_analysis['domain_type'] = 'apple_ecosystem'
        else:
            domain_analysis['domain_type'] = 'custom_domain'
        
        # Check security features
        security_checks = {
            'has_mx_record': False,
            'has_spf_record': False,
            'has_dmarc_record': False,
            'has_dkim': False
        }
        
        try:
            # MX record check (simplified)
            mx_check_url = f"https://dns.google/resolve?name={domain}&type=MX"
            response = self.session.get(mx_check_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('Answer'):
                    security_checks['has_mx_record'] = True
            
            domain_analysis['security_features'] = security_checks
            
        except Exception as e:
            domain_analysis['security_check_error'] = str(e)
        
        # Reputation indicators
        reputation = {
            'domain_age': 'unknown',
            'category': 'unknown',
            'risk_level': 'low'
        }
        
        # Apple domains are generally reputable
        if 'apple' in domain or 'icloud' in domain:
            reputation['category'] = 'technology'
            reputation['risk_level'] = 'very_low'
        
        domain_analysis['reputation_indicators'] = reputation
        
        return domain_analysis
    
    def generate_email_variations(self, email):
        """Generate possible email variations for investigation"""
        print("[*] Generating email variations...")
        
        local_part = email.split('@')[0]
        domain = email.split('@')[1]
        
        variations = {
            'original': email,
            'common_variations': [],
            'typosquatting_variations': [],
            'similar_domains': []
        }
        
        # Common variations
        base_variations = [
            f"{local_part}@gmail.com",
            f"{local_part}@yahoo.com",
            f"{local_part}@outlook.com",
            f"{local_part}@hotmail.com"
        ]
        
        # Add variations with separators
        if '.' not in local_part and '_' not in local_part:
            base_variations.extend([
                f"{local_part}.{local_part}@{domain}",
                f"{local_part}_{local_part}@{domain}"
            ])
        
        variations['common_variations'] = list(set(base_variations))
        
        # Typosquatting variations
        typo_domains = [
            'icloud.co', 'icloud.net', 'icloude.com', 'icloud.org',
            'icloud.io', 'icloud.me', 'icloud.us'
        ]
        
        typo_variations = [f"{local_part}@{d}" for d in typo_domains]
        variations['typosquatting_variations'] = typo_variations
        
        # Similar domains
        similar_domains = ['me.com', 'mac.com', 'apple.com']
        similar_variations = [f"{local_part}@{d}" for d in similar_domains]
        variations['similar_domains'] = similar_variations
        
        return variations
    
    def extract_metadata_from_email(self, email):
        """Extract technical metadata from email"""
        print("[*] Extracting technical metadata...")
        
        metadata = {
            'email': email,
            'hashes': {},
            'encoding_info': {},
            'technical_analysis': {}
        }
        
        # Generate various hashes
        metadata['hashes'] = {
            'md5': hashlib.md5(email.encode()).hexdigest(),
            'sha1': hashlib.sha1(email.encode()).hexdigest(),
            'sha256': hashlib.sha256(email.encode()).hexdigest()
        }
        
        # Encoding analysis
        try:
            metadata['encoding_info'] = {
                'base64': base64.b64encode(email.encode()).decode(),
                'url_encoded': requests.utils.quote(email),
                'html_encoded': email.replace('@', '&#64;').replace('.', '&#46;')
            }
        except:
            metadata['encoding_info'] = {'error': 'Encoding failed'}
        
        # Technical analysis
        metadata['technical_analysis'] = {
            'total_length': len(email),
            'local_part_length': len(email.split('@')[0]),
            'domain_length': len(email.split('@')[1]),
            'is_valid_format': bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)),
            'risk_indicators': {
                'sequential_numbers': bool(re.search(r'\d{3,}', email)),
                'repeated_chars': bool(re.search(r'(.)\1{2,}', email)),
                'suspicious_pattern': bool(re.search(r'[0-9]{4,}', email))
            }
        }
        
        return metadata
    
    def generate_comprehensive_report(self, email):
        """Generate comprehensive email intelligence report"""
        print(f"[+] Generating comprehensive intelligence for: {email}")
        
        report = {
            'email': email,
            'timestamp': datetime.now().isoformat(),
            'report_type': 'comprehensive_email_intelligence',
            'analysis_sections': {}
        }
        
        # Run all analysis modules
        report['analysis_sections']['structure_analysis'] = self.analyze_email_structure(email)
        time.sleep(1)
        
        report['analysis_sections']['domain_intelligence'] = self.analyze_domain_intelligence(
            report['analysis_sections']['structure_analysis']['domain']
        )
        time.sleep(1)
        
        report['analysis_sections']['breach_analysis'] = self.check_breach_databases(email)
        time.sleep(1)
        
        report['analysis_sections']['email_variations'] = self.generate_email_variations(email)
        time.sleep(1)
        
        report['analysis_sections']['technical_metadata'] = self.extract_metadata_from_email(email)
        
        # Generate intelligence summary
        report['intelligence_summary'] = self.generate_intelligence_summary(report['analysis_sections'])
        
        return report
    
    def generate_intelligence_summary(self, sections):
        """Generate intelligence summary from all sections"""
        summary = {
            'risk_assessment': 'low',
            'confidence_level': 'medium',
            'key_insights': [],
            'investigation_recommendations': []
        }
        
        structure = sections.get('structure_analysis', {})
        domain_info = sections.get('domain_intelligence', {})
        
        # Risk assessment
        risk_factors = 0
        
        if structure.get('character_analysis', {}).get('has_numbers'):
            risk_factors += 1
            
        if structure.get('pattern_analysis', {}).get('detected_pattern') == 'custom':
            risk_factors += 1
            
        if domain_info.get('domain_type') == 'custom_domain':
            risk_factors += 1
        
        if risk_factors >= 2:
            summary['risk_assessment'] = 'medium'
        elif risk_factors >= 3:
            summary['risk_assessment'] = 'high'
        
        # Key insights
        insights = []
        
        if structure.get('name_extraction'):
            insights.append(f"Possible name patterns detected: {len(structure['name_extraction'])}")
        
        if domain_info.get('domain_type'):
            insights.append(f"Domain type: {domain_info['domain_type']}")
        
        if structure.get('cultural_indicators', {}).get('estimated_origin') != 'unknown':
            insights.append(f"Cultural origin indicator: {structure['cultural_indicators']['estimated_origin']}")
        
        summary['key_insights'] = insights
        
        # Investigation recommendations
        recommendations = []
        
        if structure.get('name_extraction'):
            recommendations.append("Investigate extracted name patterns for identity correlation")
        
        if domain_info.get('domain_type') == 'apple_ecosystem':
            recommendations.append("Focus on Apple ecosystem services and linked accounts")
        
        variations = sections.get('email_variations', {})
        if variations.get('common_variations'):
            recommendations.append(f"Check {len(variations['common_variations'])} email variations for additional accounts")
        
        summary['investigation_recommendations'] = recommendations
        
        return summary
    
    def save_report(self, report, filename=None):
        """Save comprehensive intelligence report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"email_intelligence_{report['email']}_{timestamp}.json"
        
        filepath = os.path.join('/home/user/Desktop/FoXEmp-Final/FOXEMP_REPORTS', filename)
        
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"[+] Intelligence report saved to: {filepath}")
            return filepath
        except Exception as e:
            print(f"[-] Error saving report: {e}")
            return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 email_intelligence_tool.py <email>")
        print("Example: python3 email_intelligence_tool.py user@icloud.com")
        sys.exit(1)
    
    email = sys.argv[1]
    tool = EmailIntelligenceTool()
    
    report = tool.generate_comprehensive_report(email)
    
    if report:
        tool.save_report(report)
        
        # Print summary
        print("\n" + "="*70)
        print("COMPREHENSIVE EMAIL INTELLIGENCE SUMMARY")
        print("="*70)
        summary = report['intelligence_summary']
        print(f"Email: {report['email']}")
        print(f"Risk Assessment: {summary['risk_assessment']}")
        print(f"Confidence Level: {summary['confidence_level']}")
        print("\nKey Insights:")
        for insight in summary['key_insights']:
            print(f"  • {insight}")
        print("\nInvestigation Recommendations:")
        for rec in summary['investigation_recommendations']:
            print(f"  → {rec}")

if __name__ == "__main__":
    main()
