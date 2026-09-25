"""Block 04 (Kareem intro): "+100 ألف متدرّب" → "… حضوريًا وأونلاين", so it reads
as the total (the hero's 40k is the paid online courses only)."""


def apply(path):
    s = path.read_text(encoding="utf-8")
    s = s.replace("متدرّب", "متدرّب حضوريًا وأونلاين", 1)
    path.write_text(s, encoding="utf-8")
    return len(s)
