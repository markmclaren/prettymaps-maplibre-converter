# Halftone MapLibre implementation notes

The referenced SnailBones article demonstrates a practical MapLibre GL JS halftone technique based on generated SVG pattern images. The core approach is to create small SVG tiles in JavaScript, load each SVG into an `HTMLImageElement`, register the image in the active MapLibre style with `map.addImage`, and then assign the registered image names to polygon layers with the `fill-pattern` paint property.

Important implementation details:

- The pattern tile size controls the visual repeat interval, for example 4 px or 8 px square images.
- Dot size can be varied by generating several images such as `circle-1` through `circle-10` and selecting among them with a MapLibre expression such as `step`.
- The SVG can include a background `rect` so the pattern is opaque rather than transparent. This avoids lower fill layers showing through dot gaps.
- The same method can be applied to any fill layer, not only bathymetry; for this repository it can approximate prettymaps hatching and textured fills on water, parks, landcover, beaches, forests, and other polygon layers.
- For static style JSON files that should work from GitHub Pages, a robust alternative to runtime `addImage` is to generate an on-disk sprite PNG and corresponding sprite JSON, then set layer `fill-pattern` values to sprite icon names.

Source: https://snailbones.medium.com/halftone-bathymetry-in-maplibre-gl-js-b143651410c2
