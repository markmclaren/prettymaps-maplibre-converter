#!/usr/bin/env python3.11
"""Static checks for handcrafted special style integration."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def assert_contains(path: Path, needle: str) -> None:
    text = path.read_text()
    if needle not in text:
        raise AssertionError(f"{path.name} does not contain expected text: {needle}")


def check_viewer(path: Path) -> None:
    text = path.read_text()
    expectations = [
        "'le-shine': 'outputs/special/le-shine.json'",
        "'ukiyoe': 'outputs/special/ukiyoe.json'",
        "const specialStyles = new Set(['le-shine', 'ukiyoe']);",
        "id: 'le-shine-paris'",
        "location: 'Paris, France'",
        "center: [2.3522, 48.8566]",
        "id: 'ukiyoe-museum-matsumoto'",
        "location: 'Japan Ukiyo-e Museum, Matsumoto, Japan'",
        "center: [137.9351, 36.2303]",
        "textureSelect.disabled = isSpecialStyle;",
        "Texture switching is disabled for special handcrafted styles",
    ]
    for needle in expectations:
        if needle not in text:
            raise AssertionError(f"{path.name} missing {needle}")


def check_style() -> None:
    style = json.loads((ROOT / "outputs/special/ukiyoe.json").read_text())
    meta = json.loads((ROOT / "assets/ukiyoe-sprite.json").read_text())
    meta_2x = json.loads((ROOT / "assets/ukiyoe-sprite@2x.json").read_text())
    if style.get("sprite") != "../../assets/ukiyoe-sprite":
        raise AssertionError("Ukiyo-e sprite URL is not relative to the assets sprite base")
    if set(meta) != set(meta_2x):
        raise AssertionError("Ukiyo-e 1x and 2x sprite metadata keys differ")
    patterns = [layer.get("paint", {}).get("fill-pattern") for layer in style.get("layers", [])]
    patterns = [pattern for pattern in patterns if pattern]
    missing = sorted(set(patterns) - set(meta))
    if missing:
        raise AssertionError(f"Ukiyo-e style references missing sprite patterns: {missing}")
    if len(patterns) < 5:
        raise AssertionError("Expected multiple patterned fill layers in Ukiyo-e style")
    for asset in [
        "assets/ukiyoe-sprite.png",
        "assets/ukiyoe-sprite.json",
        "assets/ukiyoe-sprite@2x.png",
        "assets/ukiyoe-sprite@2x.json",
    ]:
        if not (ROOT / asset).exists():
            raise AssertionError(f"Missing asset {asset}")
    print(f"Ukiyo-e style references {len(patterns)} patterned fill layers: {sorted(set(patterns))}")


def main() -> None:
    for viewer in [ROOT / "index.html", ROOT / "showcase_viewer.html"]:
        check_viewer(viewer)
    check_style()
    print("Special style integration checks passed.")


if __name__ == "__main__":
    main()
