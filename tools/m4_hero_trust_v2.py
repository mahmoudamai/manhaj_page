"""Block 03 (hero trust) v2: the discount and saving right under the hero button.

The hero button ("ابدأ الآن بـ 7,500 جنيه فقط") is the first place visitors see
the price, so the first line of this block anchors it: old price + saving.
Keep OLD_PRICE / SAVING / DISCOUNT in sync with Block 21 (offer) and 10B.
"""

OLD_PRICE = "9,500 جنيه"
SAVING = "وفّر 2,000 جنيه"
DISCOUNT = "خصم أكثر من 20%"

CSS = r"""
/* ---------------- v2 · price anchor under the hero button ---------------- */
#m4-hero-trust .m4-hero-trust__price {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 6px 10px;
  margin: 0 auto 16px;
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

#m4-hero-trust .m4-hero-trust__price b {
  color: var(--m4-primary-deep);
  font-weight: 800;
}

#m4-hero-trust .m4-hero-trust__price-badge {
  padding: 3px 11px;
  border-radius: 999px;
  background: color-mix(in srgb, var(--m4-alert) 12%, transparent);
  color: var(--m4-alert);
  font-size: .86em;
  font-weight: 800;
}

#m4-hero-trust .m4-hero-trust__price-sep {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--m4-accent);
}

/* the proof + trust rows sit under a hairline, so the price reads as part of the button */
#m4-hero-trust .m4-hero-trust__price + .m4-hero-trust__proof {
  padding-top: 14px;
  border-top: 1px solid color-mix(in srgb, var(--m4-primary) 10%, transparent);
}

@media (max-width: 768px) {
  #m4-hero-trust .m4-hero-trust__price {
    gap: 5px 8px;
    margin-bottom: 13px;
    font-size: calc(.84rem * var(--m4-type-scale));
  }

  #m4-hero-trust .m4-hero-trust__price + .m4-hero-trust__proof {
    padding-top: 12px;
  }
}
"""


def html():
    return f"""
    <div class="m4-hero-trust__price">
      <span class="m4-hero-trust__price-badge">{DISCOUNT}</span>
      <span>بدلًا من <del>{OLD_PRICE}</del></span>
      <span class="m4-hero-trust__price-sep" aria-hidden="true"></span>
      <b>{SAVING}</b>
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
