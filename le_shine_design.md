# Lè Shine adaptation design

The repository will add a **Lè Shine–inspired** OpenFreeMap/MapLibre style rather than copying the original Mapbox-hosted style. The source article describes a monochromatic blue globe aesthetic with country color distinction, Futura-like labels, ocean currents, dot-patterned hill shading, and a split between low-zoom geographic structure and high-zoom urban detail. Because this repository targets OpenFreeMap vector tiles and static GitHub Pages hosting, the implementation will approximate those traits using the current OpenFreeMap source layers, generated style JSON, and local sprite assets.

| Reference trait | MapLibre/OpenFreeMap adaptation |
|---|---|
| Monochromatic blue palette | Apply a blue and cyan palette across land, water, roads, boundaries, labels, and natural areas. |
| Dot-patterned hill shading | Reuse the repository halftone sprite as subtle dotted overlays on parks, forests, beaches, and other polygon areas. |
| Country distinction | Tint land/background and boundaries in close blue values; use existing boundary layers where available. |
| Futura-like labels | Use the existing OpenFreeMap glyph stack with clean sans-serif label styling and high-contrast blue text halos. |
| Ocean currents | Approximate the mood with darker blue water and optional contour-like texture; true ocean-current geometry is not available in the current tile source. |
| High-zoom city detail | Keep roads, buildings, transit, POIs, and labels visible but recolored into the Lè Shine palette. |

The implementation will create `outputs/special/le-shine.json` as a standalone style derived from the validated converted `default` style. It will set the sprite to `assets/halftone-sprite`, recolor existing fill, line, circle, symbol, and background layers according to semantic layer IDs and source layers, and add `fill-pattern` overlays to selected natural polygon layers where MapLibre permits patterns. The viewer will expose this style as a normal style option, and texture handling will avoid rewriting the path into `outputs/all_presets_halftone/` for this special style.
