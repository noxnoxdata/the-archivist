#!/usr/bin/env python3
"""Generate Chapter 1 manga panels locally with Draw Things.

Usage:
    python3 generate_panels.py --start 0 --end 6
    python3 generate_panels.py --start 0 --end 24 --force

Requires draw-things-cli and the Animagine XL 4.0 model.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL = "animagine_xl_4.0_f16.ckpt"
STYLE = (
    "monochrome Japanese manga, clean black ink line art, varied line weight, "
    "screentone shading, simple background, no text"
)
NEGATIVE = (
    "color, complex background, noisy texture, hatching everywhere, chibi, moe, "
    "glossy, 3d, text, speech bubble, extra fingers, deformed hands, watermark"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=24)
    parser.add_argument("--steps", type=int, default=18)
    parser.add_argument("--cfg", type=float, default=5.5)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--ids", default="", help="Comma-separated panel ids to generate.")
    args = parser.parse_args()

    data = json.loads((ROOT / "panels.json").read_text(encoding="utf-8"))
    panels = data["panels"]
    out_dir = ROOT / "panels"
    out_dir.mkdir(exist_ok=True)
    wanted = {i.strip() for i in args.ids.split(",") if i.strip()}

    for index in range(args.start, min(args.end, len(panels))):
        panel = panels[index]
        if wanted and panel["id"] not in wanted:
            continue
        out = out_dir / f"{panel['id']}.png"
        if out.exists() and not args.force:
            print(f"skip {panel['id']}")
            continue
        prompt = f"{panel['prompt']}. {STYLE}"
        command = [
            "draw-things-cli", "generate", "--local",
            "--model", MODEL,
            "--prompt", prompt,
            "--negative-prompt", NEGATIVE,
            "--width", "1024", "--height", "640",
            "--steps", str(args.steps), "--cfg", str(args.cfg),
            "--seed", str(panel["seed"]),
            "--output", str(out),
        ]
        print(f"[{index + 1}/{len(panels)}] {panel['id']}", flush=True)
        subprocess.run(command, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
