# Flatcap 2.0 — Quiet precision

**Token version:** `2.0.0`. Flatcap is a core visual scheme and design foundation for focused work: editors, terminals, administrative tools, documentation, and data-rich interfaces. See [integration](usage.md), [typography](typography.md), and the [palette](palette.md).

> The interface organizes. Content takes the foreground. Color informs.

## 1. Design direction

Near-neutral graphite, mineral blue, restrained accents, and typography without decorative gestures. Professional without bureaucracy; quiet without hiding information. Matte surfaces, clear hierarchy, and purposeful interaction define the system—not a fixed page composition or a collection of colored buttons.

**Principles:**

1. Reduce visual competition, not legibility.
2. Essential differences must remain clear without color.
3. Give each role a token and each color pairing an intended surface.
4. Use one interaction accent; do not turn everything into a call to action.
5. Control density through spacing, not tiny text.
6. Design for real rasterizers and the sRGB gamut.
7. Let users control mode, scale, contrast, and motion.

## 2. Workflows and composition

- **Development:** explore files → read code → edit → review diagnostics → run. Syntax supports scanning; focus and errors remain unambiguous.
- **Operations:** find a service → compare metrics → filter a table → address an incident. Make the table central rather than building a wall of cards.
- **Administration:** complete a form → correct an error → save → receive persistent confirmation. Use real labels, keyboard navigation, and errors that do not rely on color alone.
- **Reading:** find documentation → read → navigate between sections. Start with a line length of roughly 60–75 characters and configurable text size.

Navigation structure belongs to the product. Flatcap defines surfaces and patterns, not a universal sitemap. Prefer spacing, alignment, headings, and tables over enclosing every block in a card.

## 3. Two modes, not an inversion

**Slate:** the primary dark mode for users who prefer it and environments with controlled lighting. Its `#191D22` canvas supports separation without relying on nearly black details. Pure black is not the normal background.

**Daylight:** an equivalent light mode for bright offices, reading, and individual preference. Its `#F3F5F7` canvas combines near-white surfaces with dark ink. White `#FFFFFF` is reserved for raised surfaces, not prohibited as a matter of style.

Both modes share roles and hierarchy, with separately chosen values. Slate is the export default. A product may offer `system` as its initial choice and persist manual preferences. Do not change modes by time of day or panel detection. Restore the choice before first paint to avoid flashes, without a global theme-change transition.

Neither mode guarantees reduced fatigue. Preference, visual acuity, environment, scale, and physical display brightness all matter.

## 4. Color contract

[src/theme.json](../src/theme.json) is the canonical source of values: 43 colors per mode, typography, metrics, density, elevation, and brand roles. The [generated palette](palette.md) lists every key and CSS variable. Colors are opaque sRGB values; do not infer aliases from matching colors or maintain a parallel color catalog. Alpha blending on a new surface requires its own contrast check.

| Purpose | Roles |
| --- | --- |
| Surfaces | `bg.canvas`, `bg.surface`, `bg.raised`, `bg.hover`, `bg.selected` |
| Text | `text.primary`, `text.secondary`, `text.muted`, `text.disabled` |
| Separation | Decorative `border.subtle`; functional `border.control` |
| Links | `accent.fg` |
| Filled actions | `accent.fill`, `accent.hover`, `accent.pressed`, paired with `accent.on` |
| Keyboard focus | `focus.ring` |
| Text selection | `selection.bg`, paired with `selection.fg` |

`bg.selected` identifies selected components such as rows, files, and tabs. `selection.bg` identifies selected text. Do not interchange them without checking the resulting pairings.

Do not use `text.disabled` for informative content. `text.muted` does not mean illegible or translucent. Avoid unnecessary gray hierarchies: if secondary and muted text have no distinct purpose in a component, use only one.

### Feedback

Use the foreground/background pairs `success.fg`/`.bg`, `warning.fg`/`.bg`, `danger.fg`/`.bg`, and `info.fg`/`.bg`. Read their generated values rather than copying hex values into components.

Information reuses blue; it does not need another color identity. Reserve red for errors, risk, and destruction—not general decoration. Include a word and an additional visual cue: “Error,” “Under review,” or “Completed.” Normal metrics use neutral ink, not green by default.

For destructive actions, use a neutral button with an explicit label and risk symbol; use the appropriate danger pairing for hover or confirmation after checking contrast. Do not assume white text works on every red background.

### Increased contrast

Increased contrast is independent of mode, not a third brand identity. In `more`, `contrast.text.primary`, `contrast.text.secondary`, `contrast.text.muted`, and `contrast.border.control` replace their base roles. CSS resolves these overrides through variables; Sass accepts an explicit argument. See the [integration API](usage.md).

Increase text contrast and functional boundary visibility without changing semantic meaning. Support `prefers-contrast: more` where available and provide an explicit option. In `forced-colors`, favor system colors, outlines, and symbols; do not apply `forced-color-adjust: none` globally.

### Contrast rules

Use WCAG 2.x relative luminance in sRGB, without rounding ratios before comparing them with a threshold. Follow the pairings in the [accessibility contract](accessibility.md):

- Informative text and syntax: at least **5:1** on intended surfaces.
- Primary text and increased-contrast text: at least **7:1** on intended surfaces.
- Button, feedback, and selection labels: at least **4.5:1** within their specified pairings.
- Functional boundaries, focus indicators, and data marks: at least **3:1** against the specified adjacent surfaces.

A mark contrasting with its background does not establish distinguishability between series. Subtle borders are decorative and must never be the only way to identify an input, selection, or focus. Low contrast between decorative surfaces is acceptable when structure, spacing, and essential cues remain clear.

These are design constraints, not a claim of full WCAG conformance. Products must also address complete workflows, semantics, keyboard interaction, assistive technology, and actual component states.

## 5. Screen typography

### UI and reading

**IBM Plex Sans** is the primary family for UI, navigation, forms, and documents. **IBM Plex Sans Condensed** is opt-in for trees, lists, and dense textual columns with short labels. Do not apply it globally, use it for long paragraphs, or use it to hide layout problems. Layout density and condensed typography are independent controls.

- UI stack: `"IBM Plex Sans", "Segoe UI", system-ui, sans-serif`.
- Dense stack: `"IBM Plex Sans Condensed", "IBM Plex Sans", system-ui, sans-serif`.

### Code and terminals

**Cascadia Code** is the primary code family. Use **Cascadia Code NF** for terminals that need Nerd Fonts icons. Cascadia Mono or Mono NF provides an alternative without programming ligatures. PL includes Powerline symbols, not the full NF repertoire. Check the exact internal family name and host support.

Code stack: `"Cascadia Code", "Cascadia Code NF", "CaskaydiaCove Nerd Font Mono", ui-monospace, Consolas, monospace`. Configure a terminal with the exact installed NF family it needs; a web stack neither installs fonts nor guarantees icons.

Recommend contextual ligatures in editors with a user control to disable them. Disable them for logs, hashes, IDs, and literal comparisons. Ligatures do not change copied characters or reduce operator cell counts. Use standard italics; do not enable decorative cursive `ss01` by default.

Inter, Source Sans 3, JetBrains Mono, and IBM Plex Mono are valid alternatives for specific product needs. Do not load every alternative. Application icons use SVG with an accessible name, not private-use glyphs from a terminal font.

### Type scale

| Use | Size / line height | Weight |
| --- | --- | --- |
| Long-form document | 16px / 26px | 400 |
| Application text | 15px / 23–24px | 400 |
| Controls and tables | 14px / 20px | 400–500 |
| Noncritical metadata | 13px / 18–20px | 400 |
| Code editor | 15px / 24px, configurable | 400 |
| Section heading | 18px / 26px | 600 |
| View title | 24px / 32px | 600 |

Weights 400, 500, and 600 cover most needs; use 700 sparingly. Avoid 200/300 in small UI text and negative tracking in body or small text. Use tabular numerals in tables and a differentiated zero in identifiers where supported.

Use rem units without overriding the user's root size. Allow zoom and growing containers; support 200% text size, reflow at 320 CSS px except justified two-dimensional regions, and WCAG 1.4.12 text-spacing overrides without content loss.

Prefer self-hosted WOFF2 with pinned versions, preserved licenses, `font-display: swap`, and checked fallbacks. Do not force global `-webkit-font-smoothing` or text strokes, or expect identical rasterization across platforms. See the [typography guide](typography.md) for usage and distribution.

## 6. Borders, elevation, and geometry

- Base grid: **4px**. Spacing scale: **4, 8, 12, 16, 24, 32, 48**.
- Radii: **4px** for fields and buttons, **6px** for panels, **8px** for dialogs. Reserve pills for short status labels, not every component.
- Essential borders: **1 CSS px**, not fragile 0.5px hairlines. Align to whole CSS pixels where possible.
- Use subtle separators only when they add structure. Prefer space, headings, and alignment to enclosing every block.
- Form fields need a visible functional border, persistent label, and associated help. A placeholder is not a label.
- Focus: **2px outline with 2px offset**, unclipped and contrasting against the local surface. Use a checked double-outline solution on additional backgrounds. Focus is not selection; this design target does not make WCAG 2.4.13's AAA requirements a general AA requirement.
- Elevation uses surface and border. Shadows belong only to floating overlays: Slate `0 8px 24px rgb(0 0 0 / 24%)`; Daylight `0 8px 24px rgb(25 29 34 / 10%)`. A shadow alone does not identify a control.
- No glass, blur, decorative gradients, glowing borders, or noisy backgrounds.
- SVG icons: **20px**, **1.75–2px** stroke; **16px** in compact layouts. Label non-obvious functions. Avoid Unicode pictograms that change across platforms.

## 7. Density and interaction

Two densities share the same type scale:

- **Comfortable:** controls at least **40px** high, rows at least **44px**, spacing guidance **12–16px**.
- **Compact:** controls at least **32px** high, rows at least **36px**, spacing guidance **8–12px**. Do not shrink fonts to fit data.
- **Touch/coarse input:** aim for targets of at least **44×44 CSS px**. WCAG 2.2 AA specifies **24×24 CSS px** with exceptions; 44px is not its universal minimum.

These are minimum sizes, not rigid heights that clip enlarged text. Use the [density tokens](../src/theme.json) for component padding; the spacing ranges are not a replacement for those per-axis values. Give genuinely wide tables accessible local scrolling rather than overflowing the page. Do not hide secondary navigation without an equivalent route.

Cover default, hover, pressed, focus-visible, selected, busy, disabled, and error states. Selected states need a persistent non-color cue and appropriate native or ARIA semantics. Distinguish disabled from read-only. Do not reduce an entire disabled block's opacity and hide useful help; explain a blocked action in readable text when needed.

Loading preserves label, size, and focus, announces status through `aria-busy` or an appropriate status region, and avoids layout jumps. Errors include actionable text beside the field and a summary where appropriate; they do not disappear on blur.

Keep routine confirmations discreet; failures and pending actions persist. Important feedback must not depend on a fleeting toast. Avoid success flashes and screens full of green normal-state metrics.

### Motion: fast, fluid, and quietly precise

Motion acknowledges actions and explains changes without taking center stage. Show pressed states and keyboard focus immediately. Use **100–140ms** for small state changes, with the shared **120ms** token default, and **160–220ms** for contextual panels and dialogs. Exits are no slower than entrances; most routine transitions finish within **250ms**.

Use controlled deceleration, subtle opacity changes, and short **4–8px** movements when they explain a relationship. Keep transitions smooth, interruptible, and consistent across equivalent components. Prefer `opacity` and `transform` where appropriate; avoid bounce, overshoot, decorative button scaling, cascading table reveals, and continuous decoration. Never delay actions or invent loading time to showcase an effect.

Respect `prefers-reduced-motion`: remove nonessential movement and show final states directly. Do not animate global theme changes. Data refreshes preserve focus, scroll, and predictable ordering. See the [motion guide](motion.md) for timing, curves, component implementation, and reduced-motion behavior; timing ranges beyond `motion.fast` are guidance, not additional exported tokens.

## 8. Syntax, terminals, and data

### Low-fragmentation syntax

Use semantic syntax roles rather than copying colors into editor rules:

| Element | Role |
| --- | --- |
| Keywords | `syntax.keyword` |
| Functions | `syntax.function` |
| Strings | `syntax.string` |
| Numbers and literals | `syntax.number` |
| Types | `syntax.type` |
| Variables, operators, punctuation | `text.primary`; optional secondary punctuation in `text.secondary` |
| Comments | `syntax.comment`, without extra opacity or mandatory italics |
| Errors | `danger.fg` with underline or diagnostic, not an entire red line |

Limit colorization by scope rather than activating every accent on every line. Do not enable rainbow brackets by default. Diffs use +/− signs and semantic backgrounds with readable text.

### Terminals

Preserve ANSI meaning: map red, green, yellow, blue, magenta, and cyan to appropriate semantic and syntax roles. ANSI black must remain usable on the canvas; check its mapping in context. Bright need not mean neon, and bold need not mean bright. Check all 16 entries and bold, dim, inverse, cursor, selection, and TUI behavior in the target emulator. A foreground pairing on the canvas does not establish suitability as an ANSI background or under inverse.

### Data visualization

Use accents to identify series; keep ordinary text and metrics neutral. For six categories, use blue, sage, lavender, clay, teal, and amber through the independent roles `data.1`…`data.6`. Do not couple series identity to operational outcomes or syntax roles. Avoid red for routine categories.

Color is never enough: add direct labels, markers, dashed lines, units, and value tables or textual alternatives. Blue/teal and red/green distinctions can be difficult depending on vision and display. Review protan, deutan, tritan, and grayscale views for each chart; simulations do not guarantee universal distinguishability. Use perceptually ordered sequential scales for magnitude, and diverging scales around a meaningful center—not the categorical cycle.

## 9. Displays and environment

No palette equalizes uncalibrated displays. Flatcap avoids fragile dependencies; it does not correct gamma, PWM, subpixel arrangements, reflections, or aging.

- Use sRGB without depending on Display-P3 or HDR. Respect browser and OS color management and correct profiles; do not force a global gamma setting.
- Do not rely on tiny near-black differences, especially across changing gamma or viewing angles. Add labels, position, and functional boundaries to fills.
- On TN, check luminance differences across vertical position and angle. Calculated contrast margins do not compensate for tonal inversion.
- On IPS, inspect surface separation and reflections under ambient light. Tokens do not solve IPS glow.
- On OLED, inspect text at native scale, low luminance, and the actual subpixel layout. A nonblack canvas is a visual and structural choice, not a cure for smear, fringing, burn-in, or flicker. Avoid unnecessary large fixed white elements; do not animate the entire UI to “prevent burn-in.”
- Do not base identity on 1px RGB stripes or color as the only distinction in small text. Do not prescribe universal brightness or promise medical benefits from reducing blue.
- Keep mode, size, and contrast controls available. Ambient lighting and reasonable display brightness remain under user control.

Review representative displays and rasterizers at native and 125/150% scale, in bright and dim conditions. Include 1px lines, focus, errors, columns, `0/O/1/l/I`, selection, and scrolling text. Evaluate reading comfort with people in representative sessions rather than inferring it from a contrast ratio.

## 10. Using the foundation

Flatcap has three layers: **semantic source → generated exports → consumer components**. Keep roles distinct, such as `accent.fill` and `accent.fg`, even when their values match.

Use [theme.json](../src/theme.json) as the canonical source. [theme.css](../src/theme.css) exports variables without a reset or application components; [theme.scss](../src/theme.scss) provides Sass maps, functions, and opt-in token emission. See [integration and generation](usage.md) for the API and build workflow. Do not edit generated exports or raster assets by hand.

The [example](../examples/index.html) illustrates the foundation rather than prescribing a universal layout. Map each product's components and states to the roles, preserve the user's preferences, and assess the integration in its actual host. See the [branding guide](branding.md) for artwork rules.

## References

- [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [Text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
- [Non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)
- [Focus Appearance (AAA)](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html)
- [Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)
- [Text spacing](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html)
- [IBM Plex](https://github.com/IBM/plex)
- [Cascadia Code](https://github.com/microsoft/cascadia-code)
- [Carbon typography](https://www.carbondesignsystem.com/building-blocks/foundations/typography)
- [Dark-mode preferences and performance](https://www.nngroup.com/articles/dark-mode/)
- [Dark-mode structural considerations](https://www.nngroup.com/articles/dark-mode-users-issues/)
- [Monitor, viewing-angle, and gamma checks](https://www.eizo.be/monitor-test/)

These sources inform the design criteria. The Flatcap combination is not an endorsement by those organizations or a claim of medical benefit.
