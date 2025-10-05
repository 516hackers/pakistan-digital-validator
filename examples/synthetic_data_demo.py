#!/usr/bin/env python3
"""
Synthetic Data Generation Demo
Generate test CNICs for development and testing
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from pak_validator import SyntheticCNICGenerator, CNICValidator

def demo_synthetic_generation():
    print("=== Synthetic CNIC Generation Demo ===")
    print("Generating test data for development purposes only.\n")
    
    generator = SyntheticCNICGenerator()
    validator = CNICValidator()
    
    # Generate with specific parameters
    print("1. Specific Region and Gender:")
    cnic1 = generator.generate_synthetic_cnic(region='1', gender='male')
    parsed1 = validator.parse_cnic(cnic1)
    print(f"   CNIC: {cnic1}")
    print(f"   Region: {parsed1['region']}, Gender: {parsed1['gender']}")
    
    cnic2 = generator.generate_synthetic_cnic(region='4', gender='female')
    parsed2 = validator.parse_cnic(cnic2)
    print(f"   CNIC: {cnic2}")
    print(f"   Region: {parsed2['region']}, Gender: {parsed2['gender']}")
    
    # Generate batch
    print("\n2. Batch Generation (5 CNICs):")
    batch = generator.generate_batch(5)
    for i, cnic in enumerate(batch, 1):
        parsed = validator.parse_cnic(cnic)
        print(f"   {i}. {cnic} -> {parsed['region']}, {parsed['gender']}")
    
    # Generate for all regions
    print("\n3. One CNIC from each region:")
    regions = ['1', '2', '3', '4', '5', '6', '7']
    for region in regions:
        cnic = generator.generate_synthetic_cnic(region=region)
        parsed = validator.parse_cnic(cnic)
        print(f"   Region {region}: {cnic} -> {parsed['region']}")

if __name__ == "__main__":
    demo_synthetic_generation()
