# منهج الطمأنينة — GHL Landing Page

> **Phase 1 (current production refactor): see [REFACTOR.md](REFACTOR.md) and `refactor/blocks/`.**
> Below is the separate v3 redesign proposal (`src/`, `dist/`) for the next phase.

## v3 redesign proposal

المراجعة الكاملة والـ gaps والأرقام اللي محتاجة تأكيد موجودة في **[REVIEW.md](REVIEW.md)**.

## الملفات

```
src/main.css          ← Main CSS: الألوان + المكوّنات + تصميم كل سكشن
src/core.js           ← JS واحد للصفحة كلها (reveal، الفيديو + PiP، الشريط الثابت، اللاب…)
src/head.html         ← قالب الـ Head: الخطوط + الإعدادات + core.js
src/sections/*.html   ← البلوكات (فيها {{tokens}} للروابط والأيقونات)
build.py              ← بيبني dist/ من src/
dist/                 ← ملفات جاهزة للنسخ واللصق في GHL
```

## التركيب في GHL

1. **Page Settings → Custom CSS**: الصق `dist/main.css`، أو `dist/main.min.css` لو في حد أقصى للحجم.
2. **Page Settings → Tracking Code → Head**: الصق `dist/ghl-head.html`.
3. **لكل سكشن:** اعمل Section → Row بعرض كامل (full width) و padding = 0، وجوّاه Code Block، والصق الملف من `dist/blocks/` بالترتيب.
4. **`16-sticky.html`**: الصقه جوه السكشن الثابت (fixed bottom) اللي عندك في GHL زي ما هو.
5. **شريط اللوجوهات** (عنصر GHL): حطه بعد `01-hero` أو بعد `10-kareem`.

> العناوين (h1/h2) والـ ids (`#mh-offer`، `#mh-faq`…) ثابتة في البلوكات، والـ JS بيعتمد عليها. لو غيّرت ترتيب البلوكات مفيش حاجة هتبوظ.

## تغيير الألوان وتجربة التركيبات

**من غير ما تعدّل أي حاجة:** افتح الصفحة المنشورة وزوّد على الرابط:

```
?mh-lab=1                          ← لوحة Palette Lab تحت على الشمال
?mh-theme=clay&mh-accent=coral     ← تركيبة معيّنة على طول
?mh-lab=0                          ← تقفل اللاب
```

في اللاب، اختار الألوان والخطوط، وبعدين دوس **Copy config for GHL** والصق السطر اللي هيتنسخ في `ghl-head.html` مكان سطر `window.MH_CONFIG`.

**لإضافة palette جديدة:** انسخ أي بلوك `:root[data-mh-theme="…"]` في `main.css`، وغيّر قيم الألوان، وزوّد اسمه في `OPTIONS.theme` في `core.js`.

**سكشن فاتح ↔ غامق:** غيّر `data-tone="deep"` في البلوك لـ `alt` أو `paper`، أو العكس.

## تغيير الخطوط (مركزي زي الألوان)

الخطوط اتقسمت لـ 3 أدوار: **headings** (العناوين)، و**body** (النص)، و**accent** (الكلمة المميزة في كل عنوان والآيات والاقتباسات).

- **`type`**: تركيبة جاهزة: `geometric` (الافتراضي: Alexandria + IBM Plex + Markazi)، `editorial`، `classic` (Tajawal)، `kufi`، `modern`، `warm`، `bold`.
- **`head` / `body` / `serif`**: تغيّر دور واحد بس فوق التركيبة، مثلًا `head: "tajawal"`.
- **من غير تعديل:** `?mh-lab=1` هتلاقي في اللاب قسم TYPE ومعاه معاينة حية، أو `?mh-type=kufi&mh-head=cairo` على الرابط.
- مقارنة التركيبات: `docs-font-pairings.png`.

## التعديل وإعادة البناء

الروابط (checkout، واتساب، الفيديو، السياسات) موجودة في `CONFIG` جوه `build.py`. عدّل هناك، وبعدين شغّل:

```
python3 build.py
```

وافتح `dist/preview.html` في المتصفح عشان تشوف الصفحة كاملة واللاب شغّال.
