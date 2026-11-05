---
name: flatcap-design
description: >-
  Apply Flatcap 2.0 to web interfaces, admin panels, dashboards, forms, tables,
  documentation, editors, terminals, and data visualizations. Activate when asked
  to apply the Flatcap identity, migrate from Flatcap 1, integrate its tokens into
  a framework, create an editor or terminal theme, configure charts, or review
  an implementation's visual fidelity and accessibility.
license: MIT
metadata:
  version: "2.0.0"
---

# Flatcap 2.0 — implementation guide

> The interface organizes. Content takes the foreground. Color informs.

Applying Flatcap means resolving hierarchy, content, states, and host adaptation—not recoloring buttons or imposing the same composition on every product. Work on the real product, preserve its functionality, and provide evidence for the scope you actually verified.

## 1. Sources and portable contract

The following paths are relative to this skill's root, which is also the repository root. Resolve them from there, not from the consuming application's working directory. Read the resources you need with the available tools; nothing is preloaded, no fonts are installed, and no commands run implicitly.

| Resource | Authority and use |
| --- | --- |
| [src/theme.json](src/theme.json) | **Single source of truth**, version `2.0.0`: colors, typography, and metrics. |
| [docs/design-system.md](docs/design-system.md) | Rules for roles, states, geometry, and visual direction. |
| [docs/typography.md](docs/typography.md) | Families, scale, ligatures, distribution, and validation guidance. |
| [docs/usage.md](docs/usage.md) | API, selectors, CSS/SCSS integration, and application adaptation. |
| [docs/accessibility.md](docs/accessibility.md) | Contrast contracts and application validation requirements. |
| [docs/migration.md](docs/migration.md) | Breaking changes from Flatcap 1 and migration by meaning. |
| [docs/branding.md](docs/branding.md) | Identity and asset usage; does not replace component rules. |
| [docs/palette.md](docs/palette.md) | **Generated** role tables for reference; do not edit their values. |
| [src/theme.css](src/theme.css) | Generated CSS variables; no reset or application components. |
| [src/theme.scss](src/theme.scss) | Generated Sass maps, functions, and mixins; check signatures before use. |
| [examples/index.html](examples/index.html) | Opt-in demonstration; not a dependency or component library. |

Read the design rules and integration contract first, then typography, accessibility, and the resource for the domain you are working on. If a reference is unavailable, state the limitation; do not substitute a remembered palette or legacy tokens. If derived files disagree with the JSON, use the JSON for values and report the drift. Do not hide it with silent local overrides.

### Schema to preserve

- `version: "2.0.0"`; `themes.slate` and `themes.daylight` contain the same roles.
- Each theme retains **37 semantic color keys**, including `bg.canvas`, `text.primary`, `accent.fill`, and `contrast.text.primary`, plus **six data keys**: `data.1`…`data.6`. That is 43 roles per theme, not 37 in total.
- `typography` and `metrics` are top-level fields. Inspect their current fields; do not invent a size or family API.
- The CSS exporter replaces dots with hyphens and adds `--fc-`: `bg.canvas` → `--fc-bg-canvas`, `data.1` → `--fc-data-1`.
- Preserve roles even when values match: `accent.fg` does not replace `accent.fill`; `data.*` does not become `success.*` or `syntax.*` because colors happen to match.
- Do not maintain manual hex lists in this skill, components, or presets. If a host requires literal values, generate them from the JSON and document the version and mapping.

## 2. Workflow

### Step 1 — Inventory before designing

Inspect the relevant code, configuration, and screens. Record:

- Host, framework, and relevant versions; global styles, resets, existing themes, and distribution constraints.
- Real workflows: finding information, filtering, editing, saving, resolving errors, comparing data, or running commands.
- Surfaces and components: navigation, content, tables, forms, overlays, editors, charts, and empty states.
- Available fonts and assets; internal desktop font names; required languages, scales, and fallbacks.
- Existing themes, densities, accessibility preferences, and persistence. Do not create a second, incompatible controller.
- Layout and semantic issues: overflow, missing labels, lost focus, redundant hierarchies, and color-only states.

For a review, deliver findings with location, impact, and a proposed solution without modifying files. For an implementation, limit changes to the assignment and preserve business rules, contracts, and user preferences. Preparing a configuration does not authorize font installation, overwriting global preferences, publication, or deployment.

### Step 2 — Map elements to roles

Build a short `element → role → surface → states → file/configuration` table. Resolve meaning before color similarity.

| Element | Roles and decision |
| --- | --- |
| Main area / navigation / overlay | `bg.canvas` / `bg.surface` / `bg.raised`; elevate only elements that actually float. |
| Neutral hover / persistent selection | `bg.hover` / `bg.selected`; selection needs an additional persistent indicator. |
| Separator / essential outline | `border.subtle` / `border.control`; a decorative border does not identify a field. |
| Text and headings / metadata / help | `text.primary` / `text.secondary` / `text.muted`; use only the hierarchy needed. |
| Genuinely inactive control | `text.disabled`; never for information that remains necessary. |
| Link / primary action | `accent.fg` / `accent.fill` with `accent.on`; do not assume white text. |
| Keyboard focus | `focus.ring`; independent of hover, selection, and the text cursor. |
| Text selection | The `selection.bg` + `selection.fg` pair; not a substitute for row selection. |
| Feedback | `success`, `warning`, `danger`, `info` pairs, each `.fg` + `.bg`, with a word and an additional indicator. |
| Syntax | `syntax.keyword`, `.function`, `.string`, `.number`, `.type`, `.comment`; variables and operators use primary text ink. |
| Increased contrast | `contrast.text.primary`, `.secondary`, `.muted`, `contrast.border.control`; overrides for their base roles. |
| Categorical series | `data.1`…`data.6`; series identity is independent of operational status. |

Do not derive a token automatically from RGB proximity. Do not carry `flatcap-0`…`flatcap-19` indices into the 2.0 API or perform positional substitution. Consult migration guidance and review each use.

### Step 3 — Resolve composition, typography, and complete states

**Hierarchy and geometry.** Favor space, alignment, headings, and tables over a wall of cards. Use a 4px grid and a 4/8/12/16/24/32/48 scale. Reference radii: 4px for controls, 6px for panels, 8px for dialogs. Essential borders are 1 CSS px; avoid fragile hairlines. Use surface and border for elevation; reserve shadows for overlays. No glow, glass, blur, decorative gradients, or noisy backgrounds. Implemented values must follow `metrics` and the design rules.

**Density.** Comfortable: controls at least 40px and rows at least 44px. Compact: controls at least 32px and rows at least 36px. These are minimums that may grow, not fixed heights. Keep the type scale when compacting; adjust padding and spacing. For coarse pointers, aim for 44×44 CSS px targets; do not present this as the universal WCAG AA minimum. Do not hide essential navigation or data to make a layout fit.

**Typography.** Use IBM Plex Sans for UI, reading, forms, and navigation. IBM Plex Sans Condensed is opt-in for short labels, trees, and dense text columns, **independently of density**. Do not enable it globally when selecting compact or use it to compress paragraphs. Start with standard Cascadia Code in editors; use an NF variant only when a terminal needs its glyph repertoire, with its **exact installed family name**. A CSS stack does not install fonts.

Starting scale: reading 16/26px, application 15/23–24px, controls and tables 14/20px, noncritical metadata 13/18–20px, configurable code 15/24px, headings 18/26px and 24/32px. Use rem without overriding the user's root size; weights 400/500/600, with 700 used selectively. Avoid Thin/Light in small UI, negative tracking, and width transforms. Start long-form text around 60–75 `ch` per column, not a universal fixed width.

Recommend contextual ligatures for editable code, with an option to disable them. Turn them off in logs, hashes, IDs, and literal comparisons; scope this rule to avoid breaking shaping in other languages. Decorative `ss01` is off by default. Use tabular figures in tables when supported, visible units, and consistent alignment; do not make all data monospace. Use SVG application icons with accessible names, not private Nerd Font glyphs.

On the web, prefer self-hosted WOFF2, pinned versions, language coverage, `font-display: swap`, measured fallbacks, and preserved licenses. Do not introduce an external download or load every alternative. Do not force global font smoothing or strokes. Flatcap's MIT license does not replace font licenses. For brand distribution, consult `docs/branding.md`. Preserve attribution and the original terms for the pre-existing artwork credited to Vexels; permission to modify and reuse that artwork does not relicense it under MIT.

Explicitly cover each applicable component state:

| State | Implementation contract |
| --- | --- |
| Default | Text, surface, border, and affordance are readable without hover. |
| Hover | Subtle change; not the only way to discover a function. |
| Pressed / active | Perceptible response; the primary action uses `accent.pressed` with `accent.on`. |
| Focus-visible | Visible 2px outline with a 2px offset, without clipping or being hidden by overlays. Check the local surface. |
| Selected / checked / current | Persistent indicator plus appropriate native or ARIA state; not fill alone. |
| Busy / loading | Preserve label, size, and focus; announce through `aria-busy` or an appropriate status region. Avoid redundant announcements. |
| Disabled / read-only | Distinguish the two; do not fade the whole block with opacity. Explain unavailable actions in readable text where appropriate. |
| Error / invalid | Label, actionable message associated with the field, and a non-color indicator; a summary where appropriate. Do not clear on blur. |
| Empty / success / pending | Explain the situation and next action; important confirmations and failures persist rather than depending on a fleeting toast. |

Forms: persistent labels, associated help, native controls where possible, and logical keyboard order. Tables: semantic headers, announced sorting, units, and accessible local scrolling when genuinely two-dimensional. Dialogs: accessible name, initial and restored focus, closing behavior, and focus containment appropriate to modality. Do not add ARIA to compensate for broken interaction.

**Motion.** Follow [docs/motion.md](docs/motion.md): fast, fluid, and quietly precise. Show pressed states and keyboard focus immediately; use 100–140ms for small changes (shared `motion.fast`: 120ms) and 160–220ms for contextual panels/dialogs. Exits are no slower than entrances; keep most routine transitions within 250ms. These additional timing ranges and curves are guidance, not exported tokens. Prefer controlled deceleration, subtle opacity changes, and 4–8px movement where it explains a relationship. Keep transitions interruptible and prefer `opacity`/`transform` where appropriate; no bounce, overshoot, decorative button scaling, routine stagger, or fake loading delays. With reduced motion, remove nonessential movement and show the final state directly; the generated token alone does not disable unrelated animations. Do not animate global theme changes. Preserve focus, scroll position, and context; application logic must work without animation completion events.

### Step 4 — Adapt to the framework or host

#### Web, components, and dashboards

1. Consume [theme.css](src/theme.css) through the project's pipeline. **It includes no reset, font loading, body styles, or components**: make those decisions explicitly in the consuming application.
2. Place preferences on the root element. Slate is the default; following the system requires the `system` option and is not implied by a missing attribute.

```html
<html lang="en"
      data-fc-theme="slate"
      data-fc-contrast="standard"
      data-fc-density="comfortable">
```

| Root attribute | Accepted values | Effect |
| --- | --- | --- |
| `data-fc-theme` | `slate`, `daylight`, `system` | Mode; `system` follows `prefers-color-scheme`. |
| `data-fc-contrast` | `standard`, `more`, `system` | Independent contrast preference; `system` follows `prefers-contrast` where supported. |
| `data-fc-density` | `comfortable`, `compact` | Spacing metrics; does not change font family or size. |

3. If the product supports preference selection, provide accessible controls, persist manual choices, and restore them before first paint with a mechanism compatible with its CSP and SSR/hydration. Do not impose changes based on time, monitor, or geolocation. Do not require JavaScript to read the initial interface.
4. Bind component styles to semantic variables, including states. Contrast overrides must reach components through effective roles; do not hard-code standard values locally or always use `contrast.*` as the base theme.
5. In Tailwind, CSS Modules, CSS-in-JS, or another system, map roles to `var(--fc-...)` according to the installed version's API. Avoid a second hex catalog and check purge rules, specificity, portals, Shadow DOM, and scope. Overlays must receive the same theme.
6. For Sass, read the actual signatures in [theme.scss](src/theme.scss) and [usage.md](docs/usage.md). Do not invent mixin names or import examples as dependencies. If a consuming application cannot use variables, generate an adapter from JSON for each mode and document how it switches themes.

Minimal role application in the consuming application—not a component library or complete state coverage:

```css
.app-shell { background: var(--fc-bg-canvas); color: var(--fc-text-primary); }
.app-panel { background: var(--fc-bg-surface); }
.app-help { color: var(--fc-text-muted); }
.app-control { border: 1px solid var(--fc-border-control); }
.app-primary { background: var(--fc-accent-fill); color: var(--fc-accent-on); }
.app-primary:hover { background: var(--fc-accent-hover); }
.app-primary:active { background: var(--fc-accent-pressed); }
.app-control:focus-visible, .app-primary:focus-visible {
  outline: 2px solid var(--fc-focus-ring);
  outline-offset: 2px;
}
.app-literal {
  font-variant-ligatures: none;
  font-feature-settings: "calt" 0, "liga" 0;
}
```

Check these pairs on their actual surfaces and adapt disabled states, selection, errors, and forced colors before considering a component complete. In `forced-colors: active`, favor system colors, outlines, and structural indicators. Do not apply `forced-color-adjust: none` globally or rely exclusively on shadows or backgrounds that the system may suppress.

#### Editors

Generate the editor's native format from both JSON modes. Map the workbench, panels, inputs, menus, focus, selection, search, diagnostics, and diff—not only syntax highlighting. Avoid color fragmentation: comments use `syntax.comment`, variables and operators stay neutral, errors have diagnostics/underlines, and diffs have +/− signs as well as backgrounds.

Start with standard Cascadia Code, configurable size, and optional ligatures. Do not enable rainbow brackets, decorative italics, or NF as a universal requirement. Test precedence between syntax tokens and semantic highlighting, inactive selection, cursor, gutter, and diagnostic contrast. Do not claim support for an editor whose schema or runtime has not been checked.

#### Terminals

HTML attributes do not configure an emulator. Translate roles into the host's actual schema and test behavior. Preserve the meaning of ANSI red/green/yellow/blue/magenta/cyan: do not indiscriminately replace all 16 entries with six data colors. Review black and bright black in context; mapping one to the canvas may make text invisible. Do not assume bold means bright.

Validate all 16 ANSI entries and the combinations used with bold, dim, inverse, colored backgrounds, cursor, selection, and real TUI applications. A color validated as a foreground on canvas is not thereby validated as an ANSI background or under inverse. Document uncovered pairs; generating a file does not establish universal ANSI compatibility.

Use the exact installed NF family if the prompt requires it; distinguish Cascadia Code NF, Mono variants, PL, and Nerd Fonts builds. Test box drawing, Powerline, single/double-width glyphs, and the host's cell calculations. NF does not guarantee ligatures, and ligatures do not reduce operator cell counts. For logs and literal reading, disable them where the emulator allows it and state the limitation if there is no per-region control.

#### Data visualization

- Use `data.1`…`data.6` for categories: blue, sage, lavender, clay, teal, and amber. Keep identity stable across filters and views; do not recolor a series when its operational outcome changes.
- Do not use red as an ordinary category or green for every normal metric. Reserve semantic feedback for real states, with a textual explanation.
- Separate ink, axes, ticks, grid, background, tooltip, selection, and series. A text token does not automatically validate thin lines, small points, or transparent areas.
- Add direct labels, markers, line styles, units, and a table or text alternative. Interactive tooltips must be keyboard-accessible; critical information must be available without hover.
- For magnitudes, use a perceptually ordered sequential scale; for values on either side of a meaningful center, use a diverging scale with an explicit center. The categorical cycle is not a heatmap scale.
- With more than six categories, consider filters, grouping, small multiples, or additional indicators before cycling through indistinguishable colors. Treat any new scales as an application extension and validate them; do not invent official tokens.
- In Matplotlib, Grafana, or another host, translate JSON into the supported format without assuming an API or installed preset. Check mode switching, static export, printing, and contrast on the final background. Do not use alpha over unknown backgrounds as a shortcut.
- Review protan/deutan/tritan simulations and grayscale for each chart. Simulations help find problems; they do not establish universal distinguishability or replace testing with people.

### Step 5 — Verify and deliver evidence

Distinguish **token integrity**, **application integration**, **workflow accessibility**, and **physical/user evaluation**. Passing one layer does not pass the others.

If the assignment changes the token system, run from the repository root with the available tools:

```sh
python3 scripts/build.py
python3 scripts/validate.py
python3 -m unittest discover -s tests
```

[build.py](scripts/build.py) generates CSS/SCSS, mapped SVG fills, and the palette table; review the diff rather than editing derived files by hand. [validate.py](scripts/validate.py) checks color contracts. For integration-only work, do not regenerate or alter upstream without need and authorization; run its checks in the available copy and the application's tests/build as appropriate to scope. Do not claim to have run commands that were only prepared.

Minimum applicable application checks:

- **Visual matrix:** Slate and Daylight; standard/more contrast and system tracking; comfortable/compact; complete states, overlays, and real long text. Check preference precedence and avoidable flashes.
- **Keyboard:** logical order, visible unobscured focus, activation, escape, and focus restoration; no traps outside interactions that require containment. Inspect accessible names, roles, and states; test announcements with assistive technology where available.
- **Scaling and reflow:** 200% text, 320 CSS px width, WCAG 1.4.12 spacing overrides, and unrestricted zoom. No loss of content or functionality; use two-dimensional scrolling only where justified, with local access.
- **Preferences:** `forced-colors`, `prefers-reduced-motion`, increased contrast, and mode preference. Verify in the actual host or state what was emulated and what remains untested.
- **Contrast:** check effective pairs, including interaction, focus, and feedback. Internal targets: informational text/syntax ≥5:1 and primary text ≥7:1 on intended surfaces; `accent.on` on default/hover/pressed and feedback/selection labels ≥4.5:1; functional outlines and focus ≥3:1 against adjacent colors; increased-contrast text overrides ≥7:1. Consult the contrast matrix and validate every new surface; do not round before comparing with the threshold or treat these figures as whole-product approval.
- **Data:** labels, units, missing values, zero, negatives, long series, navigation without hover, and text alternatives. Review color and shape together, including grayscale.
- **Typography:** actual glyph coverage, unclipped fallbacks, accents, `Il1/O0/rn/m`, numbers, and literal selection/copying. Test NF and ANSI only in the declared hosts.
- **Regression:** relevant tests/build, inspection of screens or configurations, and evidence scoped to changed workflows. Screenshots support visual inspection but do not independently prove interaction or accessibility.

Do not claim full WCAG conformance, hardware validation, or user testing without documented checks. Do not extrapolate historical reports to a new integration or claim that Flatcap reduces fatigue, protects eyesight, or resolves PWM, fringing, or burn-in. sRGB, contrast margins, and user controls do not make TN/IPS/OLED panels or rasterizers equivalent. Identify physical and user testing as unverified where applicable.

## 3. Semantic anti-patterns — correct the meaning

- Choosing a similar hex, recycling 1.x names, or copying demo values as a new source of truth.
- Using `border.subtle` to identify inputs, `text.disabled` for help, or `text.muted` with additional opacity.
- Hard-coding white on `accent.fill` or `danger.fg`; mixing feedback pairs without validation.
- Confusing focus with hover, row selection with text selection, or selected with pressed.
- Coloring normal metrics green, assigning danger to a category, or coupling series to syntax for convenience.
- Building a dashboard as a wall of cards, coloring every number, or removing labels to make it look “clean.”
- Hiding errors in a toast, using placeholders as labels, or communicating state through color alone.
- Compacting by shrinking text, fixing heights that clip zoomed content, enabling Condensed globally, or condensing with `scaleX`.
- Requiring NF for web icons, assuming font family names are interchangeable, or claiming that stack entries are installed.
- Removing outlines, blocking forced colors, animating everything on theme change, or using a fixed dark fallback inside Daylight.
- Treating token ratios, a screenshot, or a color-vision simulation as proof that a product is accessible.

## 4. Delivery checklist

Deliver only what is relevant to the assignment, with a clear conclusion:

- [ ] Inventory and scope: host, workflows, components, and affected files; review or implementation boundaries respected.
- [ ] Role mapping traceable to `src/theme.json` `2.0.0`, without a parallel catalog or invented tokens.
- [ ] Both modes, contrast, and density integrated according to host capabilities; limitations explicit.
- [ ] Typography and licenses resolved; Condensed independent of compact; literal content without ligatures; exact NF family only where needed.
- [ ] States, keyboard, semantics, errors, and user preferences covered, not just an ideal screen.
- [ ] For data: series identity, non-color indicators, labels, units, and text alternative verified.
- [ ] For editors/terminals: native mapping, syntax/diagnostics or ANSI matrix, and fonts checked within the declared scope.
- [ ] Tests actually run, their results, and evidence; distinguish failures, blockers, and unverified checks.
- [ ] Change summary, integration instructions, and migration differences; no claims of publication, installation, or conformance that did not occur.
