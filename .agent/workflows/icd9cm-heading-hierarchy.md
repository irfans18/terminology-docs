---
description: Convert ICD-9-CM markdown files to use proper heading hierarchy for cross-referencing
---

# ICD-9-CM Heading Hierarchy Cleanup

This skill converts bold procedure code items to proper heading hierarchy in ICD-9-CM documentation.

## Hierarchy Structure

| Level | Markdown | Example                                                       |
| ----- | -------- | ------------------------------------------------------------- |
| h1    | `#`      | `# 0. PROCEDURES AND INTERVENTIONS...` (Chapter title)        |
| h2    | `##`     | `## 00 Procedures and interventions...` (Section - 2-digit)   |
| h3    | `###`    | `### 00.0 Therapeutic ultrasound` (Category - 3-digit)        |
| h4    | `####`   | `#### 00.01 Therapeutic ultrasound...` (Procedure - 4+ digit) |

## Reference File

Use `icd9cm/chapter-0/index.md` as the reference for correct formatting.

## Conversion Steps

### 1. Convert Bold Codes to H4 Headings

Run sed command to convert `- **XX.XX** Title {#anchor}` to `#### XX.XX Title {#anchor}`:

```bash
// turbo
sed -E 's/^- \*\*([0-9]+\.[0-9]+)\*\* (.*)/#### \1 \2/' icd9cm/chapter-X/index.md > temp.md && mv temp.md icd9cm/chapter-X/index.md
```

Replace `chapter-X` with the target chapter.

### 2. Verify VitePress Config

Ensure `.vitepress/config.mts` has outline depth set to show h4:

```typescript
themeConfig: {
  outline: [2, 4], // Show h2-h4 in "On this page" sidebar
  // ...
}
```

### 3. Manual Cleanup (if needed)

After sed conversion, check for:

- Sub-items that were indented under bold items should now be list items under the h4 heading
- Ensure blank line after each h4 heading before list items
- Fix any Excludes/Includes that need proper nesting

### 4. Verify in Browser

```bash
// turbo
yarn docs:dev --port 5174
```

Navigate to the chapter page and verify:

- [ ] H4 headings appear in "On this page" sidebar
- [ ] Anchors work (e.g., `#00-01`)
- [ ] Visual hierarchy is correct

## Cross-Referencing

After conversion, codes can be referenced:

**Same chapter:**

```markdown
See [00.01](#00-01)
```

**Different chapter:**

```markdown
See [00.01](/icd9cm/chapter-0/#00-01)
```

## Chapter Status

- [x] chapter-0 ✅ (Reference)
- [ ] chapter-1
- [ ] chapter-2
- [ ] chapter-3
- [ ] chapter-3a
- [ ] chapter-4
- [ ] chapter-5
- [ ] chapter-6
- [ ] chapter-7
- [ ] chapter-8
- [ ] chapter-9
- [ ] chapter-10
- [ ] chapter-11
- [ ] chapter-12
- [ ] chapter-13
- [ ] chapter-14
- [ ] chapter-15
- [ ] chapter-16 (ON HOLD)
