---
sidebar_position: 8
title: Screenshot pipeline
audience: Anyone adding screenshots to the guide
summary: End-to-end flow for capturing, optimizing, annotating and embedding a screenshot in the guide. References the live demo at localhost:8080 and the script set under scripts/.
topics: [screenshots, playwright, webp, annotation, pipeline]
---

# Screenshot pipeline

How a new screenshot gets from "I need a picture of the new orders screen" to a rendered, annotated, WebP-optimized image in the guide. Three stages: capture, optimize, annotate.

## Stage 1 — capture

### Source: localhost:8080 (the demo tenant)

The guide images all come from a clean demo tenant running locally. To run it:

```bash
cd ~/projects/salesdoctor/sd-main
# follow the project's local setup; typically docker-compose up
# then open http://localhost:8080 in a browser
```

If you don't have the demo set up, ask the maintainer for credentials and a docker-compose start command.

### Capture tools

Three options, in order of preference:

#### 1. Playwright (programmatic, repeatable)

Best when you're capturing many screenshots at known URLs. The pattern used throughout sd-docs:

```javascript
const { chromium } = require('playwright');

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await page.goto('http://localhost:8080/orders/list');
await page.screenshot({ path: 'static/screens/guide/66-new-page.png', fullPage: false });
```

For full-page captures (long scrollable views), use `fullPage: true` — but be aware these produce tall images (sometimes >4000 px).

There's an existing harvester at `scripts/annotate-screenshots.mjs` that you can extend.

#### 2. Browser DevTools "Capture full size screenshot"

In Chrome DevTools (`Cmd+Shift+P` → "Capture full size screenshot"). Saves as PNG. Manual but fine for one-off shots.

#### 3. macOS `Cmd+Shift+4`

Region select. Simplest, lowest quality control (window chrome, browser UI may sneak in).

### Filename convention

```
static/screens/guide/<NN>-<surface>.png
```

- `NN` — two-digit zero-padded sequence (`01`, `02`, …). The current high-water mark is in the directory listing — check before picking.
- `surface` — short hyphenated description matching the URL or feature (`orders-list`, `new-order-form`, `settings-bonus`).

Examples:

```
static/screens/guide/03-orders-list.png
static/screens/guide/33-new-order-empty.png
static/screens/guide/65-planning-outlet.png
```

### Viewport

- **1440 × 900** for normal pages — matches a typical laptop browser.
- **1440 × full-page** for long pages (full dashboards, full reports) — set `fullPage: true`.
- **Don't use mobile viewports** for the web guide — capture mobile UI separately (Phase 24 of the v2 ultraplan).

### Demo data hygiene

The screenshots end up in the public guide. Before capturing:

- Sign in as the demo admin (`admin` or whatever your seed user is named)
- Make sure the visible data is plausible-but-not-private — don't capture pages showing real customer names from production
- The demo tenant has seeded fake clients (`Магазин Yulduz`, etc.) — those are safe to show

## Stage 2 — optimize

After capturing the PNG, generate a WebP variant (50–60% smaller, modern browsers prefer it):

```bash
python3 scripts/optimize-guide-images.py
```

This walks `static/screens/guide/*.png` and writes a sibling `*.webp` for each. Idempotent — safe to re-run.

After running:

- The original `.png` stays on disk (archival fallback, not referenced)
- The new `.webp` is what your markdown references

### Why WebP

Original PNGs total ~7.7 MB for 64 screenshots. WebP at quality=85 brings that to 3.8 MB — a 52% reduction with no visible quality loss. Chrome, Safari, Firefox, Edge all support WebP. Coverage is ~98% of real users.

### Referencing the WebP in markdown

```markdown
![Orders list with status filter applied](/screens/guide/03-orders-list.webp)
```

Always reference `.webp`, never `.png`. The PNG is just a backup.

## Stage 3 — annotate (optional)

When a screenshot needs numbered circles pointing at specific click targets, add a callouts sidecar JSON.

### Define callouts

Create `static/data/callouts-guide/<NN>-<surface>.json`:

```json
{
  "callouts": [
    { "x": 1370, "y": 110, "label": "Step 1: + Add" },
    { "x": 200,  "y": 240, "label": "Step 2: Click row" },
    { "x": 720,  "y": 500, "label": "Step 3: Review detail" }
  ]
}
```

| Field | Meaning |
|-------|---------|
| `x` | Pixel x-coordinate of the circle's center (relative to the image, 0 = left edge) |
| `y` | Pixel y-coordinate of the circle's center (0 = top edge) |
| `label` | Currently stored but not rendered — reserved for future hover tooltips |

### Run the annotator

```bash
python3 scripts/annotate-guide-screenshots.py
```

This walks `static/screens/guide/*.webp`, finds matching JSONs in `static/data/callouts-guide/`, and renders red-circled annotations into `static/screens/guide-annotated/<file>.webp`.

Then copy the annotated WebPs back over the originals:

```bash
for j in static/data/callouts-guide/*.json; do
  name=$(basename "$j" .json)
  cp "static/screens/guide-annotated/${name}.webp" "static/screens/guide/${name}.webp"
done
rm -rf static/screens/guide-annotated
```

(The pipeline overwrites in-place because that means markdown references don't change.)

### Positioning tips

- **Open the screenshot in Preview / an image viewer** that shows pixel coordinates. The coordinate you want is **the center of the click target**.
- **Default viewport is 1440 × 900** — most coordinates fall in that range.
- **Full-page screenshots** can be 1440 × 4000+ — adjust y accordingly.
- **Aim slightly above the target** if there are nearby labels you don't want to obscure.
- **Spread circles** — too close together makes the numbers hard to read.

### When NOT to annotate

- The screenshot is just a "here's what the dashboard looks like" overview — no specific steps to point at.
- The page has too many click targets — readers won't follow a 7-number trail. Break the workflow into multiple screenshots.

## Embedding in a guide page

Standard markdown:

```markdown
## Step 2 — Click "+ Add agent"

Click **+ Добавить агента** at the top right:

![Agents list with the Add button highlighted](/screens/guide/07-agents-list.webp)
```

The annotated WebP renders inline. The alt text is what screen readers read aloud — keep it descriptive but short.

## Common issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Image is huge on the page | Captured at high DPI; viewport doesn't constrain width | Set `viewport: { width: 1440 }` in Playwright |
| Image is blurry | PNG was compressed before WebP conversion | Re-capture at full resolution, don't pre-process |
| Annotated circle is misplaced | Coordinates wrong | Open the image, find the right pixel, update JSON, re-run annotator |
| Build fails: "Markdown image with URL '/screens/guide/X.webp' couldn't be resolved" | The file doesn't exist | Did you run `optimize-guide-images.py` after adding the PNG? |
| Image shows in EN but not in RU/UZ | Markdown references differ between locales | Sync the references — same `.webp` path in all 3 |

## See also

- [Contributing →](./contributing) — workflow, build, PR checklist
- [Style guide →](./style-guide) — screenshot conventions, MDX rules
- [Translating →](./translating) — alt text is translated per locale
- Scripts:
  - `scripts/optimize-guide-images.py` — PNG → WebP
  - `scripts/annotate-guide-screenshots.py` — callout renderer
  - `scripts/annotate-screenshots.mjs` — older Playwright harvester (legacy, for `static/screens/annotated/`)
