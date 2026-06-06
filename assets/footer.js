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

  /* ── Newsletter styles (injected once) ───────────────────── */
  const nlStyle = document.createElement('style');
  nlStyle.textContent = `
    .footer-newsletter {
      background: var(--forest);
      padding: 40px var(--gutter);
    }
    .footer-newsletter-inner {
      max-width: var(--max-w);
      margin: 0 auto;
      display: flex;
      align-items: center;
      gap: 40px;
      flex-wrap: wrap;
    }
    .footer-nl-copy { flex: 1; min-width: 220px; }
    .footer-nl-copy h3 {
      font-family: var(--font-display);
      font-size: 20px;
      font-weight: 700;
      color: var(--white);
      margin: 0 0 6px;
    }
    .footer-nl-copy p {
      font-size: 14px;
      color: rgba(255,255,255,.7);
      margin: 0;
      line-height: 1.5;
    }
    .footer-nl-form {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      flex-shrink: 0;
    }
    .footer-nl-input {
      padding: 10px 16px;
      border-radius: var(--r-pill);
      border: 1.5px solid rgba(255,255,255,.25);
      background: rgba(255,255,255,.12);
      color: var(--white);
      font-size: 14px;
      width: 240px;
      outline: none;
      transition: border-color .15s;
    }
    .footer-nl-input::placeholder { color: rgba(255,255,255,.5); }
    .footer-nl-input:focus { border-color: rgba(255,255,255,.6); }
    .footer-nl-btn {
      padding: 10px 22px;
      border-radius: var(--r-pill);
      background: var(--white);
      color: var(--forest);
      font-size: 14px;
      font-weight: 600;
      border: none;
      cursor: pointer;
      white-space: nowrap;
      transition: opacity .15s;
    }
    .footer-nl-btn:hover { opacity: .9; }
    .footer-nl-thanks {
      font-size: 14px;
      color: rgba(255,255,255,.85);
      display: none;
      align-items: center;
      gap: 8px;
      padding: 10px 0;
    }
    @media (max-width: 600px) {
      .footer-nl-input { width: 100%; }
      .footer-nl-form  { width: 100%; }
      .footer-nl-btn   { width: 100%; text-align: center; }
    }
  `;
  document.head.appendChild(nlStyle);

  /* ── Newsletter strip ─────────────────────────────────────── */
  const nlStrip = document.createElement('div');
  nlStrip.className = 'footer-newsletter';
  nlStrip.innerHTML = `
    <div class="footer-newsletter-inner">
      <div class="footer-nl-copy">
        <h3>Get the field notes</h3>
        <p>New guides, campground additions, and seasonal picks — straight to your inbox.</p>
      </div>
      <div>
        <!-- TODO: Replace this form action with your newsletter platform embed (Beehiiv, Mailchimp, etc.) -->
        <form class="footer-nl-form" onsubmit="(function(e){
          e.preventDefault();
          var f=e.target; var inp=f.querySelector('.footer-nl-input');
          if(!inp.value||!inp.value.includes('@'))return;
          f.style.display='none';
          f.nextElementSibling.style.display='flex';
        })(event)">
          <input class="footer-nl-input" type="email" placeholder="your@email.com" required>
          <button class="footer-nl-btn" type="submit">Subscribe</button>
        </form>
        <div class="footer-nl-thanks">
          <span>✓</span> <span>You're on the list — talk soon.</span>
        </div>
      </div>
    </div>`;

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

  /* Insert newsletter strip + footer just before </body> */
  document.body.appendChild(nlStrip);
  document.body.appendChild(footer);

})();
