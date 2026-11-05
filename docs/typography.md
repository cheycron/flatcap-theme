# Typography — Density without losing clarity

Flatcap uses a small set of complementary type roles: IBM Plex Sans for interfaces and reading, optional IBM Plex Sans Condensed for short dense labels, and Cascadia for code and terminals. Typography supports hierarchy and usable content—not decorative variety.

## 1. Type roles

| Role | Family | Usage |
| --- | --- | --- |
| UI, navigation, forms, and reading | **IBM Plex Sans** | Default proportional family for a consistent interface |
| Trees, lists, and dense textual columns | **IBM Plex Sans Condensed** | Optional for short labels where horizontal space matters |
| Code editor | **Cascadia Code** | Contextual programming ligatures, configurable weight, and continuity with the terminal |
| Terminal with icons | **Cascadia Code NF** | Nerd Fonts repertoire; use the exact family supported by the host |
| Logs, hashes, IDs, and literal comparisons | **Cascadia Mono / Mono NF**, or Code with ligatures disabled | Character-by-character visual representation |

The condensed family does **not** activate automatically with compact spacing. These are independent preferences: one controls glyph design, the other control spacing. Do not use `scaleX`, negative tracking, or smaller text to simulate condensation. Do not apply Condensed globally to paragraphs, critical instructions, or whole documents.

“IBM Plex” alone does not identify a specific width or role: the family includes Sans, Sans Condensed, Mono, and Serif. Flatcap does not require all text to be condensed.

## 2. Scale and layout

| Use | Nominal size | Line height | Weight |
| --- | --- | --- | --- |
| Documentation | 16px / 1rem | 26px / 1.625rem | 400 |
| Application body | 15px / .9375rem | 23–24px | 400 |
| Controls, tables, and dense labels | 14px / .875rem | 20px / 1.25rem | 400–500 |
| Noncritical metadata | 13px / .8125rem | 18–20px | 400 |
| Editor / terminal | 15px as a configurable starting point | 23–24px, depending on host | 400 |
| Section heading | 18px / 1.125rem | 26px | 600 |
| View title | 24px / 1.5rem | 32px | 600 |

The rem equivalents assume a 16px root; do not fix the root size to override user preferences. Do not shrink essential data to 12px to fit columns. Increase size or leading when the user or rasterization requires it. Weights 400/500/600 cover most needs; use 700 sparingly and avoid Light/Thin in small UI text. Do not require italic comments or prolonged uppercase navigation.

For long-form reading, start with a line length of roughly 60–75 characters; the default reading-width token is `70ch`. Let columns adapt rather than enforcing a universal fixed width. Nominally equal sizes do not guarantee equal perceived size across fonts: check x-height, apparent weight, wrapping, and fallback in the product.

Use growing containers, unrestricted zoom, and local scrolling for genuinely two-dimensional content. Support text at 200%, reflow at 320 CSS px, and WCAG 1.4.12 spacing overrides without losing content or functionality.

## 3. Applying the tokens

The [canonical typography values](../src/theme.json) are exported as CSS variables. Import [theme.css](../src/theme.css), then apply the roles in the consumer's styles; importing tokens does not apply body or component styles.

```css
body {
  font-family: var(--fc-font-ui);
  font-size: var(--fc-font-size-body);
  line-height: var(--fc-font-line-body);
}
.dense-label { font-family: var(--fc-font-dense); }
.code {
  font-family: var(--fc-font-code);
  font-variant-ligatures: contextual;
}
.literal {
  font-family: var(--fc-font-literal);
  font-variant-ligatures: none;
  font-feature-settings: "calt" 0, "liga" 0;
}
.numeric { font-variant-numeric: tabular-nums lining-nums; }
```

Do not disable `calt` globally: it may affect shaping in other languages. Limit literal selectors to the relevant technical content. In numeric tables, use tabular figures when supported, align values consistently—usually to the right—and retain separators and units. Do not turn all data into monospace.

Default stacks:

- **UI:** `"IBM Plex Sans", "Segoe UI", system-ui, sans-serif`.
- **Dense labels:** `"IBM Plex Sans Condensed", "IBM Plex Sans", system-ui, sans-serif`.
- **Code:** `"Cascadia Code", "Cascadia Code NF", "CaskaydiaCove Nerd Font Mono", ui-monospace, Consolas, monospace`.
- **Literal text:** `"Cascadia Mono", "Cascadia Mono NF", "Cascadia Code", ui-monospace, Consolas, monospace`.

A font stack does not install its families. Check actual availability, glyph coverage, and fallback metrics instead of assuming that a named family will render.

## 4. Ligatures and icons

- **Code** includes programming ligatures; **Mono** omits them. **PL** supplies Powerline symbols; **NF** supplies Nerd Fonts symbols. A non-NF variant does not guarantee every prompt icon.
- In editors, recommend contextual ligatures with a user option to disable them. Use standard italics; do not enable decorative cursive `ss01` by default.
- Disable ligatures in logs, IDs, hashes, and literal comparisons. `!=`, `=>`, or `===` may otherwise appear joined, but their original characters, copied text, and cell advances remain unchanged.
- Configure terminals with the exact installed NF family when needed. Upstream “Cascadia Code NF” and Nerd Fonts “CaskaydiaCove” are not interchangeable family names. Check cursor, selection, box drawing, Powerline, single-/double-width icons, and the host's cell-width handling. Installing a font does not guarantee emulator ligature support.
- Application icons use SVG with an accessible name or a visible label, not a private-use terminal glyph. No function should disappear when a terminal font is unavailable.

## 5. Loading and distribution

- For the web, prefer self-hosted WOFF2, pinned versions, language-appropriate subsets, and preserved licenses. Do not load an entire NF font for a few code blocks; use standard Code unless the repertoire is genuinely needed.
- Use `font-display: swap`; check fallback layout shifts, clipping, and coverage. Load only the families and weights the product uses.
- On desktop, Cascadia's upstream recommendation favors variable TTF, particularly on systems using TrueType hinting. Use static builds when required by the host. Do not assume every Plex family or format exposes the same variable axes.
- Do not apply global `-webkit-font-smoothing`, text strokes, or glyph scaling. Rasterizers and displays differ; one rendering override does not make them equivalent.
- IBM Plex and Cascadia use **SIL OFL 1.1**. Preserve licenses and respect reserved names when redistributing or modifying fonts; also review the terms of any patched build. Flatcap's MIT license does not replace font licenses.

## 6. Alternatives without multiplying families

| Alternative | When it fits | Integration guidance |
| --- | --- | --- |
| Inter | An established product using its screen-oriented variable family | Keep it when continuity matters; check size, wrapping, and fallback rather than assuming identical metrics |
| Source Sans 3 | A compact UI with a humanist tone | Use as a deliberate alternative, not another mandatory family |
| JetBrains Mono | User preference for its construction, x-height, and symbol differentiation | Check editor and terminal metrics and ligature preferences |
| IBM Plex Mono | Family continuity with Plex UI text | Do not assume an NF repertoire or programming ligatures equivalent to Cascadia |
| System font | Restricted loading, accessibility, or user preference | A valid fallback; metrics and rendering vary by platform |

Documentation shares Plex Sans with the interface. A serif can be a reader preference, not a mandatory third family; Merriweather is not required.

## 7. Product-level checks

Review the actual fonts and fallbacks in the target product at 100/125/150% scale, with 200% text, narrow layouts, and text-spacing overrides. Include accented text such as “Configuration,” “Résumé,” and “Ångström,” `Il1/O0/rn/m`, punctuation, hashes, tabular numbers, and the languages the product supports. Check selection and copied literal text as well as appearance.

Consider DirectWrite, FreeType, and CoreText where relevant, plus representative TN/IPS/OLED displays and ambient lighting. Check sustained reading, label recognition, and symbol confusion with people when those tasks are central. Font choice, static samples, and width measurements alone do not establish reading performance, comfort, or medical benefit.

## References

- [IBM Plex: families, formats, and licensing](https://github.com/IBM/plex)
- [Carbon typography](https://www.carbondesignsystem.com/building-blocks/foundations/typography) and [type sets](https://www.carbondesignsystem.com/building-blocks/foundations/typography/type-sets)
- [Cascadia Code: variants and OpenType features](https://github.com/microsoft/cascadia-code)
- [Inter](https://rsms.me/inter/)
- [Source Sans 3](https://github.com/adobe-fonts/source-sans)
- [JetBrains Mono](https://www.jetbrains.com/lp/mono/)
- [Nerd Fonts: patches, naming, and icon widths](https://github.com/ryanoasis/nerd-fonts)
- [WCAG text spacing](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html)

Flatcap uses its own type scale; using Plex does not imply implementation of Carbon or endorsement by a font's authors.
