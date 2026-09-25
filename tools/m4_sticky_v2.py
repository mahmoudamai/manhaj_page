"""Block 24 (sticky bar) v2 — visible over dark AND light sections:
- its fill is a notch lighter than the dark sections (primary, not primary-deep)
- a crisp gold line on top with a thin light line above it (separates it from
  dark sections) and an upward shadow (separates it from light sections)."""

CSS = r"""
/* ---------------- v2 · stands out on dark and light sections ---------------- */
.m4-sticky__action-bar,
.m4-sticky__action-bar::after {
  background:
    radial-gradient(circle at 8% 0%, color-mix(in srgb, var(--m4-accent) 12%, transparent), transparent 30%),
    linear-gradient(118deg, color-mix(in srgb, var(--m4-primary) 92%, var(--m4-black)) 0%, var(--m4-primary) 55%, color-mix(in srgb, var(--m4-primary) 88%, var(--m4-highlight)) 100%);
}

.m4-sticky__action-bar {
  border-top: 0;
}

.m4-sticky__action-bar::after {
  box-shadow:
    0 -1px 0 color-mix(in srgb, var(--m4-white) 45%, transparent),
    0 -14px 34px rgba(0, 0, 0, .22);
}

/* the gold line along the top edge */
.m4-sticky__action-bar::before {
  z-index: 2;
  top: 0;
  right: auto;
  left: 50%;
  width: 100vw;
  transform: translateX(-50%);
  height: 2px;
  background: linear-gradient(90deg, transparent 0%, var(--m4-accent) 18%, var(--m4-accent-soft) 50%, var(--m4-accent) 82%, transparent 100%);
  opacity: .9;
}
"""


def apply(path):
    s = path.read_text(encoding="utf-8")
    # this block has no self-check marker: add the CSS at the end of its <style>
    m = s.index("</style>")
    s = s[:m] + CSS.strip() + "\n\n" + s[m:]
    path.write_text(s, encoding="utf-8")
    return len(s)
