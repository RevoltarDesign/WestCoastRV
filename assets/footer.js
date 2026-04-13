/* ============================================================
   West Coast RV Camping — Shared Footer
   Single source of truth for footer HTML.
   Reads data-footer-note from <body> for per-page context.

   Usage — add to <body> if needed:
     data-footer-note="Data verified March 2026"
   ============================================================ */

(function () {

  const note = document.body.dataset.footerNote || '';

  const footer = document.createElement('footer');
  footer.innerHTML = `
    <div class="footer-inner">
      <div class="footer-top">

        <div class="footer-brand">
          <div class="footer-logo">West Coast RV Camping</div>
          <p>The most complete independent guide to RV camping in Washington State — built for your rig, not a tent.</p>
        </div>

        <div class="footer-col">
          <h4>Explore</h4>
          <a href="/campgrounds">All Campgrounds</a>
          <a href="/campgrounds?type=national">National Parks</a>
          <a href="/campgrounds?type=state">State Parks</a>
          <a href="/campgrounds?hookup=full">Full Hookups</a>
        </div>

        <div class="footer-col">
          <h4>Field Notes</h4>
          <a href="/field-notes">All Articles</a>
          <a href="/field-notes?cat=seasonal">Seasonal Guides</a>
          <a href="/field-notes?cat=destination">Destination Guides</a>
          <a href="/field-notes?cat=gear">RV Gear</a>
        </div>

        <div class="footer-col">
          <h4>Info</h4>
          <a href="/about">About</a>
          <a href="/about#methodology">Our Methodology</a>
          <a href="mailto:andysantosjohnson@gmail.com">Contact</a>
        </div>

      </div>
      <div class="footer-bottom">
        <span class="footer-copy">© ${new Date().getFullYear()} West Coast RV Camping. Independent — no paid placements.</span>
        ${note ? `<span class="footer-note">${note}</span>` : ''}
      </div>
      <p class="footer-disclaimer">Campground information is sourced from official park agencies and publicly available data. Always confirm details directly with the campground before your visit — fees, availability, and conditions change.</p>
    </div>`;

  /* Insert just before </body> */
  document.body.appendChild(footer);

})();
