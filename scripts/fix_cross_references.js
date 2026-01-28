const fs = require('fs');
const path = require('path');
const glob = require('glob');

const icd9Dir = path.resolve(__dirname, '../icd9cm');

// Mapping of code ranges to chapter directories
const chapterMapping = [
  { range: [0, 0], dir: 'chapter-0' },
  { range: [1, 5], dir: 'chapter-1' },
  { range: [6, 7], dir: 'chapter-2' },
  { range: [8, 16], dir: 'chapter-3' },
  { range: [17, 17], dir: 'chapter-3a' },
  { range: [18, 20], dir: 'chapter-4' },
  { range: [21, 29], dir: 'chapter-5' },
  { range: [30, 34], dir: 'chapter-6' },
  { range: [35, 39], dir: 'chapter-7' },
  { range: [40, 41], dir: 'chapter-8' },
  { range: [42, 54], dir: 'chapter-9' },
  { range: [55, 59], dir: 'chapter-10' },
  { range: [60, 64], dir: 'chapter-11' },
  { range: [65, 71], dir: 'chapter-12' },
  { range: [72, 75], dir: 'chapter-13' },
  { range: [76, 84], dir: 'chapter-14' },
  { range: [85, 86], dir: 'chapter-15' },
  { range: [87, 99], dir: 'chapter-16' },
];

function getChapterDir(code) {
  const codeNum = parseFloat(code);
  const chapter = chapterMapping.find(
    (c) => codeNum >= c.range[0] && codeNum <= c.range[1]
  );
  return chapter ? chapter.dir : null;
}

// Find all markdown files
const files = glob.sync('**/*.md', { cwd: icd9Dir, absolute: true });

files.forEach((file) => {
  let content = fs.readFileSync(file, 'utf8');
  const currentChapterDir = path.basename(path.dirname(file));

  // Regex to match links like [87.02](#87-02) or [06.91](#06-91)
  // It captures the text in group 1 and the target hash in group 2
  // Modified to be more robust for the target hash which relies on converting dots to dashes
  // The hash should be a rough match to the code
  
  // We look for links where the href starts with # and looks like a code anchor
  const regex = /\[([^\]]+)\]\(#([0-9]{2}-[0-9]{2})\)/g;

  let modified = false;

  const newContent = content.replace(regex, (match, linkText, anchor) => {
    // Reconstruct the code from the anchor (e.g. 87-02 -> 87.02) to find the chapter
    // Or just use the first part of the anchor (87 of 87-02)
    const codePrefix = anchor.split('-')[0];
    
    // We can also try to use the linkText itself if it looks like a code
    // usage: [06.91](#06-91) -> code is 06.91
    
    // Let's use the start of the anchor to identify the chapter logic
    const chapterDir = getChapterDir(codePrefix);

    if (chapterDir) {
      if (chapterDir !== currentChapterDir) {
         // Create relative link
         // From icd9cm/chapter-X/index.md to icd9cm/chapter-Y/index.md
         // Path is ../chapter-Y/index.md
         const relativePath = `../${chapterDir}/index.md#${anchor}`;
         console.log(`Updating ${match} to [${linkText}](${relativePath}) in ${currentChapterDir}`);
         modified = true;
         return `[${linkText}](${relativePath})`;
      } else {
        // Same chapter, keep as is
        return match;
      }
    }
    
    return match;
  });

  if (modified) {
    fs.writeFileSync(file, newContent);
    console.log(`Saved changes to ${file}`);
  }
});
