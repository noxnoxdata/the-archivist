#!/usr/bin/env python3
"""Compose page 1 of the manga one-shot from generated panels."""

from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
PANELS = ROOT / "panels"
PAGES = ROOT / "pages"
PAGES.mkdir(exist_ok=True)

W, H = 1200, 1700
M = 40
INK = "black"
PAPER = "white"

FONT_TITLE = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_BODY = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_DIALOGUE = "/System/Library/Fonts/MarkerFelt.ttc"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def manga_panel(path: Path, width: int, height: int, centering=(0.5, 0.35)) -> Image.Image:
    image = Image.open(path).convert("RGB")
    image = ImageOps.grayscale(image)
    image = ImageEnhance.Contrast(image).enhance(1.6)
    image = ImageOps.posterize(image.convert("L"), 3)
    image = ImageOps.fit(image, (width, height), method=Image.LANCZOS, centering=centering)
    return image.convert("RGB")


def draw_caption(draw: ImageDraw.ImageDraw, box, text: str, fnt) -> None:
    x, y, w = box
    lines = textwrap.wrap(text, width=42)
    line_h = fnt.size + 8
    h = len(lines) * line_h + 24
    draw.rectangle((x, y, x + w, y + h), fill=PAPER, outline=INK, width=3)
    for i, line in enumerate(lines):
        draw.text((x + 14, y + 12 + i * line_h), line, font=fnt, fill=INK)


def speech_bubble(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, text: str,
                  fnt, tail: tuple[int, int]) -> None:
    lines = textwrap.wrap(text, width=26)
    line_h = fnt.size + 8
    h = len(lines) * line_h + 26
    tx, ty = tail
    # Tail first, then the bubble on top, so the base line is hidden.
    draw.polygon([(x + w * 0.32, y + h - 2), (tx, ty), (x + w * 0.58, y + h - 2)],
                 fill=PAPER, outline=INK)
    draw.rounded_rectangle((x, y, x + w, y + h), radius=26, fill=PAPER, outline=INK, width=3)
    for i, line in enumerate(lines):
        draw.text((x + 18, y + 14 + i * line_h), line, font=fnt, fill=INK)


def main() -> None:
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)

    # Title block
    draw.text((M, 36), "The Archive of Quiet Things", font=font(FONT_TITLE, 46), fill=INK)
    draw.text((M, 96), "Part 1: The Boy Without a Book", font=font(FONT_BODY, 24), fill=INK)
    draw.text((M, 132), "Chapter 1: The Boy in the Rain", font=font(FONT_TITLE, 28), fill=INK)
    draw.line((M, 178, W - M, 178), fill=INK, width=3)

    # Panel 1: Hina
    top = manga_panel(PANELS / "p02a.png", W - 2 * M, 600, centering=(0.42, 0.3))
    page.paste(top, (M, 220))
    draw.rectangle((M, 220, W - M, 820), outline=INK, width=5)
    draw_caption(draw, (M + 24, 244, 620),
                 "Three hours before the typhoon. The archive was not ready.",
                 font(FONT_BODY, 22))
    speech_bubble(draw, 650, 244, 470,
                  "Obaasan! The north window won't latch!",
                  font(FONT_DIALOGUE, 25), (520, 470))

    # Panel 2: Obaasan
    bottom = manga_panel(PANELS / "p03a.png", W - 2 * M, 600, centering=(0.64, 0.36))
    page.paste(bottom, (M, 880))
    draw.rectangle((M, 880, W - M, 1480), outline=INK, width=5)

    speech_bubble(draw, 82, 908, 540,
                  "Leave it. The quiet ones like the rain.",
                  font(FONT_DIALOGUE, 25), (720, 1120))
    draw_caption(draw, (82, 1290, 560),
                 "Every memory becomes a book. The forgotten ones go quiet.",
                 font(FONT_BODY, 20))

    # Footer
    draw.line((M, 1570, W - M, 1570), fill=INK, width=2)
    draw.text((M, 1592), "A one-shot manga adaptation of the original story.", font=font(FONT_BODY, 18), fill=INK)
    draw.text((W - 110, 1592), "1", font=font(FONT_TITLE, 22), fill=INK)

    out = PAGES / "page-01.png"
    page.save(out, "PNG")
    page.save(ROOT / "chapter1-page1.pdf", "PDF", resolution=150.0)
    print(f"Wrote {out}")
    print(f"Wrote {ROOT / 'chapter1-page1.pdf'}")


if __name__ == "__main__":
    main()
