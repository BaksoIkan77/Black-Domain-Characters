#!/usr/bin/env python3
"""
Lengkapi baris "Tier" di tabel Record (infobox Overview) tiap karakter,
mengikuti format Azalea:  <b>8.9</b> · Ruler

Azalea tidak disentuh (sudah lengkap).
Idempoten: aman dijalankan berulang.
"""

import re
from pathlib import Path

PATH = Path("index.html")

# key section -> (nama karakter, isi <dd> baru)
NEW_TIER = {
    "v": ("vorlag", "<b>8.7</b> · Ruler · 9.0 at midnight"),
    "k": ("kazagar", "<b>8.7</b> · Vanguard"),
    "g": ("gorath", "<b>8.7</b> · Tanker"),
    "a": ("alleen", "<b>8.6</b> · Magician"),
    "z": ("zargoth", "<b>8.0</b> · Versatile"),
    "x": ("vexia", "<b>7.8</b> · Magician / Assassin"),
    "s": ("silphira", "<b>7.7</b> · Speedster"),
    "n": ("nuva", "<b>7.6</b> · Assassin"),
}


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    original = text
    problems: list[str] = []

    for key, (name, dd) in NEW_TIER.items():
        section_re = re.compile(
            rf'<section class="sec" id="{key}-over">.*?</section>', re.S
        )
        m = section_re.search(text)
        if not m:
            problems.append(f"{name}: section #{key}-over tidak ditemukan")
            continue

        window = m.group(0)
        new_window, count = re.subn(
            r"<dt>Tier</dt><dd>.*?</dd>",
            f"<dt>Tier</dt><dd>{dd}</dd>",
            window,
            count=1,
        )
        if count != 1:
            problems.append(f"{name}: baris Tier tidak ditemukan")
            continue

        text = text[: m.start()] + new_window + text[m.end() :]
        print(f"OK  {name:<9} -> {dd}")

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
