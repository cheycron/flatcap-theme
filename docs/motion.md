# Motion — Fast, fluid, and quietly precise

Flatcap motion makes an interface feel responsive, coherent, and dependable without taking center stage. Every transition should acknowledge an action, explain a change, or preserve spatial context. If movement adds no useful information, leave it out.

The visual character is modern and minimal: short distances, controlled deceleration, stable surfaces, and clear endpoints. Smoothness matters more than spectacle. Motion supports **Quiet precision**, not a separate layer of decoration.

## 1. Respond first

- Show pressed states, keyboard focus, and the start of an operation immediately. Never wait for an entrance or exit animation before handling input.
- Show genuine busy feedback while work continues. Preserve the control's label, dimensions, and focus; announce status where appropriate. Do not invent progress, hide failure, or add a minimum loading delay to display an animation.
- Keep navigation and repeated tasks direct. Typing, table sorting, filtering, and routine data refreshes must not trigger choreographed screen reveals.
- Let users interrupt or reverse transitions. Continue from the current visual state where practical instead of snapping to the start or queuing effects. Coalesce obsolete visual updates, not the user's underlying actions.
- Treat animation as presentation, not application logic. State, focus management, and completion must work with animations disabled; do not depend solely on `transitionend` or `animationend` events.

The goal is perceived responsiveness backed by honest feedback. Animation does not make a slow operation faster or establish usability without evaluating the actual product.

## 2. Timing by purpose

These ranges are starting points for consuming products, not additional exported tokens. Choose the shortest duration that keeps the change understandable and use it consistently for equivalent components.

| Purpose | Guidance | Behavior |
| --- | --- | --- |
| Pressed state and keyboard focus | Immediate | Do not fade in the only focus or activation cue. |
| Hover, selection accent, small state change | 100–140ms | Use the shared **120ms** default; keep a persistent non-color cue where needed. |
| Tooltip, menu, or small popover | 120–160ms entrance; 80–120ms exit | Minimal fade or short directional movement; no travel across the screen. |
| Dialog, drawer, or contextual panel | 160–220ms entrance; 120–180ms exit | Establish the destination quickly; exits are no slower than entrances. |
| Accordion or meaningful local layout change | 160–220ms | Keep surrounding content stable and avoid repeated layout work in large regions. |

Most routine transitions should finish within **250ms**. Do not exceed **300ms** for frequent interactions; shorten the movement or remove it rather than making routine work wait. Do not animate every row in a table. Avoid stagger on routine screens; if a one-off explanatory reveal genuinely needs it, keep the whole sequence within the same 250ms budget and make it skippable.

The canonical token is `metrics.motion.fast: "120ms"` in [theme.json](../src/theme.json), exported as `--fc-motion-fast`. Generated CSS resolves it to `0ms` for `prefers-reduced-motion: reduce`. This does **not** disable unrelated component animations. Additional durations and curves belong to the consumer's component styles unless added to the canonical source through a separate token change.

## 3. Curves and distance

| Purpose | Suggested CSS curve | Character |
| --- | --- | --- |
| Small state transitions and local changes | `cubic-bezier(0.2, 0, 0, 1)` | Quick response with a controlled finish. |
| Entering overlays and panels | `cubic-bezier(0.16, 1, 0.3, 1)` | Decelerate into the destination without overshoot. |
| Dismissal | `cubic-bezier(0.4, 0, 1, 1)` | Leave promptly; use a shorter duration than entry. |

Curves are recommendations, not exported Flatcap variables. Native platforms may use equivalent non-oscillating curves. If the framework uses springs, choose a critically damped or overdamped response with no visible bounce and a settling time within the duration budget.

Keep movement around **4–8 CSS px** for small surfaces. A larger drawer may travel farther only when its edge relationship needs explaining; prefer a short offset or direct appearance to a full-screen journey. Never move text while the user is reading or typing. Avoid decorative button scaling, rubber-band effects, parallax, spinning interface elements, and overshoot. Loading indicators are functional exceptions, not permission for continuous decoration.

## 4. Smoothness and continuity

- Prefer `opacity` and `transform` when they convey the change without disturbing layout. They are often compositor-friendly, but smoothness still depends on layer size, rendering, and the device; do not assume automatic GPU acceleration or a guaranteed frame rate.
- Avoid `transition: all`. List only the properties that should change. Do not animate filters, large shadows, or full-page theme colors as decoration.
- Use color transitions only for small local states whose intermediate colors remain readable. Keep focus immediately visible and selection semantically updated.
- Size-changing disclosures may need layout animation. Keep them local, avoid reading and writing layout on every frame, and remove the effect if it causes stutter or disorientation. Do not apply `will-change` globally.
- Reserve space for incoming content. Preserve scroll, focus, readable labels, and predictable data ordering. Data updates should not reorder rows beneath the pointer or replay chart entrances.
- Make opened overlays operable promptly. Hidden or closing content must not remain an invisible keyboard or pointer target; coordinate visibility, focus, and semantics without waiting for a decorative effect.
- Avoid simultaneous movement across unrelated regions. Keep page navigation direct; no mandatory route choreography, logo reveals, looping shimmer, or decorative success bursts.

## 5. Reduced motion and user control

Honor `prefers-reduced-motion` on the web and the equivalent platform preference. A product setting may reduce motion further; it must not silently override a system request for less movement.

- Remove nonessential translation, scaling, parallax, stagger, and animated layout changes. Show the final state directly, rather than merely accelerating the same movement.
- Keep all actions, status text, focus, and navigation available without motion. Use a static busy indicator with accessible status instead of a continuously moving loader when appropriate.
- Disable animated scrolling for the affected workflow. Do not animate global theme changes, even when reduced motion is not requested.
- If a brief opacity change is genuinely needed, offer a direct-state alternative. Avoid flashing or pulsing as a substitute for movement.

### Minimal CSS pattern

This is a component-scoped example, not a full popover implementation. The host must provide correct visibility, keyboard behavior, and focus management. Apply it only to an already-rendered surface; animation from `display: none` requires separate lifecycle handling.

```css
.context-surface {
  opacity: 0;
  transform: translateY(4px);
  transition:
    opacity var(--fc-motion-fast) cubic-bezier(0.2, 0, 0, 1),
    transform var(--fc-motion-fast) cubic-bezier(0.2, 0, 0, 1);
}
.context-surface[data-open="true"] {
  opacity: 1;
  transform: none;
}

@media (prefers-reduced-motion: reduce) {
  .context-surface {
    transition: none;
    transform: none;
  }
}
```

The explicit media query removes movement even if a product later overrides the duration. Apply equivalent rules to every animated component, including JavaScript-driven animations; changing one duration token is not comprehensive reduced-motion support.

## 6. Review in the product

Check entry, exit, interruption, rapid repeated input, keyboard use, scrolling, and reduced motion. Test on representative lower-powered devices and under realistic rendering and data load. Inspect for dropped frames, layout shifts, unexpected focus changes, unreadable intermediate states, and feedback that ends too soon. Tools can reveal rendering issues; user evaluation determines whether the motion is comfortable and useful.

Motion passes the design intent when an action feels acknowledged, the change is understandable, and the animation itself is not what the user remembers. See [accessibility](accessibility.md), [the design system](design-system.md), and [integration](usage.md).
