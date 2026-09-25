"""Block 03 (hero trust) v2: the discount and saving right under the hero button.

The hero button ("ابدأ الآن بـ 7,500 جنيه فقط") is the first place visitors see
the price, so the first line of this block anchors it: old price + saving.
Keep OLD_PRICE / SAVING / DISCOUNT in sync with Block 21 (offer) and 10B.
"""

OLD_PRICE = "9,500 جنيه"
SAVING = "وفّر 2,000 جنيه"
DISCOUNT = "خصم أكثر من 20%"

CSS = r"""
/* ---------------- the GHL section that holds the hero blocks ----------------
   Give that GHL section the CSS class  m4-hero-host
   It continues the hero's colour behind the video, the stats, the button and
   this block, then fades into the cream of the next section (Kareem). */
.m4-hero-host {
  background:
    linear-gradient(180deg, var(--m4-bg-cloud) 0%, var(--m4-bg-cloud) 55%, var(--m4-bg-cream) 100%) !important;
}

/* ---------------- v2 · price anchor under the hero button ---------------- */
#m4-hero-trust .m4-hero-trust__price {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 6px 12px;
  margin: 0 auto 18px;
  color: var(--m4-text);
  font-size: calc(.95rem * var(--m4-type-scale));
  line-height: 1.5;
  font-weight: 600;
}

#m4-hero-trust .m4-hero-trust__price del {
  color: var(--m4-text-muted);
  font-weight: 700;
  text-decoration-color: var(--m4-alert);
  text-decoration-thickness: 2px;
}

/* one colour for the gain: the discount lives inside the green pill */
#m4-hero-trust .m4-hero-trust__price b {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 13px 4px 14px;
  border-radius: 999px;
  background: color-mix(in srgb, var(--m4-success, #177A4E) 11%, transparent);
  color: var(--m4-success, #177A4E);
  font-weight: 800;
}

#m4-hero-trust .m4-hero-trust__price b small {
  font-size: .84em;
  font-weight: 600;
  opacity: .85;
}

#m4-hero-trust .m4-hero-trust__price b svg {
  width: 14px;
  height: 14px;
  fill: none;
  stroke: currentColor;
  stroke-width: 2.6;
  stroke-linecap: round;
  stroke-linejoin: round;
}

/* «أكثر من 40 ألف مشترك» at the same weight as the trust points next to it */
#m4-hero-trust .m4-hero-trust__proof-text strong,
#m4-hero-trust .m4-hero-trust__trust-item {
  font-weight: 700;
}

/* phones: price, then a hairline, then proof and trust stacked */
@media (max-width: 768px) {
  #m4-hero-trust .m4-hero-trust__price {
    gap: 6px 8px;
    margin-bottom: 14px;
    font-size: calc(.86rem * var(--m4-type-scale));
  }

  #m4-hero-trust .m4-hero-trust__proof-text strong,
  #m4-hero-trust .m4-hero-trust__trust-item {
    font-size: calc(.76rem * var(--m4-type-scale));
  }

  #m4-hero-trust .m4-hero-trust__price + .m4-hero-trust__proof {
    padding-top: 13px;
    border-top: 1px solid color-mix(in srgb, var(--m4-primary) 10%, transparent);
  }
}

/* desktop: undo the old "smaller on desktop" sizes and put proof + trust on
   one row with a separator, under the price line */
@media (min-width: 769px) {
  #m4-hero-trust .m4-hero-trust__wrap {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    column-gap: 30px;
  }

  #m4-hero-trust .m4-hero-trust__price {
    flex-basis: 100%;
  }

  #m4-hero-trust .m4-hero-trust__proof {
    margin: 0;
  }

  #m4-hero-trust .m4-hero-trust__trust-row {
    margin: 0;
    padding-right: 30px;
    border-right: 1px solid color-mix(in srgb, var(--m4-primary) 14%, transparent);
  }

  #m4-hero-trust .m4-hero-trust__avatars span {
    width: 30px;
    height: 30px;
    flex-basis: 30px;
  }

  #m4-hero-trust .m4-hero-trust__avatars span:not(:first-child) {
    margin-right: -10px;
  }

  #m4-hero-trust .m4-hero-trust__proof-text strong {
    font-size: calc(.82rem * var(--m4-type-scale));
  }

  #m4-hero-trust .m4-hero-trust__proof-text small {
    font-size: calc(.7rem * var(--m4-type-scale));
  }

  #m4-hero-trust .m4-hero-trust__trust-item {
    font-size: calc(.82rem * var(--m4-type-scale));
  }

  #m4-hero-trust .m4-hero-trust__icon {
    width: 30px;
    height: 30px;
    flex-basis: 30px;
  }

  #m4-hero-trust .m4-hero-trust__icon svg {
    width: 14px;
    height: 14px;
  }
}
"""


def html():
    return f"""
    <div class="m4-hero-trust__price">
      <span>بدلًا من <del>{OLD_PRICE}</del></span>
      <b><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12 5 5 9-10"/></svg>{SAVING} <small>· {DISCOUNT}</small></b>
    </div>
"""


def apply(path):
    s = path.read_text(encoding="utf-8")
    marker = s.rindex("/* self-check")
    s = s[:marker] + CSS.strip() + "\n\n" + s[marker:]
    anchor = '<div class="m4-hero-trust__proof">'
    i = s.index(anchor)
    s = s[:i] + html().strip() + "\n\n    " + s[i:]
    path.write_text(s, encoding="utf-8")
    return len(s)
