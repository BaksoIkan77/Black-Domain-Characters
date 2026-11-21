/* ═══════════════════════════════════════════════════════════
   Codex of Ruinea — shared behaviour
   Dipakai oleh semua halaman karakter.
   Berisi: image loader, avatar sidebar, form tabs.
   (router URL ada di commander.html)
   ═══════════════════════════════════════════════════════════ */

/* ═══ AUTO IMAGE LOADER ═══ */
(function () {
  const EXT = ['webp', 'png', 'jpg', 'jpeg'];

  document.querySelectorAll('.ph[data-img]').forEach(ph => {
    if (ph.dataset.label) {
      const s = document.createElement('span');
      s.innerHTML = ph.dataset.label;
      ph.appendChild(s);
    }

    const base = 'assets/' + ph.dataset.img;
    const alts = [];
    for (const e of EXT) alts.push(base + '.' + e);
    // fallback: kalau -grid tidak ada, coba -roster
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
    img.onload = () => ph.classList.add('has-img');
    img.onerror = () => {
      i++;
      if (i < alts.length) img.src = alts[i];
      else img.remove();
    };
    img.src = alts[0];

    ph.prepend(img);
    img.loading = 'lazy';
  });

  /* ═══ avatar strip sidebar ═══ */
  document.querySelectorAll('.roster .av').forEach(av => {
    const link = av.closest('a');
    const href = link && (link.getAttribute('href') || '');
    const m = href.match(/^([a-z0-9'-]+)\.html$/i);
    if (!m) return;

    const base = 'assets/' + m[1].toLowerCase() + '-roster';
    const im = new Image();
    let i = 0;
    im.onerror = () => {
      i++;
      if (i < EXT.length) im.src = base + '.' + EXT[i];
      else im.remove();
    };
    im.onload = () => { av.appendChild(im); };
    im.src = base + '.' + EXT[0];
  });
})();

/* ═══ FORM TABS ═══ */
document.addEventListener('click', e => {
  const tab = e.target.closest('.forms__tab');
  if (!tab) return;
  const box = tab.closest('[data-forms]');
  const tabs = [...box.querySelectorAll('.forms__tab')];
  const idx = tabs.indexOf(tab);
  tabs.forEach((t, i) => t.classList.toggle('is-active', i === idx));
  box.querySelectorAll('.forms__panels > .panel')
     .forEach((p, i) => p.classList.toggle('is-active', i === idx));
});
