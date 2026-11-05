"""Measure the documented font corpus without installing or downloading fonts.

Requires Pillow with RAQM and Fontconfig's fc-scan. Output never includes full paths.
"""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

import PIL
from PIL import ImageFont, features

SAMPLES = [
    "Configuración del sistema",
    "Administración de servicios",
    "Última actualización: hace 5 minutos",
    "Seleccionar todos los registros",
    "Pendiente de revisión",
    "Error de conexión con el servidor",
    "Guardar cambios",
    "CPU 24,8 % · RAM 16,2 GB",
    "El servicio responde correctamente. Revisá los registros y la configuración antes de continuar.",
    "ÁÉÍÓÚ áéíóú ñ Ñ ü ¿Qué pasó? ¡Conexión!",
    "Il1 | O0 · 0123456789 · rn m",
    "if (value !== null && total >= 10) return result;",
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plex-dir", required=True, type=Path)
    parser.add_argument("--fonts-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if not features.check("raqm"):
        parser.error("Pillow must include RAQM to reproduce this shaping method")
    files = {
        "IBM Plex Sans": args.plex_dir / "IBMPlexSans-Regular.ttf",
        "IBM Plex Sans Condensed": args.plex_dir / "IBMPlexSansCondensed-Regular.ttf",
        "Inter": args.fonts_dir / "Inter-VariableFont_opsz,wght.ttf",
        "Source Sans 3": args.fonts_dir / "SourceSans3-VariableFont_wght.ttf",
        "Cascadia Code": args.fonts_dir / "CascadiaCode.ttf",
        "JetBrains Mono (Nerd Font build)": args.fonts_dir / "JetBrainsMonoNerdFontMono-Regular.ttf",
    }
    report = {
        "method": "Pillow FreeType with RAQM; 14 px, weight 400, Inter optical size 14; default shaping; lengths in px; same nominal size is NOT equal perceived size",
        "pillow": PIL.__version__,
        "raqm": features.check("raqm"),
        "samples": SAMPLES,
        "fonts": [],
    }
    for name, path in files.items():
        font = ImageFont.truetype(str(path), 14)
        try:
            axes = font.get_variation_axes()
        except OSError:
            axes = []
        if axes:
            font.set_variation_by_axes([
                400 if axis["name"] == b"Weight"
                else 14 if axis["name"] == b"Optical size"
                else axis["default"]
                for axis in axes
            ])
        widths = [round(font.getlength(text), 4) for text in SAMPLES]
        metadata = subprocess.check_output(
            ["fc-scan", "--format", "%{family}\n%{style}\n%{fontversion}", str(path)],
            text=True,
        )
        report["fonts"].append({
            "family": name,
            "file": path.name,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "metadata": metadata,
            "axes": [dict(axis, name=axis["name"].decode()) for axis in axes],
            "widths": widths,
            "uiCorpusTotal": round(sum(widths[:8]), 4),
            "monoCell": round(font.getlength("0"), 6),
            "asciiColumnsIn960px": math.floor(960 / font.getlength("0")),
        })
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"Measured {len(files)} fonts; report: {args.output}")


if __name__ == "__main__":
    main()
