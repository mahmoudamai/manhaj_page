#!/usr/bin/env python3
"""
Build the GHL-ready files from /src.

    python3 build.py

src/sections/*.html use {{tokens}} (links + icons) so the source stays short.
The build expands them and writes paste-ready files to /dist:

    dist/main.css            → GHL: Page Settings → Custom CSS   (readable)
    dist/main.min.css        → same, minified (use if GHL complains about size)
    dist/ghl-head.html       → GHL: Tracking Code → Head   (fonts + config + JS)
    dist/blocks/NN-*.html    → one GHL Code Block each, in this order
    dist/preview.html        → the whole page in one file, with the Palette Lab on
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
DIST = ROOT / "dist"

# ---------------------------------------------------------------------------
# Page settings — change here, then re-run the build.
# ---------------------------------------------------------------------------
CONFIG = {
    "checkout": "https://courses.mentalhealthmena.com/manhaj/checkout",
    "whatsapp": (
        "https://wa.me/971509396851?text=%D9%85%D8%B1%D8%AD%D8%A8%D8%A7%D8%8C%20"
        "%D9%85%D8%AD%D8%AA%D8%A7%D8%AC%20%D9%85%D8%B3%D8%A7%D8%B9%D8%AF%D8%A9%20"
        "%D9%81%D9%8A%20%D8%A7%D9%84%D8%A7%D8%B4%D8%AA%D8%B1%D8%A7%D9%83%20%D9%81%D9%8A%20"
        "%D9%85%D9%86%D9%87%D8%AC%20%D8%A7%D9%84%D8%B7%D9%85%D8%A3%D9%86%D9%8A%D9%86%D8%A9"
    ),
    # TODO: YouTube / Vimeo link, or the .mp4 URL from GHL Media
    "video_url": "",
    # TODO: a 16:9 poster image (thumbnail) for the video
    "video_poster": "",
    # TODO: real policy pages
    "url_refund": "#mh-guarantee",
    "url_privacy": "#",
    "url_terms": "#",
}

_S = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
ICONS = {
    "arrow": f'<svg {_S} stroke-width="2.2"><path d="M19 12H5M11 18l-6-6 6-6"/></svg>',
    "play": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.5-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5Z"/></svg>',
    "x": f'<svg {_S} stroke-width="2.4"><path d="M6 6l12 12M18 6 6 18"/></svg>',
    "calendar": f'<svg {_S}><rect x="3" y="5" width="18" height="16" rx="2.5"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
    "layers": f'<svg {_S}><path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 13 9 5 9-5"/></svg>',
    "book": f'<svg {_S}><path d="M4 19V5a2 2 0 0 1 2-2h14v15H6a2 2 0 0 0-2 2Zm0 0a2 2 0 0 0 2 2h14"/></svg>',
    "bolt": f'<svg {_S}><path d="M13 2 4 14h7l-1 8 9-12h-7l1-8Z"/></svg>',
    "shield": f'<svg {_S}><path d="M12 3 19 6v5c0 4.5-2.8 8.5-7 10-4.2-1.5-7-5.5-7-10V6l7-3Z"/><path d="m9 12 2 2 4-4"/></svg>',
    "plus": f'<svg {_S} stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>',
    "minus": f'<svg {_S} stroke-width="2"><path d="M5 12h14"/></svg>',
    "check": f'<svg {_S} stroke-width="2.2"><path d="m5 12.5 4.5 4.5L19 7"/></svg>',
    "refresh": f'<svg {_S}><path d="M20 11a8 8 0 1 0-2.3 5.7M20 5v6h-6"/></svg>',
    "mic": f'<svg {_S}><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg>',
    "send": f'<svg {_S}><path d="M21 4 3 11l6 2.5M21 4l-4 16-8-6.5M21 4 9 13.5V19l3-3"/></svg>',
    "info": f'<svg {_S}><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></svg>',
    "pen": f'<svg {_S}><path d="M4 20h4L19 9l-4-4L4 16v4Z"/><path d="m14 6 4 4"/></svg>',
    "help": f'<svg {_S}><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6V14M12 17h.01"/></svg>',
    "whatsapp": (
        '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>'
    ),
}


def expand(html: str) -> str:
    def repl(m):
        key = m.group(1)
        if key.startswith("icon:"):
            name = key[5:]
            if name not in ICONS:
                raise KeyError(f"unknown icon: {name}")
            return ICONS[name]
        if key not in CONFIG:
            raise KeyError(f"unknown token: {key}")
        return CONFIG[key]

    out = re.sub(r"\{\{([\w:-]+)\}\}", repl, html)
    # an empty poster url would still request the page itself
    return out.replace("style=\"--poster:url('')\"", "")


def minify_css(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = css.replace(";}", "}")
    return css.strip()


def minify_js(js: str) -> str:
    js = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    lines = [ln.strip() for ln in js.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def main():
    (DIST / "blocks").mkdir(parents=True, exist_ok=True)
    for old in (DIST / "blocks").glob("*.html"):
        old.unlink()

    css = (SRC / "main.css").read_text(encoding="utf-8")
    js = (SRC / "core.js").read_text(encoding="utf-8")
    head_tpl = (SRC / "head.html").read_text(encoding="utf-8")

    (DIST / "main.css").write_text(css, encoding="utf-8")
    (DIST / "main.min.css").write_text(minify_css(css), encoding="utf-8")
    head = head_tpl.replace("/*@@CORE@@*/", minify_js(js))
    (DIST / "ghl-head.html").write_text(head, encoding="utf-8")

    blocks = []
    for f in sorted((SRC / "sections").glob("*.html")):
        html = expand(f.read_text(encoding="utf-8"))
        (DIST / "blocks" / f.name).write_text(html, encoding="utf-8")
        blocks.append((f.stem, html))

    body = []
    for name, html in blocks:
        if name.endswith("sticky"):
            # GHL renders this block inside a fixed-bottom section; mimic that here
            html = f'<div style="position:fixed;inset:auto 0 0 0;z-index:9000">{html}</div>'
        body.append(html)

    preview_head = head.replace(
        'progress: true };', 'progress: true, lab: true };'
    )
    preview = f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>منهج الطمأنينة</title>
<meta name="description" content="Preview of the Manhaj landing page built from the GHL blocks.">
{preview_head}
<style>
body{{margin:0;background:var(--mh-paper)}}
{css}
</style>
</head>
<body>
{chr(10).join(body)}
</body>
</html>
"""
    (DIST / "preview.html").write_text(preview, encoding="utf-8")

    kb = lambda p: f"{(DIST / p).stat().st_size / 1024:.1f} KB"
    print("main.css", kb("main.css"), "| min", kb("main.min.css"), "| head", kb("ghl-head.html"))
    print(len(blocks), "blocks | preview", kb("preview.html"))


if __name__ == "__main__":
    main()
