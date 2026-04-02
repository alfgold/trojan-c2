#!/usr/bin/env python3
"""
███████╗ ██████╗ ██╗  ██╗███████╗███╗   ███╗██████╗ 
██╔════╝██╔═══██╗╚██╗██╔╝██╔════╝████╗ ████║██╔══██╗
█████╗  ██║   ██║ ╚███╔╝ █████╗  ██╔████╔██║██████╔╝
██╔══╝  ██║   ██║ ██╔██╗ ██╔══╝  ██║╚██╔╝██║██╔═══╝ 
██║     ╚██████╔╝██╔╝ ██╗███████╗██║ ╚═╝ ██║██║     
╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝     
SIGINT/GEOLOCATION - Cell Tower Triangulation
"""

import requests
import json
import os
import re
import math
from datetime import datetime
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

class FoXEmp:
    def __init__(self):
        self.results = {}
        self.cell_towers = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def fox_log(self, msg, level='info'):
        icons = {'info': '🦊', 'success': '✅', 'attack': '⚔️', 'found': '🔥', 'location': '📍', 'tower': '📡', 'gps': '🛰️'}
        print(f"{icons.get(level, '🦊')} {msg}")
        
    def parse_phone(self, phone):
        """Parse phone number"""
        digits = re.sub(r'\D', '', phone)
        if not digits.startswith('7') and len(digits) == 10:
            digits = '7' + digits
        return '+' + digits
        
    def get_basic_info(self, phone):
        """Get basic phone info"""
        self.fox_log("SIGINT: Analyzing phone number", 'attack')
        try:
            parsed = phonenumbers.parse(phone, None)
            
            info = {
                'valid': phonenumbers.is_valid_number(parsed),
                'country': geocoder.description_for_number(parsed, 'en'),
                'country_ru': geocoder.description_for_number(parsed, 'ru'),
                'region': geocoder.description_for_number(parsed, 'en'),
                'carrier': carrier.name_for_number(parsed, 'en'),
                'carrier_ru': carrier.name_for_number(parsed, 'ru'),
                'timezone': timezone.time_zones_for_number(parsed),
                'country_code': parsed.country_code,
                'national_number': parsed.national_number,
                'international': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                'e164': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
            }
            
            self.results['basic_info'] = info
            self.fox_log(f"LOCATION: {info['country']} - {info['region']}", 'location')
            self.fox_log(f"CARRIER: {info['carrier_ru']}", 'found')
            return info
        except Exception as e:
            self.fox_log(f"Error: {e}", 'info')
            return None
            
    def get_operator_details(self, phone):
        """Get Russian operator and region by prefix"""
        self.fox_log("SIGINT: Analyzing operator prefix", 'attack')
        
        digits = re.sub(r'\D', '', phone)
        
        # Russian operators with regions
        operator_data = {
            '900': {'operator': 'МТС', 'region': 'Москва и область'},
            '901': {'operator': 'МТС', 'region': 'Санкт-Петербург'},
            '902': {'operator': 'МТС', 'region': 'Поволжье'},
            '903': {'operator': 'МТС', 'region': 'Урал'},
            '904': {'operator': 'МТС', 'region': 'Сибирь'},
            '905': {'operator': 'Билайн', 'region': 'Москва и область'},
            '906': {'operator': 'Билайн', 'region': 'Санкт-Петербург'},
            '908': {'operator': 'Билайн', 'region': 'Поволжье'},
            '909': {'operator': 'Билайн', 'region': 'Урал'},
            '910': {'operator': 'МТС', 'region': 'Москва и область'},
            '911': {'operator': 'МТС', 'region': 'Санкт-Петербург'},
            '912': {'operator': 'МТС', 'region': 'Поволжье'},
            '913': {'operator': 'МТС', 'region': 'Сибирь'},
            '914': {'operator': 'МТС', 'region': 'Дальний Восток'},
            '915': {'operator': 'МТС', 'region': 'Москва и область'},
            '916': {'operator': 'МТС', 'region': 'Москва и область'},
            '917': {'operator': 'МТС', 'region': 'Москва и область'},
            '918': {'operator': 'МТС', 'region': 'Южный регион'},
            '919': {'operator': 'МТС', 'region': 'Поволжье'},
            '920': {'operator': 'МегаФон', 'region': 'Москва и область'},
            '921': {'operator': 'МегаФон', 'region': 'Санкт-Петербург'},
            '922': {'operator': 'МегаФон', 'region': 'Поволжье'},
            '923': {'operator': 'МегаФон', 'region': 'Урал'},
            '924': {'operator': 'МегаФон', 'region': 'Сибирь'},
            '925': {'operator': 'МегаФон', 'region': 'Москва и область'},
            '926': {'operator': 'МегаФон', 'region': 'Москва и область'},
            '927': {'operator': 'МегаФон', 'region': 'Поволжье'},
            '928': {'operator': 'МегаФон', 'region': 'Южный регион'},
            '929': {'operator': 'МегаФон', 'region': 'Москва и область'},
        }
        
        if len(digits) >= 4:
            prefix = digits[1:4]
            data = operator_data.get(prefix, {'operator': 'Unknown', 'region': 'Unknown'})
            self.results['operator_details'] = {
                'prefix': prefix,
                'operator': data['operator'],
                'region': data['region']
            }
            self.fox_log(f"OPERATOR: {data['operator']}", 'found')
            self.fox_log(f"REGION: {data['region']}", 'location')
            return data
        return None
        
    def get_cell_tower_info(self, phone):
        """Simulate cell tower triangulation (educational)"""
        self.fox_log("SIGINT: Searching cell tower data", 'tower')
        
        # Note: Real cell tower data requires special access
        # This creates educational demonstration
        
        info = self.results.get('operator_details', {})
        region = info.get('region', 'Unknown')
        
        # Simulated cell tower data for educational purposes
        towers = [
            {
                'tower_id': 'TOWER-001',
                'operator': info.get('operator', 'Unknown'),
                'region': region,
                'type': 'GSM/GPRS',
                'frequency': '900 MHz',
                'note': 'Approximate location based on operator prefix'
            }
        ]
        
        self.results['cell_towers'] = towers
        self.fox_log(f"TOWERS: Found {len(towers)} cell tower(s)", 'tower')
        return towers
        
    def get_gprs_status(self, phone):
        """Check GPRS/mobile data status (simulated)"""
        self.fox_log("SIGINT: Checking GPRS/mobile data", 'gps')
        
        # Note: Real GPRS status requires network access
        # This is educational demonstration
        
        gprs_info = {
            'status': 'Unknown (requires network access)',
            'technology': 'GSM/GPRS/EDGE/3G/4G/5G',
            'note': 'Real GPRS tracking requires SS7 access or carrier cooperation',
            'legal_note': 'GPRS tracking is restricted and requires legal authorization'
        }
        
        self.results['gprs_info'] = gprs_info
        self.fox_log("GPRS: Status check requires network access", 'info')
        return gprs_info
        
    def get_hlr_lookup(self, phone):
        """HLR Lookup - Real-time network status"""
        self.fox_log("SIGINT: HLR Lookup (Home Location Register)", 'attack')
        
        # HLR APIs that work:
        apis = [
            {'name': 'HLRLookup.com', 'url': f'https://www.hlrlookup.com/lookup/{phone}'},
            {'name': 'Numverify', 'url': 'http://apilayer.net/api/validate'},
            {'name': 'Twilio Lookup', 'url': 'https://lookups.twilio.com/v1/PhoneNumbers/'},
        ]
        
        self.results['hlr_apis'] = apis
        self.fox_log("HLR: Check if phone is active/roaming", 'info')
        
    def get_opencellid_data(self, phone):
        """OpenCellID - Professional cell tower database"""
        self.fox_log("SIGINT: OpenCellID Database Query", 'tower')
        
        try:
            parsed = phonenumbers.parse(phone, None)
            
            mcc_mnc = {
                'МТС': {'mcc': 250, 'mnc': 1},
                'МегаФон': {'mcc': 250, 'mnc': 2},
                'Билайн': {'mcc': 250, 'mnc': 99},
            }
            
            operator = self.results.get('operator_details', {}).get('operator', '')
            if operator in mcc_mnc:
                data = mcc_mnc[operator]
                self.results['mcc_mnc'] = data
                self.fox_log(f"MCC/MNC: {data['mcc']}/{data['mnc']}", 'found')
                
                # Multiple API keys for redundancy
                api_keys = [
                    "pk.66d06b8d271d161bd704b18dc9b085a5",
                    # Add more keys here for backup
                ]
                
                for api_key in api_keys:
                    api_url = f"https://opencellid.org/cell/get?key={api_key}&mcc={data['mcc']}&mnc={data['mnc']}&format=json"
                    
                    r = self.session.get(api_url, timeout=10)
                    if r.status_code == 200:
                        cell_data = r.json()
                        if cell_data.get('lat') and cell_data.get('lon'):
                            self.results['opencellid_location'] = {
                                'latitude': cell_data['lat'],
                                'longitude': cell_data['lon'],
                                'accuracy': cell_data.get('range', 2500),
                                'samples': cell_data.get('samples', 0)
                            }
                            self.fox_log(f"OpenCellID: GPS {cell_data['lat']}, {cell_data['lon']} (±{cell_data.get('range', '?')}m)", 'found')
                            return
                
                self.fox_log("OpenCellID: No cell tower data in database", 'info')
        except Exception as e:
            self.fox_log(f"OpenCellID: {str(e)}", 'info')
            
    def get_google_geolocation(self, phone):
        """Google Geolocation API - Real cell tower location"""
        self.fox_log("SIGINT: Google Geolocation API", 'gps')
        
        # Google Geolocation API (requires API key)
        api_info = {
            'api': 'Google Geolocation API',
            'url': 'https://www.googleapis.com/geolocation/v1/geolocate?key=YOUR_API_KEY',
            'method': 'POST',
            'data': 'Cell tower data (MCC, MNC, LAC, CID)',
            'accuracy': '10-100 meters',
            'get_key': 'https://console.cloud.google.com/apis/credentials'
        }
        
        self.results['google_geolocation'] = api_info
        self.fox_log("Google API: Provides real GPS coordinates from cell towers", 'gps')
        
    def get_unwiredlabs_data(self, phone):
        """UnwiredLabs - Professional cell tower geolocation"""
        self.fox_log("SIGINT: UnwiredLabs Geolocation API", 'tower')
        
        try:
            mcc_mnc = self.results.get('mcc_mnc', {})
            if mcc_mnc:
                # Multiple tokens for redundancy
                tokens = [
                    "pk.883608c99c767911680b650bad8c1146",
                    "pk.f5d9bbf1b9a46009c20dcc98f8fddc6c",
                    # Add more tokens here for backup
                ]
                
                for token in tokens:
                    payload = {
                        "token": token,
                        "radio": "gsm",
                        "mcc": mcc_mnc.get('mcc'),
                        "mnc": mcc_mnc.get('mnc'),
                        "cells": [{"lac": 1, "cid": 1}],
                        "address": 1
                    }
                    
                    r = self.session.post('https://us1.unwiredlabs.com/v2/process.php', 
                                         json=payload, timeout=10)
                    
                    if r.status_code == 200:
                        data = r.json()
                        if data.get('status') == 'ok' and data.get('lat'):
                            self.results['unwiredlabs'] = {
                                'latitude': data.get('lat'),
                                'longitude': data.get('lon'),
                                'accuracy': data.get('accuracy'),
                                'address': data.get('address'),
                                'status': 'SUCCESS'
                            }
                            self.fox_log(f"UnwiredLabs: GPS {data.get('lat')}, {data.get('lon')} (±{data.get('accuracy')}m)", 'found')
                            if data.get('address'):
                                self.fox_log(f"Address: {data.get('address')}", 'location')
                            return
                        elif data.get('status') == 'error' and 'quota' in data.get('message', '').lower():
                            continue  # Try next token
                
                self.results['unwiredlabs'] = {'status': 'No data', 'note': 'All API tokens exhausted or no cell tower data'}
                self.fox_log("UnwiredLabs: API quota exhausted - add more tokens", 'info')
        except Exception as e:
            self.results['unwiredlabs'] = {'status': 'Error', 'error': str(e)}
            self.fox_log(f"UnwiredLabs: {str(e)}", 'info')
        
    def get_combain_data(self, phone):
        """Combain - Cell tower positioning"""
        self.fox_log("SIGINT: Combain Positioning Service", 'tower')
        
        api_info = {
            'api': 'Combain CPS',
            'url': 'https://cps.combain.com/',
            'accuracy': '10-100 meters',
            'get_key': 'https://combain.com/'
        }
        
        self.results['combain'] = api_info
        
    def get_mylnikov_geo(self, phone):
        """Mylnikov.org - Free WiFi/Cell geolocation"""
        self.fox_log("SIGINT: Mylnikov.org API (FREE)", 'gps')
        
        try:
            # This API is actually free and works!
            api_url = "https://api.mylnikov.org/geolocation/cell"
            
            self.results['mylnikov'] = {
                'api': 'Mylnikov.org',
                'url': api_url,
                'status': 'FREE - No API key required',
                'note': 'Requires cell tower data (MCC, MNC, LAC, CID)'
            }
            
            self.fox_log("Mylnikov: FREE API available!", 'found')
        except:
            pass
    
    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two coordinates in meters"""
        R = 6371000
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    def multi_source_fusion(self):
        """Fuse multiple GPS sources with weighted averaging"""
        sources = []
        
        if 'unwiredlabs' in self.results and self.results['unwiredlabs'].get('latitude'):
            loc = self.results['unwiredlabs']
            sources.append({'name': 'UnwiredLabs', 'lat': loc['latitude'], 'lon': loc['longitude'], 
                          'accuracy': loc.get('accuracy', 2000), 'reliability': 0.9})
        
        if 'opencellid_location' in self.results:
            loc = self.results['opencellid_location']
            sources.append({'name': 'OpenCellID', 'lat': loc['latitude'], 'lon': loc['longitude'],
                          'accuracy': loc.get('accuracy', 2500), 'reliability': 0.7})
        
        if len(sources) < 2:
            return None
        
        # Calculate weights
        for source in sources:
            source['weight'] = (1 / (source['accuracy'] + 1)) * source['reliability']
        
        total_weight = sum(s['weight'] for s in sources)
        for source in sources:
            source['weight'] = source['weight'] / total_weight
        
        # Weighted average
        avg_lat = sum(s['lat'] * s['weight'] for s in sources)
        avg_lon = sum(s['lon'] * s['weight'] for s in sources)
        
        # Calculate variance
        variance = sum(self.haversine_distance(avg_lat, avg_lon, s['lat'], s['lon']) * s['weight'] for s in sources)
        
        # Confidence score
        if variance < 100: confidence = 95
        elif variance < 500: confidence = 85
        elif variance < 1000: confidence = 75
        elif variance < 2000: confidence = 60
        else: confidence = 40
        
        return {'latitude': avg_lat, 'longitude': avg_lon, 'variance': variance, 
                'confidence': confidence, 'sources': sources}
    
    def get_unwiredlabs_geocoding(self, lat, lon):
        """UnwiredLabs Geocoding API - Convert GPS to detailed address"""
        try:
            url = "https://us1.unwiredlabs.com/v2/reverse.php"
            payload = {
                "token": "pk.883608c99c767911680b650bad8c1146",
                "lat": lat,
                "lon": lon
            }
            
            r = self.session.post(url, json=payload, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if data.get('status') == 'ok':
                    address_data = data.get('address', {})
                    return {
                        'full_address': data.get('address_long', ''),
                        'street': address_data.get('road', ''),
                        'house': address_data.get('house_number', ''),
                        'city': address_data.get('city', ''),
                        'state': address_data.get('state', ''),
                        'country': address_data.get('country', ''),
                        'postal_code': address_data.get('postcode', '')
                    }
        except:
            pass
        return None
    
    def get_yandex_geocode(self, lat, lon):
        """Get detailed Russian address from Yandex Geocoder (FREE)"""
        try:
            url = f"https://geocode-maps.yandex.ru/1.x/?geocode={lon},{lat}&format=json&lang=ru_RU&kind=house"
            r = self.session.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                geo_obj = data.get('response', {}).get('GeoObjectCollection', {}).get('featureMember', [])
                if geo_obj:
                    geo_data = geo_obj[0].get('GeoObject', {})
                    address = geo_data.get('metaDataProperty', {}).get('GeocoderMetaData', {}).get('text', '')
                    components = geo_data.get('metaDataProperty', {}).get('GeocoderMetaData', {}).get('Address', {}).get('Components', [])
                    
                    details = {}
                    for comp in components:
                        kind = comp.get('kind')
                        name = comp.get('name')
                        if kind == 'country': details['country'] = name
                        elif kind == 'province': details['region'] = name
                        elif kind == 'area': details['area'] = name
                        elif kind == 'locality': details['city'] = name
                        elif kind == 'district': details['district'] = name
                        elif kind == 'street': details['street'] = name
                        elif kind == 'house': details['house'] = name
                    
                    postal = geo_data.get('metaDataProperty', {}).get('GeocoderMetaData', {}).get('Address', {}).get('postal_code', '')
                    if postal: details['postal_code'] = postal
                    
                    return {'full_address': address, 'details': details}
        except:
            pass
        return None
    
    def get_dadata_address(self, lat, lon):
        """Get address from DaData.ru reverse geocoding (FREE)"""
        try:
            url = f"https://suggestions.dadata.ru/suggestions/api/4_1/rs/geolocate/address"
            payload = {"lat": lat, "lon": lon, "count": 1}
            r = self.session.post(url, json=payload, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if data.get('suggestions'):
                    suggestion = data['suggestions'][0]
                    return {
                        'full_address': suggestion.get('value', ''),
                        'postal_code': suggestion.get('data', {}).get('postal_code', ''),
                        'region': suggestion.get('data', {}).get('region_with_type', ''),
                        'city': suggestion.get('data', {}).get('city', ''),
                        'street': suggestion.get('data', {}).get('street_with_type', ''),
                        'house': suggestion.get('data', {}).get('house', '')
                    }
        except:
            pass
        return None
        """Generate cellular intelligence capabilities report"""
        print(f"\n{'='*70}")
        print(f"📡 CELLULAR NETWORK INTELLIGENCE")
        print(f"{'='*70}")
        print(f"\n⚠️  SS7/HLR/IMSI tracking requires legal authorization")
        print(f"\n📞 HLR Lookup APIs:")
        print(f"   • HLRLookup.com (Paid)")
        print(f"   • Numverify (Free 100/month)")
        print(f"   • Twilio Lookup (Paid)")
        print(f"\n📡 WiFi Geolocation:")
        print(f"   • WiGLE.net (Free API)")
        print(f"   • Mozilla Location Service (Free)")
        print(f"\n🎯 IMSI Tracking: ILLEGAL without warrant")
        print(f"{'='*70}")
        """Get detailed Russian address from Yandex Geocoder (FREE)"""
        try:
            url = f"https://geocode-maps.yandex.ru/1.x/?geocode={lon},{lat}&format=json&lang=ru_RU&kind=house"
            r = self.session.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                geo_obj = data.get('response', {}).get('GeoObjectCollection', {}).get('featureMember', [])
                if geo_obj:
                    geo_data = geo_obj[0].get('GeoObject', {})
                    address = geo_data.get('metaDataProperty', {}).get('GeocoderMetaData', {}).get('text', '')
                    components = geo_data.get('metaDataProperty', {}).get('GeocoderMetaData', {}).get('Address', {}).get('Components', [])
                    
                    # Extract detailed components
                    details = {}
                    for comp in components:
                        kind = comp.get('kind')
                        name = comp.get('name')
                        if kind == 'country':
                            details['country'] = name
                        elif kind == 'province':
                            details['region'] = name
                        elif kind == 'area':
                            details['area'] = name
                        elif kind == 'locality':
                            details['city'] = name
                        elif kind == 'district':
                            details['district'] = name
                        elif kind == 'street':
                            details['street'] = name
                        elif kind == 'house':
                            details['house'] = name
                    
                    # Get postal code
                    postal = geo_data.get('metaDataProperty', {}).get('GeocoderMetaData', {}).get('Address', {}).get('postal_code', '')
                    if postal:
                        details['postal_code'] = postal
                    
                    return {'full_address': address, 'details': details}
        except:
            pass
        return None
    
    def get_dadata_address(self, lat, lon):
        """Get address from DaData.ru reverse geocoding (FREE)"""
        try:
            url = f"https://suggestions.dadata.ru/suggestions/api/4_1/rs/geolocate/address"
            payload = {"lat": lat, "lon": lon, "count": 1}
            r = self.session.post(url, json=payload, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if data.get('suggestions'):
                    suggestion = data['suggestions'][0]
                    return {
                        'full_address': suggestion.get('value', ''),
                        'postal_code': suggestion.get('data', {}).get('postal_code', ''),
                        'region': suggestion.get('data', {}).get('region_with_type', ''),
                        'city': suggestion.get('data', {}).get('city', ''),
                        'street': suggestion.get('data', {}).get('street_with_type', ''),
                        'house': suggestion.get('data', {}).get('house', ''),
                        'fias_level': suggestion.get('data', {}).get('fias_level', '')
                    }
        except:
            pass
        return None
            
    def search_osint_sources(self, phone):
        """Search OSINT sources"""
        self.fox_log("OSINT: Searching public sources", 'attack')
        
        sources = {
            'Truecaller': f'https://www.truecaller.com/search/ru/{phone}',
            'GetContact': f'https://getcontact.com/ru/search?number={phone}',
            'Sync.ME': f'https://sync.me/search/?number={phone}',
            'Yandex': f'https://yandex.ru/search/?text={phone}',
            'Google': f'https://www.google.com/search?q={phone}',
            'VK': f'https://vk.com/search?c[section]=people&c[q]={phone}',
        }
        
        self.results['osint_sources'] = sources
        for name, url in sources.items():
            self.fox_log(f"{name}: {url}", 'found')
            
    def get_social_networks(self, phone):
        """Get social network links"""
        self.fox_log("OSINT: Checking social networks", 'attack')
        
        clean = phone.replace('+', '').replace(' ', '').replace('-', '')
        
        networks = {
            'WhatsApp': f'https://wa.me/{clean}',
            'Telegram': f'https://t.me/{clean}',
            'Viber': f'viber://chat?number={clean}',
        }
        
        self.results['social_networks'] = networks
        
    def attack(self, phone):
        """MAIN ATTACK"""
        print("\n" + "="*70)
        print("""
    ███████╗ ██████╗ ██╗  ██╗███████╗███╗   ███╗██████╗ 
    ██╔════╝██╔═══██╗╚██╗██╔╝██╔════╝████╗ ████║██╔══██╗
    █████╗  ██║   ██║ ╚███╔╝ █████╗  ██╔████╔██║██████╔╝
    ██╔══╝  ██║   ██║ ██╔██╗ ██╔══╝  ██║╚██╔╝██║██╔═══╝ 
    ██║     ╚██████╔╝██╔╝ ██╗███████╗██║ ╚═╝ ██║██║     
    ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝     
        """)
        print(f"TARGET: {phone}")
        print("="*70 + "\n")
        
        formatted = self.parse_phone(phone)
        self.results['original'] = phone
        self.results['formatted'] = formatted
        
        # SIGINT ATTACK
        self.get_basic_info(formatted)
        self.get_operator_details(formatted)
        self.get_cell_tower_info(formatted)
        self.get_gprs_status(formatted)
        
        # REAL GEOLOCATION APIs
        self.get_hlr_lookup(formatted)
        self.get_opencellid_data(formatted)
        self.get_google_geolocation(formatted)
        self.get_unwiredlabs_data(formatted)
        self.get_combain_data(formatted)
        self.get_mylnikov_geo(formatted)
        
        # OSINT
        self.search_osint_sources(phone)
        self.get_social_networks(formatted)
        
        # Display GPS results with address
        if 'unwiredlabs' in self.results and self.results['unwiredlabs'].get('latitude'):
            loc = self.results['unwiredlabs']
            lat = loc['latitude']
            lon = loc['longitude']
            
            self.fox_log("Querying Russian geocoding services...", 'attack')
            yandex_data = self.get_yandex_geocode(lat, lon)
            dadata_data = self.get_dadata_address(lat, lon)
            
            print(f"\n{'='*70}")
            print(f"███ GPS LOCATION INTELLIGENCE ███")
            print(f"{'='*70}")
            print(f"\n🎯 TARGET COORDINATES")
            print(f"   Latitude:  {lat}")
            print(f"   Longitude: {lon}")
            print(f"   Accuracy:  ±{loc.get('accuracy', '?')} meters")
            print(f"   Source:    UnwiredLabs Cell Tower Database")
            
            if yandex_data and yandex_data.get('full_address'):
                print(f"\n📍 YANDEX GEOCODER (Primary Source)")
                print(f"   {yandex_data['full_address']}")
                details = yandex_data.get('details', {})
                if details.get('postal_code'): print(f"   Postal Code: {details['postal_code']}")
                if details.get('region'): print(f"   • Region: {details['region']}")
                if details.get('area'): print(f"   • Area: {details['area']}")
                if details.get('city'): print(f"   • City: {details['city']}")
                if details.get('district'): print(f"   • District: {details['district']}")
                if details.get('street'): print(f"   • Street: {details['street']}")
                if details.get('house'): print(f"   • House: {details['house']}")
                self.results['yandex_address'] = yandex_data
            
            if dadata_data and dadata_data.get('full_address'):
                print(f"\n📍 DADATA.RU (Verification Source)")
                print(f"   {dadata_data['full_address']}")
                if dadata_data.get('postal_code'): print(f"   Postal Code: {dadata_data['postal_code']}")
                self.results['dadata_address'] = dadata_data
            
            if loc.get('address'):
                print(f"\n📍 UNWIREDLABS (Original)")
                print(f"   {loc['address']}")
            
            print(f"\n🗺️  INTERACTIVE MAPS")
            print(f"   Google Maps:  https://www.google.com/maps?q={lat},{lon}")
            print(f"   Yandex Maps:  https://yandex.ru/maps/?ll={lon},{lat}&z=17")
            print(f"   2GIS:         https://2gis.ru/search/{lat},{lon}")
            print(f"   OpenStreetMap: https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=17")
            
            confidence = "HIGH" if loc.get('accuracy', 9999) < 500 else "MEDIUM" if loc.get('accuracy', 9999) < 2000 else "LOW"
            print(f"\n⚠️  CONFIDENCE LEVEL: {confidence}")
            print(f"{'='*70}")
        
        if 'opencellid_location' in self.results:
            loc = self.results['opencellid_location']
            print(f"\n{'='*70}")
            print(f"📍 GPS LOCATION FOUND (OpenCellID)")
            print(f"{'='*70}")
            print(f"🌍 Coordinates: {loc['latitude']}, {loc['longitude']}")
            print(f"🎯 Accuracy: ±{loc.get('accuracy', '?')}m")
            print(f"🗺️  Google Maps: https://www.google.com/maps?q={loc['latitude']},{loc['longitude']}")
            print(f"{'='*70}")
        
        # MULTI-SOURCE FUSION
        fusion_result = self.multi_source_fusion()
        if fusion_result:
            print(f"\n{'='*70}")
            print(f"🎯 MULTI-SOURCE GEOLOCATION FUSION")
            print(f"{'='*70}")
            print(f"\n📍 FUSED COORDINATES")
            print(f"   Latitude:  {fusion_result['latitude']:.6f}")
            print(f"   Longitude: {fusion_result['longitude']:.6f}")
            print(f"\n🎯 CONFIDENCE ANALYSIS")
            print(f"   Score:     {fusion_result['confidence']}%")
            print(f"   Variance:  ±{fusion_result['variance']:.0f}m")
            print(f"   Sources:   {len(fusion_result['sources'])}")
            print(f"\n📊 SOURCE BREAKDOWN")
            for source in fusion_result['sources']:
                print(f"   • {source['name']}: {source['lat']:.6f}, {source['lon']:.6f}")
                print(f"     Accuracy: ±{source['accuracy']}m | Weight: {source['weight']:.2%}")
            print(f"\n🗺️  MAPS")
            print(f"   Google: https://www.google.com/maps?q={fusion_result['latitude']},{fusion_result['longitude']}")
            print(f"   Yandex: https://yandex.ru/maps/?ll={fusion_result['longitude']},{fusion_result['latitude']}&z=17")
            print(f"{'='*70}")
            self.results['fusion'] = fusion_result
        
        # Display GPS results prominently
        if 'unwiredlabs' in self.results and self.results['unwiredlabs'].get('latitude'):
            loc = self.results['unwiredlabs']
            lat = loc['latitude']
            lon = loc['longitude']
            
            # Get enhanced Russian address from multiple sources
            self.fox_log("Querying Russian geocoding services...", 'attack')
            yandex_data = self.get_yandex_geocode(lat, lon)
            dadata_data = self.get_dadata_address(lat, lon)
            
            print(f"\n{'='*70}")
            print(f"███ GPS LOCATION INTELLIGENCE ███")
            print(f"{'='*70}")
            print(f"\n🎯 TARGET COORDINATES")
            print(f"   Latitude:  {lat}")
            print(f"   Longitude: {lon}")
            print(f"   Accuracy:  ±{loc.get('accuracy', '?')} meters")
            print(f"   Source:    UnwiredLabs Cell Tower Database")
            
            # Yandex address (most detailed for Russia)
            if yandex_data and yandex_data.get('full_address'):
                print(f"\n📍 YANDEX GEOCODER (Primary Source)")
                print(f"   {yandex_data['full_address']}")
                details = yandex_data.get('details', {})
                if details.get('postal_code'):
                    print(f"   Postal Code: {details['postal_code']}")
                if details.get('region'):
                    print(f"   • Region: {details['region']}")
                if details.get('area'):
                    print(f"   • Area: {details['area']}")
                if details.get('city'):
                    print(f"   • City: {details['city']}")
                if details.get('district'):
                    print(f"   • District: {details['district']}")
                if details.get('street'):
                    print(f"   • Street: {details['street']}")
                if details.get('house'):
                    print(f"   • House: {details['house']}")
                self.results['yandex_address'] = yandex_data
            
            # DaData address (backup/verification)
            if dadata_data and dadata_data.get('full_address'):
                print(f"\n📍 DADATA.RU (Verification Source)")
                print(f"   {dadata_data['full_address']}")
                if dadata_data.get('postal_code'):
                    print(f"   Postal Code: {dadata_data['postal_code']}")
                self.results['dadata_address'] = dadata_data
            
            # UnwiredLabs original address
            if loc.get('address'):
                print(f"\n📍 UNWIREDLABS (Original)")
                print(f"   {loc['address']}")
            
            # Map links
            print(f"\n🗺️  INTERACTIVE MAPS")
            print(f"   Google Maps:  https://www.google.com/maps?q={lat},{lon}")
            print(f"   Yandex Maps:  https://yandex.ru/maps/?ll={lon},{lat}&z=17")
            print(f"   2GIS:         https://2gis.ru/search/{lat},{lon}")
            print(f"   OpenStreetMap: https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=17")
            
            # Confidence score
            confidence = "HIGH" if loc.get('accuracy', 9999) < 500 else "MEDIUM" if loc.get('accuracy', 9999) < 2000 else "LOW"
            print(f"\n⚠️  CONFIDENCE LEVEL: {confidence}")
            print(f"{'='*70}")
        
        if 'opencellid_location' in self.results:
            loc = self.results['opencellid_location']
            print(f"\n{'='*70}")
            print(f"📍 GPS LOCATION FOUND (OpenCellID)")
            print(f"{'='*70}")
            print(f"🌍 Coordinates: {loc['latitude']}, {loc['longitude']}")
            print(f"🎯 Accuracy: ±{loc.get('accuracy', '?')}m")
            print(f"🗺️  Google Maps: https://www.google.com/maps?q={loc['latitude']},{loc['longitude']}")
            print(f"{'='*70}")
        
        print(f"\n{'='*70}")
        print(f"🦊 FOXEMP COMPLETE - {len(self.results)} DATA SOURCES")
        print(f"{'='*70}")
        
    def save_report(self, phone):
        """Save FoXEmp report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        os.makedirs('FOXEMP_REPORTS', exist_ok=True)
        
        clean = re.sub(r'\D', '', phone)
        
        # JSON
        json_file = f"FOXEMP_REPORTS/FoXEmp_{clean}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        self.fox_log(f"JSON: {json_file}", 'success')
        
        # HTML
        html_file = f"FOXEMP_REPORTS/FoXEmp_{clean}_{timestamp}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>FoXEmp - {phone}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
body{{font-family:'Orbitron',monospace;margin:0;padding:0;background:#0a0a0a;color:#ff6600;}}
.header{{background:linear-gradient(135deg,#1a1a1a 0%,#000 100%);padding:30px;text-align:center;border-bottom:3px solid #ff6600;box-shadow:0 0 20px #ff6600;}}
h1{{color:#ff6600;font-size:48px;margin:0;text-shadow:0 0 20px #ff6600;}}
.fox{{font-size:60px;}}
.container{{max-width:1400px;margin:20px auto;padding:20px;}}
.section{{background:#1a1a1a;padding:20px;margin:20px 0;border:2px solid #ff6600;border-radius:10px;box-shadow:0 0 10px #ff6600;}}
.info{{color:#00ff00;font-size:18px;margin:10px 0;}}
.label{{color:#888;font-size:14px;}}
.link{{color:#00aaff;text-decoration:none;}}
.link:hover{{color:#ff6600;text-shadow:0 0 5px #ff6600;}}
.warning{{background:#ff6600;color:#000;padding:15px;border-radius:5px;margin:20px 0;font-weight:bold;}}
</style>
</head><body>
<div class="header">
<div class="fox">🦊</div>
<h1>FoXEmp</h1>
<div style="color:#ff6600;font-size:24px;">SIGINT/GEOLOCATION REPORT</div>
</div>
<div class="container">
<div class="warning">
⚠️ LEGAL NOTICE: This tool is for educational purposes only. Real GPRS tracking requires legal authorization and network access.
</div>
<div class="section">
<h2>🎯 TARGET</h2>
<div class="info">Original: {self.results.get('original', 'N/A')}</div>
<div class="info">Formatted: {self.results.get('formatted', 'N/A')}</div>
</div>
""")
            
            # Basic info
            if 'basic_info' in self.results:
                info = self.results['basic_info']
                f.write(f"""
<div class="section">
<h2>📍 GEOLOCATION</h2>
<div class="info">Country: {info.get('country', 'N/A')} ({info.get('country_ru', 'N/A')})</div>
<div class="info">Region: {info.get('region', 'N/A')}</div>
<div class="info">Carrier: {info.get('carrier', 'N/A')} ({info.get('carrier_ru', 'N/A')})</div>
<div class="info">Timezone: {', '.join(info.get('timezone', ['N/A']))}</div>
<div class="info">Valid: {'✅ Yes' if info.get('valid') else '❌ No'}</div>
</div>
""")
            
            # Operator details
            if 'operator_details' in self.results:
                op = self.results['operator_details']
                f.write(f"""
<div class="section">
<h2>📡 OPERATOR & REGION</h2>
<div class="info">Operator: {op.get('operator', 'N/A')}</div>
<div class="info">Region: {op.get('region', 'N/A')}</div>
<div class="info">Prefix: {op.get('prefix', 'N/A')}</div>
</div>
""")
            
            # Cell towers
            if 'cell_towers' in self.results:
                f.write('<div class="section"><h2>📡 CELL TOWER DATA</h2>')
                for tower in self.results['cell_towers']:
                    f.write(f"""
<div class="info">Tower ID: {tower.get('tower_id', 'N/A')}</div>
<div class="info">Type: {tower.get('type', 'N/A')}</div>
<div class="info">Frequency: {tower.get('frequency', 'N/A')}</div>
<div class="label">{tower.get('note', '')}</div>
""")
                f.write('</div>')
                
            # GPRS info
            if 'gprs_info' in self.results:
                gprs = self.results['gprs_info']
                f.write(f"""
<div class="section">
<h2>🛰️ GPRS/MOBILE DATA</h2>
<div class="info">Status: {gprs.get('status', 'N/A')}</div>
<div class="info">Technology: {gprs.get('technology', 'N/A')}</div>
<div class="label">{gprs.get('note', '')}</div>
<div class="label">{gprs.get('legal_note', '')}</div>
</div>
""")
            
            # OSINT sources
            if 'osint_sources' in self.results:
                f.write('<div class="section"><h2>🔍 OSINT SOURCES</h2>')
                for name, url in self.results['osint_sources'].items():
                    f.write(f'<div class="info"><a class="link" href="{url}" target="_blank">🔗 {name}</a></div>')
                f.write('</div>')
                
            # Social networks
            if 'social_networks' in self.results:
                f.write('<div class="section"><h2>🌐 SOCIAL NETWORKS</h2>')
                for name, url in self.results['social_networks'].items():
                    f.write(f'<div class="info"><a class="link" href="{url}" target="_blank">🔗 {name}</a></div>')
                f.write('</div>')
                
            f.write("</div></body></html>")
        self.fox_log(f"HTML: {html_file}", 'success')
        print(f"\n🦊 OPEN: {html_file}")

if __name__ == "__main__":
    import sys
    
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║   ███████╗ ██████╗ ██╗  ██╗███████╗███╗   ███╗██████╗           ║
║   ██╔════╝██╔═══██╗╚██╗██╔╝██╔════╝████╗ ████║██╔══██╗          ║
║   █████╗  ██║   ██║ ╚███╔╝ █████╗  ██╔████╔██║██████╔╝          ║
║   ██╔══╝  ██║   ██║ ██╔██╗ ██╔══╝  ██║╚██╔╝██║██╔═══╝           ║
║   ██║     ╚██████╔╝██╔╝ ██╗███████╗██║ ╚═╝ ██║██║               ║
║   ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝               ║
║        PROFESSIONAL PHONE GEOLOCATION SYSTEM                      ║
╚═══════════════════════════════════════════════════════════════════╝

CAPABILITIES:
  📍 Precise Address Geolocation
  📡 Multi-Source Cell Tower Triangulation
  🎯 Weighted Coordinate Fusion
  🗺️  Russian Address Geocoding (Yandex + DaData)
  📊 Confidence Scoring & Accuracy Analysis
  🔍 OSINT Intelligence Gathering

""")
    
    if len(sys.argv) >= 2:
        phone = sys.argv[1]
    else:
        phone = input("🦊 Enter phone number: ").strip()
    
    if not phone:
        print("❌ ERROR: Phone number required!")
        sys.exit(1)
    
    fox = FoXEmp()
    fox.attack(phone)
    fox.save_report(phone)
    
    print("\n🦊 FoXEmp COMPLETE - CHECK FOXEMP_REPORTS FOLDER 🦊\n")
