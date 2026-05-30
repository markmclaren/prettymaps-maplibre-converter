import fs from 'node:fs';
import path from 'node:path';
import * as specNamespace from '@maplibre/maplibre-gl-style-spec';
import specDefault from '@maplibre/maplibre-gl-style-spec';

const validate =
  specNamespace.validateStyleMin ||
  specNamespace.validateStyle ||
  specNamespace.validate ||
  specDefault?.validateStyleMin ||
  specDefault?.validateStyle ||
  specDefault?.validate;

if (typeof validate !== 'function') {
  throw new TypeError('Could not find a MapLibre style validation function in @maplibre/maplibre-gl-style-spec');
}

const target = process.argv[2] || 'outputs/all_presets';
const stat = fs.statSync(target);
const files = stat.isDirectory()
  ? fs.readdirSync(target).filter((name) => name.endsWith('.json')).sort().map((name) => path.join(target, name))
  : [target];

let failures = 0;
const rows = [];
for (const full of files) {
  const style = JSON.parse(fs.readFileSync(full, 'utf8'));
  const errors = validate(style);
  const displayName = path.relative(process.cwd(), full) || full;
  if (errors && errors.length) {
    failures += 1;
    rows.push([displayName, 'FAIL', errors.map((e) => e.message || String(e)).join('; ')]);
  } else {
    rows.push([displayName, 'PASS', `${style.layers.length} layers`]);
  }
}

const lines = ['# MapLibre style-spec validation report\n', '| File | Status | Details |', '|---|---|---|'];
for (const [file, status, details] of rows) {
  lines.push(`| \`${file}\` | **${status}** | ${details.replaceAll('\n', '<br>')} |`);
}
fs.writeFileSync('maplibre_validation_report.md', lines.join('\n') + '\n');
console.log('maplibre_validation_report.md');
process.exit(failures);
