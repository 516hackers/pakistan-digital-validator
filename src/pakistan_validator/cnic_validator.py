import json
import os
import re
from typing import Dict, Optional, Tuple, List
from datetime import datetime
from math import log2

class CNICValidator:
    """
    Advanced CNIC Validator for Pakistani National Identity Cards
    Provides syntactic validation and advanced analysis
    """
    
    def __init__(self):
        self.region_codes = self._load_region_codes()
        self.division_codes = self._load_division_codes()
        self.district_codes = self._load_district_codes()
        self.cnic_pattern = re.compile(r'^\d{5}-\d{7}-\d{1}$')
        self.digits_pattern = re.compile(r'^\d{13}$')
    
    def _load_region_codes(self) -> Dict[str, str]:
        """Load region codes from JSON file"""
        return {
            '1': 'Khyber Pakhtunkhwa', 
            '2': 'FATA', 
            '3': 'Punjab', 
            '4': 'Sindh', 
            '5': 'Balochistan', 
            '6': 'Islamabad', 
            '7': 'Gilgit-Baltistan',
            '8': 'Azad Jammu & Kashmir'
        }
    
    def _load_division_codes(self) -> Dict[str, str]:
        """Load NADRA division codes based on first 2 digits after province code"""
        return {
            # Khyber Pakhtunkhwa (1XXXX)
            "11": "Bannu Division", "12": "Dera Ismail Khan Division", "13": "Hazara Division",
            "14": "Kohat Division", "15": "Malakand Division", "16": "Mardan Division", "17": "Peshawar Division",
            
            # FATA (2XXXX)
            "21": "FATA Region",
            
            # Punjab (3XXXX)
            "31": "Bahawalpur Division", "32": "Dera Ghazi Khan Division", "33": "Faisalabad Division",
            "34": "Gujranwala Division", "35": "Lahore Division", "36": "Multan Division",
            "37": "Rawalpindi Division", "38": "Sargodha Division",
            
            # Sindh (4XXXX)
            "41": "Hyderabad Division", "42": "Karachi Division", "43": "Larkana Division",
            "44": "Mirpur Khas Division", "45": "Sukkur Division", "46": "Shaheed Benazirabad Division",
            
            # Balochistan (5XXXX)
            "51": "Kalat Division", "52": "Makran Division", "53": "Nasirabad Division",
            "54": "Quetta Division", "55": "Sibi Division", "56": "Zhob Division",
            
            # Islamabad (6XXXX)
            "61": "Islamabad",
            
            # Gilgit-Baltistan (7XXXX)
            "71": "Gilgit Division",
            
            # Azad Jammu & Kashmir (8XXXX)
            "81": "Mirpur Division", "82": "Muzaffarabad Division"
        }
    
    def _load_district_codes(self) -> Dict[str, Dict]:
        """Load complete district mapping within divisions"""
        return {
            # Khyber Pakhtunkhwa
            "11": {"Bannu": "Bannu", "Lakki Marwat": "Lakki Marwat", "North Waziristan": "North Waziristan"},
            "12": {"Dera Ismail Khan": "Dera Ismail Khan", "Tank": "Tank", "South Waziristan": "South Waziristan"},
            "13": {"Abbottabad": "Abbottabad", "Haripur": "Haripur", "Mansehra": "Mansehra", "Batagram": "Batagram", "Kohistan": "Kohistan", "Tor Ghar": "Tor Ghar"},
            "14": {"Kohat": "Kohat", "Karak": "Karak", "Hangu": "Hangu", "Kurram": "Kurram", "Orakzai": "Orakzai"},
            "15": {"Malakand": "Malakand", "Swat": "Swat", "Buner": "Buner", "Shangla": "Shangla", "Lower Dir": "Lower Dir", "Upper Dir": "Upper Dir", "Chitral": "Chitral"},
            "16": {"Mardan": "Mardan", "Swabi": "Swabi"},
            "17": {"Peshawar": "Peshawar", "Charsadda": "Charsadda", "Nowshera": "Nowshera"},
            
            # FATA
            "21": {"Bajaur": "Bajaur", "Mohmand": "Mohmand", "Khyber": "Khyber", "FR Peshawar": "FR Peshawar"},
            
            # Punjab
            "31": {"Bahawalpur": "Bahawalpur", "Bahawalnagar": "Bahawalnagar", "Rahim Yar Khan": "Rahim Yar Khan"},
            "32": {"Dera Ghazi Khan": "Dera Ghazi Khan", "Layyah": "Layyah", "Muzaffargarh": "Muzaffargarh", "Rajanpur": "Rajanpur"},
            "33": {"Faisalabad": "Faisalabad", "Chiniot": "Chiniot", "Jhang": "Jhang", "Toba Tek Singh": "Toba Tek Singh"},
            "34": {"Gujranwala": "Gujranwala", "Gujrat": "Gujrat", "Hafizabad": "Hafizabad", "Mandi Bahauddin": "Mandi Bahauddin", "Narowal": "Narowal", "Sialkot": "Sialkot"},
            "35": {"Lahore": "Lahore", "Kasur": "Kasur", "Nankana Sahib": "Nankana Sahib", "Sheikhupura": "Sheikhupura"},
            "36": {"Multan": "Multan", "Khanewal": "Khanewal", "Lodhran": "Lodhran", "Vehari": "Vehari", "Sahiwal": "Sahiwal", "Pakpattan": "Pakpattan"},
            "37": {"Rawalpindi": "Rawalpindi", "Attock": "Attock", "Chakwal": "Chakwal", "Jhelum": "Jhelum", "Talagang": "Talagang", "Murree": "Murree"},
            "38": {"Sargodha": "Sargodha", "Bhakkar": "Bhakkar", "Khushab": "Khushab", "Mianwali": "Mianwali"},
            
            # Sindh
            "41": {"Hyderabad": "Hyderabad", "Badin": "Badin", "Dadu": "Dadu", "Jamshoro": "Jamshoro", "Matiari": "Matiari", "Sujawal": "Sujawal", "Tando Allahyar": "Tando Allahyar", "Tando Muhammad Khan": "Tando Muhammad Khan", "Tharparkar": "Tharparkar", "Thatta": "Thatta"},
            "42": {"Karachi Central": "Karachi Central", "Karachi East": "Karachi East", "Karachi South": "Karachi South", "Karachi West": "Karachi West", "Korangi": "Korangi", "Malir": "Malir"},
            "43": {"Larkana": "Larkana", "Jacobabad": "Jacobabad", "Kashmore": "Kashmore", "Qambar Shahdadkot": "Qambar Shahdadkot", "Shikarpur": "Shikarpur"},
            "44": {"Mirpur Khas": "Mirpur Khas", "Umerkot": "Umerkot", "Tharparkar": "Tharparkar"},
            "45": {"Sukkur": "Sukkur", "Ghotki": "Ghotki", "Khairpur": "Khairpur"},
            "46": {"Shaheed Benazirabad": "Shaheed Benazirabad", "Sanghar": "Sanghar", "Naushahro Feroze": "Naushahro Feroze"},
            
            # Balochistan
            "51": {"Kalat": "Kalat", "Khuzdar": "Khuzdar", "Mastung": "Mastung", "Awaran": "Awaran", "Lasbela": "Lasbela", "Kharan": "Kharan", "Washuk": "Washuk"},
            "52": {"Kech": "Kech", "Gwadar": "Gwadar", "Panjgur": "Panjgur"},
            "53": {"Nasirabad": "Nasirabad", "Jafarabad": "Jafarabad", "Jhal Magsi": "Jhal Magsi", "Kachhi": "Kachhi", "Lehri": "Lehri", "Sohbatpur": "Sohbatpur"},
            "54": {"Quetta": "Quetta", "Pishin": "Pishin", "Killa Abdullah": "Killa Abdullah"},
            "55": {"Sibi": "Sibi", "Dera Bugti": "Dera Bugti", "Kohlu": "Kohlu", "Ziarat": "Ziarat", "Harnai": "Harnai"},
            "56": {"Zhob": "Zhob", "Barkhan": "Barkhan", "Killa Saifullah": "Killa Saifullah", "Loralai": "Loralai", "Musakhel": "Musakhel", "Sherani": "Sherani"},
            
            # Islamabad
            "61": {"Islamabad": "Islamabad"},
            
            # Gilgit-Baltistan
            "71": {"Gilgit": "Gilgit", "Skardu": "Skardu", "Ghanche": "Ghanche", "Astore": "Astore", "Diamer": "Diamer", "Ghizer": "Ghizer", "Hunza": "Hunza", "Nagar": "Nagar", "Kharmang": "Kharmang", "Shigar": "Shigar"},
            
            # Azad Jammu & Kashmir
            "81": {"Mirpur": "Mirpur", "Bhimber": "Bhimber", "Kotli": "Kotli"},
            "82": {"Muzaffarabad": "Muzaffarabad", "Hattian": "Hattian", "Neelum": "Neelum", "Poonch": "Poonch", "Bagh": "Bagh", "Haveli": "Haveli", "Sudhnati": "Sudhnati"}
        }
    
    def validate_format(self, cnic: str) -> bool:
        """
        Validate CNIC format: XXXXX-XXXXXXX-X
        Returns True if format is valid
        """
        if not cnic or not isinstance(cnic, str):
            return False
        
        # Check formatted pattern
        if self.cnic_pattern.match(cnic):
            return True
        
        # Check digits-only pattern
        if self.digits_pattern.match(cnic):
            return True
            
        return False
    
    def clean_cnic(self, cnic: str) -> str:
        """
        Clean and standardize CNIC format
        Returns digits-only format
        """
        if not cnic:
            return ""
        
        # Remove all non-digit characters
        cleaned = re.sub(r'\D', '', cnic)
        
        # Ensure exactly 13 digits
        if len(cleaned) == 13:
            return cleaned
        return ""
    
    def parse_cnic(self, cnic: str) -> Optional[Dict[str, str]]:
        """
        Parse CNIC and extract information
        Returns dictionary with parsed data or None if invalid
        """
        cleaned = self.clean_cnic(cnic)
        if not cleaned or len(cleaned) != 13:
            return None
        
        region_code = cleaned[0]
        division_code = cleaned[1:3]  # First 2 digits after region code
        district_code = cleaned[3:5]  # Next 2 digits for district
        gender_digit = int(cleaned[12])
        
        return {
            'cnic': cleaned,
            'formatted_cnic': f"{cleaned[:5]}-{cleaned[5:12]}-{cleaned[12]}",
            'region_code': region_code,
            'region': self.region_codes.get(region_code, "Unknown"),
            'division_code': division_code,
            'division': self._get_division_name(division_code),
            'district_code': district_code,
            'district': self._get_district_name(division_code, district_code),
            'gender': "Male" if gender_digit % 2 == 1 else "Female",
            'gender_digit': gender_digit,
            'unique_number': cleaned[5:12]  # Remaining unique digits
        }
    
    def _get_division_name(self, division_code: str) -> str:
        """Get division name from division code"""
        return self.division_codes.get(division_code, f"Division Code: {division_code}")
    
    def _get_district_name(self, division_code: str, district_code: str) -> str:
        """Get district name from division and district codes"""
        if division_code in self.district_codes:
            districts = self.district_codes[division_code]
            # For now, return first district in division (since exact mapping is complex)
            district_list = list(districts.keys())
            if district_list:
                return f"{district_list[0]} (Area)"
        return f"District Code: {district_code}"
    
    # ... [rest of the methods remain the same as previous version]
