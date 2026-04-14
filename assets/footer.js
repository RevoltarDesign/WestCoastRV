/* ============================================================
   West Coast RV Camping — Shared Footer
   Single source of truth for footer HTML.
   Reads data-footer-note from <body> for per-page context.

   Usage — add to <body> if needed:
     data-footer-note="Data verified March 2026"
   ============================================================ */

/* ============================================================
   Stat Bar Enhancements
   Runs on campground pages only (checks for .stats-bar).
   - Highlights notable limiting values in gold so they jump out
   - Trims overly long stat-note subtitles
   ============================================================ */
(function () {
  const statsBar = document.querySelector('.stats-bar');
  if (statsBar) {
    // Inject highlight styles once
    const style = document.createElement('style');
    style.textContent = `
      .stat-val--flag {
        color: #F0A800 !important;
      }
      .stat-val--flag::after {
        content: '';
        display: inline-block;
        width: 6px;
        height: 6px;
        background: #F0A800;
        border-radius: 50%;
        margin-left: 6px;
        vertical-align: middle;
        position: relative;
        top: -2px;
      }
    `;
    document.head.appendChild(style);

    // Rules: which values on which labels should be flagged
    const FLAG_RULES = [
      { label: 'hookups',      values: ['none', 'dry camping', 'no hookups'] },
      { label: 'dump station', values: ['none', 'no', 'not available'] },
    ];

    // Max length: flag if ≤ 25 ft (small RVs only)
    const MAX_LENGTH_THRESHOLD = 25;

    // Subtitle replacements — keep these short
    const NOTE_REPLACEMENTS = {
      'available to all registered campers': 'all registered campers',
      'registered campers only':             'registered campers',
    };

    document.querySelectorAll('.stat').forEach(stat => {
      const labelEl = stat.querySelector('.stat-label');
      const valEl   = stat.querySelector('.stat-val');
      const noteEl  = stat.querySelector('.stat-note');

      if (!labelEl || !valEl) return;

      const label = labelEl.textContent.trim().toLowerCase();
      const val   = valEl.textContent.trim().toLowerCase();

      // Check flag rules
      const rule = FLAG_RULES.find(r => label.includes(r.label));
      if (rule && rule.values.some(v => val.includes(v))) {
        valEl.classList.add('stat-val--flag');
      }

      // Check max length threshold
      if (label.includes('max length') || label.includes('length')) {
        const num = parseInt(val, 10);
        if (!isNaN(num) && num <= MAX_LENGTH_THRESHOLD) {
          valEl.classList.add('stat-val--flag');
          // Add a clarifying note if not already set
          if (noteEl && !noteEl.textContent.toLowerCase().includes('small')) {
            noteEl.textContent = 'small RVs only';
          }
        }
      }

      // Fix long subtitles
      if (noteEl) {
        const noteText = noteEl.textContent.trim().toLowerCase();
        for (const [from, to] of Object.entries(NOTE_REPLACEMENTS)) {
          if (noteText === from) {
            noteEl.textContent = to;
            break;
          }
        }
      }
    });
  }
})();

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
          <h4>Campgrounds</h4>
          <a href="/campgrounds">All Campgrounds</a>
          <a href="/near-seattle">Near Seattle</a>
          <a href="/campgrounds?type=national">National Parks</a>
          <a href="/campgrounds?type=state">State Parks</a>
          <a href="/campgrounds?hookup=full">Full Hookups</a>
        </div>

        <div class="footer-col">
          <h4>Info</h4>
          <a href="/field-notes">Field Notes</a>
          <a href="/about">About</a>
        </div>

      </div>
      <div class="footer-bottom">
        <span class="footer-copy">© ${new Date().getFullYear()} West Coast RV Camping. No paid placements.</span>
        ${note ? `<span class="footer-note">${note}</span>` : ''}
      </div>
      <p class="footer-disclaimer">Campground information is sourced from official park agencies and publicly available data. Always confirm details directly with the campground before your visit — fees, availability, and conditions change.</p>
    </div>`;

  /* Insert just before </body> */
  document.body.appendChild(footer);

})();
