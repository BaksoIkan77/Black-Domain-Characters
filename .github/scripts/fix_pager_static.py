#!/usr/bin/env python3
"""
Paksa pager (Previous | Home | Next) selalu 3 kolom sejajar di semua ukuran layar/zoom.

Masalah: aturan lama punya flex-wrap:wrap + flex-basis besar, sehingga pada viewport
sempit (mobile / zoom besar) tombol turun ke baris baru.

Fix: override di akhir <style> (menang urutan cascade):
- .pager{flex-wrap:nowrap}
- .pager a{flex:1 1 0;min-width:0;overflow:hidden}
- label di dalam tombol pakai ellipsis supaya nama panjang tidak memaksa lebar
- di layar kecil padding & font diperkecil agar 3 kolom tetap muat
"""

import re
from pathlib import Path

MARKER = "PAGER: 3 kolom selalu sejajar"

OVERRIDE = """
/* ═══ PAGER: 3 kolom selalu sejajar ═══ */
.pager{display:flex;gap:12px;flex-wrap:nowrap;align-items:stretch}
.pager a{flex:1 1 0;min-width:0;overflow:hidden}
.pager small{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pager strong{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
@media (max-width:620px){
  .pager{gap:8px}
  .pager a{padding:13px 11px}
  .pager small{font-size:8px;letter-spacing:.1em}
  .pager strong{font-size:13.5px;line-height:1.25}
}
</style>
"""


def patch(path: Path) -> None:
    if not path.exists():
        print(f"!!  {path} tidak ada")
        return
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        print(f"OK  {path}: override pager sudah ada")
        return
    if "</style>" not in text:
        print(f"!!  {path}: </style> tidak ditemukan")
        return
    # ganti </style> pertama (head) dengan override
    text = text.replace("</style>", OVERRIDE.strip() + "\n", 1)
    path.write_text(text, encoding="utf-8")
    print(f"OK  {path}: override pager ditambahkan ({len(text)} bytes)")


def main() -> int:
    patch(Path("commander.html"))
    patch(Path("index.html"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
