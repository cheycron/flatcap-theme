# README visuals

These images present the Flatcap visual language and are linked by relative paths from the root README.

| Asset | Content |
| --- | --- |
| `overview.png` | Illustrative composition of the same semantic roles in Slate and Daylight. |
| `palette.png` | Selected color roles and exact values from the canonical JSON. |
| `example-slate.png` | The repository example in Slate. |
| `example-daylight.png` | The same example in Daylight. |
| `example-mobile.png` | The example at a 375px browser viewport. |

The overview and palette are presentation boards; the example images are screenshots of the HTML/CSS in `examples/`. All visible copy is in English.

## Update the images

From the repository root:

```sh
python3 scripts/build_visuals.py
python3 -m http.server 4188 --bind 127.0.0.1
```

The [board source](../../docs/visual-preview.html) is generated from [the canonical tokens](../../src/theme.json). Change the generator or the example rather than painting PNGs manually.

With Playwright available, capture the images using the repository helper:

```js
const fs = require('node:fs/promises');
const { chromium } = require('playwright');
const capture = require('./scripts/capture_visuals');
(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ deviceScaleFactor: 1 });
    await capture(page, {
      url: 'http://127.0.0.1:4188',
      // Optional local font fixtures; no public font service is required.
      // fontBaseURL: 'http://127.0.0.1:4188/.test-results/fonts',
      save: (name, png) => fs.writeFile(`images/readme/${name}.png`, png)
    });
  } finally { await browser.close(); }
})();
```

Inspect the images and update [the asset manifest](manifest.json) when changing inputs or captures. It records dimensions, input hashes and capture settings.

## Capture settings

Current images use Chromium 156.0.8078.79 at device scale factor 1. Presentation boards are 1440px wide; desktop examples are 1280px wide and the mobile example is 375px wide. All examples use standard contrast and comfortable spacing.

IBM Plex Sans Regular, Plex Sans Condensed Regular and Cascadia Code were supplied from local fixtures identified in [the font manifest](../../docs/evidence/font-manifest.json). Plex weights 500/600 may be synthesized. Fonts are not bundled with the repository or downloaded by the example. Font and browser versions can affect line wrapping and rasterization.

[Typography](../../docs/typography.md) · [Brand assets and attribution](../../docs/branding.md)
