import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from pak_validator import SyntheticCNICGenerator, CNICValidator

class TestSyntheticCNIC(unittest.TestCase):
    
    def setUp(self):
        self.generator = SyntheticCNICGenerator()
        self.validator = CNICValidator()
    
    def test_single_generation(self):
        cnic = self.generator.generate_synthetic_cnic()
        self.assertTrue(self.validator.validate_format(cnic))
    
    def test_generation_with_region(self):
        cnic = self.generator.generate_synthetic_cnic(region='3')
        parsed = self.validator.parse_cnic(cnic)
        self.assertEqual(parsed['region_code'], '3')
        self.assertEqual(parsed['region'], 'Punjab')
    
    def test_generation_with_gender(self):
        # Test male
        cnic_male = self.generator.generate_synthetic_cnic(gender='male')
        parsed_male = self.validator.parse_cnic(cnic_male)
        self.assertEqual(parsed_male['gender'], 'Male')
        
        # Test female
        cnic_female = self.generator.generate_synthetic_cnic(gender='female')
        parsed_female = self.validator.parse_cnic(cnic_female)
        self.assertEqual(parsed_female['gender'], 'Female')
    
    def test_batch_generation(self):
        batch = self.generator.generate_batch(5)
        self.assertEqual(len(batch), 5)
        
        for cnic in batch:
            self.assertTrue(self.validator.validate_format(cnic))

if __name__ == '__main__':
    unittest.main()
