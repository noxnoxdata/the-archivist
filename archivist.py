#!/usr/bin/env python3
"""The Archivist.

A local story bible and continuity guard for long-form fiction.

Commands:
    python3 archivist.py context
    python3 archivist.py threads
    python3 archivist.py check --file story/part1-the-boy-without-a-book.md
    python3 archivist.py check --file story/draft-with-errors.md --write-report
    python3 archivist.py check --file story/part1-the-boy-without-a-book.md --llm
    python3 archivist.py export notebook
    python3 archivist.py export comic

No third-party dependencies. Python 3.9+.
The optional --llm flag calls Ollama on 127.0.0.1 only.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_STORY = ROOT / "bible" / "story.json"
DEFAULT_CHAPTER = ROOT / "story" / "part1-the-boy-without-a-book.md"
EXPORTS = ROOT / "exports"
MANGA = ROOT / "manga"

COLORS = {
    "black", "brown", "blue", "green", "grey", "gray", "hazel",
    "amber", "violet", "red", "silver", "white", "gold", "copper",
}

SLOP_PHRASES = [
    "a testament to",
    "a symphony of",
    "little did she know",
    "little did he know",
    "little did they know",
    "in that moment",
    "a whirlwind of",
    "a mix of",
    "couldn't help but",
    "could not help but",
    "a shiver ran down",
    "the air was thick with",
    "time seemed to slow",
    "everything changed",
    "a pang of",
    "a wave of",
    "a cascade of",
    "a tapestry of",
]

BANNED_CONTENT = ["explicit sex", "graphic sex", "gore", "torture"]


def load_story(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def find_color_near(text: str, part: str) -> str | None:
    """Return the colour that directly modifies a body part, not a nearby object.

    Handles both "grey eyes" and "eyes were dark brown".
    """
    before = re.search(rf"\b([A-Za-z]+)\s+{part}\b", text, re.I)
    if before and before.group(1).lower() in COLORS:
        return before.group(1).lower()
    after = re.search(
        rf"\b{part}\b\s+(?:were|are|was|is)\s+(?:[A-Za-z]+\s+)?([A-Za-z]+)",
        text,
        re.I,
    )
    if after and after.group(1).lower() in COLORS:
        return after.group(1).lower()
    return None


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def check_story(story: dict, text: str) -> list[dict]:
    findings: list[dict] = []
    sentences = split_sentences(text)

    # Character-aware checks: only look at sentences that mention the character
    # (or the sentence just before), so one character's eye colour is never
    # attributed to another.
    for index, sentence in enumerate(sentences):
        window = sentence if index == 0 else f"{sentences[index - 1]} {sentence}"
        for character in story.get("characters", []):
            first_name = character["name"].split()[0]
            if first_name.lower() not in window.lower():
                continue
            attrs = character.get("attributes", {})
            for part in ("eyes", "hair"):
                expected = attrs.get(part)
                if not expected:
                    continue
                if not re.search(rf"\b{part}\b", sentence, re.I):
                    continue
                found = find_color_near(sentence, part)
                if not found or found == expected.lower():
                    continue
                if {found, expected.lower()} == {"grey", "gray"}:
                    continue
                findings.append({
                    "severity": "high",
                    "type": "continuity",
                    "message": f"{character['name']}: bible says {expected} {part}, text says {found}.",
                })

    lowered = text.lower()
    for phrase in SLOP_PHRASES:
        for _ in re.finditer(re.escape(phrase), lowered):
            findings.append({
                "severity": "medium",
                "type": "voice",
                "message": f"AI-slop phrase: '{phrase}'.",
            })

    for phrase in BANNED_CONTENT:
        if phrase in lowered:
            findings.append({
                "severity": "high",
                "type": "rating",
                "message": f"Banned content for PG-13: '{phrase}'.",
            })

    for rule in story.get("north_star", {}).get("must_not", []):
        key = rule.lower()
        if key in lowered:
            findings.append({
                "severity": "high",
                "type": "north_star",
                "message": f"Violates the North Star: '{rule}'.",
            })

    return findings


def format_report(story: dict, source: str, findings: list[dict]) -> str:
    lines = [f"# Continuity Report: {story['title']}", f"Source: `{source}`", ""]
    if not findings:
        lines.append("No issues found. The chapter is consistent with the story bible.")
        return "\n".join(lines)

    counts: dict[str, int] = {}
    for finding in findings:
        counts[finding["severity"]] = counts.get(finding["severity"], 0) + 1
    summary = ", ".join(f"{k}: {v}" for k, v in sorted(counts.items()))
    lines.append(f"Findings: {summary}")
    lines.append("")
    for severity in ("high", "medium", "low"):
        group = [f for f in findings if f["severity"] == severity]
        if not group:
            continue
        lines.append(f"## {severity.capitalize()}")
        for finding in group:
            lines.append(f"- [{finding['type']}] {finding['message']}")
        lines.append("")
    return "\n".join(lines)


def context_pack(story: dict) -> str:
    ns = story.get("north_star", {})
    lines = [f"# Context Pack: {story['title']}", f"## {story.get('part', '')}", ""]
    lines.append("## North Star")
    lines.append(f"- Premise: {ns.get('premise', '')}")
    lines.append(f"- Themes: {', '.join(ns.get('themes', []))}")
    lines.append(f"- Tone: {ns.get('tone', '')}")
    lines.append(f"- Ending: {ns.get('ending', '')}")
    lines.append(f"- Must not: {', '.join(ns.get('must_not', []))}")
    lines.append("")

    chapters = story.get("chapters", [])
    written = [c for c in chapters if c.get("status") == "written"]
    next_number = max((c["number"] for c in written), default=0) + 1
    lines.append("## Next chapter")
    lines.append(f"Chapter {next_number}. Keep the current POV and the open threads in view.")
    lines.append("")

    lines.append("## Characters in play")
    for character in story.get("characters", []):
        lines.append(f"- **{character['name']}** ({character.get('role', '')}): {character.get('voice', '')}")
        lines.append(f"  - Want: {character.get('want', '')}")
        lines.append(f"  - Fear: {character.get('fear', '')}")
    lines.append("")

    lines.append("## Open threads")
    for thread in story.get("threads", []):
        if thread.get("status") == "open":
            lines.append(f"- **{thread['id']}** {thread['name']} (planted: {thread.get('planted', '?')})")
    lines.append("")

    lines.append("## Recent chapters")
    for chapter in written[-3:]:
        lines.append(f"- Ch {chapter['number']}, {chapter['title']}: {chapter.get('summary', '')}")
    lines.append("")

    lines.append("## Reminder")
    lines.append("Write the chapter, then run `check`. Update the bible before you forget.")
    return "\n".join(lines)


def threads_report(story: dict) -> str:
    lines = [f"# Plot Threads: {story['title']}", ""]
    for status in ("open", "resolved"):
        group = [t for t in story.get("threads", []) if t.get("status") == status]
        if not group:
            continue
        lines.append(f"## {status.capitalize()}")
        for thread in group:
            lines.append(f"- **{thread['id']}** {thread['name']} ({thread.get('note', '')})")
        lines.append("")
    return "\n".join(lines)


def notebook_pack(story: dict) -> str:
    lines = [f"# {story['title']}", f"{story.get('part', '')}", ""]
    lines.append("## Premise")
    lines.append(story.get("north_star", {}).get("premise", ""))
    lines.append("")
    lines.append("## Themes and tone")
    ns = story.get("north_star", {})
    lines.append(f"- Themes: {', '.join(ns.get('themes', []))}")
    lines.append(f"- Tone: {ns.get('tone', '')}")
    lines.append(f"- Ending: {ns.get('ending', '')}")
    lines.append("")
    lines.append("## Characters")
    for character in story.get("characters", []):
        lines.append(f"### {character['name']}")
        lines.append(f"- Role: {character.get('role', '')}")
        lines.append(f"- Voice: {character.get('voice', '')}")
        lines.append(f"- Want: {character.get('want', '')}")
        lines.append(f"- Fear: {character.get('fear', '')}")
        lines.append(f"- Visual: {character.get('visual', '')}")
        lines.append("")
    lines.append("## World rules")
    for rule in story.get("world_rules", []):
        lines.append(f"- {rule}")
    lines.append("")
    lines.append("## Timeline")
    for event in story.get("timeline", []):
        lines.append(f"- Day {event['day']}: {event['event']} (Ch {event['chapter']})")
    lines.append("")
    lines.append("## Chapter summaries")
    for chapter in story.get("chapters", []):
        lines.append(f"### Ch {chapter['number']}: {chapter['title']}")
        lines.append(chapter.get("summary", ""))
        lines.append("")
    lines.append("## Threads")
    for thread in story.get("threads", []):
        lines.append(f"- {thread['id']} {thread['name']} [{thread['status']}] {thread.get('note', '')}")
    lines.append("")
    lines.append("## Glossary")
    for entry in story.get("glossary", []):
        lines.append(f"- **{entry['term']}**: {entry['meaning']}")
    return "\n".join(lines)


def export_comic(story: dict) -> None:
    out = EXPORTS / "comic-kit"
    out.mkdir(parents=True, exist_ok=True)
    for name in ("character-sheets.md", "style-guide.md", "panel-script-ch1.md", "image-prompts.md"):
        shutil.copy2(MANGA / name, out / name)
    manifest = [
        f"# Comic Kit: {story['title']}",
        f"## {story.get('part', '')}",
        "",
        "Contents:",
        "- character-sheets.md",
        "- style-guide.md",
        "- panel-script-ch1.md",
        "- image-prompts.md",
        "",
        "Format: B5 manga, right-to-left, monochrome interiors.",
        "Local image model: not bundled. Use ComfyUI, Draw Things, or DiffusionBee with the prompts in image-prompts.md.",
        "Lettering: add speech bubbles and SFX in a vector editor after the art.",
    ]
    (out / "MANIFEST.md").write_text("\n".join(manifest), encoding="utf-8")


def local_llm_review(story: dict, text: str, model: str, host: str) -> str:
    prompt = (
        "You are a continuity editor. Compare the chapter to the story bible facts. "
        "List only concrete problems: contradictions, out-of-character lines, dropped threads, timeline errors. "
        "If there are none, say so. Do not rewrite the chapter.\n\n"
        f"TITLE: {story['title']}\n"
        f"PREMISE: {story.get('north_star', {}).get('premise', '')}\n"
        f"CHARACTERS: {json.dumps(story.get('characters', []), ensure_ascii=False)}\n"
        f"OPEN THREADS: {json.dumps([t for t in story.get('threads', []) if t.get('status') == 'open'], ensure_ascii=False)}\n"
        f"CHAPTER:\n{text[:12000]}"
    )
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
    request = urllib.request.Request(
        f"{host}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            data = json.load(response)
        return (data.get("response") or "").strip()
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        return f"(local model unavailable: {exc})"


def main() -> int:
    parser = argparse.ArgumentParser(description="The Archivist: a story bible and continuity guard.")
    parser.add_argument("--story", default=str(DEFAULT_STORY))
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("context", help="Print the context pack for the next chapter.")
    sub.add_parser("threads", help="List plot threads by status.")
    sub.add_parser("export", help="Export the Gemini Notebook pack or the comic kit.").add_argument(
        "kind", choices=["notebook", "comic"]
    )
    check = sub.add_parser("check", help="Check a chapter against the story bible.")
    check.add_argument("--file", default=str(DEFAULT_CHAPTER))
    check.add_argument("--llm", action="store_true", help="Also ask a local Ollama model for a review.")
    check.add_argument("--write-report", action="store_true", help="Write exports/continuity-report.md.")
    check.add_argument("--model", default="qwen2.5:7b")
    check.add_argument("--host", default="http://127.0.0.1:11434")

    args = parser.parse_args()
    story = load_story(Path(args.story))

    if args.command == "context":
        print(context_pack(story))
        return 0

    if args.command == "threads":
        print(threads_report(story))
        return 0

    if args.command == "export":
        EXPORTS.mkdir(exist_ok=True)
        if args.kind == "notebook":
            out = EXPORTS / "gemini-notebook-pack.md"
            out.write_text(notebook_pack(story), encoding="utf-8")
            print(f"Wrote {out}")
        else:
            export_comic(story)
            print(f"Wrote {EXPORTS / 'comic-kit'}")
        return 0

    if args.command == "check":
        source = Path(args.file)
        text = source.read_text(encoding="utf-8")
        findings = check_story(story, text)
        report = format_report(story, str(source.relative_to(ROOT)) if source.is_relative_to(ROOT) else str(source), findings)
        print(report)
        if args.llm:
            print("\n## Local LLM review\n")
            print(local_llm_review(story, text, args.model, args.host.rstrip("/")))
        if args.write_report:
            EXPORTS.mkdir(exist_ok=True)
            out = EXPORTS / "continuity-report.md"
            out.write_text(report, encoding="utf-8")
            print(f"\nWrote {out}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
