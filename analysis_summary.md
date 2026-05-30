# Analysis summary

## prettymaps built-in presets

| Preset | Layers | Style layers | Style keys |
|---|---|---|---|
| `abraca-redencao` | building, forest, garden, green, park, perimeter, school, streets, water | background, building, forest, garden, green, park, perimeter, school, streets, water | `dilate, ec, fc, fill, lw, palette, zorder` |
| `barcelona-plotter` | building, green, streets | buildings, perimeter, streets | `draw, fill, penWidth, stroke` |
| `barcelona` | building, green, perimeter, streets | background, building, green, perimeter, streets, water | `alpha, ec, fc, fill, hatch, hatch_c, lw, palette, zorder` |
| `cb-bf-f` | building, forest, garden, park, streets, water | building, forest, garden, park, perimeter, streets, water | `ec, fc, fill, lw, palette, zorder` |
| `default` | beach, building, forest, green, parking, perimeter, rock, sea, streets, water, waterway | background, beach, building, forest, green, parking, perimeter, rock, sea, streets, water, waterway | `alpha, ec, fc, fill, hatch, hatch_c, lw, palette, zorder` |
| `heerhugowaard` | beach, building, forest, green, parking, perimeter, streets, water | background, beach, building, forest, green, parking, perimeter, streets, water | `alpha, ec, fc, fill, hatch, hatch_c, lw, palette, zorder` |
| `macao` | building, forest, green, parking, perimeter, streets, water | background, building, forest, green, parking, perimeter, streets, water | `alpha, ec, fc, hatch, hatch_c, lw, palette, zorder` |
| `minimal` | building, perimeter, streets | background, building, perimeter, streets | `ec, fc, fill, lw, zorder` |
| `plotter` | beach, building, forest, green, parking, perimeter, streets, water | background, beach, building, forest, green, parking, perimeter, streets, water | `` |
| `tijuca` | beach, building, grass, park, pedestrian, perimeter, streets, water, wetland | beach, building, grass, park, pedestrian, perimeter, streets, water, wetland | `ec, fc, fill, hatch, lw, zorder` |

## prettymaps layer frequency

| Layer | Preset count |
|---|---:|
| `streets` | 10 |
| `building` | 10 |
| `perimeter` | 8 |
| `water` | 7 |
| `green` | 7 |
| `forest` | 6 |
| `beach` | 4 |
| `parking` | 4 |
| `park` | 3 |
| `garden` | 2 |
| `school` | 1 |
| `waterway` | 1 |
| `sea` | 1 |
| `rock` | 1 |
| `grass` | 1 |
| `wetland` | 1 |
| `pedestrian` | 1 |
| `background` | 0 |
| `buildings` | 0 |

## prettymaps OSM tag filters observed

| Layer.tag | Count |
|---|---:|
| `building.building` | 10 |
| `water.natural` | 7 |
| `green.landuse` | 7 |
| `green.leisure` | 7 |
| `forest.landuse` | 6 |
| `building.landuse` | 5 |
| `green.natural` | 5 |
| `beach.natural` | 4 |
| `parking.amenity` | 4 |
| `parking.highway` | 4 |
| `parking.man_made` | 4 |
| `park.leisure` | 3 |
| `garden.leisure` | 2 |
| `building.leisure` | 1 |
| `school.amenity` | 1 |
| `water.amenity` | 1 |
| `garden.landuse` | 1 |
| `waterway.waterway` | 1 |
| `rock.natural` | 1 |
| `park.landuse` | 1 |
| `park.boundary` | 1 |
| `park.place` | 1 |
| `park.natural` | 1 |
| `park.amenity` | 1 |
| `grass.landuse` | 1 |
| `grass.natural` | 1 |
| `wetland.natural` | 1 |
| `pedestrian.area:highway` | 1 |

## prettymaps width classes observed

| Layer | Classes |
|---|---|
| `streets` | cycleway, footway, motorway, path, pedestrian, primary, residential, secondary, service, tertiary, trunk, unclassified |
| `waterway` | river, stream |

## prettymaps style key frequency

| Style key | Count |
|---|---:|
| `zorder` | 64 |
| `lw` | 59 |
| `ec` | 54 |
| `fc` | 51 |
| `hatch` | 21 |
| `hatch_c` | 11 |
| `fill` | 9 |
| `palette` | 6 |
| `alpha` | 4 |
| `stroke` | 2 |
| `dilate` | 1 |
| `draw` | 1 |
| `penWidth` | 1 |

## OpenFreeMap MapLibre source-layer usage across bundled styles

| Source layer | Layer count | Properties referenced | Representative layer IDs |
|---|---:|---|---|
| `transportation` | 178 | `brunnel, class, oneway, ramp, subclass` | tunnel-service-track-casing, tunnel-motorway-link-casing, tunnel-minor-casing, tunnel-link-casing, tunnel-secondary-tertiary-casing, tunnel-trunk-primary-casing, tunnel-motorway-casing, tunnel-path |
| `place` | 48 | `capital, class, rank` | label_other, label_village, label_town, label_state, label_city, label_city_capital, label_country_3, label_country_2 |
| `transportation_name` | 22 | `class, network, ref_length` | highway-name-path, highway-name-minor, highway-name-major, highway-shield-non-us, highway-shield-us-interstate, road_shield_us, highway_name_other, highway_name_motorway |
| `aeroway` | 20 | `class` | aeroway-taxiway-casing, aeroway-runway-casing, aeroway-area, aeroway-taxiway, aeroway-runway, aeroway-taxiway, aeroway-runway-casing, aeroway-area |
| `landcover` | 18 | `class, subclass` | landcover-glacier, landcover-wood, landcover-grass, landcover-ice-shelf, landcover-sand, landcover_ice_shelf, landcover_glacier, landcover_wood |
| `landuse` | 18 | `class, subclass` | landuse-residential, landuse-suburb, landuse-commercial, landuse-industrial, landuse-cemetery, landuse-hospital, landuse-school, landuse-railway |
| `waterway` | 16 | `brunnel, class, intermittent` | waterway_tunnel, waterway-other, waterway-other-intermittent, waterway-stream-canal, waterway-stream-canal-intermittent, waterway-river, waterway-river-intermittent, waterway_line_label |
| `boundary` | 15 | `admin_level, disputed, maritime` | boundary_3, boundary_2, boundary_disputed, boundary_state, boundary_country_z0-4, boundary_country_z5-, boundary_state, boundary_country_z0-4 |
| `water_name` | 8 | `—` | water_name_point_label, water_name_line_label, water_name, water_name, water_name_point_label, water_name_line_label, water_name_point_label, water_name_line_label |
| `poi` | 8 | `class, rank` | poi_r20, poi_r7, poi_r1, poi_transit, poi_r20, poi_r7, poi_r1, poi_transit |
| `park` | 7 | `class` | park, landcover-grass-park, park, park_outline, park, park_outline, park |
| `building` | 7 | `—` | building, building-top, building, building, building, building-3d, building |
| `(none)` | 6 | `—` | background, background, background, background, natural_earth, background |
| `water` | 6 | `brunnel, intermittent` | water, water-intermittent, water, water, water, water |
| `aerodrome_label` | 3 | `—` | airport, airport, airport |

## MapLibre layer type frequency

| Type | Count |
|---|---:|
| `line` | 211 |
| `symbol` | 98 |
| `fill` | 64 |
| `background` | 5 |
| `raster` | 1 |
| `fill-extrusion` | 1 |
