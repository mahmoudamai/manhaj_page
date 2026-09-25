#!/usr/bin/env python3
"""
Phase-1 refactor of the production GHL page (legacy/*.html → refactor/).

    python3 tools/refactor_legacy.py

What it does, block by block (content, order and links are never touched):
  · strips every per-block <link>/<style>/<script>
  · renames ids/classes to one system:  #m4-<section>  ·  .m4-<section>__<element>
  · moves all section CSS into ONE main stylesheet, where
      - colours → theme tokens (exact, or colour-mix of two tokens, error ≤ 4/255)
      - font-family → --m4-font-primary / --m4-font-display
      - font-size × --m4-type-scale, root padding × --m4-space-scale,
        radius × --m4-radius-scale, durations × --m4-motion-scale
      - scroll-reveal "hidden until JS" states removed (content visible by default)
      - dead rules (classes that exist nowhere) dropped, keyframes namespaced
  · rewrites all per-block JS as one shared script (00B)
"""
import html as htmllib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "legacy"
OUT = ROOT / "refactor"

# ---------------------------------------------------------------------------
# block order + naming
# ---------------------------------------------------------------------------
BLOCKS = [
    # file,      new slug,        old root id,               GHL position label
    ("s01b01", "hero",           "mhhm-videoIntro",        "Section 01 · Block 01 — Hero"),
    ("s01b04", "hero-stats",     "mhhm-heroStats",         "Section 01 · Block 04 — Course info"),
    ("s01b06", "hero-trust",     "mhhm-purchaseTrust",     "Section 01 · Block 06 — Trust"),
    ("s02b01", "kareem-intro",   "mhhm-mini-kareem",       "Section 02 · Block 01 — Kareem intro"),
    ("s03b00", "pain",           "mhhm-pain",              "Section 03 — Pain"),
    ("s04b00", "faqah",          "mhhm-faqah",             "Section 04 — سر الفاقة"),
    ("s05b00", "member-story",   "mhhm-rasha-moment",      "Section 05 — Member comment"),
    ("s06b00", "method",         "mhhm-methodology",       "Section 06 — How it was built"),
    ("s07b00", "curriculum",     "mhhm-curriculum",        "Section 07 — The four axes"),
    ("s08b00", "yusuf",          "mhhm-yusuf",             "Section 08 — Surat Yusuf"),
    ("s09b00", "lectures",       "mhhm-lectures",          "Section 09 — Lectures so far"),
    ("s10b00", "lecture-notes",  "mhhm-content-proofs",    "Section 10 — Attendee comments"),
    ("s11b00", "practice",       "mhhm-practice",          "Section 11 — رياضة الفكر"),
    ("s12b00", "live",           "mhhm-live",              "Section 12 — Live sessions"),
    ("s13b00", "telegram",       "mhhm-telegram",          "Section 13 — Telegram community"),
    ("s14b00", "wa-reviews",     "mhhm-wa-masonry",        "Section 14 — WhatsApp screenshots"),
    ("s15b00", "fit",            "mhhm-fit",               "Section 15 — Is it for you"),
    ("s16b00", "year",           "mhhm-yearJourney",       "Section 16 — The year journey"),
    ("s17b00", "testimonials",   "mhhm-main-testimonials", "Section 17 — Written testimonials"),
    ("s18b00", "kareem",         "mhhm-kareem",            "Section 18 — Kareem full profile"),
    ("s19b00", "offer",          "mhhm-offer",             "Section 19 — Price & offer"),
    ("s20b00", "guarantee",      "mhhm-guarantee",         "Section 20 — 7-day guarantee"),
    ("s21b00", "faq",            "mhhm-faq",               "Section 21 — FAQ"),
    ("s22b00", "sticky",         None,                     "Section 22 — Sticky bar (inside the fixed GHL section)"),
    ("s23b00", "footer",         "mhhm-footer",            "Section 23 — Footer"),
]
OLD_IDS = {old: slug for _, slug, old, _ in BLOCKS if old}
OLD_IDS["mhhm-hero"] = "hero"            # referenced by the old sticky script

STATE = {"visible": None, "mhhm-visible": None,          # reveal → removed
         "mhhm-open": "is-open", "mhh-sticky-visible": "is-visible", "is-visible": "is-visible"}
STICKY_HOST_OLD = "mhh-sticky-cta"                          # class set on the GHL section itself
STICKY_HOST = "m4-sticky-host"

# elements the old scripts revealed (querySelector lists), per block
REVEAL_TARGETS = {
    "s01b01": [".reveal"], "s01b04": [".item"], "s01b06": [".wrap"],
    "s02b01": [".mhhm-photoReveal", ".mhhm-reveal"], "s03b00": [".mhhm-card", ".mhhm-visual"],
    "s04b00": [".mhhm-reveal"], "s05b00": [".mhhm-context", ".mhhm-message"],
    "s06b00": [".mhhm-item"], "s07b00": [".mhhm-head", ".mhhm-center", ".mhhm-stage", ".mhhm-board"],
    "s08b00": [".mhhm-content", ".mhhm-divider", ".mhhm-visual"],
    "s09b00": [".mhhm-head", ".mhhm-groupHead", ".mhhm-card", ".mhhm-continue"],
    "s10b00": [".mhhm-head", ".mhhm-reaction"],
    "s11b00": [".mhhm-head", ".mhhm-feature", ".mhhm-libraryHead", ".mhhm-card", ".mhhm-continue", ".mhhm-memberNote"],
    "s12b00": [".mhhm-head", ".mhhm-values", ".mhhm-card", ".mhhm-continue"],
    "s13b00": [".mhhm-head", ".mhhm-experience", ".mhhm-closing"],
    "s14b00": [".mhhm-head", ".mhhm-proofLabel", ".mhhm-card", ".mhhm-closing"],
    "s15b00": [".mhhm-introBlock", ".mhhm-visual", ".mhhm-lowerContent"],
    "s16b00": [".mhhm-head", ".mhhm-yearLabel", ".mhhm-card", ".mhhm-closing"],
    "s17b00": [".mhhm-head", ".mhhm-card", ".mhhm-closing"],
    "s18b00": [".mhhm-head", ".mhhm-profile", ".mhhm-stats", ".mhhm-event"],
    "s19b00": [".mhhm-head", ".mhhm-grid", ".mhhm-bottom"],
    "s20b00": [".mhhm-head", ".mhhm-card", ".mhhm-bottom"],
    "s21b00": [".mhhm-head", ".mhhm-list", ".mhhm-bottom"],
}
# the old ".x.visible" rules that were written as a bare ".visible" on the section
BARE_VISIBLE = {"s02b01": [".mhhm-photoReveal", ".mhhm-reveal"], "s05b00": [".mhhm-context", ".mhhm-message"]}

# editorial (display) font: quotes, testimonials and emotional one-liners
DISPLAY_SELECTORS = [
    r"#m4-member-story \.m4-member-story__message\b",
    r"#m4-lecture-notes \.m4-lecture-notes__reaction p\b",
    r"#m4-testimonials \.m4-testimonials__card p\b",
    r"#m4-practice \.m4-practice__member-note p\b",
    r"#m4-faqah \.m4-faqah__term\b",
    r"#m4-kareem \.m4-kareem__philosophy\b",
]

# ---------------------------------------------------------------------------
# theme tokens (exact values taken from the production CSS)
# ---------------------------------------------------------------------------
TOKENS = [
    ("primary", "#1E5960"), ("primary-deep", "#123C42"), ("primary-alt", "#294E63"), ("ink", "#354859"),
    ("secondary", "#A7BCA6"), ("secondary-soft", "#DDE8DC"), ("highlight", "#8EC9C4"), ("highlight-soft", "#A9DED8"),
    ("accent", "#D3B267"), ("accent-soft", "#E9D8A8"), ("accent-deep", "#90794C"), ("olive", "#3C5141"),
    ("bg-paper", "#FFFDF8"), ("bg-ivory", "#FBF7EF"), ("bg-cream", "#F7F3EA"), ("bg-cloud", "#EEF3F1"),
    ("text", "#5D6A70"), ("text-muted", "#748086"),
    ("white", "#FFFFFF"), ("black", "#000000"),
]
UTILITY = [("live", "#FF3B30"), ("alert", "#E75C4D"), ("telegram", "#2AABEE"), ("whatsapp", "#25D366")]
MIX_EXCLUDE = {"white", "black"}


def hex_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


TOK_RGB = [(n, hex_rgb(h)) for n, h in TOKENS + UTILITY]
_color_cache = {}
color_stats = {"exact": 0, "mix": 0, "literal": 0}
literal_left = set()


def fmt_pct(x):
    s = f"{x * 100:.1f}".rstrip("0").rstrip(".")
    return s + "%"


def color_expr(rgb):
    """rgb tuple → CSS expression built from tokens."""
    if rgb in _color_cache:
        return _color_cache[rgb]
    best = None
    for n, t in TOK_RGB:
        d = max(abs(a - b) for a, b in zip(rgb, t))
        if best is None or d < best[0]:
            best = (d, f"var(--m4-{n})")
    if best[0] <= 2:
        color_stats["exact"] += 1
        _color_cache[rgb] = best[1]
        return best[1]
    util = set(dict(UTILITY))
    brand = TOK_RGB
    cand = None
    for i, (na, ta) in enumerate(brand):
        for nb, tb in brand[i + 1:]:
            if na in MIX_EXCLUDE and nb in MIX_EXCLUDE:
                continue
            # utility colours only mix with neutrals or each other
            if (na in util) != (nb in util) and not ({na, nb} & MIX_EXCLUDE):
                continue
            # best p for A*p + B*(1-p) per least squares
            num = sum((c - b) * (a - b) for c, a, b in zip(rgb, ta, tb))
            den = sum((a - b) ** 2 for a, b in zip(ta, tb)) or 1
            p = min(1, max(0, num / den))
            p = round(p * 200) / 200
            mix = [a * p + b * (1 - p) for a, b in zip(ta, tb)]
            err = max(abs(c - m) for c, m in zip(rgb, mix))
            if cand is None or err < cand[0]:
                cand = (err, na, nb, p)
    if cand and cand[0] <= 7:
        err, na, nb, p = cand
        if p >= 0.5:
            e = f"color-mix(in srgb, var(--m4-{na}) {fmt_pct(p)}, var(--m4-{nb}))"
        else:
            e = f"color-mix(in srgb, var(--m4-{nb}) {fmt_pct(1 - p)}, var(--m4-{na}))"
        color_stats["mix"] += 1
        _color_cache[rgb] = e
        return e
    color_stats["literal"] += 1
    lit = "#%02X%02X%02X" % rgb
    literal_left.add(lit)
    _color_cache[rgb] = lit
    return lit


def with_alpha(expr, a):
    if a >= 0.9999:
        return expr
    return f"color-mix(in srgb, {expr} {fmt_pct(a)}, transparent)"


NEUTRAL_ALPHA = {(255, 255, 255), (0, 0, 0)}


def map_colors(value):
    def rep_hex(m):
        return color_expr(hex_rgb(m.group(0)))

    def rep_rgb(m):
        parts = [p.strip() for p in m.group(1).split(",")]
        rgb = tuple(int(float(p)) for p in parts[:3])
        a = float(parts[3]) if len(parts) > 3 else 1.0
        if rgb in NEUTRAL_ALPHA and a < 1:
            return m.group(0).replace(" ", "")      # plain white/black glass stays literal
        return with_alpha(color_expr(rgb), a)

    value = re.sub(r"rgba?\(([^()]*)\)", rep_rgb, value)
    value = re.sub(r"#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b(?![0-9A-Fa-f])", rep_hex, value)
    return value


# ---------------------------------------------------------------------------
# CSS parsing
# ---------------------------------------------------------------------------
def parse_css(text):
    """→ list of nodes: {"t":"rule","sel","decls"} | {"t":"at","prelude","body"(nodes)} | {"t":"raw","prelude","raw"}"""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    nodes, i, n = [], 0, len(text)
    while i < n:
        j = text.find("{", i)
        if j < 0:
            break
        prelude = text[i:j].strip()
        depth, k = 1, j + 1
        while k < n and depth:
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
            k += 1
        body = text[j + 1:k - 1]
        if prelude.startswith("@keyframes") or prelude.startswith("@-webkit-keyframes") or prelude.startswith("@font-face"):
            nodes.append({"t": "raw", "prelude": prelude, "raw": body})
        elif prelude.startswith("@"):
            nodes.append({"t": "at", "prelude": prelude, "body": parse_css(body)})
        else:
            nodes.append({"t": "rule", "sel": prelude, "decls": parse_decls(body)})
        i = k
    return nodes


def parse_decls(body):
    out, buf, depth = [], "", 0
    for ch in body:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == ";" and depth == 0:
            if buf.strip():
                out.append(buf.strip())
            buf = ""
        else:
            buf += ch
    if buf.strip():
        out.append(buf.strip())
    decls = []
    for d in out:
        if ":" not in d:
            continue
        p, v = d.split(":", 1)
        decls.append([p.strip().lower() if not p.strip().startswith("--") else p.strip(), re.sub(r"\s+", " ", v.strip())])
    return decls


def norm_sel(s):
    return re.sub(r"\s+", " ", s).strip()


def camel_kebab(s):
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", s)
    return s.lower()


def class_new(slug, name):
    if name.startswith("m4-"):
        return name
    if name in STATE:
        return STATE[name]
    if name == STICKY_HOST_OLD:
        return STICKY_HOST
    base = re.sub(r"^(mhhm-|mhh-)", "", name)
    if slug == "sticky":
        base = re.sub(r"^sticky-", "", base)
    parts = base.split("--")
    base = "--".join(camel_kebab(p) for p in parts)
    return f"m4-{slug}__{base}"


def map_selector(sel, slug):
    sel = norm_sel(sel)

    def rep_id(m):
        old = m.group(1)
        return "#m4-" + OLD_IDS[old] if old in OLD_IDS else m.group(0)

    sel = re.sub(r"#([A-Za-z][\w-]*)", rep_id, sel)
    sel = sel.replace("." + STICKY_HOST_OLD, "\u00a7HOST\u00a7")
    sel = re.sub(r"\.(-?[A-Za-z_][\w-]*)", lambda m: "." + class_new(slug, m.group(1)), sel)
    sel = sel.replace("\u00a7HOST\u00a7", ":is(.m4-sticky-host, .mhh-sticky-cta)")
    return sel


# ---------------------------------------------------------------------------
# declaration transforms
# ---------------------------------------------------------------------------
HEADING_RX = re.compile(r"(^|[\s>+~,(])h[1-3]\b|title|headline", re.I)


def max_px(v):
    nums = [float(x) for x in re.findall(r"(\d*\.?\d+)px", v)]
    rems = [float(x) * 16 for x in re.findall(r"(\d*\.?\d+)rem", v)]
    return max(nums + rems) if nums + rems else 0


def scale_len(v, var):
    return re.sub(r"(?<![\w.-])(\d*\.?\d+)px\b",
                  lambda m: m.group(0) if float(m.group(1)) == 0 else f"calc({m.group(0)} * var({var}))", v)


def transform_decl(prop, val, sel, slug, is_root, local_vars, keep_important):
    important = "!important" in val
    val = val.replace("!important", "").strip()

    # local custom properties → inline them (they were per-section copies of the theme)
    def rep_var(m):
        name = m.group(1)
        if name in local_vars:
            return local_vars[name]
        return m.group(0)

    val = re.sub(r"var\((--[\w-]+)\)", rep_var, val)
    val = map_colors(val)

    if prop == "font-family":
        if any(re.search(rx, sel) for rx in DISPLAY_SELECTORS):
            val = "var(--m4-font-display)"
        elif HEADING_RX.search(sel):
            val = "var(--m4-font-heading)"
        else:
            val = "var(--m4-font-primary)"
    elif prop == "font-size" and re.search(r"\d", val) and not re.fullmatch(r"[\d.]+(em|%)", val):
        scale = "--m4-heading-scale" if (HEADING_RX.search(sel) or max_px(val) >= 26) else "--m4-type-scale"
        val = f"calc({val} * var({scale}))"
    elif prop == "border-radius" or prop.startswith("border-") and prop.endswith("-radius"):
        if "/" not in val:
            val = scale_len(val, "--m4-radius-scale")
    elif prop in ("padding", "padding-top", "padding-bottom", "padding-block") and is_root:
        val = scale_len(val, "--m4-space-scale")
    elif prop in ("transition", "transition-duration", "transition-delay"):
        val = re.sub(r"cubic-bezier\([^)]*\)|\bease-in-out\b|\bease-out\b|\bease\b", "var(--m4-ease)", val)
        val = re.sub(r"(?<![\w.-])(\d*\.?\d+)(ms|s)\b",
                     lambda m: m.group(0) if float(m.group(1)) == 0 else f"calc({m.group(0)} * var(--m4-motion-scale))", val)
    elif prop in ("animation", "animation-duration"):
        val = re.sub(r"(?<![\w.-])(\d*\.?\d+)(ms|s)\b",
                     lambda m: m.group(0) if float(m.group(1)) == 0 else f"calc({m.group(0)} * var(--m4-motion-scale))", val)
    if important and keep_important:
        val += " !important"
    return prop, val


# ---------------------------------------------------------------------------
# per-block processing
# ---------------------------------------------------------------------------
def split_block(src):
    styles = re.findall(r"<style[^>]*>(.*?)</style>", src, flags=re.S)
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", src, flags=re.S)
    body = re.sub(r"<style[^>]*>.*?</style>|<script[^>]*>.*?</script>|<link[^>]*>", "", src, flags=re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    return "\n".join(styles), scripts, body.strip()


def collect_classes(html):
    s = set()
    for c in re.findall(r'class="([^"]*)"', html):
        s.update(c.split())
    return s


def strip_state(sel):
    """reveal-state class → .m4-reveal (always present on revealed elements), so the
    old "final" rules keep their exact specificity and simply always apply"""
    new = re.sub(r"\.(mhhm-visible|visible)\b", ".m4-reveal", sel)
    return norm_sel(new), new != sel


def process_block(fname, slug, old_id, label):
    src = (SRC / f"{fname}.html").read_text(encoding="utf-8")
    css_text, scripts, body = split_block(src)
    nodes = parse_css(css_text)
    html_classes = collect_classes(body)

    # local vars defined in this block (theme copies)
    local_vars = {}

    def gather_vars(nl):
        for nd in nl:
            if nd["t"] == "rule":
                for p, v in nd["decls"]:
                    if p.startswith("--"):
                        local_vars[p] = map_colors(v)
            elif nd["t"] == "at":
                gather_vars(nd["body"])

    gather_vars(nodes)
    # only colour-valued locals are inlined; anything else stays local
    local_vars = {k: v for k, v in local_vars.items() if "var(--m4-" in v or "color-mix" in v or v.startswith("#")}

    # 1) reveal states: collect state rules → final-state rules; remember props per base selector
    reveal_props = {}   # (context, stripped legacy selector) → set(props)

    def reveal_pass(nl, ctx):
        out = []
        for nd in nl:
            if nd["t"] == "at":
                nd["body"] = reveal_pass(nd["body"], ctx + (nd["prelude"],))
                out.append(nd)
                continue
            if nd["t"] != "rule":
                out.append(nd)
                continue
            new_parts = []
            for part in nd["sel"].split(","):
                part = norm_sel(part)
                stripped, had = strip_state(part)
                if not had:
                    new_parts.append(part)
                    continue
                if fname in BARE_VISIBLE and stripped == f"#{old_id}":
                    new_parts.append(f"#{old_id} .m4-reveal")
                    for t in BARE_VISIBLE[fname]:
                        reveal_props.setdefault(f"#{old_id} {t}", set()).update(p for p, _ in nd["decls"])
                    continue
                new_parts.append(stripped)
                bare = norm_sel(re.sub(r"\.m4-reveal\b", "", stripped))
                if ":" not in bare.split(" ")[-1]:
                    reveal_props.setdefault(bare, set()).update(p for p, _ in nd["decls"])
            nd["sel"] = ", ".join(dict.fromkeys(new_parts))
            out.append(nd)
        return out

    # mark which rules were state rules before stripping
    def mark(nl):
        for nd in nl:
            if nd["t"] == "rule":
                nd["_was_state"] = bool(re.search(r"\.(mhhm-visible|visible)\b", nd["sel"]))
            elif nd["t"] == "at":
                mark(nd["body"])

    mark(nodes)
    nodes = reveal_pass(nodes, ())

    # 2) remove hidden-state props from base rules (same selector, not a state rule)
    HIDE_PROPS = {"opacity", "transform", "width", "filter", "clip-path", "visibility"}

    def unhide(nl):
        for nd in nl:
            if nd["t"] == "at":
                unhide(nd["body"])
            elif nd["t"] == "rule" and not nd["_was_state"]:
                sels = [norm_sel(p) for p in nd["sel"].split(",")]
                props = set()
                for s in sels:
                    props |= reveal_props.get(s, set())
                props &= HIDE_PROPS
                if props and len(sels) == 1:
                    nd["decls"] = [d for d in nd["decls"] if d[0] not in props]
                elif props:
                    # grouped selector: only drop if every member is a reveal target
                    if all(s in reveal_props for s in sels):
                        nd["decls"] = [d for d in nd["decls"] if d[0] not in props]

    unhide(nodes)

    # 3) dead-rule removal (classes that exist nowhere in this block's html and are not states)
    known = html_classes | set(STATE) | {STICKY_HOST_OLD, "m4-reveal"}

    def alive(sel):
        for part in sel.split(","):
            cls = re.findall(r"\.(-?[A-Za-z_][\w-]*)", part)
            if all(c in known for c in cls):
                return True
        return False

    def prune(nl):
        out = []
        for nd in nl:
            if nd["t"] == "rule":
                parts = [p for p in nd["sel"].split(",") if alive(p)]
                if not parts or not nd["decls"]:
                    continue
                nd["sel"] = ", ".join(norm_sel(p) for p in parts)
                out.append(nd)
            elif nd["t"] == "at":
                nd["body"] = prune(nd["body"])
                if nd["body"]:
                    out.append(nd)
            else:
                out.append(nd)
        return out

    nodes = prune(nodes)

    # 4) keyframes namespacing
    kf_map = {}
    for nd in nodes:
        if nd["t"] == "raw" and "keyframes" in nd["prelude"]:
            old = nd["prelude"].split()[-1]
            kf_map[old] = f"m4-{slug}-{camel_kebab(re.sub(r'^(mhhm|mhh)', '', old)).strip('-')}"

    # 5) selector + declaration transforms
    keep_imp = slug == "sticky"

    def xform(nl):
        out = []
        for nd in nl:
            if nd["t"] == "rule":
                sel = ", ".join(map_selector(p, slug) for p in nd["sel"].split(","))
                is_root = sel == f"#m4-{slug}"
                decls = []
                for p, v in nd["decls"]:
                    if p.startswith("--") and p in local_vars:
                        continue
                    for o, nn in kf_map.items():
                        v = re.sub(rf"\b{re.escape(o)}\b", nn, v)
                    p2, v2 = transform_decl(p, v, sel, slug, is_root, local_vars, keep_imp or (is_root and p in ("width", "margin-left", "margin-right", "font-family")))
                    decls.append((p2, v2))
                if decls:
                    out.append({"t": "rule", "sel": sel, "decls": decls})
            elif nd["t"] == "at":
                body = xform(nd["body"])
                if body:
                    out.append({"t": "at", "prelude": nd["prelude"].replace("prefers-reduced-motion:reduce", "prefers-reduced-motion: reduce"), "body": body})
            else:
                pre = nd["prelude"]
                for o, nn in kf_map.items():
                    pre = re.sub(rf"\b{re.escape(o)}\b", nn, pre)
                raw = map_colors(re.sub(r"\s+", " ", nd["raw"]))
                out.append({"t": "raw", "prelude": pre, "raw": raw})
        return out

    nodes = xform(nodes)

    # CTA buttons read the central CTA tokens
    def cta(nl):
        for nd in nl:
            if nd["t"] == "at":
                cta(nd["body"])
            elif nd["t"] == "rule" and re.search(r"m4-offer__cta\b|m4-sticky__checkout-btn\b", nd["sel"]):
                nd["decls"] = [(p, v.replace("var(--m4-live)", "var(--m4-cta-bg)")
                                 .replace("var(--m4-white)", "var(--m4-cta-text)") if (p in ("color", "fill", "stroke") or p.startswith("background") or p.startswith("border") or p in ("box-shadow", "outline")) else v)
                               for p, v in nd["decls"]]

    cta(nodes)

    # 6) html
    def rep_class_attr(m):
        classes = [class_new(slug, c) for c in m.group(1).split()]
        classes = [c for c in classes if c]
        return f'class="{" ".join(classes)}"'

    body = re.sub(r'class="([^"]*)"', rep_class_attr, body)
    body = re.sub(r'id="([^"]+)"', lambda m: f'id="m4-{OLD_IDS[m.group(1)]}"' if m.group(1) in OLD_IDS else m.group(0), body)
    body = re.sub(r'href="#([^"]+)"', lambda m: f'href="#m4-{OLD_IDS[m.group(1)]}"' if m.group(1) in OLD_IDS else m.group(0), body)

    # reveal hooks
    targets = [class_new(slug, t.lstrip(".")) for t in REVEAL_TARGETS.get(fname, [])]

    def add_reveal(m):
        cl = m.group(1).split()
        if any(t in cl for t in targets) and "m4-reveal" not in cl:
            cl.append("m4-reveal")
        return f'class="{" ".join(cl)}"'

    body = re.sub(r'class="([^"]*)"', add_reveal, body)

    # section root gets the shared section primitive
    if old_id:
        body = re.sub(rf'(<(?:section|footer)[^>]*id="m4-{slug}"[^>]*?)(\s*class="([^"]*)")?(\s*[^>]*>)',
                      lambda m: m.group(0) if m.group(2) else m.group(1) + ' class="m4-section"' + m.group(4), body, count=1)

    return nodes, body, scripts


# ---------------------------------------------------------------------------
# serialisation
# ---------------------------------------------------------------------------
def dump(nodes, indent=""):
    out = []
    for nd in nodes:
        if nd["t"] == "rule":
            sels = [s.strip() for s in nd["sel"].split(",")]
            head = (",\n" + indent).join(sels)
            decls = "\n".join(f"{indent}  {p}: {v};" for p, v in nd["decls"])
            out.append(f"{indent}{head} {{\n{decls}\n{indent}}}")
        elif nd["t"] == "at":
            out.append(f"{indent}{nd['prelude']} {{\n{dump(nd['body'], indent + '  ')}\n{indent}}}")
        else:
            raw = re.sub(r"\s*\}\s*", " }\n" + indent + "  ", nd["raw"]).strip()
            out.append(f"{indent}{nd['prelude']} {{\n{indent}  {raw}\n{indent}}}")
    return "\n\n".join(out)


def pretty_html(body):
    lines = [ln.rstrip() for ln in body.splitlines()]
    out, blank = [], 0
    for ln in lines:
        if not ln.strip():
            blank += 1
            if blank > 1:
                continue
        else:
            blank = 0
        out.append(ln)
    return "\n".join(out).strip() + "\n"


def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};>])\s*", r"\1", css)
    return css.replace(";}", "}").strip()


FONTS_LINK = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
              '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
              '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=Amiri:wght@400;700&family=Tajawal:wght@400;500;700;800;900&family=Alexandria:wght@400;500;600;700;800&family=Readex+Pro:wght@400;500;600;700&family=Cairo:wght@400;500;600;700;800&family=Almarai:wght@400;700;800&family=Markazi+Text:wght@400;500;600;700&family=Noto+Naskh+Arabic:wght@400;500;600;700&display=swap">\n')
FONTS_IMPORT = ('@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=Amiri:wght@400;700&family=Tajawal:wght@400;500;700;800;900&family=Alexandria:wght@400;500;600;700;800&family=Readex+Pro:wght@400;500;600;700&family=Cairo:wght@400;500;600;700;800&family=Almarai:wght@400;700;800&family=Markazi+Text:wght@400;500;600;700&family=Noto+Naskh+Arabic:wght@400;500;600;700&display=swap");\n'
                '/* fonts are only downloaded when a font is actually used */\n\n')


def main():
    blocks = OUT / "blocks"
    blocks.mkdir(parents=True, exist_ok=True)
    for f in list(blocks.rglob("*")):
        if f.is_file():
            f.unlink()
    for d in sorted(blocks.rglob("*"), reverse=True):
        if d.is_dir():
            d.rmdir()

    base = (ROOT / "tools" / "m4-base.css").read_text(encoding="utf-8")
    extra = (ROOT / "tools" / "m4-overrides.css").read_text(encoding="utf-8")

    # ---- Block 00: theme + shared system (small: fits any GHL field) ----
    import importlib.util
    spec = importlib.util.spec_from_file_location("m4themes", ROOT / "tools" / "m4-themes.py")
    tm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tm)
    theme_css = ["/* =====================================================================\n"
                 "   7 · READY-MADE THEMES\n"
                 "   Preview on the live page:  add ?m4-theme=emerald (sage, indigo, clay, olive)\n"
                 "   Make one permanent: paste its file from /themes at the END of Custom CSS.\n"
                 "   ===================================================================== */"]
    tdir = OUT / "themes"
    tdir.mkdir(exist_ok=True)
    for f in tdir.glob("*.css"):
        f.unlink()
    for n, (name, (desc, vals)) in enumerate(tm.THEMES.items(), 1):
        decl = "".join(f"--m4-{k}:{v};" for k, v in vals.items())
        theme_css.append(f':root[data-m4-theme="{name}"]{{{decl}}}')
        pretty = "\n".join(f"  --m4-{k}: {v};" for k, v in vals.items())
        (tdir / f"{n}-{name}.css").write_text(
            f"/* M4 THEME · {desc}\n   Paste at the very END of page Settings → Custom CSS (after Block 00).\n"
            f"   To switch theme: replace this block. To go back to the original: delete it. */\n"
            f":root {{\n{pretty}\n}}\n", encoding="utf-8")
    theme = (":root { --m4-parts: 1; }\n\n" + base.rstrip() + "\n\n" + extra.rstrip() + "\n\n" + "\n".join(theme_css) +
             "\n\n/* end of Block 00 */\n:root { --m4-part-1: 1; }\n")
    theme = theme.replace("""   4 · SECTIONS
   Each block below is scoped to its own #m4-<section> id, so nothing
   leaks into GHL forms, menus or checkout elements.""", """   4 · SECTIONS
   Each section's own styles live inside its GHL block (a <style> at the
   top of the block), scoped to its #m4-<section> id so nothing leaks into
   GHL forms, menus or checkout. They read the tokens above, so the theme
   is still edited only here.""")
    head00 = ("<!-- =====================================================================\n"
              "     M4 · BLOCK 00 — THEME + SHARED SYSTEM (fonts, tokens, primitives, motion)\n"
              "     ===================================================================== -->\n")
    (blocks / "00-theme.css").write_text(
        FONTS_IMPORT + "/* M4 · BLOCK 00 — for GHL → page Settings → Custom CSS (pure CSS) */\n\n" + theme, encoding="utf-8")
    (blocks / "00-theme.html").write_text(head00 + FONTS_LINK + "<style>\n" + theme + "</style>\n", encoding="utf-8")

    js = (ROOT / "tools" / "m4-shared.js").read_text(encoding="utf-8")
    (blocks / "00B-shared-js.html").write_text(
        "<!-- M4 · BLOCK 00B — SHARED JAVASCRIPT. Put it in Settings → Tracking Code → Footer or Head,\n"
        "     or in the LAST Code Element on the page. -->\n<script>\n" + js + "</script>\n", encoding="utf-8")

    # ---- section blocks: own <style> + HTML ----
    all_css = [base]
    sizes = []
    for i, (fname, slug, old_id, label) in enumerate(BLOCKS, 1):
        nodes, body, _ = process_block(fname, slug, old_id, label)
        css = dump(nodes)
        if old_id:
            css += f"\n\n/* self-check: this block is the current version */\n#m4-{slug} {{\n  --m4-styled: {i};\n}}"
        all_css.append(f"/* ===== {i:02d} · {label} · #m4-{slug} ===== */\n\n{css}\n")
        header = (f"<!-- =====================================================================\n"
                  f"     M4 · BLOCK {i:02d} — {label}\n"
                  f"     Section styles are scoped to #m4-{slug}. Colours, fonts, sizes and\n"
                  f"     speeds come from Block 00 — edit the theme there, not here.\n"
                  f"     ===================================================================== -->\n")
        if slug == "sticky":
            header += ("<!-- The fixed GHL section that holds this block must have the CSS class\n"
                       "     \"m4-sticky-host\" (the old class \"mhh-sticky-cta\" still works too). -->\n")
        out = header + "<style>\n" + css + "\n</style>\n\n" + pretty_html(body)
        (blocks / f"{i:02d}-{slug}.html").write_text(out, encoding="utf-8")
        sizes.append((f"{i:02d}-{slug}", len(out)))
    # ---- block 13 v2: real cover mockups (tools/m4_practice_v2.py) ----
    spec2 = importlib.util.spec_from_file_location("m4practice", ROOT / "tools" / "m4_practice_v2.py")
    pv2 = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(pv2)
    print("practice v2:", pv2.apply(blocks / "13-practice.html"))

    # ---- block 03 v2: discount + saving under the hero button (tools/m4_hero_trust_v2.py) ----
    spec3 = importlib.util.spec_from_file_location("m4herotrust", ROOT / "tools" / "m4_hero_trust_v2.py")
    ht2 = importlib.util.module_from_spec(spec3)
    spec3.loader.exec_module(ht2)
    ht2.apply(blocks / "03-hero-trust.html")

    # ---- block 06 v2: new Faqah intro (tools/m4_faqah_v2.py) ----
    spec6 = importlib.util.spec_from_file_location("m4faqah", ROOT / "tools" / "m4_faqah_v2.py")
    fq2 = importlib.util.module_from_spec(spec6)
    spec6.loader.exec_module(fq2)
    fq2.apply(blocks / "06-faqah.html")

    # ---- block 09 v2: «محاور المنهج» (Block 08 merged in, so 08 is dropped) ----
    spec9 = importlib.util.spec_from_file_location("m4curr", ROOT / "tools" / "m4_curriculum_v2.py")
    cu2 = importlib.util.module_from_spec(spec9)
    spec9.loader.exec_module(cu2)
    cu2.apply(blocks / "09-curriculum.html")
    (blocks / "08-method.html").unlink()

    # ---- hand-written new blocks (05-pain v2 replaces the generated one) (not from the legacy page), e.g. 16b-offer-early ----
    for f in sorted((ROOT / "tools" / "new-blocks").glob("*.html")):
        (blocks / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
    all_css.append(extra)
    (OUT / "main.css").write_text("\n\n".join(all_css), encoding="utf-8")

    # ---- preview (GHL elements shown as placeholders in their real positions) ----
    def ph(name):
        return (f'<div style="max-width:900px;margin:0 auto;padding:18px;text-align:center;border:2px dashed #bbb;'
                f'font:14px sans-serif;color:#777;background:#f3f3f3">GHL element: {name}</div>')
    order = [("01", None), ("GHL", "video (block 02) + video style (03)"), ("02", None), ("GHL", "button (block 05)"),
             ("03", None), ("04", None), ("GHL", "logos marquee"), ("05", None), ("06", None), ("07", None), ("16", None), ("09", None), ("18", None),
             ("10", None), ("10b", None), ("11", None), ("12", None), ("13", None), ("14", None), ("15", None),
             ("17", None), ("19", None), ("20", None), ("21", None), ("22", None), ("23", None), ("25", None)]
    parts = []
    files = {f.name.split("-")[0]: f for f in blocks.glob("[0-9][0-9]*-*.html")}
    for key, label in order:
        parts.append(ph(label) if key == "GHL" else files[key].read_text(encoding="utf-8"))
    sticky = files["24"].read_text(encoding="utf-8")
    page = ("<!doctype html>\n<html lang=\"ar\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<title>M4 preview</title>\n"
            "<style>body{margin:0}</style>\n"
            + (blocks / "00-theme.html").read_text(encoding="utf-8")
            + (blocks / "00B-shared-js.html").read_text(encoding="utf-8")
            + "</head>\n<body>\n" + "\n".join(parts)
            + '\n<div class="m4-sticky-host" style="position:fixed;left:0;right:0;bottom:0;z-index:999">' + sticky + "</div>\n</body>\n</html>\n")
    (OUT / "preview.html").write_text(page, encoding="utf-8")
    print("colors:", color_stats, "literals left:", sorted(literal_left))
    print("Block 00:", len(theme), "chars; largest blocks:", sorted(sizes, key=lambda x: -x[1])[:4])


if __name__ == "__main__":
    main()
