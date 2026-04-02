╔═══════════════════════════════════════════════════════════════════╗
║                    FOXEMP - FINAL VERSION                         ║
║          Professional Phone Number Geolocation System             ║
╚═══════════════════════════════════════════════════════════════════╝

USAGE:
======
cd ~/Desktop/FoXEmp-Final
python3 FoXEmp.py +79187644740

FEATURES:
=========
✓ Find address from phone number
✓ GPS coordinates (±500-2000m accuracy)
✓ Multi-source geolocation fusion
✓ Russian address geocoding (Yandex + DaData)
✓ 2 API tokens (200 requests/day)
✓ Automatic token switching
✓ HTML/JSON reports

FILES:
======
FoXEmp.py                    - Main tool
README.txt                   - This file
FOXEMP_REPORTS/              - Generated reports

API TOKENS:
===========
Token 1: pk.883608c99c767911680b650bad8c1146
Token 2: pk.f5d9bbf1b9a46009c20dcc98f8fddc6c

Total: 200 requests/day (100 per token)

Add more tokens at line 265 in FoXEmp.py

REPORTS:
========
JSON: FOXEMP_REPORTS/FoXEmp_[PHONE]_[TIMESTAMP].json
HTML: FOXEMP_REPORTS/FoXEmp_[PHONE]_[TIMESTAMP].html

SUPPORT:
========
UnwiredLabs: https://unwiredlabs.com/
OpenCellID: https://opencellid.org/
