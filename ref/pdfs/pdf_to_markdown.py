import os
import re
import pdfplumber
from tabulate import tabulate

# Configuration
PDF_DIR = "pdfs"
OUTPUT_DIR = "src/content/docs/icd9cm"
TOC_FILE = os.path.join(PDF_DIR, "toc.md")

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def parse_toc(toc_path):
    """Parses existing toc.md to map chapter numbers to titles."""
    chapters = {}
    if not os.path.exists(toc_path):
        print(f"Warning: TOC file not found at {toc_path}")
        return chapters
    
    with open(toc_path, 'r') as f:
        lines = f.readlines()
        
    # Skip header lines (first 2)
    for line in lines[2:]:
        if not line.strip(): continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 4:
            chap_num = parts[1]
            title = parts[2]
            chapters[chap_num] = title
    return chapters

def clean_text(text):
    """Cleans extracted text."""
    if not text: return ""
    # Remove header/footer noise (simple heuristic)
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        if "ICD-9-CM" in line or line.strip().isdigit(): # specific ICD9 header/footer noise
            continue
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

def extract_content_from_pdf(pdf_path):
    """Extracts text and tables from a single PDF."""
    content_blocks = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 1. Extract tables
            tables = page.extract_tables()
            
            # 2. Extract text (filtering out table areas could be complex, 
            # for now we append text then tables, or just text if no tables)
            # A simple strategy: Extract text, then append tables found on page.
            # Ideally we'd replace table area with table md, but that's hard.
            # Let's try to just extract text and append tables at the bottom of the page content
            # or interleaved if we can map usage.
            # Simplified approach: Text first.
            
            text = page.extract_text()
            cleaned = clean_text(text)
            content_blocks.append(cleaned)
            
            if tables:
                for table in tables:
                     # Filter empty rows/cols
                    clean_table = [[cell.replace('\n', ' ') if cell else '' for cell in row] for row in tables[0]]
                    # Convert to markdown
                    if clean_table:
                        md_table = tabulate(clean_table, headers="firstrow", tablefmt="github")
                        content_blocks.append("\n\n" + md_table + "\n\n")

    return "\n".join(content_blocks)

def process_cross_references(text, chapter_map):
    """
    Detects 'See 35.0', 'See also category 81' etc. and links them.
    Logic:
    1. Find patterns like "See [code]" or "See also [code]".
    2. [code] usually maps to a chapter.
    3. We need a way to know which code belongs to which chapter.
    
    Since we don't have a perfect code-to-chapter map from just reading the PDF text linearly without parsing every code,
    we can try a heuristic or just link to the search if unsure, but strict linking requires a map.
    
    Let's build a simple map from the TOC titles if possible, or just link to the main folder?
    Actually, the TOC titles have ranges: "Operations on the Nervous System (01-05)".
    We can parse these ranges to know which chapter a code belongs to.
    """
    
    def replace_ref(match):
        full_match = match.group(0)
        ref_type = match.group(1) # See or See also
        code = match.group(2)
        
        # Try to find which chapter this code belongs to
        target_chapter = find_chapter_for_code(code, chapter_map)
        if target_chapter:
             return f"[{full_match}](/icd9cm/chapter-{target_chapter.lower().replace(' ', '-')})"
        return full_match

    # This regex is a starting point, might need refinement
    # Matches "See 12.34" or "refer to 01"
    # Assuming codes are digits, maybe dots.
    # Pattern: (See|See also|refer to)\s+category\s+([0-9\.]+)  OR  (See|See also)\s+([0-9\.]+)
    # Let's stick to simple "See [code]" for now
    
    # Not implementing full cross-ref logic in this step without the full code-range map logic ready.
    # I'll implement the map builder helper first.
    return text

def parse_chapter_ranges(chapters_dict):
    """
    Extracts code ranges from chapter titles.
    Format: "Title (XX-YY)" or "Title (XX)"
    Returns list of dicts: {'chapter': '01', 'start': 1, 'end': 5}
    """
    ranges = []
    for chap, title in chapters_dict.items():
        # parsing "(01-05)" or "(00)"
        match = re.search(r'\((\d{2})-?(\d{2})?\)', title)
        if match:
            start = int(match.group(1))
            end = int(match.group(2)) if match.group(2) else start
            ranges.append({'chapter': chap, 'start': start, 'end': end, 'slug': f"chapter-{chap}"})
    return ranges

def find_chapter_for_code(code_str, ranges):
    """Finds chapter slug for a given code (e.g. '35.0' or '01')."""
    try:
        # Take first 2 digits
        parts = code_str.split('.')
        base_code = int(parts[0])
        for r in ranges:
            if r['start'] <= base_code <= r['end']:
                return r['slug']
    except:
        return None
    return None

def main():
    ensure_dir(OUTPUT_DIR)
    
    # 1. Parse TOC
    toc_map = parse_toc(TOC_FILE)
    chapter_ranges = parse_chapter_ranges(toc_map)
    
    # 2. Process PDFs
    pdf_files = sorted([f for f in os.listdir(PDF_DIR) if f.endswith('.pdf')])
    
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}...")
        
        # Determine chapter number from filename or content? 
        # Filenames are like "ICD9_01_chapter_0.pdf" -> chapter 0
        # "ICD9_02_chapter_1.pdf" -> chapter 1
        # Extract "chapter_X" part
        
        match = re.search(r'chapter_([0-9A-Z]+)\.pdf', pdf_file)
        if not match:
            print(f"Skipping {pdf_file} (naming pattern mismatch)")
            continue
            
        chapter_num = match.group(1)
        title = toc_map.get(chapter_num, f"Chapter {chapter_num}")
        
        # Extract content
        raw_content = extract_content_from_pdf(os.path.join(PDF_DIR, pdf_file))
        
        # Post-process content (Cross-refs)
        # Use regex to replace "See X.Y" with links
        # Regex for "See [also] [category] X.Y"
        # We'll just do a simple pass for "See X.Y" or "category X"
        
        def link_replacer(m):
            prefix = m.group(1)
            code = m.group(2)
            slug = find_chapter_for_code(code, chapter_ranges)
            if slug:
                return f"{prefix} [{code}](/icd9cm/{slug})"
            return m.group(0)

        # Regex: (See|See also|excludes)\s+(\d{2}(?:\.\d{1,2})?)
        # Adjust regex to catch more natural language if needed
        processed_content = re.sub(r'(See|See also|Excludes|code)\s+(\d{2}(?:\.\d{1,2})?)', link_replacer, raw_content, flags=re.IGNORECASE)

        
        # Create Frontmatter
        # Ensure 2 digits for order if numeric, but chapter_num can be "3A"
        # Just use file index or try to parse int
        
        frontmatter = f"""---
title: "{title}"
description: "ICD-9-CM Volume 3 Chapter {chapter_num}"
sidebar:
  order: {chapter_num if chapter_num.isdigit() else 999}
---
"""
        
        # Write to MD
        out_filename = f"chapter-{chapter_num}.md"
        with open(os.path.join(OUTPUT_DIR, out_filename), 'w') as f:
            f.write(frontmatter + "\n\n" + processed_content)
            
    # Create Index
    index_content = """---
title: ICD-9-CM Volume 3
description: Procedures and Interventions
sidebar:
  order: 0
---

## Table of Contents

"""
    # use toc_map to build index
    # Sort keys: 0, 1, 2... 3A...
    # Custom sort for 3A etc.
    def sort_key(k):
        if k.isdigit():
            return (int(k), "")
        # Split digits and chars
        m = re.match(r"(\d+)([a-zA-Z]+)", k)
        if m:
            return (int(m.group(1)), m.group(2))
        return (999, k)

    sorted_chapters = sorted(toc_map.keys(), key=sort_key)
    
    for chap in sorted_chapters:
        title = toc_map[chap]
        link = f"chapter-{chap}"
        index_content += f"- [Chapter {chap}: {title}](./{link})\n"

    with open(os.path.join(OUTPUT_DIR, "index.md"), 'w') as f:
        f.write(index_content)

if __name__ == "__main__":
    main()
