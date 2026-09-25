"""Block 13 (رياضة الفكر) v2: real cover mockups instead of sample pages.

Runs after refactor_legacy.py has generated 13-practice.html:
  - drops the CSS of the removed parts (sample pages, cropped cards, "continue" bar)
  - adds the book-mockup CSS
  - replaces the section HTML (header and member note are kept as they were)
Edit COVERS below to change or reorder the covers.
"""
import re

# the 9 cover images, in the order they appear on the shelf (first 3 = the fanned stack)
COVERS = [
    "https://assets.cdn.filesafe.space/25e9iURIgsa3JiXdcvsZ/media/6ab670be974a9da6eebcdf0c.jpg",
    "https://assets.cdn.filesafe.space/25e9iURIgsa3JiXdcvsZ/media/6ab670be8256c2fa61388333.jpg",
    "https://assets.cdn.filesafe.space/25e9iURIgsa3JiXdcvsZ/media/6ab670bd974a9da6eebcded4.jpg",
    "https://assets.cdn.filesafe.space/25e9iURIgsa3JiXdcvsZ/media/6ab670bd3dbd5f2bbbc9d2d6.jpg",
    "https://assets.cdn.filesafe.space/25e9iURIgsa3JiXdcvsZ/media/6ab670bc974a9da6eebcdec4.jpg",
    "https://assets.cdn.filesafe.space/25e9iURIgsa3JiXdcvsZ/media/6ab670bd6407f2cbe4d20a93.jpg",
    "https://assets.cdn.filesafe.space/25e9iURIgsa3JiXdcvsZ/media/6ab670bdd1d912a85814bd0f.jpg",
    "https://assets.cdn.filesafe.space/25e9iURIgsa3JiXdcvsZ/media/6ab670be6407f2cbe4d20ab0.jpg",
    "https://assets.cdn.filesafe.space/25e9iURIgsa3JiXdcvsZ/media/6ab670be48b1d5ffbefab648.jpg",
]

REMOVED = r"__(workbook|page|page-tag|page--\w+|mini-list|rings?|reflection-box|preview-label|library-head|library-kicker|library-note|grid|card|media|body|unit|continue|continue-copy|plus|year-tag)\b"

CSS = r"""
/* ---------------- v2 · book mockups of the real covers ---------------- */

/* one book: cover + spine crease on the right (Arabic binding) + page edges */
#m4-practice .m4-practice__book {
  position: relative;
  display: block;
  aspect-ratio: 1 / 1.414;
  border-radius: calc(7px * var(--m4-radius-scale)) 2px 2px calc(7px * var(--m4-radius-scale));
  background: var(--m4-white);
  box-shadow:
    -3px 3px 0 -1px var(--m4-bg-paper),
    -3px 3px 0 0 color-mix(in srgb, var(--m4-primary-deep) 10%, transparent),
    -6px 6px 0 -1px var(--m4-bg-cream),
    -6px 6px 0 0 color-mix(in srgb, var(--m4-primary-deep) 10%, transparent),
    0 22px 38px -10px color-mix(in srgb, var(--m4-primary-deep) 34%, transparent);
  transition: transform calc(.35s * var(--m4-motion-scale)) var(--m4-ease), box-shadow calc(.35s * var(--m4-motion-scale)) var(--m4-ease);
}

#m4-practice .m4-practice__book img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: inherit;
}

#m4-practice .m4-practice__book::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  pointer-events: none;
  background:
    linear-gradient(270deg, rgba(0,0,0,.16) 0, rgba(255,255,255,.5) 2.2%, rgba(0,0,0,.1) 4.6%, rgba(0,0,0,0) 9%),
    linear-gradient(115deg, rgba(255,255,255,0) 40%, rgba(255,255,255,.18) 52%, rgba(255,255,255,0) 64%);
}

/* ---- the fanned stack inside the dark card ---- */
#m4-practice .m4-practice__stack {
  position: relative;
  min-height: 420px;
}

#m4-practice .m4-practice__stack .m4-practice__book {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 44%;
}

#m4-practice .m4-practice__stack .m4-practice__book:nth-child(1) {
  z-index: 3;
  transform: translate(-50%, -54%);
}

#m4-practice .m4-practice__stack .m4-practice__book:nth-child(2) {
  z-index: 2;
  transform: translate(-6%, -48%) rotate(8deg);
}

#m4-practice .m4-practice__stack .m4-practice__book:nth-child(3) {
  z-index: 1;
  transform: translate(-94%, -48%) rotate(-8deg);
}

#m4-practice .m4-practice__stack-badge {
  position: absolute;
  z-index: 4;
  left: 50%;
  bottom: 0;
  transform: translateX(-50%);
  white-space: nowrap;
  padding: 8px 16px;
  border-radius: 999px;
  background: var(--m4-accent);
  color: var(--m4-primary-deep);
  font-size: calc(.8rem * var(--m4-type-scale));
  font-weight: 900;
  box-shadow: 0 10px 24px rgba(0,0,0,.22);
}

/* ---- the library shelf ---- */
#m4-practice .m4-practice__shelf-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px 24px;
  margin-bottom: 30px;
}

#m4-practice .m4-practice__shelf-kicker {
  display: block;
  margin-bottom: 6px;
  color: var(--m4-accent-deep);
  font-size: calc(.72rem * var(--m4-type-scale));
  font-weight: 900;
}

#m4-practice .m4-practice__shelf-head h3 {
  margin: 0;
  color: var(--m4-primary-deep);
  font-size: calc(clamp(1.35rem, 2.3vw, 1.9rem) * var(--m4-heading-scale));
  line-height: 1.45;
  font-weight: 900;
}

#m4-practice .m4-practice__count {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: baseline;
  gap: 8px;
  padding: 10px 16px;
  border-radius: calc(14px * var(--m4-radius-scale));
  border: 1px solid color-mix(in srgb, var(--m4-accent) 40%, transparent);
  background: var(--m4-bg-paper);
  color: var(--m4-text);
  font-size: calc(.8rem * var(--m4-type-scale));
  font-weight: 700;
}

#m4-practice .m4-practice__count strong {
  color: var(--m4-primary);
  font-size: calc(1.5rem * var(--m4-heading-scale));
  line-height: 1;
  font-weight: 900;
}

#m4-practice .m4-practice__shelf {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 34px 30px;
  padding: 0 6px 6px 12px;
}

#m4-practice .m4-practice__more {
  aspect-ratio: 1 / 1.414;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px;
  text-align: center;
  border-radius: calc(10px * var(--m4-radius-scale));
  border: 1.5px dashed color-mix(in srgb, var(--m4-accent) 70%, transparent);
  background: color-mix(in srgb, var(--m4-accent-soft) 18%, var(--m4-bg-paper));
  color: var(--m4-primary-deep);
  font-size: calc(.84rem * var(--m4-type-scale));
  line-height: 1.7;
  font-weight: 800;
}

#m4-practice .m4-practice__more b {
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--m4-primary);
  color: var(--m4-white);
  font-size: 1.5rem;
  line-height: 1;
}

#m4-practice .m4-practice__more small {
  display: block;
  color: var(--m4-text);
  font-size: .86em;
  font-weight: 600;
}

#m4-practice .m4-practice__swipe {
  display: none;
}

@media (hover: hover) {
  #m4-practice .m4-practice__shelf .m4-practice__book:hover {
    transform: translateY(-8px) rotate(-1.5deg);
  }
}

@media (max-width: 920px) {
  #m4-practice .m4-practice__stack {
    min-height: 340px;
  }

  #m4-practice .m4-practice__shelf {
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 28px 22px;
  }
}

/* phones: the fan gets smaller, the shelf becomes a swipeable row */
@media (max-width: 620px) {
  #m4-practice .m4-practice__stack {
    min-height: 290px;
  }

  #m4-practice .m4-practice__stack .m4-practice__book {
    width: 42%;
  }

  #m4-practice .m4-practice__stack-badge {
    font-size: calc(.72rem * var(--m4-type-scale));
  }

  #m4-practice .m4-practice__shelf-head {
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 20px;
  }

  #m4-practice .m4-practice__shelf-head h3 {
    font-size: calc(1.25rem * var(--m4-heading-scale));
  }

  #m4-practice .m4-practice__shelf {
    display: flex;
    gap: 16px;
    margin: 0 calc(-14px * var(--m4-space-scale));
    padding: 4px calc(20px * var(--m4-space-scale)) 26px;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
  }

  #m4-practice .m4-practice__shelf::-webkit-scrollbar {
    display: none;
  }

  #m4-practice .m4-practice__shelf > * {
    flex: 0 0 42%;
    scroll-snap-align: start;
  }

  #m4-practice .m4-practice__more {
    font-size: calc(.74rem * var(--m4-type-scale));
  }

  #m4-practice .m4-practice__swipe {
    display: block;
    margin-top: -8px;
    text-align: center;
    color: var(--m4-text-muted);
    font-size: calc(.74rem * var(--m4-type-scale));
    font-weight: 600;
  }
}
"""


def html(member_note):
    stack = "\n".join(
        f'        <span class="m4-practice__book"><img src="{u}" alt="غلاف ملف من ملفات رياضة الفكر" loading="lazy"></span>'
        for u in COVERS[:3])
    shelf = "\n".join(
        f'      <span class="m4-practice__book"><img src="{u}" alt="غلاف ملف من ملفات رياضة الفكر" loading="lazy"></span>'
        for u in COVERS)
    n = len(COVERS)
    return f"""<section
  id="m4-practice" class="m4-section"
  dir="rtl"
  lang="ar"
  aria-label="رياضة الفكر والملفات التطبيقية"
>

  <div class="m4-practice__wrap">

    <header class="m4-practice__head m4-reveal">
      <div class="m4-practice__kicker">
        تطبيقات رياضة الفكر
      </div>
      <h2>
        المحاضرة تفتح الفكرة...
        وهنا تبدأ المراجعة
      </h2>
      <p>
        ملفات تطبيقية تصاحب محتوى المنهج،
        تمنحك مساحة للتوقف أمام ما تعلمته،
        ومراجعته وربطه بأفكارك وتجاربك وحياتك.
      </p>
    </header>

    <div class="m4-practice__feature m4-reveal">

      <div class="m4-practice__feature-copy">
        <span class="m4-practice__feature-kicker">
          جزء عملي من الرحلة
        </span>
        <h3>
          لا تكتف بأن تفهم الفكرة...
          اكتب، راجع، واربطها بتجربتك
        </h3>
        <p>
          في ملفات رياضة الفكر ستجد مساحات
          للتأمل والكتابة، وأسئلة تساعدك على مراجعة
          ما دار في المحاضرة، إلى جانب خرائط ومفاهيم
          تعينك على رؤية الصورة بصورة أوضح.
        </p>
        <div class="m4-practice__actions">
          <span class="m4-practice__action">توقف وتأمل</span>
          <span class="m4-practice__action">راجع أفكارك</span>
          <span class="m4-practice__action">اكتب واربط</span>
        </div>
      </div>

      <div class="m4-practice__stack" aria-label="أغلفة من ملفات رياضة الفكر">
{stack}
        <span class="m4-practice__stack-badge">{n} ملفات تطبيقية حتى الآن</span>
      </div>

    </div>

    <div class="m4-practice__shelf-head m4-reveal">
      <div>
        <span class="m4-practice__shelf-kicker">
          داخل اشتراكك
        </span>
        <h3>
          مكتبة رياضة الفكر
        </h3>
      </div>
      <div class="m4-practice__count">
        <strong>{n}</strong>
        ملفات تطبيقية · وتزيد مع كل مرحلة
      </div>
    </div>

    <div class="m4-practice__shelf m4-reveal" aria-label="ملفات رياضة الفكر">
{shelf}
      <div class="m4-practice__more">
        <b aria-hidden="true">+</b>
        <span>
          ملفات جديدة
          <small>تضاف مع المحاضرات القادمة خلال العام</small>
        </span>
      </div>
    </div>

    <div class="m4-practice__swipe">
      اسحب لرؤية باقي الملفات ←
    </div>

{member_note}

  </div>

</section>
"""


def _rules(css):
    """split CSS into (prelude, body) at depth 0"""
    out, depth, start, sel, bstart = [], 0, 0, "", 0
    for i, c in enumerate(css):
        if c == "{":
            if depth == 0:
                sel, bstart = css[start:i].strip(), i + 1
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                out.append((sel, css[bstart:i]))
                start = i + 1
    return out


def _filter(css, indent=""):
    parts = []
    for sel, body in _rules(css):
        if sel.startswith("@media") or sel.startswith("@supports"):
            inner = _filter(body, indent + "  ")
            if inner.strip():
                parts.append(f"{indent}{sel} {{\n{inner}\n{indent}}}")
        elif sel.startswith("@keyframes"):
            parts.append(f"{indent}{sel} {{{body}}}")
        else:
            sels = [s.strip() for s in sel.split(",")]
            keep = [s for s in sels if not re.search(REMOVED, s)]
            if keep:
                parts.append(f"{indent}{(',' + chr(10) + indent).join(keep)} {{{body}}}")
    return "\n\n".join(parts)


def apply(path):
    s = path.read_text(encoding="utf-8")
    head = s[:s.index("<style>")]
    css = s[s.index("<style>") + 7:s.index("</style>")]
    body = s[s.index("</style>") + 8:]
    i = body.index('<div class="m4-practice__member-note')
    j = body.rindex("</div>", 0, body.rindex("</section>"))  # closes the wrap
    member = body[i:j].rstrip()
    marker = css[css.rindex("/* self-check"):]
    kept = _filter(css[:css.rindex("/* self-check")])
    new = head + "<style>\n" + kept + "\n" + CSS + "\n" + marker.strip() + "\n</style>\n\n" + html("    " + member)
    path.write_text(new, encoding="utf-8")
    return len(s), len(new)
