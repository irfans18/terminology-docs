#!/usr/bin/env python3
"""
Convert ICD-9-CM Volume 3 extracted text files to VitePress-compatible markdown.
Preserves indentation hierarchy using nested lists.
"""

import os
import re
from pathlib import Path

# Mapping of file numbers to letters
FILE_MAP = {
    '01': ('A', 'Abbe operation to Azure'),
    '02': ('B', 'Baffes operation to Bypass'),
    '03': ('C', 'Caldwell operation to Cystourethroscopy'),
    '04': ('D', 'Dacryoadenectomy to Dura'),
    '05': ('E', 'E2F decoy to Extubation'),
    '06': ('F', 'Face lift to Fusion'),
    '07': ('G', 'Gait training to Guthrie'),
    '08': ('H', 'Hagner operation to Hz'),
    '09': ('I', 'IAEMT to Irwin'),
    '10': ('J', 'Jaboulay operation to Jejunopexy'),
    '11': ('K', 'Kangaroo care to Krukenberg'),
    '12': ('L', 'Labbe operation to Lysis'),
    '13': ('M', 'Madlener operation to Myringotomy'),
    '14': ('N', 'Nailing to Nutrition'),
    '15': ('O', 'Ober operation to Ozaki'),
    '16': ('P', 'Pacemaker to Pylorotomy'),
    '17': ('Q', 'Quadrant resection to Quilecea'),
    '18': ('R', 'Rachicentesis to Russe'),
    '19': ('S', 'Sacculotomy to Syme'),
    '20': ('T', 'Taarnhoj operation to Tylectomy'),
    '21': ('U', 'Uchida operation to Utriculotomy'),
    '22': ('V', 'Vaccination to Vulvectomy'),
    '23': ('W', 'Wada test to Wrist'),
    '24': ('X', 'Xenograft to X-ray'),
    '25': ('Y', 'Young operation to Yount'),
    '26': ('Z', 'Zancolli operation to Z-plasty'),
}

def count_leading_spaces(line):
    """Count leading spaces in a line."""
    return len(line) - len(line.lstrip())

def is_page_header(line):
    """Check if line is a page header or page number."""
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith('ICD-9-CM With Indonesian Modification'):
        return True
    if stripped == 'Index to Procedures':
        return True
    if re.match(r'^\d+$', stripped):  # Page numbers
        return True
    if stripped == '\x0c':  # Form feed character
        return True
    return False

def is_section_header(line, letter):
    """Check if line is a section header for the given letter."""
    stripped = line.strip()
    # Match single letter section headers
    return stripped == letter

def find_section_start(lines, letter):
    """Find the index where the actual section for the given letter starts."""
    for i, line in enumerate(lines):
        if is_section_header(line, letter):
            return i + 1  # Start after the section header
    return 0  # If not found, start from beginning

def convert_to_markdown(input_file, output_file, letter, description):
    """Convert a single extracted text file to markdown."""
    with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    
    # Find where the actual section starts
    section_start = find_section_start(lines, letter)
    lines = lines[section_start:]
    
    md_lines = []
    md_lines.append(f'# {letter} - Alphabetic Index\n')
    md_lines.append(f'\n{description}\n\n')
    
    for line in lines:
        # Skip page headers and empty lines
        if is_page_header(line):
            continue
        
        # Remove form feed characters
        line = line.replace('\x0c', '')
        
        # Skip if the line is now empty
        stripped = line.rstrip()
        if not stripped:
            continue
        
        # Count indentation (use spaces)
        indent = count_leading_spaces(line)
        content = stripped.strip()
        
        # Skip empty content
        if not content:
            continue
        
        # Skip single letter section headers for OTHER letters (we may have stray ones)
        if re.match(r'^[A-Z]$', content) and content != letter:
            continue
        
        # Skip the letter section header itself
        if content == letter:
            continue
        
        # Determine hierarchy level based on indentation
        # 0 spaces = main term (## heading)
        # 5+ spaces = sub-term (list item with appropriate depth)
        
        if indent == 0:
            # Main term - use ## heading
            md_lines.append(f'\n## {content}\n')
        else:
            # Sub-term - calculate list depth
            # Typically: 5 spaces = level 1, 10 spaces = level 2, etc.
            depth = max(0, (indent - 1) // 5)
            prefix = '  ' * depth + '- '
            md_lines.append(f'{prefix}{content}\n')
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(md_lines)
    
    print(f'Created: {output_file}')

def main():
    base_dir = Path('/Users/irfams/Sites/doc-vitepress')
    input_dir = base_dir / 'ref/pdfs/vol3/extracted'
    output_dir = base_dir / 'src/docs/icd9cmvol3'
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each file
    for file_num, (letter, description) in FILE_MAP.items():
        input_file = input_dir / f'ICD9_{file_num}_{letter}.txt'
        output_file = output_dir / f'{letter.lower()}.md'
        
        if input_file.exists():
            convert_to_markdown(input_file, output_file, letter, description)
        else:
            print(f'Warning: {input_file} not found')

if __name__ == '__main__':
    main()
