import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from pak_validator import PhoneValidator

class TestPhoneValidator(unittest.TestCase):
    
    def setUp(self):
        self.validator = PhoneValidator()
    
    def test_valid_pakistani_numbers(self):
        valid_numbers = [
            '+923001234567',
            '03001234567',
            '3001234567',
            '+923211234567'
        ]
        
        for number in valid_numbers:
            with self.subTest(number=number):
                result = self.validator.validate_phone(number)
                self.assertTrue(result['is_valid'])
    
    def test_invalid_numbers(self):
        invalid_numbers = [
            '123456789',           # Too short
            '+441234567890',       # UK number
            'abc1234567',          # Non-digits
            '+92300123456789'      # Too long
        ]
        
        for number in invalid_numbers:
            with self.subTest(number=number):
                result = self.validator.validate_phone(number)
                self.assertFalse(result['is_valid'])

if __name__ == '__main__':
    unittest.main()
