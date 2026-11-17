#!/usr/bin/env python3
"""
Perbaikan tampilan desktop:

1. Keepsake (Azalea): gambar 4:3 dipaksa `height:100%` sehingga lebarnya
   melebar melewati kolom 250px dan menutupi awal setiap baris teks.
   Solusi: beri `width:100%;min-width:0` supaya tetap di dalam kolomnya.

2. Teks paragraf: `max-width` dalam ch membuat baris berhenti lebih awal
   dan menyisakan ruang kosong di kanan pada layar lebar.
   Solusi: hilangkan batasnya untuk blok prosa (paragraf utama, panel form,
   timeline, caption plate). Kutipan (.quote p) & hero__tag dibiarkan.

Idempoten: kalau sudah diterapkan, dilewati.
"""

from pathlib import Path

PATH = Path("index.html")

FIXES = [
    (
        "keepsake: gambar meluber ke kolom teks",
        ".keepsake .ph{border:0;border-radius:0;aspect-ratio:4/3;height:100%}",
        ".keepsake .ph{border:0;border-radius:0;aspect-ratio:4/3;height:100%;width:100%;min-width:0}",
    ),
    (
        "paragraf section: batas 70ch",
        ".sec p{margin:0 0 15px;color:var(--ink-2);max-width:70ch}",
        ".sec p{margin:0 0 15px;color:var(--ink-2);max-width:none}",
    ),
    (
        "paragraf panel form: batas 66ch",
        ".panel p{margin:0 auto 12px;font-size:14.5px;color:var(--ink-2);max-width:66ch;text-align:left}",
        ".panel p{margin:0 auto 12px;font-size:14.5px;color:var(--ink-2);max-width:none;text-align:left}",
    ),
    (
        "paragraf timeline: batas 66ch",
        ".tl__item p{margin:0;font-size:14.5px;line-height:1.68;color:var(--ink-2);max-width:66ch}",
        ".tl__item p{margin:0;font-size:14.5px;line-height:1.68;color:var(--ink-2);max-width:none}",
    ),
    (
        "caption plate: batas 74ch",
        ".plate figcaption p{margin:0;max-width:74ch;font:400 15px/1.7 var(--serif);color:var(--ink-2)}",
        ".plate figcaption p{margin:0;font:400 15px/1.7 var(--serif);color:var(--ink-2)}",
    ),
]


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    original = text
    problems: list[str] = []

    for label, old, new in FIXES:
        if new in text and old not in text:
            print(f"OK  {label:<45}: sudah diterapkan")
            continue
        if old not in text:
            problems.append(f"{label}: pola CSS tidak ditemukan")
            continue
        n = text.count(old)
        text = text.replace(old, new)
        print(f"OK  {label:<45}: {n} aturan diubah")

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
