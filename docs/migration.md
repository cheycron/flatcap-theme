# Migrating to Flatcap 2.0

Version `2.0.0` replaces the numbered palette API with semantic roles. This is a breaking change: migrate each use by meaning rather than renaming colors by index or matching hex values.

## Why there is no positional mapping

A numbered color does not describe its purpose. The same legacy value may have been used for text, feedback, syntax, or data series, each requiring a different role in Flatcap 2.0. Review the surrounding surface and interaction states before choosing a replacement.

The [v1 reference](legacy/v1-reference.md) provides historical context, not the current API. Use [src/theme.json](../src/theme.json) as the source of truth for current values.

## Breaking changes

| Before | Now | Action |
| --- | --- | --- |
| `flatcap-0`…`flatcap-19` and numbered Sass variables | Semantic roles and `--fc-*` variables | Review each use; do not substitute by index or hex proximity |
| Global example styles in exports | Tokens without a reset or components | Apply body, link, selection, and focus styles in the consuming application |
| A single dark scheme | Slate and Daylight | Map both modes rather than inverting colors |
| Ambiguous borders | Decorative `border.subtle` / functional `border.control` | Use the functional border to identify inputs |
| Isolated status colors | `.fg`/`.bg` pairs and non-color indicators | Review messages, errors, and actions |
| A general font family without a density distinction | Plex Sans, opt-in Condensed, and Cascadia by role | Preserve text size in compact layouts; do not enable Condensed globally |
| Multiple manual catalogs | Canonical JSON and reproducible build | Edit the source and regenerate exports |
| Legacy global SCSS | Dart Sass `@use` module | Adopt the functions and mixin documented in [usage](usage.md) |

Numbered aliases are not provided because they would imply a false equivalence. Keep the previous upstream version pinned during a gradual migration if the product still depends on it. Do not mix APIs without an explicit boundary.

## Map by intent

- Main area → `bg.canvas`; navigation/panel → `bg.surface`; overlay → `bg.raised`.
- Content text → `text.primary`; metadata/help → `text.secondary` or `text.muted`. Use `text.disabled` only for inactive controls.
- Link → `accent.fg`; filled action → `accent.fill` + `accent.on`, with its own hover/pressed states. Do not hard-code white text on the accent.
- Focus → `focus.ring`; component selection → `bg.selected` plus an indicator; text selection → the `selection.*` pair.
- Status → a success/warning/danger/info pair with a word or symbol. A legacy purple used for information may now need blue; when used for a number, it needs `syntax.number` instead.
- Series → `data.1`…`data.6`, without tying categories to success/error or assuming six colors can distinguish every series.

## Migration sequence

1. Inventory workflows, surfaces, fonts, and preferences; pin the previous version and define the scope.
2. Integrate tokens in a bounded area. Test Slate/Daylight, standard/more, and comfortable/compact with real content.
3. Map every state, keyboard interaction, label, error, overlay, selection, and host-specific behavior. Preserve business rules.
4. Resolve font distribution, fallbacks, licenses, and exact NF family names. Do not implicitly install fonts or modify global preferences.
5. Run the application's build and tests. Check contrast for new pairs, reflow, spacing, forced colors, reduced motion, and required assistive technologies. Follow the [accessibility requirements](accessibility.md).
6. Update screenshots and version references after verifying the integration. Publishing and deployment require separate authorization.

For terminals, define and test ANSI 0–15 with bold/dim/inverse, cursor, selection, backgrounds, box drawing, and wide glyphs. For editors, map the workbench, diagnostics, search, and diff as well as syntax. Validate each integration in its actual host; token-level checks do not replace application-level testing.
