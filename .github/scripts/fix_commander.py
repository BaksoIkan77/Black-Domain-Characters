#!/usr/bin/env python3
"""
Fix: commander.html kehilangan view detail karena regex restructure_index.py
gagal match (case mismatch: komentar "AZALEA" vs id "view-azalea").

Script ini:
1. Ambil index.html asli dari git history (sebelum restructure)
2. Extract semua view-XXX blocks + CSS + JS
3. Tulis commander.html yang lengkap
4. Perbaiki topbar: data-view="roster" → href="index.html"

Idempoten: kalau commander.html sudah punya view-azalea, dilewati.
"""

import re
import subprocess
from pathlib import Path

CMD_PATH = Path("commander.html")


def main() -> int:
    # Cek apakah commander.html sudah punya view detail
    if CMD_PATH.exists():
        cmd_text = CMD_PATH.read_text(encoding="utf-8")
        if 'id="view-azalea"' in cmd_text:
            print("OK  commander.html sudah punya view detail, skip")
            return 0

    # 1. Ambil index.html asli dari git history
    # Cari commit sebelum restructure (punya view-azalea di index.html)
    result = subprocess.run(
        ["git", "log", "--all", "--oneline", "--", "index.html"],
        capture_output=True, text=True, check=True,
    )
    lines = result.stdout.strip().split("\n")
    # Ambil commit yang bukan hasil restructure
    original_sha = None
    for line in lines:
        sha = line.split()[0]
        r = subprocess.run(
            ["git", "show", f"{sha}:index.html"],
            capture_output=True, text=True,
        )
        if r.returncode == 0 and 'id="view-azalea"' in r.stdout and 'id="view-nuva"' in r.stdout:
            original_sha = sha
            break

    if not original_sha:
        print("!!  tidak bisa menemukan index.html asli di git history")
        return 1

    print(f"OK  index.html asli ditemukan di commit {original_sha}")
    text = subprocess.run(
        ["git", "show", f"{original_sha}:index.html"],
        capture_output=True, text=True, check=True,
    ).stdout

    # 2. Extract CSS
    css_match = re.search(r"<style>(.*?)</style>", text, re.S)
    css_body = css_match.group(1) if css_match else ""

    # 3. Extract detail views: ambil semua dari <!-- AZALEA sampai <script>
    # Cari marker pertama (AZALEA) dan terakhir (NUVA)
    azalea_pos = text.find('<!-- ═')
    # Cari yang mengandung AZALEA
    while azalea_pos != -1:
        if "AZALEA" in text[azalea_pos:azalea_pos+100]:
            break
        azalea_pos = text.find('<!-- ═', azalea_pos + 1)

    script_pos = text.find('<script>')

    if azalea_pos == -1 or script_pos == -1:
        print("!!  tidak bisa menemukan blok view detail")
        return 1

    detail_html = text[azalea_pos:script_pos].strip()

    # 4. Extract topbar
    topbar_match = re.search(r'(<div class="topbar">.*?</div>\s*</div>)', text, re.S)
    topbar = topbar_match.group(1) if topbar_match else ""

    # Perbaiki topbar: data-view="roster" → href="index.html"
    topbar = topbar.replace('data-view="roster"', 'href="index.html"')

    # 5. Extract JS blocks
    js_match = re.search(r"<script>(.*?)</script>", text, re.S)
    js_body = js_match.group(1) if js_match else ""

    # Extract sub-blocks
    img_loader = re.search(r'/\* ═══ AUTO IMAGE LOADER.*?(?=/\* ═══ FORM)', js_body, re.S)
    img_loader = img_loader.group(0) if img_loader else ""

    forms_js = re.search(r'/\* ═══ FORM TABS.*?(?=/\* ═══ ROUTER)', js_body, re.S)
    forms_js = forms_js.group(0) if forms_js else ""

    # Router JS baru (URL hash based)
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

// Init from hash
const initialId = window.location.hash.slice(1) || 'azalea';
go(initialId);"""

    # 6. Perbaiki pager & cross-links di detail views
    detail_html = detail_html.replace('data-view="roster"', 'href="index.html"')
    detail_html = re.sub(
        r'data-view="(azalea|vorlag|kazagar|gorath|alleen|zargoth|vexia|silphira|nuva)"',
        r'href="commander.html#\1"',
        detail_html,
    )

    # 7. Tulis commander.html
    commander = f"""<!doctype html>
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

{detail_html}

<script>
{img_loader}

{forms_js}

{router_js}
</script>
</body>
</html>"""

    CMD_PATH.write_text(commander, encoding="utf-8")
    print(f"commander.html ditulis: {len(commander)} bytes")
    print(f"  view-azalea: {'ada' if 'id=\"view-azalea\"' in commander else 'TIDAK ADA'}")
    print(f"  view-nuva:   {'ada' if 'id=\"view-nuva\"' in commander else 'TIDAK ADA'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
