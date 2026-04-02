#!/usr/bin/env python3
"""
Deep Footprint Analyzer - Advanced analysis of digital footprints
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

class DeepFootprintAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def analyze_github_footprint(self, email):
        """Deep analysis of GitHub footprint"""
        print("[*] Analyzing GitHub footprint...")
        
        results = {
            'platform': 'GitHub',
            'email': email,
            'findings': {}
        }
        
        try:
            # Search for email in GitHub
            search_url = f"https://github.com/search?q={email}&type=users"
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for user results
                user_links = soup.find_all('a', {'class': 'mr-1'})
                
                users_found = []
                for link in user_links:
                    href = link.get('href', '')
                    if href.startswith('/') and len(href) > 1:
                        username = href[1:]
                        users_found.append({
                            'username': username,
                            'profile_url': f"https://github.com{href}",
                            'found_in_search': True
                        })
                
                results['findings']['users'] = users_found
                
                # Search in code repositories
                code_search_url = f"https://github.com/search?q={email}&type=code"
                code_response = self.session.get(code_search_url, timeout=10)
                
                if code_response.status_code == 200:
                    code_soup = BeautifulSoup(code_response.text, 'html.parser')
                    repo_links = code_soup.find_all('a', {'class': 'v-align-middle'})
                    
                    repositories = []
                    for repo_link in repo_links[:5]:  # Limit to first 5 results
                        href = repo_link.get('href', '')
                        if href:
                            repositories.append({
                                'repository': href,
                                'url': f"https://github.com{href}",
                                'contains_email': True
                            })
                    
                    results['findings']['repositories'] = repositories
                
                # Check specific user profiles if any found
                detailed_profiles = []
                for user in users_found[:3]:  # Analyze top 3 users
                    profile_data = self.analyze_github_profile(user['profile_url'], email)
                    if profile_data:
                        detailed_profiles.append(profile_data)
                
                results['findings']['detailed_profiles'] = detailed_profiles
                
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    def analyze_github_profile(self, profile_url, email):
        """Analyze individual GitHub profile"""
        try:
            response = self.session.get(profile_url, timeout=10)
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            profile_data = {
                'url': profile_url,
                'username': profile_url.split('/')[-1],
                'email_found': False,
                'bio': '',
                'location': '',
                'company': '',
                'followers': 0,
                'following': 0,
                'repositories': 0
            }
            
            # Extract bio
            bio_elem = soup.find('div', {'class': 'p-note'})
            if bio_elem:
                profile_data['bio'] = bio_elem.get_text().strip()
            
            # Extract location
            location_elem = soup.find('span', {'class': 'p-label'})
            if location_elem:
                profile_data['location'] = location_elem.get_text().strip()
            
            # Extract company
            company_elem = soup.find('span', {'class': 'p-org'})
            if company_elem:
                profile_data['company'] = company_elem.get_text().strip()
            
            # Extract follower counts
            followers_elem = soup.find('a', {'href': f"{profile_url}?tab=followers"})
            if followers_elem:
                followers_text = followers_elem.get_text().strip()
                profile_data['followers'] = self.extract_number(followers_text)
            
            following_elem = soup.find('a', {'href': f"{profile_url}?tab=following"})
            if following_elem:
                following_text = following_elem.get_text().strip()
                profile_data['following'] = self.extract_number(following_text)
            
            # Check if email is visible in profile
            page_text = response.text.lower()
            if email.lower() in page_text:
                profile_data['email_found'] = True
            
            return profile_data
            
        except Exception as e:
            return {'error': str(e), 'url': profile_url}
    
    def analyze_linkedin_footprint(self, email):
        """Deep analysis of LinkedIn footprint"""
        print("[*] Analyzing LinkedIn footprint...")
        
        results = {
            'platform': 'LinkedIn',
            'email': email,
            'findings': {}
        }
        
        try:
            # LinkedIn search is more restricted, so we'll use public search
            search_url = f"https://www.linkedin.com/search/results/all/?keywords={email}"
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                # LinkedIn heavily uses JavaScript, so we'll extract what we can
                page_content = response.text
                
                # Look for profile patterns
                profile_patterns = [
                    r'linkedin\.com/in/([a-zA-Z0-9-]+)',
                    r'"firstName":"([^"]+)"',
                    r'"lastName":"([^"]+)"',
                    r'"headline":"([^"]+)"'
                ]
                
                profiles_found = []
                for pattern in profile_patterns:
                    matches = re.findall(pattern, page_content)
                    if matches:
                        profiles_found.extend(matches)
                
                results['findings']['raw_matches'] = list(set(profiles_found))  # Remove duplicates
                
                # Check for email in page content
                if email.lower() in page_content.lower():
                    results['findings']['email_present'] = True
                else:
                    results['findings']['email_present'] = False
                
                # Extract any visible profile information
                soup = BeautifulSoup(page_content, 'html.parser')
                
                # Look for name patterns
                title_elements = soup.find_all(['h1', 'h2', 'h3'])
                names_found = []
                for elem in title_elements:
                    text = elem.get_text().strip()
                    if len(text) > 2 and len(text) < 50:
                        names_found.append(text)
                
                results['findings']['potential_names'] = list(set(names_found))
                
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    def analyze_twitter_footprint(self, email):
        """Deep analysis of Twitter footprint"""
        print("[*] Analyzing Twitter footprint...")
        
        results = {
            'platform': 'Twitter',
            'email': email,
            'findings': {}
        }
        
        try:
            search_url = f"https://twitter.com/search?q={email}"
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                page_content = response.text
                
                # Look for Twitter handles
                handle_pattern = r'@([a-zA-Z0-9_]+)'
                handles = re.findall(handle_pattern, page_content)
                results['findings']['handles_found'] = list(set(handles))
                
                # Check for email mentions
                if email.lower() in page_content.lower():
                    results['findings']['email_mentioned'] = True
                else:
                    results['findings']['email_mentioned'] = False
                
                # Look for profile links
                profile_pattern = r'twitter\.com/([a-zA-Z0-9_]+)'
                profiles = re.findall(profile_pattern, page_content)
                results['findings']['profiles_found'] = list(set(profiles))
                
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    def extract_number(self, text):
        """Extract number from text like '1.2k followers'"""
        number_match = re.search(r'[\d,.]+', text)
        if number_match:
            number_str = number_match.group().replace(',', '')
            if 'k' in text.lower():
                return int(float(number_str) * 1000)
            elif 'm' in text.lower():
                return int(float(number_str) * 1000000)
            else:
                return int(number_str)
        return 0
    
    def correlate_findings(self, github_data, linkedin_data, twitter_data):
        """Correlate findings across platforms"""
        print("[*] Correlating findings across platforms...")
        
        correlation = {
            'cross_platform_patterns': [],
            'common_usernames': [],
            'potential_identity_links': []
        }
        
        # Extract usernames/handles from each platform
        github_usernames = []
        if 'users' in github_data.get('findings', {}):
            github_usernames = [user['username'] for user in github_data['findings']['users']]
        
        linkedin_handles = []
        if 'raw_matches' in linkedin_data.get('findings', {}):
            linkedin_handles = linkedin_data['findings']['raw_matches']
        
        twitter_handles = twitter_data.get('findings', {}).get('profiles_found', [])
        
        # Look for common patterns
        all_handles = github_usernames + linkedin_handles + twitter_handles
        handle_counts = {}
        for handle in all_handles:
            if isinstance(handle, str) and len(handle) > 2:
                clean_handle = handle.lower().replace('-', '').replace('_', '')
                handle_counts[clean_handle] = handle_counts.get(clean_handle, 0) + 1
        
        # Find handles that appear multiple times
        common_handles = {k: v for k, v in handle_counts.items() if v > 1}
        correlation['common_usernames'] = common_handles
        
        # Analyze potential identity links
        if github_usernames and linkedin_handles:
            correlation['potential_identity_links'].append({
                'type': 'github_linkedin_correlation',
                'github_users': github_usernames[:3],
                'linkedin_matches': linkedin_handles[:3]
            })
        
        return correlation
    
    def generate_deep_analysis_report(self, email):
        """Generate comprehensive deep analysis report"""
        print(f"[+] Starting deep footprint analysis for: {email}")
        
        # Analyze each platform
        github_analysis = self.analyze_github_footprint(email)
        time.sleep(2)  # Rate limiting
        
        linkedin_analysis = self.analyze_linkedin_footprint(email)
        time.sleep(2)
        
        twitter_analysis = self.analyze_twitter_footprint(email)
        
        # Correlate findings
        correlation = self.correlate_findings(github_analysis, linkedin_analysis, twitter_analysis)
        
        # Compile comprehensive report
        report = {
            'email': email,
            'timestamp': datetime.now().isoformat(),
            'analysis_type': 'deep_footprint_analysis',
            'platforms': {
                'github': github_analysis,
                'linkedin': linkedin_analysis,
                'twitter': twitter_analysis
            },
            'correlation': correlation,
            'summary': self.generate_summary(github_analysis, linkedin_analysis, twitter_analysis, correlation)
        }
        
        return report
    
    def generate_summary(self, github_data, linkedin_data, twitter_data, correlation):
        """Generate analysis summary"""
        summary = {
            'total_platforms_with_footprints': 0,
            'platforms_found': [],
            'identity_confidence': 'low',
            'key_findings': []
        }
        
        # Check which platforms have footprints
        if github_data.get('findings', {}).get('users'):
            summary['total_platforms_with_footprints'] += 1
            summary['platforms_found'].append('GitHub')
            summary['key_findings'].append(f"GitHub: {len(github_data['findings']['users'])} potential users found")
        
        if linkedin_data.get('findings', {}).get('email_present'):
            summary['total_platforms_with_footprints'] += 1
            summary['platforms_found'].append('LinkedIn')
            summary['key_findings'].append("LinkedIn: Email present in search results")
        
        if twitter_data.get('findings', {}).get('email_mentioned'):
            summary['total_platforms_with_footprints'] += 1
            summary['platforms_found'].append('Twitter')
            summary['key_findings'].append("Twitter: Email mentioned in search results")
        
        # Determine confidence level
        if correlation.get('common_usernames'):
            summary['identity_confidence'] = 'medium'
            summary['key_findings'].append(f"Cross-platform patterns detected: {len(correlation['common_usernames'])}")
        
        if summary['total_platforms_with_footprints'] >= 2:
            summary['identity_confidence'] = 'high'
        
        return summary
    
    def save_report(self, report, filename=None):
        """Save deep analysis report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"deep_analysis_{report['email']}_{timestamp}.json"
        
        filepath = os.path.join('/home/user/Desktop/FoXEmp-Final/FOXEMP_REPORTS', filename)
        
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"[+] Deep analysis report saved to: {filepath}")
            return filepath
        except Exception as e:
            print(f"[-] Error saving report: {e}")
            return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 deep_footprint_analyzer.py <email>")
        sys.exit(1)
    
    email = sys.argv[1]
    analyzer = DeepFootprintAnalyzer()
    
    report = analyzer.generate_deep_analysis_report(email)
    
    if report:
        analyzer.save_report(report)
        
        # Print summary
        print("\n" + "="*60)
        print("DEEP FOOTPRINT ANALYSIS SUMMARY")
        print("="*60)
        summary = report['summary']
        print(f"Email: {report['email']}")
        print(f"Platforms with footprints: {summary['total_platforms_with_footprints']}")
        print(f"Platforms found: {', '.join(summary['platforms_found'])}")
        print(f"Identity confidence: {summary['identity_confidence']}")
        print("\nKey Findings:")
        for finding in summary['key_findings']:
            print(f"  • {finding}")

if __name__ == "__main__":
    main()
