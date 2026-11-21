#!/usr/bin/env python3
"""
rename_silphira.py
==================
Merapikan nama aset ilustrasi Silphira yang ter-upload dengan typo
("shilpira-" -> "silphira-").

Mengapa lewat CI dan bukan lewat API teks: file ilustrasi itu biner.
Dipindahkan dengan os.rename + git add, jadi isi file tidak dibaca/ditulis
ulang sama sekali dan git mencatatnya sebagai `renamed` (riwayat utuh).

Idempoten: file yang sudah bernama benar dilewati, dan kalau tidak ada
satu pun yang berubah, tidak ada commit (bot memang berhenti sendiri).

Tidak ada HTML yang diubah: codex.js sudah punya alias shilpira/silphira
sebagai pengaman, jadi gambar tetap tampil selama transisi.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"

RENAMES = [
    ("shilpira-hero.webp", "silphira-hero.webp"),
    ("shilpira-elite.webp", "silphira-elite.webp"),
    ("shilpira-monstrous.webp", "silphira-monstrous.webp"),
    ("shilpira-cinematic.webp", "silphira-cinematic.webp"),
    ("shilpira-ability.webp", "silphira-ability.webp"),
    ("shilpira-grid.jpg", "silphira-grid.jpg"),
    ("shilpira-roster.jpg", "silphira-roster.jpg"),
]


def main() -> int:
    moved, skipped, missing = [], [], []

    for old_name, new_name in RENAMES:
        src, dst = ASSETS / old_name, ASSETS / new_name

        if dst.exists() and not src.exists():
            skipped.append(new_name)
            continue

        if not src.exists():
            missing.append(old_name)
            continue

        if dst.exists():
            print(f"!! bentrok: {old_name} dan {new_name} sama-sama ada — dilewati",
                  file=sys.stderr)
            continue

        src.rename(dst)
        moved.append(f"{old_name} -> {new_name}")

    if moved:
        # git mv di atas os.rename hanya untuk memastikan index ikut ter-stage;
        # -A menangkap pasangan rename supaya git melabelinya "renamed".
        subprocess.run(["git", "add", "-A", "assets"], cwd=ROOT, check=True)
        print("Rename berhasil:")
        for line in moved:
            print("  " + line)

    if skipped:
        print("Sudah bernama benar (dilewati): " + ", ".join(skipped))
    if missing:
        print("Tidak ditemukan di assets/: " + ", ".join(missing))
    if not moved:
        print("Tidak ada yang perlu di-rename.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
