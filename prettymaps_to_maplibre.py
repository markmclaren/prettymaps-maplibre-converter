#!/usr/bin/env python3
"""Convert prettymaps preset JSON files to OpenFreeMap-compatible MapLibre styles.

This converter translates the visual intent of a prettymaps preset into a
standalone MapLibre Style Specification v8 JSON document. It targets the
OpenMapTiles schema used by OpenFreeMap.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable

DEFAULT_DOMAIN = "https://tiles.openfreemap.org"
DEFAULT_PRESET_DIR = Path("/home/ubuntu/prettymaps/prettymaps/presets")
DEFAULT_BASE_STYLE = Path("/home/ubuntu/openfreemap-styles/styles/positron/style.json")
DEFAULT_HALFTONE_SPRITE = "assets/halftone-sprite"

COLOR_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")

ROAD_CLASS_MAP = {
    "motorway": "motorway",
    "trunk": "trunk",
    "primary": "primary",
    "secondary": "secondary",
    "tertiary": "tertiary",
    "residential": "minor",
    "unclassified": "minor",
    "service": "service",
    "track": "track",
    "path": "path",
    "footway": "path",
    "cycleway": "path",
    "pedestrian": "path",
    "steps": "path",
}

DEFAULT_ROAD_WIDTHS = {
    "motorway": 5.0,
    "trunk": 5.0,
    "primary": 4.5,
    "secondary": 4.0,
    "tertiary": 3.5,
    "minor": 3.0,
    "service": 2.0,
    "track": 2.0,
    "path": 1.5,
}

WATERWAY_CLASS_MAP = {
    "river": "river",
    "stream": "stream",
    "canal": "canal",
    "ditch": "ditch",
    "drain": "drain",
}

DEFAULT_WATERWAY_WIDTHS = {"river": 3.0, "canal": 2.2, "stream": 1.4, "ditch": 1.0, "drain": 1.0}

UNSUPPORTED_STYLE_KEYS = {"hatch", "hatch_c", "dilate", "draw", "penWidth", "stroke", "ls", "dashes"}


class ConversionContext:
    def __init__(self) -> None:
        self.warnings: list[str] = []
        self.unsupported_keys: dict[str, list[str]] = {}

    def warn(self, message: str) -> None:
        if message not in self.warnings:
            self.warnings.append(message)

    def record_unsupported(self, layer: str, keys: Iterable[str]) -> None:
        values = sorted(set(keys))
        if values:
            self.unsupported_keys[layer] = values
            for key in values:
                self.warn(f"Layer '{layer}' uses prettymaps key '{key}', which is only partially supported or unsupported in MapLibre.")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def resolve_preset(value: str) -> Path:
    candidate = Path(value)
    if candidate.exists():
        return candidate
    if not value.endswith(".json"):
        candidate = DEFAULT_PRESET_DIR / f"{value}.json"
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Could not find preset '{value}'. Pass a JSON path or a built-in prettymaps preset name.")


def normalize_domain(domain: str) -> str:
    return domain.rstrip("/")


def replace_domain_placeholders(obj: Any, domain: str) -> Any:
    if isinstance(obj, str):
        return obj.replace("https://__TILEJSON_DOMAIN__", domain).replace("__TILEJSON_DOMAIN__", domain.replace("https://", "").replace("http://", ""))
    if isinstance(obj, list):
        return [replace_domain_placeholders(x, domain) for x in obj]
    if isinstance(obj, dict):
        return {k: replace_domain_placeholders(v, domain) for k, v in obj.items()}
    return obj


def valid_color(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    if COLOR_RE.match(value):
        return True
    return value.startswith("rgb(") or value.startswith("rgba(") or value.startswith("hsl(") or value.startswith("hsla(")


def color_from_style(style: dict[str, Any], key: str, fallback: str, ctx: ConversionContext, layer: str) -> str:
    value = style.get(key)
    if isinstance(value, list) and value:
        ctx.warn(f"Layer '{layer}' uses a color list for '{key}'; MapLibre output uses the first color.")
        value = value[0]
    if valid_color(value):
        return str(value)
    if value is not None:
        ctx.warn(f"Layer '{layer}' has unsupported color value {value!r} for '{key}'; using {fallback}.")
    return fallback


def alpha_from_style(style: dict[str, Any], default: float = 1.0) -> float:
    value = style.get("alpha", default)
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return default


def lw_from_style(style: dict[str, Any], default: float = 0.0) -> float:
    value = style.get("lw", default)
    try:
        return max(0.0, float(value))
    except (TypeError, ValueError):
        return default


def style_fill_color(layer_name: str, style: dict[str, Any], ctx: ConversionContext, fallback: str = "#dddddd") -> str:
    if "palette" in style and isinstance(style["palette"], list) and style["palette"]:
        ctx.warn(f"Layer '{layer_name}' uses a palette; MapLibre output uses the first palette color for deterministic styling.")
        first = style["palette"][0]
        if valid_color(first):
            return first
    return color_from_style(style, "fc", fallback, ctx, layer_name)


def geom_filter(types: list[str]) -> list[Any]:
    return ["match", ["geometry-type"], types, True, False]


def eq_filter(prop: str, value: Any) -> list[Any]:
    return ["==", ["get", prop], value]


def match_filter(prop: str, values: list[Any]) -> list[Any]:
    return ["match", ["get", prop], values, True, False]


def all_filter(*parts: list[Any]) -> list[Any]:
    return ["all", *parts]


def fill_layer(layer_id: str, source_layer: str, filter_expr: list[Any], color: str, opacity: float = 1.0, minzoom: float | None = None, maxzoom: float | None = None) -> dict[str, Any]:
    layer: dict[str, Any] = {
        "id": layer_id,
        "type": "fill",
        "source": "openmaptiles",
        "source-layer": source_layer,
        "filter": filter_expr,
        "paint": {"fill-color": color, "fill-opacity": opacity, "fill-antialias": True},
    }
    if minzoom is not None:
        layer["minzoom"] = minzoom
    if maxzoom is not None:
        layer["maxzoom"] = maxzoom
    return layer


def outline_layer(layer_id: str, source_layer: str, filter_expr: list[Any], color: str, width: float, opacity: float = 1.0, minzoom: float | None = None) -> dict[str, Any]:
    layer: dict[str, Any] = {
        "id": layer_id,
        "type": "line",
        "source": "openmaptiles",
        "source-layer": source_layer,
        "filter": filter_expr,
        "layout": {"line-cap": "round", "line-join": "round"},
        "paint": {"line-color": color, "line-width": width, "line-opacity": opacity},
    }
    if minzoom is not None:
        layer["minzoom"] = minzoom
    return layer


def line_width_expression(widths_by_class: dict[str, float], zoom_scale: float = 1.0) -> list[Any]:
    match_items: list[Any] = ["match", ["get", "class"]]
    for klass, width in sorted(widths_by_class.items()):
        match_items.extend([klass, max(0.1, float(width))])
    match_items.append(1.0)
    return [
        "interpolate",
        ["exponential", 1.35],
        ["zoom"],
        9,
        ["*", match_items, 0.30 * zoom_scale],
        14,
        ["*", match_items, 1.00 * zoom_scale],
        20,
        ["*", match_items, 4.00 * zoom_scale],
    ]


def width_dict_to_omt(width_spec: Any, mapping: dict[str, str], defaults: dict[str, float], ctx: ConversionContext, layer_name: str) -> dict[str, float]:
    if isinstance(width_spec, dict) and width_spec:
        result: dict[str, float] = {}
        for source_class, width in width_spec.items():
            mapped = mapping.get(str(source_class))
            if mapped is None:
                ctx.warn(f"Layer '{layer_name}' width class '{source_class}' has no OpenMapTiles mapping and was ignored.")
                continue
            try:
                numeric = float(width)
            except (TypeError, ValueError):
                ctx.warn(f"Layer '{layer_name}' width for class '{source_class}' is not numeric and was ignored.")
                continue
            result[mapped] = max(result.get(mapped, 0.0), numeric)
        return result or defaults
    if isinstance(width_spec, (int, float)):
        return {klass: float(width_spec) for klass in defaults}
    return defaults


def build_road_layers(layer_name: str, layer_spec: dict[str, Any], layer_style: dict[str, Any], ctx: ConversionContext) -> list[dict[str, Any]]:
    fc = color_from_style(layer_style, "fc", "#ffffff", ctx, layer_name)
    ec = color_from_style(layer_style, "ec", fc, ctx, layer_name)
    lw = lw_from_style(layer_style, 0.0)
    opacity = alpha_from_style(layer_style)
    widths = width_dict_to_omt(layer_spec.get("width"), ROAD_CLASS_MAP, DEFAULT_ROAD_WIDTHS, ctx, layer_name)
    classes = sorted(widths)
    filter_expr = all_filter(geom_filter(["LineString", "MultiLineString"]), match_filter("class", classes), ["!=", ["get", "brunnel"], "tunnel"])
    width_expr = line_width_expression(widths)
    layers: list[dict[str, Any]] = []
    if lw > 0 and ec != fc:
        casing_widths = {klass: width + (lw * 2) for klass, width in widths.items()}
        casing_width = line_width_expression(casing_widths)
        layers.append({
            "id": f"pm-{layer_name}-casing",
            "type": "line",
            "source": "openmaptiles",
            "source-layer": "transportation",
            "filter": filter_expr,
            "layout": {"line-cap": "round", "line-join": "round"},
            "paint": {"line-color": ec, "line-width": casing_width, "line-opacity": opacity},
        })
    layers.append({
        "id": f"pm-{layer_name}-inner",
        "type": "line",
        "source": "openmaptiles",
        "source-layer": "transportation",
        "filter": filter_expr,
        "layout": {"line-cap": "round", "line-join": "round"},
        "paint": {"line-color": fc, "line-width": width_expr, "line-opacity": opacity},
    })
    return layers


def build_waterway_layers(layer_name: str, layer_spec: dict[str, Any], layer_style: dict[str, Any], ctx: ConversionContext) -> list[dict[str, Any]]:
    fc = color_from_style(layer_style, "fc", "#9bc3d4", ctx, layer_name)
    ec = color_from_style(layer_style, "ec", fc, ctx, layer_name)
    lw = lw_from_style(layer_style, 0.0)
    opacity = alpha_from_style(layer_style)
    widths = width_dict_to_omt(layer_spec.get("width"), WATERWAY_CLASS_MAP, DEFAULT_WATERWAY_WIDTHS, ctx, layer_name)
    classes = sorted(widths)
    filter_expr = all_filter(geom_filter(["LineString", "MultiLineString"]), match_filter("class", classes), ["!=", ["get", "brunnel"], "tunnel"])
    width_expr = line_width_expression(widths, zoom_scale=0.8)
    layers: list[dict[str, Any]] = []
    if lw > 0 and ec != fc:
        casing_widths = {klass: width + (lw * 2) for klass, width in widths.items()}
        casing_width = line_width_expression(casing_widths, zoom_scale=0.8)
        layers.append({
            "id": f"pm-{layer_name}-casing",
            "type": "line",
            "source": "openmaptiles",
            "source-layer": "waterway",
            "filter": filter_expr,
            "layout": {"line-cap": "round", "line-join": "round"},
            "paint": {"line-color": ec, "line-width": casing_width, "line-opacity": opacity},
        })
    layers.append({
        "id": f"pm-{layer_name}",
        "type": "line",
        "source": "openmaptiles",
        "source-layer": "waterway",
        "filter": filter_expr,
        "layout": {"line-cap": "round", "line-join": "round"},
        "paint": {"line-color": fc, "line-width": width_expr, "line-opacity": opacity},
    })
    return layers


def add_fill_and_outline(base_id: str, source_layer: str, filter_expr: list[Any], layer_style: dict[str, Any], ctx: ConversionContext, fallback: str, minzoom: float | None = None) -> list[dict[str, Any]]:
    color = style_fill_color(base_id, layer_style, ctx, fallback)
    ec = color_from_style(layer_style, "ec", color, ctx, base_id)
    lw = lw_from_style(layer_style, 0.0)
    opacity = alpha_from_style(layer_style)
    fill_enabled = layer_style.get("fill", True) is not False
    layers: list[dict[str, Any]] = []
    if fill_enabled:
        layers.append(fill_layer(f"pm-{base_id}", source_layer, filter_expr, color, opacity, minzoom=minzoom))
    if lw > 0:
        layers.append(outline_layer(f"pm-{base_id}-outline", source_layer, filter_expr, ec, lw, opacity, minzoom=minzoom))
    return layers


def build_polygon_semantic_layers(layer_name: str, layer_style: dict[str, Any], ctx: ConversionContext) -> list[dict[str, Any]]:
    poly = geom_filter(["Polygon", "MultiPolygon"])
    specs: list[tuple[str, str, list[Any], str, float | None]] = []
    name = layer_name.lower()

    if name in {"building", "buildings"}:
        specs.append((layer_name, "building", poly, "#d8d0c8", 12))
    elif name in {"water", "sea"}:
        specs.append((layer_name, "water", all_filter(poly, ["!=", ["get", "brunnel"], "tunnel"]), "#a8e1e6", None))
    elif name == "forest":
        specs.append((layer_name, "landcover", all_filter(poly, match_filter("class", ["wood"])), "#64B96A", None))
    elif name in {"green", "park", "garden"}:
        specs.extend([
            (f"{layer_name}-park", "park", poly, "#8BB174", None),
            (f"{layer_name}-grass", "landcover", all_filter(poly, match_filter("class", ["grass"])), "#8BB174", None),
            (f"{layer_name}-wood", "landcover", all_filter(poly, match_filter("class", ["wood"])), "#8BB174", None),
        ])
    elif name == "grass":
        specs.append((layer_name, "landcover", all_filter(poly, match_filter("class", ["grass"])), "#8BB174", None))
    elif name == "wetland":
        specs.append((layer_name, "landcover", all_filter(poly, match_filter("subclass", ["wetland"])), "#8BB174", None))
    elif name == "beach":
        specs.append((layer_name, "landcover", all_filter(poly, match_filter("class", ["sand"])), "#FCE19C", None))
    elif name == "rock":
        specs.append((layer_name, "landcover", all_filter(poly, match_filter("class", ["rock"])), "#BDC0BA", None))
    elif name == "parking":
        specs.extend([
            (f"{layer_name}-pier", "transportation", all_filter(poly, eq_filter("class", "pier")), "#F2F4CB", None),
            (f"{layer_name}-landuse", "landuse", all_filter(poly, match_filter("class", ["parking"])), "#F2F4CB", None),
        ])
    elif name == "school":
        specs.append((layer_name, "landuse", all_filter(poly, match_filter("class", ["school"])), "#e8dac6", None))
    elif name == "pedestrian":
        specs.append((layer_name, "transportation", all_filter(poly, match_filter("class", ["path", "minor"])), "#f5f1e9", None))
    else:
        ctx.warn(f"Layer '{layer_name}' has no built-in semantic mapping to OpenMapTiles and was ignored.")
        return []

    output: list[dict[str, Any]] = []
    for base_id, source_layer, filt, fallback, minzoom in specs:
        output.extend(add_fill_and_outline(base_id, source_layer, filt, layer_style, ctx, fallback, minzoom=minzoom))
    return output


def halftone_pattern_for_layer(layer_id: str) -> str | None:
    """Return a local sprite pattern for a generated prettymaps fill layer."""
    lid = layer_id.lower()
    if not lid.startswith("pm-") or lid.endswith("-outline") or lid.endswith("-halftone"):
        return None
    if any(token in lid for token in ["water", "sea"]):
        return "pm-water-dot"
    if any(token in lid for token in ["forest", "wood"]):
        return "pm-forest-dot"
    if any(token in lid for token in ["green", "park", "garden", "grass"]):
        return "pm-green-dot"
    if any(token in lid for token in ["beach", "sand"]):
        return "pm-beach-dot"
    if "wetland" in lid:
        return "pm-wetland-cross"
    if "rock" in lid:
        return "pm-rock-speckle"
    if any(token in lid for token in ["parking", "pedestrian", "school", "building"]):
        return "pm-surface-hatch"
    return None


def add_halftone_overlays(style_obj: dict[str, Any], sprite_url: str, ctx: ConversionContext) -> None:
    """Add semi-transparent pattern overlays above eligible fill layers."""
    existing_sprite = style_obj.get("sprite")
    if isinstance(existing_sprite, str):
        style_obj["sprite"] = [
            {"id": "default", "url": existing_sprite},
            {"id": "halftone", "url": sprite_url},
        ]
    elif isinstance(existing_sprite, list):
        if not any(item.get("id") == "halftone" for item in existing_sprite if isinstance(item, dict)):
            existing_sprite.append({"id": "halftone", "url": sprite_url})
    else:
        style_obj["sprite"] = [{"id": "halftone", "url": sprite_url}]

    textured_layers: list[dict[str, Any]] = []
    overlay_count = 0
    for layer in style_obj.get("layers", []):
        textured_layers.append(layer)
        if layer.get("type") != "fill":
            continue
        pattern = halftone_pattern_for_layer(str(layer.get("id", "")))
        if not pattern:
            continue
        overlay = deepcopy(layer)
        overlay["id"] = f"{layer['id']}-halftone"
        overlay["paint"] = {
            "fill-pattern": pattern,
            "fill-opacity": 0.72,
            "fill-antialias": True,
        }
        overlay["metadata"] = {"prettymaps:halftone_overlay": True}
        textured_layers.append(overlay)
        overlay_count += 1
    style_obj["layers"] = textured_layers
    style_obj["metadata"]["texture_mode"] = "halftone"
    style_obj["metadata"]["halftone_sprite"] = sprite_url
    style_obj["metadata"]["halftone_overlay_count"] = overlay_count
    ctx.warn(f"Halftone texture mode added {overlay_count} semi-transparent pattern overlay layer(s).")


def build_background_layer(style: dict[str, Any], ctx: ConversionContext) -> dict[str, Any]:
    return {
        "id": "background",
        "type": "background",
        "paint": {"background-color": color_from_style(style, "fc", "#f2f3f0", ctx, "background")},
    }


def layer_zorder(layer_name: str, styles: dict[str, dict[str, Any]]) -> float:
    spec = styles.get(layer_name, {}) if isinstance(styles.get(layer_name), dict) else {}
    try:
        return float(spec.get("zorder", 0))
    except (TypeError, ValueError):
        return 0.0


def extract_label_layers(base_style: dict[str, Any]) -> list[dict[str, Any]]:
    labels = []
    for layer in base_style.get("layers", []):
        if layer.get("type") == "symbol":
            labels.append(deepcopy(layer))
    return labels


def build_style(preset: dict[str, Any], preset_path: Path, args: argparse.Namespace) -> dict[str, Any]:
    ctx = ConversionContext()
    domain = normalize_domain(args.domain)
    layers_spec = preset.get("layers") or {}
    styles = preset.get("style") or {}
    if not isinstance(layers_spec, dict):
        raise ValueError("Preset 'layers' must be an object.")
    if not isinstance(styles, dict):
        raise ValueError("Preset 'style' must be an object.")

    style_obj: dict[str, Any] = {
        "version": 8,
        "name": args.name or f"prettymaps-{preset_path.stem}-openfreemap",
        "metadata": {
            "generator": "prettymaps_to_maplibre.py",
            "source_preset": str(preset_path),
            "conversion_model": "visual-semantic approximation from prettymaps Matplotlib styles to OpenMapTiles/MapLibre layers",
        },
        "sources": {
            "openmaptiles": {"type": "vector", "url": f"{domain}/planet"},
        },
        "sprite": f"{domain}/sprites/ofm_f384/ofm",
        "glyphs": f"{domain}/fonts/{{fontstack}}/{{range}}.pbf",
        "layers": [],
    }

    base_style: dict[str, Any] | None = None
    if args.base_style:
        base_style_path = Path(args.base_style)
        if base_style_path.exists():
            base_style = replace_domain_placeholders(load_json(base_style_path), domain)
            if args.reuse_base_sources:
                for key in ["sources", "sprite", "glyphs"]:
                    if key in base_style:
                        style_obj[key] = deepcopy(base_style[key])
        else:
            ctx.warn(f"Base style '{args.base_style}' was not found; generated style uses default OpenFreeMap source settings.")

    background_style = styles.get("background", {}) if isinstance(styles.get("background"), dict) else {}
    style_obj["layers"].append(build_background_layer(background_style, ctx))

    layer_names = sorted(set(layers_spec) | set(styles), key=lambda n: (layer_zorder(n, styles), n))
    for layer_name in layer_names:
        if layer_name in {"background", "perimeter"}:
            if layer_name == "perimeter":
                ctx.warn("Layer 'perimeter' is ignored because MapLibre styles do not define map bounds.")
            continue
        layer_style = styles.get(layer_name, {}) if isinstance(styles.get(layer_name), dict) else {}
        layer_spec = layers_spec.get(layer_name, {}) if isinstance(layers_spec.get(layer_name), dict) else {}
        ctx.record_unsupported(layer_name, set(layer_style) & UNSUPPORTED_STYLE_KEYS)
        if layer_name in {"streets", "railway"}:
            style_obj["layers"].extend(build_road_layers(layer_name, layer_spec, layer_style, ctx))
        elif layer_name == "waterway":
            style_obj["layers"].extend(build_waterway_layers(layer_name, layer_spec, layer_style, ctx))
        else:
            style_obj["layers"].extend(build_polygon_semantic_layers(layer_name, layer_style, ctx))

    if args.texture_mode == "halftone":
        add_halftone_overlays(style_obj, args.halftone_sprite, ctx)

    if args.include_labels:
        if base_style is None:
            base_path = DEFAULT_BASE_STYLE
            if base_path.exists():
                base_style = replace_domain_placeholders(load_json(base_path), domain)
            else:
                ctx.warn("No base style available for --include-labels; labels were not added.")
        if base_style is not None:
            style_obj["layers"].extend(extract_label_layers(base_style))

    style_obj["metadata"]["conversion_warnings"] = ctx.warnings
    style_obj["metadata"]["unsupported_prettymaps_style_keys"] = ctx.unsupported_keys
    style_obj["metadata"]["layer_count"] = len(style_obj["layers"])
    return style_obj


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert a prettymaps preset JSON to an OpenFreeMap-compatible MapLibre style JSON.")
    parser.add_argument("preset", help="Built-in prettymaps preset name, or path to a prettymaps preset JSON file.")
    parser.add_argument("-o", "--output", required=True, help="Output MapLibre style JSON path.")
    parser.add_argument("--domain", default=DEFAULT_DOMAIN, help=f"OpenFreeMap tile domain. Default: {DEFAULT_DOMAIN}")
    parser.add_argument("--name", default=None, help="Style name to write into the output JSON.")
    parser.add_argument("--include-labels", action="store_true", help="Append symbol label layers from an OpenFreeMap base style.")
    parser.add_argument("--base-style", default=str(DEFAULT_BASE_STYLE), help="Path to an OpenFreeMap base style JSON used for label reuse and optional sources.")
    parser.add_argument("--reuse-base-sources", action="store_true", help="Reuse sources/sprite/glyphs from --base-style after replacing OpenFreeMap placeholders.")
    parser.add_argument("--texture-mode", choices=["none", "halftone"], default="none", help="Optionally add prettymaps-like pattern overlays to polygon fill layers.")
    parser.add_argument("--halftone-sprite", default=DEFAULT_HALFTONE_SPRITE, help="Sprite URL prefix for halftone patterns, without .json/.png suffix.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print output JSON.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        preset_path = resolve_preset(args.preset)
        preset = load_json(preset_path)
        style = build_style(preset, preset_path, args)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8") as f:
            json.dump(style, f, indent=2 if args.pretty else None, ensure_ascii=False)
            f.write("\n")
        warnings = style.get("metadata", {}).get("conversion_warnings", [])
        print(f"Wrote {output} with {len(style['layers'])} layers and {len(warnings)} warning(s).")
        if warnings:
            print("Warnings:")
            for warning in warnings:
                print(f"- {warning}")
        return 0
    except Exception as exc:  # noqa: BLE001 - CLI should present user-friendly error.
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
