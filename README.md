# prettymaps to OpenFreeMap MapLibre converter

Experiment with prettymaps to MapLibre styles conversion.

This package contains a Python command-line converter that translates the visual intent of [`prettymaps`](https://github.com/marceloprates/prettymaps) preset JSON files into standalone MapLibre Style Specification v8 JSON files that use OpenFreeMap vector tiles. Prettymaps presets are designed for static Matplotlib rendering over raw OSM-derived geometries, whereas OpenFreeMap styles are MapLibre styles over OpenMapTiles vector tiles; consequently, the converter performs a **visual-semantic approximation** rather than a lossless data-schema conversion. See [prettymaps](https://github.com/marceloprates/prettymaps), [OpenFreeMap quick start](https://openfreemap.org/quick_start/), and the [MapLibre style specification](https://maplibre.org/maplibre-style-spec/).

> The practical outcome is a usable MapLibre style JSON that can be loaded with MapLibre GL JS and pointed at `https://tiles.openfreemap.org/planet`, using OpenFreeMap sprites and glyphs by default. See [OpenFreeMap quick start](https://openfreemap.org/quick_start/) and the [MapLibre style specification](https://maplibre.org/maplibre-style-spec/).

## Contents

| File or directory | Purpose |
|---|---|
| `prettymaps_to_maplibre.py` | Main converter CLI. |
| `conversion_design.md` | Detailed design notes and mapping rationale. |
| `research_notes.md` | Source-model research notes for prettymaps and OpenFreeMap. |
| `analysis_summary.md` | Inventory of built-in prettymaps preset layers and OpenFreeMap source-layer usage. |
| `index.html` | GitHub Pages showcase viewer for prettymaps example places. |
| `showcase_viewer.html` | Same showcase viewer retained as a named standalone page. |
| `showcase_extraction.md` | Extracted prettymaps example locations and preset associations used by the viewer. |
| `test_converter.py` | Smoke-test script that converts all built-in prettymaps presets and checks JSON structure. |
| `validate_maplibre_styles.mjs` | Formal MapLibre style-spec validation script. |
| `outputs/all_presets/` | Generated MapLibre styles for every built-in prettymaps preset. |
| `test_report.md` | Smoke-test results. |
| `maplibre_validation_report.md` | Formal style-spec validation results. |

## Quick start

Clone this repository first, then run the converter from the repo root.

```bash
git clone git@github.com:markmclaren/prettymaps-maplibre-converter.git
cd prettymaps-maplibre-converter
```

Also clone the prettymaps repository so the converter can load built-in preset JSON files from the source presets directory.

```bash
git clone https://github.com/marceloprates/prettymaps.git ./prettymaps
```

Run the converter with either a built-in prettymaps preset name or a path to a prettymaps preset JSON file. The default OpenFreeMap domain is `https://tiles.openfreemap.org`.

```bash
./prettymaps_to_maplibre.py default -o outputs/default-openfreemap.json --pretty --include-labels
```

If you are using a self-hosted OpenFreeMap deployment, pass your own domain. The converter will generate a style that uses your `planet`, `sprites`, and `fonts` endpoints.

```bash
./prettymaps_to_maplibre.py minimal \
  -o outputs/minimal-selfhosted.json \
  --domain https://maps.example.com \
  --pretty
```

The resulting JSON can be used directly in a MapLibre GL JS map:

```javascript
const map = new maplibregl.Map({
  container: 'map',
  style: 'outputs/default-openfreemap.json',
  center: [2.1734, 41.3851],
  zoom: 13
});
```

## GitHub Pages showcase

The repository root `index.html` is an interactive MapLibre viewer for the places used in the prettymaps examples notebook. It includes **Stad van de Zon, Heerhugowaard**, **Praça Ferreira do Amaral in Macau**, **Barcelona**, **Barra da Tijuca**, several **Porto Alegre** neighbourhoods, **Honolulu**, and **Garopaba**. Each place is paired with the closest converted prettymaps preset style, and the page also allows manual switching across all generated styles.

Because this repository already contains the converted style JSON files under `outputs/all_presets/`, GitHub Pages can serve the page directly from `index.html` without a build step.

## Conversion model

The converter maps the most common prettymaps layers to OpenMapTiles source layers. This is necessarily approximate because prettymaps can query arbitrary raw OSM tags, while OpenFreeMap exposes the already transformed OpenMapTiles schema. See [prettymaps](https://github.com/marceloprates/prettymaps) and [OpenFreeMap quick start](https://openfreemap.org/quick_start/).

| prettymaps concept | MapLibre/OpenMapTiles output | Notes |
|---|---|---|
| `background` | MapLibre `background` layer | Uses prettymaps `fc` as `background-color`. |
| `building` / `buildings` | `building` fill and optional outline | `palette` is reduced to the first color for deterministic JSON styling. |
| `streets` / `railway` | `transportation` line layers | Uses prettymaps width dictionaries to build zoom-dependent MapLibre line-width expressions. |
| `water`, `sea` | `water` fill and optional outline | Excludes tunnel water where the tile attribute is available. |
| `waterway` | `waterway` line layers | Width classes such as `river` and `stream` become OpenMapTiles class filters. |
| `green`, `park`, `garden`, `grass` | `park`, `landcover`, and `landuse` fills | Split across multiple OpenMapTiles source layers to approximate OSM tag groups. |
| `forest` | `landcover` wood fill | OpenMapTiles class/subclass detail is less granular than raw OSM tag filters. |
| `beach` | `landcover` sand fill | Approximates natural beach/sand styling. |
| `parking`, `school`, `pedestrian`, `wetland`, `rock` | Best-effort OpenMapTiles filters | Unsupported or absent tile attributes are reported as warnings. |
| `perimeter` | Ignored | A MapLibre style file does not define a circular or polygonal map crop; viewport bounds are controlled by the map application. |

## Supported prettymaps style keys

The converter intentionally handles only those Matplotlib style properties that have a meaningful MapLibre analogue. Unsupported keys are preserved as warnings in `metadata.conversion_warnings` so that manual follow-up remains transparent.

| prettymaps key | MapLibre translation |
|---|---|
| `fc` | `fill-color`, inner `line-color`, or `background-color`. |
| `ec` | Outline or casing `line-color`. |
| `lw` | Outline or casing `line-width`. |
| `alpha` | `fill-opacity` or `line-opacity`. |
| `zorder` | Relative ordering of generated layer groups. |
| `palette` | First palette entry only. |
| `fill` | Suppresses polygon fill when `false`, while allowing outlines. |
| `hatch`, `hatch_c` | Reported as unsupported unless custom sprite patterns are added later. |

## Validation results

The converter was tested against all ten built-in prettymaps presets found in the cloned repository. Each output passed both the local structural smoke test and the official [MapLibre style spec validator](https://maplibre.org/maplibre-style-spec/).

| Validation artifact | Result |
|---|---|
| `test_report.md` | All built-in prettymaps presets converted successfully. |
| `maplibre_validation_report.md` | All generated MapLibre styles passed formal validation. |
| `outputs/all_presets/*.json` | Ready-to-load generated styles for each built-in preset. |

## Important limitations and next improvements

This tool does **not** reproduce the exact raw OSM feature queries used by prettymaps because those queries happen before rendering, while OpenFreeMap serves a fixed vector-tile schema. It also does not reproduce Matplotlib hatching or random per-feature building palettes. These can be improved by adding a custom sprite sheet with hatch patterns, introducing a deterministic feature-id color expression where tile data supports it, or creating preset-specific post-processing rules for a known OpenMapTiles schema variant.

If you want a closer visual match, the best next step is to load a converted style in a MapLibre viewer, compare it against a prettymaps render for the same city, then tune the layer mapping table in `prettymaps_to_maplibre.py`. The converter is intentionally written as a single readable Python script so that the mapping can be adapted quickly.

## References

- [`prettymaps`](https://github.com/marceloprates/prettymaps) — prettymaps GitHub repository
- [OpenFreeMap quick start](https://openfreemap.org/quick_start/) — OpenFreeMap quick start
- [MapLibre style specification](https://maplibre.org/maplibre-style-spec/) — MapLibre Style Specification


## Halftone texture mode

The converter now supports an optional `--texture-mode halftone` flag that adds semi-transparent `fill-pattern` overlays to selected polygon layers. The repository includes a GitHub Pages-compatible sprite at `assets/halftone-sprite.{json,png}` and pre-generated textured styles in `outputs/all_presets_halftone/`. In the showcase viewer, use the **Texture** selector to switch between the original flat-color conversion and the halftone overlay variant.


## Lè Shine-inspired style

This repository includes `outputs/special/le-shine.json`, a standalone OpenFreeMap/MapLibre adaptation inspired by Mapbox’s public **Rise and Lè Shine** design article. It uses a monochromatic blue palette and the existing halftone sprite assets to approximate the source style’s globe-like dot texture while remaining fully static and GitHub Pages compatible. The showcase viewer exposes it as the `le-shine` style option.
