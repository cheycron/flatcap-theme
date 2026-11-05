# Accessibility

Flatcap provides semantic roles and contrast targets. Validate semantics, interaction, and content in each consuming application against [WCAG 2.2](https://www.w3.org/TR/WCAG22/).

## Color and contrast

Use the foreground/background pairs defined by the tokens, not arbitrary combinations. Flatcap's design targets are:

| Purpose | Intended surface | Target |
| --- | --- | ---: |
| Informative text, links, feedback foregrounds and syntax | The five `bg.*` surfaces | 5:1 |
| Primary text and increased-contrast text | The five `bg.*` surfaces | 7:1 |
| Functional borders, focus and data marks | Their adjacent surfaces | 3:1 |
| `accent.on` | `accent.fill`, `accent.hover`, `accent.pressed` | 4.5:1 |
| Feedback labels | Their corresponding feedback backgrounds | 4.5:1 |
| `selection.fg` | `selection.bg` | 4.5:1 |
| Filled actions | Their surrounding `bg.*` surfaces | 3:1 |

The five surfaces are canvas, surface, raised, hover, and selected. A filled button is identified by its fill against the **surrounding** background, not by a neutral border compared with its own fill. The focus offset must leave the local surface visible; check adjacent colors again when placing a control on a different background.

The internal 5:1 and 7:1 targets do not make displays or rasterizers equivalent. These pairings do not cover arbitrary combinations, transparency, background images, text on `data.*`, focus directly on fills without an offset, or every ANSI combination. Add contracts when a consuming application introduces new pairs.

Reserve `text.disabled` for genuinely inactive controls; it is not validated informational text. `border.subtle` is decorative and must not be the sole functional identifier. Contrast between a `data.*` mark and its background does not establish distinguishability between series or text legibility on that mark.

## Application requirements

- Keep labels visible and associate help and errors with their controls. Expose invalid states and actionable messages. Do not use placeholders as labels or communicate errors through color alone.
- Provide full keyboard operation, a logical order, a skip link where appropriate, and visible 2px focus outlines with a 2px offset, without clipping. Selected/current states need a persistent indicator and semantics distinct from focus.
- Preserve size, label, and focus while loading. Use appropriate, nonredundant announcements. Disabled and read-only are different states; explanations of unavailable actions must remain readable.
- Support text at 200%, reflow at 320 CSS px, and WCAG 1.4.12 text spacing without loss of content or functionality. Genuinely two-dimensional regions may use local scrolling with an accessible name and keyboard access.
- Use minimum control sizes, not fixed heights. Aim for 44×44 CSS px touch targets; distinguish this target from the 24×24 AA minimum and its exceptions.
- For `forced-colors: active`, use system colors, outlines, and structural indicators. Do not apply `forced-color-adjust: none` globally; shadows and fills may disappear.
- Reduced motion must remove unnecessary motion, not merely shorten a transition. Show final states directly, preserve focus and status without animation, and honor the system preference in CSS and JavaScript. Do not animate theme changes globally. See the [motion guide](motion.md).
- Give charts units, labels, markers, and a table or text alternative. Review grayscale and color-vision simulations without assuming universal distinguishability.
- Test screen readers, real tasks, and the assistive technologies required by the product. Accessibility snapshots and screenshots do not replace these checks.

## Applying the guidelines

Contrast checks apply to the defined token pairs, not to an entire product. Evaluate new integrations with their actual content, interactions, assistive technologies, displays, and rasterizers. Do not infer health benefits or full WCAG conformance from a palette, font, dark mode, contrast ratio, screenshot, or simulation.
