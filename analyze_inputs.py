#!/usr/bin/env python3
"""Summarize prettymaps presets and OpenFreeMap MapLibre styles."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path('/home/ubuntu')
PRESETS = ROOT / 'prettymaps/prettymaps/presets'
OFM_STYLES = ROOT / 'openfreemap-styles/styles'
OUT = ROOT / 'prettymaps-maplibre-converter/analysis_summary.md'


def jdump(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True)


def collect_expr_gets(expr: Any, out: set[str]) -> None:
    if isinstance(expr, list):
        if len(expr) >= 2 and expr[0] == 'get' and isinstance(expr[1], str):
            out.add(expr[1])
        for item in expr:
            collect_expr_gets(item, out)


def main() -> None:
    preset_rows = []
    style_keys = Counter()
    layer_names = Counter()
    layer_tag_keys = Counter()
    widths: dict[str, set[str]] = defaultdict(set)

    for path in sorted(PRESETS.glob('*.json')):
        data = json.loads(path.read_text())
        layers = data.get('layers') or {}
        style = data.get('style') or {}
        for lname, spec in layers.items():
            layer_names[lname] += 1
            if isinstance(spec, dict):
                for tag_key in (spec.get('tags') or {}).keys():
                    layer_tag_keys[f'{lname}.{tag_key}'] += 1
                for klass in (spec.get('width') or {}).keys():
                    widths[lname].add(str(klass))
        for lname, spec in style.items():
            layer_names[lname] += 0
            if isinstance(spec, dict):
                for key in spec.keys():
                    style_keys[key] += 1
        preset_rows.append({
            'preset': path.stem,
            'layers': ', '.join(sorted(layers.keys())),
            'style_layers': ', '.join(sorted(style.keys())),
            'style_keys': ', '.join(sorted({k for v in style.values() if isinstance(v, dict) for k in v.keys()})),
        })

    source_layer_counter = Counter()
    maplibre_type_counter = Counter()
    property_by_source = defaultdict(set)
    layer_ids_by_source = defaultdict(list)

    for path in sorted(OFM_STYLES.glob('*/style.json')):
        style = json.loads(path.read_text())
        for layer in style.get('layers', []):
            source_layer = layer.get('source-layer') or '(none)'
            source_layer_counter[source_layer] += 1
            maplibre_type_counter[layer.get('type', '(unknown)')] += 1
            layer_ids_by_source[source_layer].append(layer.get('id'))
            fields: set[str] = set()
            collect_expr_gets(layer.get('filter'), fields)
            collect_expr_gets(layer.get('paint'), fields)
            collect_expr_gets(layer.get('layout'), fields)
            property_by_source[source_layer].update(fields)

    lines = []
    lines.append('# Analysis summary\n')
    lines.append('## prettymaps built-in presets\n')
    lines.append('| Preset | Layers | Style layers | Style keys |')
    lines.append('|---|---|---|---|')
    for row in preset_rows:
        lines.append(f"| `{row['preset']}` | {row['layers']} | {row['style_layers']} | `{row['style_keys']}` |")

    lines.append('\n## prettymaps layer frequency\n')
    lines.append('| Layer | Preset count |')
    lines.append('|---|---:|')
    for name, count in layer_names.most_common():
        lines.append(f'| `{name}` | {count} |')

    lines.append('\n## prettymaps OSM tag filters observed\n')
    lines.append('| Layer.tag | Count |')
    lines.append('|---|---:|')
    for name, count in layer_tag_keys.most_common():
        lines.append(f'| `{name}` | {count} |')

    lines.append('\n## prettymaps width classes observed\n')
    lines.append('| Layer | Classes |')
    lines.append('|---|---|')
    for lname, classes in sorted(widths.items()):
        lines.append(f"| `{lname}` | {', '.join(sorted(classes))} |")

    lines.append('\n## prettymaps style key frequency\n')
    lines.append('| Style key | Count |')
    lines.append('|---|---:|')
    for key, count in style_keys.most_common():
        lines.append(f'| `{key}` | {count} |')

    lines.append('\n## OpenFreeMap MapLibre source-layer usage across bundled styles\n')
    lines.append('| Source layer | Layer count | Properties referenced | Representative layer IDs |')
    lines.append('|---|---:|---|---|')
    for source_layer, count in source_layer_counter.most_common():
        props = ', '.join(sorted(property_by_source[source_layer])) or '—'
        ids = ', '.join([x for x in layer_ids_by_source[source_layer][:8] if x])
        lines.append(f'| `{source_layer}` | {count} | `{props}` | {ids} |')

    lines.append('\n## MapLibre layer type frequency\n')
    lines.append('| Type | Count |')
    lines.append('|---|---:|')
    for key, count in maplibre_type_counter.most_common():
        lines.append(f'| `{key}` | {count} |')

    OUT.write_text('\n'.join(lines) + '\n')
    print(OUT)


if __name__ == '__main__':
    main()
