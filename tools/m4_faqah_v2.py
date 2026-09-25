"""Block 06 (الفاقة) v2: the learning designer's new intro text.

Only the copy column changes (kicker, title, paragraphs); the design and the
definition card stay as generated.
"""

COPY = """<div class="m4-faqah__copy m4-faqah__reveal m4-reveal">
        <div class="m4-faqah__kicker">
          سمة هذا العصر
        </div>
        <h2>
          لماذا يستمر الشعور بالفراغ
          رغم كل ما نحققه؟
        </h2>
        <p>
          نعيش اليوم في زمن يتسارع فيه كل شيء من حولنا:
          أهداف متزايدة، وخيارات لا حصر لها، ومقارنات لا تتوقف،
          إلى جانب سيل من المحتوى الذي يملي علينا
          كيف نعيش وماذا ينبغي أن نملك.
        </p>
        <p>
          ورغم السعي، يظل يرافقنا ذلك الشعور الخفي بالحيرة والنقص،
          فنركض كثيرًا دون أن ندري ما الذي نبحث عنه،
          أو متى سنصل إلى مرحلة الكفاية والرضا.
        </p>
        <p>
          من هذا المنطلق، نتوقف في
          <strong>«منهج الطمأنينة»</strong>
          عند مفهوم
          <strong>«الفاقة»</strong>
          وعلاقته العميقة بحالة التيه،
          وكيف يؤثر على نظرتنا لأنفسنا وللحياة وما ننتظره منها.
        </p>
        <p>
          ومن هنا نبدأ في مراجعة الصورة الأوسع:
          ما الذي نسعى إليه؟ ماذا ننتظر منه؟
          وما التصورات والمهارات التي نحتاجها
          حتى نتعامل مع أنفسنا وحياتنا بوعي أكبر؟
        </p>
      </div>"""


def apply(path):
    s = path.read_text(encoding="utf-8")
    a = s.index('<div class="m4-faqah__copy')
    b = s.index('<aside', a)
    b = s.rindex("</div>", a, b) + len("</div>")
    s = s[:a] + COPY + s[b:]
    path.write_text(s, encoding="utf-8")
    return len(s)
