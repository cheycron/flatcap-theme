# Brand and assets

**Flatcap** is one word with a capital F. The technical identifier is `flatcap`; the design direction is **Quiet precision**. Do not use “Flat Cap” or “Flat-Cap” as the official name.

## Masters and derivatives

| File | Use |
| --- | --- |
| `src/logo.svg` | Square symbol: graphite disc and mineral cap, with a vector viewBox |
| `src/readme_logo.svg` | Symbol, Flatcap wordmark, and Quiet precision descriptor |
| `images/logo.png` | 500×500 raster with transparent outer background |
| `images/readme_logo.png` | 415×600 raster with transparent outer background |

The SVGs include accessible titles/descriptions and `data-fc-role` fills that `scripts/build.py` resolves through `branding.roles` in the [canonical JSON](../src/theme.json). The brand uses a fixed Slate scheme; it does not recolor automatically with the product's mode.

Preserve aspect ratio, contours, and clear space of at least one cap-band height around the symbol. Do not crop the cap, stretch it, or add glow, shadows, or gradients. On surfaces that cannot support the light wordmark, use the symbol on its disc or a Slate backing rather than inventing an inverted variant.

## Mineral variant

The Mineral mark uses three related blues, without a teal band. Its brand-only colors do not change the interface palette.

| Part | Color | Source |
| --- | --- | --- |
| Cap crown | `#9BBFDF` | Slate `accent.fg` |
| Band | `#638BAA` | `branding.colors.cap.band` |
| Underside | `#344D62` | `branding.colors.cap.underside` |
| Disc | `#191D22` | Slate `bg.canvas` |

`branding.roles` resolves names from the selected theme and the dedicated values in `branding.colors`. The two brand-only blues are not UI tokens and do not change syntax, surfaces, or control contrast rules. Do not copy their hex values into components. Contrast between the mark's pieces does not communicate functional states.

The wordmark and descriptor are IBM Plex Sans outlines, so rendering does not depend on an installed font. The generator changes annotated fills only, not geometry or outlines. After generation, rasterize with `scripts/render_assets.py`; `--check` compares dimensions and RGBA pixels. Do not edit PNGs by hand.

## Accessible placement

For an HTML `<img>`, use `alt="Flatcap"` when it identifies the brand, or `alt=""` when adjacent text already provides the same information. Internal descriptions in an SVG linked as an image do not automatically replace the consumer's alt text.

Keep the mark separate from functional controls and status indicators. Apply the [design-system roles](design-system.md) to the surrounding interface rather than using brand-only colors as interaction tokens.

## Artwork attribution and permissions

The cap retains the pre-existing artwork geometry and attribution: **“Designed by Vexels.com - 2021 All Rights Reserved”**, with the original [Vexels terms link](https://vexels.com/terms-and-conditions/). Both SVG masters preserve this attribution. Cheycron, the repository owner, has confirmed permission to modify and reuse the symbol.

Preserve the attribution and honor the original permission terms. The repository's MIT license does not relicense the pre-existing third-party artwork or replace font licenses.

The lettering derives from [IBM Plex](https://github.com/IBM/plex), licensed under SIL OFL 1.1. No font binaries are included, and no exclusive rights are claimed over the letterforms. See [typography and distribution](typography.md).
