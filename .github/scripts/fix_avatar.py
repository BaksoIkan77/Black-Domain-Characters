#!/usr/bin/env python3
"""
Fix avatar roster (bundar) di sidebar commander.html tidak terload.

Penyebab: saat split, data-view="azalea" diubah jadi href="commander.html#azalea".
Loader avatar masih membaca link.dataset.view (sekarang undefined) -> returnearly,
gambar tidak pernah dimuat.

Fix: ambil ID dari href hash (#azalea / commander.html#azalea).
"""

from pathlib import Path

PATH = Path("commander.html")

OLD = """    const link = av.closest('a');
    const id = link && link.dataset.view;
    if (!id) return;"""

NEW = """    const link = av.closest('a');
    const href = link && (link.getAttribute('href') || '');
    const m = href && href.match(/#(\\w+)$/);
    const id = m && m[1];
    if (!id) return;"""


def main() -> int:
    text = PATH.read_text(encoding="utf-8")

    if NEW in text:
        print("OK  sudah diperbaiki")
        return 0
    if OLD not in text:
        print("!!  pola lama tidak ditemukan")
        return 1

    text = text.replace(OLD, NEW, 1)
    PATH.write_text(text, encoding="utf-8")
    print("OK  avatar loader diperbaiki (id dari href hash)")
    print(f"commander.html ditulis: {len(text)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
