# How to change the theme and fonts of the whole page

All colours and fonts come from **Block 00** (`00-theme.css`, in page Settings → Custom CSS).
The section blocks never contain their own colours, so one change there restyles the whole page.

---

## 1 · Try a theme without changing anything

Open your live page and add this to the end of the URL:

| Theme | Add to the URL | Mood |
|---|---|---|
| 0 · Original | (nothing) | Petrol & Gold — current design |
| 1 · Emerald | `?m4-theme=emerald` | Deep emerald + gold. Premium, calm |
| 2 · Sage | `?m4-theme=sage` | Sage green + terracotta. Warm, earthy, human |
| 3 · Indigo | `?m4-theme=indigo` | Midnight indigo + rose gold. Elegant, quiet |
| 4 · Clay | `?m4-theme=clay` | Clay blue + coral. The colours of the رياضة الفكر covers |
| 5 · Olive | `?m4-theme=olive` | Olive + sand. Natural, grounded, mature |

Example: `https://courses.mentalhealthmena.com/manhaj/welcome_-664847-367037?m4-theme=sage`

Only you see this, because only you open that link. Visitors keep seeing the normal page.
`themes-comparison.png` shows all 6 side by side.

---

## 2 · Make a theme permanent

1. GHL → page **Settings → Custom CSS**.
2. Keep everything that is there (Block 00).
3. Go to the **very end** and paste the contents of one theme file, for example `2-sage.css`:

```css
:root {
  --m4-primary: #3F6B5C;
  --m4-primary-deep: #1F3D34;
  ...
}
```

4. Save and publish.

- **Switch to another theme:** replace that block with another theme file.
- **Back to the original:** delete that block.

---

## 3 · Change the fonts

**Default:** the whole page is in **Tajawal** (titles, text and quotes).

### Try a ready-made combination (no editing)

Add `?m4-fonts=NAME` to the page URL (works on the live GHL page and on `preview.html`,
which also has a small font picker in the corner):

| NAME | Titles | Text | Quotes | Feel |
|---|---|---|---|---|
| `tajawal` *(default)* | Tajawal | Tajawal | Tajawal | one clean family |
| `alexandria` | Alexandria | Tajawal | Tajawal | strong, modern titles |
| `readex` | Readex Pro | Tajawal | Tajawal | soft, contemporary titles |
| `plex` | Tajawal | IBM Plex Sans Arabic | Amiri | the previous look |
| `markazi` | Markazi Text | Tajawal | Markazi Text | warm, calm naskh titles |
| `amiri` | Amiri | Tajawal | Amiri | classic, spiritual titles |
| `cairo` | Cairo | Cairo | Cairo | bold, familiar |
| `almarai` | Almarai | Almarai | Almarai | simple, friendly |

Can be combined with a theme: `?m4-theme=sage&m4-fonts=markazi`.
"Titles" = section titles (h1/h2); card titles stay in the text font.
The combinations also correct the title size (Alexandria runs wide → ×0.9,
Markazi/Amiri run small → ×1.16/×1.08).

### Make one permanent

Paste its lines at the **end** of Custom CSS (after Block 00):

| NAME | Paste this |
|---|---|
| `alexandria` | `:root{--m4-font-heading:"Alexandria",sans-serif;--m4-heading-scale:.9}` |
| `readex` | `:root{--m4-font-heading:"Readex Pro",sans-serif;--m4-heading-scale:.96}` |
| `plex` | `:root{--m4-font-primary:"IBM Plex Sans Arabic",sans-serif;--m4-font-heading:"Tajawal",sans-serif;--m4-font-display:"Amiri",serif}` |
| `markazi` | `:root{--m4-font-heading:"Markazi Text",serif;--m4-font-display:"Markazi Text",serif;--m4-heading-scale:1.16}` |
| `amiri` | `:root{--m4-font-heading:"Amiri",serif;--m4-font-display:"Amiri",serif;--m4-heading-scale:1.08}` |
| `cairo` | `:root{--m4-font-primary:"Cairo",sans-serif;--m4-heading-scale:.96}` |
| `almarai` | `:root{--m4-font-primary:"Almarai",sans-serif}` |

(Or, in Block 00B, set `window.M4_CONFIG = { fonts: "markazi" };` before the script.)

### Mix your own

The page uses 3 font roles:

| Variable | Used for | URL preview |
|---|---|---|
| `--m4-font-primary` | all text, buttons, numbers, card titles | `?m4-font=…` |
| `--m4-font-heading` | section titles (follows primary unless you set it) | `?m4-heading=…` |
| `--m4-font-display` | member quotes, testimonials, «الفاقة» (follows primary unless you set it) | `?m4-display=…` |

**Fonts already loaded, ready to use:**

| Name to type in CSS | URL short name | Style |
|---|---|---|
| `"Tajawal"` | `tajawal` | clean, familiar (default) |
| `"IBM Plex Sans Arabic"` | `plex` | very readable |
| `"Alexandria"` | `alexandria` | geometric, strong headings |
| `"Readex Pro"` | `readex` | modern, soft |
| `"Cairo"` | `cairo` | bold, popular |
| `"Almarai"` | `almarai` | simple, friendly |
| `"Amiri"` | `amiri` | classic naskh |
| `"Markazi Text"` | `markazi` | modern naskh, warm |
| `"Noto Naskh Arabic"` | `naskh` | neutral naskh |

Example: `?m4-heading=alexandria&m4-display=markazi` = Alexandria titles, Tajawal text, Markazi quotes.

---

## 4 · Fine-tune (optional)

At the end of Custom CSS, inside the same `:root { }`:

| Variable | Default | What it does |
|---|---|---|
| `--m4-cta-bg` / `--m4-cta-text` | red / white | the "ابدأ رحلتك الآن" buttons |
| `--m4-type-scale` | `1` | all text sizes (`1.05` = 5% bigger) |
| `--m4-heading-scale` | `1` | all titles |
| `--m4-radius-scale` | `1` | roundness (`0` = sharp, `1.5` = softer) |
| `--m4-space-scale` | `1` | top/bottom spacing of sections |
| `--m4-motion-scale` | `1` | animation speed (`0` = no animation) |

Want your own colours? Copy any theme file, change the hex codes, and paste it at the end the same way.
