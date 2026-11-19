#!/usr/bin/env python3
"""
Fix pager: 3 kolom sejajar (Previous | Home | Next) tidak wrap.

Masalah: flex:1 1 200px + flex-wrap:wrap → 3 item × 200px = 600px,
pada layar sempit atau sidebar sempit mereka wrap ke bawah.

Fix: flex:1 1 0 + flex-wrap:nowrap → 3 kolom selalu sejajar.
"""

from pathlib import Path

PATH = Path("commander.html")

OLD = ".pager{margin-top:60px;padding-top:22px;border-top:1px solid var(--line-soft);display:flex;gap:12px;flex-wrap:wrap}"
NEW = ".pager{margin-top:60px;padding-top:22px;border-top:1px solid var(--line-soft);display:flex;gap:12px;flex-wrap:nowrap}"

OLD_FLEX = ".pager a{flex:1 1 200px;"
NEW_FLEX = ".pager a{flex:1 1 0;min-width:0;"


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    changed = False

    if OLD in text:
        text = text.replace(OLD, NEW, 1)
        changed = True
        print("OK  flex-wrap:wrap → nowrap")
    else:
        print("OK  flex-wrap sudah nowrap (atau pola berbeda)")

    if OLD_FLEX in text:
        text = text.replace(OLD_FLEX, NEW_FLEX, 1)
        changed = True
        print("OK  flex:1 1 200px → flex:1 1 0 + min-width:0")
    else:
        print("OK  flex sudah diperbaiki (atau pola berbeda)")

    if changed:
        PATH.write_text(text, encoding="utf-8")
        print(f"commander.html ditulis: {len(text)} bytes")
    else:
        print("Tidak ada perubahan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
