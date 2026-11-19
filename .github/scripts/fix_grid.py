#!/usr/bin/env python3
"""
Fix dua bug di index.html:
1. cmd-scroll terpotong (hanya Azalea, 8 kartu hilang) → ganti dengan 9 kartu lengkap
2. Banner blackdomain-hero duplikat di bd-overview → hapus yang di bd-overview
"""

from pathlib import Path

PATH = Path("index.html")

# 9 kartu commander lengkap untuk cmd-scroll
CMD_SCROLL = """<div class="cmd-scroll">
      <a class="cmd cmd--lead" href="commander.html#azalea"><div class="ph" data-img="azalea-grid" data-fit="cover" data-alt="Azalea"></div>
        <div class="cmd__body"><div class="cmd__name">Azalea</div><div class="cmd__title">The Unraveler</div>
        <div class="cmd__meta"><span>Malakh-Kar</span><b>8.9</b></div></div></a>

      <a class="cmd" href="commander.html#vorlag"><div class="ph" data-img="vorlag-grid" data-fit="cover" data-alt="Vorlag"></div>
        <div class="cmd__body"><div class="cmd__name">Vorlag</div><div class="cmd__title">The Night King</div>
        <div class="cmd__meta"><span>Nightreach</span><b>8.7</b></div></div></a>

      <a class="cmd" href="commander.html#kazagar"><div class="ph" data-img="kazagar-grid" data-fit="cover" data-alt="Kazagar"></div>
        <div class="cmd__body"><div class="cmd__name">Kazagar</div><div class="cmd__title">The Molten Heart</div>
        <div class="cmd__meta"><span>Emberhold</span><b>8.7</b></div></div></a>

      <a class="cmd" href="commander.html#gorath"><div class="ph" data-img="gorath-grid" data-fit="cover" data-alt="Gorath"></div>
        <div class="cmd__body"><div class="cmd__name">Gorath</div><div class="cmd__title">The Unstoppable</div>
        <div class="cmd__meta"><span>Stonefall</span><b>8.7</b></div></div></a>

      <a class="cmd" href="commander.html#alleen"><div class="ph" data-img="alleen-grid" data-fit="cover" data-alt="Alleen"></div>
        <div class="cmd__body"><div class="cmd__name">Alleen</div><div class="cmd__title">The Serene</div>
        <div class="cmd__meta"><span>Verathiel</span><b>8.6</b></div></div></a>

      <a class="cmd" href="commander.html#zargoth"><div class="ph" data-img="zargoth-grid" data-fit="cover" data-alt="Zar'goth"></div>
        <div class="cmd__body"><div class="cmd__name">Zar'goth</div><div class="cmd__title">The Sky-Scorcher</div>
        <div class="cmd__meta"><span>The Aeries</span><b>8.0</b></div></div></a>

      <a class="cmd" href="commander.html#vexia"><div class="ph" data-img="vexia-grid" data-fit="cover" data-alt="Vexia"></div>
        <div class="cmd__body"><div class="cmd__name">Vexia</div><div class="cmd__title">The Quiet Broker</div>
        <div class="cmd__meta"><span>Silkhaven</span><b>7.8</b></div></div></a>

      <a class="cmd" href="commander.html#silphira"><div class="ph" data-img="silphira-grid" data-fit="cover" data-alt="Silphira"></div>
        <div class="cmd__body"><div class="cmd__name">Silphira</div><div class="cmd__title">The Whisper</div>
        <div class="cmd__meta"><span>Vaelthorn</span><b>7.7</b></div></div></a>

      <a class="cmd" href="commander.html#nuva"><div class="ph" data-img="nuva-grid" data-fit="cover" data-alt="Nuva"></div>
        <div class="cmd__body"><div class="cmd__name">Nuva</div><div class="cmd__title">The Shadow That Answers</div>
        <div class="cmd__meta"><span>No Territory</span><b>7.6</b></div></div></a>
    </div>"""

# Banner duplikat yang harus dihapus dari bd-overview
DUP_BANNER = '        <div class="ph ph--wide" style="margin-bottom:28px" data-img="blackdomain-hero" data-fit="cover" data-label="The western wasteland · 16:9"></div>\n'


def main() -> int:
    text = PATH.read_text(encoding="utf-8")

    # 1. Ganti cmd-scroll yang terpotong
    # Pola: dari <div class="cmd-scroll"> sampai </div>\n  </div>\n</div>
    # Cari cmd-scroll yang ada
    old_start = text.find('<div class="cmd-scroll">')
    if old_start == -1:
        print("!!  cmd-scroll tidak ditemukan")
        return 1

    # Cari akhir blok: </div>\n  </div>\n</div> setelah cmd-scroll
    # Pola: </div> (tutup cmd-scroll) lalu </div> (tutup wrap) lalu </div> (tutup view-roster)
    old_end = text.find('</div>\n</div>', old_start)
    if old_end == -1:
        print("!!  akhir blok cmd-scroll tidak ditemukan")
        return 1
    old_end += len('</div>\n</div>')

    old_block = text[old_start:old_end]

    if 'cmd__body' in old_block and 'nuva-grid' in old_block:
        print("OK  cmd-scroll sudah lengkap, skip")
    else:
        text = text[:old_start] + CMD_SCROLL + '\n  </div>\n</div>' + text[old_end:]
        print(f"OK  cmd-scroll diganti ({len(CMD_SCROLL)} bytes)")

    # 2. Hapus banner duplikat dari bd-overview
    # Cari banner di dalam section bd-overview (bukan bd-intro)
    overview_start = text.find('id="bd-overview"')
    if overview_start != -1:
        # Cari banner setelah overview_start
        banner_pos = text.find(DUP_BANNER.strip(), overview_start)
        if banner_pos != -1:
            # Hapus baris ini plus newline
            line_start = text.rfind('\n', 0, banner_pos) + 1
            line_end = text.find('\n', banner_pos) + 1
            text = text[:line_start] + text[line_end:]
            print("OK  banner duplikat di bd-overview dihapus")
        else:
            print("OK  banner duplikat tidak ditemukan di bd-overview (sudah bersih)")
    else:
        print("!!  section bd-overview tidak ditemukan")

    PATH.write_text(text, encoding="utf-8")
    print(f"index.html ditulis: {len(text)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
