# Lè Shine viewer smoke test

The GitHub Pages viewer was served locally at `http://127.0.0.1:8091/index.html` and the style selector was switched to `le-shine`.

| Check | Result |
|---|---|
| Viewer page loads | **PASS** |
| `outputs/special/le-shine.json` loads | **PASS** |
| Relative sprite URL is absolutized by the viewer before `setStyle` | **PASS** |
| Halftone sprite image IDs match `fill-pattern` values | **PASS** |
| Browser console after selecting Lè Shine | **PASS** — no output |
| Formal MapLibre validation | **PASS** — 56 layers |

The earlier missing-image warnings were caused by generated `fill-pattern` names that did not match the generated sprite metadata. The generated styles now use sprite image IDs such as `pm-water-dot`, `pm-green-dot`, and `pm-surface-hatch` directly.
