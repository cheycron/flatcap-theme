"""Render trusted repository SVG masters to PNG. Requires CairoSVG 2.8.2.

Run after scripts/build.py. PNG files are derived artifacts; never edit them directly.
"""
import argparse
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = [("logo", 500, 500), ("readme_logo", 415, 600)]


def render(name, width, height):
    import cairosvg
    return cairosvg.svg2png(url=str(ROOT / "src" / f"{name}.svg"),
                           output_width=width, output_height=height)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Compare decoded pixels without writing")
    args = parser.parse_args()
    for name, width, height in ASSETS:
        target = ROOT / "images" / f"{name}.png"
        content = render(name, width, height)
        if args.check:
            from PIL import Image
            if not target.exists():
                parser.exit(1, f"Missing {target.relative_to(ROOT)}\n")
            actual = Image.open(target).convert("RGBA")
            expected = Image.open(io.BytesIO(content)).convert("RGBA")
            if actual.size != expected.size or actual.tobytes() != expected.tobytes():
                parser.exit(1, f"Stale PNG: {target.relative_to(ROOT)}\n")
            print(f"Pixel parity OK: {target.relative_to(ROOT)}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            print(f"Rendered {target.relative_to(ROOT)} ({width}×{height})")


if __name__ == "__main__":
    main()
