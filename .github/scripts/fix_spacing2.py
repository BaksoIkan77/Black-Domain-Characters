#!/usr/bin/env python3
"""
Fix: terlalu banyak empty space di landing page desktop.

Penyebab: Black Domain section pakai .layout (grid 208px + content)
→ konten terbatas di kolom sempit, space kosong di sisi.

Fix: ganti .layout → .wrap (full width max 1180px)
TOC dari sidebar → grid horizontal di atas konten.
"""

from pathlib import Path

PATH = Path("index.html")


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    changed = False

    # 1. Ganti pembuka Black Domain: .layout + aside → .wrap + TOC horizontal
    old_open = """<!-- ══════════ THE BLACK DOMAIN ══════════ -->
<div class="layout">
  <aside class="side">
    <h2>Contents</h2>
    <nav class="toc"><ol>"""

    new_open = """<!-- ══════════ THE BLACK DOMAIN ══════════ -->
<div class="wrap" style="padding-top:20px">
  <nav class="toc" style="margin:0 0 32px"><ol style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:4px">"""

    if old_open in text:
        text = text.replace(old_open, new_open, 1)
        changed = True
        print("OK  .layout → .wrap, TOC jadi grid horizontal")

    # 2. Ganti penutup aside + pembuka main
    old_mid = """    </ol></nav>
  </aside>
  <main>"""

    new_mid = """    </ol></nav>
  <div>"""

    if old_mid in text:
        text = text.replace(old_mid, new_mid, 1)
        changed = True
        print("OK  </aside><main> → </nav><div>")

    # 3. Ganti penutup </main></div> → </div></div>
    old_close = "  </main>\n</div>\n\n<script>"
    new_close = "  </div>\n</div>\n\n<script>"

    if old_close in text:
        text = text.replace(old_close, new_close, 1)
        changed = True
        print("OK  </main></div> → </div></div>")

    # 4. Kurangi padding roster
    old_pad = '<div class="wrap" style="padding-bottom:40px">'
    new_pad = '<div class="wrap" style="padding-bottom:20px;padding-top:0">'
    if old_pad in text:
        text = text.replace(old_pad, new_pad, 1)
        changed = True
        print("OK  roster padding dikurangi")

    if changed:
        PATH.write_text(text, encoding="utf-8")
        print(f"index.html ditulis: {len(text)} bytes")
    else:
        print("Tidak ada perubahan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
