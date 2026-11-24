# Leanings

**Live:** https://leanings-three.vercel.app

Leanings is a swipe tool for interdisciplinary people. Each card is a subject: a course by default, or a scholar when live data is on. You swipe right to save it and left to pass. Each card shows two things: a **knowledge diagram** of where the subject leans across 8 disciplines, and a **heat map** over the years.

It is built on top of [Chloeverse](https://chloeni.studio/fun/chloeverse/), a knowledge graph of courses and projects, which is used here as the **Example** "you" profile. Every card marks where you sit (red ●), says how much the subject overlaps with you, and names what it brings that you don't. The **Example** tab shows the original graph.

Made as a vibe-coding homework for [English 298AI: Humanities AI Lab](https://english.fas.harvard.edu/english-298ai-humanities-ai-lab) at Harvard.

## Views

- **Deck**: swipe, or use ← / →. Undo with ⌫.
  - *Knowledge diagram*: the 8 disciplines sit on a ring and each node is sized by its share of the scholar's output. The scholar's dot sits at the weighted centre of their last 3 years. A dotted trail shows earlier years, and the red segment leads into the present.
  - *Heat map*: rows are disciplines and columns are years. The red frame marks the "now" window.
- **Saved**: what you saved plus you, drawn as a Chloeverse-style force graph, with a matrix comparing what each person leans toward now.
- **Example**: the original Chloeverse knowledge graph.

## Data

- **Courses (default deck)**: the Harvard and MIT courses from 2025 on in the Example record, each linked to its course page. On a course card, the heat map shows the Example record over time, and red frames mark the course's year and disciplines, so you can see where the course sits in your path.
- **Live scholars** come from [OpenAlex](https://openalex.org). Paste a free API key into the top bar, then search by topic or by name. Each work's OpenAlex topics are mapped to the 8 Chloeverse disciplines by the rules in `SUB_RULES` / `FIELD_RULES` in `index.html`. The key is stored only in your own browser.
- **You (Example)** come from `chloeverse/data.js`. Each course or project is tagged with its disciplines.

## Run locally

```sh
python3 -m http.server 5173
# open http://localhost:5173
```

The site is static: one HTML file plus d3 from a CDN. There is no build step.
