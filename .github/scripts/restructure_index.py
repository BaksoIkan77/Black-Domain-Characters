#!/usr/bin/env python3
"""
Restructure: split index.html → index.html (landing + lore) + commander.html (detail).

1. Generate lore fragment (panggil generate_lore.py)
2. Baca index.html, pisahkan:
   - Landing (view-roster + CSS + JS dasar) → index.html baru
   - Detail (view-azalea s/d view-nuva + JS routing) → commander.html
3. Landing page:
   - Grid commander jadi horizontal scroll-snap carousel
   - Tambah section "The Black Domain" dengan lore dari fragment
   - TOC untuk lore sections
4. commander.html:
   - CSS lengkap (shared style block)
   - Routing pakai URL hash (#azalea, #vorlag, dll) agar tombol back browser jalan
   - Tombol "back" di pager → href="index.html"
5. Cross-link: kartu commander di landing → href="commander.html#azalea"
"""

import re
import subprocess
from pathlib import Path

SRC = Path("index.html")
LORE_FRAGMENT = Path(".github/scripts/_lore_fragment.html")


def main() -> int:
    # 1. Generate lore fragment
    subprocess.run(["python3", ".github/scripts/generate_lore.py"], check=True)
    lore = LORE_FRAGMENT.read_text(encoding="utf-8")

    # 2. Baca source
    text = SRC.read_text(encoding="utf-8")

    # 3. Extract CSS block (sebelum </head>...<body>)
    css_match = re.search(r"(<style>)(.*?)(</style>)", text, re.S)
    if not css_match:
        print("!! CSS block tidak ditemukan")
        return 1
    css_open, css_body, css_close = css_match.group(1), css_match.group(2), css_match.group(3)

    # 4. Extract views
    roster_match = re.search(r'(<div class="view" id="view-roster">.*?</div>\s*)(?=<!--)', text, re.S)
    if not roster_match:
        print("!! view-roster tidak ditemukan")
        return 1
    roster_html = roster_match.group(1)

    # Extract semua view-XXX blocks
    detail_views = []
    for m in re.finditer(
        r'(<!-- ═+\s*(\w+)\s+═+\s*-->\s*)(<div class="view" id="view-\2"[^>]*>.*?</div>\s*)(?=<!--|$)',
        text, re.S,
    ):
        detail_views.append((m.group(2).lower(), m.group(1), m.group(3)))

    # 5. Extract JS
    js_match = re.search(r"(<script>)(.*?)(</script>)", text, re.S)
    if not js_match:
        print("!! JS block tidak ditemukan")
        return 1
    js_body = js_match.group(2)

    # 6. Extract topbar
    topbar_match = re.search(r'(<div class="topbar">.*?</div>\s*</div>)', text, re.S)
    topbar = topbar_match.group(1) if topbar_match else ""

    # ── BUILD INDEX.HTML (landing) ──────────────────────────────────
    # Grid → horizontal carousel CSS
    carousel_css = """
/* ═══ CAROUSEL (horizontal scroll) ═══ */
.cmd-scroll{display:flex;gap:15px;overflow-x:auto;scroll-snap-type:x mandatory;
  -webkit-overflow-scrolling:touch;padding:4px 28px 20px;scrollbar-width:thin;
  scrollbar-color:var(--line) transparent}
.cmd-scroll::-webkit-scrollbar{height:6px}
.cmd-scroll::-webkit-scrollbar-track{background:transparent}
.cmd-scroll::-webkit-scrollbar-thumb{background:var(--line);border-radius:99px}
.cmd-scroll .cmd{flex:0 0 200px;scroll-snap-align:start}
@media (max-width:900px){.cmd-scroll .cmd{flex:0 0 160px}
  .cmd-scroll{padding:4px 20px 16px}}
"""

    # Lore TOC
    lore_toc = '''<nav class="toc" style="margin:0 0 28px"><ol>
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
    </ol></nav>'''

    # Convert grid → carousel in roster HTML
    roster_html = roster_html.replace(
        '<div class="grid">',
        '<div class="cmd-scroll">',
    )

    # Convert commander links → commander.html#XXX
    roster_html = re.sub(
        r'data-view="(azalea|vorlag|kazagar|gorath|alleen|zargoth|vexia|silphira|nuva)"',
        r'href="commander.html#\1"',
        roster_html,
    )

    # Build landing page
    index_new = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0a0708">
<title>Codex of Ruinea — The Black Domain</title>
<style>
{css_body}
{carousel_css}
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
  <div class="wrap">
    {roster_html}
  </div>
</div>

<!-- ══════════ THE BLACK DOMAIN ══════════ -->
<div class="wrap" style="padding-top:0">
  {lore_toc}
  {lore}
</div>

<script>
/* ═══ AUTO IMAGE LOADER ═══ */
(function(){{
  const EXT = ['webp','png','jpg','jpeg'];
  document.querySelectorAll('.ph[data-img]').forEach(ph => {{
    if (ph.dataset.label) {{
      const s = document.createElement('span');
      s.innerHTML = ph.dataset.label;
      ph.appendChild(s);
    }}
    const base = 'assets/' + ph.dataset.img;
    const img = new Image();
    img.alt = ph.dataset.alt || '';
    img.decoding = 'async';
    img.style.objectFit = ph.dataset.fit || 'cover';
    img.style.objectPosition = ph.dataset.pos || 'center';
    let i = 0;
    img.onload = () => {{ ph.classList.add('has-img'); }};
    img.onerror = () => {{
      i++;
      if (i < EXT.length) img.src = base + '.' + EXT[i];
      else img.remove();
    }};
    img.src = base + '.' + EXT[0];
    ph.prepend(img);
    img.loading = 'lazy';
  }});
}})();
</script>
</body>
</html>"""

    # ── BUILD COMMANDER.HTML (detail) ───────────────────────────────
    detail_blocks = "\n".join(
        f"{comment}\n{view_html}" for _, comment, view_html in detail_views
    )

    # Rewrite pager links → index.html
    detail_blocks = detail_blocks.replace('data-view="roster"', 'href="index.html"')

    # Rewrite cross-commander links → commander.html#XXX
    detail_blocks = re.sub(
        r'data-view="(azalea|vorlag|kazagar|gorath|alleen|zargoth|vexia|silphira|nuva)"',
        r'href="commander.html#\1"',
        detail_blocks,
    )

    # Router JS: URL hash based
    router_js = """
/* ═══ ROUTER (URL hash) ═══ */
const TITLES = {roster:'Commanders',azalea:'Azalea',vorlag:'Vorlag',kazagar:'Kazagar',
  gorath:'Gorath',alleen:'Alleen',zargoth:"Zar'goth",vexia:'Vexia',silphira:'Silphira',nuva:'Nuva'};

function go(id){
  const target = document.getElementById('view-' + id) || document.getElementById('view-roster');
  if (!target) return;
  document.querySelectorAll('.view').forEach(v => { v.hidden = (v !== target); });
  document.getElementById('crumb').textContent = TITLES[id] || 'Commanders';
  window.scrollTo(0, 0);
  document.querySelectorAll('.roster a').forEach(a => {
    const href = a.getAttribute('href') || '';
    const match = href.match(/#(\\w+)$/);
    const viewId = match ? match[1] : null;
    if (viewId === id) a.setAttribute('aria-current','page');
    else a.removeAttribute('aria-current');
  });
}

window.addEventListener('hashchange', () => {
  const id = window.location.hash.slice(1) || 'azalea';
  go(id);
});

document.addEventListener('click', e => {
  const el = e.target.closest('[href^="#"]');
  if (!el) return;
  const id = el.getAttribute('href').slice(1);
  if (!id || !document.getElementById('view-' + id)) return;
  // let hashchange handle it
});

// Init from hash
const initialId = window.location.hash.slice(1) || 'azalea';
go(initialId);
"""

    # Keep form-tabs JS and image loader JS from original
    forms_js = re.search(r'/\* ═══ FORM TABS ═══ \*/.*?(?=/\* ═══ ROUTER)', js_body, re.S)
    forms_js = forms_js.group(0) if forms_js else ""

    img_loader_js = re.search(r'/\* ═══ AUTO IMAGE LOADER ═══ \*/.*?(?=/\* ═══ FORM TABS)', js_body, re.S)
    img_loader_js = img_loader_js.group(0) if img_loader_js else ""

    commander_new = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0a0708">
<title>Commander — Codex of Ruinea</title>
<style>
{css_body}
</style>
</head>
<body>

{topbar}

{detail_blocks}

<script>
{img_loader_js}

{forms_js}

{router_js}
</script>
</body>
</html>"""

    # Write files
    SRC.write_text(index_new, encoding="utf-8")
    Path("commander.html").write_text(commander_new, encoding="utf-8")
    print(f"index.html    ditulis: {len(index_new)} bytes")
    print(f"commander.html ditulis: {len(commander_new)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
