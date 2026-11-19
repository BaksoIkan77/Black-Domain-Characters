#!/usr/bin/env python3
"""
Tingkatkan responsiveness desktop untuk index.html dan commander.html:
1. Max-width container (--maxw) dibuat fluid & lebih lebar di layar desktop (1440px - 1600px)
2. Tipografi fluid (clamp + vw): judul, p.lead, dan body text membesar otomatis mengikuti resolusi layar
3. Kartu carousel commander di desktop diperbesar (200px -> 250px/270px) agar mengisi layar lebih proporsional
4. Sidebar & layout gap diperlebar di layar besar agar tidak terlihat sempit/kosong di pinggir
"""

import re
from pathlib import Path

FLUID_CSS = """
/* ═══ FLUID DESKTOP RESPONSIVENESS ═══ */
:root{
  --maxw:min(1420px, 92vw);
}
@media (min-width: 1440px){
  :root{
    --maxw:min(1600px, 94vw);
  }
}

body{
  font-size:clamp(16px, 0.4vw + 14.5px, 18px);
}

.hero__in--wide{
  max-width:min(1100px, 95%);
}
.hero__tag{
  max-width:min(80ch, 100%);
  font-size:clamp(16.5px, 0.35vw + 15px, 19.5px);
}

.sec h2{
  font-size:clamp(26px, 1.4vw + 18px, 38px);
}
.sec p.lead{
  font-size:clamp(18.5px, 0.35vw + 17px, 21.5px);
}

@media (min-width: 1100px){
  .cmd-scroll .cmd{flex:0 0 245px}
  .layout{grid-template-columns:230px minmax(0,1fr);gap:60px}
}
@media (min-width: 1500px){
  .cmd-scroll .cmd{flex:0 0 270px}
  .layout{grid-template-columns:260px minmax(0,1fr);gap:72px}
}
"""

def patch_file(filepath: Path):
    if not filepath.exists():
        print(f"!! {filepath} tidak ditemukan")
        return
    text = filepath.read_text(encoding="utf-8")
    if "FLUID DESKTOP RESPONSIVENESS" in text:
        print(f"OK  {filepath}: CSS fluid sudah ada")
        return

    # Sisipkan sebelum </style>
    if "</style>" in text:
        text = text.replace("</style>", FLUID_CSS + "\n</style>", 1)
        filepath.write_text(text, encoding="utf-8")
        print(f"OK  {filepath}: CSS fluid desktop ditambahkan")
    else:
        print(f"!! {filepath}: </style> tidak ditemukan")

def main() -> int:
    patch_file(Path("index.html"))
    patch_file(Path("commander.html"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
