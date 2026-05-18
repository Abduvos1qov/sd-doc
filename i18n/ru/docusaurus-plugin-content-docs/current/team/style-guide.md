---
sidebar_position: 6
title: Style guide
audience: Writers, translators, anyone editing sd-docs
summary: Voice, terminology, MDX safety rules, file naming, screenshot conventions. The reference every contributor checks before opening a PR.
topics: [style, voice, terminology, mdx, conventions]
---

# Style guide

Rules for writing sd-docs. Half are aesthetic (voice, structure), half are technical (MDX-safe markdown). Both matter — the technical ones break the build if violated.

## Voice

### For `docs/*` (developer docs)

- **Direct and dense.** Engineers skim. Frontload the answer, then explain.
- **Use precise terms.** `Order.STATUS = 2` not "the second-status order."
- **Reference real file paths.** `protected/modules/orders/controllers/OrderStateController.php` not "the order state controller."
- **Don't apologise.** "TODO: this section is incomplete" is fine; "We haven't gotten to this yet, sorry!" is not.
- **Cite the source.** When documenting a behaviour, link to the controller / model / migration that implements it.

### For `guide/*` (client onboarding)

- **Warm, practical, professional.** Like a colleague explaining over a coffee.
- **No jargon.** Define `AKB` / `OKB` / `MML` the first time they appear.
- **No internals.** A client should never read `protected/modules/orders/controllers/`. They see `Заявки → Список заявок`.
- **Step-by-step.** Every workflow gets `## Step 1 — short caption` headings with screenshots between.
- **Russian UI labels stay Russian.** If the button says `Войти`, the prose says **Войти** (in bold) — even in English text.

## Terminology

Use these standard translations across all locales:

| EN | RU | UZ (Latin) |
|----|----|----|
| agent | агент | agent |
| supervisor | супервайзер | supervayzer |
| expeditor | экспедитор | ekspeditor |
| client / outlet | клиент / торговая точка | mijoz / savdo nuqtasi |
| warehouse | склад | ombor |
| stock | остатки / товары | qoldiq |
| order | заявка | buyurtma |
| delivery | доставка | yetkazib berish |
| visit | визит | tashrif |
| audit | аудит | audit |
| debt | долг | qarz |
| cashbox | касса | kassa |
| cashier | кассир | kassir |
| branch / filial | филиал | filial |
| trip | рейс | reys |
| return | возврат | qaytarish |
| refusal | отказ | rad etish |
| discount | скидка | chegirma |
| bonus | бонус | bonus |
| sales | продажи / сбыт | sotuv / savdo |
| report | отчёт | hisobot |
| dashboard | дашборд | boshqaruv paneli |

Acronyms that stay as-is: **KPI**, **MML**, **AKB**, **OKB** (RU: АКБ / ОКБ; UZ: AKB / OKB).

## Headings

- **One H1 per page** (`# Title`). Frontmatter `title` and the H1 should match.
- **H2 for major sections**, H3 for subsections. Never skip levels (don't go H2 → H4).
- **No trailing punctuation** in headings (`## Step 1 — caption` not `## Step 1 — caption.`).
- **Numbered step headings** for workflows: `## Step 1 — Open the form`, `## Step 2 — Fill it in`. In RU: `## Шаг 1 — …`; in UZ: `## Qadam 1 — …`.

## Tables

- **First column is the label**, second column is the value. Single-row tables read like definitions.
- **Right-align numeric columns** with `---:` in the header divider.
- **Inline code in cells** is OK — `\`columnName\`` reads cleanly.
- **Avoid HTML inside cells** unless necessary. If you need a line break, use `<br/>` only inside Mermaid blocks (see below).

## Links

- **Relative links inside the same plugin** instance: `[label](./other-page)` or `[label](./other-page.md)` — both work.
- **Absolute links across the site**: `[label](/docs/section/page)` or `[label](/guide/section/page)`.
- **Always end the link target on a real file** — Docusaurus's `onBrokenLinks: 'throw'` setting blocks builds when a `.md` link doesn't resolve.
- **`See also` lists** at the bottom of every substantive page improve discoverability.

## MDX safety rules (the build will fail otherwise)

Docusaurus uses **MDX 3** to parse markdown. MDX treats markdown as JSX-aware, which means a handful of plain-text patterns get interpreted as JSX and break the build.

### 1. Wrap `<N` and `<word>` in backticks

These look like JSX tags to MDX:

| ❌ Will fail | ✅ Safe |
|----|----|
| `SUMMA<0 then …` | `` `SUMMA<0` then … `` |
| `URL: <filial.domain>.salesdoc.io` | `` URL: `{filial.domain}.salesdoc.io` `` |
| `Format: <prefix>-<id>,…` | `` Format: `{prefix}-{id},…` `` |

### 2. No bare `{x}` outside backticks

MDX parses `{anything}` as a JavaScript expression. If it can't evaluate, the build fails.

| ❌ Will fail | ✅ Safe |
|----|----|
| `Body fields: { id, name, role }` | `` Body fields: `id`, `name`, `role` `` |
| `{filial.domain}` (in prose) | `` `{filial.domain}` `` (in code) |

### 3. `<br/>` only inside Mermaid code blocks

| ❌ Will fail | ✅ Safe |
|----|----|
| `Line one<br/>Line two` (in prose) | `Line one. Line two.` (use sentences) |
| `<br/>` inside a table cell | use slashes or hyphens to separate |
| `<br/>` inside a Mermaid `flowchart`/`sequenceDiagram` block | ✅ OK — Mermaid renders it |

### 4. No bare pipe `|` inside backtick spans in table cells

| ❌ Will fail | ✅ Safe |
|----|----|
| `` \| col \| `a\|b` \| col \| `` | use `a / b` or `a or b` |
| `` \| col \| `'show'\|'create'` \| `` | write as `(show, create, update)` outside backticks |

### 5. HTML-encoded escapes

If you must write a literal `<`, `>`, or `{` in prose, use:

- `&lt;` for `<`
- `&gt;` for `>`
- `&#123;` for `{`

These render correctly but don't trigger MDX parsing.

### 6. Mermaid blocks

```` ```mermaid
sequenceDiagram
  participant U as User
  U->>Server: GET /orders/list
  Server-->>U: 200 OK
``` ````

Mermaid is permissive — `<br/>`, `{foo}`, and `<word>` all work *inside* the code fence. They only break MDX outside fences.

## File naming

- `kebab-case.md` for doc files
- `lower_snake_or_kebab.png` for screenshots (`07-agents-list.webp`, not `Agents List.webp`)
- `numbered prefix` for ordering when there's a sequence: `01-`, `02-`, etc.
- Match the slug to the filename — Docusaurus uses the filename as the URL slug unless you override.

## Screenshot conventions

- **WebP, not PNG** — see Phase 22 in `ULTRAPLAN-V2.md` at the repo root for the rationale. Run `python3 scripts/optimize-guide-images.py` after adding a PNG.
- **Numbered prefixes** (`66-new-feature.webp`) — keeps the directory listing chronologically navigable.
- **Annotate with callouts** — if a screenshot needs "click here / fill this," see [Screenshot pipeline →](./screenshot-pipeline).
- **One image per Step N** when writing a workflow guide.
- **Captions are short** — `![Orders list with status filter](/screens/guide/03-orders-list.webp)` reads cleanly. Don't write paragraph-length alt text.

## Cross-references

Every substantive page should link both UP (to its parent concept / module) and ACROSS (to related pages). A page in isolation is invisible.

Example pattern at the bottom of every page:

```markdown
## See also

- [Parent concept](./parent)
- [Related workflow](./related)
- [Source code](https://github.com/.../path/to/file.php)
```

## TODOs

- Tag work-in-progress with a Docusaurus admonition:

```markdown
:::warning Work in progress
This section is partial. See [Issue #123](...) for the full scope.
:::
```

- Don't ship `lorem ipsum` placeholder text — leave the section out entirely, or use a `:::warning Work in progress :::` admonition.

## See also

- [Contributing →](./contributing) — workflow, build, PR checklist
- [Translating →](./translating) — voice and terminology per locale
- [Screenshot pipeline →](./screenshot-pipeline) — capture, optimize, annotate
