# Deliverables

This folder contains a working converter from prettymaps presets to OpenFreeMap-compatible MapLibre styles.

| Deliverable | Path |
|---|---|
| Main converter | `prettymaps_to_maplibre.py` |
| User documentation | `README.md` |
| Conversion design | `conversion_design.md` |
| Research notes | `research_notes.md` |
| Source analysis summary | `analysis_summary.md` |
| Browser example | `example_viewer.html` |
| Structural test script | `test_converter.py` |
| Formal MapLibre validator | `validate_maplibre_styles.mjs` |
| Generated converted styles | `outputs/all_presets/*.json` |
| Generated halftone styles | `outputs/all_presets_halftone/*.json` |
| Halftone sprite assets | `assets/halftone-sprite*.{json,png}` |
| Halftone design notes | `halftone_design.md` |
| Smoke-test report | `test_report.md` |
| Halftone smoke-test report | `halftone_smoke_test.md` |
| MapLibre validation report | `maplibre_validation_report.md` |
| Flat style validation report | `maplibre_validation_report_flat.md` |
| Halftone style validation report | `maplibre_validation_report_halftone.md` |

Validation status: all built-in prettymaps presets converted successfully, all generated flat styles passed MapLibre style-spec validation, and all generated halftone styles passed MapLibre style-spec validation.
