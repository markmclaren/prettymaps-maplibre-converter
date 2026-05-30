import fs from 'node:fs';
import path from 'node:path';
import spec from '@maplibre/maplibre-gl-style-spec';

const validate = spec.validateStyleMin || spec.validateStyle;
const dir = process.argv[2] || 'outputs/all_presets';
const files = fs.readdirSync(dir).filter((name) => name.endsWith('.json')).sort();
let failures = 0;
const rows = [];
for (const file of files) {
  const full = path.join(dir, file);
  const style = JSON.parse(fs.readFileSync(full, 'utf8'));
  const errors = validate(style);
  if (errors && errors.length) {
    failures += 1;
    rows.push([file, 'FAIL', errors.map((e) => e.message || String(e)).join('; ')]);
  } else {
    rows.push([file, 'PASS', `${style.layers.length} layers`]);
  }
}
const lines = ['# MapLibre style-spec validation report\n', '| File | Status | Details |', '|---|---|---|'];
for (const [file, status, details] of rows) {
  lines.push(`| \`${file}\` | **${status}** | ${details.replaceAll('\n', '<br>')} |`);
}
fs.writeFileSync('maplibre_validation_report.md', lines.join('\n') + '\n');
console.log('maplibre_validation_report.md');
process.exit(failures);
