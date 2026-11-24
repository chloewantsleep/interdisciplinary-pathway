# Interdisciplinary Pathway

**Live:** https://interdisciplinary-pathway.vercel.app

Interdisciplinary Pathway is a swipe tool for interdisciplinary people. Each card is a course, drawn at random from current Harvard GSD and MIT offerings. You swipe right to save it and left to pass. Each card shows two things: a **knowledge diagram** of where the subject leans across 8 disciplines, and a **heat map** over the years.

It is built on top of [Chloeverse](https://chloeni.studio/fun/chloeverse/), a knowledge graph of courses and projects, which is used here as the **Example** "you" profile. Every card marks where you sit (red ●), says how much the subject overlaps with you, and names what it brings that you don't. The **Example** tab shows the original graph.

Made as a vibe-coding homework for [English 298AI: Humanities AI Lab](https://english.fas.harvard.edu/english-298ai-humanities-ai-lab) at Harvard.

## Views

- **Deck**: 50 random courses. Swipe, or use ← / →; undo with ⌫. **Shuffle** draws 50 new ones.
  - *Knowledge diagram*: the 8 disciplines sit on a ring. The course's dot sits between the disciplines it touches, and the red YOU marker shows where the Example record leans now.
  - *Heat map*: the Example record's disciplines (rows) across years (columns). Red frames mark where this course would sit in that path.
- **Saved**: what you saved plus you, drawn as a Chloeverse-style force graph, with a comparison matrix.
- **Example**: the original Chloeverse knowledge graph.

## Data

- **Courses**: `data/courses.json`, about 1,000 courses from fall 2025 on. It is built by `python3 scripts/build_courses.py` from the [Harvard GSD course API](https://www.gsd.harvard.edu/courses/) and the [MIT subject listing](https://student.mit.edu/catalog/index.cgi). Courses are tagged with the 8 disciplines by keyword rules on their department, title and description (see `KW` in the script), so treat the tags as rough.
- **You (Example)** come from `chloeverse/data.js`. Each course or project is tagged with its disciplines.

## Run locally

```sh
python3 -m http.server 5173
# open http://localhost:5173
```

The site is static: one HTML file plus d3 from a CDN. There is no build step.
