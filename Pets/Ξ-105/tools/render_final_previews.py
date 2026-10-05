#!/usr/bin/env python3
"""Extract exact atlas cells and render the non-standard pet QA previews."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CELL_W = 192
CELL_H = 208
STATES = [
    ("idle", 0, 6),
    ("running-right", 1, 8),
    ("running-left", 2, 8),
    ("waving", 3, 4),
    ("jumping", 4, 5),
    ("failed", 5, 8),
    ("waiting", 6, 6),
    ("running", 7, 6),
    ("review", 8, 6),
]


def checkerboard(size: tuple[int, int]) -> Image.Image:
    image = Image.new("RGBA", size, (248, 248, 248, 255))
    draw = ImageDraw.Draw(image)
    step = 16
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) % 2:
                draw.rectangle((x, y, x + step - 1, y + step - 1), fill=(226, 229, 233, 255))
    return image


def labeled_frame(frame: Image.Image, label: str) -> Image.Image:
    canvas = checkerboard((CELL_W, CELL_H + 24))
    canvas.alpha_composite(frame, (0, 24))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, CELL_W, 24), fill=(20, 24, 31, 255))
    draw.text((7, 6), label, fill=(255, 255, 255, 255), font=ImageFont.load_default())
    return canvas


def save_gif(frames: list[Image.Image], durations: list[int], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas")
    parser.add_argument("--frames-root", required=True)
    parser.add_argument("--preview-dir", required=True)
    args = parser.parse_args()

    atlas_path = Path(args.atlas).resolve()
    frames_root = Path(args.frames_root).resolve()
    preview_dir = Path(args.preview_dir).resolve()
    frames_root.mkdir(parents=True, exist_ok=True)
    preview_dir.mkdir(parents=True, exist_ok=True)

    with Image.open(atlas_path) as opened:
        atlas = opened.convert("RGBA")

    state_frames: dict[str, list[Image.Image]] = {}
    for state, row, count in STATES:
        state_dir = frames_root / state
        state_dir.mkdir(parents=True, exist_ok=True)
        extracted = []
        for column in range(count):
            frame = atlas.crop((column * CELL_W, row * CELL_H, (column + 1) * CELL_W, (row + 1) * CELL_H))
            frame.save(state_dir / f"{column:02d}.png")
            extracted.append(frame)
        state_frames[state] = extracted

    look_frames = []
    for index in range(16):
        row = 9 + index // 8
        column = index % 8
        look_frames.append(atlas.crop((column * CELL_W, row * CELL_H, (column + 1) * CELL_W, (row + 1) * CELL_H)))
    save_gif(look_frames, [120] * 16, preview_dir / "look-loop.gif")

    idle_jump = [state_frames["idle"][0], *state_frames["jumping"], state_frames["idle"][0]]
    save_gif(idle_jump, [320, 140, 140, 140, 140, 280, 360], preview_dir / "idle-jump-idle.gif")

    all_frames = []
    all_durations = []
    for state, _, _ in STATES:
        for frame in state_frames[state]:
            all_frames.append(labeled_frame(frame, state))
            all_durations.append(140)
        all_durations[-1] = 500
    save_gif(all_frames, all_durations, preview_dir / "all-states.gif")

    still_specs = [
        ("idle", 0, "01-idle"),
        ("running-right", 2, "02-running-right"),
        ("jumping", 2, "03-jump-peak"),
        ("review", 3, "04-review"),
    ]
    still_dir = preview_dir / "stills"
    still_dir.mkdir(parents=True, exist_ok=True)
    for state, index, name in still_specs:
        labeled_frame(state_frames[state][index], name.replace("-", " ")).save(still_dir / f"{name}.png")


if __name__ == "__main__":
    main()
