# Research notes: prettymaps to OpenFreeMap/MapLibre

## prettymaps model

The `prettymaps` project defines visual presets as JSON files under `prettymaps/prettymaps/presets`. A preset contains at least a `layers` object and a `style` object. The `layers` object controls which OSM features are fetched and grouped, usually via OSM tag dictionaries and sometimes via width maps for street/waterway-like line categories. The `style` object is effectively a Matplotlib styling dictionary keyed by layer name. Common fields are `fc` (face/fill color), `ec` (edge/stroke color), `lw` (line width), `alpha`, `zorder`, `hatch`, `hatch_c`, `palette`, and `fill`.

Rendering semantics from `draw.py`: polygon features are rendered with a fill patch and a separate silhouette/outline patch. For line-like layers (`streets`, `railway`, `waterway`), OSM line features are buffered into polygons using the preset `width` values before being drawn. `palette` is used for random per-feature fill selection, especially buildings. `background` is rendered as a Matplotlib background patch rather than a data layer. `zorder` controls the Matplotlib draw order.

Important limitation: prettymaps works from raw OSM data fetched through osmnx/geopandas and can filter by arbitrary OSM tags. OpenFreeMap serves OpenMapTiles vector tiles. The vector tile schema is derived from OSM but is already generalized and transformed into OpenMapTiles source layers and attributes. Therefore, conversion cannot be a perfect one-to-one translation of arbitrary OSM tag filters.

## OpenFreeMap/MapLibre model

OpenFreeMap quick-start uses MapLibre style URLs such as `https://tiles.openfreemap.org/styles/liberty`. The styles repository uses MapLibre Style Specification version 8 JSON. OpenFreeMap styles define an `openmaptiles` vector source with `url: https://__TILEJSON_DOMAIN__/planet`, `sprite: https://__TILEJSON_DOMAIN__/sprites/ofm_f384/ofm`, and `glyphs: https://__TILEJSON_DOMAIN__/fonts/{fontstack}/{range}.pbf`. In public hosted output, the placeholder should become `https://tiles.openfreemap.org`.

OpenFreeMap states that its map schema is unmodified OpenMapTiles. The relevant source layers found in the Positron style include `park`, `water`, `landcover`, `landuse`, `waterway`, `building`, `transportation`, `transportation_name`, `boundary`, `place`, `water_name`, `aeroway`, and `aerodrome_label`.

## Conversion implications

A practical converter should produce a new MapLibre style JSON, preserving OpenFreeMap `sources`, `sprite`, and `glyphs`, while generating or replacing style layers corresponding to prettymaps concepts. The strongest mapping is visual and semantic, not data-exact. For example, prettymaps `streets` should map to OpenMapTiles `transportation` line classes; `building` maps to `building` fill; `water` maps to `water`; `waterway` maps to `waterway`; `green`, `forest`, `beach`, `parking`, and `rock` require OpenMapTiles `park`, `landcover`, `landuse`, or `transportation` filters.

