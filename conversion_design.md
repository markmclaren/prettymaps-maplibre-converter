# Conversion design: prettymaps presets to OpenFreeMap MapLibre styles

## Goal and scope

The converter will transform the **visual intent** of a prettymaps preset into a standalone MapLibre Style Specification v8 JSON document that can be loaded by MapLibre GL JS with OpenFreeMap tiles. It does not attempt a lossless translation of raw OSM tag fetching. Prettymaps fetches raw OSM features and styles them with Matplotlib, while OpenFreeMap exposes generalized OpenMapTiles vector layers. The converter therefore maps common prettymaps semantic groups to their closest OpenMapTiles source layers and attributes.

## Style output structure

The generated file will contain a complete MapLibre style object with `version`, `name`, `metadata`, `sources`, `sprite`, `glyphs`, and `layers`. The source will be OpenFreeMap’s `openmaptiles` vector source. By default the public domain prefix is `https://tiles.openfreemap.org`; this can be overridden for self-hosted OpenFreeMap deployments. The converter may also preserve label layers from a supplied OpenFreeMap base style if the user passes `--include-labels`.

| Output component | Default behavior |
|---|---|
| `sources.openmaptiles` | `{ "type": "vector", "url": "https://tiles.openfreemap.org/planet" }` |
| `sprite` | `https://tiles.openfreemap.org/sprites/ofm_f384/ofm` |
| `glyphs` | `https://tiles.openfreemap.org/fonts/{fontstack}/{range}.pbf` |
| `layers` | Generated from prettymaps layer styles, ordered by `zorder` when available. |
| `metadata` | Includes source preset path, conversion warnings, and unsupported prettymaps keys. |

## Semantic layer mapping

The converter will use hand-written mappings for the built-in prettymaps layer vocabulary observed in the repository. Unknown layers are reported in `metadata.conversion_warnings` and ignored unless they can be recognized by generic hints.

| prettymaps layer | MapLibre output | OpenMapTiles source-layer | Filter strategy |
|---|---|---|---|
| `background` | `background` | none | MapLibre background paint. |
| `perimeter` | ignored | none | The MapLibre map viewport controls extent, not a Matplotlib polygon. |
| `water`, `sea` | fill plus optional outline | `water` | Polygon geometry and non-tunnel water. |
| `waterway` | line plus optional casing | `waterway` | Line geometry; optionally class `river`, `stream`, `canal` when width keys are present. |
| `building`, `buildings` | fill plus optional outline | `building` | All building polygons. |
| `streets`, `railway` | road casing and inner line layers | `transportation` | Road classes mapped from prettymaps highway width keys. |
| `parking` | fill plus optional outline | `transportation`, `landuse` | Piers from transportation and parking-like landuse where available. |
| `green`, `park`, `garden`, `grass` | fill plus optional outline | `park`, `landcover`, `landuse` | Park/grass/green classes split into several fill layers. |
| `forest` | fill plus optional outline | `landcover` | Wood/forest classes. |
| `beach` | fill plus optional outline | `landcover` | Sand/beach-like classes. |
| `wetland` | fill plus optional outline | `landcover` | Wetland subclass where available. |
| `rock` | fill plus optional outline | `landcover` | Rock/bare-rock-like classes where available. |
| `school` | fill plus optional outline | `landuse` | School class where available. |
| `pedestrian` | fill/line approximation | `transportation` | Pedestrian/path classes. |

## Style key translation

Matplotlib-oriented prettymaps properties are reduced to MapLibre `paint` and `layout` properties. Unsupported properties are recorded in metadata rather than silently treated as exact translations.

| prettymaps key | Meaning in prettymaps | MapLibre translation |
|---|---|---|
| `fc` | face/fill color | `fill-color` for polygons, `line-color` for inner road/waterway lines, `background-color` for background. |
| `ec` | edge/stroke color | outline `line-color` for polygons or casing `line-color` for roads. |
| `lw` | Matplotlib stroke width | outline/casing width in pixels. |
| `alpha` | opacity | `fill-opacity` or `line-opacity`. |
| `zorder` | draw order | Used to order generated layer groups. |
| `palette` | random feature fill palette | Uses the first palette color by default; optional future work could use feature-state or id-based expressions. |
| `hatch`, `hatch_c` | Matplotlib hatching | Not represented directly; `hatch_c` may be recorded but is otherwise unsupported because OpenFreeMap’s sprite set does not provide these hatch patterns. |
| `fill` | Matplotlib fill boolean | `false` prevents polygon fill where feasible; outlines may remain. |

## Road and waterway width translation

Prettymaps road widths are not pixel widths; they are used to buffer geometries in projected coordinates. In MapLibre, width is screen-pixel based and changes with zoom. The converter will turn width dictionaries into `match` expressions nested in `interpolate` zoom expressions. For example, `primary: 4.5` becomes a width that is narrow at low zoom, medium at city zoom, and wider at high zoom. Casing width adds approximately `2 * lw` pixels to the inner width.

## Known limitations

The converter cannot reproduce arbitrary OSM tag filters because OpenMapTiles has a different attribute schema from raw OSM. It cannot reproduce Matplotlib hatching unless a compatible sprite pattern is added. It cannot reproduce prettymaps’ random building palettes exactly in static MapLibre JSON. It also does not implement bounded/circular map extents; MapLibre extents are controlled by map initialization, not the style JSON.
