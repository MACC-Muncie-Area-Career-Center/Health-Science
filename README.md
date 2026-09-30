# MACC Health Sciences, Dental, and EMT Programs

Medical terminology games and practice activities shared by the MACC Health Sciences, Dental, and EMT programs.

## What's here

```
index.html                  Landing page for all three programs
meddecode/tiles/index.html  MedDecode Tiles: Mahjong-style matching game
meddecode/sort/index.html   MedDecode Sort: drag-and-drop sorting game
meddecode/dissect/index.html MedDecode Dissect: cut terms into word parts
.nojekyll                   Tells GitHub Pages to serve the files as-is
```

Each page is a single self-contained HTML file with no build step and nothing to install. The only outside resource is Google Fonts; if it's blocked, the pages fall back to system fonts.

## Publish with GitHub Pages

1. Upload all of these files to the root of the repository, keeping the folders.
2. In the repository, go to **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to **Deploy from a branch**, pick **main** and **/ (root)**, then click **Save**.
4. After a minute or two the site is live at `https://<organization>.github.io/<repository-name>/`.

All links are relative, so the site works at any address, and it also runs by opening `index.html` directly from a folder.

## Adding a new game

1. Create a folder, for example `meddecode/flashcards/`, and put the game in `index.html` inside it.
2. Add a back link at the top of the page: `<a href="../../">← MACC Health Sciences, Dental &amp; EMT</a>`.
3. Copy one of the `<a class="game">` cards in the root `index.html` and update the text and link.

## Content

The game content is **draft** and needs instructor approval. Instructors write and approve items in `MedDecode_Content_Template.xlsx`, which is kept outside this repository.

- MedDecode Tiles reads its pairs from the `PAIRS` list in `meddecode/tiles/index.html`, which matches the **Match Pairs** sheet.
- MedDecode Sort reads its cards from the `ITEMS` list in `meddecode/sort/index.html`, which matches the **Sort Items** sheet.
- MedDecode Dissect reads its terms from the `TERMS` list in `meddecode/dissect/index.html`, which matches the **Dissect Terms** sheet.

For now, approved spreadsheet rows are copied into those lists by hand. A later version will load them from a shared data file.

## Student data

These games do not save or send any student information. Scores disappear when the page is closed.
