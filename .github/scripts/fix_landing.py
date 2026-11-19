#!/usr/bin/env python3
"""
Fix index.html:
1. Hapus duplikasi nested view-roster (3x → 1x)
2. Hapus CSS carousel duplikat
3. Restrukturisasi Black Domain section:
   - Title "The Black Domain" pakai h1.sm (setara "The Commanders")
   - Layout sidebar (.layout) seperti commander detail: TOC di sisi kiri desktop
   - Banner 16:9 setelah header
   - Gap dipangkas
4. Fix image loader: hapus avatar strip code (tidak ada .roster di landing)

Script ini membaca index.html, ekstrak bagian penting, tulis ulang bersih.
"""

import re
from pathlib import Path

PATH = Path("index.html")


def main() -> int:
    text = PATH.read_text(encoding="utf-8")

    # ── 1. Ekstrak CSS (bersihkan duplikat carousel) ───────────────────
    css_match = re.search(r"<style>(.*?)</style>", text, re.S)
    css = css_match.group(1) if css_match else ""

    # Hapus duplikat blok carousel CSS
    carousel_block = """/* ═══ CAROUSEL (horizontal scroll) ═══ */
.cmd-scroll{display:flex;gap:15px;overflow-x:auto;scroll-snap-type:x mandatory;
  -webkit-overflow-scrolling:touch;padding:4px 28px 20px;scrollbar-width:thin;
  scrollbar-color:var(--line) transparent}
.cmd-scroll::-webkit-scrollbar{height:6px}
.cmd-scroll::-webkit-scrollbar-track{background:transparent}
.cmd-scroll::-webkit-scrollbar-thumb{background:var(--line);border-radius:99px}
.cmd-scroll .cmd{flex:0 0 200px;scroll-snap-align:start}
@media (max-width:900px){.cmd-scroll .cmd{flex:0 0 160px}
  .cmd-scroll{padding:4px 20px 16px}}"""

    # Hitung berapa kali carousel muncul
    css = css.replace(carousel_block, "", css.count(carousel_block) - 1)
    # Pastikan minimal 1 copy
    if carousel_block not in css:
        css += "\n" + carousel_block

    # ── 2. Ekstrak topbar ──────────────────────────────────────────────
    topbar_match = re.search(r'(<div class="topbar">.*?</div>\s*</div>)', text, re.S)
    topbar = topbar_match.group(1) if topbar_match else ""

    # ── 3. Ekstrak commander cards dari cmd-scroll ─────────────────────
    # Cari blok cmd-scroll lengkap
    scroll_match = re.search(
        r'(<div class="cmd-scroll">.*?</div>)', text, re.S
    )
    cmd_scroll = scroll_match.group(1) if scroll_match else ""

    # ── 4. Ekstrak semua lore sections (bd-overview s/d bd-borders) ────
    # Cari dari <section class="sec" id="bd-overview" sampai section terakhir sebelum </div>\n</div>\n<script>
    lore_start = text.find('<section class="sec" id="bd-overview"')
    lore_end = text.find('</div>\n\n<script>', lore_start)
    if lore_start == -1:
        # Coba pola alternatif
        lore_start = text.find('<section class="sec" id="bd-overview"')
        # Cari script tag
        script_pos = text.find('<script>', lore_start)
        # Mundur untuk menemukan akhir blok lore
        lore_end = text.rfind('</section>', lore_start, script_pos)
        if lore_end != -1:
            lore_end += len('</section>')

    lore = text[lore_start:lore_end].strip() if lore_start != -1 and lore_end != -1 else ""

    # ── 5. Ekstrak image loader JS (tanpa avatar strip) ────────────────
    img_loader = """/* ═══ AUTO IMAGE LOADER ═══ */
(function(){
  const EXT = ['webp','png','jpg','jpeg'];
  document.querySelectorAll('.ph[data-img]').forEach(ph => {
    if (ph.dataset.label) {
      const s = document.createElement('span');
      s.innerHTML = ph.dataset.label;
      ph.appendChild(s);
    }
    const base = 'assets/' + ph.dataset.img;
    const img = new Image();
    img.alt = ph.dataset.alt || '';
    img.decoding = 'async';
    img.style.objectFit = ph.dataset.fit || 'cover';
    img.style.objectPosition = ph.dataset.pos || 'center';
    let i = 0;
    img.onload = () => { ph.classList.add('has-img'); };
    img.onerror = () => {
      i++;
      if (i < EXT.length) img.src = base + '.' + EXT[i];
      else img.remove();
    };
    img.src = base + '.' + EXT[0];
    ph.prepend(img);
    img.loading = 'lazy';
  });
})();"""

    # ── 6. Build TOC untuk sidebar ─────────────────────────────────────
    toc = """<nav class="toc"><ol>
      <li><a href="#bd-overview"><i>01</i>Overview &amp; Culture</a></li>
      <li><a href="#bd-history"><i>02</i>History</a></li>
      <li><a href="#bd-geography"><i>03</i>Geography</a></li>
      <li><a href="#bd-population"><i>04</i>Population &amp; Hazards</a></li>
      <li><a href="#bd-government"><i>05</i>Government &amp; Politics</a></li>
      <li><a href="#bd-military"><i>06</i>Military &amp; Defense</a></li>
      <li><a href="#bd-technology"><i>07</i>Technology &amp; Transport</a></li>
      <li><a href="#bd-economy"><i>08</i>Economy &amp; Satellites</a></li>
      <li><a href="#bd-locations"><i>09</i>Key Locations</a></li>
      <li><a href="#bd-settlement"><i>10</i>Settlement Pattern</a></li>
      <li><a href="#bd-borders"><i>11</i>Borders</a></li>
    </ol></nav>"""

    # ── 7. Build index.html bersih ─────────────────────────────────────
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0a0708">
<title>Codex of Ruinea — The Black Domain</title>
<style>
{css}
</style>
</head>
<body>

{topbar}

<!-- ══════════ ROSTER ══════════ -->
<div class="view" id="view-roster">
  <header class="hero">
    <div class="hero__in hero__in--wide">
      <div>
        <p class="eyebrow">The Black Domain · Malakh-Kar</p>
        <h1 class="sm">The Commanders</h1>
        <p class="hero__tag">
          One sovereign, eight commanders, and a hierarchy arranged as a weapon. The radicals
          hold the frontier and receive honour, danger, and the dying. The loyalists hold the
          interior and receive food, roads, and the supply belt. Every one of them can see
          exactly what that arrangement means.
        </p>
      </div>
    </div>
  </header>
  <div class="wrap" style="padding-bottom:40px">
    {cmd_scroll}
  </div>
</div>

<!-- ══════════ THE BLACK DOMAIN ══════════ -->
<div class="layout">
  <aside class="side">
    <h2>Contents</h2>
    {toc}
  </aside>
  <main>
    <section class="sec" id="bd-intro" style="padding-top:0">
      <div class="sec__head">
        <span class="sec__kick">Codex of Ruinea</span>
        <h1 class="sm" style="font:400 clamp(30px,5.4vw,56px)/.96 var(--serif);letter-spacing:-.02em;color:#f4ecea;margin:0">The Black Domain</h1>
      </div>
      <div class="ph ph--wide" style="margin-bottom:28px" data-img="blackdomain-hero" data-fit="cover" data-label="The western wasteland · 16:9"></div>
    </section>

    {lore}
  </main>
</div>

<script>
{img_loader}
</script>
</body>
</html>"""

    PATH.write_text(html, encoding="utf-8")
    print(f"index.html ditulis: {len(html)} bytes")
    print(f"  cmd-scroll: {'OK' if 'cmd-scroll' in html else 'MISSING'}")
    print(f"  bd-overview: {'OK' if 'bd-overview' in html else 'MISSING'}")
    print(f"  bd-borders: {'OK' if 'bd-borders' in html else 'MISSING'}")
    print(f"  layout: {'OK' if 'class=\"layout\"' in html else 'MISSING'}")
    print(f"  h1.sm: {'OK' if 'h1 class=\"sm\"' in html else 'MISSING'}")
    print(f"  carousel duplikat: {html.count('cmd-scroll{display:flex')} (harusnya 1)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
