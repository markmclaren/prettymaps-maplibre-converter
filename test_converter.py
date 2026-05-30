#!/usr/bin/env python3
"""Smoke tests for prettymaps_to_maplibre.py."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path('/home/ubuntu/prettymaps-maplibre-converter')
PRESETS = Path('/home/ubuntu/prettymaps/prettymaps/presets')
OUTDIR = ROOT / 'outputs/all_presets'
REPORT = ROOT / 'test_report.md'

REQUIRED_LAYER_KEYS = {
    'background': {'id', 'type', 'paint'},
    'fill': {'id', 'type', 'source', 'source-layer', 'paint'},
    'line': {'id', 'type', 'source', 'source-layer', 'paint'},
    'symbol': {'id', 'type', 'source', 'source-layer'},
}


def validate_style(path: Path) -> list[str]:
    errors: list[str] = []
    data = json.loads(path.read_text())
    if data.get('version') != 8:
        errors.append('version is not 8')
    if 'sources' not in data or 'openmaptiles' not in data['sources']:
        errors.append('missing openmaptiles source')
    if not isinstance(data.get('layers'), list) or not data['layers']:
        errors.append('missing layers')
    ids = []
    for i, layer in enumerate(data.get('layers', [])):
        layer_type = layer.get('type')
        ids.append(layer.get('id'))
        req = REQUIRED_LAYER_KEYS.get(layer_type)
        if req is None:
            errors.append(f'layer {i} has unsupported type {layer_type!r}')
            continue
        missing = req - set(layer)
        if missing:
            errors.append(f"layer {layer.get('id', i)!r} missing keys {sorted(missing)}")
        if layer_type in {'fill', 'line', 'symbol'} and layer.get('source') != 'openmaptiles':
            errors.append(f"layer {layer.get('id', i)!r} has unexpected source {layer.get('source')!r}")
    if len(ids) != len(set(ids)):
        errors.append('duplicate layer ids')
    return errors


def main() -> int:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rows = []
    failures = 0
    for preset_path in sorted(PRESETS.glob('*.json')):
        output = OUTDIR / f'{preset_path.stem}.json'
        cmd = [str(ROOT / 'prettymaps_to_maplibre.py'), str(preset_path), '-o', str(output), '--pretty', '--include-labels']
        proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if proc.returncode != 0:
            failures += 1
            rows.append((preset_path.stem, 'FAIL', 'converter returned non-zero', proc.stderr.strip()))
            continue
        errors = validate_style(output)
        data = json.loads(output.read_text())
        warnings = data.get('metadata', {}).get('conversion_warnings', [])
        if errors:
            failures += 1
            rows.append((preset_path.stem, 'FAIL', '; '.join(errors), proc.stdout.strip()))
        else:
            rows.append((preset_path.stem, 'PASS', f"{len(data['layers'])} layers, {len(warnings)} warnings", ''))

    lines = ['# Converter smoke-test report\n', '| Preset | Status | Details | Notes |', '|---|---|---|---|']
    for preset, status, details, notes in rows:
        safe_notes = notes.replace('\n', '<br>')
        lines.append(f'| `{preset}` | **{status}** | {details} | {safe_notes} |')
    REPORT.write_text('\n'.join(lines) + '\n')
    print(REPORT)
    return failures


if __name__ == '__main__':
    raise SystemExit(main())
