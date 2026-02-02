#!/usr/bin/env python3
"""
Fix ALL remaining split ICD titles including:
1. Lines ending with comma followed by "- ... (IM" (incomplete parenthesis)
2. Multi-line splits where (IM) is on its own line
"""

import re


def fix_all_remaining_splits(file_path):
    """Fix all remaining split ICD titles."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fixes_count = 0
    
    # Fix 1: Heading with comma followed by "- ... (IM" (incomplete)
    pattern1 = r'(######|#####) ([^\n]+),\n\n- ([^\n]+) \(IM$'
    def replace1(m):
        nonlocal fixes_count
        fixes_count += 1
        print(f"Fixed incomplete (IM: {m.group(2)[:60]}...")
        return f'{m.group(1)} {m.group(2)}, {m.group(3)} (IM)'
    
    content = re.sub(pattern1, replace1, content, flags=re.MULTILINE)
    
    # Fix 2: Heading with comma/space followed by multi-line "- ...\n- (IM)"
    pattern2 = r'(######|#####) ([^\n]+),?\n\n- ([^\n]+)\n- \(IM\)'
    def replace2(m):
        nonlocal fixes_count
        fixes_count += 1
        print(f"Fixed multi-line with standalone (IM): {m.group(2)[:60]}...")
        return f'{m.group(1)} {m.group(2)}, {m.group(3)} (IM)'
    
    content = re.sub(pattern2, replace2, content)
    
    # Fix 3: Heading with comma/space followed by multi-line "- ...\n- ... (IM)"
    pattern3 = r'(######|#####) ([^\n]+),?\n\n- ([^\n]+)\n- ([^\n]+) \(IM\)'
    def replace3(m):
        nonlocal fixes_count
        fixes_count += 1
        print(f"Fixed two-line continuation: {m.group(2)[:60]}...")
        return f'{m.group(1)} {m.group(2)}, {m.group(3)} {m.group(4)} (IM)'
    
    content = re.sub(pattern3, replace3, content)
    
    # Write back the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return fixes_count


def main():
    file_path = '/Users/irfams/Sites/doc-vitepress/src/docs/icd9cm/chapter-16/index.md'
    
    print(f"Fixing all remaining split titles in {file_path}...")
    fixes_count = fix_all_remaining_splits(file_path)
    
    print(f"\n✅ Fixed {fixes_count} remaining split titles")


if __name__ == '__main__':
    main()
