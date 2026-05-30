# Halftone pattern design

This update adds a lightweight, static halftone system that fits GitHub Pages and the existing MapLibre style JSON workflow. MapLibre `fill-pattern` values must refer to images available in the style sprite, and seamless pattern images should use power-of-two dimensions such as 8 px or 16 px. The implementation therefore generates a local sprite sheet containing small dot, diagonal-dot, hatch, and crosshatch tiles, then writes the associated sprite JSON metadata next to it.

| Component | Decision | Rationale |
| --- | --- | --- |
| Pattern delivery | Local `assets/halftone-sprite.png` plus `assets/halftone-sprite.json` | Works on GitHub Pages without runtime image-generation dependencies. |
| Style integration | Optional `--texture-mode halftone` converter flag | Keeps the original flat-color styles available while enabling textured variants. |
| Sprite declaration | Multiple sprite sources with OpenFreeMap as `default` and local patterns as `halftone` | Preserves OpenFreeMap icons while allowing pattern references such as `halftone:pm-dot-4`. |
| Layer targeting | Polygon fill layers for water, green/park/grass/wood, forest, beach/sand, wetland, rock, and parking | These are the closest MapLibre equivalents to prettymaps filled/hatchable polygon features. |
| Visual strategy | Preserve the original `fill-color`, add `fill-pattern`, and use opaque pattern backgrounds derived from the layer color | Produces prettymaps-like texture while retaining each preset’s palette. |

The converter will infer a pattern family from the generated layer id and color. Water uses cool dot patterns, parks and forests use green diagonal dots, beaches use sparse dots, wetlands use crosshatch, rock uses small speckles, and parking/pedestrian-like surfaces use subtle hatch textures. Each generated style records the texture mode and sprite URL in its metadata.

References:

[1]: https://snailbones.medium.com/halftone-bathymetry-in-maplibre-gl-js-b143651410c2 "Halftone Bathymetry in MapLibre GL JS"
[2]: https://www.maplibre.org/maplibre-style-spec/sprite/ "MapLibre Style Spec: Sprite"
[3]: https://maplibre.org/maplibre-style-spec/layers/#paint-fill-fill-pattern "MapLibre Style Spec: fill-pattern"
