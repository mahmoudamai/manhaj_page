"""Block 04 (Kareem intro) — dark tone. Breaks the long light opening
(hero → Kareem → Pain) and makes the introduction feel more premium.
Only colours change; appended after the section's CSS so it wins."""

CSS = r"""
/* ---------------- dark tone (page rhythm) ---------------- */
#m4-kareem-intro {
  color: var(--m4-white);
  background:
    radial-gradient(circle at 10% 18%, color-mix(in srgb, var(--m4-accent) 12%, transparent), transparent 30%),
    radial-gradient(circle at 92% 88%, color-mix(in srgb, var(--m4-highlight) 10%, transparent), transparent 30%),
    linear-gradient(180deg, var(--m4-primary-deep) 0%, color-mix(in srgb, var(--m4-primary-deep) 86%, var(--m4-black)) 100%);
}

#m4-kareem-intro .m4-kareem-intro__card {
  border-color: color-mix(in srgb, var(--m4-white) 12%, transparent);
  background: linear-gradient(160deg, color-mix(in srgb, var(--m4-white) 8%, transparent), color-mix(in srgb, var(--m4-white) 3%, transparent));
  box-shadow: inset 0 1px 0 color-mix(in srgb, var(--m4-white) 8%, transparent), 0 24px 50px rgba(0, 0, 0, .18);
}

#m4-kareem-intro .m4-kareem-intro__card:hover {
  border-color: color-mix(in srgb, var(--m4-accent) 40%, transparent);
  box-shadow: inset 0 1px 0 color-mix(in srgb, var(--m4-white) 8%, transparent), 0 24px 50px rgba(0, 0, 0, .22);
}

#m4-kareem-intro .m4-kareem-intro__visual::before {
  background: radial-gradient(ellipse at center, color-mix(in srgb, var(--m4-accent) 22%, transparent) 0%, transparent 70%);
}

#m4-kareem-intro .m4-kareem-intro__photo {
  border-color: color-mix(in srgb, var(--m4-accent) 55%, transparent);
  background: var(--m4-primary-deep);
}

#m4-kareem-intro .m4-kareem-intro__kicker {
  color: var(--m4-accent);
}

#m4-kareem-intro h3 {
  color: var(--m4-white);
}

#m4-kareem-intro .m4-kareem-intro__role {
  color: color-mix(in srgb, var(--m4-white) 82%, transparent);
}

#m4-kareem-intro .m4-kareem-intro__role strong {
  color: var(--m4-accent-soft);
}

#m4-kareem-intro .m4-kareem-intro__description {
  color: color-mix(in srgb, var(--m4-white) 66%, transparent);
  border-color: color-mix(in srgb, var(--m4-white) 12%, transparent);
}

#m4-kareem-intro .m4-kareem-intro__proof {
  border-color: color-mix(in srgb, var(--m4-white) 12%, transparent);
}

#m4-kareem-intro .m4-kareem-intro__value {
  color: var(--m4-accent);
}

#m4-kareem-intro .m4-kareem-intro__label {
  color: color-mix(in srgb, var(--m4-white) 64%, transparent);
}

#m4-kareem-intro .m4-kareem-intro__metric,
#m4-kareem-intro .m4-kareem-intro__credential {
  border-color: color-mix(in srgb, var(--m4-white) 12%, transparent);
  background: color-mix(in srgb, var(--m4-white) 5%, transparent);
}

#m4-kareem-intro .m4-kareem-intro__credential {
  color: color-mix(in srgb, var(--m4-white) 76%, transparent);
}

#m4-kareem-intro .m4-kareem-intro__credential strong {
  color: var(--m4-white);
}

#m4-kareem-intro .m4-kareem-intro__credential-icon {
  color: var(--m4-accent);
  background: color-mix(in srgb, var(--m4-accent) 14%, transparent);
  box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--m4-accent) 35%, transparent);
}
"""


def apply(path):
    s = path.read_text(encoding="utf-8")
    m = s.rindex("/* self-check")
    s = s[:m] + CSS.strip() + "\n\n" + s[m:]
    path.write_text(s, encoding="utf-8")
    return len(s)
