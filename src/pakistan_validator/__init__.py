"""
Pakistan Digital Validator
Ethical toolkit for CNIC and phone number validation
"""

from .cnic_validator import CNICValidator
from .phone_validator import PhoneValidator
from .synthetic_cnic import SyntheticCNICGenerator
from .cnic_ocr import CNICOCR

__version__ = "1.0.0"
__author__ = "516 Hackers"
__all__ = ['CNICValidator', 'PhoneValidator', 'SyntheticCNICGenerator', 'CNICOCR']
