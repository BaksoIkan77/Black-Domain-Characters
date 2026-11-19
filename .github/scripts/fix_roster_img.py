#!/usr/bin/env python3
"""
Fix gambar roster tidak terload:
1. CSS: .cmd-scroll .cmd .ph tidak dapat tinggi (selector lama menarget .grid)
   → tambah aturan aspect-ratio untuk .cmd-scroll
2. Loader: kalau *-grid tidak ada, coba *-roster sebagai fallback basename
"""

from pathlib import Path

PATH = Path("index.html")

CSS_ADD = """
/* ═══ CAROUSEL FIX: tinggi placeholder ═══ */
.cmd-scroll .cmd .ph{aspect-ratio:3/4;width:100%}
.cmd-scroll .cmd--lead .ph{aspect-ratio:3/4}
"""

# Loader baru dengan fallback basename -grid -> -roster
LOADER_OLD_START = "/* ═══ AUTO IMAGE LOADER ═══ */"
LOADER_NEW = """/* ═══ AUTO IMAGE LOADER ═══ */
(function(){
  const EXT = ['webp','png','jpg','jpeg'];
  document.querySelectorAll('.ph[data-img]').forEach(ph => {
    if (ph.dataset.label) {
      const s = document.createElement('span');
      s.innerHTML = ph.dataset.label;
      ph.appendChild(s);
    }
    const base = 'assets/' + ph.dataset.img;
    // daftar kandidat: semua ekstensi untuk basename, lalu fallback -roster
    const alts = [];
    for (const e of EXT) alts.push(base + '.' + e);
    if (/-grid$/.test(ph.dataset.img)) {
      const rb = base.replace(/-grid$/, '-roster');
      for (const e of EXT) alts.push(rb + '.' + e);
    }
    const img = new Image();
    img.alt = ph.dataset.alt || '';
    img.decoding = 'async';
    img.style.objectFit = ph.dataset.fit || 'cover';
    img.style.objectPosition = ph.dataset.pos || 'center';
    let i = 0;
    img.onload = () => { ph.classList.add('has-img'); };
    img.onerror = () => {
      i++;
      if (i < alts.length) img.src = alts[i];
      else img.remove();
    };
    img.src = alts[0];
    ph.prepend(img);
    img.loading = 'lazy';
  });
})();"""


def main() -> int:
    text = PATH.read_text(encoding="utf-8")

    # 1. Tambah CSS fix (idempoten)
    if ".cmd-scroll .cmd .ph{aspect-ratio:3/4" not in text:
        # sisipkan setelah blok carousel
        anchor = ".cmd-scroll{padding:4px 20px 16px}}"
        if anchor in text:
            text = text.replace(anchor, anchor + "\n" + CSS_ADD.strip(), 1)
            print("OK  CSS aspect-ratio untuk .cmd-scroll ditambahkan")
        else:
            # fallback: tambah sebelum </style>
            text = text.replace("</style>", CSS_ADD + "</style>", 1)
            print("OK  CSS ditambahkan (sebelum </style>)")
    else:
        print("OK  CSS sudah ada")

    # 2. Ganti loader (idempoten: cek penanda fallback)
    if "fallback -roster" in text or "-grid$" in text:
        print("OK  loader fallback sudah ada")
    else:
        start = text.find(LOADER_OLD_START)
        if start == -1:
            print("!!  loader tidak ditemukan")
            return 1
        end = text.find("})();", start)
        if end == -1:
            print("!!  akhir loader tidak ditemukan")
            return 1
        end += len("})();")
        text = text[:start] + LOADER_NEW + text[end:]
        print("OK  loader diganti dengan versi fallback -roster")

    PATH.write_text(text, encoding="utf-8")
    print(f"index.html ditulis: {len(text)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
