"""Block 19 (testimonials) — dark tone, for the light/dark rhythm of the new
page order (it sits in the long light stretch fit → before/after → testimonials
→ Kareem). Only colours change; layout stays as generated. The rules are
appended after the section's own CSS, so they win at the same specificity."""

CSS = r"""
/* ---------------- dark tone (page rhythm) ---------------- */
#m4-testimonials {
  color: var(--m4-white);
  background:
    radial-gradient(circle at 8% 12%, color-mix(in srgb, var(--m4-accent) 12%, transparent), transparent 30%),
    radial-gradient(circle at 94% 88%, color-mix(in srgb, var(--m4-highlight) 10%, transparent), transparent 30%),
    linear-gradient(180deg, var(--m4-primary-deep) 0%, color-mix(in srgb, var(--m4-primary-deep) 84%, var(--m4-black)) 100%);
}

#m4-testimonials::before {
  border-color: color-mix(in srgb, var(--m4-white) 6%, transparent);
}

#m4-testimonials::after {
  border-color: color-mix(in srgb, var(--m4-accent) 14%, transparent);
}

#m4-testimonials .m4-testimonials__kicker {
  color: var(--m4-accent);
}

#m4-testimonials h2 {
  color: var(--m4-white);
}

#m4-testimonials .m4-testimonials__sub {
  color: color-mix(in srgb, var(--m4-white) 70%, transparent);
}

#m4-testimonials .m4-testimonials__card,
#m4-testimonials .m4-testimonials__card:nth-child(even) {
  border-color: color-mix(in srgb, var(--m4-white) 10%, transparent);
  background: linear-gradient(160deg, color-mix(in srgb, var(--m4-white) 8%, transparent), color-mix(in srgb, var(--m4-white) 3%, transparent));
  box-shadow: inset 0 1px 0 color-mix(in srgb, var(--m4-white) 8%, transparent);
}

#m4-testimonials .m4-testimonials__card::before {
  color: color-mix(in srgb, var(--m4-accent) 30%, transparent);
}

#m4-testimonials .m4-testimonials__card p {
  color: color-mix(in srgb, var(--m4-white) 86%, transparent);
}

#m4-testimonials .m4-testimonials__avatar {
  background: color-mix(in srgb, var(--m4-accent) 22%, transparent);
  border: 1px solid color-mix(in srgb, var(--m4-accent) 45%, transparent);
  color: var(--m4-accent-soft);
  box-shadow: none;
}

#m4-testimonials .m4-testimonials__person strong {
  color: var(--m4-white);
}

#m4-testimonials .m4-testimonials__card.m4-reveal:hover {
  border-color: color-mix(in srgb, var(--m4-accent) 40%, transparent);
  box-shadow: 0 20px 46px rgba(0, 0, 0, .25);
}

/* the closing quote: a gold-tinted glass bar instead of a dark bar on dark */
#m4-testimonials .m4-testimonials__closing {
  border-color: color-mix(in srgb, var(--m4-accent) 35%, transparent);
  background: linear-gradient(135deg, color-mix(in srgb, var(--m4-accent) 16%, transparent), color-mix(in srgb, var(--m4-accent) 6%, transparent));
}
"""


def apply(path):
    s = path.read_text(encoding="utf-8")
    m = s.rindex("/* self-check")
    s = s[:m] + CSS.strip() + "\n\n" + s[m:]
    path.write_text(s, encoding="utf-8")
    return len(s)
