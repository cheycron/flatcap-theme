/* Optional: NODE_PATH=/path/to/node_modules node tests/sass-check.js */
const fs = require('node:fs');
const path = require('node:path');
const sass = require('sass');
const root = path.resolve(__dirname, '..');
const source = JSON.parse(fs.readFileSync(path.join(root, 'src/theme.json'), 'utf8'));
let passed = 0;
const compile = code => sass.compileString('@use "src/theme" as fc;\n' + code, {loadPaths:[root]}).css;
if (compile('') !== '') throw new Error('Import emits implicit CSS');
passed++;
for (const mode of ['slate', 'daylight']) {
  for (const contrast of ['standard', 'more']) {
    for (const density of ['comfortable', 'compact']) {
      const css = compile(`.sample { @include fc.tokens("${mode}", "${contrast}", "${density}"); color: fc.color("text.primary", "${mode}", "${contrast}"); font-family: fc.value("font.ui"); }`);
      const expected = {...source.typography, ...source.metrics, ...source.themes[mode], ...source.density[density], ...source.elevation[mode]};
      if (contrast === 'more') for (const key of Object.keys(expected)) if (key.startsWith('contrast.')) expected[key.slice(9)] = expected[key];
      for (const [key, value] of Object.entries(expected)) {
        const actual = css.match(new RegExp('--fc-' + key.replaceAll('.', '-') + ': ([^;]+);'))?.[1];
        if (actual !== value) throw new Error(`${mode}/${contrast}/${density} ${key}: ${actual} != ${value}`);
      }
      const ink = expected['text.primary'].toLowerCase();
      if (!css.toLowerCase().includes(`color: ${ink};`)) throw new Error('color() not resolved');
      passed++;
    }
  }
}
for (const code of [
  '.x { color:fc.color("missing"); }',
  '.x { color:fc.color("text.primary","missing"); }',
  '.x { color:fc.color("text.primary","slate","system"); }',
  '.x { x:fc.value("missing"); }',
  '.x { @include fc.tokens("slate","standard","tiny"); }',
  '.x { @include fc.tokens("slate","system"); }',
]) {
  let failed = false;
  try { compile(code); } catch { failed = true; }
  if (!failed) throw new Error('Accepted invalid API: ' + code);
  passed++;
}
console.log(JSON.stringify({version:source.version, sass:sass.info, checks:passed, passed}, null, 2));
