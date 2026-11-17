#!/usr/bin/env python3
"""
Rename file biner di assets/ memakai `git mv` (isi file tidak disentuh,
riwayat tetap terjaga).

Daftar: (nama lama, nama baru)
Idempoten: kalau sudah di-rename, dilewati.
"""

import subprocess
from pathlib import Path

RENAMES = [
    ("assets/allen-partial.webp", "assets/alleen-partial.webp"),
]


def main() -> int:
    problems: list[str] = []

    for src, dst in RENAMES:
        s, d = Path(src), Path(dst)

        if not s.exists() and d.exists():
            print(f"OK  {src} -> {dst}: sudah di-rename")
            continue
        if not s.exists():
            problems.append(f"{src}: tidak ditemukan")
            continue
        if d.exists():
            problems.append(f"{dst}: sudah ada, rename dilewati")
            continue

        subprocess.run(["git", "mv", src, dst], check=True)
        print(f"OK  {src} -> {dst}")

    for p in problems:
        print("!! ", p)

    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
