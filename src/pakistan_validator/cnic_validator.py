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
        self.exact_district_mapping = self._load_exact_district_mapping()
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
            
            # Punjab (3XXXX) - CORRECTED MAPPING
            "31": "Bahawalpur Division",  # Includes Bahawalpur, Bahawalnagar, Rahim Yar Khan
            "32": "Dera Ghazi Khan Division",
            "33": "Faisalabad Division", 
            "34": "Gujranwala Division",
            "35": "Lahore Division",
            "36": "Multan Division",
            "37": "Rawalpindi Division",
            "38": "Sargodha Division",
            
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
            
            # Punjab - CORRECTED
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
    
    def _load_exact_district_mapping(self) -> Dict[str, str]:
        """Load exact district mapping based on first 5 digits"""
        return {
            # Bahawalpur Division (31XXX)
            "31101": "Bahawalpur", "31102": "Bahawalpur", "31103": "Bahawalpur",
            "31201": "Bahawalnagar", "31202": "Bahawalnagar", "31203": "Bahawalnagar", 
            "31301": "Rahim Yar Khan", "31302": "Rahim Yar Khan", "31303": "Rahim Yar Khan", "31304": "Rahim Yar Khan",
            
            # Lahore Division (35XXX)
            "35101": "Lahore", "35102": "Lahore", "35103": "Lahore",
            "35201": "Kasur", "35202": "Kasur", "35203": "Kasur",
            "35301": "Nankana Sahib", "35302": "Nankana Sahib",
            "35401": "Sheikhupura", "35402": "Sheikhupura",
            
            # Rawalpindi Division (37XXX)
            "37101": "Rawalpindi", "37102": "Rawalpindi",
            "37201": "Attock", "37202": "Attock",
            "37301": "Chakwal", "37302": "Chakwal",
            "37401": "Jhelum", "37402": "Jhelum",
            
            # Faisalabad Division (33XXX)
            "33101": "Faisalabad", "33102": "Faisalabad",
            "33201": "Chiniot", "33202": "Chiniot",
            "33301": "Jhang", "33302": "Jhang",
            "33401": "Toba Tek Singh", "33402": "Toba Tek Singh",
            
            # Multan Division (36XXX)
            "36101": "Multan", "36102": "Multan",
            "36201": "Khanewal", "36202": "Khanewal",
            "36301": "Lodhran", "36302": "Lodhran",
            "36401": "Vehari", "36402": "Vehari",
            "36501": "Sahiwal", "36502": "Sahiwal",
            "36601": "Pakpattan", "36602": "Pakpattan",
            
            # Gujranwala Division (34XXX)
            "34101": "Gujranwala", "34102": "Gujranwala",
            "34201": "Gujrat", "34202": "Gujrat",
            "34301": "Hafizabad", "34302": "Hafizabad",
            "34401": "Mandi Bahauddin", "34402": "Mandi Bahauddin",
            "34501": "Narowal", "34502": "Narowal",
            "34601": "Sialkot", "34602": "Sialkot",
            
            # Add more exact mappings as verified
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
        full_district_code = cleaned[1:5]  # Full 4-digit code for exact mapping
        gender_digit = int(cleaned[12])
        
        return {
            'cnic': cleaned,
            'formatted_cnic': f"{cleaned[:5]}-{cleaned[5:12]}-{cleaned[12]}",
            'region_code': region_code,
            'region': self.region_codes.get(region_code, "Unknown"),
            'division_code': division_code,
            'division': self._get_division_name(division_code),
            'district_code': district_code,
            'district': self._get_exact_district_name(full_district_code, division_code, district_code),
            'gender': "Male" if gender_digit % 2 == 1 else "Female",
            'gender_digit': gender_digit,
            'unique_number': cleaned[5:12]  # Remaining unique digits
        }
    
    def _get_division_name(self, division_code: str) -> str:
        """Get division name from division code"""
        return self.division_codes.get(division_code, f"Division Code: {division_code}")
    
    def _get_exact_district_name(self, full_district_code: str, division_code: str, district_code: str) -> str:
        """Get exact district name using full 5-digit code"""
        # Try exact mapping first
        if full_district_code in self.exact_district_mapping:
            return self.exact_district_mapping[full_district_code]
        
        # Fallback to division-based mapping
        if division_code in self.district_codes:
            districts = self.district_codes[division_code]
            district_list = list(districts.keys())
            if district_list:
                return f"{district_list[0]} (Division Area)"
        
        return f"Area Code: {district_code}"
    
    def validate_comprehensive(self, cnic: str) -> Dict:
        """
        Comprehensive validation with detailed results
        """
        result = {
            'is_valid': False,
            'input': cnic,
            'cleaned': None,
            'region': None,
            'division': None,
            'district': None,
            'gender': None,
            'advanced_analysis': {},
            'errors': [],
            'warnings': []
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
        
        # Advanced analysis
        advanced = self._advanced_analysis(cleaned)
        
        result.update({
            'is_valid': True,
            'cleaned': cleaned,
            'formatted': parsed['formatted_cnic'],
            'region': parsed['region'],
            'division': parsed['division'],
            'district': parsed['district'],
            'gender': parsed['gender'],
            'advanced_analysis': advanced,
            'errors': []
        })
        
        return result
    
    def _advanced_analysis(self, cnic: str) -> Dict:
        """
        Perform advanced analysis on CNIC
        """
        analysis = {
            'digit_analysis': self._analyze_digits(cnic),
            'pattern_analysis': self._analyze_patterns(cnic),
            'security_analysis': self._security_checks(cnic),
            'statistical_analysis': self._statistical_analysis(cnic)
        }
        return analysis
    
    def _analyze_digits(self, cnic: str) -> Dict:
        """Analyze digit patterns and sequences"""
        digits = [int(d) for d in cnic]
        
        return {
            'total_digits': len(cnic),
            'digit_sum': sum(digits),
            'even_digits': sum(1 for d in digits if d % 2 == 0),
            'odd_digits': sum(1 for d in digits if d % 2 == 1),
            'repeated_digits': self._count_repeated_digits(cnic),
            'sequential_patterns': self._find_sequential_patterns(cnic),
            'digit_frequency': {str(i): cnic.count(str(i)) for i in range(10) if cnic.count(str(i)) > 0}
        }
    
    def _count_repeated_digits(self, cnic: str) -> List[Dict]:
        """Count repeated digit patterns"""
        repeated = []
        for i in range(10):
            count = cnic.count(str(i))
            if count > 1:
                repeated.append({'digit': i, 'count': count})
        return repeated
    
    def _find_sequential_patterns(self, cnic: str) -> List[str]:
        """Find sequential number patterns"""
        patterns = []
        for i in range(len(cnic) - 2):
            # Check ascending sequence
            if (int(cnic[i]) + 1 == int(cnic[i+1]) and 
                int(cnic[i+1]) + 1 == int(cnic[i+2])):
                patterns.append(f"Ascending: {cnic[i:i+3]}")
            # Check descending sequence
            if (int(cnic[i]) - 1 == int(cnic[i+1]) and 
                int(cnic[i+1]) - 1 == int(cnic[i+2])):
                patterns.append(f"Descending: {cnic[i:i+3]}")
        return patterns
    
    def _analyze_patterns(self, cnic: str) -> Dict:
        """Analyze various patterns in CNIC"""
        return {
            'is_sequential': self._is_sequential(cnic),
            'is_repeating': self._is_repeating_pattern(cnic),
            'palindrome_check': self._is_palindrome(cnic),
            'prime_digits': self._count_prime_digits(cnic)
        }
    
    def _is_sequential(self, cnic: str) -> bool:
        """Check if CNIC has sequential digits"""
        # Check if first 5 digits are sequential
        first_five = cnic[:5]
        return (first_five in ['12345', '54321'] or 
                all(int(first_five[i]) + 1 == int(first_five[i+1]) for i in range(4)))
    
    def _is_repeating_pattern(self, cnic: str) -> bool:
        """Check for repeating digit patterns"""
        return len(set(cnic)) <= 5  # If 5 or fewer unique digits
    
    def _is_palindrome(self, cnic: str) -> bool:
        """Check if CNIC is palindrome"""
        return cnic == cnic[::-1]
    
    def _count_prime_digits(self, cnic: str) -> int:
        """Count prime digits in CNIC"""
        primes = {2, 3, 5, 7}
        return sum(1 for d in cnic if int(d) in primes)
    
    def _security_checks(self, cnic: str) -> Dict:
        """Perform security-related checks"""
        return {
            'suspicious_pattern': self._is_suspicious_pattern(cnic),
            'test_number': self._is_test_number(cnic),
            'common_pattern': self._is_common_pattern(cnic),
            'fake_indicator': self._fake_number_indicators(cnic)
        }
    
    def _is_suspicious_pattern(self, cnic: str) -> bool:
        """Check for suspicious patterns that might indicate fake CNIC"""
        suspicious_patterns = [
            '0000000000000', '1111111111111', '1234567890123',
            '9999999999999', '0123456789012'
        ]
        return cnic in suspicious_patterns or self._is_sequential(cnic)
    
    def _is_test_number(self, cnic: str) -> bool:
        """Check if this might be a test number"""
        # Test numbers often start with specific patterns
        test_patterns = ['00001', '99999', '12345']
        return any(cnic.startswith(pattern) for pattern in test_patterns)
    
    def _is_common_pattern(self, cnic: str) -> bool:
        """Check for common fake CNIC patterns"""
        common_fakes = [
            cnic[0] * 13,  # All same digit
            '1234512345123'  # Repeated pattern
        ]
        return cnic in common_fakes
    
    def _fake_number_indicators(self, cnic: str) -> List[str]:
        """List indicators that might suggest a fake CNIC"""
        indicators = []
        
        if self._is_sequential(cnic):
            indicators.append("Sequential digit pattern")
        if self._is_repeating_pattern(cnic):
            indicators.append("Repeating digit pattern")
        if len(set(cnic)) <= 3:
            indicators.append("Very few unique digits")
        if cnic[:5] in ['00000', '11111', '99999']:
            indicators.append("Suspicious prefix")
            
        return indicators
    
    def _statistical_analysis(self, cnic: str) -> Dict:
        """Perform statistical analysis"""
        return {
            'digit_distribution': self._digit_distribution(cnic),
            'entropy_score': self._calculate_entropy(cnic),
            'randomness_score': self._randomness_score(cnic)
        }
    
    def _digit_distribution(self, cnic: str) -> Dict:
        """Calculate digit distribution"""
        total = len(cnic)
        distribution = {}
        for i in range(10):
            count = cnic.count(str(i))
            if count > 0:
                distribution[str(i)] = {
                    'count': count,
                    'percentage': round((count / total) * 100, 2)
                }
        return distribution
    
    def _calculate_entropy(self, cnic: str) -> float:
        """Calculate entropy of CNIC digits (measure of randomness)"""
        freq = {}
        for digit in cnic:
            freq[digit] = freq.get(digit, 0) + 1
        
        entropy = 0.0
        for count in freq.values():
            p = count / len(cnic)
            entropy -= p * log2(p)
        
        return round(entropy, 4)
    
    def _randomness_score(self, cnic: str) -> float:
        """Calculate randomness score (0-1)"""
        entropy = self._calculate_entropy(cnic)
        max_entropy = 3.3219  # log2(10) for 10 possible digits
        return round(entropy / max_entropy, 4)
    
    def batch_analyze(self, cnics: List[str]) -> Dict:
        """
        Analyze multiple CNICs for patterns and statistics
        """
        valid_count = 0
        regional_distribution = {}
        gender_distribution = {'Male': 0, 'Female': 0}
        advanced_stats = {
            'total_analyzed': len(cnics),
            'valid_cnics': 0,
            'regional_breakdown': {},
            'gender_ratio': {},
            'pattern_analysis': {}
        }
        
        for cnic in cnics:
            result = self.validate_comprehensive(cnic)
            if result['is_valid']:
                valid_count += 1
                region = result['region']
                gender = result['gender']
                
                # Update regional distribution
                regional_distribution[region] = regional_distribution.get(region, 0) + 1
                gender_distribution[gender] = gender_distribution.get(gender, 0) + 1
        
        advanced_stats['valid_cnics'] = valid_count
        advanced_stats['regional_breakdown'] = regional_distribution
        advanced_stats['gender_ratio'] = gender_distribution
        advanced_stats['validity_rate'] = round((valid_count / len(cnics)) * 100, 2) if cnics else 0
        
        return advanced_stats
