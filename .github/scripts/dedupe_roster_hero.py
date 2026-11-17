#!/usr/bin/env python3
"""
Bersihkan duplikat blok override hero landing (#view-roster .hero).

Blok ini sempat tertulis dua kali karena dua script lama saling menimpa.
Efek visualnya tidak berubah (aturannya identik), tapi source jadi kotor.
Idempoten: kalau hanya ada satu blok, tidak melakukan apa-apa.
"""

from pathlib import Path

PATH = Path("index.html")

BLOCK = (
    "/* landing (grid): hero melebur ke latar, tanpa garis potong */\n"
    "#view-roster .hero{border-bottom:0;background:\n"
    "  radial-gradient(120% 80% at 50% -10%,rgba(126,22,48,.45) 0%,rgba(126,22,48,.14) 36%,transparent 70%),\n"
    "  radial-gradient(80% 80% at 88% 0%,rgba(58,24,88,.32) 0%,transparent 62%),\n"
    "  linear-gradient(180deg,rgba(27,16,21,.88) 0%,rgba(21,13,17,.55) 38%,rgba(10,7,8,0) 100%)}\n"
    "#view-roster .hero::before{background:linear-gradient(180deg,transparent 0%,"
    "rgba(140,30,55,.10) 45%,transparent 100%)}\n"
)


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    n = text.count(BLOCK)

    if n <= 1:
        print(f"OK  blok #view-roster .hero: {n} salinan, tidak ada duplikat")
        return 0

    text = text.replace(BLOCK, "", n - 1)
    PATH.write_text(text, encoding="utf-8")
    print(f"OK  blok #view-roster .hero: {n} salinan -> 1 (duplikat dihapus)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
