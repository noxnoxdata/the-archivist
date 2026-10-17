# The Archivist

**AI is good at sentences. It is bad at memory. The Archivist is the memory.**

A local story bible and continuity guard for long-form fiction. Built for writers who use AI and refuse to lose the plot.

This repo contains the tool, an original PG-13 story, and a manga kit for that story.

---

## What is here

- `archivist.py`: a dependency-free CLI that holds the story bible, builds a context pack, checks a chapter for continuity problems, tracks plot threads, and exports packs.
- `bible/story.json`: the story bible for the included story.
- `story/part1-the-boy-without-a-book.md`: Part 1 of an original serialized story, PG-13, manga-ready.
- `story/draft-with-errors.md`: a deliberately broken excerpt to test the checker.
- `manga/`: character sheets, a proper Japanese manga style guide, a panel script for Chapter 1, and image prompts for a local model.
- `exports/`: generated context packs, continuity reports, the Gemini Notebook pack, and the comic kit.

---

## Why

AI can draft a chapter in minutes. Then it forgets chapter 3 by chapter 12. Characters change eye colour, dead threads come back, promises are never paid off, and the voice drifts.

A bigger context window does not fix this. A structured story state does.

The Archivist keeps the North Star, the characters, the world rules, the timeline, and the plot threads in one place. Before each writing session it builds a compact context pack. After each chapter it checks the draft against the bible. Then you update the state and keep going.

The loop:

1. Load the context pack.
2. Write the chapter.
3. Check it.
4. Update the story state.
5. Repeat.

At 100k words, the book still knows itself.

---

## The story

**The Archive of Quiet Things**
*Part 1: The Boy Without a Book*

A seaside town. An archive that keeps the memories of everyone who visits, each one turned into a book. Hina Aizawa can hear those memories when she touches the pages. Then a boy arrives in a typhoon with no memory and no book of his own.

Part 1 is three chapters, PG-13, and ends on a hook for Part 2.

Read it here: `story/part1-the-boy-without-a-book.md`

---

## Quickstart

```bash
python3 archivist.py context
python3 archivist.py threads
python3 archivist.py check --file story/part1-the-boy-without-a-book.md
python3 archivist.py check --file story/draft-with-errors.md
python3 archivist.py export notebook
python3 archivist.py export comic
```

No third-party dependencies. Python 3.9+.

Optional local review with Ollama (localhost only):

```bash
python3 archivist.py check --file story/part1-the-boy-without-a-book.md --llm
```

---

## What the checker catches

- **Continuity:** a character's eye or hair colour contradicts the bible. It is character-aware, so one person's description is not attributed to another.
- **Voice:** a list of AI-slop phrases, such as "a testament to" or "a whirlwind of".
- **Rating:** banned content for PG-13.
- **North Star:** the chapter violates one of the story's must-not rules.

The checker is a guardrail, not a judge. It flags, you decide.

---

## The manga kit

`manga/` contains:

- **character-sheets.md**: Hina, Ren, Obaasan, the archive, the books. Silhouettes, expressions, visual consistency.
- **style-guide.md**: B5 format, right-to-left, screentone, line weight, paneling, lettering, SFX, AI-slop guardrails.
- **panel-script-ch1.md**: an 8-page panel-by-panel script for Chapter 1, with camera notes, dialogue, and SFX.
- **image-prompts.md**: prompts for a local image model (SDXL, Flux, ComfyUI), plus negative prompts and consistency notes.

The kit does not bundle an image model. Generate the art locally with the prompts, then add lettering in a vector editor or Clip Studio Paint. Interiors are black and white. Colour belongs on the cover.

---

## Gemini Notebook pack

NotebookLM is now **Gemini Notebook** as of July 2026. It ingests sources and gives cited answers plus Audio and Video Overviews. There is no comic generator inside it.

`python3 archivist.py export notebook` writes a source pack with the story bible, characters, world rules, timeline, summaries, threads, and glossary. Upload it to Gemini Notebook for research, Q&A, and overviews.

---

## Privacy

- The tool is local. No cloud calls by default.
- The optional `--llm` check calls Ollama on `127.0.0.1` only.
- Your fiction stays on your machine.
- Gemini Notebook is a cloud service. Only upload what you are comfortable sharing.
- The included story is original and public. Painted in Ashes is not part of this repo and stays private.

---

## Limitations

- The checker uses simple, deterministic rules. It catches clear contradictions, not subtle thematic drift.
- The slop list is a starting point, not a complete style guide.
- The manga kit is a script and a style guide, not finished art.
- The story is Part 1 of a series. The black book is deliberately unresolved.

---

## Part 2 threads

- **T1** Ren's missing memory and missing book.
- **T2** The black book with Hina's name.
- **T3** Hina's own blank book and her fear of being forgotten.
- **T5** What Obaasan is not telling Hina.

`python3 archivist.py threads` lists them.

---

## License

MIT. The story is original work by Bridget Moh.
