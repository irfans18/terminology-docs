#!/usr/bin/env python3
"""
Fix all remaining split ICD titles in Chapter 16.

This script handles special cases:
1. Multi-line splits with "(I M)" (with space)
2. Titles split across multiple bullet lines
"""

import re


def fix_multi_line_splits(file_path):
    """Fix multi-line split ICD titles in the file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fixes_count = 0
    
    # Fix case 1: Heading line followed by multi-line continuation ending with "(I M)"
    # Example: ###### 91.3601 ... followed by "- ... \n- from biopsy (I M)"
    pattern1 = r'(######|#####) ([^\n]+)\n\n- ([^\n]+)\n- ([^\n]+) \(I M\)'
    def replace1(m):
        nonlocal fixes_count
        fixes_count += 1
        heading = m.group(1)
        title_part1 = m.group(2)
        title_part2 = m.group(3)
        title_part3 = m.group(4)
        print(f"Fixed multi-line split: {title_part1[:60]}...")
        return f'{heading} {title_part1} {title_part2} {title_part3} (IM)'
    
    content = re.sub(pattern1, replace1, content)
    
    # Fix case 2: Heading line with continuation ending with "(I M)" with spaces
    # Example: ##### 90.194 ... followed by "- for the H uman I mmunodeficiency ... (I M)"
    pattern2 = r'(######|#####) ([^\n]+)\n\n- ([^\n]+) \(I M\)'
    def replace2(m):
        nonlocal fixes_count
        # Only fix if main title doesn't end with (IM) or (I M)
        if not m.group(2).endswith(('(IM)', '(I M)')):
            fixes_count += 1
            heading = m.group(1)
            title_part1 = m.group(2)
            title_part2 = m.group(3)
            print(f"Fixed split with (I M): {title_part1[:60]}...")
            return f'{heading} {title_part1} {title_part2} (IM)'
        return m.group(0)
    
    content = re.sub(pattern2, replace2, content)
    
    # Write back the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return fixes_count


def main():
    file_path = '/Users/irfams/Sites/doc-vitepress/src/docs/icd9cm/chapter-16/index.md'
    
    print(f"Analyzing {file_path} for remaining splits...")
    fixes_count = fix_multi_line_splits(file_path)
    
    print(f"\n✅ Fixed {fixes_count} additional split ICD titles")


if __name__ == '__main__':
    main()
