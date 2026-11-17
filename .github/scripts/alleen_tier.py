#!/usr/bin/env python3
"""
Alleen: Tier 8.5 -> 8.6 di semua tempat, KECUALI bar stat di chart
(STR/SPD/DUR/STA/MAG tidak diubah, MAG tetap 8.5).

Cakupan:
  - kartu di halaman Roster   (cmd__meta)
  - chip di hero Alleen       (Tier 8.5)
  - daftar commander sidebar  (semua view, <span class="t">8.5</span>)

Idempoten: kalau sudah 8.6, tidak diubah.
"""

from pathlib import Path

PATH = Path("index.html")
OLD, NEW = "8.5", "8.6"

STAT_ANCHOR = '<span class="stat__v">8.5</span>'  # penanda chart, harus tetap ada


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    original = text
    total = 0

    # 1. kartu roster
    card_old = '<div class="cmd__meta"><span>Verathiel</span><b>8.5</b></div>'
    card_new = '<div class="cmd__meta"><span>Verathiel</span><b>8.6</b></div>'
    if card_old in text:
        n = text.count(card_old)
        text = text.replace(card_old, card_new)
        total += n
        print(f"OK  kartu roster          : {n}")
    else:
        print("OK  kartu roster          : sudah 8.6")

    # 2. chip hero Alleen
    chip_old = "<li>Pure Demon · Elite Path</li><li>Tier 8.5</li>"
    chip_new = "<li>Pure Demon · Elite Path</li><li>Tier 8.6</li>"
    if chip_old in text:
        n = text.count(chip_old)
        text = text.replace(chip_old, chip_new)
        total += n
        print(f"OK  chip hero             : {n}")
    else:
        print("OK  chip hero             : sudah 8.6")

    # 3. daftar commander di sidebar (semua view)
    side_old = '<span class="nm">Alleen</span><span class="t">8.5</span>'
    side_new = '<span class="nm">Alleen</span><span class="t">8.6</span>'
    if side_old in text:
        n = text.count(side_old)
        text = text.replace(side_old, side_new)
        total += n
        print(f"OK  sidebar commander     : {n} view")
    else:
        print("OK  sidebar commander     : sudah 8.6")

    # ── verifikasi: chart tidak ikut berubah ────────────────────────────
    if STAT_ANCHOR not in text:
        print("!!  PERINGATAN: bar stat MAG 8.5 hilang dari chart")
        return 1
    print("OK  chart stat tetap      : MAG 8.5 utuh")

    if text == original:
        print("Tidak ada perubahan.")
        return 0

    PATH.write_text(text, encoding="utf-8")
    print(f"index.html ditulis ({total} penggantian).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
