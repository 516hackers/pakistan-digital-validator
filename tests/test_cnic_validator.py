import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from pak_validator import CNICValidator, SyntheticCNICGenerator

class TestCNICValidator(unittest.TestCase):
    
    def setUp(self):
        self.validator = CNICValidator()
        self.generator = SyntheticCNICGenerator()
    
    def test_valid_formats(self):
        valid_cnics = [
            '12345-6789012-3',
            '35201-1234567-8',
            '41234-5678901-2'
        ]
        
        for cnic in valid_cnics:
            with self.subTest(cnic=cnic):
                self.assertTrue(self.validator.validate_format(cnic))
    
    def test_invalid_formats(self):
        invalid_cnics = [
            '1234-5678901-2',      # Too short
            '123456-789012-3',     # Wrong hyphen placement
            'abcde-fghijkl-m',     # Non-digits
            '12345-6789012-',      # Missing last digit
        ]
        
        for cnic in invalid_cnics:
            with self.subTest(cnic=cnic):
                self.assertFalse(self.validator.validate_format(cnic))
    
    def test_parse_cnic(self):
        cnic = '35201-1234567-8'
        parsed = self.validator.parse_cnic(cnic)
        
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed['region_code'], '3')
        self.assertEqual(parsed['region'], 'Punjab')
        self.assertEqual(parsed['gender'], 'Female')
    
    def test_synthetic_generation(self):
        synthetic = self.generator.generate_synthetic_cnic(region='3', gender='male')
        self.assertTrue(self.validator.validate_format(synthetic))
        
        parsed = self.validator.parse_cnic(synthetic)
        self.assertEqual(parsed['region_code'], '3')
        self.assertEqual(parsed['gender'], 'Male')

if __name__ == '__main__':
    unittest.main()
