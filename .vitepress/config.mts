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
      pattern: `${env.VITE_REPO_URL}/edit/${env.VITE_REPO_BRANCH}/:path`,
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
      chunkSizeWarningLimit: 3000,
    },
  },
});