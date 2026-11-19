#!/usr/bin/env python3
"""
Tambah "Home / Main Page" di tengah pager semua commander.
"""

import re
from pathlib import Path

PATH = Path("commander.html")

ORDER = [
    ("azalea",   "nuva",      "Nuva",      "vorlag",   "Vorlag"),
    ("vorlag",   "azalea",    "Azalea",    "kazagar",  "Kazagar"),
    ("kazagar",  "vorlag",    "Vorlag",    "gorath",   "Gorath"),
    ("gorath",   "kazagar",   "Kazagar",   "alleen",   "Alleen"),
    ("alleen",   "gorath",    "Gorath",    "zargoth",  "Zar'goth"),
    ("zargoth",  "alleen",    "Alleen",    "vexia",    "Vexia"),
    ("vexia",    "zargoth",   "Zar'goth",  "silphira", "Silphira"),
    ("silphira", "vexia",     "Vexia",     "nuva",     "Nuva"),
    ("nuva",     "silphira",  "Silphira",  "azalea",   "Azalea"),
]


def build_pager(pid, pn, nid, nn):
    return (
        f'<nav class="pager">'
        f'<a href="commander.html#{pid}"><small>← Previous</small><strong>{pn}</strong></a>'
        f'<a href="index.html" style="text-align:center"><small>Home</small><strong>Main Page</strong></a>'
        f'<a href="commander.html#{nid}" style="text-align:right"><small>Next →</small><strong>{nn}</strong></a>'
        f'</nav>'
    )


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    count = 0

    for cid, pid, pn, nid, nn in ORDER:
        new_pager = build_pager(pid, pn, nid, nn)
        if new_pager in text:
            print(f"OK  {cid:<9}: sudah 3-kolom")
            continue

        # Cari pager lama berdasarkan pola yang berisi commander sebelumnya/sesudahnya
        if cid == "azalea":
            old = r'<nav class="pager"><a href="index\.html"><small>← Back</small><strong>All Commanders</strong></a>\s*<a href="commander\.html#vorlag"[^>]*><small>Next →</small><strong>Vorlag, the Night King</strong></a></nav>'
        elif cid == "nuva":
            old = r'<nav class="pager"><a href="commander\.html#silphira"><small>← Previous</small><strong>Silphira</strong></a>\s*<a href="index\.html"[^>]*><small>Back to</small><strong>All Commanders</strong></a></nav>'
        else:
            old = rf'<nav class="pager"><a href="commander\.html#{re.escape(pid)}"><small>← Previous</small><strong>{re.escape(pn)}</strong></a>\s*<a href="commander\.html#{re.escape(nid)}"[^>]*><small>Next →</small><strong>{re.escape(nn)}</strong></a></nav>'

        new_text, n = re.subn(old, new_pager, text, count=1)
        if n > 0:
            text = new_text
            count += 1
            print(f"OK  {cid:<9}: pager diperbarui")
        else:
            print(f"!!  {cid:<9}: pager tidak ditemukan")

    if count > 0:
        PATH.write_text(text, encoding="utf-8")
        print(f"commander.html ditulis ({count} pager diperbarui)")
    else:
        print("Tidak ada perubahan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
