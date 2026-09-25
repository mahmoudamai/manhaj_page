"""Bigger explanation text in Block 09 (four axes) and Block 18 (the year) —
the card paragraphs were 12–13px on desktop and ~11px on phones. Layout,
spacing and headings stay as they are; only reading text, lists and tags grow."""

CSS = {
    "09-curriculum.html": r"""
/* ---------------- readability · larger explanation text ---------------- */
/* desktop: the four cards sat at fixed absolute spots, so longer text made
   them overlap. Same picture as a grid — right cards | goal | left cards —
   so each card grows with its text (the rings stay behind). */
@media (min-width: 901px) {
  #m4-curriculum .m4-curriculum__board {
    min-height: 0;
    display: grid;
    grid-template-columns: minmax(0, 1fr) 250px minmax(0, 1fr);
    grid-template-rows: auto auto;
    gap: 34px 46px;
    align-items: stretch;
    padding: 40px;
  }

  #m4-curriculum .m4-curriculum__center {
    position: relative;
    top: auto;
    left: auto;
    grid-column: 2;
    grid-row: 1 / span 2;
    align-self: center;
    transform: none;
  }

  #m4-curriculum .m4-curriculum__center.m4-reveal {
    transform: none;
  }

  #m4-curriculum .m4-curriculum__stage {
    position: relative;
    top: auto;
    right: auto;
    bottom: auto;
    left: auto;
    width: auto;
    transform: none;
  }

  #m4-curriculum .m4-curriculum__stage.m4-reveal {
    transform: none;
  }

  #m4-curriculum .m4-curriculum__stage--one   { grid-column: 1; grid-row: 1; }
  #m4-curriculum .m4-curriculum__stage--two   { grid-column: 3; grid-row: 1; }
  #m4-curriculum .m4-curriculum__stage--three { grid-column: 1; grid-row: 2; }
  #m4-curriculum .m4-curriculum__stage--four  { grid-column: 3; grid-row: 2; }

  /* the short connector lines reach across the gap to the goal */
  #m4-curriculum .m4-curriculum__stage::before {
    width: 46px;
  }

  #m4-curriculum .m4-curriculum__stage--one::before,
  #m4-curriculum .m4-curriculum__stage--three::before {
    left: -46px;
  }

  #m4-curriculum .m4-curriculum__stage--two::before,
  #m4-curriculum .m4-curriculum__stage--four::before {
    right: -46px;
  }
}

#m4-curriculum .m4-curriculum__stage p {
  font-size: calc(.93rem * var(--m4-type-scale));
  line-height: 1.9;
}

#m4-curriculum .m4-curriculum__center p {
  font-size: calc(.9rem * var(--m4-type-scale));
}

#m4-curriculum .m4-curriculum__stage-type {
  font-size: calc(.72rem * var(--m4-type-scale));
}

#m4-curriculum .m4-curriculum__stage h3 {
  font-size: calc(1.16rem * var(--m4-heading-scale));
}

#m4-curriculum .m4-curriculum__tags span {
  font-size: calc(.78rem * var(--m4-type-scale));
}

#m4-curriculum .m4-curriculum__layers span {
  font-size: calc(.9rem * var(--m4-type-scale));
}

#m4-curriculum .m4-curriculum__closing {
  font-size: calc(1.08rem * var(--m4-type-scale));
}

@media (max-width: 600px) {
  #m4-curriculum .m4-curriculum__stage p,
  #m4-curriculum .m4-curriculum__center p {
    font-size: calc(.88rem * var(--m4-type-scale));
    line-height: 1.85;
  }

  #m4-curriculum .m4-curriculum__stage-type {
    font-size: calc(.66rem * var(--m4-type-scale));
  }

  #m4-curriculum .m4-curriculum__stage h3 {
    font-size: calc(1.08rem * var(--m4-heading-scale));
  }

  #m4-curriculum .m4-curriculum__tags span {
    font-size: calc(.74rem * var(--m4-type-scale));
  }

  #m4-curriculum .m4-curriculum__layers span {
    font-size: calc(.8rem * var(--m4-type-scale));
  }

  #m4-curriculum .m4-curriculum__closing {
    font-size: calc(.96rem * var(--m4-type-scale));
  }
}
""",
    "18-year.html": r"""
/* ---------------- readability · larger explanation text ---------------- */
#m4-year .m4-year__card > p {
  font-size: calc(.9rem * var(--m4-type-scale));
  line-height: 1.85;
}

#m4-year li {
  font-size: calc(.86rem * var(--m4-type-scale));
  line-height: 1.7;
}

/* keep the tag off the last list line when the card is at its min height */
#m4-year ul {
  margin-bottom: 16px;
}

#m4-year .m4-year__step {
  font-size: calc(.66rem * var(--m4-type-scale));
}

#m4-year .m4-year__tag {
  font-size: calc(.7rem * var(--m4-type-scale));
}

#m4-year .m4-year__closing p {
  font-size: calc(.92rem * var(--m4-type-scale));
}

@media (max-width: 620px) {
  #m4-year .m4-year__card h3 {
    font-size: calc(1rem * var(--m4-heading-scale));
  }

  #m4-year .m4-year__card > p {
    font-size: calc(.86rem * var(--m4-type-scale));
  }

  #m4-year li {
    font-size: calc(.82rem * var(--m4-type-scale));
  }

  #m4-year .m4-year__tag {
    font-size: calc(.66rem * var(--m4-type-scale));
  }

  #m4-year .m4-year__closing p {
    font-size: calc(.84rem * var(--m4-type-scale));
  }
}
""",
}


def apply(blocks):
    for name, css in CSS.items():
        path = blocks / name
        s = path.read_text(encoding="utf-8")
        m = s.rfind("/* self-check")
        if m < 0:
            m = s.index("</style>")
        s = s[:m] + css.strip() + "\n\n" + s[m:]
        path.write_text(s, encoding="utf-8")
