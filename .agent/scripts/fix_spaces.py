import re

file_path = "/Users/irfams/Sites/doc-vitepress/src/docs/icd9cm/chapter-16/index.md"

# 1. Exact string replacements (Safe because likely unique)
# Note: "f or" is NOT in this list.
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
    "f er": "fer", # "f er" might be dangerous? "Pref erred" -> "Preferred". "Transf er" -> "Transfer". "f er" -> "fer" (standalone?). 
                   # "f er" -> "fer"? "of er"? "offer"? "of er". 
                   # "f er" matches "of er" (of errors). "offer" -> "o ff er". No. "o f f e r".
                   # "of errors". "o f e r r o r s". "f" " " "e" "r". Matches.
                   # "of errors" -> "oferrors". BAD.
                   # So I should NOT replace "f er" blindly.
                   # I will replace "f er" only if I know the word.
                   # "transf er" -> "transfer".
                   # "pref erred" -> "preferred".
                   # I'll remove "f er" from the generic list and add specific ones.
}

specific_replacements = {
    "transf er": "transfer",
    "pref erred": "preferred",
    "dif f erent": "different", # just in case
}

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

original_content = content

# Apply generic replacements
for bad, good in replacements.items():
    if bad == "f er": continue # Skip the dangerous one
    new_content = content.replace(bad, good)
    if new_content != content:
        cnt = content.count(bad)
        print(f"Replaced '{bad}' with '{good}': {cnt} times")
        content = new_content

for bad, good in specific_replacements.items():
    new_content = content.replace(bad, good)
    if new_content != content:
        cnt = content.count(bad)
        print(f"Replaced '{bad}' with '{good}': {cnt} times")
        content = new_content


# 2. Handle "f or" safely
# Only replace "f or" if it is preceded by whitespace (start of word).
# This avoids "of orbit" -> "of forbit".
# Regex: `(?<=\s)f or`
# Note: This will not catch "something-f or". But ICD-9 usually uses spaces.
# It will catch " f or".

regex_for = r'(?<=\s)f or'
matches = len(re.findall(regex_for, content))
if matches > 0:
    print(f"Replacing '(?<=\s)f or' with 'for': {matches} times")
    # Review substitutions
    for m in re.finditer(regex_for, content):
        start = max(0, m.start() - 20)
        end = min(len(content), m.end() + 20)
        # print(f"Context: {content[start:end].replace(chr(10), ' ')}")
    
    content = re.sub(regex_for, 'for', content)

# 3. Validation: Check if "f [a-z]" still exists?
remaining = re.findall(r'f [a-z]', content)
if remaining:
    print(f"WARNING: Remaining 'f [a-z]' patterns found: {len(remaining)}")
    for r in list(set(remaining))[:10]:
        print(f"  - '{r}'")
        # Find context
        idx = content.find(r)
        if idx != -1:
            print(f"    Context: ...{content[idx-10:idx+15].replace(chr(10), ' ')}...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done.")
