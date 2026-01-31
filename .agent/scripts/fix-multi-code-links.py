#!/usr/bin/env python3
"""
Script to convert comma-separated ICD-9-CM codes to individual markdown hyperlinks.

Converts patterns like:
  (35.20, 35.22, 35.24, 35.26, 35.28)
To:
  ([35.20](#35-20), [35.22](#35-22), [35.24](#35-24), [35.26](#35-26), [35.28](#35-28))

Also handles code ranges like:
  (36.10-36.99)
To:
  ([36.10](#36-10)-[36.99](#36-99))
"""

import re
import sys
import os

def code_to_link(code):
    """Convert a single code like '35.20' to markdown link '[35.20](#35-20)'"""
    code = code.strip()
    if not code:
        return code
    # Convert code to anchor format (replace . with -)
    anchor = code.replace('.', '-')
    return f'[{code}](#{anchor})'

def process_code_list(match):
    """Process a parenthetical list of codes"""
    content = match.group(1)
    
    # Split by comma
    parts = content.split(',')
    
    processed_parts = []
    for part in parts:
        part = part.strip()
        
        # Check if this part contains a range (e.g., 36.10-36.99)
        range_match = re.match(r'^(\d+\.\d+)-(\d+\.\d+)$', part)
        if range_match:
            start_code = range_match.group(1)
            end_code = range_match.group(2)
            processed_parts.append(f'{code_to_link(start_code)}-{code_to_link(end_code)}')
        elif re.match(r'^\d+\.\d+$', part):
            # Single code
            processed_parts.append(code_to_link(part))
        else:
            # Not a code pattern, keep as-is
            processed_parts.append(part)
    
    return '(' + ', '.join(processed_parts) + ')'

def process_file(filepath):
    """Process a single markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match parentheses containing comma-separated codes
    # Matches: (35.20, 35.22, 35.24) or (35.02, 35.12) etc.
    # But NOT already linked codes like ([35.20](#35-20), ...)
    pattern = r'\((\d+\.\d+(?:\s*,\s*\d+\.\d+(?:-\d+\.\d+)?)+)\)'
    
    # Also match single codes with ranges like (36.10-36.99)
    range_pattern = r'\((\d+\.\d+(?:-\d+\.\d+)?(?:\s*,\s*\d+\.\d+(?:-\d+\.\d+)?)*)\)'
    
    new_content = re.sub(range_pattern, process_code_list, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix-multi-code-links.py <file_or_directory>")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if os.path.isfile(target):
        if process_file(target):
            print(f"Updated: {target}")
        else:
            print(f"No changes: {target}")
    elif os.path.isdir(target):
        for root, dirs, files in os.walk(target):
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    if process_file(filepath):
                        print(f"Updated: {filepath}")
    else:
        print(f"Error: {target} not found")
        sys.exit(1)

if __name__ == '__main__':
    main()
