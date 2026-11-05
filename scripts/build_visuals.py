"""Generate README presentation boards from the canonical JSON (stdlib only).

Run after build.py. This generates HTML, not screenshots or a second token source.
Capture instructions: images/readme/README.md. --check never writes.
"""
import argparse
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def render():
    data = json.loads((ROOT / 'src/theme.json').read_text())
    def variables(theme):
        return ';'.join(f'--fc-{key.replace(".", "-")}:{value}' for key, value in theme.items())
    def panel(mode, palette=False):
        theme = data['themes'][mode]
        heading = 'Slate' if mode == 'slate' else 'Daylight'
        subtitle = 'Matte graphite · mineral blue' if mode == 'slate' else 'Soft surfaces · deliberate contrast'
        top = f'<section class="mode" style="{escape(variables(theme), quote=True)}"><header><span class="eyebrow">{heading.upper()}</span><h2>{heading}</h2><p>{subtitle}</p></header>'
        if palette:
            groups = [('Surfaces', ['bg.canvas', 'bg.surface', 'bg.raised', 'bg.hover', 'bg.selected']), ('Ink & structure', ['text.primary', 'text.secondary', 'text.muted', 'border.subtle', 'border.control']), ('Interaction', ['accent.fg', 'accent.fill', 'accent.on', 'focus.ring']), ('Feedback foregrounds', ['success.fg', 'warning.fg', 'danger.fg', 'info.fg'])]
            for title, roles in groups:
                top += f'<h3>{title}</h3><div class="swatches">'
                for role in roles:
                    top += f'<div class="swatch"><span style="background:{theme[role]}"></span><code>{role}</code><small>{theme[role]}</small></div>'
                top += '</div>'
            top += '<h3>Categorical data · identity, not status</h3><div class="series">'
            for i in range(1, 7):
                top += f'<div><span style="background:{theme[f"data.{i}"]}"></span><code>data.{i}</code><small>{theme[f"data.{i}"]}</small></div>'
            return top + '</div></section>'
        return top + '''<div class="sample-head"><div><small class="eyebrow">WORKSPACE / OVERVIEW</small><h3>Everything in its place.</h3></div><span class="small-link">View activity →</span></div>
<p class="description">Clear hierarchy. Useful color. Room for the work.</p>
<div class="service"><span>API / operations</span><span class="badge success">✓ Available</span><span>42 ms</span></div>
<div class="service"><span>Report queue</span><span class="badge warning">! Review</span><span>218 ms</span></div>
<div class="service"><span>Audit archive</span><span class="badge danger">× Offline</span><span>—</span></div>
<div class="editor"><span class="comment">// Let the content lead.</span><br><span class="keyword">const</span> theme = <span class="string">"flatcap"</span>;<br><span class="keyword">if</span> (ready) <span class="function">start</span>(theme);</div>
<div class="sample-controls"><span class="primary">Save changes</span><span class="secondary">View details</span><span class="focus">Visible focus</span></div>
<div class="category-label">CATEGORIES ≠ FEEDBACK</div><div class="categories">''' + ''.join(f'<span><i style="background:{theme[f"data.{i}"]}"></i>0{i}</span>' for i in range(1, 7)) + '</div></section>'
    return '''<!doctype html>
<html lang="en" data-fc-theme="slate"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Flatcap — visual overview</title><link rel="stylesheet" href="../src/theme.css"><style>
*{box-sizing:border-box}body{margin:0;background:var(--fc-bg-canvas);color:var(--fc-text-primary);font:16px/1.5 var(--fc-font-ui)}.board{width:1440px;padding:56px 56px 40px}.mast{display:flex;justify-content:space-between;align-items:center;margin-bottom:36px}.identity{display:flex;gap:16px;align-items:center;font-size:24px;font-weight:500}.identity img{width:48px;height:48px}.release{font-size:14px;color:var(--fc-text-secondary);letter-spacing:.08em}.lede{display:flex;justify-content:space-between;align-items:end;margin-bottom:36px}.lede h1{font-size:52px;font-weight:500;line-height:1.1;margin:0}.lede p{max-width:460px;margin:0;color:var(--fc-text-secondary);font-size:18px}.modes{display:grid;grid-template-columns:1fr 1fr;gap:24px}.mode{padding:32px;background:var(--fc-bg-canvas);color:var(--fc-text-primary);border:1px solid var(--fc-border-subtle);border-radius:8px;overflow:hidden}.mode header{border-bottom:1px solid var(--fc-border-subtle);padding-bottom:20px;margin-bottom:24px}.eyebrow{font-size:12px;letter-spacing:.12em;color:var(--fc-text-secondary)}h2{font-size:32px;font-weight:500;margin:4px 0}header p{margin:0;color:var(--fc-text-secondary)}h3{font-size:18px;font-weight:500;margin:8px 0}.sample-head{display:flex;justify-content:space-between;align-items:end;gap:12px}.small-link{font-size:13px;color:var(--fc-accent-fg);white-space:nowrap}.description{font-size:14px;color:var(--fc-text-muted);margin:4px 0 24px}.service{display:grid;grid-template-columns:1fr 118px 60px;align-items:center;gap:12px;padding:14px 0;border-bottom:1px solid var(--fc-border-subtle);font-size:14px}.service>span:last-child{text-align:right;font-variant-numeric:tabular-nums}.badge{padding:4px 8px;border-radius:4px;font-size:13px;justify-self:start}.success{color:var(--fc-success-fg);background:var(--fc-success-bg)}.warning{color:var(--fc-warning-fg);background:var(--fc-warning-bg)}.danger{color:var(--fc-danger-fg);background:var(--fc-danger-bg)}.editor{font:15px/1.8 var(--fc-font-code);padding:20px;margin:24px 0;background:var(--fc-bg-surface);border-radius:6px}.comment{color:var(--fc-syntax-comment)}.keyword{color:var(--fc-syntax-keyword)}.string{color:var(--fc-syntax-string)}.function{color:var(--fc-syntax-function)}.sample-controls{display:flex;gap:12px;align-items:center;font-size:13px}.sample-controls>span{padding:10px 14px;border-radius:4px}.primary{background:var(--fc-accent-fill);color:var(--fc-accent-on)}.secondary{border:1px solid var(--fc-border-control)}.focus{outline:2px solid var(--fc-focus-ring);outline-offset:2px}.category-label{font-size:11px;letter-spacing:.1em;color:var(--fc-text-secondary);margin:30px 0 12px}.categories{display:flex;justify-content:space-between;font-size:13px}.categories span{display:flex;gap:8px;align-items:center}.categories i{width:10px;height:10px}.caption{display:flex;justify-content:space-between;margin-top:28px;color:var(--fc-text-secondary);font-size:13px}.palette h1{font-size:40px}.palette .mode h3{font-size:14px;margin:22px 0 12px}.palette .mode{padding:28px}.palette .mode header{margin-bottom:16px}.swatches{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}.swatch{min-width:0}.swatch>span{display:block;height:48px;border-radius:4px;border:1px solid var(--fc-border-control);margin-bottom:8px}code{font:11px var(--fc-font-code)}.swatch code{display:block;font-size:10px;white-space:nowrap}small{color:var(--fc-text-secondary);font-size:11px}.series{display:flex;gap:12px}.series>div{flex:1;min-width:0}.series span{display:block;height:32px;border-radius:4px;margin-bottom:8px}.series code,.series small{display:block}a{color:var(--fc-accent-fg)}
</style></head><body>
<section class="board" id="overview"><div class="mast"><div class="identity"><img src="../src/logo.svg" alt="">Flatcap</div><span class="release">2.0 / SEMANTIC VISUAL SYSTEM</span></div><div class="lede"><h1>Quiet precision.</h1><p>The interface organizes.<br>Content takes the foreground. Color informs.</p></div><div class="modes">''' + panel('slate') + panel('daylight') + '''</div><div class="caption"><span>Neutral graphite · mineral blue · matte surfaces</span><span>IBM Plex Sans / Cascadia Code</span></div></section>
<section class="board palette" id="palette"><div class="mast"><div class="identity"><img src="../src/logo.svg" alt="">Flatcap / color by purpose</div><span class="release">2.0 / SELECTED SEMANTIC ROLES</span></div><div class="lede"><h1>One system. Two considered modes.</h1><p>Not an inversion. Each mode has its own tuned values.<br>Roles stay stable; their colors adapt.</p></div><div class="modes">''' + panel('slate', True) + panel('daylight', True) + '''</div><div class="caption"><span>Generated from src/theme.json · sRGB · standard contrast</span><span>Selected roles only. Full 43-role palette per mode: docs/palette.md</span></div></section>
</body></html>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    target = ROOT / 'docs/visual-preview.html'
    content = render()
    if args.check:
        if not target.exists() or target.read_text() != content:
            parser.exit(1, 'Visual boards are stale; run python3 scripts/build_visuals.py\n')
        print('Visual boards are current')
    else:
        target.write_text(content)
        print('Generated docs/visual-preview.html')


if __name__ == '__main__':
    main()
