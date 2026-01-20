# Flatcap UI Theme

![Version](https://img.shields.io/badge/version-1.0.0-blueviolet) ![License](https://img.shields.io/badge/license-MIT-blue)

**Flatcap** is a design system and color scheme tailored for application interfaces, code editors, and data-dense dashboards. Drawing inspiration from the *Nord theme*, it embraces principles of calm, clean aesthetics, and a dimmed pastel color approach to reduce eye strain during long coding or administration sessions.

## 1. Philosophy

Flatcap is built to be:

- **Minimalist:** Reduces visual noise by avoiding harsh contrasts and saturated primaries.
- **Comfortable:** Specifically tuned for low-light environments; low contrast helps maintain focus without fatigue.
- **Modern:** Uses a flat, matte color finish that feels distinct yet familiar.

## 2. Naming Conventions

To maintain brand consistency, always adhere to these naming rules:

*   **Official Name:** Always write as **Flatcap** (Single word, capitalized 'F').
*   **Prohibited Forms:** Never use "Flat Cap" (with space) or "Flat-Cap" (with hyphen).
*   **Variables:** Use `flatcap` (all lowercase) ONLY when the technical context (e.g., code variables, file paths) strictly requires lowercase.

## 3. Technical Palette Definitions

The system relies on **20 core colors** divided into four distinct families.
*Note: This specification includes semantic optimizations for better accessibility and state recognition.*

### 🌑 Deep Twilight (Structural)
Used for the structural foundation of the interface. The contrast ratio between levels is tuned to create depth without using heavy drop shadows.

| Token ID | Swatch | Variable Name | Hex Value | Usage |
| :--- | :---: | :--- | :--- | :--- |
| **FC-00** | <img src="https://placehold.co/100x40/121418/121418/png" width="50" height="20" alt="FC-00"/> | `bg-main` | `#121418` | **Canvas.** The deepest shade. Main editor background. |
| **FC-01** | <img src="https://placehold.co/100x40/191c22/191c22/png" width="50" height="20" alt="FC-01"/> | `bg-surface` | `#191c22` | **Panels.** Sidebars, tree views, terminal backgrounds. |
| **FC-02** | <img src="https://placehold.co/100x40/2e3440/2e3440/png" width="50" height="20" alt="FC-02"/> | `bg-elevated` | `#2e3440` | **Float.** Modals, popups, cards, dropdowns. |
| **FC-03** | <img src="https://placehold.co/100x40/3b4252/3b4252/png" width="50" height="20" alt="FC-03"/> | `ui-border` | `#3b4252` | **Borders.** Splitters, rulers, input borders. |
| **FC-04** | <img src="https://placehold.co/100x40/484f5c/484f5c/png" width="50" height="20" alt="FC-04"/> | `ui-detail` | `#484f5c` | **Details.** Scrollbars, disabled states, subtle shadows. |

### 🌫️ Dawnlight (Typography)
A monochromatic scale designed to provide text hierarchy while maintaining low contrast relative to the background.

| Token ID | Swatch | Variable Name | Hex Value | Usage |
| :--- | :---: | :--- | :--- | :--- |
| **FC-05** | <img src="https://placehold.co/100x40/6a7280/6a7280/png" width="50" height="20" alt="FC-05"/> | `text-faint` | `#6a7280` | **Ignored.** Inactive line numbers, invisible characters. |
| **FC-06** | <img src="https://placehold.co/100x40/b2b6bf/b2b6bf/png" width="50" height="20" alt="FC-06"/> | `text-muted` | `#b2b6bf` | **Metadata.** Comments, timestamps, breadcrumbs. |
| **FC-07** | <img src="https://placehold.co/100x40/cbced5/cbced5/png" width="50" height="20" alt="FC-07"/> | `text-body` | `#cbced5` | **Standard.** Primary body text. Optimized for readability. |
| **FC-08** | <img src="https://placehold.co/100x40/d8dadf/d8dadf/png" width="50" height="20" alt="FC-08"/> | `text-heading` | `#d8dadf` | **Titles.** Headings, active file names. |
| **FC-09** | <img src="https://placehold.co/100x40/e4e6e9/e4e6e9/png" width="50" height="20" alt="FC-09"/> | `text-bright` | `#e4e6e9` | **Emphasis.** Bold text, hover states, strong highlights. |

### 🌊 Ocean Blues (Primary Interaction)
The core brand identity. Cool, calming blues used for navigation, selection, and primary actions.

| Token ID | Swatch | Variable Name | Hex Value | Usage |
| :--- | :---: | :--- | :--- | :--- |
| **FC-10** | <img src="https://placehold.co/100x40/5e81ac/5e81ac/png" width="50" height="20" alt="FC-10"/> | `act-subtle` | `#5e81ac` | **Secondary.** Icon buttons, unselected tabs. |
| **FC-11** | <img src="https://placehold.co/100x40/81a1c1/81a1c1/png" width="50" height="20" alt="FC-11"/> | `act-primary` | `#81a1c1` | **Brand.** Primary buttons, links, key functions. |
| **FC-12** | <img src="https://placehold.co/100x40/88c0d0/88c0d0/png" width="50" height="20" alt="FC-12"/> | `act-focus` | `#88c0d0` | **Focus.** Selection highlights, focus rings, carets. |
| **FC-13** | <img src="https://placehold.co/100x40/8fbcbb/8fbcbb/png" width="50" height="20" alt="FC-13"/> | `act-active` | `#8fbcbb` | **Active.** Toggles on, pressed states, progress bars. |
| **FC-14** | <img src="https://placehold.co/100x40/95b1b0/95b1b0/png" width="50" height="20" alt="FC-14"/> | `act-decor` | `#95b1b0` | **Ambient.** Glow effects, illustration fills. |

### 🚥 Vivid Accents (Semantic Feedback)
Strictly semantic colors. These have been optimized to diverge from the blue spectrum to ensure errors and warnings are instantly engaging.

| Token ID | Swatch | Variable Name | Hex Value | Usage |
| :--- | :---: | :--- | :--- | :--- |
| **FC-15** | <img src="https://placehold.co/100x40/bf616a/bf616a/png" width="50" height="20" alt="FC-15"/> | `state-error` | `#bf616a` | **Error.** Validation errors, destructive actions (Red). |
| **FC-16** | <img src="https://placehold.co/100x40/ebcb8b/ebcb8b/png" width="50" height="20" alt="FC-16"/> | `state-warn` | `#ebcb8b` | **Warning.** Alerts, deprecation notices (Amber). |
| **FC-17** | <img src="https://placehold.co/100x40/a3be8c/a3be8c/png" width="50" height="20" alt="FC-17"/> | `state-success` | `#a3be8c` | **Success.** Confirmations, passes, added lines (Sage). |
| **FC-18** | <img src="https://placehold.co/100x40/b48ead/b48ead/png" width="50" height="20" alt="FC-18"/> | `state-info` | `#b48ead` | **Info.** Tips, documentation links (Orchid/Purple). |
| **FC-19** | <img src="https://placehold.co/100x40/d08770/d08770/png" width="50" height="20" alt="FC-19"/> | `state-syntax` | `#d08770` | **Highlight.** Key syntax, params, distinct logic (Orange). |

## 4. Typography System

Flatcap utilizes high-quality open-source typefaces that support **Variable Font** technology for precise weight control.

| Role | Font Family | Rationale |
| :--- | :--- | :--- |
| **UI & Systems** | **Inter** | Industry standard for screen legibility. Neutral, tall x-height, and versatile. |
| **Code & Mono** | **Cascadia Code NF** | Microsoft's modern monospace. Includes ligatures (`!=`, `=>`) and Nerd Font icons out-of-the-box. |
| **Document/Serif** | **Merriweather** | Used for long-form documentation or "Reader Mode". Excellent readability on high-DPI screens. |

### Font Requirements

For the best visual experience, please install:

*   **[Inter](https://fonts.google.com/specimen/Inter)** (UI & Text)
*   **[Cascadia Code NF](https://github.com/microsoft/cascadia-code/releases)** (Code & Monospace)
*   **[Merriweather](https://fonts.google.com/specimen/Merriweather)** (Documents)

## 5. UI Metrics

To maintain the "Flat, but distinct" aesthetic:

*   **Corner Radius:** Standardize on **4px** (Soft).
*   **Elevation (Shadows):** Minimalist. Use elevation only to separate floating layers, not for decoration.
    *   *Drop Shadow:* `0 2px 10px rgba(0, 0, 0, 0.3)` (Tight and subtle).
    *   *Borders:* Prefer using `1px solid var(--fc-border)` over shadows for component separation.

## 6. Syntax Highlighting Map

This mapping separates **Logic** (Blues/Cyans) from **Data** (Greens/Purples/Oranges) to create a semantic scanning flow.

| Token Scope | Color Token | Visual Result | Logic |
| :--- | :--- | :--- | :--- |
| **Comments** | `text-muted` (FC-06) | <span style="color:#b2b6bf">Grey</span> | Recedes into background. |
| **Keywords** | `act-primary` (FC-11) | <span style="color:#81a1c1">Blue</span> | Control flow (`if`, `return`, `function`). |
| **Functions** | `act-focus` (FC-12) | <span style="color:#88c0d0">Cyan</span> | Actionable methods (`.map()`, `print()`). |
| **Classes/Types** | `act-decor` (FC-14) | <span style="color:#95b1b0">Teal</span> | Static structures (`User`, `String`, `void`). |
| **Strings** | `state-success` (FC-17)| <span style="color:#a3be8c">Sage</span> | Text content. Calm and distinct. |
| **Numbers/Const**| `state-info` (FC-18) | <span style="color:#b48ead">Orchid</span> | Immutable data (`42`, `true`, `null`). |
| **Operators** | `state-syntax` (FC-19) | <span style="color:#d08770">Orange</span> | Logic glue (`=`, `+`, `=>`, `{}`). |
| **Variables** | `text-body` (FC-07) | <span style="color:#cbced5">White/Grey</span>| Standard identifiers. |

## 7. Implementation

### CSS Variables

```css
:root {
  /* -- Deep Twilight -- */
  --fc-bg-main:     #121418;
  --fc-bg-surface:  #191c22;
  --fc-bg-elevated: #2e3440;
  --fc-border:      #3b4252;
  --fc-detail:      #484f5c;

  /* -- Dawnlight -- */
  --fc-text-faint:   #6a7280;
  --fc-text-muted:   #b2b6bf;
  --fc-text-body:    #cbced5;
  --fc-text-heading: #d8dadf;
  --fc-text-bright:  #e4e6e9;

  /* -- Ocean Blues -- */
  --fc-act-subtle:  #5e81ac;
  --fc-act-primary: #81a1c1;
  --fc-act-focus:   #88c0d0;
  --fc-act-active:  #8fbcbb;
  --fc-act-decor:   #95b1b0;

  /* -- Vivid Accents -- */
  --fc-err:         #bf616a;
  --fc-warn:        #ebcb8b;
  --fc-success:     #a3be8c;
  --fc-info:        #b48ead;
  --fc-highlight:   #d08770;
}
```

## Example Implementations

#### [Visual Studio Code](https://github.com/cheycron/flatcap-vscode)
[![Installs](https://img.shields.io/visual-studio-marketplace/i/cheycron.flatcap-theme?color=81a1c1&logo=visual-studio-code)](https://marketplace.visualstudio.com/items?itemName=cheycron.flatcap-theme)
<p align="center">
  <a href="https://github.com/cheycron/flatcap-vscode">
    <img src="https://raw.githubusercontent.com/cheycron/flatcap-vscode/main/images/screenshot.png" alt="Flatcap VS Code" width="100%"/>
  </a>
</p>

#### [Obsidian](https://github.com/cheycron/flatcap-obsidian)
![Downloads](https://img.shields.io/obsidian/downloads/theme/FlatCap?color=81a1c1&logo=obsidian)
<p align="center">
  <a href="https://github.com/cheycron/flatcap-obsidian">
    <img src="https://raw.githubusercontent.com/cheycron/flatcap-obsidian/main/screenshot.png" alt="Flatcap Obsidian" width="100%"/>
  </a>
</p>

#### [Windows Terminal](https://github.com/cheycron/flatcap-windows-terminal)
<p align="center">
  <a href="https://github.com/cheycron/flatcap-windows-terminal">
    <img src="https://raw.githubusercontent.com/cheycron/flatcap-windows-terminal/main/images/screenshot.png" alt="Flatcap Windows Terminal" width="100%"/>
  </a>
</p>

#### [Firefox](https://github.com/cheycron/flatcap-firefox)
<p align="center">
  <a href="https://github.com/cheycron/flatcap-firefox">
    <img src="https://raw.githubusercontent.com/cheycron/flatcap-firefox/main/images/screenshot.png" alt="Flatcap Firefox" width="100%"/>
  </a>
</p>

#### [FreshRSS](https://github.com/cheycron/flatcap-freshrss)
<p align="center">
  <a href="https://github.com/cheycron/flatcap-freshrss">
    <img src="https://raw.githubusercontent.com/cheycron/flatcap-freshrss/main/images/screenshot.png" alt="Flatcap FreshRSS" width="100%"/>
  </a>
</p>

---

<p align="center">
  Distributed under the MIT License.
</p>

<p align="center">
  <a href="https://www.buymeacoffee.com/cheycron">
    <img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee">
  </a>
</p>