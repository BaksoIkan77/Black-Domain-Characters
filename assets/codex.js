/* ═══════════════════════════════════════════════════════════
   Codex of Ruinea — shared behaviour
   Dipakai oleh semua halaman karakter.
   Berisi: image loader, avatar sidebar, form tabs.
   (router URL ada di commander.html)
   ═══════════════════════════════════════════════════════════ */

/* ═══ ALIAS NAMA FILE ═══
   Sebagian ilustrasi ter-upload dengan nama yang salah ketik
   (mis. "shilpira-" untuk Silphira). Loader mencoba nama yang
   benar lebih dulu, lalu varian alias ini. Jadi file boleh
   di-rename kapan saja tanpa mengubah HTML. */
const NAME_ALIASES = {
  silphira: 'shilpira'   // nama benar: varian typo yang ada di assets/
};

const EXT = ['webp', 'png', 'jpg', 'jpeg'];

/* semua varian basename untuk satu nama aset */
function baseVariants(name) {
  const out = [name];
  for (const [correct, alias] of Object.entries(NAME_ALIASES)) {
    if (name.includes(correct)) out.push(name.split(correct).join(alias));
  }
  return out;
}

/* daftar URL kandidat, berurutan; opsional fallback -grid → -roster */
function imageCandidates(name, gridFallback) {
  const names = baseVariants(name);
  if (gridFallback && /-grid$/.test(name)) {
    names.push(...baseVariants(name.replace(/-grid$/, '-roster')));
  }
  const urls = [];
  for (const n of names) {
    for (const e of EXT) urls.push('assets/' + n + '.' + e);
  }
  return urls;
}

/* ═══ AUTO IMAGE LOADER ═══ */
(function () {
  document.querySelectorAll('.ph[data-img]').forEach(ph => {
    if (ph.dataset.label) {
      const s = document.createElement('span');
      s.innerHTML = ph.dataset.label;
      ph.appendChild(s);
    }

    const urls = imageCandidates(ph.dataset.img, true);

    const img = new Image();
    img.alt = ph.dataset.alt || '';
    img.decoding = 'async';
    img.style.objectFit = ph.dataset.fit || 'cover';
    img.style.objectPosition = ph.dataset.pos || 'center';

    let i = 0;
    img.onload = () => ph.classList.add('has-img');
    img.onerror = () => {
      i++;
      if (i < urls.length) img.src = urls[i];
      else img.remove();
    };
    img.src = urls[0];

    ph.prepend(img);
    img.loading = 'lazy';
  });

  /* ═══ avatar strip sidebar ═══ */
  document.querySelectorAll('.roster .av').forEach(av => {
    const link = av.closest('a');
    const href = link && (link.getAttribute('href') || '');
    const m = href.match(/^([a-z0-9'-]+)\.html$/i);
    if (!m) return;

    const urls = imageCandidates(m[1].toLowerCase() + '-roster', false);
    const im = new Image();
    let i = 0;
    im.onerror = () => {
      i++;
      if (i < urls.length) im.src = urls[i];
      else im.remove();
    };
    im.onload = () => { av.appendChild(im); };
    im.src = urls[0];
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
