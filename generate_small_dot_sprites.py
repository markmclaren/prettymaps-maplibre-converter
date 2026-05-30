#!/usr/bin/env python3
"""Regenerate halftone sprite sheets with smaller, more numerous dots.

Produces assets/halftone-sprite.png and assets/halftone-sprite@2x.png
with corresponding JSON metadata files.

Uses explicit 3×3 pixel squares for dots (fully opaque at the sprite level).
Transparency is handled by the MapLibre fill-opacity on the overlay layer.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ASSETS = Path("assets")
TILE_SIZE = 16
TILE_SIZE_2X = TILE_SIZE * 2

PATTERNS: list[str] = [
    "pm-water-dot",
    "pm-green-dot",
    "pm-forest-dot",
    "pm-beach-dot",
    "pm-wetland-cross",
    "pm-rock-speckle",
    "pm-surface-hatch",
]

# Light grey dots that blend smoothly over fill colors
DOT_COLOR = (160, 160, 160, 255)  # fully opaque grey
LINE_COLOR = (160, 160, 160, 255)


def _draw_3x3_dot(tile: Image.Image, cx: int, cy: int) -> None:
    """Place a 3×3 pixel square at (cx, cy) as center."""
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            tile.putpixel((cx + dx, cy + dy), DOT_COLOR)


def make_1x_tile(name: str) -> Image.Image:
    """Create a 16×16 pattern tile."""
    tile = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))

    if name == "pm-water-dot":
        # 3 rows x 2 dots per row with 4px offset on odd rows
        for x in (2, 10):
            _draw_3x3_dot(tile, x, 2)
        for x in (6, 14):
            _draw_3x3_dot(tile, x, 7)
        for x in (2, 10):
            _draw_3x3_dot(tile, x, 12)

    elif name == "pm-green-dot":
        # 4 rows staggered
        for x in (2, 10):
            _draw_3x3_dot(tile, x, 2)
        for x in (6, 14):
            _draw_3x3_dot(tile, x, 5)
        for x in (2, 10):
            _draw_3x3_dot(tile, x, 9)
        for x in (6, 14):
            _draw_3x3_dot(tile, x, 12)

    elif name == "pm-forest-dot":
        # 4 rows, tighter spacing
        for x in (2, 9):
            _draw_3x3_dot(tile, x, 2)
        for x in (5, 12):
            _draw_3x3_dot(tile, x, 6)
        for x in (2, 9):
            _draw_3x3_dot(tile, x, 10)
        for x in (5, 12):
            _draw_3x3_dot(tile, x, 14)

    elif name == "pm-beach-dot":
        # 2 rows, sparse
        for x in (2, 10):
            _draw_3x3_dot(tile, x, 3)
        for x in (6, 14):
            _draw_3x3_dot(tile, x, 10)

    elif name == "pm-wetland-cross":
        for i in range(-TILE_SIZE, TILE_SIZE * 2, 4):
            for w in range(1):
                _draw_line_1x(tile, i, 0, i + TILE_SIZE, TILE_SIZE)
                _draw_line_1x(tile, i + TILE_SIZE, 0, i, TILE_SIZE)

    elif name == "pm-rock-speckle":
        for cx, cy in [(3, 3), (11, 3), (6, 7), (14, 7), (3, 11), (10, 13)]:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    tile.putpixel((cx + dx, cy + dy), DOT_COLOR)

    elif name == "pm-surface-hatch":
        for i in range(-TILE_SIZE, TILE_SIZE * 2, 3):
            _draw_line_1x(tile, i, 0, i + TILE_SIZE, TILE_SIZE)

    return tile


def _draw_line_1x(tile: Image.Image, x0: int, y0: int, x1: int, y1: int) -> None:
    """Draw a single-pixel-width diagonal line using a simple Bresenham-ish approach."""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while True:
        if 0 <= x < TILE_SIZE and 0 <= y < TILE_SIZE:
            tile.putpixel((x, y), LINE_COLOR)
            if x + 1 < TILE_SIZE:
                tile.putpixel((x + 1, y), LINE_COLOR)  # thicker line
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy


def make_2x_tile(name: str) -> Image.Image:
    """Create a 32×32 pattern tile for retina displays. Dots are 6×6 pixel blocks."""
    tile = Image.new("RGBA", (TILE_SIZE_2X, TILE_SIZE_2X), (0, 0, 0, 0))
    dot_color = DOT_COLOR

    def _dot(cx: int, cy: int) -> None:
        for dx in (-2, -1, 0, 1, 2):
            for dy in (-2, -1, 0, 1, 2):
                tile.putpixel((cx + dx, cy + dy), dot_color)

    if name == "pm-water-dot":
        for x in (4, 20):
            _dot(x, 4)
        for x in (12, 28):
            _dot(x, 14)
        for x in (4, 20):
            _dot(x, 24)

    elif name == "pm-green-dot":
        for x in (4, 20):
            _dot(x, 4)
        for x in (12, 28):
            _dot(x, 10)
        for x in (4, 20):
            _dot(x, 18)
        for x in (12, 28):
            _dot(x, 24)

    elif name == "pm-forest-dot":
        for x in (4, 18):
            _dot(x, 4)
        for x in (10, 24):
            _dot(x, 11)
        for x in (4, 18):
            _dot(x, 18)
        for x in (10, 24):
            _dot(x, 25)

    elif name == "pm-beach-dot":
        for x in (4, 20):
            _dot(x, 6)
        for x in (12, 28):
            _dot(x, 20)

    elif name == "pm-wetland-cross":
        for i in range(-TILE_SIZE_2X, TILE_SIZE_2X * 2, 6):
            _draw_line_2x(tile, i, 0, i + TILE_SIZE_2X, TILE_SIZE_2X)
            _draw_line_2x(tile, i + TILE_SIZE_2X, 0, i, TILE_SIZE_2X)

    elif name == "pm-rock-speckle":
        for cx, cy in [(5, 5), (15, 3), (8, 14), (20, 12), (5, 22), (16, 25), (26, 7), (13, 20)]:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    tile.putpixel((cx + dx, cy + dy), DOT_COLOR)

    elif name == "pm-surface-hatch":
        for i in range(-TILE_SIZE_2X, TILE_SIZE_2X * 2, 4):
            _draw_line_2x(tile, i, 0, i + TILE_SIZE_2X, TILE_SIZE_2X)

    return tile


def _draw_line_2x(tile: Image.Image, x0: int, y0: int, x1: int, y1: int) -> None:
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while True:
        if 0 <= x < TILE_SIZE_2X and 0 <= y < TILE_SIZE_2X:
            tile.putpixel((x, y), LINE_COLOR)
            if x + 1 < TILE_SIZE_2X:
                tile.putpixel((x + 1, y), LINE_COLOR)
            if y + 1 < TILE_SIZE_2X:
                tile.putpixel((x, y + 1), LINE_COLOR)
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy


def pack_sprite_1x() -> tuple[Image.Image, dict[str, dict]]:
    num = len(PATTERNS)
    sheet = Image.new("RGBA", (num * TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    meta: dict[str, dict] = {}
    for i, name in enumerate(PATTERNS):
        tile = make_1x_tile(name)
        x_offset = i * TILE_SIZE
        sheet.paste(tile, (x_offset, 0))
        meta[name] = {
            "width": TILE_SIZE,
            "height": TILE_SIZE,
            "x": x_offset,
            "y": 0,
            "pixelRatio": 1,
        }
    return sheet, meta


def pack_sprite_2x() -> tuple[Image.Image, dict[str, dict]]:
    gutter = 2
    step = TILE_SIZE_2X + gutter
    num = len(PATTERNS)
    total_width = num * step - gutter
    sheet = Image.new("RGBA", (total_width, TILE_SIZE_2X), (0, 0, 0, 0))
    meta: dict[str, dict] = {}
    for i, name in enumerate(PATTERNS):
        tile = make_2x_tile(name)
        x_offset = i * step
        sheet.paste(tile, (x_offset, 0))
        meta[name] = {
            "width": TILE_SIZE_2X,
            "height": TILE_SIZE_2X,
            "x": x_offset,
            "y": 0,
            "pixelRatio": 2,
        }
    return sheet, meta


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)

    print("Generating 1x sprite...")
    img1, meta1 = pack_sprite_1x()
    img1.save(str(ASSETS / "halftone-sprite.png"))
    (ASSETS / "halftone-sprite.json").write_text(json.dumps(meta1, indent=2) + "\n")
    print(f"  1x sprite: {img1.size}, {len(PATTERNS)} tiles")

    print("Generating 2x sprite...")
    img2, meta2 = pack_sprite_2x()
    img2.save(str(ASSETS / "halftone-sprite@2x.png"))
    (ASSETS / "halftone-sprite@2x.json").write_text(json.dumps(meta2, indent=2) + "\n")
    print(f"  2x sprite: {img2.size}, {len(PATTERNS)} tiles")

    # Quick verification
    for name in PATTERNS:
        m1 = meta1[name]
        m2 = meta2[name]
        tile1 = img1.crop((m1["x"], m1["y"], m1["x"] + m1["width"], m1["y"] + m1["height"]))
        tile2 = img2.crop((m2["x"], m2["y"], m2["x"] + m2["width"], m2["y"] + m2["height"]))
        px1 = sum(1 for p in tile1.getdata() if p[3] > 0)
        px2 = sum(1 for p in tile2.getdata() if p[3] > 0)
        print(f"  {name}: 1x={px1}px, 2x={px2}px")

    print("\nDone!")


if __name__ == "__main__":
    main()