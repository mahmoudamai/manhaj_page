"""Block 02 (hero stats) v2: content duration instead of "30 محاضرة" (which
suggested 30 short videos). Update HOURS as lectures are added."""

LABEL = "المحتوى حتى الآن"
VALUE = "قرابة 17 ساعة · ويزيد كل 10 أيام"


def apply(path):
    s = path.read_text(encoding="utf-8")
    s = s.replace("عدد المحاضرات", LABEL, 1)
    s = s.replace("30 محاضرة + لقاءات مباشرة", VALUE, 1)
    path.write_text(s, encoding="utf-8")
    return len(s)
