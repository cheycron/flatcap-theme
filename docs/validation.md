# Maintainer verification record

This document records reproducible checks and historical evidence for maintainers. It is separate from Flatcap's visual presentation and design guidance.

## Current documentation and English example

The core presentation, linked guides, portable skill, and interactive example use English. The README presents the shared visual foundation rather than local implementation or external adapter status. Tokens and brand geometry are unchanged by this editorial update.

The English example was checked in Chromium **156.0.8078.79**, with **56/56** browser checks passing. The five README images were recaptured with that browser, standard contrast, comfortable spacing, and local font fixtures. Current input hashes, dimensions and capture settings are in [the visual manifest](../images/readme/manifest.json); [image maintenance instructions](../images/readme/README.md) describe the process. Browser/OS changes may alter pixels and line wrapping.

## Reproducible tools

From the repository root, with Python 3.10+:

```sh
python3 scripts/build.py --check
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

The generator checks the schema and detects stale exports without writing in `--check` mode. The color validator checks 372 defined pairs using unrounded WCAG 2.x sRGB contrast ratios. The Python suite covers generated exports, roles, SVG provenance and geometry, example resources and labels, portable skill structure, local links, visual manifests, and the English core presentation.

For optional PNG rendering, install the pinned packages in `scripts/requirements-assets.txt` in an isolated environment:

```sh
python3 scripts/render_assets.py --check
```

This compares decoded RGBA dimensions and pixels, not PNG compression bytes. Native Cairo and rasterizer versions affect cross-platform reproduction.

## Optional Sass checks

With Dart Sass available:

```sh
node tests/sass-check.js
# Or set NODE_PATH to an isolated installation's node_modules.
```

The suite covers `color()`, `value()`, `tokens()`, both modes, contrast and density choices, empty output from import alone, and invalid API inputs. LibSass is not supported. Tokens have no npm runtime dependency.

The preserved [Sass report](evidence/sass-report.json) records 15/15 checks with Dart Sass 1.93.2.

## Browser checks

`tests/browser-check.js` exports a runner receiving a Playwright `page` and `{url}` pointing to this repository's served `examples/` directory. It does not install dependencies. The optional `fontBaseURL` serves local QA fixtures; omitting it checks local families or fallbacks without establishing exact font availability.

```js
const { chromium } = require('playwright');
const run = require('./tests/browser-check');
(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage();
    console.log(JSON.stringify(await run(page, {
      url: 'http://127.0.0.1:4188/examples/'
    }), null, 2));
  } finally { await browser.close(); }
})();
```

The suite covers effective tokens, system preferences and manual overrides, independent density and Condensed choices, persistence, reflow, text scaling and spacing, keyboard focus, form feedback, literal ligatures, and a no-JavaScript baseline. Forced colors, reduced motion and other media preferences are Chromium emulations. Root text at 200% is not every browser or OS zoom mechanism.

The three font fixtures are identified by [their hashes](evidence/font-manifest.json). They are not distributed or downloaded by the example. Plex Regular and Cascadia were loaded for the current captures; Plex 500/600 may be synthesized. This does not cover every weight, script or glyph.

## Preserved historical evidence

- [Original browser report](evidence/browser-report.json): Chromium 154.0.8037.0, before the English editorial update. The original screenshots under `docs/evidence/` also predate the current presentation; do not confuse them with `images/readme/`.
- [Typography measurements](evidence/measurements.json), [upstream references](evidence/upstream.json), and [study image](evidence/typography-study.png): sample-specific horizontal advances, not reading performance or comfort measurements.
- [Implementation manifest](evidence/implementation-manifest.json): current source hashes and the scope of the recorded checks.

## Scope boundaries

Token checks and screenshots do not certify a whole product's WCAG conformance, display performance or user comfort. No screen-reader study, representative user study, Firefox/WebKit matrix, physical TN/IPS/OLED evaluation, OS rasterizer comparison, external adapter migration, or ANSI 0–15 implementation is established by these checks.

Font licenses and pre-existing artwork terms remain distinct from the repository's MIT code/token license. The owner confirmed permission to modify and reuse the symbol; see [brand attribution](branding.md). Verification does not authorize publication or deployment.
