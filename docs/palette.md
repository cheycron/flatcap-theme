# Flatcap palette and tokens

Version 2.0.0. Generated from `src/theme.json` with `python3 scripts/build.py`; do not edit this table by hand.

Opaque sRGB values. Roles describe purpose, even when their hex values match. Use each role on the appropriate surface; see the [accessibility guidelines](accessibility.md).

| Role | CSS variable | Slate | Daylight |
| --- | --- | --- | --- |
| `bg.canvas` | `--fc-bg-canvas` | `#191D22` | `#F3F5F7` |
| `bg.surface` | `--fc-bg-surface` | `#20252B` | `#FAFBFC` |
| `bg.raised` | `--fc-bg-raised` | `#292F36` | `#FFFFFF` |
| `bg.hover` | `--fc-bg-hover` | `#323A43` | `#E6EBF0` |
| `bg.selected` | `--fc-bg-selected` | `#263E53` | `#DCE9F4` |
| `border.subtle` | `--fc-border-subtle` | `#3D4652` | `#D2D9E0` |
| `border.control` | `--fc-border-control` | `#8593A5` | `#6C7A89` |
| `text.primary` | `--fc-text-primary` | `#D5DBE3` | `#28313B` |
| `text.secondary` | `--fc-text-secondary` | `#AEB8C4` | `#465463` |
| `text.muted` | `--fc-text-muted` | `#A7B3C2` | `#536273` |
| `text.disabled` | `--fc-text-disabled` | `#7E8998` | `#89939E` |
| `accent.fg` | `--fc-accent-fg` | `#9BBFDF` | `#285D85` |
| `accent.fill` | `--fc-accent-fill` | `#9BBFDF` | `#285D85` |
| `accent.hover` | `--fc-accent-hover` | `#ACCCE7` | `#214F73` |
| `accent.pressed` | `--fc-accent-pressed` | `#89AECD` | `#1C4362` |
| `accent.on` | `--fc-accent-on` | `#101820` | `#FAFBFC` |
| `focus.ring` | `--fc-focus-ring` | `#B0D2F0` | `#285D85` |
| `success.fg` | `--fc-success-fg` | `#9FC3AD` | `#32664D` |
| `success.bg` | `--fc-success-bg` | `#25372F` | `#E4EEE8` |
| `warning.fg` | `--fc-warning-fg` | `#D8BC87` | `#765319` |
| `warning.bg` | `--fc-warning-bg` | `#3A3225` | `#F4ECD9` |
| `danger.fg` | `--fc-danger-fg` | `#E2A0A5` | `#A43F4A` |
| `danger.bg` | `--fc-danger-bg` | `#382A30` | `#F5E5E7` |
| `info.fg` | `--fc-info-fg` | `#9BBFDF` | `#285D85` |
| `info.bg` | `--fc-info-bg` | `#263E53` | `#DCE9F4` |
| `syntax.keyword` | `--fc-syntax-keyword` | `#9BBFDF` | `#285D85` |
| `syntax.function` | `--fc-syntax-function` | `#ABC9CB` | `#306770` |
| `syntax.string` | `--fc-syntax-string` | `#9FC3AD` | `#32664D` |
| `syntax.number` | `--fc-syntax-number` | `#B6AED5` | `#68598C` |
| `syntax.type` | `--fc-syntax-type` | `#D6AF95` | `#84533D` |
| `syntax.comment` | `--fc-syntax-comment` | `#A7B3C2` | `#536273` |
| `selection.bg` | `--fc-selection-bg` | `#3C546B` | `#C8DDF0` |
| `selection.fg` | `--fc-selection-fg` | `#D5DBE3` | `#28313B` |
| `contrast.text.primary` | `--fc-contrast-text-primary` | `#EFF3F8` | `#17212C` |
| `contrast.text.secondary` | `--fc-contrast-text-secondary` | `#CBD5E1` | `#2B3D50` |
| `contrast.text.muted` | `--fc-contrast-text-muted` | `#C8D4E2` | `#35485B` |
| `contrast.border.control` | `--fc-contrast-border-control` | `#B0C0D2` | `#53677C` |
| `data.1` | `--fc-data-1` | `#9BBFDF` | `#285D85` |
| `data.2` | `--fc-data-2` | `#9FC3AD` | `#32664D` |
| `data.3` | `--fc-data-3` | `#B6AED5` | `#68598C` |
| `data.4` | `--fc-data-4` | `#D6AF95` | `#84533D` |
| `data.5` | `--fc-data-5` | `#ABC9CB` | `#306770` |
| `data.6` | `--fc-data-6` | `#D8BC87` | `#765319` |

## Typography

| Token | CSS variable | Value |
| --- | --- | --- |
| `font.ui` | `--fc-font-ui` | `"IBM Plex Sans", "Segoe UI", system-ui, sans-serif` |
| `font.dense` | `--fc-font-dense` | `"IBM Plex Sans Condensed", "IBM Plex Sans", system-ui, sans-serif` |
| `font.code` | `--fc-font-code` | `"Cascadia Code", "Cascadia Code NF", "CaskaydiaCove Nerd Font Mono", ui-monospace, Consolas, monospace` |
| `font.literal` | `--fc-font-literal` | `"Cascadia Mono", "Cascadia Mono NF", "Cascadia Code", ui-monospace, Consolas, monospace` |
| `font.size.body` | `--fc-font-size-body` | `0.9375rem` |
| `font.size.control` | `--fc-font-size-control` | `0.875rem` |
| `font.size.meta` | `--fc-font-size-meta` | `0.8125rem` |
| `font.size.reading` | `--fc-font-size-reading` | `1rem` |
| `font.size.code` | `--fc-font-size-code` | `0.9375rem` |
| `font.size.heading` | `--fc-font-size-heading` | `1.125rem` |
| `font.size.title` | `--fc-font-size-title` | `1.5rem` |
| `font.line.body` | `--fc-font-line-body` | `1.6` |
| `font.line.control` | `--fc-font-line-control` | `1.428571` |
| `font.line.reading` | `--fc-font-line-reading` | `1.625` |
| `font.line.code` | `--fc-font-line-code` | `1.6` |
| `font.weight.regular` | `--fc-font-weight-regular` | `400` |
| `font.weight.medium` | `--fc-font-weight-medium` | `500` |
| `font.weight.semibold` | `--fc-font-weight-semibold` | `600` |

## Metrics

| Token | CSS variable | Value |
| --- | --- | --- |
| `space.1` | `--fc-space-1` | `0.25rem` |
| `space.2` | `--fc-space-2` | `0.5rem` |
| `space.3` | `--fc-space-3` | `0.75rem` |
| `space.4` | `--fc-space-4` | `1rem` |
| `space.6` | `--fc-space-6` | `1.5rem` |
| `space.8` | `--fc-space-8` | `2rem` |
| `space.12` | `--fc-space-12` | `3rem` |
| `radius.control` | `--fc-radius-control` | `0.25rem` |
| `radius.panel` | `--fc-radius-panel` | `0.375rem` |
| `radius.dialog` | `--fc-radius-dialog` | `0.5rem` |
| `border.width` | `--fc-border-width` | `1px` |
| `focus.width` | `--fc-focus-width` | `2px` |
| `focus.offset` | `--fc-focus-offset` | `2px` |
| `motion.fast` | `--fc-motion-fast` | `120ms` |
| `reading.width` | `--fc-reading-width` | `70ch` |
| `target.touch` | `--fc-target-touch` | `2.75rem` |

## Density

| Token | Comfortable | Compact |
| --- | --- | --- |
| `control.min.height` | `2.5rem` | `2rem` |
| `row.min.height` | `2.75rem` | `2.25rem` |
| `control.padding.inline` | `1rem` | `0.75rem` |
| `control.padding.block` | `0.5rem` | `0.25rem` |
| `cell.padding` | `0.75rem` | `0.5rem` |

The Condensed family is independent of spacing density. `motion.fast` resolves to `0ms` in the generated CSS when the system requests reduced motion. Shadows live in `elevation`; they do not identify controls on their own.
