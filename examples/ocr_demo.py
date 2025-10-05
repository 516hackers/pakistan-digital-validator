#!/usr/bin/env python3
"""
OCR Demo for CNIC processing (requires explicit consent)
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from pak_validator import CNICOCR

def demo_ocr_consent_flow():
    print("=== CNIC OCR Demo (Ethical Usage) ===")
    print("This demo shows the consent-required workflow for CNIC OCR processing.")
    print("In real usage, explicit user consent must be obtained.\n")
    
    ocr = CNICOCR()
    
    # Simulate different consent scenarios
    test_cases = [
        {"consent": False, "description": "Without user consent"},
        {"consent": True, "description": "With user consent"}
    ]
    
    for case in test_cases:
        print(f"\n--- {case['description']} ---")
        
        # Simulate processing (in real usage, you would provide an actual image path)
        result = ocr.process_with_consent(
            image_path="dummy_path.jpg",  # Replace with actual image path
            consent_obtained=case['consent']
        )
        
        print(f"Success: {result.get('success', False)}")
        if result.get('success'):
            print(f"CNIC Found: {result['data']['cnic_info']['formatted_cnic']}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            if result.get('consent_required'):
                print("ℹ️  Explicit user consent required for CNIC processing")

if __name__ == "__main__":
    demo_ocr_consent_flow()
