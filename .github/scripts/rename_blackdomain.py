#!/usr/bin/env python3
"""
rename_blackdomain.py
=====================
Membetulkan nama ilustrasi landing page (The Black Domain).

Upload:  assets/blackdomain.webp
Dipakai: data-img="blackdomain-hero"  ->  assets/blackdomain-hero.webp

Dipindah dengan os.rename + git add supaya isi biner tidak disentuh
dan git mencatatnya sebagai `renamed`.

Idempoten: kalau file tujuan sudah ada, tidak terjadi apa-apa.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"

RENAMES = [
    ("blackdomain.webp", "blackdomain-hero.webp"),
    # cadangan kalau suatu saat di-upload sebagai PNG
    ("blackdomain.png", "blackdomain-hero.png"),
]


def main() -> int:
    moved = []

    for old_name, new_name in RENAMES:
        src, dst = ASSETS / old_name, ASSETS / new_name

        if dst.exists() and not src.exists():
            print(f"{new_name} sudah benar — dilewati.")
            continue

        if not src.exists():
            continue

        if dst.exists():
            print(f"!! bentrok: {old_name} dan {new_name} sama-sama ada — dilewati",
                  file=sys.stderr)
            continue

        src.rename(dst)
        moved.append(f"{old_name} -> {new_name}")

    if moved:
        subprocess.run(["git", "add", "-A", "assets"], cwd=ROOT, check=True)
        print("Rename berhasil:")
        for line in moved:
            print("  " + line)
    else:
        print("Tidak ada yang perlu di-rename.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
