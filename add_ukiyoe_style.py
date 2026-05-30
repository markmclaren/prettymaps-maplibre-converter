#!/usr/bin/env python3.11
"""Generate a Ukiyo-e / woodblock-print special MapLibre style and patch the viewer."""

from __future__ import annotations

import json
import math
from copy import deepcopy
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
SPECIAL = ROOT / "outputs" / "special"
BASE_STYLE = ROOT / "outputs" / "all_presets" / "default.json"
UKIYOE_STYLE = SPECIAL / "ukiyoe.json"

PATTERNS = [
    "uk-water-wave",
    "uk-green-hatch",
    "uk-paper-grain",
    "uk-building-grain",
    "uk-red-hatch",
]

PALETTE = {
    "paper": "#f2e4bf",
    "paper_deep": "#dcc694",
    "ink": "#22384f",
    "ink_soft": "#34566f",
    "water": "#1f5f91",
    "water_dark": "#143b64",
    "green": "#8fa56b",
    "green_dark": "#526b48",
    "building": "#e8d7aa",
    "vermilion": "#b64a34",
    "sand": "#d8b96e",
}


def hex_rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def draw_pattern(name: str, tile: int, scale: int) -> Image.Image:
    size = tile * scale
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    s = scale

    if name == "uk-water-wave":
        draw.rectangle([0, 0, size, size], fill=hex_rgba(PALETTE["water"], 235))
        stroke = hex_rgba("#dce8e6", 120)
        dark = hex_rgba(PALETTE["water_dark"], 95)
        for y in range(4 * s, size + 8 * s, 8 * s):
            for x in range(-8 * s, size, 16 * s):
                draw.arc([x, y - 5 * s, x + 14 * s, y + 5 * s], 8, 172, fill=stroke, width=max(1, 1 * s))
                draw.arc([x + 7 * s, y - 1 * s, x + 21 * s, y + 9 * s], 188, 352, fill=dark, width=max(1, 1 * s))
    elif name == "uk-green-hatch":
        draw.rectangle([0, 0, size, size], fill=hex_rgba(PALETTE["green"], 215))
        stroke = hex_rgba(PALETTE["green_dark"], 110)
        for x in range(-size, size * 2, 8 * s):
            draw.line([(x, size), (x + size, 0)], fill=stroke, width=max(1, 1 * s))
        for x in range(3 * s, size, 12 * s):
            draw.line([(x, 5 * s), (x + 4 * s, 1 * s)], fill=hex_rgba("#e9dfb8", 75), width=max(1, 1 * s))
    elif name == "uk-paper-grain":
        draw.rectangle([0, 0, size, size], fill=hex_rgba(PALETTE["paper"], 230))
        flecks = [
            (2, 3, 1), (7, 11, 1), (13, 5, 1), (20, 14, 1), (27, 2, 1),
            (30, 24, 1), (16, 25, 1), (4, 21, 1), (23, 29, 1), (10, 18, 1)
        ]
        for x, y, r in flecks:
            draw.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s], fill=hex_rgba(PALETTE["paper_deep"], 95))
    elif name == "uk-building-grain":
        draw.rectangle([0, 0, size, size], fill=hex_rgba(PALETTE["building"], 235))
        for y in range(2 * s, size, 7 * s):
            draw.line([(0, y), (size, y + 2 * s)], fill=hex_rgba(PALETTE["ink"], 35), width=max(1, 1 * s))
        for x in range(5 * s, size, 11 * s):
            draw.line([(x, 0), (x - 3 * s, size)], fill=hex_rgba(PALETTE["paper_deep"], 55), width=max(1, 1 * s))
    elif name == "uk-red-hatch":
        draw.rectangle([0, 0, size, size], fill=hex_rgba(PALETTE["paper"], 130))
        for x in range(-size, size * 2, 7 * s):
            draw.line([(x, size), (x + size, 0)], fill=hex_rgba(PALETTE["vermilion"], 150), width=max(1, 1 * s))
    return img


def write_sprite(scale: int) -> None:
    tile = 32
    w = tile * len(PATTERNS) * scale
    h = tile * scale
    atlas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    meta: dict[str, Any] = {}
    for idx, name in enumerate(PATTERNS):
        pattern = draw_pattern(name, tile, scale)
        atlas.alpha_composite(pattern, (idx * tile * scale, 0))
        meta[name] = {
            "width": tile,
            "height": tile,
            "x": idx * tile * scale,
            "y": 0,
            "pixelRatio": scale,
        }
    suffix = "@2x" if scale == 2 else ""
    atlas.save(ASSETS / f"ukiyoe-sprite{suffix}.png")
    (ASSETS / f"ukiyoe-sprite{suffix}.json").write_text(json.dumps(meta, indent=2) + "\n")


def layer_text(layer: dict[str, Any]) -> str:
    return " ".join(str(layer.get(k, "")) for k in ("id", "source-layer", "type")).lower()


def set_paint(layer: dict[str, Any], key: str, value: Any) -> None:
    layer.setdefault("paint", {})[key] = value


def restyle_layer(layer: dict[str, Any]) -> dict[str, Any]:
    l = deepcopy(layer)
    kind = l.get("type")
    text = layer_text(l)

    if kind == "background":
        l["paint"] = {"background-color": PALETTE["paper"]}
        return l

    if kind == "fill":
        paint = l.setdefault("paint", {})
        paint["fill-antialias"] = True
        if "water" in text or "ocean" in text:
            paint.update({"fill-color": PALETTE["water"], "fill-opacity": 0.96, "fill-pattern": "uk-water-wave"})
        elif any(k in text for k in ["park", "green", "grass", "forest", "wood", "landcover", "nature", "farmland", "wetland"]):
            paint.update({"fill-color": PALETTE["green"], "fill-opacity": 0.82, "fill-pattern": "uk-green-hatch"})
        elif any(k in text for k in ["building", "house"]):
            paint.update({"fill-color": PALETTE["building"], "fill-opacity": 0.92, "fill-pattern": "uk-building-grain"})
        elif any(k in text for k in ["beach", "sand"]):
            paint.update({"fill-color": PALETTE["sand"], "fill-opacity": 0.86, "fill-pattern": "uk-paper-grain"})
        else:
            paint.update({"fill-color": PALETTE["paper"], "fill-opacity": min(float(paint.get("fill-opacity", 0.72) or 0.72), 0.78), "fill-pattern": "uk-paper-grain"})
        return l

    if kind == "line":
        paint = l.setdefault("paint", {})
        if any(k in text for k in ["motorway", "trunk", "primary", "major"]):
            paint.update({"line-color": PALETTE["vermilion"], "line-opacity": 0.88})
        elif any(k in text for k in ["road", "street", "path", "track", "minor", "service"]):
            paint.update({"line-color": "#f8edce", "line-opacity": 0.92})
        elif "water" in text:
            paint.update({"line-color": "#dce8e6", "line-opacity": 0.68})
        elif any(k in text for k in ["outline", "boundary", "admin"]):
            paint.update({"line-color": PALETTE["ink_soft"], "line-opacity": 0.46})
        else:
            paint.update({"line-color": PALETTE["ink"], "line-opacity": min(float(paint.get("line-opacity", 0.7) or 0.7), 0.72)})
        if isinstance(paint.get("line-width"), (int, float)):
            paint["line-width"] = max(0.35, paint["line-width"] * 0.9)
        return l

    if kind == "symbol":
        paint = l.setdefault("paint", {})
        layout = l.setdefault("layout", {})
        if "text-field" in layout:
            paint.update({
                "text-color": PALETTE["ink"],
                "text-halo-color": "#f7e9c2",
                "text-halo-width": 1.2,
                "text-halo-blur": 0.25,
            })
        if "icon" in text:
            paint["icon-opacity"] = min(float(paint.get("icon-opacity", 0.8) or 0.8), 0.75)
        return l

    if kind == "circle":
        l.setdefault("paint", {}).update({"circle-color": PALETTE["vermilion"], "circle-stroke-color": PALETTE["ink"], "circle-opacity": 0.85})
        return l

    return l


def build_style() -> None:
    style = json.loads(BASE_STYLE.read_text())
    style["name"] = "Ukiyo-e woodblock inspired — OpenFreeMap"
    style["sprite"] = "../../assets/ukiyoe-sprite"
    style.setdefault("metadata", {})["prettymaps-maplibre-converter:special-style"] = "ukiyoe"
    style["metadata"]["description"] = "A Japanese woodblock-print inspired OpenFreeMap/MapLibre style with Prussian-blue water, washi-paper land, indigo linework, vermilion accents, and sprite-based printed textures."
    style["layers"] = [restyle_layer(layer) for layer in style.get("layers", [])]

    # Add a translucent paper-grain wash over non-water polygon areas where source-layer coverage exists.
    # Keep the base layer list schema intact; pattern fills above are the primary texture mechanism.
    SPECIAL.mkdir(parents=True, exist_ok=True)
    UKIYOE_STYLE.write_text(json.dumps(style, indent=2) + "\n")


def patch_viewer(path: Path) -> None:
    text = path.read_text()
    text = text.replace("'le-shine': 'outputs/special/le-shine.json'", "'le-shine': 'outputs/special/le-shine.json',\n      'ukiyoe': 'outputs/special/ukiyoe.json'")
    text = text.replace("const specialStyles = new Set(['le-shine']);", "const specialStyles = new Set(['le-shine', 'ukiyoe']);")
    le_card = """      {\n        id: 'le-shine-paris',\n        name: 'Lè Shine blue-globe style',\n        location: 'Paris, France',\n        source: \"Mapbox Lè Shine article-inspired special style\",\n        center: [2.3522, 48.8566],\n        zoom: 12.8,\n        bearing: -20,\n        pitch: 0,\n        style: 'le-shine',\n        note: 'A standalone blue, globe-inspired MapLibre style with subtle dotted polygon texture; shown over Paris as the home of Lè Shine.'\n      }"""
    uki_card = """      {\n        id: 'le-shine-paris',\n        name: 'Lè Shine blue-globe style',\n        location: 'Paris, France',\n        source: \"Mapbox Lè Shine article-inspired special style\",\n        center: [2.3522, 48.8566],\n        zoom: 12.8,\n        bearing: -20,\n        pitch: 0,\n        style: 'le-shine',\n        note: 'A standalone blue, globe-inspired MapLibre style with subtle dotted polygon texture; shown over Paris as the home of Lè Shine.'\n      },\n      {\n        id: 'ukiyoe-museum-matsumoto',\n        name: 'Ukiyo-e woodblock style',\n        location: 'Japan Ukiyo-e Museum, Matsumoto, Japan',\n        source: 'Japanese woodblock-print inspired special style',\n        center: [137.9351, 36.2303],\n        zoom: 14.2,\n        bearing: -18,\n        pitch: 0,\n        style: 'ukiyoe',\n        note: 'A standalone washi-paper, Prussian-blue, indigo, and vermilion MapLibre style with wave and hatch sprite textures; shown at the Japan Ukiyo-e Museum.'\n      }"""
    if "id: 'ukiyoe-museum-matsumoto'" not in text:
        text = text.replace(le_card, uki_card)
    path.write_text(text)


def patch_docs() -> None:
    readme = ROOT / "README.md"
    if readme.exists():
        txt = readme.read_text()
        if "outputs/special/ukiyoe.json" not in txt:
            insert = "\n### Ukiyo-e woodblock special style\n\nThis repository also includes `outputs/special/ukiyoe.json`, a standalone OpenFreeMap/MapLibre style inspired by Japanese Ukiyo-e landscape prints. It uses a warm washi-paper base, Prussian-blue water, indigo linework, muted green landcover, vermilion road accents, and a dedicated `assets/ukiyoe-sprite` texture atlas for wave, hatch, paper-grain, and building-grain fills. The GitHub Pages viewer exposes it as the `ukiyoe` style option.\n"
            marker = "### Lè Shine special style"
            if marker in txt:
                txt = txt.replace(marker, insert + "\n" + marker)
            else:
                txt += insert
            readme.write_text(txt)

    deliverables = ROOT / "DELIVERABLES.md"
    if deliverables.exists():
        txt = deliverables.read_text()
        if "outputs/special/ukiyoe.json" not in txt:
            txt += "\n## Ukiyo-e special style\n\nThe file `outputs/special/ukiyoe.json` provides a standalone Japanese woodblock-print inspired style. It is backed by `assets/ukiyoe-sprite.png`, `assets/ukiyoe-sprite.json`, and their `@2x` variants, and it is available in both GitHub Pages viewers as the `ukiyoe` style option. The design note is stored in `ukiyoe_design.md`.\n"
            deliverables.write_text(txt)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for scale in (1, 2):
        write_sprite(scale)
    build_style()
    for viewer in (ROOT / "index.html", ROOT / "showcase_viewer.html"):
        patch_viewer(viewer)
    patch_docs()
    print(f"Wrote {UKIYOE_STYLE.relative_to(ROOT)}")
    print("Wrote assets/ukiyoe-sprite.{json,png} and @2x variants")


if __name__ == "__main__":
    main()
