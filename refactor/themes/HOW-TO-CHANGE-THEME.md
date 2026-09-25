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

## 3 · Change the font (e.g. Tajawal)

**Try it without editing:** add `?m4-font=tajawal` to the URL.
You can combine it with a theme: `?m4-theme=sage&m4-font=tajawal`.

**Make it permanent:** paste this at the **end** of Custom CSS:

```css
:root {
  --m4-font-primary: "Tajawal", sans-serif;
}
```

The page uses 3 font roles. Change one or all of them:

| Variable | Used for | URL preview |
|---|---|---|
| `--m4-font-primary` | all text, buttons, numbers | `?m4-font=…` |
| `--m4-font-heading` | section titles (follows primary unless you set it) | `?m4-heading=…` |
| `--m4-font-display` | quotes, testimonials, «الفاقة» (currently Amiri) | `?m4-display=…` |

**Fonts already loaded, ready to use:**

| Name to type in CSS | URL short name | Style |
|---|---|---|
| `"IBM Plex Sans Arabic"` | `plex` | clean, very readable (current) |
| `"Tajawal"` | `tajawal` | your previous font |
| `"Alexandria"` | `alexandria` | geometric, strong headings |
| `"Readex Pro"` | `readex` | modern, soft |
| `"Cairo"` | `cairo` | bold, popular |
| `"Almarai"` | `almarai` | simple, friendly |
| `"Amiri"` | `amiri` | classic naskh (current quotes) |
| `"Markazi Text"` | `markazi` | modern naskh, warm |
| `"Noto Naskh Arabic"` | `naskh` | neutral naskh |

Example: Tajawal for text, Alexandria for titles, Markazi for quotes:

```css
:root {
  --m4-font-primary: "Tajawal", sans-serif;
  --m4-font-heading: "Alexandria", sans-serif;
  --m4-font-display: "Markazi Text", serif;
}
```

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
