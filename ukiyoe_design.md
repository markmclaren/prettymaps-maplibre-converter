# Ukiyo-e / woodblock-print MapLibre style design

This style is a standalone special MapLibre style intended to sit beside `le-shine` in the GitHub Pages viewer. It uses the existing OpenFreeMap vector source and sprite-pattern mechanism, but applies a Japanese woodblock-print inspired palette and texture strategy rather than attempting to reproduce any copyrighted map style directly.

## Visual direction

The style should evoke nineteenth-century Ukiyo-e landscape prints through **warm washi paper land**, **Prussian-blue water**, **indigo linework**, **muted green vegetation**, **vermilion accents**, and subtle carved or printed surface texture. The map should remain legible at the showcase zooms and should avoid overly dense patterns that obscure OpenStreetMap geometry.

| Feature family | Treatment | Intended effect |
|---|---|---|
| Background and land | warm cream / aged paper fill | washi-paper base |
| Water | deep and mid Prussian blue with wave-line pattern | Hokusai-like water emphasis without literal illustration |
| Parks and vegetation | muted green with sparse bamboo/grass hatch pattern | hand-printed natural areas |
| Buildings | pale rice-paper blocks with dark indigo outlines | carved-block urban texture |
| Roads | light paper roads with indigo casing and occasional vermilion hierarchy | print-like route hierarchy |
| Labels | dark blue-gray text with pale halo | inked annotations on paper |
| Boundaries and minor lines | low-opacity indigo | engraved linework |

## Sprite assets

The existing halftone sprite already provides reusable pattern infrastructure. This addition should create a new `sprites/ukiyoe` sprite set with small transparent PNG patterns and matching JSON metadata.

| Sprite ID | Pattern | Primary use |
|---|---|---|
| `uk-water-wave` | thin horizontal/curved blue strokes | water fills |
| `uk-green-hatch` | sparse organic green hatching | parks, forests, grass, farmland |
| `uk-paper-grain` | very subtle tan flecks | land and background overlays |
| `uk-building-grain` | pale block-print speckle | building fills |
| `uk-red-hatch` | sparse vermilion diagonal strokes | selected road/feature accents if useful |

## MapLibre implementation

The style should be generated as `outputs/special/ukiyoe.json`. It should reference the OpenFreeMap vector source, the OpenFreeMap glyph endpoint, and the new `sprites/ukiyoe` sprite. Because GitHub Pages may serve the style from nested paths, the existing viewer logic for special styles should fetch the style JSON and absolutize relative sprite URLs before calling `map.setStyle()`.

The style should be built from a valid existing generated style, preferably `outputs/all_presets/default.json`, and then restyled programmatically. This keeps source-layer names, filters, zoom ranges, and label layers compatible with the OpenFreeMap schema while minimizing risk. Polygon fill layers should receive Ukiyo-e colors and selected `fill-pattern` values; line layers should be recolored with indigo/vermilion/paper tones; text layers should use ink-like text colors and light halos.

## Viewer integration

Add `ukiyoe` to the `styles` map and `specialStyles` set in both `index.html` and `showcase_viewer.html`. Add a showcase place card, ideally `ukiyoe-edo-water`, centered on a water-and-city-rich location such as Sumida / Asakusa in Tokyo. This makes the water wave pattern, compact urban geometry, parks, roads, and labels visible in one view.

## Validation

The implementation should run the existing static reference checks, formal MapLibre style validation, and a local browser smoke test. The smoke test should specifically select the `ukiyoe` option and confirm that there are no missing sprite images or console errors.
