#!/usr/bin/env python3
"""
Fix: terlalu banyak empty space di landing page (desktop).

Penyebab:
  1. Roster section punya padding-bottom:40px tapi tidak ada max-width
     constraint → kartu carousel lebar dengan space kosong di bawah
  2. Black Domain section pakai .layout (grid 208px + 1fr) →
     di layar lebar konten terlalu sempit dibanding lebar viewport

Fix:
  1. Bungkus roster dalam .layout juga (sidebar kosong, konten penuh)
     ATAU lebih sederhana: batasi lebar roster dengan max-width dan center
  2. Ganti .layout dengan .wrap (max-width:1180px, padding normal)
     untuk Black Domain section, TOC jadi horizontal di atas
  3. Kurangi padding-bottom roster
"""

from pathlib import Path

PATH = Path("index.html")


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    changed = False

    # 1. Roster: batasi lebar dan kurangi padding bawah
    old_roster_wrap = '<div class="wrap" style="padding-bottom:40px">'
    new_roster_wrap = '<div class="wrap" style="padding-bottom:20px;padding-top:0">'
    if old_roster_wrap in text:
        text = text.replace(old_roster_wrap, new_roster_wrap, 1)
        changed = True
        print("OK  roster padding dikurangi")

    # 2. Black Domain: ganti .layout (grid 2-kolom) → .wrap (single column)
    #    TOC dipindah dari sidebar ke horizontal di atas konten
    old_bd_start = """<!-- ══════════ THE BLACK DOMAIN ══════════ -->
<div class="layout">
  <aside class="side">
    <h2>Contents</h2>
    <nav class="toc"><ol>"""

    new_bd_start = """<!-- ══════════ THE BLACK DOMAIN ══════════ -->
<div class="wrap" style="padding-top:20px">
  <nav class="toc" style="margin:0 0 28px;display:block"><ol style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:4px">"""

    if old_bd_start in text:
        text = text.replace(old_bd_start, new_bd_start, 1)
        changed = True
        print("OK  Black Domain: .layout → .wrap, TOC jadi grid horizontal")

    # 3. Tutup aside yang sekarang hilang, dan ganti struktur penutup
    old_toc_end = """    </ol></nav>
  </aside>
  <main>"""

    new_toc_end = """    </ol></nav>
  <main style="padding-top:0">"""

    if old_toc_end in text:
        text = text.replace(old_toc_end, new_toc_end, 1)
        changed = True
        print("OK  aside ditutup, main langsung di bawah TOC")

    # 4. Ganti penutup </main></div> di akhir (sebelum <script>)
    #    Struktur lama: </main>\n</div>\n\n<script>
    #    Struktur baru: sama (wrap tidak punya aside lagi)
    #    Tapi kalau ada </main> yang sebelumnya dipasangkan dengan </div></div>
    #    dari .layout, pastikan tertutup benar
    #    Sebenarnya cukup pastikan ada </main> dan </div> sebelum <script>

    if changed:
        PATH.write_text(text, encoding="utf-8")
        print(f"index.html ditulis: {len(text)} bytes")
    else:
        print("Tidak ada perubahan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
