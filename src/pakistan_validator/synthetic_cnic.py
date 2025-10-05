import random
from typing import List, Optional

class SyntheticCNICGenerator:
    """
    Generate synthetic CNIC numbers for testing purposes only
    These are valid format but NOT real CNICs
    """
    
    def __init__(self):
        self.region_codes = ['1', '2', '3', '4', '5', '6', '7']
    
    def generate_synthetic_cnic(self, region: Optional[str] = None, 
                              gender: Optional[str] = None) -> str:
        """
        Generate a synthetic CNIC for testing
        """
        # Region code (first digit)
        if region and region in self.region_codes:
            region_code = region
        else:
            region_code = random.choice(self.region_codes)
        
        # Next 4 digits (random)
        middle_four = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        
        # Next 7 digits (random)
        next_seven = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        
        # Gender digit (last digit)
        if gender and gender.lower() == 'female':
            gender_digit = str(random.choice([0, 2, 4, 6, 8]))
        elif gender and gender.lower() == 'male':
            gender_digit = str(random.choice([1, 3, 5, 7, 9]))
        else:
            gender_digit = str(random.randint(0, 9))
        
        cnic_digits = region_code + middle_four + next_seven + gender_digit
        
        # Format: XXXXX-XXXXXXX-X
        return f"{cnic_digits[:5]}-{cnic_digits[5:12]}-{cnic_digits[12]}"
    
    def generate_batch(self, count: int = 10, **kwargs) -> List[str]:
        """
        Generate multiple synthetic CNICs
        """
        return [self.generate_synthetic_cnic(**kwargs) for _ in range(count)]
