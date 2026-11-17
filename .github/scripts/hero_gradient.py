#!/usr/bin/env python3
"""
Landing page: hilangkan "balok" hero yang terpotong.

Sebelumnya:
  - .hero punya background sendiri (radial + linear) yang berakhir di #0a0708
  - lalu dipotong `border-bottom` 1px
  - body punya dasar #1a0d13 yang lebih terang
  => muncul garis/tepian keras tepat di bawah hero.

Sesudah:
  - latar dipindah ke body: dua glow radial halus di atas + gradient vertikal
    yang makin gelap ke bawah sampai #070506, tanpa henti di tengah
  - .hero jadi transparan, border bawah dihapus -> menyambung mulus
  - .hero::before diubah agar memudar ke transparan di dasar hero

Idempoten: kalau sudah diterapkan, dilewati.
"""

from pathlib import Path

PATH = Path("index.html")

FIXES = [
    (
        "body: gradient panjang makin gelap ke bawah",
        "body{margin:0;overflow-wrap:break-word;\n"
        "  background:radial-gradient(90% 60% at 50% -10%,#1a0d13 0%,transparent 60%),var(--bg);\n",
        "body{margin:0;overflow-wrap:break-word;\n"
        "  background:\n"
        "    radial-gradient(120% 70% at 50% -12%,rgba(126,22,48,.42) 0%,rgba(126,22,48,.16) 34%,transparent 66%),\n"
        "    radial-gradient(80% 70% at 88% 0%,rgba(58,24,88,.30) 0%,transparent 62%),\n"
        "    linear-gradient(180deg,#1b1015 0%,#150d11 16%,#0f090c 38%,#0a0708 62%,#070506 100%);\n"
        "  background-repeat:no-repeat;\n"
        "  background-color:var(--bg);\n",
    ),
    (
        "hero: transparan, tanpa border bawah",
        ".hero{position:relative;overflow:hidden;border-bottom:1px solid var(--line-soft);\n"
        "  background:\n"
        "    radial-gradient(110% 80% at 50% 0%,rgba(126,22,48,.48),transparent 62%),\n"
        "    radial-gradient(80% 110% at 88% 8%,rgba(58,24,88,.38),transparent 66%),\n"
        "    linear-gradient(180deg,#180e12 0%,#0a0708 88%)}",
        ".hero{position:relative;overflow:hidden;background:transparent}",
    ),
    (
        "hero::before: memudar di dasar",
        '.hero::before{content:"";position:absolute;left:0;right:0;bottom:0;height:45%;\n'
        '  background:linear-gradient(180deg,transparent,rgba(140,30,55,.10));pointer-events:none}',
        '.hero::before{content:"";position:absolute;left:0;right:0;bottom:0;height:70%;\n'
        '  background:linear-gradient(180deg,transparent 0%,rgba(140,30,55,.10) 45%,transparent 100%);'
        "pointer-events:none}",
    ),
]


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    original = text
    problems: list[str] = []

    for label, old, new in FIXES:
        if new in text and old not in text:
            print(f"OK  {label:<42}: sudah diterapkan")
            continue
        if old not in text:
            problems.append(f"{label}: pola tidak ditemukan")
            continue
        text = text.replace(old, new, 1)
        print(f"OK  {label:<42}: diubah")

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
