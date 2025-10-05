# Pakistan Digital Validator 🇵🇰

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Ethical](https://img.shields.io/badge/ethical-AI-yellow)
![Security](https://img.shields.io/badge/security-focused-red)
![Team](https://img.shields.io/badge/team-516_Hackers-purple)

A comprehensive, ethical toolkit for Pakistani CNIC and phone number validation. Designed for developers, researchers, and organizations requiring digital identity verification with strong privacy protections.

## 🚀 Features

- **CNIC Validation**: Format validation, region detection, gender identification
- **Phone Validation**: Pakistani number validation with carrier detection  
- **Synthetic Data Generation**: Safe test data generation for development
- **OCR Capabilities**: CNIC extraction from images (with ethical constraints)
- **Privacy-First**: No real data storage, explicit consent requirements
- **Comprehensive Testing**: Full test coverage and validation

## 📋 Requirements

- Python 3.7+
- Tesseract OCR (for OCR functionality)

## 🔧 Installation

### Method 1: PIP Installation
```bash
pip install pakistan-digital-validator
```

### Method 2: Source Installation
```bash
# Clone repository
git clone https://github.com/your-username/pakistan-digital-validator.git
cd pakistan-digital-validator

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Install Tesseract OCR (Required for OCR features)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki) and add to PATH.

## 🛠️ Quick Start

### Basic CNIC Validation
```python
from pak_validator import CNICValidator

validator = CNICValidator()

# Validate CNIC format
result = validator.validate_comprehensive('35201-1234567-8')
print(f"Valid: {result['is_valid']}")
print(f"Region: {result['region']}")
print(f"Gender: {result['gender']}")
```

### Phone Number Validation
```python
from pak_validator import PhoneValidator

validator = PhoneValidator()

# Validate phone number
result = validator.get_basic_info('+923001234567')
print(f"Valid: {result['is_valid']}")
print(f"Carrier: {result['carrier_type']}")
print(f"Area: {result['area']}")
```

## 📚 Comprehensive Usage Guide

### 1. CNIC Validation

```python
from pak_validator import CNICValidator

validator = CNICValidator()

# Various validation methods
cnic = '35201-1234567-8'

# Basic format validation
is_valid = validator.validate_format(cnic)

# Comprehensive validation with details
details = validator.validate_comprehensive(cnic)

# Parse CNIC information
parsed = validator.parse_cnic(cnic)

# Clean and standardize format
cleaned = validator.clean_cnic(cnic)
```

### 2. Phone Number Analysis

```python
from pak_validator import PhoneValidator

validator = PhoneValidator()

# Basic validation
result = validator.validate_phone('03001234567')

# Get comprehensive information
info = validator.get_basic_info('+923001234567')

# Batch processing
numbers = ['03001234567', '0211234567', '3001234567']
for num in numbers:
    result = validator.get_basic_info(num)
    print(f"{num}: {result['carrier_type']} - {result.get('area', 'N/A')}")
```

### 3. Synthetic Data Generation

```python
from pak_validator import SyntheticCNICGenerator

generator = SyntheticCNICGenerator()

# Generate single synthetic CNIC
test_cnic = generator.generate_synthetic_cnic(region='3', gender='male')

# Generate batch for testing
batch = generator.generate_batch(10, region='4', gender='female')

# All regions example
regions = ['1', '2', '3', '4', '5', '6', '7']
for region in regions:
    cnic = generator.generate_synthetic_cnic(region=region)
    print(f"Region {region}: {cnic}")
```

### 4. Ethical OCR Processing

```python
from pak_validator import CNICOCR

ocr = CNICOCR()

# Process with explicit consent (REQUIRED)
result = ocr.process_with_consent(
    image_path="cnic_image.jpg",
    consent_obtained=True  # Must be explicitly set to True
)

if result['success']:
    cnic_info = result['data']['cnic_info']
    print(f"Extracted CNIC: {cnic_info['formatted_cnic']}")
else:
    print(f"Error: {result['error']}")
```

## 🧪 Testing

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Test Modules
```bash
python -m pytest tests/test_cnic_validator.py
python -m pytest tests/test_phone_validator.py
python -m pytest tests/test_synthetic_cnic.py
```

### Test with Coverage
```bash
python -m pytest --cov=src.pak_validator tests/
```

## 📋 Example Outputs

### CNIC Validation Output
```json
{
  "is_valid": true,
  "input": "35201-1234567-8",
  "cleaned": "3520112345678",
  "formatted": "35201-1234567-8",
  "region": "Punjab",
  "gender": "Female",
  "errors": []
}
```

### Phone Validation Output
```json
{
  "is_valid": true,
  "input": "+923001234567",
  "formatted": "+92 300 1234567",
  "carrier_type": "Mobile",
  "area": "Unknown",
  "area_code": "300",
  "errors": []
}
```

## 🔒 Ethical Usage Guidelines

### Required Practices
- ✅ Obtain explicit user consent before processing personal data
- ✅ Use synthetic data for testing and development
- ✅ Implement proper data encryption and security measures
- ✅ Follow Pakistan's data protection regulations
- ✅ Provide clear opt-out mechanisms

### Prohibited Practices
- ❌ Processing without explicit consent
- ❌ Storing real CNIC numbers unnecessarily
- ❌ Using for unauthorized identity verification
- ❌ Sharing personal data with third parties without consent
- ❌ Using synthetic data as real identifiers

## 🏗️ Project Structure

```
pakistan-digital-validator/
├── src/
│   └── pak_validator/
│       ├── __init__.py
│       ├── cnic_validator.py      # CNIC validation logic
│       ├── phone_validator.py     # Phone validation logic
│       ├── synthetic_cnic.py      # Test data generation
│       ├── cnic_ocr.py           # OCR processing (ethical)
│       └── data/
│           └── regions.json      # Region code mappings
├── tests/                        # Comprehensive test suite
├── examples/                     # Usage examples
├── requirements.txt              # Dependencies
└── setup.py                     # Package configuration
```

## 🚨 Legal Disclaimer

This software is provided for educational and authorized business purposes only. Users are solely responsible for:

- Complying with Pakistan's NADRA regulations and data protection laws
- Obtaining proper user consent for data processing
- Implementing appropriate security measures
- Ensuring ethical usage in all applications

The developers are not liable for misuse or unauthorized applications of this software.

## 🤝 Contributing

We welcome contributions from the community! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/your-username/pakistan-digital-validator.git
cd pakistan-digital-validator
pip install -r requirements.txt
pip install -e .
python -m pytest  # Run tests before contributing
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

**516 Hackers** - Building ethical AI solutions for Pakistan's digital ecosystem.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the examples directory for usage patterns
- Review the test cases for implementation examples

## 🔄 Version History

- **1.0.0** - Initial release with CNIC validation, phone validation, OCR, and synthetic data generation

---

**Note**: Always prioritize user privacy and obtain explicit consent when handling personal identification data.
