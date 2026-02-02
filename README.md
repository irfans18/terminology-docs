# Terminology Documentation

A modern, high-performance documentation site for medical terminologies, built with **VitePress**. This project currently serves as the digital repository for **ICD-9-CM 2010 Volume 1 and Volume 3**.

## 🚀 Features

- **Fast & Lightweight**: Built on top of Vite and Vue.
- **Local Search**: Integrated local search with detailed view enabled by default.
- **Organized Structure**: Segmented by chapters (Volume 1) and alphabetic index (Volume 3).
- **Changelog**: Track changes and updates to the documentation.
- **Last Updated**: Automatic tracking of page updates.

## 🛠 Tech Stack

- **Framework**: [VitePress](https://vitepress.dev/)
- **Runtime**: [Node.js](https://nodejs.org/)
- **Package Manager**: `yarn` (or `npm`)
- **Content**: Markdown (GFM)

## 📦 Getting Started

### Prerequisites

- Node.js (v18 or higher recommended)
- yarn or npm

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd doc-vitepress
   ```

2. Install dependencies:
   ```bash
   yarn install
   ```

### Development

Run the development server:

```bash
yarn run docs:dev
```

The site will be available at `http://localhost:5173`.

### Production Build

To build the project for production:

```bash
yarn run docs:build
```

The static files will be generated in `.vitepress/dist`.

### Preview Build

To preview the production build locally:

```bash
yarn run docs:preview
```

## 📂 Project Structure

- `.vitepress/`: VitePress configuration, theme, and assets.
- `src/docs/`: Main documentation content in Markdown.
  - `icd9cm/`: ICD-9-CM Volume 1 chapters.
  - `icd9cmvol3/`: ICD-9-CM Volume 3 alphabetic index.
  - `index.md`: Home page.
  - `changelog.md`: Project changelog.
- `ref/`: Reference materials and utility files (excluded from build).
- `scripts/`: Automation scripts for data processing.

## 📝 Usage

- Use the **Sidebar** to navigate through different volumes and chapters.
- Use the **Search bar** (Shortcut: `Ctrl+K`) to quickly find specific codes or terms.
- The **"Edit this page"** link at the bottom of each page allows for quick contributions via GitHub.

## ⚖️ License

[MIT](LICENSE)
