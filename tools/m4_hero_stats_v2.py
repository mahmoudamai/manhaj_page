"""Block 02 (hero stats) v2 — the lectures slot shows two different numbers,
told apart by words and by a "live" dot:
  total over the year  → «أكثر من 30 محاضرة على مدار العام»
  available right now  → «● متاح الآن: قرابة 17 ساعة»  (grows every 10 days)
Update NOW_HOURS as content grows (also Blocks 15B, 21, 23)."""

LABEL = "عدد المحاضرات"
TOTAL = "أكثر من 30 محاضرة على مدار العام"
NOW_HOURS = "قرابة 17 ساعة"

CSS = r"""
/* v2 · "available now" chip under the lectures total, with a live dot */
#m4-hero-stats .m4-hero-stats__now {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 5px;
  padding: 2px 9px 2px 10px;
  border-radius: 999px;
  background: color-mix(in srgb, var(--m4-success, #177A4E) 10%, transparent);
  color: var(--m4-success, #177A4E);
  font-size: calc(.7rem * var(--m4-type-scale));
  line-height: 1.6;
  font-weight: 800;
  white-space: nowrap;
}

#m4-hero-stats .m4-hero-stats__now i {
  position: relative;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: currentColor;
}

#m4-hero-stats .m4-hero-stats__now i::after {
  content: "";
  position: absolute;
  inset: -3px;
  border-radius: 50%;
  border: 1.5px solid currentColor;
  opacity: 0;
  animation: m4-stats-live calc(2s * var(--m4-motion-scale)) ease-out infinite;
}

@keyframes m4-stats-live {
  0% { transform: scale(.6); opacity: .8; }
  100% { transform: scale(1.6); opacity: 0; }
}

@media (prefers-reduced-motion: reduce) {
  #m4-hero-stats .m4-hero-stats__now i::after {
    animation: none;
  }
}
"""


def apply(path):
    s = path.read_text(encoding="utf-8")
    s = s.replace("عدد المحاضرات", LABEL, 1)
    s = s.replace("30 محاضرة + لقاءات مباشرة",
                  f'{TOTAL}\n          </span>\n\n          <span class="m4-hero-stats__now"><i aria-hidden="true"></i>متاح الآن: {NOW_HOURS}',
                  1)
    m = s.rindex("/* self-check")
    s = s[:m] + CSS.strip() + "\n\n" + s[m:]
    path.write_text(s, encoding="utf-8")
    return len(s)
