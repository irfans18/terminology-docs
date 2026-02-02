import { defineConfig, loadEnv } from "vitepress";

const env = loadEnv('', process.cwd())

// https://vitepress.dev/reference/site-config
export default defineConfig({
  srcDir: 'src/docs',
  title: "Terminology Documentation",
  description: "Terminology Documentation",
  srcExclude: ["**/ref/**"],
  ignoreDeadLinks: true,
  lastUpdated: true,
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    outline: [2, 6], // Show h2-h6 in "On this page" sidebar
    editLink: {
      pattern: `${env.VITE_REPO_URL}/edit/${env.VITE_REPO_BRANCH}/src/docs/:path`,
      text: 'Edit this page on GitHub'
    },
    nav: [
      { text: "Home", link: "/" },
      // { text: "Examples", link: "/markdown-examples" },
      { text: "ICD-9-CM", link: "/icd9cm/chapter-0/" },
      // { text: "Changelog", link: "/changelog" },
    ],

    sidebar: [
      // {
      //   text: "Examples",
      //   items: [
      //     { text: "Markdown Examples", link: "/markdown-examples" },
      //     { text: "Runtime API Examples", link: "/api-examples" },
      //   ],
      // },
      {
        text: "ICD-9-CM 2010 Vol 1",
        collapsed: true,
        items: [
          { text: "0 - Procedures and Interventions (00)", link: "/icd9cm/chapter-0/" },
          { text: "1 - Nervous System (01-05)", link: "/icd9cm/chapter-1/" },
          { text: "2 - Endocrine System (06-07)", link: "/icd9cm/chapter-2/" },
          { text: "3 - Eye (08-16)", link: "/icd9cm/chapter-3/" },
          { text: "3a - Other Misc Procedures (17)", link: "/icd9cm/chapter-3a/" },
          { text: "4 - Ear (18-20)", link: "/icd9cm/chapter-4/" },
          { text: "5 - Nose, Mouth, Pharynx (21-29)", link: "/icd9cm/chapter-5/" },
          { text: "6 - Respiratory System (30-34)", link: "/icd9cm/chapter-6/" },
          { text: "7 - Cardiovascular System (35-39)", link: "/icd9cm/chapter-7/" },
          { text: "8 - Hemic and Lymphatic System (40-41)", link: "/icd9cm/chapter-8/" },
          { text: "9 - Digestive System (42-54)", link: "/icd9cm/chapter-9/" },
          { text: "10 - Urinary System (55-59)", link: "/icd9cm/chapter-10/" },
          { text: "11 - Male Genital Organs (60-64)", link: "/icd9cm/chapter-11/" },
          { text: "12 - Female Genital Organs (65-71)", link: "/icd9cm/chapter-12/" },
          { text: "13 - Obstetrical Procedures (72-75)", link: "/icd9cm/chapter-13/" },
          { text: "14 - Musculoskeletal System (76-84)", link: "/icd9cm/chapter-14/" },
          { text: "15 - Integumentary System (85-86)", link: "/icd9cm/chapter-15/" },
          { text: "16 - Diagnostic/Therapeutic (87-99)", link: "/icd9cm/chapter-16/" },
        ],
      },
      {
        text: "ICD-9-CM 2010 Vol 3",
        collapsed: true,
        items: [
          { text: "Index Overview", link: "/icd9cmvol3/" },
          { text: "A - Abbe to Azure", link: "/icd9cmvol3/a" },
          { text: "B - Baffes to Bypass", link: "/icd9cmvol3/b" },
          { text: "C - Caldwell to Cystourethroscopy", link: "/icd9cmvol3/c" },
          { text: "D - Dacryoadenectomy to Dura", link: "/icd9cmvol3/d" },
          { text: "E - E2F decoy to Extubation", link: "/icd9cmvol3/e" },
          { text: "F - Face lift to Fusion", link: "/icd9cmvol3/f" },
          { text: "G - Gait training to Guthrie", link: "/icd9cmvol3/g" },
          { text: "H - Hagner to Hz", link: "/icd9cmvol3/h" },
          { text: "I - IAEMT to Irwin", link: "/icd9cmvol3/i" },
          { text: "J - Jaboulay to Jejunopexy", link: "/icd9cmvol3/j" },
          { text: "K - Kangaroo care to Krukenberg", link: "/icd9cmvol3/k" },
          { text: "L - Labbe to Lysis", link: "/icd9cmvol3/l" },
          { text: "M - Madlener to Myringotomy", link: "/icd9cmvol3/m" },
          { text: "N - Nailing to Nutrition", link: "/icd9cmvol3/n" },
          { text: "O - Ober to Ozaki", link: "/icd9cmvol3/o" },
          { text: "P - Pacemaker to Pylorotomy", link: "/icd9cmvol3/p" },
          { text: "Q - Quadrant resection to Quilecea", link: "/icd9cmvol3/q" },
          { text: "R - Rachicentesis to Russe", link: "/icd9cmvol3/r" },
          { text: "S - Sacculotomy to Syme", link: "/icd9cmvol3/s" },
          { text: "T - Taarnhoj to Tylectomy", link: "/icd9cmvol3/t" },
          { text: "U - Uchida to Utriculotomy", link: "/icd9cmvol3/u" },
          { text: "V - Vaccination to Vulvectomy", link: "/icd9cmvol3/v" },
          { text: "W - Wada test to Wrist", link: "/icd9cmvol3/w" },
          { text: "X - Xenograft to X-ray", link: "/icd9cmvol3/x" },
          { text: "Y - Young to Yount", link: "/icd9cmvol3/y" },
          { text: "Z - Zancolli to Z-plasty", link: "/icd9cmvol3/z" },
        ],
      },
      { text: "Changelog", link: "/changelog" },
    ],

    socialLinks: [
      { icon: "github", link: env.VITE_REPO_URL },
    ],

    search: {
      provider: "local",
      options: {
        detailedView: true,
      },
    },
  },
  vite: {
    build: {
      chunkSizeWarningLimit: 5000,
    },
  },
});