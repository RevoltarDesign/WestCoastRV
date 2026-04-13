/* ============================================================
   West Coast RV Camping — Shared Nav
   Single source of truth for nav HTML + behaviour.

   Pages control nav via <body> data attributes:

     data-nav-transparent          – nav starts clear, solidifies on scroll
                                     (campground detail pages only)
     data-nav-cta-text="…"        – button label  (default: "Browse all 110 →")
     data-nav-cta-url="…"         – button href   (default: "/campgrounds")
     data-nav-cta-external        – adds target="_blank" to the CTA

   Active link is set automatically from window.location.pathname.
   ============================================================ */

(function () {

  /* ── Config from body attributes ─────────────────────────── */
  const body         = document.body;
  const transparent  = body.hasAttribute('data-nav-transparent');
  const ctaText      = body.dataset.navCtaText || 'Browse all 110 →';
  const ctaUrl       = body.dataset.navCtaUrl  || '/campgrounds';
  const ctaExternal  = body.hasAttribute('data-nav-cta-external');

  /* ── Asset path (pages in /campground/ are one level deeper) */
  const inSubdir     = window.location.pathname.includes('/campground/');
  const assetRoot    = inSubdir ? '../assets/' : 'assets/';

  /* ── Active link detection ────────────────────────────────── */
  const p = window.location.pathname;
  function active(key) {
    return p.includes(key) ? ' class="active"' : '';
  }

  /* ── Build nav HTML ───────────────────────────────────────── */
  const nav = document.createElement('nav');
  nav.id        = 'site-nav';
  nav.className = 'nav' + (transparent ? '' : ' scrolled');
  nav.innerHTML = `
    <a href="/" class="nav-logo">
      <img src="${assetRoot}west-coast-rv-logo-mark.png"
           alt="West Coast RV Camping"
           class="nav-logo-img"
           height="44">
    </a>
    <div class="nav-right">
      <ul class="nav-links">
        <li><a href="/campgrounds"${active('campground')}>Campgrounds</a></li>
        <li><a href="/field-notes"${active('field-note')}>Field Notes</a></li>
        <li><a href="/about"${active('about')}>About</a></li>
      </ul>
      <a href="${ctaUrl}"
         class="nav-btn"
         ${ctaExternal ? 'target="_blank" rel="noopener"' : ''}>
        ${ctaText}
      </a>
    </div>`;

  /* ── Inject before any other body content ─────────────────── */
  document.body.insertAdjacentElement('afterbegin', nav);

  /* ── Scroll → solid behaviour (transparent navs only) ─────── */
  if (transparent) {
    function onScroll() {
      nav.classList.toggle('scrolled', window.scrollY > 40);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); // run once on load
  }

})();
