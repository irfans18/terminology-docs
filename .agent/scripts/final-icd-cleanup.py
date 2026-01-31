#!/usr/bin/env python3
"""
Final cleanup of all ICD title issues in Chapter 16:
1. Fix "(I M)" spacing issues to "(IM)"
2. Fix incomplete "(IM" to "(IM)"
3. Fix remaining split titles
"""

import re


def final_cleanup(file_path):
    """Perform final cleanup of ICD titles."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fixes_count = 0
    
    # Fix 1: Replace "(I M)" with "(IM)" in all headings
    pattern1 = r'(######|#####) (.+?) \(I M\)'
    def replace1(m):
        nonlocal fixes_count
        fixes_count += 1
        return f'{m.group(1)} {m.group(2)} (IM)'
    
    content = re.sub(pattern1, replace1, content)
    
    # Fix 2: Replace incomplete "(IM" with "(IM)" in headings
    pattern2 = r'(######|#####) (.+?) \(IM$'
    def replace2(m):
        nonlocal fixes_count
        fixes_count += 1
        return f'{m.group(1)} {m.group(2)} (IM)'
    
    content = re.sub(pattern2, replace2, content, flags=re.MULTILINE)
    
    # Fix 3: Handle headings ending with comma that have continuation with "- ... (IM)"
    pattern3 = r'(######|#####) ([^\n]+),\n\n- ([^\n]+) \(IM\)'
    def replace3(m):
        nonlocal fixes_count
        fixes_count += 1
        heading = m.group(1)
        title_part1 = m.group(2)
        title_part2 = m.group(3)
        print(f"Fixed trailing comma split: {title_part1[:60]}...")
        return f'{heading} {title_part1}, {title_part2} (IM)'
    
    content = re.sub(pattern3, replace3, content)
    
    # Write back the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return fixes_count


def main():
    file_path = '/Users/irfams/Sites/doc-vitepress/src/docs/icd9cm/chapter-16/index.md'
    
    print(f"Performing final cleanup on {file_path}...")
    fixes_count = final_cleanup(file_path)
    
    print(f"\n✅ Applied {fixes_count} final cleanups")


if __name__ == '__main__':
    main()
