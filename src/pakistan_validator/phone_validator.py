import re
import phonenumbers
from typing import Dict, Optional

class PhoneValidator:
    """
    Ethical Phone Number Validator for Pakistani numbers
    Provides format validation and basic carrier information
    """
    
    def __init__(self):
        self.pakistan_code = "PK"
        # Major Pakistani mobile prefixes
        self.mobile_prefixes = [
            '300', '301', '302', '303', '304', '305', '306', '307', '308', '309',
            '310', '311', '312', '313', '314', '315', '316', '317', '318', '319',
            '320', '321', '322', '323', '324', '325', '326', '327', '328', '329',
            '330', '331', '332', '333', '334', '335', '336', '337', '338', '339',
            '340', '341', '342', '343', '344', '345', '346', '347', '348', '349'
        ]
    
    def validate_phone(self, phone_number: str) -> Dict:
        """
        Validate Pakistani phone number format
        Returns validation results
        """
        result = {
            'is_valid': False,
            'input': phone_number,
            'formatted': None,
            'carrier_type': None,
            'errors': []
        }
        
        try:
            # Parse with phonenumbers library
            parsed = phonenumbers.parse(phone_number, self.pakistan_code)
            
            if not phonenumbers.is_valid_number_for_region(parsed, self.pakistan_code):
                result['errors'].append("Not a valid Pakistani number")
                return result
            
            # Format the number
            formatted = phonenumbers.format_number(
                parsed, 
                phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )
            
            result['is_valid'] = True
            result['formatted'] = formatted
            result['carrier_type'] = self._get_carrier_type(parsed)
            
        except phonenumbers.NumberParseException as e:
            result['errors'].append(f"Parse error: {str(e)}")
        
        return result
    
    def _get_carrier_type(self, parsed_number) -> str:
        """
        Determine carrier type based on number pattern
        """
        national_number = str(parsed_number.national_number)
        
        # Check if it's a mobile number
        if any(national_number.startswith(prefix) for prefix in self.mobile_prefixes):
            return "Mobile"
        
        # Check for landline patterns (typically starting with specific area codes)
        if len(national_number) >= 2:
            area_code = national_number[:2]
            if area_code in ['21', '42', '51', '61', '71', '81', '91']:
                return "Landline"
        
        return "Unknown"
    
    def get_basic_info(self, phone_number: str) -> Dict:
        """
        Get basic information about phone number (ethical use only)
        """
        validation = self.validate_phone(phone_number)
        
        if not validation['is_valid']:
            return validation
        
        # Add basic geographic info based on area code
        info = validation.copy()
        national_number = str(phonenumbers.parse(phone_number, self.pakistan_code).national_number)
        
        # Basic geographic mapping (simplified)
        area_info = self._get_area_info(national_number)
        info.update(area_info)
        
        return info
    
    def _get_area_info(self, national_number: str) -> Dict:
        """
        Get basic area information based on prefix (ethical use only)
        """
        if len(national_number) < 2:
            return {}
        
        area_codes = {
            '21': 'Karachi',
            '42': 'Lahore', 
            '51': 'Islamabad/Rawalpindi',
            '22': 'Hyderabad',
            '41': 'Faisalabad',
            '61': 'Multan',
            '71': 'Sukkur',
            '81': 'Quetta',
            '91': 'Peshawar'
        }
        
        area_code = national_number[:2]
        if area_code in area_codes:
            return {'area': area_codes[area_code], 'area_code': area_code}
        
        return {'area': 'Unknown', 'area_code': area_code}
