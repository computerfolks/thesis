"""
This file contains all functions associated with collecting 'zip codes' from users
"""

import sys
sys.path.append(".")
import json
from descriptors import start_stations_to_zips

def ask_user_for_zip_code_list():
    """
    prompt the user for a zip code list, return raw input

    output:
        raw_zip_code_list_string: raw input provided by the user
    """
    print("Please note that only the following zip codes have bike data available:")
    print(start_stations_to_zips.values())
    raw_zip_code_list_string = input(f"Please enter list of US 5-digit zip codes separated by commas (ex. '12345,54321,77777'). : ")
    return raw_zip_code_list_string


def is_valid_zip_code(raw_zip_code_string):
    """
    ensure that a single string meant to be a zip code is in correct format and is valid
    to be valid, a zip code must be five digits and be a real US zip code

    input:
        raw_zip_code_string: string to be examined
    
    output:
        T/F
    """
    # check for format
    if not raw_zip_code_string.isdigit():
        print(f"Error: {raw_zip_code_string} contains non-numeric characters")
        return False
    
    # check for length
    elif len(raw_zip_code_string) != 5:
        print(f"Error: length must be five, got length {len(raw_zip_code_string)} for zip code {raw_zip_code_string}")
        return False
    
    # open json with valid zip codes
    with open('user/valid_zip_codes.json', 'r') as f:
        valid_zip_codes = json.load(f)

    # check if raw code is in list
    if raw_zip_code_string in valid_zip_codes:
        return True
    
    else:
        print(f"Error: {raw_zip_code_string} is not a valid US zip code")
        return False
    

def is_valid_zip_code_list(raw_zip_code_list):
    """
    loop through a list of zip codes, determine if every zip code is valid

    input:
        zip_code_list: a list of prospective zip codes

    output:
        T/F (false when a single zip code is invalid, true when all are valid)
    """
    for zip_code in raw_zip_code_list:
        if is_valid_zip_code(zip_code) is False:
            return False
    return True
    

def collect_valid_zip_code_list():
    """
    call on other functions, return valid zip code list

    output:
        valid_zip_code_list: a list with valid zip codes
    """
    raw_zip_code_list_string = ask_user_for_zip_code_list()

    # break down raw input by removing whitespace and splitting on commas
    raw_zip_code_list = [x.strip() for x in raw_zip_code_list_string.split(',')]

    # while the zip code list is invalid
    while is_valid_zip_code_list(raw_zip_code_list) is False:
        raw_zip_code_list_string = ask_user_for_zip_code_list()
        raw_zip_code_list = [x.strip() for x in raw_zip_code_list_string.split(',')]

    # return the zip code list when the whole list is valid
    valid_zip_code_list = raw_zip_code_list
    return valid_zip_code_list