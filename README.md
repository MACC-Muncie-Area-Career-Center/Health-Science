# MACC Health Sciences, Dental, and EMT Programs

Medical terminology games and practice activities shared by the MACC Health Sciences, Dental, and EMT programs.

## What's here

```
index.html                  Landing page for all three programs
meddecode/tiles/index.html  MedDecode Tiles: Mahjong-style matching game
meddecode/sort/index.html   MedDecode Sort: drag-and-drop sorting game
meddecode/dissect/index.html MedDecode Dissect: cut terms into word parts
meddecode/build/index.html  MedDecode Build: build terms from word parts to answer a case
meddecode/encounter/index.html MedDecode Encounter: patient-interview scenarios by program
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

- MedDecode Tiles deals each board from the `ALL_PAIRS` pool in `meddecode/tiles/index.html`, generated from the master list (24, 36 or 48 tiles per board).
- MedDecode Sort reads its cards from the `ITEMS` list in `meddecode/sort/index.html`, which matches the **Sort Items** sheet.
- MedDecode Dissect reads its terms from the `TERMS` list in `meddecode/dissect/index.html`, which matches the **Dissect Terms** sheet.
- MedDecode Build reads its cases from the `CASES` list (41 cases; rounds of 8, 12 or 20) and its word list from the `LEX` list in `meddecode/build/index.html`, which match the **Build Cases** and **Build Word List** sheets. Its **Jeopardy** mode reads the `JEOP` list, generated from the master list by `content/gen_jeopardy.py`.

- MedDecode Encounter reads its 20 scenarios (5 each for EMT, CNA, CCMA and Dental) from the `S` list and its question bank (about 45 questions plus 10 hands-on actions) from the `Q` and `ACTIONS` lists in `meddecode/encounter/index.html`.

For now, approved spreadsheet rows are copied into those lists by hand. A later version will load them from a shared data file.

## Master word list

`content/master.py` is the MedDecode master list of word parts and terms (meaning, pronunciation, body system, what each term names). `content/gen_content.py` checks it (every term must be spelled by its parts) and generates the content for **Tiles** (the pair pool), **Dissect** (terms and cuts) and **Sort** (cards). Build and Encounter content is still written by hand.

To add terms: add rows to `master.py`, run `python3 content/gen_content.py`, and copy the generated content into the games (Claude can do this step). The same lists appear in the **Master Word Parts** and **Master Terms** sheets of the content spreadsheet for instructor review.

## Classroom mode and Team mode (all five games)

Each game has a **Classroom tools** bar under its title.

- **Classroom mode** enlarges text and controls for a large touchscreen and shows a big definition board (term, pronunciation, Hear it, meaning, word parts) after each correct answer. Tap ✕ to hide it.
- **Team mode** sets up 2 to 4 named teams and the points for a correct play. Teams take turns; each turn is one play (a pair in Tiles, a card in Sort, a check in Dissect or Build, a question or decision in Encounter). A correct play adds points, and the turn passes to the next team. The scoreboard has +/− buttons for corrections, a Turn button to change whose turn it is, Skip turn, Show winner and Reset scores.
- **Full screen** hides the browser bars.

Team names and scores are saved in the browser, so a class can keep one running score across all five games on the same device. Nothing is sent anywhere.

Tip: on a large TV, browser zoom (Ctrl and +) also works well alongside Classroom mode.

## Instructor links for MedDecode Encounter

Open MedDecode Encounter, expand **Instructor setup**, choose programs, body systems, ages, scenarios, question methods and mode, then press **Copy student link**. The settings travel in the link, for example:

`.../meddecode/encounter/?program=EMT&mode=test&limit=12`

Students who open that link see only the matching scenarios.

## Student data

These games do not save or send any student information. Scores disappear when the page is closed. In MedDecode Encounter, the optional Speak button uses the browser's speech recognition; in Chrome, that audio is processed by Google's speech service.
