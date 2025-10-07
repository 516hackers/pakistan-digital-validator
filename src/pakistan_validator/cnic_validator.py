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
        self.district_codes = self._load_district_codes()
        self.cnic_pattern = re.compile(r'^\d{5}-\d{7}-\d{1}$')
        self.digits_pattern = re.compile(r'^\d{13}$')
    
    def _load_region_codes(self) -> Dict[str, str]:
        """Load region codes from JSON file"""
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'regions.json')
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Extract only region codes, not district mapping
                return {k: v for k, v in data.items() if k not in ['district_mapping', 'advanced_info']}
        except:
            return {
                '1': 'Khyber Pakhtunkhwa', '2': 'FATA', '3': 'Punjab', 
                '4': 'Sindh', '5': 'Balochistan', '6': 'Islamabad', 
                '7': 'Gilgit-Baltistan'
            }
    
    def _load_district_codes(self) -> Dict[str, Dict]:
        """Load advanced district codes"""
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'regions.json')
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('district_mapping', {})
        except:
            return {
                '1': {'01': 'Peshawar', '02': 'Mardan', '03': 'Charsadda', '04': 'Swabi'},
                '3': {'01': 'Lahore', '02': 'Faisalabad', '03': 'Rawalpindi', '04': 'Gujranwala'},
                '4': {'01': 'Karachi East', '02': 'Karachi West', '03': 'Karachi South', '04': 'Karachi Central'},
                '5': {'01': 'Quetta', '02': 'Turbat', '03': 'Khuzdar', '04': 'Chaman'},
                '6': {'01': 'Islamabad'},
                '7': {'01': 'Gilgit', '02': 'Skardu', '03': 'Ghizer', '04': 'Ghanche'}
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
        district_code = cleaned[1:3]  # First 2 digits after region
        gender_digit = int(cleaned[12])
        
        return {
            'cnic': cleaned,
            'formatted_cnic': f"{cleaned[:5]}-{cleaned[5:12]}-{cleaned[12]}",
            'region_code': region_code,
            'region': self.region_codes.get(region_code, "Unknown"),
            'district_code': district_code,
            'district': self._get_district_name(region_code, district_code),
            'gender': "Male" if gender_digit % 2 == 1 else "Female",
            'gender_digit': gender_digit,
            'unique_number': cleaned[3:12]  # Remaining unique digits
        }
    
    def _get_district_name(self, region_code: str, district_code: str) -> str:
        """Get district name from region and district codes"""
        if region_code in self.district_codes:
            districts = self.district_codes[region_code]
            if district_code in districts:
                return districts[district_code]
            else:
                return f"District Code: {district_code}"
        return "Unknown Region"
    
    def validate_comprehensive(self, cnic: str) -> Dict:
        """
        Comprehensive validation with detailed results
        """
        result = {
            'is_valid': False,
            'input': cnic,
            'cleaned': None,
            'region': None,
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
