"""Block 01 (hero) v2 — new opening copy (content phase):
kicker «رحلة نفسية إيمانية», title «من التيه… / إلى الطمأنينة», and a subtitle
that names both dimensions (psychological + faith) plus skills.
Only text changes; the design stays as generated."""

KICKER = "رحلة نفسية إيمانية"
LINE_1 = "من التيه…"
LINE_2 = 'إلى <em class="m4-hero__title-accent">الطمأنينة</em>'
SUBTITLE = ("منهج متدرج على مدار عام، يعيد ترتيب فهمك لنفسك ولحياتك؛ "
            "بالجمع بين الفهم النفسي، والمرجعية الإيمانية، والمهارات العملية.")

CSS = r"""
/* v2 · the title is now short, so it can be bigger (relative to every
   breakpoint's own h1 size) */
#m4-hero .m4-hero__hero-title-line {
  font-size: 1.22em;
}

/* the key word: brand colour + the same gold marker as «المعارك الخفية» */
#m4-hero .m4-hero__title-accent {
  font-style: normal;
  color: var(--m4-primary);
  padding: 0 .08em;
  background: linear-gradient(transparent 68%, color-mix(in srgb, var(--m4-accent) 38%, transparent) 68%, color-mix(in srgb, var(--m4-accent) 38%, transparent) 90%, transparent 90%);
}

@media (max-width: 768px) {
  #m4-hero .m4-hero__hero-title-line {
    font-size: 1.1em;
  }
}
"""


def apply(path):
    s = path.read_text(encoding="utf-8")
    a = s.index('<div class="m4-hero__kicker')
    k0 = s.index("<strong>", a) + len("<strong>")
    k1 = s.index("</strong>", k0)
    s = s[:k0] + f"\n        {KICKER}\n      " + s[k1:]

    h0 = s.index("<h1")
    h0 = s.index(">", h0) + 1
    h1 = s.index("</h1>", h0)
    s = s[:h0] + (f'\n      <span class="m4-hero__hero-title-line">\n        {LINE_1}\n      </span>\n'
                  f'      <span class="m4-hero__hero-title-line">\n        {LINE_2}\n      </span>\n    ') + s[h1:]

    p0 = s.index('<p class="m4-hero__subtitle')
    p0 = s.index(">", p0) + 1
    p1 = s.index("</p>", p0)
    s = s[:p0] + f"\n      {SUBTITLE}\n    " + s[p1:]

    m = s.rindex("/* self-check")
    s = s[:m] + CSS.strip() + "\n\n" + s[m:]
    path.write_text(s, encoding="utf-8")
    return len(s)
