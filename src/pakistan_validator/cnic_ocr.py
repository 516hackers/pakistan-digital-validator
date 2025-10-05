import cv2
import pytesseract
import re
from typing import Optional, Dict
import numpy as np

class CNICOCR:
    """
    CNIC OCR Processor for authorized use cases only
    Requires explicit user consent and ethical usage
    """
    
    def __init__(self):
        self.validator = CNICValidator()
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess image for better OCR results
        """
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not load image")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Noise removal
        kernel = np.ones((1, 1), np.uint8)
        processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        processed = cv2.medianBlur(processed, 3)
        
        return processed
    
    def extract_text(self, image_path: str) -> str:
        """
        Extract text from CNIC image using Tesseract OCR
        """
        try:
            processed_image = self.preprocess_image(image_path)
            
            # Configure Tesseract for numeric text
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789-'
            
            text = pytesseract.image_to_string(processed_image, config=custom_config)
            return text.strip()
            
        except Exception as e:
            raise Exception(f"OCR processing failed: {str(e)}")
    
    def extract_cnic(self, image_path: str) -> Optional[Dict]:
        """
        Extract and validate CNIC from image
        Returns parsed CNIC info if found and valid
        """
        text = self.extract_text(image_path)
        
        # Look for CNIC patterns in extracted text
        patterns = [
            r'\d{5}-\d{7}-\d{1}',  # Formatted CNIC
            r'\d{13}'              # Digits-only CNIC
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                # Validate the found pattern
                parsed = self.validator.parse_cnic(match)
                if parsed:
                    return {
                        'cnic_info': parsed,
                        'raw_text': text,
                        'matched_pattern': match
                    }
        
        return None
    
    def process_with_consent(self, image_path: str, consent_obtained: bool = False) -> Dict:
        """
        Main processing method that requires explicit consent
        """
        if not consent_obtained:
            return {
                'success': False,
                'error': 'Explicit user consent required for CNIC processing',
                'consent_required': True
            }
        
        try:
            result = self.extract_cnic(image_path)
            if result:
                return {
                    'success': True,
                    'data': result,
                    'consent_obtained': True
                }
            else:
                return {
                    'success': False,
                    'error': 'No valid CNIC found in image',
                    'consent_obtained': True
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'consent_obtained': True
            }
