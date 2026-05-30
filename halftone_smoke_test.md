# Halftone viewer smoke test

The GitHub Pages viewer was served locally with `python3.11 -m http.server 8090` and opened at `http://127.0.0.1:8090/index.html`.

Validation checks completed:

- The base showcase map loaded successfully with the flat converted style.
- The **Texture** selector exposed `Flat color` and `Halftone overlays` options.
- Switching to `Halftone overlays` loaded the generated `outputs/all_presets_halftone/default.json` style.
- The viewer patches relative sprite URLs to absolute URLs before passing halftone style objects to MapLibre GL JS, which resolves the MapLibre runtime requirement for absolute sprite URLs.
- Browser console output after toggling halftone mode: no errors or warnings.
