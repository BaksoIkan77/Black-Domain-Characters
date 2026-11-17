#!/usr/bin/env python3
"""
Batasi efek "latar menyatu" hanya untuk landing page (roster / grid).

- body      : dikembalikan ke latar semula
- .hero     : dikembalikan ke semula (ada border pemisah + gradient sendiri),
              jadi halaman detail karakter punya sekat hero -> konten
- #view-roster .hero : versi menyatu, gradient berakhir transparan sehingga
              langsung melebur ke latar, tanpa garis

Idempoten: kalau sudah diterapkan, dilewati.
"""

from pathlib import Path

PATH = Path("index.html")

BODY_OLD = (
    "body{margin:0;overflow-wrap:break-word;\n"
    "  background:\n"
    "    radial-gradient(120% 70% at 50% -12%,rgba(126,22,48,.42) 0%,rgba(126,22,48,.16) 34%,transparent 66%),\n"
    "    radial-gradient(80% 70% at 88% 0%,rgba(58,24,88,.30) 0%,transparent 62%),\n"
    "    linear-gradient(180deg,#1b1015 0%,#150d11 16%,#0f090c 38%,#0a0708 62%,#070506 100%);\n"
    "  background-repeat:no-repeat;\n"
    "  background-color:var(--bg);\n"
)
BODY_NEW = (
    "body{margin:0;overflow-wrap:break-word;\n"
    "  background:radial-gradient(90% 60% at 50% -10%,#1a0d13 0%,transparent 60%),var(--bg);\n"
)

HERO_OLD = (
    ".hero{position:relative;overflow:hidden;background:transparent}\n"
    '.hero::before{content:"";position:absolute;left:0;right:0;bottom:0;height:70%;\n'
    '  background:linear-gradient(180deg,transparent 0%,rgba(140,30,55,.10) 45%,transparent 100%);pointer-events:none}'
)

HERO_NEW = (
    ".hero{position:relative;overflow:hidden;border-bottom:1px solid var(--line-soft);\n"
    "  background:\n"
    "    radial-gradient(110% 80% at 50% 0%,rgba(126,22,48,.48),transparent 62%),\n"
    "    radial-gradient(80% 110% at 88% 8%,rgba(58,24,88,.38),transparent 66%),\n"
    "    linear-gradient(180deg,#180e12 0%,#0a0708 88%)}\n"
    '.hero::before{content:"";position:absolute;left:0;right:0;bottom:0;height:45%;\n'
    "  background:linear-gradient(180deg,transparent,rgba(140,30,55,.10));pointer-events:none}\n"
    "/* landing (grid): hero melebur ke latar, tanpa garis potong */\n"
    "#view-roster .hero{border-bottom:0;background:\n"
    "  radial-gradient(120% 80% at 50% -10%,rgba(126,22,48,.45) 0%,rgba(126,22,48,.14) 36%,transparent 70%),\n"
    "  radial-gradient(80% 80% at 88% 0%,rgba(58,24,88,.32) 0%,transparent 62%),\n"
    "  linear-gradient(180deg,rgba(27,16,21,.88) 0%,rgba(21,13,17,.55) 38%,rgba(10,7,8,0) 100%)}\n"
    "#view-roster .hero::before{background:linear-gradient(180deg,transparent 0%,rgba(140,30,55,.10) 45%,transparent 100%)}"
)


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    original = text
    problems: list[str] = []

    # 1. body kembali ke semula
    if BODY_OLD in text:
        text = text.replace(BODY_OLD, BODY_NEW, 1)
        print("OK  body: dikembalikan ke latar semula")
    elif BODY_NEW in text:
        print("OK  body: sudah semula")
    else:
        problems.append("body: pola tidak ditemukan")

    # 2. hero: semula + override untuk landing
    if "#view-roster .hero{" in text and HERO_OLD not in text:
        print("OK  hero: override landing sudah ada")
    elif HERO_OLD in text:
        text = text.replace(HERO_OLD, HERO_NEW, 1)
        print("OK  hero: dipulihkan + override #view-roster ditambahkan")
    else:
        problems.append("hero: pola tidak ditemukan")

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
