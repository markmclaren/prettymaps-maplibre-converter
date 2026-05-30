# Lè Shine research notes

Source: https://blog.mapbox.com/rise-and-l%C3%A8-shine-c0eaf9a964d5

The Mapbox Lè Shine style was designed by Nathaniel Slaughter and is described as inspired by a physical globe. The key reference characteristics are:

- Monochromatic blue palette.
- Country distinction through color at low zooms.
- Futura-like place labels with hierarchy based on population.
- Predominant ocean currents at low zoom levels.
- Dot-patterned hill shading.
- Low zoom design emphasizes ocean currents, country polygons, natural and built-up areas, and place networks.
- Mid/high zoom design emphasizes road networks, cities, transit systems, and points of interest.
- The style is intended as a systematic, single-primary-color map whose palette can be adapted.

Implementation implications for this repo:

- Use OpenFreeMap vector layers rather than Mapbox-specific proprietary style URLs.
- Approximate the globe-inspired look with a blue-toned palette applied to land, water, roads, boundaries, labels, and natural polygons.
- Reuse or extend the existing halftone sprite system for dot-patterned landcover/terrain-like overlays, since OpenFreeMap does not expose the same Mapbox terrain/hillshade layers in the current style outputs.
- Add a standalone generated style file and viewer option, rather than treating Lè Shine as a prettymaps preset conversion.
