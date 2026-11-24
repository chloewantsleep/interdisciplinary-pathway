# Leanings

**Live:** https://leanings-three.vercel.app

Leanings is a swipe tool for interdisciplinary people. Each card is a scholar. You swipe right to save them and left to pass. Each card shows two things: a **knowledge diagram** of where the scholar's research leans across 8 disciplines, and a **heat map** of how that mix has shifted year by year.

It is built on top of [Chloeverse](https://chloeni.studio/fun/chloeverse/), my own knowledge graph of courses and projects. Chloeverse acts as the **"you"** profile: every card marks where you sit (red ●), says how much the scholar overlaps with you, and names what they bring that you don't. The **Chloeverse** tab shows the original graph.

Made as a vibe-coding homework for [English 298AI: Humanities AI Lab](https://english.fas.harvard.edu/english-298ai-humanities-ai-lab) at Harvard.

## Views

- **Deck**: swipe, or use ← / →. Undo with ⌫.
  - *Knowledge diagram*: the 8 disciplines sit on a ring and each node is sized by its share of the scholar's output. The scholar's dot sits at the weighted centre of their last 3 years. A dotted trail shows earlier years, and the red segment leads into the present.
  - *Heat map*: rows are disciplines and columns are years. The red frame marks the "now" window.
- **Saved**: the scholars you saved plus you, drawn as a Chloeverse-style force graph, with a matrix comparing what each person leans toward now.
- **Chloeverse**: the original knowledge graph.

## Data

- **Sample scholars** are fictional and labelled `SAMPLE`. They are used when no API key is set.
- **Live scholars** come from [OpenAlex](https://openalex.org). Paste a free API key into the top bar, then search by topic or by name. Each work's OpenAlex topics are mapped to the 8 Chloeverse disciplines by the rules in `SUB_RULES` / `FIELD_RULES` in `index.html`. The key is stored only in your own browser.
- **You** come from `chloeverse/data.js`. Each course or project is tagged with its disciplines.

## Run locally

```sh
python3 -m http.server 5173
# open http://localhost:5173
```

The site is static: one HTML file plus d3 from a CDN. There is no build step.
