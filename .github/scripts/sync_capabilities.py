#!/usr/bin/env python3
"""
Samakan blok "05 — Capabilities" semua karakter dengan milik Azalea:

  1. banner 16:9  (<div class="ph ph--wide">) tepat setelah judul section
  2. heading      <h3>Signature capabilities</h3> tepat sebelum daftar ability

Azalea tidak disentuh (sudah punya keduanya).
Idempoten: kalau sudah ada, tidak diduplikasi.
"""

import re
from pathlib import Path

PATH = Path("index.html")

# key section -> nama karakter (dipakai untuk nama file gambar)
KEY2NAME = {
    "v": "vorlag",
    "k": "kazagar",
    "g": "gorath",
    "a": "alleen",
    "z": "zargoth",
    "x": "vexia",
    "s": "silphira",
    "n": "nuva",
}

CAPTION = {
    "vorlag": "Wide banner · 16:9 · Nightfall",
    "kazagar": "Wide banner · 16:9 · Molten Front",
    "gorath": "Wide banner · 16:9 · The Anvil",
    "alleen": "Wide banner · 16:9 · Folded Sky",
    "zargoth": "Wide banner · 16:9 · Burning Air",
    "vexia": "Wide banner · 16:9 · Silk and Shadow",
    "silphira": "Wide banner · 16:9 · Mothlight",
    "nuva": "Wide banner · 16:9 · The Open Door",
}


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    original = text

    banners_done: list[str] = []
    h3_done: list[str] = []

    # ── 1. banner 16:9 setelah judul section capabilities ────────────────
    banner_re = re.compile(
        r'<section class="sec" id="(?P<key>[a-z])-cap">'
        r'<div class="sec__head">[^\n]*?</div>'
        r'(?!\n\s*<div class="ph ph--wide")'
    )

    def _banner(m: re.Match) -> str:
        key = m.group("key")
        name = KEY2NAME.get(key)
        if not name:
            return m.group(0)
        banners_done.append(name)
        return (
            m.group(0)
            + '\n        <div class="ph ph--wide" style="margin-bottom:24px" '
            + f'data-img="{name}-ability" data-fit="cover" '
            + f'data-label="{CAPTION[name]}"></div>'
        )

    text = banner_re.sub(_banner, text)

    # ── 2. heading "Signature capabilities" sebelum daftar ability ───────
    abilities_re = re.compile(r'(?m)^(?P<ind>[ \t]*)<div class="abilities">')

    def _h3(m: re.Match) -> str:
        before = text[max(0, m.start() - 200) : m.start()]
        if "Signature capabilities" in before:
            return m.group(0)
        h3_done.append("abilities")
        ind = m.group("ind")
        return (
            f'{ind}<h3>Signature capabilities</h3>\n'
            f'{ind}<div class="abilities">'
        )

    text = abilities_re.sub(_h3, text)

    # ── laporan ──────────────────────────────────────────────────────────
    print("banner ditambahkan :", len(banners_done), banners_done)
    print("heading ditambahkan:", len(h3_done))
    print("total .ph--wide    :", text.count("ph--wide"), "(1 di CSS + 9 banner)")
    print("total h3 Signature :", text.count("<h3>Signature capabilities</h3>"))

    if text == original:
        print("Tidak ada perubahan.")
        return 0

    PATH.write_text(text, encoding="utf-8")
    print("index.html ditulis.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
