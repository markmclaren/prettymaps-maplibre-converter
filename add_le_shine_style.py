from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE_STYLE = ROOT / "outputs" / "all_presets_halftone" / "default.json"
OUT_DIR = ROOT / "outputs" / "special"
OUT_STYLE = OUT_DIR / "le-shine.json"
INDEX = ROOT / "index.html"
SHOWCASE = ROOT / "showcase_viewer.html"
README = ROOT / "README.md"
DELIVERABLES = ROOT / "DELIVERABLES.md"

PALETTE = {
    "background": "#d7edf2",
    "land": "#c8e2ea",
    "land_alt": "#b9d8e4",
    "water": "#163f66",
    "water_deep": "#0e2f52",
    "park": "#9ec8d2",
    "forest": "#86b4c4",
    "sand": "#bfdbe2",
    "building": "#98bfce",
    "building_outline": "#6d9cad",
    "road_major": "#eef8fb",
    "road_minor": "#d9edf4",
    "road_outline": "#7daabb",
    "rail": "#477996",
    "boundary": "#3f7795",
    "label": "#12314e",
    "label_halo": "#dff4f8",
    "poi": "#245d80",
    "accent": "#ffffff",
    "pattern": "halftone-blue-dot-3",
}

TEXT_KEYS = {"text-color", "text-halo-color"}
FILL_COLOR_KEYS = {"fill-color", "fill-outline-color"}
LINE_COLOR_KEYS = {"line-color"}
CIRCLE_COLOR_KEYS = {"circle-color", "circle-stroke-color"}


def layer_text(layer: dict) -> str:
    parts = [layer.get("id", ""), layer.get("source-layer", "")]
    f = layer.get("filter")
    if f is not None:
        parts.append(json.dumps(f, ensure_ascii=False))
    return " ".join(parts).lower()


def classify(layer: dict) -> str:
    txt = layer_text(layer)
    lid = layer.get("id", "").lower()
    source_layer = layer.get("source-layer", "").lower()
    if layer.get("type") == "background":
        return "background"
    if "water" in txt or source_layer in {"water", "waterway"}:
        return "water"
    if any(word in txt for word in ["park", "forest", "wood", "grass", "nature", "landcover", "landuse", "garden", "wetland"]):
        return "natural"
    if any(word in txt for word in ["sand", "beach", "bare", "scrub"]):
        return "sand"
    if "building" in txt:
        return "building"
    if any(word in txt for word in ["motorway", "trunk", "primary", "secondary", "tertiary", "road", "street", "path", "track", "bridge", "tunnel"]):
        return "road"
    if any(word in txt for word in ["rail", "transit", "subway"]):
        return "rail"
    if any(word in txt for word in ["boundary", "admin", "country", "state"]):
        return "boundary"
    if any(word in txt for word in ["label", "place", "poi", "housenumber", "name"]):
        return "label"
    if layer.get("type") == "fill" and ("land" in lid or source_layer in {"landcover", "landuse"}):
        return "land"
    return "other"


def recolor(layer: dict) -> dict:
    layer = deepcopy(layer)
    kind = classify(layer)
    paint = layer.setdefault("paint", {})
    layout = layer.setdefault("layout", {}) if layer.get("type") == "symbol" else layer.get("layout", {})
    ltype = layer.get("type")

    if ltype == "background":
        paint["background-color"] = PALETTE["background"]

    elif ltype == "fill":
        if kind == "water":
            paint["fill-color"] = PALETTE["water"]
            paint["fill-opacity"] = paint.get("fill-opacity", 1)
        elif kind == "natural":
            paint["fill-color"] = PALETTE["park"]
            paint["fill-opacity"] = 0.78
            paint["fill-pattern"] = PALETTE["pattern"]
        elif kind == "sand":
            paint["fill-color"] = PALETTE["sand"]
            paint["fill-opacity"] = 0.82
            paint["fill-pattern"] = PALETTE["pattern"]
        elif kind == "building":
            paint["fill-color"] = PALETTE["building"]
            paint["fill-outline-color"] = PALETTE["building_outline"]
            paint["fill-opacity"] = 0.82
        elif kind == "boundary":
            paint["fill-color"] = PALETTE["land_alt"]
            paint["fill-opacity"] = 0.35
        else:
            paint["fill-color"] = PALETTE["land"]
            paint.setdefault("fill-opacity", 0.92)

    elif ltype == "line":
        if kind == "water":
            paint["line-color"] = PALETTE["water_deep"]
            paint["line-opacity"] = 0.65
        elif kind == "road":
            paint["line-color"] = PALETTE["road_major"] if any(w in layer_text(layer) for w in ["motorway", "trunk", "primary", "secondary"]) else PALETTE["road_minor"]
            paint["line-opacity"] = 0.88
        elif kind == "rail":
            paint["line-color"] = PALETTE["rail"]
            paint["line-opacity"] = 0.72
        elif kind == "boundary":
            paint["line-color"] = PALETTE["boundary"]
            paint["line-opacity"] = 0.62
        else:
            paint["line-color"] = PALETTE["road_outline"]
            paint.setdefault("line-opacity", 0.55)

    elif ltype == "circle":
        paint["circle-color"] = PALETTE["poi"]
        paint["circle-stroke-color"] = PALETTE["label_halo"]
        paint.setdefault("circle-stroke-width", 1)
        paint.setdefault("circle-opacity", 0.86)

    elif ltype == "symbol":
        if "text-field" in layout:
            paint["text-color"] = PALETTE["label"]
            paint["text-halo-color"] = PALETTE["label_halo"]
            paint["text-halo-width"] = paint.get("text-halo-width", 1.1) or 1.1
            paint["text-halo-blur"] = paint.get("text-halo-blur", 0.3) or 0.3
        if "icon-image" in layout:
            paint["icon-color"] = PALETTE["poi"]
            paint.setdefault("icon-opacity", 0.82)

    # Remove nulls that can trigger runtime validation failures in MapLibre.
    for group in (paint, layout if isinstance(layout, dict) else {}):
        for key in list(group.keys()):
            if group[key] is None:
                del group[key]
    return layer


def make_le_shine() -> None:
    style = json.loads(BASE_STYLE.read_text())
    style["name"] = "Lè Shine inspired — OpenFreeMap"
    style["metadata"] = style.get("metadata", {})
    style["metadata"].update({
        "prettymaps:style": "le-shine",
        "prettymaps:description": "Blue globe-inspired Lè Shine adaptation for OpenFreeMap/MapLibre, based on the public Mapbox design article rather than the proprietary Mapbox style.",
        "mapbox:autocomposite": False,
    })
    style["sprite"] = "../../assets/halftone-sprite"
    style["glyphs"] = style.get("glyphs", "https://tiles.openfreemap.org/fonts/{fontstack}/{range}.pbf")
    style["layers"] = [recolor(layer) for layer in style["layers"]]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_STYLE.write_text(json.dumps(style, indent=2, ensure_ascii=False) + "\n")


def patch_viewer(path: Path) -> None:
    text = path.read_text()
    if "'le-shine': 'outputs/special/le-shine.json'" not in text:
        text = text.replace(
            "      'plotter': 'outputs/all_presets/plotter.json'\n    };",
            "      'plotter': 'outputs/all_presets/plotter.json',\n      'le-shine': 'outputs/special/le-shine.json'\n    };",
        )
    if "specialStyles" not in text:
        text = text.replace(
            "    const places = [",
            "    const specialStyles = new Set(['le-shine']);\n\n    const places = [",
        )
    old = """    function styleUrl(styleKey) {
      const flatUrl = styles[styleKey];
      if (currentTexture === 'halftone') {
        return flatUrl.replace('outputs/all_presets/', 'outputs/all_presets_halftone/');
      }
      return flatUrl;
    }
"""
    new = """    function styleUrl(styleKey) {
      const flatUrl = styles[styleKey];
      if (specialStyles.has(styleKey)) return flatUrl;
      if (currentTexture === 'halftone') {
        return flatUrl.replace('outputs/all_presets/', 'outputs/all_presets_halftone/');
      }
      return flatUrl;
    }
"""
    if old in text:
        text = text.replace(old, new)
    if "style: 'le-shine'" not in text:
        insert_after = """      {
        id: 'garopaba',
        name: 'Garopaba',
        location: 'Santa Catarina, Brazil',
        source: "prettymaps.plot('Garopaba', radius = 5000)",
        center: [-48.6126, -28.0275],
        zoom: 12.8,
        bearing: 0,
        pitch: 0,
        style: 'default',
        note: 'A coastal keypoints example from the notebook; rendered here as an OpenFreeMap vector map.'
      }
"""
        le_place = """      {
        id: 'le-shine-globe',
        name: 'Lè Shine blue-globe style',
        location: 'Barcelona, Spain',
        source: "Mapbox Lè Shine article-inspired special style",
        center: [2.17557, 41.39491],
        zoom: 13.2,
        bearing: -20,
        pitch: 0,
        style: 'le-shine',
        note: 'A standalone blue, globe-inspired MapLibre style with subtle dotted polygon texture.'
      }
"""
        text = text.replace(insert_after, insert_after.rstrip() + ",\n" + le_place)
    if "Lè Shine" not in text[:5000]:
        text = text.replace(
            "applies the converted MapLibre styles created from the prettymaps presets.",
            "applies the converted MapLibre styles created from the prettymaps presets, plus a Lè Shine-inspired blue-globe style.",
        )
    path.write_text(text)


def patch_docs() -> None:
    readme = README.read_text()
    if "Lè Shine" not in readme:
        readme += "\n\n## Lè Shine-inspired style\n\nThis repository includes `outputs/special/le-shine.json`, a standalone OpenFreeMap/MapLibre adaptation inspired by Mapbox’s public **Rise and Lè Shine** design article. It uses a monochromatic blue palette and the existing halftone sprite assets to approximate the source style’s globe-like dot texture while remaining fully static and GitHub Pages compatible. The showcase viewer exposes it as the `le-shine` style option.\n"
        README.write_text(readme)
    deliverables = DELIVERABLES.read_text()
    if "le-shine.json" not in deliverables:
        deliverables += "\n\n## Lè Shine-inspired addition\n\nThe file `outputs/special/le-shine.json` provides a standalone blue-globe style inspired by Mapbox’s public Lè Shine article. The GitHub Pages viewer includes it in the style selector, and the accompanying notes are stored in `le_shine_research_notes.md` and `le_shine_design.md`.\n"
        DELIVERABLES.write_text(deliverables)


if __name__ == "__main__":
    make_le_shine()
    patch_viewer(INDEX)
    if SHOWCASE.exists():
        patch_viewer(SHOWCASE)
    patch_docs()
    print(f"Wrote {OUT_STYLE.relative_to(ROOT)}")
