#!/usr/bin/env python3
"""
Split: ambil index.html asli dari git history (commit 72fde9f),
pecah jadi index.html (landing + lore) + commander.html (detail).

Script ini menggantikan semua script restructure sebelumnya.
Dijalankan sekali. Idempoten: kalau sudah split dengan benar, skip.
"""

import subprocess
import re
from pathlib import Path

# Commit yang punya index.html lengkap (sebelum restructure)
ORIGINAL_COMMIT = "72fde9f491e9beb7d927e3774da39885644b7d7c"


def main() -> int:
    # 1. Ambil index.html asli dari git history
    result = subprocess.run(
        ["git", "show", f"{ORIGINAL_COMMIT}:index.html"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print("!!  tidak bisa ambil index.html dari git history")
        print(result.stderr)
        return 1

    text = result.stdout
    print(f"OK  index.html asli: {len(text)} bytes dari {ORIGINAL_COMMIT[:7]}")

    # Verifikasi: punya view detail?
    if 'id="view-azalea"' not in text:
        print("!!  index.html asli tidak punya view-azalea")
        return 1

    # 2. Extract CSS block
    css_match = re.search(r"<style>(.*?)</style>", text, re.S)
    css_body = css_match.group(1) if css_match else ""

    # 3. Extract topbar
    topbar_match = re.search(r'(<div class="topbar">.*?</div>\s*</div>)', text, re.S)
    topbar = topbar_match.group(1) if topbar_match else ""

    # 4. Extract roster section
    # Cari dari <div class="view" id="view-roster"> sampai sebelum <!-- AZALEA
    roster_start = text.find('<div class="view" id="view-roster">')
    roster_end = text.find('<!-- ═', roster_start)
    if roster_start == -1 or roster_end == -1:
        print("!!  tidak bisa menemukan batas roster")
        return 1
    roster_html = text[roster_start:roster_end].strip()

    # 5. Extract detail views: dari <!-- AZALEA sampai <script>
    detail_start = text.find('<!-- ═', roster_end)
    detail_end = text.find('<script>')
    if detail_start == -1 or detail_end == -1:
        print("!!  tidak bisa menemukan blok view detail")
        return 1
    detail_html = text[detail_start:detail_end].strip()

    # 6. Extract JS blocks
    js_match = re.search(r"<script>(.*?)</script>", text, re.S)
    js_body = js_match.group(1) if js_match else ""

    img_loader = re.search(r'/\* ═══ AUTO IMAGE LOADER.*?(?=/\* ═══ FORM)', js_body, re.S)
    img_loader = img_loader.group(0) if img_loader else ""

    forms_js = re.search(r'/\* ═══ FORM TABS.*?(?=/\* ═══ ROUTER)', js_body, re.S)
    forms_js = forms_js.group(0) if forms_js else ""

    # 7. Convert roster: grid → carousel, links → commander.html#XXX
    roster_landing = roster_html.replace('<div class="grid">', '<div class="cmd-scroll">')
    roster_landing = re.sub(
        r'data-view="(azalea|vorlag|kazagar|gorath|alleen|zargoth|vexia|silphira|nuva)"',
        r'href="commander.html#\1"',
        roster_landing,
    )

    # 8. Fix detail: links → commander.html#XXX, roster → index.html
    detail_fixed = detail_html.replace('data-view="roster"', 'href="index.html"')
    detail_fixed = re.sub(
        r'data-view="(azalea|vorlag|kazagar|gorath|alleen|zargoth|vexia|silphira|nuva)"',
        r'href="commander.html#\1"',
        detail_fixed,
    )

    # 9. Fix topbar: roster → index.html
    topbar_landing = topbar.replace('data-view="roster"', 'href="index.html"')
    topbar_detail = topbar.replace('data-view="roster"', 'href="index.html"')

    # 10. Carousel CSS (single copy)
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
  .cmd-scroll{padding:4px 20px 16px}}"""

    # 11. Router JS for commander.html (URL hash based)
    router_js = """/* ═══ ROUTER (URL hash) ═══ */
const TITLES = {roster:'Commanders',azalea:'Azalea',vorlag:'Vorlag',kazagar:'Kazagar',
  gorath:'Gorath',alleen:'Alleen',zargoth:"Zar'goth",vexia:'Vexia',silphira:'Silphira',nuva:'Nuva'};

function go(id){
  const target = document.getElementById('view-' + id);
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

const initialId = window.location.hash.slice(1) || 'azalea';
go(initialId);"""

    # 12. Lore fragment (embedded)
    # Read from the fragment file if it exists, else empty
    lore_path = Path(".github/scripts/_lore_fragment.html")
    if lore_path.exists():
        lore = lore_path.read_text(encoding="utf-8")
    else:
        # Generate inline
        lore = _generate_lore_inline()

    # 13. Lore TOC
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

    # 14. Build index.html (landing)
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

{topbar_landing}

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
    {roster_landing}
  </div>
</div>

<!-- ══════════ THE BLACK DOMAIN ══════════ -->
<div class="wrap" style="padding-top:0">
  {lore_toc}
  {lore}
</div>

<script>
{img_loader}
</script>
</body>
</html>"""

    # 15. Build commander.html (detail)
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

{topbar_detail}

{detail_fixed}

<script>
{img_loader}

{forms_js}

{router_js}
</script>
</body>
</html>"""

    # 16. Write files
    Path("index.html").write_text(index_new, encoding="utf-8")
    Path("commander.html").write_text(commander_new, encoding="utf-8")

    print(f"index.html     ditulis: {len(index_new)} bytes")
    print(f"commander.html ditulis: {len(commander_new)} bytes")
    print(f"  view-azalea: {'OK' if 'id=\"view-azalea\"' in commander_new else 'MISSING'}")
    print(f"  view-nuva:   {'OK' if 'id=\"view-nuva\"' in commander_new else 'MISSING'}")
    print(f"  carousel:    {'OK' if 'cmd-scroll' in index_new else 'MISSING'}")
    print(f"  lore:        {'OK' if 'bd-overview' in index_new else 'MISSING'}")

    return 0


def _generate_lore_inline():
    """Lore fragment generated inline (fallback if file missing)."""
    return Path(".github/scripts/generate_lore.py").read_text(encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
