/* ============================================================
   West Coast RV Camping — Google Analytics 4
   ─────────────────────────────────────────────────────────────
   TODO: Replace GA_ID with your real Measurement ID from:
         analytics.google.com → Admin → Data Streams → your stream

   The snippet will NOT fire while GA_ID is the placeholder value,
   so no junk data accumulates. Just swap in the real ID and push.
   ============================================================ */
(function () {
  if (['localhost', '127.0.0.1'].includes(location.hostname)) return;
  var GA_ID = 'G-9HJLVP3QNJ';
  if (GA_ID === 'G-XXXXXXXXXX') return;
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', GA_ID);
})();

/* ============================================================
   West Coast RV Camping — Shared Nav
   Single source of truth for nav HTML + behaviour.

   Pages control nav via <body> data attributes:

     data-nav-transparent          – nav starts clear, solidifies on scroll
                                     (campground detail pages only)
     data-nav-cta-text="…"        – button label  (default: "Browse campgrounds →")
     data-nav-cta-url="…"         – button href   (default: "/campgrounds")
     data-nav-cta-external        – adds target="_blank" to the CTA

   Active link is set automatically from window.location.pathname.
   ============================================================ */

(function () {

  /* ── Config from body attributes ─────────────────────────── */
  const body         = document.body;
  const transparent  = body.hasAttribute('data-nav-transparent');
  const ctaText      = body.dataset.navCtaText || 'Browse campgrounds →';
  const ctaUrl       = body.dataset.navCtaUrl  || '/campgrounds';
  const ctaExternal  = body.hasAttribute('data-nav-cta-external');

  /* Resolve beside this script for both hosted and local-file previews. */
  const assetRoot    = new URL('.', document.currentScript.src).href;

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
           width="155" height="44">
    </a>
    <div class="nav-right">
      <ul class="nav-links">
        <li><a href="/campgrounds"${active('campground')}>Campgrounds</a></li>
        <li><a href="/map"${active('map')}>Map</a></li>
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

// Campground referral intent; no email, query string, or reservation details sent.
document.addEventListener('click', function (event) {
  const link = event.target.closest('a');
  if (!link || !location.pathname.includes('/campground/') || typeof window.gtag !== 'function') return;
  const configured = document.body.dataset.navCtaUrl;
  if (!configured) return;
  const destination = new URL(link.href, location.href);
  if (destination.href !== new URL(configured, location.href).href || destination.origin === location.origin) return;
  window.gtag('event', 'campground_outbound', {
    campground_slug: location.pathname.split('/').pop().replace(/\.html$/, ''),
    provider: destination.hostname,
    transport_type: 'beacon'
  });
});
