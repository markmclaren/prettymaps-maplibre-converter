# prettymaps to OpenFreeMap MapLibre converter

Convert [prettymaps](https://github.com/marceloprates/prettymaps) presets into MapLibre Style v8 JSON files that run on [OpenFreeMap](https://openfreemap.org/quick_start/) vector tiles.

Prettymaps presets are built for static Matplotlib renders over raw OSM geometries. This converter maps them to MapLibre styles over [OpenMapTiles](https://openmaptiles.org/) vector tiles, so the result is an approximation — the output won't be pixel-identical to a prettymaps render, but it gets the look and feel close enough.

> The end result is a standalone `.json` style you can load straight into MapLibre GL JS, backed by `https://tiles.openfreemap.org/planet` for tiles, sprites, and glyphs.

## Contents

| File or directory | Purpose |
|---|---|
| `prettymaps_to_maplibre.py` | Main converter CLI. |
| `conversion_design.md` | Design notes and mapping rationale. |
| `research_notes.md` | Research on prettymaps and OpenFreeMap internals. |
| `analysis_summary.md` | Inventory of prettymaps preset layers and OpenMapTiles source-layers. |
| `index.html` | GitHub Pages showcase viewer. |
| `showcase_extraction.md` | Extracted prettymaps example locations and preset associations. |
| `test_converter.py` | Smoke test — converts all built-in presets and checks JSON structure. |
| `validate_maplibre_styles.mjs` | Formal MapLibre style-spec validation. |
| `outputs/all_presets/` | Generated MapLibre styles for every built-in preset. |
| `outputs/all_presets_halftone/` | Same styles with halftone texture overlays. |
| `outputs/special/` | Hand-tuned special styles (Lè Shine, Ukiyo-e). |
| `assets/` | Sprite sheets for halftone and Ukiyo-e textures. |
| `test_report.md` | Smoke test results. |
| `maplibre_validation_report.md` | Style-spec validation results. |

## Quick start

Clone this repo and the prettymaps repo (so the converter can find the built-in presets):

```bash
git clone git@github.com:markmclaren/prettymaps-maplibre-converter.git
cd prettymaps-maplibre-converter
git clone https://github.com/marceloprates/prettymaps.git ./prettymaps
```

Run the converter with a built-in preset name or a path to your own preset JSON:

```bash
./prettymaps_to_maplibre.py default -o outputs/default-openfreemap.json --pretty --include-labels
```

For a self-hosted OpenFreeMap deployment, pass your domain:

```bash
./prettymaps_to_maplibre.py minimal \
  -o outputs/minimal-selfhosted.json \
  --domain https://maps.example.com \
  --pretty
```

Load the output straight into MapLibre GL JS:

```javascript
const map = new maplibregl.Map({
  container: 'map',
  style: 'outputs/default-openfreemap.json',
  center: [2.1734, 41.3851],
  zoom: 13
});
```

## Showcase viewer

`index.html` is an interactive MapLibre viewer with 18 places across 11 countries: **Stad van de Zon, Heerhugowaard** (Netherlands), **Praça Ferreira do Amaral, Macau**, **Eixample / Sagrada Família, Barcelona**, **Barra da Tijuca, Rio de Janeiro**, four **Porto Alegre** neighbourhoods (Bom Fim, Centro Histórico, Cidade Baixa, Farroupilha), **Honolulu**, **Garopaba**, **Haveforeningen Harekær, Copenhagen**, **Palmanova** (Italy), **Bourtange Fortress Museum** (Netherlands), **Palm Jebel Ali, Dubai**, **Paris** (Lè Shine style), and **Japan Ukiyo-e Museum, Matsumoto** (Ukiyo-e style). Each place loads with its closest converted preset. The **Style** dropdown lets you switch between all generated styles, and the **Texture** dropdown toggles between flat color and halftone overlays (halftone is on by default).

Since the converted style JSON files live under `outputs/`, GitHub Pages serves the page directly with no build step.

## Conversion model

The converter maps common prettymaps layers to OpenMapTiles source layers. It's an approximation — prettymaps can query arbitrary raw OSM tags, while OpenFreeMap serves a fixed tile schema.

| prettymaps concept | MapLibre/OpenMapTiles output | Notes |
|---|---|---|
| `background` | MapLibre `background` layer | Uses prettymaps `fc` as `background-color`. |
| `building` / `buildings` | `building` fill and optional outline | `palette` is reduced to the first color for deterministic JSON styling. |
| `streets` / `railway` | `transportation` line layers | Width dictionaries become zoom-dependent line-width expressions. |
| `water`, `sea` | `water` fill and optional outline | Excludes tunnel water where the tile attribute is available. |
| `waterway` | `waterway` line layers | Width classes like `river` and `stream` become class filters. |
| `green`, `park`, `garden`, `grass` | `park`, `landcover`, and `landuse` fills | Split across multiple source layers to approximate OSM tag groups. |
| `forest` | `landcover` wood fill | Tile class/subclass detail is less granular than raw OSM tags. |
| `beach` | `landcover` sand fill | Approximates natural beach/sand styling. |
| `parking`, `school`, `pedestrian`, `wetland`, `rock` | Best-effort OpenMapTiles filters | Unsupported or missing tile attributes get logged as warnings. |
| `perimeter` | Ignored | A MapLibre style doesn't crop the map to a circle/polygon; the app controls viewport bounds. |

## Supported prettymaps style keys

Only Matplotlib style properties that have a meaningful MapLibre counterpart are translated. Everything else goes into `metadata.conversion_warnings`.

| prettymaps key | MapLibre translation |
|---|---|
| `fc` | `fill-color`, inner `line-color`, or `background-color`. |
| `ec` | Outline or casing `line-color`. |
| `lw` | Outline or casing `line-width`. |
| `alpha` | `fill-opacity` or `line-opacity`. |
| `zorder` | Relative ordering of generated layer groups. |
| `palette` | First palette entry only. |
| `fill` | Suppresses polygon fill when `false`, while allowing outlines. |
| `hatch`, `hatch_c` | Reported as unsupported (would need custom sprite patterns). |

## Validation results

All ten built-in prettymaps presets were converted and passed both a local smoke test and the [MapLibre style spec validator](https://maplibre.org/maplibre-style-spec/).

| Artifact | Result |
|---|---|
| `test_report.md` | All presets converted successfully. |
| `maplibre_validation_report.md` | All styles passed formal validation. |
| `outputs/all_presets/*.json` | Ready-to-load styles for each preset. |

## Halftone texture mode

The converter supports a `--texture-mode halftone` flag that adds semi-transparent `fill-pattern` overlays to polygon layers. The sprite is at `assets/halftone-sprite.{json,png}`, and pre-generated textured styles live in `outputs/all_presets_halftone/`. In the showcase viewer, the **Texture** selector switches between flat and halftone (halftone is the default).

## Lè Shine-inspired style

`outputs/special/le-shine.json` is a standalone OpenFreeMap/MapLibre adaptation inspired by Mapbox's [Rise and Lè Shine](https://www.mapbox.com/blog/rise-and-le-shine) design. Monochromatic blue palette, halftone dot texture, globe-like feel — all fully static and GitHub Pages compatible. Available as the `le-shine` style option in the viewer.

## Ukiyo-e woodblock style

`outputs/special/ukiyoe.json` draws from Japanese Ukiyo-e landscape prints — warm washi-paper base, Prussian-blue water, indigo linework, muted greens, vermilion road accents, and a dedicated `assets/ukiyoe-sprite` atlas for wave, hatch, paper-grain, and building-grain fills. Available as the `ukiyoe` style option.

## Limitations

- **Not a pixel-for-pixel match** — prettymaps queries raw OSM features directly; OpenFreeMap serves a pre-built tile schema. The converter does its best to map one to the other, but some features won't line up.
- **No Matplotlib hatching** — hatch patterns need custom sprites. The halftone mode is a first step in that direction.
- **No per-feature building color randomisation** — prettymaps can pull from a full palette; the converter uses the first color for consistency.
- **Approximate green-space mapping** — OpenMapTiles splits parks, landcover, and landuse differently than OSM tag groups, so some categories get merged or missed.

If you want a closer match, load a converted style next to a prettymaps render of the same city and tweak the layer mapping table in `prettymaps_to_maplibre.py`. The whole thing is a single Python script, so adjusting it is straightforward.

## References

- [prettymaps](https://github.com/marceloprates/prettymaps) — the original presets
- [OpenFreeMap](https://openfreemap.org/quick_start/) — free vector tiles
- [MapLibre Style Specification](https://maplibre.org/maplibre-style-spec/) — the style format