import re
import glob
import os

# Define the pattern of files to scan
files = glob.glob("/Users/irfams/Sites/doc-vitepress/src/docs/icd9cm/*/index.md")

# Dictionary of replacements
replacements = {
    "f oreign": "foreign",
    "f rom": "from",
    "specif ied": "specified",
    "unspecif ied": "unspecified",
    "superf icial": "superficial",
    "artif icial": "artificial",
    "Transf usion": "Transfusion",
    "transf usion": "transfusion",
    "Inf usion": "Infusion",
    "inf usion": "infusion",
    "f actor": "factor",
    "warf arin": "warfarin",
    "ref itting": "refitting",
    "f ixation": "fixation",
    "classif ied": "classified",
    "perf ormed": "performed",
    "f orm": "form",
    "modif ier": "modifier",
    "interf ace": "interface",
    "ultraf iltration": "ultrafiltration",
    "inf ection": "infection",
    "Inf ection": "Infection",
    "inf ectious": "infectious",
    "af ter": "after",
    "Af ter": "After",
    "surf ace": "surface",
    "def ibrillator": "defibrillator",
    "detoxif ication": "detoxification",
    "f unction": "function",
    "dysf unction": "dysfunction",
    "Bef ore": "Before",
    "f oot": "foot",
    "f aces": "faces",
    "transf er": "transfer",
    "pref erred": "preferred",
    "dif f erent": "different",
    "f ree": "free", # Potential candidate
    "f requency": "frequency", # Potential candidate
    "f emale": "female",
    "f etal": "fetal",
    "f etus": "fetus",
    "f ever": "fever",
    "f ibrosis": "fibrosis",
    "f istula": "fistula",
    "f lap": "flap",
    "f luid": "fluid",
    "f ragment": "fragment",
    "f rozen": "frozen",
    "f usion": "fusion",
    "conf inement": "confinement",
    "def inition": "definition",
    "malf unction": "malfunction",
    "manif estation": "manifestation",
    "perf oration": "perforation",
}

# Regex for "f or" -> "for" (must be preceded by whitespace)
regex_for = r'(?<=\s)f or'

total_files_changed = 0

for file_path in files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    changes_made = False
    
    # 1. Apply generic replacements
    for bad, good in replacements.items():
        if bad in content:
            new_content = content.replace(bad, good)
            if new_content != content:
                # verify it's not partial word replacment if keys are words.
                # but "f rom" is unlikely to be part of "surf rom"? No. 
                # "f rom" has space.
                content = new_content
                changes_made = True
                print(f"[{os.path.basename(os.path.dirname(file_path))}] Replaced '{bad}' with '{good}'")

    # 2. Check "f or"
    if re.search(regex_for, content):
        matches = len(re.findall(regex_for, content))
        content = re.sub(regex_for, 'for', content)
        changes_made = True
        print(f"[{os.path.basename(os.path.dirname(file_path))}] Replaced 'f or' with 'for': {matches} times")

    if changes_made:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        total_files_changed += 1

print(f"Global fix complete. Modified {total_files_changed} files.")
