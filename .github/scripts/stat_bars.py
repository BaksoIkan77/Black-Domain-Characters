#!/usr/bin/env python3
"""
Perbarui bar stat (Pillar Distribution) untuk Gorath, Nuva, Alleen, Vexia.

Setiap bar ditulis ulang lengkap per section: lebar (--v) dihitung otomatis
dari nilainya (8.5 -> 85%), supaya chart dan angka selalu sinkron.
Idempoten: aman dijalankan berulang.
"""

import re
from pathlib import Path

PATH = Path("index.html")

# key section -> (nama, [(label, nilai), ...] urut STR/SPD/DUR/STA/MAG)
VALUES = {
    "g": ("gorath", [("STR", "7.1"), ("SPD", "6.2"), ("DUR", "8.7"), ("STA", "8.5"), ("MAG", "6.9")]),
    "n": ("nuva", [("STR", "7.0"), ("SPD", "7.6"), ("DUR", "6.1"), ("STA", "7.3"), ("MAG", "7.1")]),
    "a": ("alleen", [("STR", "7.2"), ("SPD", "7.2"), ("DUR", "7.0"), ("STA", "7.5"), ("MAG", "8.6")]),
    "x": ("vexia", [("STR", "6.7"), ("SPD", "7.5"), ("DUR", "6.1"), ("STA", "7.0"), ("MAG", "7.8")]),
}


def pct(value: str) -> int:
    """'8.5' -> 85"""
    return int(round(float(value) * 10))


def build_block(rows: list[tuple[str, str]]) -> str:
    lines = ['        <div class="stats">']
    for label, value in rows:
        lines.append(
            f'          <div class="stat"><span class="stat__k">{label}</span>'
            f'<div class="stat__bar"><i style="--v:{pct(value)}%"></i></div>'
            f'<span class="stat__v">{value}</span></div>'
        )
    lines.append("        </div>")
    return "\n".join(lines)


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    original = text
    problems: list[str] = []

    for key, (name, rows) in VALUES.items():
        section_re = re.compile(rf'<section class="sec" id="{key}-cap">.*?</section>', re.S)
        m = section_re.search(text)
        if not m:
            problems.append(f"{name}: section #{key}-cap tidak ditemukan")
            continue

        window = m.group(0)
        new_window, count = re.subn(
            r'<div class="stats">.*?\n        </div>',
            build_block(rows),
            window,
            count=1,
            flags=re.S,
        )
        if count != 1:
            problems.append(f"{name}: blok .stats tidak ditemukan")
            continue

        text = text[: m.start()] + new_window + text[m.end() :]
        print(f"OK  {name:<9} -> " + "  ".join(f"{k} {v}" for k, v in rows))

    for p in problems:
        print("!! ", p)

    if text == original:
        print("Tidak ada perubahan.")
    else:
        PATH.write_text(text, encoding="utf-8")
        print("index.html ditulis.")

    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
