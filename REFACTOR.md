# Phase 1 — Architecture refactor (M4)

Source: the production blocks in `Manhaj_Version_02.docx` (kept untouched in `legacy/`).
Output: `refactor/blocks/` — 25 section blocks plus Block 00 and Block 00B, each one ready to copy and paste.
Content, section order, prices, links, images and CTA destinations are unchanged. Section H has the checks.

---

## A. Architecture summary

| Before | After |
|---|---|
| 25 code blocks, each with its own `<link>` fonts, `<style>` and `<script>` | **Block 00** (all CSS + fonts), **Block 00B** (all JS), **25 HTML-only blocks** |
| Tajawal loaded 23 times | Fonts loaded once, in Block 00 |
| ~400 hard-coded colours, each section redefining `--petrol`, `--gold`… | **24 colour tokens**. Every other colour is derived from them with `color-mix()` (173 tints, max error 7/255, invisible) |
| ~50 IntersectionObservers in 25 scripts | 1 shared script, 4 small modules (motion, FAQ, sticky, masonry) |
| Content hidden with `opacity:0` until JS reveals it | Content visible by default. JS only animates what is still below the screen |
| 230+ `!important` | Kept only where they are needed: the sticky bar (it fights the GHL fixed section) and the hero full-bleed width |
| Mixed naming: `.reveal`, `.mhhm-card`, `.mhh-sticky-*` | One system: `#m4-<section>` and `.m4-<section>__<part>` |

**How the CSS is organised (Block 00):**
1. **Theme controls**: the only place you edit (section B).
2. **Shared primitives**: `.m4-section`, `.m4-container`, `.m4-kicker`, `.m4-heading`, `.m4-display`, `.m4-card`, `.m4-btn`, `.m4-btn-primary`, `.m4-reveal`. All are wrapped in `:where()`, so they have zero specificity and never override a section's own look. Use them for anything new.
3. **Motion system**.
4. **Sections**: each section keeps its own personality, scoped to its own `#m4-…` id. The styles are the same as before, but they now read the tokens.
5. **Typography roles**: which font headings use and which font the quotes use.
6. **No-JS safety nets**.

Each section's styling was moved as it was, without redesign. At default settings the page renders **pixel-identical** (section H).

---

## B. Main theme controls (top of Block 00)

```css
   1 · THEME CONTROLS  ← edit here
   ===================================================================== */
:root {

  /* ---------- brand colours ---------- */
  --m4-primary:          #1E5960;   /* petrol — main brand colour           */
  --m4-primary-deep:     #123C42;   /* dark petrol — dark sections, text    */
  --m4-primary-alt:      #294E63;   /* blue-petrol — gradients              */
  --m4-ink:              #354859;   /* navy — headings on light             */
  --m4-secondary:        #A7BCA6;   /* sage                                 */
  --m4-secondary-soft:   #DDE8DC;   /* light sage                           */
  --m4-highlight:        #8EC9C4;   /* teal                                 */
  --m4-highlight-soft:   #A9DED8;   /* bright teal                          */
  --m4-accent:           #D3B267;   /* gold — accents, prices, CTA          */
  --m4-accent-soft:      #E9D8A8;   /* light gold                           */
  --m4-accent-deep:      #90794C;   /* dark gold — small gold text on light */
  --m4-olive:            #3C5141;   /* olive (section 15 image card)        */

  /* ---------- backgrounds ---------- */
  --m4-bg-paper:         #FFFDF8;
  --m4-bg-ivory:         #FBF7EF;
  --m4-bg-cream:         #F7F3EA;
  --m4-bg-cloud:         #EEF3F1;

  /* ---------- text ---------- */
  --m4-text:             #5D6A70;
  --m4-text-muted:       #748086;

  /* ---------- neutrals & utility (rarely changed) ---------- */
  --m4-white:            #FFFFFF;
  --m4-black:            #000000;
  --m4-live:             #FF3B30;   /* "live" dot                           */
  --m4-alert:            #E75C4D;   /* coral — "not for you", pulses        */
  --m4-telegram:         #2AABEE;
  --m4-whatsapp:         #25D366;

  /* ---------- CTA buttons (offer "ابدأ رحلتك الآن" + sticky checkout) ---------- */
  --m4-cta-bg:           #FF3B30;   /* the current red                      */
  --m4-cta-text:         #FFFFFF;

  /* ---------- typography ----------
     primary : body text, UI, numbers
     heading : section titles (defaults to primary — set to display for an editorial look)
     display : quotes, testimonials, emotional one-liners
     Other good pairs:  "Tajawal" · "Alexandria" · "Readex Pro"  /  "Markazi Text" · "Noto Naskh Arabic"
     (load any new family in the <link> at the top of Block 00) */
  --m4-font-primary:     "IBM Plex Sans Arabic", "Tajawal", system-ui, -apple-system, "Segoe UI", sans-serif;
  --m4-font-heading:     var(--m4-font-primary);
  --m4-font-display:     "Amiri", "Noto Naskh Arabic", serif;

  --m4-type-scale:       1;         /* all body/UI text sizes     (0.9 – 1.15) */
  --m4-heading-scale:    1;         /* all headings & big numbers (0.85 – 1.2) */

  /* ---------- spacing & shape ---------- */
  --m4-space-scale:      1;         /* section top/bottom padding (0.75 – 1.25) */
  --m4-radius-scale:     1;         /* every rounded corner (0 = sharp, 1.5 = softer) */
  --m4-container:        1180px;    /* width used by .m4-container */
  --m4-gutter:           clamp(18px, 4vw, 40px);

  /* ---------- shadows (used by the shared primitives) ---------- */
  --m4-shadow-sm:        0 1px 2px color-mix(in srgb, var(--m4-ink) 8%, transparent), 0 6px 18px color-mix(in srgb, var(--m4-ink) 6%, transparent);
  --m4-shadow-md:        0 2px 6px color-mix(in srgb, var(--m4-ink) 6%, transparent), 0 18px 44px color-mix(in srgb, var(--m4-ink) 10%, transparent);
  --m4-shadow-lg:        0 4px 10px color-mix(in srgb, var(--m4-ink) 6%, transparent), 0 30px 70px color-mix(in srgb, var(--m4-ink) 14%, transparent);

  /* ---------- motion ---------- */
  --m4-motion-scale:     1;         /* every hover/transition speed (0 = off, 1.3 = slower) */
  --m4-ease:             cubic-bezier(.22, .72, .2, 1);
  --m4-ease-out:         cubic-bezier(.16, 1, .3, 1);
  --m4-reveal-duration:  .85s;      /* scroll entrance */
  --m4-reveal-distance:  18px;
  --m4-reveal-stagger:   70ms;
}
```

Notes:
- **Every colour on the page follows these tokens.** For example, change `--m4-primary` and the gradients, borders, soft tints and shadows built from it change too.
- **The `*-scale` variables multiply the existing values.** `1` = today's design, `1.1` = 10% larger or slower, `0` for radius = sharp corners.
- **The font variables have three roles.** `--m4-font-heading` defaults to the primary font. Set it to `var(--m4-font-display)` for an editorial look on the titles.

---

## C–E. The blocks

| File | Where it goes |
|---|---|
| `refactor/blocks/00-main-css.html` | **Block 00**: fonts + Main CSS (readable, 300 KB) |
| `refactor/blocks/00-main-css.min.html` | Same thing minified (260 KB) |
| `refactor/blocks/00-main-css.css` | **Pure CSS for GHL's Custom CSS box** (fonts via `@import`) |
| `refactor/blocks/00-main-css-split/` | Main CSS in **6 parts** (< 62 KB each), for Code Elements |
| `refactor/blocks/00B-shared-js.html` | **Block 00B**: shared JavaScript |
| `refactor/blocks/01-hero.html` … `25-footer.html` | One file per existing code block, in the same order |
| `refactor/preview.html` | The full page for checking (GHL-only elements shown as grey placeholders) |

---

## F. Important ID / class changes

**Section ids** (anchors and JS updated everywhere):

| # | Block | Old | New | File |
|---|---|---|---|---|
| 01 | Section 01 · Block 01 — Hero | `#mhhm-videoIntro` | `#m4-hero` | `01-hero.html` |
| 02 | Section 01 · Block 04 — Course info | `#mhhm-heroStats` | `#m4-hero-stats` | `02-hero-stats.html` |
| 03 | Section 01 · Block 06 — Trust | `#mhhm-purchaseTrust` | `#m4-hero-trust` | `03-hero-trust.html` |
| 04 | Section 02 · Block 01 — Kareem intro | `#mhhm-mini-kareem` | `#m4-kareem-intro` | `04-kareem-intro.html` |
| 05 | Section 03 — Pain | `#mhhm-pain` | `#m4-pain` | `05-pain.html` |
| 06 | Section 04 — سر الفاقة | `#mhhm-faqah` | `#m4-faqah` | `06-faqah.html` |
| 07 | Section 05 — Member comment | `#mhhm-rasha-moment` | `#m4-member-story` | `07-member-story.html` |
| 08 | Section 06 — How it was built | `#mhhm-methodology` | `#m4-method` | `08-method.html` |
| 09 | Section 07 — The four axes | `#mhhm-curriculum` | `#m4-curriculum` | `09-curriculum.html` |
| 10 | Section 08 — Surat Yusuf | `#mhhm-yusuf` | `#m4-yusuf` | `10-yusuf.html` |
| 11 | Section 09 — Lectures so far | `#mhhm-lectures` | `#m4-lectures` | `11-lectures.html` |
| 12 | Section 10 — Attendee comments | `#mhhm-content-proofs` | `#m4-lecture-notes` | `12-lecture-notes.html` |
| 13 | Section 11 — رياضة الفكر | `#mhhm-practice` | `#m4-practice` | `13-practice.html` |
| 14 | Section 12 — Live sessions | `#mhhm-live` | `#m4-live` | `14-live.html` |
| 15 | Section 13 — Telegram community | `#mhhm-telegram` | `#m4-telegram` | `15-telegram.html` |
| 16 | Section 14 — WhatsApp screenshots | `#mhhm-wa-masonry` | `#m4-wa-reviews` | `16-wa-reviews.html` |
| 17 | Section 15 — Is it for you | `#mhhm-fit` | `#m4-fit` | `17-fit.html` |
| 18 | Section 16 — The year journey | `#mhhm-yearJourney` | `#m4-year` | `18-year.html` |
| 19 | Section 17 — Written testimonials | `#mhhm-main-testimonials` | `#m4-testimonials` | `19-testimonials.html` |
| 20 | Section 18 — Kareem full profile | `#mhhm-kareem` | `#m4-kareem` | `20-kareem.html` |
| 21 | Section 19 — Price & offer | `#mhhm-offer` | `#m4-offer` | `21-offer.html` |
| 22 | Section 20 — 7-day guarantee | `#mhhm-guarantee` | `#m4-guarantee` | `22-guarantee.html` |
| 23 | Section 21 — FAQ | `#mhhm-faq` | `#m4-faq` | `23-faq.html` |
| 24 | Section 22 — Sticky bar (inside the fixed GHL section) | `(no id)` | `#m4-sticky` | `24-sticky.html` |
| 25 | Section 23 — Footer | `#mhhm-footer` | `#m4-footer` | `25-footer.html` |

**Classes:** every class inside a section follows `.m4-<section>__<part>` (camelCase → kebab-case). Examples:

| Old | New |
|---|---|
| `#mhhm-videoIntro .crown` | `#m4-hero .m4-hero__crown` |
| `#mhhm-lectures .mhhm-groupHead` | `#m4-lectures .m4-lectures__group-head` |
| `#mhhm-curriculum .mhhm-stage--four` | `#m4-curriculum .m4-curriculum__stage--four` |
| `.mhh-checkout-btn` (sticky) | `.m4-sticky__checkout-btn` |

**States:**

| Old | New | Why |
|---|---|---|
| `.visible`, `.mhhm-visible` | removed → elements carry `.m4-reveal` | Content no longer depends on JS to appear |
| `.mhhm-open` (FAQ) | `.is-open` | One state naming for the whole page |
| `.mhh-sticky-visible` | `.is-visible` | Same |
| `.mhh-sticky-cta` (class **on the GHL section**) | `.m4-sticky-host` | New name. **The old class still works**, so nothing breaks if you don't rename it yet |
| keyframes `mhhmKareemFloat`, … | `m4-kareem-intro-kareem-float`, … | Keyframe names are global, so they are namespaced per section |

Dead CSS for classes that don't exist in any block (for example `.heroDivider` and `.mhhm-brandLink`) was dropped.

---

## G. Migration steps (in GHL)

1. **Back up**: duplicate the current page in GHL before starting.
2. **Block 00 (Main CSS)**: pick ONE of these three options.
   - **A. Custom CSS box (recommended)**: page **Settings → Custom CSS** → paste **`00-main-css.css`**. This is pure CSS with no `<style>` tags; the `.html` files do **not** belong in this box. It also applies in the builder.
   - **B. Code Elements**: paste `00-main-css-split/part1 … part6` into **6 Code Elements at the very top of the page**, in order. Use this if GHL cuts long code; each part is under 62 KB.
   - **C. Single Code Element / Tracking Code**: `00-main-css.html` (300 KB). Only if your GHL account accepts that size.
   Delete any older copy of Block 00 first, so the CSS is never loaded twice.
3. **Block 00B (JS)**: paste `00B-shared-js.html` into **Tracking Code → Head** (after Block 00), or into the **last** Code Element on the page.
4. **For each existing Code Element**: select all, delete, and paste the matching file from `refactor/blocks/` (01 → 25, same order as the mapping table). Every old `<link>`, `<style>` and `<script>` disappears with this step. Nothing needs to be deleted by hand.
5. **GHL elements stay as they are**: the video (block 02), the button (block 05), the logos marquee and the fixed sticky section. The code for block 03 (video look) and block 07 (PiP) was not in the file, so they were not changed. If they are Code Elements, keep them.
6. **Sticky section**: in the fixed GHL section's settings, change the custom class `mhh-sticky-cta` → `m4-sticky-host` (optional, the old name still works).
7. **Publish, then open the live page**, not the editor, to see the entrance animations.

To try a theme: edit the tokens at the top of Block 00 and republish.

---

**Self-check:** Block 00B checks that the whole Main CSS arrived. If a part was dropped or cut, it writes a warning to the browser console. On GHL `/preview/` links, or with `?m4-debug=1`, it also shows a red bar that names the missing part.

---

## H. Final verification (run in Chromium, desktop 1440px and mobile 390px)

| Check | Result |
|---|---|
| Content unchanged | ✅ All Arabic text, all `href`, `src`, `alt`, `target`, `rel`, `aria-*`, `width` and `height` compared block by block: identical in all 25 blocks |
| Links, images, CTAs | ✅ Checkout, WhatsApp and `#faq` anchors preserved (`#mhhm-faq` → `#m4-faq`, updated in the sticky bar) |
| All sections remain | ✅ 25 blocks, same order |
| Design unchanged | ✅ Pixel diff against the original (same fonts): **22 of 24 sections 0.000% different** on desktop and mobile. Telegram (13) and written testimonials (17) differ by < 0.1% (colour rounding inside two gradients) |
| Mobile and desktop | ✅ Same diff at 390px and 1440px, no horizontal overflow |
| GHL editor/preview shows everything | ✅ Inside an iframe (how the GHL builder renders) motion is off and 0 elements are hidden |
| Visible without JavaScript | ✅ JS disabled: 0 hidden elements, FAQ answers expanded, sticky bar visible, gallery at natural size |
| Reduced motion | ✅ No hidden elements, no animation |
| Behaviour | ✅ FAQ accordion (one open at a time, `aria-expanded`), sticky show/hide (hidden at the top and over the price section), sticky "FAQ" jump, back-to-top, Kareem masonry gallery. **0 JS errors** |
| Theme editable centrally | ✅ 24 colour tokens + CTA + 3 fonts + 5 scales + motion. Only 3 decorative gold/cream tints remain as fixed values |

**Bugs found in the original and fixed along the way:**
- In the original, **the offer, guarantee and FAQ heads stayed at `opacity:0` even after scrolling the whole page on mobile**, along with the last Kareem photos. The old observers missed them. This is the "empty sections" issue. The new motion system reveals anything that has reached the screen or been scrolled past, and everything left when you reach the bottom of the page.
- **The sticky bar looked for `#mhhm-hero`**, which doesn't exist, so it always fell back to "after 650px". It now appears once the whole hero cluster (text, video, button and trust row) is behind the visitor. To go back to the old trigger, change `m4-hero-trust` to `m4-hero` in Block 00B.
- **Without JS, the Kareem gallery collapsed to 6px rows** and the FAQ answers could not be read. Both are fixed by the safety nets.

**Default fonts:** IBM Plex Sans Arabic (primary) + Amiri (display: member quotes and testimonials, the «الفاقة» term, Kareem's philosophy). To go back to the old look, set `--m4-font-primary: "Tajawal", Arial, sans-serif;` and add Tajawal to the `<link>` at the top of Block 00.

**To regenerate:** `python3 tools/refactor_legacy.py` rebuilds `refactor/` from `legacy/`.
