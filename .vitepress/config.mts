import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "My Awesome Project",
  description: "A VitePress Site",
  srcExclude: ["**/ref/**"],
  ignoreDeadLinks: true,
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: "Home", link: "/" },
      { text: "Examples", link: "/markdown-examples" },
      { text: "ICD-9-CM", link: "/icd9cm/chapter-0/" },
    ],

    sidebar: [
      {
        text: "Examples",
        items: [
          { text: "Markdown Examples", link: "/markdown-examples" },
          { text: "Runtime API Examples", link: "/api-examples" },
        ],
      },
      {
        text: "ICD-9-CM Procedures",
        collapsed: true,
        items: [
          { text: "Procedures and Interventions (00)", link: "/icd9cm/chapter-0/" },
          { text: "Nervous System (01-05)", link: "/icd9cm/chapter-1/" },
          { text: "Endocrine System (06-07)", link: "/icd9cm/chapter-2/" },
          { text: "Eye (08-16)", link: "/icd9cm/chapter-3/" },
          { text: "Other Misc Procedures (17)", link: "/icd9cm/chapter-3a/" },
          { text: "Ear (18-20)", link: "/icd9cm/chapter-4/" },
          { text: "Nose, Mouth, Pharynx (21-29)", link: "/icd9cm/chapter-5/" },
          { text: "Respiratory System (30-34)", link: "/icd9cm/chapter-6/" },
          { text: "Cardiovascular System (35-39)", link: "/icd9cm/chapter-7/" },
          { text: "Hemic and Lymphatic System (40-41)", link: "/icd9cm/chapter-8/" },
          { text: "Digestive System (42-54)", link: "/icd9cm/chapter-9/" },
          { text: "Urinary System (55-59)", link: "/icd9cm/chapter-10/" },
          { text: "Male Genital Organs (60-64)", link: "/icd9cm/chapter-11/" },
          { text: "Female Genital Organs (65-71)", link: "/icd9cm/chapter-12/" },
          { text: "Obstetrical Procedures (72-75)", link: "/icd9cm/chapter-13/" },
          { text: "Musculoskeletal System (76-84)", link: "/icd9cm/chapter-14/" },
          { text: "Integumentary System (85-86)", link: "/icd9cm/chapter-15/" },
          { text: "Diagnostic/Therapeutic (87-99)", link: "/icd9cm/chapter-16/" },
        ],
      },
    ],

    socialLinks: [
      { icon: "github", link: "https://github.com/vuejs/vitepress" },
    ],

    search: {
      provider: "local",
    },
  },
});

