import os
import re
import json

# Configuration
VOL3_DIR = os.path.abspath("src/docs/icd9cmvol3")
INDEX_FILE = os.path.abspath("scripts/icd9_index.json")

def load_index(index_path):
    with open(index_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def link_content(content, code_map, term_map, current_file_path):
    """
    Replaces procedure codes and "see" references with markdown links.
    """
    
    # 1. Link "see" and "see also" references
    
    def replace_term(match):
        full_match = match.group(0)
        prefix = match.group(1) # "see " or "see also "
        term_text = match.group(2)
        
        candidates = [term_text]
        if ',' in term_text:
            candidates.append(term_text.split(',')[0].strip())
            
        target = None
        target_key = None
        
        for cand in candidates:
            key = cand.lower().replace('(', '').replace(')', '').strip()
            if key in term_map:
                target = term_map[key]
                target_key = key
                break
        
        if target:
            # Construct relative path
            target_path = target["path"]
            rel_path = os.path.relpath(target_path, os.path.dirname(current_file_path))
            anchor = target["anchor"]
            
            return f"{prefix}[{term_text}]({rel_path}#{anchor})"
        
        return full_match

    # Pattern: (see also X) or -- see X
    # Captures: 1=prefix, 2=term
    # We look for "see " followed by text until end of line or a digit (start of code) or start of a link '['
    see_pattern = re.compile(r'(see\s+also\s+|see\s+)([^0-9\n\r\[]+?)(?=\s*$|\s+\d|\s+\[)', re.IGNORECASE | re.MULTILINE)
    
    # Apply "see" replacements FIRST
    content = see_pattern.sub(replace_term, content)
    
    # 2. Link Procedure Codes
    
    def replace_code(match):
        code = match.group(1)
        if code in code_map:
            target = code_map[code]
            target_path = target["path"]
            rel_path = os.path.relpath(target_path, os.path.dirname(current_file_path))
            anchor = target["anchor"]
            return f"[{code}]({rel_path}#{anchor})"
        return code

    # Pattern for codes: 2 digits, dot, 1-2 digits. Or just 2 digits.
    # Exclude if preceded by `[`, `]`, `(`, `#` (for anchors), or `_` etc.
    code_pattern = re.compile(r'(?<![\[\]\(\)#\w.\-])(\d{2}\.\d{1,2}|\d{2})(?![\[\]\(\)#\w.\-])')
    
    content = code_pattern.sub(replace_code, content)
    
    return content

def main():
    if not os.path.exists(INDEX_FILE):
        print(f"Index file not found: {INDEX_FILE}")
        return
        
    index = load_index(INDEX_FILE)
    code_map = index["codes"]
    term_map = index["terms"]
    
    print("Linking files in Volume 3...")
    
    for root, dirs, files in os.walk(VOL3_DIR):
        for file in files:
            if file.endswith(".md") and file != "index.md":
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = link_content(content, code_map, term_map, filepath)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {file}")
                else:
                    print(f"No changes for {file}")

if __name__ == "__main__":
    main()
