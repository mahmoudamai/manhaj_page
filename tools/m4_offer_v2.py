"""Block 21 (main offer) v2:
- a two-stat row in the price card: content hours so far + lectures per month
- the saving in green (same language as the hero trust line and 10B)
- the lectures / live-sessions items state the schedule
Update HOURS as content grows (also in Blocks 02 and 15B)."""
import re

HOURS = "قرابة 17 ساعة"

STATS = f"""
        <div class="m4-offer__stats">
          <div><strong>{HOURS}</strong><span>من المحاضرات واللقاءات متاحة الآن</span></div>
          <div><strong>3 محاضرات</strong><span>جديدة كل شهر: يوم 10 و20 و30</span></div>
        </div>
"""

LECTURES_P = f"""<p>
                {HOURS} متاحة الآن، ومحاضرة جديدة كل 10 أيام:
                يوم 10 و20 و30 من كل شهر.
              </p>"""

LIVE_P = """<p>
                يُعلن عنها قبل موعدها بـ10 أيام على الأقل،
                وتجد تسجيلها على المنصة خلال 48 ساعة.
              </p>"""

CSS = r"""
/* ---------------- v2 · hours + lectures per month in the price card ---------------- */
#m4-offer .m4-offer__stats {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
  margin-top: 18px;
  text-align: center;
}

#m4-offer .m4-offer__stats div {
  padding: 10px 8px 9px;
  border-radius: calc(14px * var(--m4-radius-scale));
  border: 1px solid color-mix(in srgb, var(--m4-white) 12%, transparent);
  background: color-mix(in srgb, var(--m4-white) 6%, transparent);
}

#m4-offer .m4-offer__stats strong {
  display: block;
  color: var(--m4-accent);
  font-size: calc(1.08rem * var(--m4-heading-scale));
  line-height: 1.3;
  font-weight: 900;
}

#m4-offer .m4-offer__stats span {
  display: block;
  margin-top: 3px;
  color: color-mix(in srgb, var(--m4-white) 72%, transparent);
  font-size: calc(.72rem * var(--m4-type-scale));
  line-height: 1.5;
}

/* the saving in green, like everywhere else on the page */
#m4-offer .m4-offer__saving {
  border-color: color-mix(in srgb, var(--m4-success, #177A4E) 55%, transparent);
  background: color-mix(in srgb, var(--m4-success, #177A4E) 32%, transparent);
  color: color-mix(in srgb, var(--m4-success, #177A4E) 35%, var(--m4-white));
  font-weight: 800;
}

@media (max-width: 600px) {
  #m4-offer .m4-offer__stats strong {
    font-size: calc(.95rem * var(--m4-heading-scale));
  }

  #m4-offer .m4-offer__stats span {
    font-size: calc(.66rem * var(--m4-type-scale));
  }
}
"""


def apply(path):
    s = path.read_text(encoding="utf-8")
    # stats row right after the saving pill
    a = s.index('<div class="m4-offer__saving">')
    b = s.index("</div>", a) + len("</div>")
    s = s[:b] + "\n" + STATS + s[b:]
    # item texts
    s = re.sub(r"<p>\s*محتوى مسجل يضاف تدريجيا\s*ضمن المسار المتكامل للمنهج\.\s*</p>", LECTURES_P, s, count=1)
    s = re.sub(r"<p>\s*محطات للمراجعة والأسئلة\s*والتفاعل مع تقدم المحتوى\.\s*</p>", LIVE_P, s, count=1)
    m = s.rindex("/* self-check")
    s = s[:m] + CSS.strip() + "\n\n" + s[m:]
    path.write_text(s, encoding="utf-8")
    return len(s)
