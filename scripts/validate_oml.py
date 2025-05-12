#!/usr/bin/env python3
"""
Script to validate OML files against grammar
"""

import os
import sys
import argparse
import glob

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.validation.validator import OMLValidator

def main():
    parser = argparse.ArgumentParser(description='Validate OML files against grammar')
    parser.add_argument('--input', '-i', type=str, help='Input OML file or directory')
    parser.add_argument('--grammar', '-g', type=str, help='Grammar file')
    args = parser.parse_args()
    
    # Check if input exists
    if not args.input:
        print("Error: Please provide an input file or directory")
        return 1
    
    # Create validator
    validator = OMLValidator(args.grammar)
    
    # Get files to validate
    files_to_validate = []
    if os.path.isdir(args.input):
        files_to_validate = glob.glob(os.path.join(args.input, "**/*.oml"), recursive=True)
    elif os.path.isfile(args.input):
        files_to_validate = [args.input]
    else:
        print(f"Error: Input {args.input} does not exist")
        return 1
    
    if not files_to_validate:
        print(f"No OML files found in {args.input}")
        return 1
    
    print(f"Validating {len(files_to_validate)} OML files")
    
    # Validate each file
    success_count = 0
    error_count = 0
    
    for file_path in files_to_validate:
        print(f"Validating {file_path}...")
        
        # Read file content
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Validate content
        is_valid, result = validator.validate(content)
        
        if is_valid:
            print(f"✅ {file_path} is valid")
            success_count += 1
        else:
            print(f"❌ {file_path} is invalid: {result}")
            error_count += 1
    
    print(f"\nValidation complete: {success_count} valid, {error_count} invalid")
    
    return 0 if error_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
