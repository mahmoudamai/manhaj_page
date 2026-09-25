"""Block 09 v2 — «محاور المنهج»: merges «كيف تم بناء منهج الطمأنينة؟» (Block 08,
now removed) into the curriculum map. Keeps the map design (centre + 4 branches).

- head: new kicker/title, the program designer's intro, and the three layers
  (meaning · understanding · skill) that used to be Block 08, as one line
- centre: الفاقة as the starting point
- axes 01/02: the program designer's titles (+ her wording in 02)
- axes 03/04: current text unchanged
- tags under each axis, and a closing line under the map
"""
import re

HEAD = """<div class="m4-curriculum__head m4-reveal">
      <div class="m4-curriculum__kicker">
        محاور المنهج
      </div>
      <h2>
        أربعة محاور… تبني الطمأنينة من جذورها
      </h2>
      <p>
        «منهج الطمأنينة» رحلة إيمانية نفسية، تهدف إلى مساعدة الإنسان
        على التحرر من المخاوف، وبناء الصلابة النفسية،
        واستعادة السلام الداخلي في ظل ضغوط الحياة المعاصرة.
      </p>
      <div class="m4-curriculum__layers" aria-label="في كل محور">
        <span class="m4-curriculum__layers-label">في كل محور:</span>
        <span><b>معنى إيماني</b> نرجع إليه</span>
        <span><b>فهم نفسي</b> يوضح ما يحدث</span>
        <span><b>مهارة</b> نعيش بها</span>
      </div>
    </div>"""

CENTER_P = """<p>
          تبدأ من فهم <b>«الفاقة»</b>،
          ثم تبني الوعي والتصورات،
          وتنتقل إلى المهارات
          وتطبيقها في الحياة اليومية.
        </p>"""

TITLES = {
    "01": "البناء التأسيسي وإعادة هيكلة الواقع",
    "02": "بناء المعتقدات والتصورات الكبرى",
}

TEXT_02 = """<p>
          لكي ينتقل الإنسان من حال نفسي إلى آخر،
          يحتاج إلى منظومة وعي جديدة
          يرى بها نفسه والحياة وتقلباتها،
          وعلى رأسها التعرف على الله عز وجل؛
          فيتحول الإيمان من معارف نظرية
          إلى يقين تُبنى عليه الصلابة النفسية.
        </p>"""

TAGS = {
    "01": ["سر الفاقة ونشأتها", "الخروج من التيه", "ترميم البوصلة"],
    "02": ["التسليم الواعي", "التوكل الصادق", "الاستغناء بالله"],
    "03": ["فهم المشاعر", "ضبط التفكير الناقد", "الحد من جلد الذات"],
    "04": ["حدود نفسية صحية", "علاقات متوازنة", "تواصل دون خوف"],
}

CLOSING = """
    <p class="m4-curriculum__closing m4-reveal">
      الفكرة ليست في كثرة المعلومات،
      <strong>بل في أن ترى الصورة مترابطة.</strong>
    </p>
"""

CSS = r"""
/* ---------------- v2 · axes: layers line, tags, closing ---------------- */
#m4-curriculum .m4-curriculum__layers {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 8px 10px;
  margin-top: 20px;
}

#m4-curriculum .m4-curriculum__layers span {
  padding: 7px 14px;
  border-radius: 999px;
  border: 1px solid color-mix(in srgb, var(--m4-primary) 12%, transparent);
  background: color-mix(in srgb, var(--m4-white) 70%, transparent);
  color: var(--m4-text);
  font-size: calc(.84rem * var(--m4-type-scale));
  line-height: 1.4;
  font-weight: 500;
}

#m4-curriculum .m4-curriculum__layers b {
  color: var(--m4-primary-deep);
  font-weight: 800;
}

#m4-curriculum .m4-curriculum__layers .m4-curriculum__layers-label {
  padding: 0;
  border: 0;
  background: none;
  color: var(--m4-accent-deep);
  font-weight: 800;
}

#m4-curriculum .m4-curriculum__center p b {
  color: var(--m4-accent-soft);
  font-weight: 800;
}

#m4-curriculum .m4-curriculum__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 12px;
}

#m4-curriculum .m4-curriculum__tags span {
  padding: 3px 10px;
  border-radius: 999px;
  background: color-mix(in srgb, var(--m4-accent-soft) 35%, var(--m4-white));
  border: 1px solid color-mix(in srgb, var(--m4-accent) 30%, transparent);
  color: var(--m4-primary-deep);
  font-size: calc(.7rem * var(--m4-type-scale));
  line-height: 1.6;
  font-weight: 700;
}

#m4-curriculum .m4-curriculum__closing {
  max-width: 720px;
  margin: 34px auto 0;
  text-align: center;
  color: var(--m4-text);
  font-size: calc(1.02rem * var(--m4-type-scale));
  line-height: 1.8;
}

#m4-curriculum .m4-curriculum__closing strong {
  color: var(--m4-primary-deep);
  font-weight: 800;
}

/* the map needs a little more room for the tags */
@media (min-width: 901px) {
  #m4-curriculum .m4-curriculum__board {
    min-height: 720px;
  }

  #m4-curriculum .m4-curriculum__stage {
    width: 330px;
  }
}

@media (max-width: 600px) {
  #m4-curriculum .m4-curriculum__layers {
    gap: 6px;
    margin-top: 14px;
  }

  #m4-curriculum .m4-curriculum__layers span {
    padding: 5px 10px;
    font-size: calc(.74rem * var(--m4-type-scale));
  }

  #m4-curriculum .m4-curriculum__layers .m4-curriculum__layers-label {
    flex-basis: 100%;
    text-align: center;
  }

  #m4-curriculum .m4-curriculum__tags span {
    font-size: calc(.66rem * var(--m4-type-scale));
  }

  #m4-curriculum .m4-curriculum__closing {
    margin-top: 22px;
    font-size: calc(.9rem * var(--m4-type-scale));
  }
}
"""


def apply(path):
    s = path.read_text(encoding="utf-8")
    s = s.replace('aria-label="مراحل منهج الطمأنينة"', 'aria-label="محاور منهج الطمأنينة"')
    # head
    a = s.index('<div class="m4-curriculum__head')
    b = s.index('<div class="m4-curriculum__board')
    b = s.rindex("</div>", a, b) + len("</div>")
    s = s[:a] + HEAD + s[b:]
    # centre text
    c = s.index('<div class="m4-curriculum__center')
    p0 = s.index("<p>", c)
    p1 = s.index("</p>", p0) + len("</p>")
    s = s[:p0] + CENTER_P + s[p1:]
    # stages
    for step in ["01", "02", "03", "04"]:
        st = s.index(f'data-step="{step}"')
        end = s.index("</article>", st)
        block = s[st:end]
        if step in TITLES:
            block = re.sub(r"<h3>.*?</h3>", f"<h3>\n          {TITLES[step]}\n        </h3>", block, count=1, flags=re.S)
        if step == "02":
            block = re.sub(r"<p>.*?</p>", TEXT_02, block, count=1, flags=re.S)
        tags = "".join(f"<span>{t}</span>" for t in TAGS[step])
        block = block.rstrip() + f'\n        <div class="m4-curriculum__tags">{tags}</div>\n      '
        s = s[:st] + block + s[end:]
    # closing line after the board (before the wrap closes)
    w = s.rindex("</section>")
    wrap_end = s.rindex("</div>", 0, w)          # closes .wrap
    s = s[:wrap_end] + CLOSING.strip("\n") + "\n\n  " + s[wrap_end:]
    # css
    m = s.rindex("/* self-check")
    s = s[:m] + CSS.strip() + "\n\n" + s[m:]
    path.write_text(s, encoding="utf-8")
    return len(s)
