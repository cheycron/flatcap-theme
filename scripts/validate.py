"""Validate Flatcap source integrity and foreground/background contracts."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODES = {"slate", "daylight"}
BASE_ROLES = {
    "bg.canvas", "bg.surface", "bg.raised", "bg.hover", "bg.selected",
    "border.subtle", "border.control", "text.primary", "text.secondary", "text.muted", "text.disabled",
    "accent.fg", "accent.fill", "accent.hover", "accent.pressed", "accent.on", "focus.ring",
    "success.fg", "success.bg", "warning.fg", "warning.bg", "danger.fg", "danger.bg", "info.fg", "info.bg",
    "syntax.keyword", "syntax.function", "syntax.string", "syntax.number", "syntax.type", "syntax.comment",
    "selection.bg", "selection.fg", "contrast.text.primary", "contrast.text.secondary", "contrast.text.muted", "contrast.border.control",
} | {f"data.{i}" for i in range(1, 7)}
SURFACES = ["bg.canvas", "bg.surface", "bg.raised", "bg.hover", "bg.selected"]
INFORMATIVE = ["text.primary", "text.secondary", "text.muted", "accent.fg", "success.fg", "warning.fg", "danger.fg", "info.fg",
               "syntax.keyword", "syntax.function", "syntax.string", "syntax.number", "syntax.type", "syntax.comment"]


def integrity(data):
    if data.get("name") != "Flatcap" or data.get("version") != "2.0.0" or data.get("colorSpace") != "sRGB":
        raise ValueError("Unexpected identity, version or color space")
    if set(data["themes"]) != MODES or data["defaultTheme"] != "slate":
        raise ValueError("Expected Slate and Daylight with Slate default")
    for mode, values in data["themes"].items():
        if set(values) != BASE_ROLES:
            raise ValueError(f"Unexpected color roles in {mode}: {set(values) ^ BASE_ROLES}")
        for key, value in values.items():
            if not isinstance(value, str) or not re.fullmatch(r"#[0-9A-F]{6}", value):
                raise ValueError(f"Expected opaque uppercase sRGB hex: {mode}.{key}")
    if set(data["density"]) != {"comfortable", "compact"} or set(data["elevation"]) != MODES:
        raise ValueError("Missing density or elevation mode")
    if set(data["density"]["comfortable"]) != set(data["density"]["compact"]):
        raise ValueError("Densities must expose the same metrics")
    keys = [*data["themes"]["slate"], *data["typography"], *data["metrics"], *data["density"]["comfortable"], *data["elevation"]["slate"]]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate token across groups")
    for key in keys:
        if not re.fullmatch(r"[a-z0-9]+(?:\.[a-z0-9]+)+", key):
            raise ValueError(f"Invalid token name: {key}")
    expected_groups = {
        "typography": {"font.ui", "font.dense", "font.code", "font.literal", "font.size.body", "font.size.control", "font.size.meta", "font.size.reading", "font.size.code", "font.size.heading", "font.size.title", "font.line.body", "font.line.control", "font.line.reading", "font.line.code", "font.weight.regular", "font.weight.medium", "font.weight.semibold"},
        "metrics": {"space.1", "space.2", "space.3", "space.4", "space.6", "space.8", "space.12", "radius.control", "radius.panel", "radius.dialog", "border.width", "focus.width", "focus.offset", "motion.fast", "reading.width", "target.touch"},
    }
    for group, expected in expected_groups.items():
        if set(data[group]) != expected or any(not isinstance(v, str) or not v for v in data[group].values()):
            raise ValueError(f"Unexpected {group} tokens or values")
    density_keys = {"control.min.height", "row.min.height", "control.padding.inline", "control.padding.block", "cell.padding"}
    for values in data["density"].values():
        if set(values) != density_keys or any(not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?rem", v) for v in values.values()):
            raise ValueError("Unexpected density token or length")
    for values in data["elevation"].values():
        if set(values) != {"shadow.overlay"} or not isinstance(values["shadow.overlay"], str):
            raise ValueError("Unexpected elevation tokens")
    if data["branding"]["theme"] not in MODES or set(data["branding"]["roles"]) != {"tile", "cap.crown", "cap.band", "cap.underside", "wordmark", "descriptor"}:
        raise ValueError("Unexpected branding mode or roles")
    brand_colors = data["branding"]["colors"]
    if data["branding"]["variant"] != "mineral" or set(brand_colors) != {"cap.band", "cap.underside"}:
        raise ValueError("Unexpected branding variant or dedicated colors")
    for role, value in brand_colors.items():
        if not isinstance(value, str) or not re.fullmatch(r"#[0-9A-F]{6}", value):
            raise ValueError(f"Expected opaque branding sRGB hex: {role}")
    for role in data["branding"]["roles"].values():
        if role not in BASE_ROLES | set(brand_colors):
            raise ValueError(f"Unknown branding color role: {role}")


def luminance(color):
    channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in channels]
    return sum(v * weight for v, weight in zip(linear, (.2126, .7152, .0722)))


def contrast(a, b):
    lo, hi = sorted((luminance(a), luminance(b)))
    return (hi + .05) / (lo + .05)


def contracts(data):
    integrity(data)
    checks = []

    def check(mode, fg, bg, minimum, context):
        palette = data["themes"][mode]
        ratio = contrast(palette[fg], palette[bg])
        checks.append(dict(mode=mode, foreground=fg, background=bg, minimum=minimum,
                           ratio=round(ratio, 6), passed=ratio >= minimum, context=context))

    for mode in data["themes"]:
        for bg in SURFACES:
            for fg in INFORMATIVE:
                check(mode, fg, bg, 5, "informative text and syntax")
            for fg in ["border.control", "focus.ring"]:
                check(mode, fg, bg, 3, "essential non-text information")
            check(mode, "text.primary", bg, 7, "primary text")
            for fg in ["contrast.text.primary", "contrast.text.secondary", "contrast.text.muted"]:
                check(mode, fg, bg, 7, "increased-contrast text")
            check(mode, "contrast.border.control", bg, 3, "increased-contrast boundary")
            for i in range(1, 7):
                check(mode, f"data.{i}", bg, 3, "data mark against surface; not series discriminability")
        for bg in ["accent.fill", "accent.hover", "accent.pressed"]:
            check(mode, "accent.on", bg, 4.5, "filled action label")
        for state in ["success", "warning", "danger", "info"]:
            check(mode, state + ".fg", state + ".bg", 4.5, "status label")
            check(mode, "text.primary", state + ".bg", 4.5, "status body")
            check(mode, "focus.ring", state + ".bg", 3, "focus on tinted surface")
            check(mode, "border.control", state + ".bg", 3, "control on tinted surface")
            check(mode, "contrast.border.control", state + ".bg", 3, "increased-contrast control on tinted surface")
            for fg in ["contrast.text.primary", "contrast.text.secondary", "contrast.text.muted"]:
                check(mode, fg, state + ".bg", 4.5, "increased-contrast status body")
        check(mode, "selection.fg", "selection.bg", 4.5, "selected text")
        # A filled button is identified by its fill against the OUTSIDE surface,
        # not by a neutral input border against the button's own fill.
        for fill in ["accent.fill", "accent.hover", "accent.pressed"]:
            for surface in SURFACES:
                check(mode, fill, surface, 3, "filled action against surrounding surface")
    return {"version": data["version"], "method": "WCAG 2.x relative luminance; opaque sRGB; unrounded decisions",
            "scope": "Only listed pair contracts, not product conformance, physical display quality or series discriminability",
            "total": len(checks), "passed": sum(c["passed"] for c in checks), "checks": checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "src/theme.json")
    parser.add_argument("--report", type=Path, help="Optional JSON report; not committed by default")
    args = parser.parse_args()
    report = contracts(json.loads(args.source.read_text(encoding="utf-8")))
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"{report['passed']}/{report['total']} contrast contracts passed")
    for check in report["checks"]:
        if not check["passed"]:
            print("FAIL", check)
    if report["passed"] != report["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
