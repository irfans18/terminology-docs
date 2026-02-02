import os
import re
import json

# Configuration
DOCS_DIR = os.path.abspath("src/docs/icd9cm")
VOL3_DIR = os.path.abspath("src/docs/icd9cmvol3")
OUTPUT_FILE = os.path.abspath("scripts/icd9_index.json")

def scan_volume_1(docs_dir):
    """
    Scans Volume 1 (Tabular List) for procedure codes and their anchors.
    Returns a dictionary: {code: {"path": relative_path, "anchor": anchor}}
    """
    code_map = {}
    print(f"Scanning Volume 1 in {docs_dir}...")
    
    # Regex to find headers with codes and anchors
    header_pattern = re.compile(r'^(#+)\s+(\d{2}\.\d{1,2}|\d{2})\s+.*?\{#([a-zA-Z0-9-]+)\}', re.MULTILINE)
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                matches = header_pattern.findall(content)
                for match in matches:
                    level, code, anchor = match
                    code_map[code] = {
                        "path": filepath,
                        "anchor": anchor
                    }
                    
    print(f"Found {len(code_map)} codes in Volume 1.")
    return code_map

def scan_volume_3(vol3_dir):
    """
    Scans Volume 3 (Alphabetic Index) for main terms.
    Adds explicit anchors to headers if missing.
    Returns a dictionary: {term_lower: {"path": filepath, "anchor": anchor, "display": original_term}}
    """
    term_map = {}
    print(f"Scanning Volume 3 in {vol3_dir}...")
    
    # Regex for main terms (headers level 2)
    # ## Abbe operation
    # Check if it already has an anchor: ## Abbe operation {#abbe-operation}
    term_pattern = re.compile(r'^(##)\s+(.*?)\s*(\{#([a-zA-Z0-9-]+)\})?$', re.MULTILINE)
    
    for root, dirs, files in os.walk(vol3_dir):
        for file in files:
            if file.endswith(".md") and file != "index.md":
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                
                # We iterate matches to build the map AND reconstruct content with anchors
                # Using sub is tricky if we want to capture data. 
                # Better to iterate line by line or use a replacement function.
                
                def replace_header(match):
                    level = match.group(1)
                    full_text = match.group(2).strip()
                    existing_anchor = match.group(4)
                    
                    term_clean = full_text
                    # Strip any markdown links if they exist (e.g. if we already ran linker)
                    # "Abdominocentesis [54.91](../...)"
                    # We want the text "Abdominocentesis"
                    
                    # Remove markdown links [text](url) -> text
                    term_clean_no_link = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', term_clean)
                    
                    # Remove code at end
                    term_text = term_clean_no_link
                    code_match = re.search(r'\s+(\d{2}\.\d{1,2}|\d{2}.*?)$', term_clean_no_link)
                    if code_match:
                         term_text = term_clean_no_link[:code_match.start()].strip()
                    
                    key = term_text.lower().replace(',', '').replace('(', '').replace(')', '').strip()
                    # Slug generation
                    slug = re.sub(r'[^a-z0-9]+', '-', key).strip('-')
                    
                    # If we have duplicate slugs in same file? (Unlikely for main terms usually)
                    # But if we process globally, we map key -> anchor.
                    
                    term_map[key] = {
                        "path": filepath,
                        "anchor": slug,
                        "display": term_text,
                        "full_header": term_clean
                    }
                    
                    if existing_anchor:
                        return match.group(0) # Keep as consists
                    else:
                        return f"{level} {full_text} {{#{slug}}}"

                new_content = term_pattern.sub(replace_header, content)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    # print(f"Updated anchors in {file}")
                    
    print(f"Found {len(term_map)} terms in Volume 3.")
    return term_map

def main():
    code_map = scan_volume_1(DOCS_DIR)
    term_map = scan_volume_3(VOL3_DIR)
    
    full_index = {
        "codes": code_map,
        "terms": term_map
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(full_index, f, indent=2)
        
    print(f"Index written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
