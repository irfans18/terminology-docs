#!/usr/bin/env python3
"""
Fix split ICD titles in Chapter 16.

This script identifies and fixes ICD titles that are incorrectly split across
multiple lines, where the ending portion appears on a separate line starting with "- " and ending with "(IM)".

Example of split title to fix:
##### 91.190 Microscopic examination of peritoneal and retroperitoneal specimen, Microscopic ISH
- examination (IM)

Should become:
##### 91.190 Microscopic examination of peritoneal and retroperitoneal specimen, Microscopic ISH examination (IM)
"""

import re
import sys

def fix_split_titles(file_path):
    """Fix split ICD titles in the file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    i = 0
    fixes_count = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a heading line (starts with ####)
        if line.startswith('#####') or line.startswith('######'):
            # Check if the line doesn't end with (IM) and there's a potential continuation
            if not line.rstrip().endswith('(IM)'):
                # Check if the next non-empty line is "- ... (IM)"
                next_idx = i + 1
                
                # Skip empty lines
                while next_idx < len(lines) and lines[next_idx].strip() == '':
                    next_idx += 1
                
                # Check if we found the split pattern: "- ... (IM)"
                if (next_idx < len(lines) and 
                    lines[next_idx].strip().startswith('- ') and
                    lines[next_idx].strip().endswith('(IM)')):
                    
                    # This is a split title - merge them
                    # Extract the continuation part (removing "- " prefix)
                    continuation = lines[next_idx].strip()[2:]  # Remove "- "
                    
                    # Remove trailing newline from current line and add the continuation
                    merged_line = line.rstrip() + ' ' + continuation + '\n'
                    fixed_lines.append(merged_line)
                    
                    # Skip the empty lines and the continuation line
                    i = next_idx + 1
                    fixes_count += 1
                    
                    print(f"Fixed split title at line {i}: {line.strip()[:80]}...")
                else:
                    # Not a split title, keep as is
                    fixed_lines.append(line)
                    i += 1
            else:
                # Line already ends with (IM), keep as is
                fixed_lines.append(line)
                i += 1
        else:
            # Not a heading line, keep as is
            fixed_lines.append(line)
            i += 1
    
    # Write back the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    return fixes_count

def main():
    file_path = '/Users/irfams/Sites/doc-vitepress/src/docs/icd9cm/chapter-16/index.md'
    
    print(f"Analyzing {file_path}...")
    fixes_count = fix_split_titles(file_path)
    
    print(f"\n✅ Fixed {fixes_count} split ICD titles")

if __name__ == '__main__':
    main()
