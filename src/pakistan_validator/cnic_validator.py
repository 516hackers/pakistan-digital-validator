import json
import os
import re
from typing import Dict, Optional, List
from datetime import datetime
from math import log2

class CNICValidator:
    """
    Advanced CNIC Validator with Deep Temporal Analysis
    Provides comprehensive validation and time-based insights
    """
    
    def __init__(self):
        self.region_codes = self._load_region_codes()
        self.division_codes = self._load_division_codes()
        self.exact_district_mapping = self._load_exact_district_mapping()
        self.cnic_pattern = re.compile(r'^\d{5}-\d{7}-\d{1}$')
        self.digits_pattern = re.compile(r'^\d{13}$')
        
        # Temporal analysis data
        self.issue_year_ranges = self._load_issue_year_ranges()
        self.generation_patterns = self._load_generation_patterns()
    
    def _load_region_codes(self) -> Dict[str, str]:
        """Load region codes from JSON file"""
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'regions.json')
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('region_codes', {})
        except:
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
        """Load division codes from JSON file"""
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'regions.json')
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('division_codes', {})
        except:
            return {
                "11": "Bannu Division", "12": "Dera Ismail Khan Division", "13": "Hazara Division",
                "14": "Kohat Division", "15": "Malakand Division", "16": "Mardan Division", "17": "Peshawar Division",
                "21": "FATA Region",
                "31": "Bahawalpur Division", "32": "Dera Ghazi Khan Division", "33": "Faisalabad Division",
                "34": "Gujranwala Division", "35": "Lahore Division", "36": "Multan Division",
                "37": "Rawalpindi Division", "38": "Sargodha Division",
                "41": "Hyderabad Division", "42": "Karachi Division", "43": "Larkana Division",
                "44": "Mirpur Khas Division", "45": "Sukkur Division", "46": "Shaheed Benazirabad Division",
                "51": "Kalat Division", "52": "Makran Division", "53": "Nasirabad Division",
                "54": "Quetta Division", "55": "Sibi Division", "56": "Zhob Division",
                "61": "Islamabad", "71": "Gilgit Division", "81": "Mirpur Division", "82": "Muzaffarabad Division"
            }
    
    def _load_exact_district_mapping(self) -> Dict[str, str]:
        """Load exact district mapping from JSON file"""
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'regions.json')
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('exact_district_mapping', {})
        except:
            return {
                "31304": "Rahim Yar Khan",
                "35101": "Lahore",
                "37101": "Rawalpindi"
            }
    
    def _load_issue_year_ranges(self) -> Dict[str, Dict]:
        """Load CNIC series to issue year mapping"""
        return {
            "31100": {"start_year": 1990, "end_year": 1995, "era": "Early 90s"},
            "31200": {"start_year": 1995, "end_year": 2000, "era": "Late 90s"},
            "31300": {"start_year": 2000, "end_year": 2005, "era": "Early 2000s"},
            "31400": {"start_year": 2005, "end_year": 2010, "era": "Late 2000s"},
            "31500": {"start_year": 2010, "end_year": 2015, "era": "Early 2010s"},
            "31600": {"start_year": 2015, "end_year": 2020, "era": "Late 2010s"},
            "31700": {"start_year": 2020, "end_year": 2025, "era": "2020s"},
            "35100": {"start_year": 1992, "end_year": 1998, "era": "Mid 90s"},
            "37100": {"start_year": 1993, "end_year": 1999, "era": "Mid-Late 90s"},
            "33100": {"start_year": 1994, "end_year": 2000, "era": "Late 90s"},
        }
    
    def _load_generation_patterns(self) -> Dict[str, Dict]:
        """Load generation analysis patterns"""
        return {
            "pre_2000": {
                "description": "Pre-2000 Generation",
                "years": [1990, 1999],
                "characteristics": ["Low digit entropy", "Sequential patterns", "Regional concentration"]
            },
            "2000_2010": {
                "description": "2000s Generation", 
                "years": [2000, 2010],
                "characteristics": ["Medium digit entropy", "Mixed patterns", "Urban expansion"]
            },
            "post_2010": {
                "description": "Post-2010 Generation",
                "years": [2011, 2025],
                "characteristics": ["High digit entropy", "Random patterns", "National distribution"]
            }
        }
    
    def validate_format(self, cnic: str) -> bool:
        """Validate CNIC format: XXXXX-XXXXXXX-X"""
        if not cnic or not isinstance(cnic, str):
            return False
        
        if self.cnic_pattern.match(cnic):
            return True
        
        if self.digits_pattern.match(cnic):
            return True
            
        return False
    
    def clean_cnic(self, cnic: str) -> str:
        """Clean and standardize CNIC format"""
        if not cnic:
            return ""
        
        cleaned = re.sub(r'\D', '', cnic)
        
        if len(cleaned) == 13:
            return cleaned
        return ""
    
    def parse_cnic(self, cnic: str) -> Optional[Dict[str, str]]:
        """Parse CNIC and extract information"""
        cleaned = self.clean_cnic(cnic)
        if not cleaned or len(cleaned) != 13:
            return None
        
        region_code = cleaned[0]
        division_code = cleaned[1:3]
        district_code = cleaned[3:5]
        full_5_digit_code = cleaned[:5]
        gender_digit = int(cleaned[12])
        
        return {
            'cnic': cleaned,
            'formatted_cnic': f"{cleaned[:5]}-{cleaned[5:12]}-{cleaned[12]}",
            'region_code': region_code,
            'region': self.region_codes.get(region_code, "Unknown"),
            'division_code': division_code,
            'division': self._get_division_name(division_code),
            'district_code': district_code,
            'district': self._get_exact_district_name(full_5_digit_code),
            'gender': "Male" if gender_digit % 2 == 1 else "Female",
            'gender_digit': gender_digit,
            'unique_number': cleaned[5:12]
        }
    
    def _get_division_name(self, division_code: str) -> str:
        """Get division name from division code"""
        return self.division_codes.get(division_code, f"Division Code: {division_code}")
    
    def _get_exact_district_name(self, full_5_digit_code: str) -> str:
        """Get exact district name using full 5-digit code"""
        return self.exact_district_mapping.get(full_5_digit_code, f"District Code: {full_5_digit_code[3:5]}")
    
    def validate_comprehensive(self, cnic: str) -> Dict:
        """Comprehensive validation with detailed results"""
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
        """Perform advanced analysis on CNIC"""
        return {
            'digit_analysis': self._analyze_digits(cnic),
            'pattern_analysis': self._analyze_patterns(cnic),
            'security_analysis': self._security_checks(cnic),
            'statistical_analysis': self._statistical_analysis(cnic),
            'temporal_analysis': self._temporal_analysis(cnic)
        }
    
    def _temporal_analysis(self, cnic: str) -> Dict:
        """Perform deep temporal analysis on CNIC"""
        return {
            'age_estimation': self._estimate_age(cnic),
            'issue_date_prediction': self._predict_issue_date(cnic),
            'generation_analysis': self._analyze_generation(cnic),
            'series_analysis': self._analyze_series(cnic),
            'temporal_patterns': self._detect_temporal_patterns(cnic)
        }
    
    def _estimate_age(self, cnic: str) -> Dict:
        """Estimate age based on CNIC series and patterns"""
        first_five = cnic[:5]
        current_year = datetime.now().year
        
        issue_info = self._get_issue_year_info(first_five)
        estimated_issue_year = issue_info.get('estimated_year', 2000)
        
        min_age = current_year - issue_info.get('end_year', 2000)
        max_age = current_year - issue_info.get('start_year', 1990)
        likely_age = current_year - estimated_issue_year
        
        if likely_age < 18:
            age_group = "Under 18"
        elif likely_age < 25:
            age_group = "Young Adult (18-24)"
        elif likely_age < 35:
            age_group = "Adult (25-34)" 
        elif likely_age < 50:
            age_group = "Middle Age (35-49)"
        else:
            age_group = "Senior (50+)"
        
        return {
            'estimated_issue_year': estimated_issue_year,
            'current_year': current_year,
            'estimated_age': likely_age,
            'age_range': f"{min_age}-{max_age} years",
            'age_group': age_group,
            'confidence': self._calculate_age_confidence(first_five),
            'era': issue_info.get('era', 'Unknown')
        }
    
    def _get_issue_year_info(self, first_five: str) -> Dict:
        """Get issue year information based on CNIC series"""
        series_key = first_five[:4] + "0"
        if series_key in self.issue_year_ranges:
            info = self.issue_year_ranges[series_key]
            estimated_year = (info['start_year'] + info['end_year']) // 2
            return {
                'start_year': info['start_year'],
                'end_year': info['end_year'],
                'estimated_year': estimated_year,
                'era': info['era']
            }
        
        region_code = first_five[0]
        division_code = first_five[1:3]
        
        if region_code == '3':
            if division_code in ['31', '32']:
                base_year = 1995
            elif division_code in ['33', '34']:
                base_year = 1998
            elif division_code in ['35', '36']:
                base_year = 2000
            else:
                base_year = 2002
        else:
            base_year = 2000
        
        last_digits = int(first_five[3:5])
        year_offset = last_digits // 5
        
        estimated_year = base_year + year_offset
        estimated_year = max(1990, min(2025, estimated_year))
        
        return {
            'start_year': estimated_year - 5,
            'end_year': estimated_year + 5,
            'estimated_year': estimated_year,
            'era': self._get_era_from_year(estimated_year)
        }
    
    def _get_era_from_year(self, year: int) -> str:
        """Convert year to era description"""
        if year < 1995:
            return "Early NADRA Era"
        elif year < 2000:
            return "Pre-2000 Era"
        elif year < 2005:
            return "Early Digital Era"
        elif year < 2010:
            return "Mid Digital Era"
        elif year < 2015:
            return "Smart CNIC Era"
        else:
            return "Recent Era"
    
    def _calculate_age_confidence(self, first_five: str) -> float:
        """Calculate confidence level for age estimation"""
        series_key = first_five[:4] + "0"
        if series_key in self.issue_year_ranges:
            return 0.85
        
        region_code = first_five[0]
        if region_code in ['3', '4']:
            return 0.70
        else:
            return 0.60
    
    def _predict_issue_date(self, cnic: str) -> Dict:
        """Predict issue date based on CNIC patterns"""
        first_five = cnic[:5]
        issue_info = self._get_issue_year_info(first_five)
        estimated_year = issue_info['estimated_year']
        
        last_digits = int(cnic[3:5])
        estimated_month = (last_digits % 12) + 1
        
        if estimated_month in [12, 1]:
            estimated_month = 3
        
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        
        issue_date = datetime(estimated_year, estimated_month, 15)
        current_date = datetime.now()
        days_since_issue = (current_date - issue_date).days
        years_since_issue = days_since_issue / 365.25
        
        return {
            'estimated_issue_year': estimated_year,
            'estimated_issue_month': month_names[estimated_month - 1],
            'estimated_issue_date': f"{month_names[estimated_month - 1]} {estimated_year}",
            'days_since_issue': int(days_since_issue),
            'years_since_issue': round(years_since_issue, 1),
            'issue_era': issue_info['era'],
            'confidence_level': f"{self._calculate_age_confidence(first_five) * 100:.1f}%"
        }
    
    def _analyze_generation(self, cnic: str) -> Dict:
        """Analyze which generation the CNIC belongs to"""
        first_five = cnic[:5]
        issue_info = self._get_issue_year_info(first_five)
        issue_year = issue_info['estimated_year']
        
        if issue_year < 2000:
            generation = "pre_2000"
        elif issue_year < 2010:
            generation = "2000_2010"
        else:
            generation = "post_2010"
        
        gen_info = self.generation_patterns[generation]
        
        digit_entropy = self._calculate_entropy(cnic)
        if digit_entropy < 2.5:
            tech_era = "Early Computerization"
        elif digit_entropy < 3.0:
            tech_era = "Digital Transition" 
        else:
            tech_era = "Modern Digital"
        
        return {
            'generation': gen_info['description'],
            'issue_period': f"{gen_info['years'][0]}-{gen_info['years'][1]}",
            'characteristics': gen_info['characteristics'],
            'technology_era': tech_era,
            'estimated_issue_year': issue_year,
            'digit_complexity': "Low" if digit_entropy < 2.5 else "Medium" if digit_entropy < 3.0 else "High"
        }
    
    def _analyze_series(self, cnic: str) -> Dict:
        """Analyze CNIC series for temporal patterns"""
        first_five = cnic[:5]
        region_code = cnic[0]
        division_code = cnic[1:3]
        
        series_number = int(first_five)
        
        if series_number < 20000:
            series_type = "Early Series"
        elif series_number < 40000:
            series_type = "Mid Series"
        else:
            series_type = "Recent Series"
        
        if region_code == '3':
            if division_code in ['31', '32']:
                region_development = "Early Developed"
            elif division_code in ['35', '36']:
                region_development = "Rapid Development"
            else:
                region_development = "Steady Development"
        else:
            region_development = "Standard Development"
        
        return {
            'series_type': series_type,
            'series_number': series_number,
            'regional_development_phase': region_development,
            'is_early_series': series_number < 25000,
            'is_recent_series': series_number > 45000,
            'progression_level': self._calculate_series_progression(series_number)
        }
    
    def _calculate_series_progression(self, series_number: int) -> str:
        """Calculate how far along the series progression"""
        if series_number < 15000:
            return "Very Early (1-15k)"
        elif series_number < 30000:
            return "Early Phase (15-30k)"
        elif series_number < 45000:
            return "Mid Phase (30-45k)"
        else:
            return "Recent Phase (45k+)"
    
    def _detect_temporal_patterns(self, cnic: str) -> Dict:
        """Detect temporal patterns in CNIC"""
        patterns = []
        
        first_five = cnic[:5]
        if self._is_sequential_issuance(first_five):
            patterns.append("Sequential issuance pattern")
        
        digit_entropy = self._calculate_entropy(cnic)
        if digit_entropy < 2.3:
            patterns.append("Low entropy - possible early issuance")
        elif digit_entropy > 3.1:
            patterns.append("High entropy - likely recent issuance")
        
        region_code = cnic[0]
        if region_code in ['1', '2'] and int(cnic[1:3]) < 20:
            patterns.append("Early KPK/FATA pattern")
        
        return {
            'detected_patterns': patterns,
            'temporal_consistency': self._check_temporal_consistency(cnic),
            'issuance_likelihood': self._calculate_issuance_likelihood(cnic),
            'historical_context': self._get_historical_context(cnic)
        }
    
    def _is_sequential_issuance(self, first_five: str) -> bool:
        """Check if CNIC shows sequential issuance pattern"""
        digits = [int(d) for d in first_five]
        
        sequential_count = 0
        for i in range(len(digits) - 1):
            if abs(digits[i] - digits[i+1]) == 1:
                sequential_count += 1
        
        return sequential_count >= 2
    
    def _check_temporal_consistency(self, cnic: str) -> str:
        """Check if CNIC shows temporal consistency"""
        first_five = cnic[:5]
        series_number = int(first_five)
        digit_entropy = self._calculate_entropy(cnic)
        
        if series_number < 20000 and digit_entropy > 2.8:
            return "Inconsistent - Early series with high entropy"
        elif series_number > 40000 and digit_entropy < 2.4:
            return "Inconsistent - Recent series with low entropy"
        else:
            return "Consistent - Matches expected temporal patterns"
    
    def _calculate_issuance_likelihood(self, cnic: str) -> str:
        """Calculate likelihood of issuance period"""
        first_five = cnic[:5]
        series_number = int(first_five)
        
        if series_number < 15000:
            return "Very High - Classic early pattern"
        elif series_number < 30000:
            return "High - Established pattern"
        elif series_number < 45000:
            return "Medium - Transitional pattern"
        else:
            return "High - Modern pattern"
    
    def _get_historical_context(self, cnic: str) -> str:
        """Get historical context for CNIC issuance"""
        first_five = cnic[:5]
        issue_info = self._get_issue_year_info(first_five)
        issue_year = issue_info['estimated_year']
        
        historical_events = {
            1990: "Early NADRA computerization begins",
            1995: "Widespread CNIC digitization",
            2000: "Massive CNIC drive for new millennium", 
            2005: "Enhanced security features introduced",
            2010: "Smart CNIC program launched",
            2015: "Biometric verification expansion",
            2020: "Digital NADRA initiatives"
        }
        
        closest_year = min(historical_events.keys(), key=lambda x: abs(x - issue_year))
        return f"Issued around {historical_events[closest_year]}"
    
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
            if (int(cnic[i]) + 1 == int(cnic[i+1]) and 
                int(cnic[i+1]) + 1 == int(cnic[i+2])):
                patterns.append(f"Ascending: {cnic[i:i+3]}")
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
        first_five = cnic[:5]
        return (first_five in ['12345', '54321'] or 
                all(int(first_five[i]) + 1 == int(first_five[i+1]) for i in range(4)))
    
    def _is_repeating_pattern(self, cnic: str) -> bool:
        """Check for repeating digit patterns"""
        return len(set(cnic)) <= 5
    
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
        test_patterns = ['00001', '99999', '12345']
        return any(cnic.startswith(pattern) for pattern in test_patterns)
    
    def _is_common_pattern(self, cnic: str) -> bool:
        """Check for common fake CNIC patterns"""
        common_fakes = [
            cnic[0] * 13,
            '1234512345123'
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
        max_entropy = 3.3219
        return round(entropy / max_entropy, 4)
    
    def batch_analyze(self, cnics: List[str]) -> Dict:
        """Analyze multiple CNICs for patterns and statistics"""
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
                
                regional_distribution[region] = regional_distribution.get(region, 0) + 1
                gender_distribution[gender] = gender_distribution.get(gender, 0) + 1
        
        advanced_stats['valid_cnics'] = valid_count
        advanced_stats['regional_breakdown'] = regional_distribution
        advanced_stats['gender_ratio'] = gender_distribution
        advanced_stats['validity_rate'] = round((valid_count / len(cnics)) * 100, 2) if cnics else 0
        
        return advanced_stats
