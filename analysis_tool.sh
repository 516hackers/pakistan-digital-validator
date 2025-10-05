#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════╗"
echo "║           PAKISTAN DIGITAL VALIDATOR        ║"
echo "║                516 Hackers                  ║"
echo "╚══════════════════════════════════════════════╝"
echo -e "${NC}"

# Function for CNIC analysis
cnic_analysis() {
    echo -e "\n${CYAN}=== CNIC ANALYSIS TOOL ===${NC}"
    echo -e "${YELLOW}Enter CNIC number (format: XXXXX-XXXXXXX-X):${NC}"
    read -p "CNIC: " cnic_input
    
    python3 << EOF
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pak_validator import CNICValidator
v = CNICValidator()
result = v.validate_comprehensive('$cnic_input')

print('')
print('┌' + '─' * 40 + '┐')
print('│' + 'CNIC ANALYSIS RESULTS'.center(40) + '│')
print('└' + '─' * 40 + '┘')

if result['is_valid']:
    print('✅ Status: VALID')
    print(f'📝 Input: {result["input"]}')
    print(f'🔢 Cleaned: {result["cleaned"]}')
    print(f'📋 Formatted: {result["formatted"]}')
    print(f'🏛️  Region: {result["region"]}')
    print(f'👤 Gender: {result["gender"]}')
else:
    print('❌ Status: INVALID')
    print(f'📝 Input: {result["input"]}')
    print('💡 Errors:')
    for error in result['errors']:
        print(f'   • {error}')
EOF
}

# Function for Phone Number analysis
phone_analysis() {
    echo -e "\n${CYAN}=== PHONE NUMBER ANALYSIS TOOL ===${NC}"
    echo -e "${YELLOW}Enter Phone Number:${NC}"
    read -p "Phone: " phone_input
    
    python3 << EOF
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pak_validator import PhoneValidator
v = PhoneValidator()
result = v.get_basic_info('$phone_input')

print('')
print('┌' + '─' * 40 + '┐')
print('│' + 'PHONE ANALYSIS RESULTS'.center(40) + '│')
print('└' + '─' * 40 + '┘')

if result['is_valid']:
    print('✅ Status: VALID PAKISTANI NUMBER')
    print(f'📝 Input: {result["input"]}')
    print(f'📞 Formatted: {result["formatted"]}')
    print(f'📱 Carrier Type: {result["carrier_type"]}')
    if result.get('area'):
        print(f'📍 Area: {result["area"]}')
    if result.get('area_code'):
        print(f'🔢 Area Code: {result["area_code"]}')
else:
    print('❌ Status: INVALID')
    print(f'📝 Input: {result["input"]}')
    print('💡 Errors:')
    for error in result['errors']:
        print(f'   • {error}')
EOF
}

# Function for batch analysis
batch_analysis() {
    echo -e "\n${CYAN}=== BATCH ANALYSIS ===${NC}"
    echo -e "${YELLOW}Select batch type:${NC}"
    echo "1) Batch CNIC Analysis"
    echo "2) Batch Phone Analysis"
    read -p "Enter choice (1-2): " batch_choice
    
    case $batch_choice in
        1)
            echo -e "\n${YELLOW}Enter CNICs separated by commas:${NC}"
            echo -e "${BLUE}Example: 35201-1234567-8, 41234-5678901-2, 12345${NC}"
            read -p "CNICs: " cnic_list
            
            python3 << EOF
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pak_validator import CNICValidator
v = CNICValidator()
print('')
print('┌' + '─' * 50 + '┐')
print('│' + 'BATCH CNIC ANALYSIS RESULTS'.center(50) + '│')
print('├' + '─' * 50 + '┤')

cnics_list = '$cnic_list'.split(',')
for i, cnic in enumerate(cnics_list, 1):
    cnic = cnic.strip()
    if cnic:
        result = v.validate_comprehensive(cnic)
        status = '✅ VALID' if result['is_valid'] else '❌ INVALID'
        region = result.get('region', 'N/A') if result['is_valid'] else 'N/A'
        gender = result.get('gender', 'N/A') if result['is_valid'] else 'N/A'
        print(f'│ {i:2d}. {cnic:20} {status:12} {region:15} {gender:6} │')

print('└' + '─' * 50 + '┘')
EOF
            ;;
        2)
            echo -e "\n${YELLOW}Enter Phone Numbers separated by commas:${NC}"
            echo -e "${BLUE}Example: +923001234567, 03001234567, 0211234567${NC}"
            read -p "Phones: " phone_list
            
            python3 << EOF
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pak_validator import PhoneValidator
v = PhoneValidator()
print('')
print('┌' + '─' * 60 + '┐')
print('│' + 'BATCH PHONE ANALYSIS RESULTS'.center(60) + '│')
print('├' + '─' * 60 + '┤')

phones_list = '$phone_list'.split(',')
for i, phone in enumerate(phones_list, 1):
    phone = phone.strip()
    if phone:
        result = v.get_basic_info(phone)
        status = '✅ VALID' if result['is_valid'] else '❌ INVALID'
        carrier = result.get('carrier_type', 'N/A') if result['is_valid'] else 'N/A'
        area = result.get('area', 'N/A') if result['is_valid'] else 'N/A'
        print(f'│ {i:2d}. {phone:15} {status:12} {carrier:8} {area:15} │')

print('└' + '─' * 60 + '┘')
EOF
            ;;
        *)
            echo -e "${RED}Invalid choice!${NC}"
            ;;
    esac
}

# Function to generate synthetic test data
synthetic_data() {
    echo -e "\n${CYAN}=== SYNTHETIC TEST DATA GENERATOR ===${NC}"
    
    python3 << EOF
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pak_validator import SyntheticCNICGenerator, CNICValidator

gen = SyntheticCNICGenerator()
val = CNICValidator()

print('Generating synthetic test CNICs...')
print('')
print('┌' + '─' * 50 + '┐')
print('│' + 'SYNTHETIC TEST CNICs (FOR TESTING ONLY)'.center(50) + '│')
print('├' + '─' * 50 + '┤')

# Generate CNICs for all regions
regions = {
    '1': 'KPK',
    '2': 'FATA', 
    '3': 'Punjab',
    '4': 'Sindh',
    '5': 'Balochistan',
    '6': 'Islamabad',
    '7': 'Gilgit-Baltistan'
}

for code, region in regions.items():
    cnic_male = gen.generate_synthetic_cnic(region=code, gender='male')
    cnic_female = gen.generate_synthetic_cnic(region=code, gender='female')
    print(f'│ {region:15} │ {cnic_male:20} │ Male  │')
    print(f'│ {region:15} │ {cnic_female:20} │ Female│')
    if code != '7':
        print('├' + '─' * 50 + '┤')

print('└' + '─' * 50 + '┘')
print('⚠️  These are SYNTHETIC numbers for testing only!')
EOF
}

# Main menu
main_menu() {
    while true; do
        echo -e "\n${PURPLE}=== MAIN MENU ===${NC}"
        echo -e "${GREEN}1) CNIC Analysis${NC}"
        echo -e "${GREEN}2) Phone Number Analysis${NC}"
        echo -e "${GREEN}3) Batch Analysis${NC}"
        echo -e "${GREEN}4) Generate Synthetic Test Data${NC}"
        echo -e "${RED}5) Exit${NC}"
        echo -e "${YELLOW}Select an option (1-5):${NC}"
        
        read -p "Choice: " choice
        
        case $choice in
            1) cnic_analysis ;;
            2) phone_analysis ;;
            3) batch_analysis ;;
            4) synthetic_data ;;
            5) 
                echo -e "${CYAN}Thank you for using Pakistan Digital Validator!${NC}"
                echo -e "${BLUE}Made with ❤️ by 516 Hackers${NC}"
                exit 0 
                ;;
            *) 
                echo -e "${RED}Invalid option! Please select 1-5${NC}"
                ;;
        esac
        
        echo -e "\n${YELLOW}Press Enter to continue...${NC}"
        read
        clear
        echo -e "${CYAN}"
        echo "╔══════════════════════════════════════════════╗"
        echo "║           PAKISTAN DIGITAL VALIDATOR        ║"
        echo "║                516 Hackers                  ║"
        echo "╚══════════════════════════════════════════════╝"
        echo -e "${NC}"
    done
}

# Start the main menu
main_menu
