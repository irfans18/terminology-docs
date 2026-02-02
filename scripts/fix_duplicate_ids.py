#!/usr/bin/env python3
"""
Fix duplicate IDs in markdown files by appending unique suffixes
"""
import re
import sys
from collections import defaultdict

def fix_duplicate_ids(filepath):
    """Fix duplicate IDs in a markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Track ID occurrences
    id_counts = defaultdict(int)
    id_line_map = defaultdict(list)
    
    # First pass: find all IDs and their line numbers
    for i, line in enumerate(lines):
        # Find {#id} patterns
        matches = re.findall(r'\{#([^}]+)\}', line)
        for id_match in matches:
            id_counts[id_match] += 1
            id_line_map[id_match].append(i)
    
    # Second pass: fix duplicates
    for id_text, count in id_counts.items():
        if count > 1:
            print(f"Fixing duplicate ID: {id_text} (found {count} times)")
            line_numbers = id_line_map[id_text]
            
            # Add suffix to each occurrence
            for idx, line_num in enumerate(line_numbers):
                suffix = idx + 1
                old_id = f"{{#{id_text}}}"
                new_id = f"{{#{id_text}-{suffix}}}"
                lines[line_num] = lines[line_num].replace(old_id, new_id, 1)
                print(f"  Line {line_num + 1}: {old_id} -> {new_id}")
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"\nFixed {filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_duplicate_ids.py <filepath>")
        sys.exit(1)
    
    fix_duplicate_ids(sys.argv[1])
