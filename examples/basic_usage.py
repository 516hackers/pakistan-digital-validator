#!/usr/bin/env python3
"""
Basic usage examples for Pakistan Digital Validator
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from pak_validator import CNICValidator, PhoneValidator, SyntheticCNICGenerator

def demo_cnic_validation():
    print("=== CNIC Validation Demo ===")
    validator = CNICValidator()
    
    test_cnics = [
        '35201-1234567-8',
        '41234-5678901-2', 
        '12345',  # Invalid
        '35201-1234567-9'  # Valid format
    ]
    
    for cnic in test_cnics:
        result = validator.validate_comprehensive(cnic)
        print(f"\nInput: {cnic}")
        print(f"Valid: {result['is_valid']}")
        if result['is_valid']:
            print(f"Formatted: {result['formatted']}")
            print(f"Region: {result['region']}")
            print(f"Gender: {result['gender']}")
        else:
            print(f"Errors: {result['errors']}")

def demo_phone_validation():
    print("\n=== Phone Validation Demo ===")
    validator = PhoneValidator()
    
    test_numbers = [
        '+923001234567',
        '03001234567',
        '3001234567',
        '12345'  # Invalid
    ]
    
    for number in test_numbers:
        result = validator.validate_phone(number)
        print(f"\nInput: {number}")
        print(f"Valid: {result['is_valid']}")
        if result['is_valid']:
            print(f"Formatted: {result['formatted']}")
            print(f"Carrier: {result['carrier_type']}")

def demo_synthetic_generation():
    print("\n=== Synthetic CNIC Generation Demo ===")
    generator = SyntheticCNICGenerator()
    
    print("Generated CNICs for testing:")
    for i in range(5):
        cnic = generator.generate_synthetic_cnic()
        print(f"  {i+1}. {cnic}")

if __name__ == "__main__":
    demo_cnic_validation()
    demo_phone_validation() 
    demo_synthetic_generation()
