import json
import os
import re
from typing import Dict, Optional, Tuple

class CNICValidator:
    """
    Ethical CNIC Validator for Pakistani National Identity Cards
    Provides syntactic validation only - no database verification
    """
    
    def __init__(self):
        self.region_codes = self._load_region_codes()
        self.cnic_pattern = re.compile(r'^\d{5}-\d{7}-\d{1}$')
        self.digits_pattern = re.compile(r'^\d{13}$')
    
    def _load_region_codes(self) -> Dict[str, str]:
        """Load region codes from JSON file"""
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'regions.json')
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
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
        gender_digit = int(cleaned[12])
        
        return {
            'cnic': cleaned,
            'formatted_cnic': f"{cleaned[:5]}-{cleaned[5:12]}-{cleaned[12]}",
            'region_code': region_code,
            'region': self.region_codes.get(region_code, "Unknown"),
            'gender': "Male" if gender_digit % 2 == 1 else "Female",
            'gender_digit': gender_digit
        }
    
    def validate_comprehensive(self, cnic: str) -> Dict:
        """
        Comprehensive validation with detailed results
        """
        result = {
            'is_valid': False,
            'input': cnic,
            'cleaned': None,
            'region': None,
            'gender': None,
            'errors': []
        }
        
        if not self.validate_format(cnic):
            result['errors'].append("Invalid CNIC format")
            return result
        
        cleaned = self.clean_cnic(cnic)
        if not cleaned:
            result['errors'].append("Failed to clean CNIC")
            return result
        
        parsed = self.parse_cnic(cleaned)
        if not parsed:
            result['errors'].append("Failed to parse CNIC")
            return result
        
        result.update({
            'is_valid': True,
            'cleaned': cleaned,
            'formatted': parsed['formatted_cnic'],
            'region': parsed['region'],
            'gender': parsed['gender'],
            'errors': []
        })
        
        return result
