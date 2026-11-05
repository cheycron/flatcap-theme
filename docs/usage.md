# Usage and integration

Flatcap 2.0 provides tokens, not a component framework. The editable source is [src/theme.json](../src/theme.json). The exports do not load fonts or include a reset, `body` styles, selection, focus, or control styles. Implement these behaviors in the consuming application.

## CSS

Import `src/theme.css` through your product's build pipeline:

```html
<link rel="stylesheet" href="/vendor/flatcap/theme.css">
<!-- On the document root element: -->
<html lang="en" data-fc-theme="slate" data-fc-contrast="standard"
      data-fc-density="comfortable">
```

| Root preference | Values | Default without attribute |
| --- | --- | --- |
| `data-fc-theme` | `slate`, `daylight`, `system` | Slate |
| `data-fc-contrast` | `standard`, `more`, `system` | Standard |
| `data-fc-density` | `comfortable`, `compact` | Comfortable |

`system` follows `prefers-color-scheme: light` or `prefers-contrast: more`, respectively. Omitting the attribute does not enable automatic system preference tracking. Unrecognized values fall back to the defaults; validate persisted choices. These selectors apply only to `:root`, not nested themes. Check inheritance and scope for portals and Shadow DOM.

Each dot-separated key is exported with the `--fc-` prefix and hyphens: `bg.canvas` → `--fc-bg-canvas`. The `more` overrides resolve effective text and border values from the `contrast.*` tokens; other colors retain their roles. Compact metrics do not change typography. `prefers-reduced-motion: reduce` resolves `--fc-motion-fast` to `0ms`; it does not remove unrelated animations that do not use the token.

Follow the [motion guide](motion.md) for quick, fluid transitions, recommended curves, interruption, and component-scoped reduced-motion handling. It distinguishes the exported 120ms token from longer component timing guidance; the stylesheet does not install component animations.

Minimal application, without complete state coverage:

```css
body {
  background: var(--fc-bg-canvas);
  color: var(--fc-text-primary);
  color-scheme: var(--fc-color-scheme);
  font: var(--fc-font-size-body)/var(--fc-font-line-body) var(--fc-font-ui);
}
a { color: var(--fc-accent-fg); text-underline-offset: .2em; }
::selection { background: var(--fc-selection-bg); color: var(--fc-selection-fg); }
.control {
  background: var(--fc-bg-surface);
  color: var(--fc-text-primary);
  border: var(--fc-border-width) solid var(--fc-border-control);
  border-radius: var(--fc-radius-control);
  min-height: var(--fc-control-min-height);
  padding: var(--fc-control-padding-block) var(--fc-control-padding-inline);
}
.control:focus-visible {
  outline: var(--fc-focus-width) solid var(--fc-focus-ring);
  outline-offset: var(--fc-focus-offset);
}
```

See the [working example](../examples/index.html) and [its CSS](../examples/example.css) for states and preferences. Review the demonstration before adapting it to production. It uses locally available fonts or fallbacks, includes no font files, and makes no external requests. For reproducible web deployment, self-host WOFF2 files and preserve their licenses as described in [typography](typography.md).

Persist explicit choices through the product's existing preference mechanism and restore them before the first paint with a CSP- and SSR-compatible solution. Do not introduce a second theme controller. The example uses an external JavaScript file and localStorage, tolerating storage errors. Without JavaScript, it remains readable in Slate; preference controls and the local form remain disabled to prevent HTML submission without its local handler.

## Sass

Use Dart Sass modules (`@use`), not LibSass/node-sass. Importing the module emits no CSS. Public API:

- `color($role, $theme: "slate", $contrast: "standard")`: resolved Sass color; invalid themes and roles produce an error. `more` applies overrides where available.
- `value($name)`: unquoted value from `typography` or `metrics`; does not accept color, density, or elevation keys.
- `tokens($theme: "slate", $contrast: "standard", $density: "comfortable")`: mixin that emits all resolved variables into the calling selector. Accepts only Slate/Daylight and standard/more; does not implement system preferences or media queries.
- `$themes`, `$foundation`, `$densities`, `$elevation`: lookup maps. Do not modify them as a parallel token catalog.

```scss
@use "../src/theme" as fc;

.product {
  @include fc.tokens("daylight", "more", "compact");
  color: var(--fc-text-primary);
  background: var(--fc-bg-canvas);
  font-family: fc.value("font.ui");
}
.static-label { color: fc.color("text.primary", "daylight", "more"); }
```

Choose dynamic CSS **or** explicitly resolve the scheme through Sass. A mixin emitted inside a container lets its children inherit variables, but does not automatically add a nested theme controller. To follow system preferences, write and test media queries in the consuming application.

## JSON and other hosts

The JSON uses a custom format, **not DTCG**, and is not a preset that any editor can import directly. It contains `themes` with 43 colors per mode, `typography`, `metrics`, `density`, `elevation`, `branding`, and metadata. Map roles to the host's native format. Keep `data.*` separate from syntax and feedback even when they share a hex value. See [migration](migration.md) for mapping guidance.

## Editing and generation

The standard-library tools require Python 3.10+; CairoSVG and Pillow are needed only for PNG rendering:

```sh
python3 scripts/build.py
# For PNG assets, with scripts/requirements-assets.txt installed:
python3 scripts/render_assets.py
```

`build.py` generates `src/theme.css`, `src/theme.scss`, `docs/palette.md`, and annotated SVG fills. It does not generate geometry or convert text to outlines: review those masters as graphics sources. `render_assets.py` rasterizes the masters. Its `--check` compares decoded pixels, not PNG compression bytes. Do not edit exports or PNGs by hand.

[Full palette](palette.md) · [Portable skill](../SKILL.md) · [Accessibility guidelines](accessibility.md).
