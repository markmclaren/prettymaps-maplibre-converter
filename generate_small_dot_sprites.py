#!/usr/bin/env python3
"""Regenerate halftone sprite sheets — 2 staggered rows of dots, tiling seamlessly.

Produces assets/halftone-sprite.png and assets/halftone-sprite@2x.png
with corresponding JSON metadata files.

Layout: exactly 2 staggered rows of dots per tile (classic halftone pattern).

Dot sizes (dense halftone matching prettymaps reference):
  1x tiles (8×8):  1×1 pixel dots
  2x tiles (16×16): 2×2 pixel blocks

All dots positioned so dot extent never touches tile edge — both left/right
edges are empty (matching), and both top/bottom edges are empty (matching).
Hatch/cross patterns get a seam fix pass.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

ASSETS = Path("assets")
TILE_SIZE = 8
TILE_SIZE_2X = TILE_SIZE * 2  # 16

PATTERNS: list[str] = [
    "pm-water-dot",
    "pm-green-dot",
    "pm-forest-dot",
    "pm-beach-dot",
    "pm-wetland-cross",
    "pm-rock-speckle",
    "pm-surface-hatch",
]

DOT_COLOR = (160, 160, 160, 255)
LINE_COLOR = (160, 160, 160, 255)


# ---------------------------------------------------------------------------
# Seam fix helpers
# ---------------------------------------------------------------------------


def _seam_fix_1x(tile: Image.Image) -> None:
    w, h = tile.size
    for y in range(h):
        tile.putpixel((w - 1, y), tile.getpixel((0, y)))
    for x in range(w):
        tile.putpixel((x, h - 1), tile.getpixel((x, 0)))


def _seam_fix_2x(tile: Image.Image) -> None:
    w, h = tile.size
    for y in range(h):
        tile.putpixel((w - 1, y), tile.getpixel((0, y)))
    for x in range(w):
        tile.putpixel((x, h - 1), tile.getpixel((x, 0)))


# ---------------------------------------------------------------------------
# Line drawing (for hatch / cross patterns)
# ---------------------------------------------------------------------------


def _draw_line_1x(tile: Image.Image, x0: int, y0: int, x1: int, y1: int) -> None:
    w = TILE_SIZE
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while True:
        wx, wy = x % w, y % w
        tile.putpixel((wx, wy), LINE_COLOR)
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy


def _draw_line_2x(tile: Image.Image, x0: int, y0: int, x1: int, y1: int) -> None:
    w = TILE_SIZE_2X
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while True:
        wx, wy = x % w, y % w
        tile.putpixel((wx, wy), LINE_COLOR)
        tile.putpixel(((wx + 1) % w, wy), LINE_COLOR)
        tile.putpixel((wx, (wy + 1) % w), LINE_COLOR)
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy


# ---------------------------------------------------------------------------
# Dot drawing / placement
#
# 1x: 1×1 pixel dot at (x, y).
#     8×8 tile: rows at y=2 and y=6. Dots placed to avoid tile edges.
#
# 2x: 2×2 pixel block at (x, y) occupies x..x+1, y..y+1.
#     16×16 tile: rows at y=3 and y=11. Max safe x=14 (block 14-15).
# ---------------------------------------------------------------------------


def _dot_1x(tile: Image.Image, x: int, y: int) -> None:
    """Draw a 1×1 pixel dot at (x, y)."""
    tile.putpixel((x, y), DOT_COLOR)


def _dot_2x(tile: Image.Image, x: int, y: int) -> None:
    """Draw a 2×2 pixel block at (x, y)."""
    tile.putpixel((x, y), DOT_COLOR)
    tile.putpixel((x + 1, y), DOT_COLOR)
    tile.putpixel((x, y + 1), DOT_COLOR)
    tile.putpixel((x + 1, y + 1), DOT_COLOR)


def _place_dots_1x(tile: Image.Image, row_y: int, xs: list[int]) -> None:
    for x in xs:
        _dot_1x(tile, x, row_y)


def _place_dots_2x(tile: Image.Image, row_y: int, xs: list[int]) -> None:
    for x in xs:
        _dot_2x(tile, x, row_y)


# ---------------------------------------------------------------------------
# Tile builders — 1x (8×8 tiles with 1×1 dots)
# ---------------------------------------------------------------------------


def make_1x_tile(name: str) -> Image.Image:
    """8×8 tile: 2 staggered rows of 1×1 dots (rows at y=2 and y=6)."""
    tile = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))

    if name == "pm-water-dot":
        # Sparse: 4 dots/tile, ~5.7px spacing
        _place_dots_1x(tile, 2, [1, 5])
        _place_dots_1x(tile, 6, [3, 7])

    elif name == "pm-green-dot":
        # Dense: 7 dots/tile, ~3px spacing (staggered)
        _place_dots_1x(tile, 2, [0, 3, 6])
        _place_dots_1x(tile, 6, [1, 4, 7])

    elif name == "pm-forest-dot":
        # Medium: 5 dots/tile, ~4px spacing
        _place_dots_1x(tile, 2, [0, 4, 7])
        _place_dots_1x(tile, 6, [2, 6])

    elif name == "pm-beach-dot":
        # Sparse regular: 4 dots/tile
        _place_dots_1x(tile, 2, [0, 4])
        _place_dots_1x(tile, 6, [0, 4])

    elif name == "pm-wetland-cross":
        for i in range(-TILE_SIZE, TILE_SIZE * 2, 4):
            _draw_line_1x(tile, i, 0, i + TILE_SIZE, TILE_SIZE)
            _draw_line_1x(tile, i + TILE_SIZE, 0, i, TILE_SIZE)
        _seam_fix_1x(tile)

    elif name == "pm-rock-speckle":
        # Sparse staggered: 4 dots/tile
        _place_dots_1x(tile, 2, [2, 6])
        _place_dots_1x(tile, 6, [0, 4])

    elif name == "pm-surface-hatch":
        for i in range(-TILE_SIZE, TILE_SIZE * 2, 3):
            _draw_line_1x(tile, i, 0, i + TILE_SIZE, TILE_SIZE)
        _seam_fix_1x(tile)

    return tile


# ---------------------------------------------------------------------------
# Tile builders — 2x (16×16 tiles with 2×2 dot blocks)
# ---------------------------------------------------------------------------


def make_2x_tile(name: str) -> Image.Image:
    """16×16 tile: 2 staggered rows of 2×2 dot blocks (rows at y=3 and y=11)."""
    tile = Image.new("RGBA", (TILE_SIZE_2X, TILE_SIZE_2X), (0, 0, 0, 0))

    if name == "pm-water-dot":
        _place_dots_2x(tile, 3, [2, 10])
        _place_dots_2x(tile, 11, [6, 14])

    elif name == "pm-green-dot":
        _place_dots_2x(tile, 3, [0, 6, 12])
        _place_dots_2x(tile, 11, [3, 9, 14])

    elif name == "pm-forest-dot":
        _place_dots_2x(tile, 3, [0, 8, 14])
        _place_dots_2x(tile, 11, [4, 12])

    elif name == "pm-beach-dot":
        _place_dots_2x(tile, 3, [0, 8])
        _place_dots_2x(tile, 11, [0, 8])

    elif name == "pm-wetland-cross":
        for i in range(-TILE_SIZE_2X, TILE_SIZE_2X * 2, 6):
            _draw_line_2x(tile, i, 0, i + TILE_SIZE_2X, TILE_SIZE_2X)
            _draw_line_2x(tile, i + TILE_SIZE_2X, 0, i, TILE_SIZE_2X)
        _seam_fix_2x(tile)

    elif name == "pm-rock-speckle":
        _place_dots_2x(tile, 3, [4, 12])
        _place_dots_2x(tile, 11, [0, 8])

    elif name == "pm-surface-hatch":
        for i in range(-TILE_SIZE_2X, TILE_SIZE_2X * 2, 4):
            _draw_line_2x(tile, i, 0, i + TILE_SIZE_2X, TILE_SIZE_2X)
        _seam_fix_2x(tile)

    return tile


# ---------------------------------------------------------------------------
# Sprite packing
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


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