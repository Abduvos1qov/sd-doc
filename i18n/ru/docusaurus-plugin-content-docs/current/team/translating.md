---
sidebar_position: 7
title: Translating
audience: Translators, contributors adding a new locale
summary: How to translate one page, how to add a new locale, and the standard glossary for terminology consistency across en / ru / uz.
topics: [translation, i18n, locale, ru, uz, glossary]
---

# Translating

sd-docs ships in three locales: **English** (source), **Russian**, **Uzbek (Latin)**. Russian is the primary working language for both developer docs and client onboarding — the UI is in Russian, and most dealer admins read Russian comfortably. Uzbek is provided so Uzbek-first staff can use the same guide.

## Layout

Every locale has its own subtree:

```
docs/                                              # EN source
i18n/ru/docusaurus-plugin-content-docs/current/    # RU
i18n/uz/docusaurus-plugin-content-docs/current/    # UZ

guide/                                                       # EN source
i18n/ru/docusaurus-plugin-content-docs-guide/current/        # RU
i18n/uz/docusaurus-plugin-content-docs-guide/current/        # UZ
```

The plugin instance for `/guide` adds the `-guide` suffix to the i18n path. Don't drop a guide translation into the wrong subtree.

## Translating one page

1. **Read the EN source** carefully. Note any inline UI labels in Russian/Uzbek (they don't get re-translated).
2. **Open the matching i18n file** — same path under `i18n/<locale>/...`.
3. **Translate prose only** — keep all frontmatter keys, screenshot paths, URLs, link targets, code blocks, table structures, admonition syntax.
4. **Translate `title:` in the frontmatter** to the locale's language.
5. **Use the standard glossary** below.
6. **Build all 3 locales** before opening a PR — `npm run build`.

## What NOT to translate

- **Russian UI labels** in **bold** — `**Войти**`, `**Сохранить**`, `**Активен**`. These are what the user sees on screen; leave them in Russian even in the EN version.
- **URLs and code paths** — `/orders/list`, `protected/modules/orders/`, `localhost:8080`.
- **Code in backticks** — `` `ServerSettings::roundingDecimalsMoney()` ``.
- **Brand names** — SalesDoctor, Telegram, Excel, Google Chrome, Payme, Click.
- **Screenshot paths** — `/screens/guide/03-orders-list.webp` stays the same in all 3 locales.
- **Acronyms** — KPI, MML. (RU writes AKB → АКБ / OKB → ОКБ; UZ keeps Latin.)

## Standard glossary

Use these terms consistently — the same source word always maps to the same target word.

| EN | RU | UZ (Latin) |
|----|----|----|
| agent | агент | agent |
| supervisor | супервайзер | supervayzer |
| expeditor | экспедитор | ekspeditor |
| client / outlet | клиент / торговая точка | mijoz / savdo nuqtasi |
| warehouse | склад | ombor |
| stock | остатки / товары | qoldiq |
| order | заявка | buyurtma |
| order line | строка заявки | buyurtma qatori |
| delivery | доставка | yetkazib berish |
| visit | визит | tashrif |
| audit | аудит | audit |
| photo report | фотоотчёт | foto hisoboti |
| debt | долг / задолженность | qarz |
| receivable | дебиторская задолженность | debet qarz |
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
| dashboard | дашборд / панель | boshqaruv paneli |
| inventory | инвентаризация / оборудование | inventarizatsiya / jihoz |
| receipt / purchase | поступление | tushum |
| markup | наценка | qo'shimcha |
| price type | тип цены | narx turi |
| credit limit | кредитный лимит | kredit limiti |
| channel | канал сбыта | sotuv kanali |
| segment / category | сегмент / категория | segment / toifa |
| approval | подтверждение | tasdiqlash |

## Translating step-by-step workflow pages

The guide uses a strict "Step N — caption" pattern.

| Source | RU | UZ |
|--------|----|----|
| `## Step 1 — Open the orders list` | `## Шаг 1 — Откройте список заявок` | `## Qadam 1 — Buyurtmalar ro'yxatini oching` |
| `## Step 2 — Pick the client` | `## Шаг 2 — Выберите клиента` | `## Qadam 2 — Mijozni tanlang` |

Don't translate "Step" to "Этап" / "Bosqich" — pick **Шаг** / **Qadam** and stay consistent.

## Translating MDX admonitions

```markdown
:::tip  First-time password
If this is your very first sign-in…
:::
```

Becomes:

| Source | RU | UZ |
|--------|----|----|
| `:::tip First-time password` | `:::tip Первый пароль` | `:::tip Birinchi parol` |
| `:::warning Work in progress` | `:::warning В работе` | `:::warning Ish jarayonida` |
| `:::info AKB vs OKB` | `:::info АКБ vs ОКБ` | `:::info AKB va OKB` |

The admonition keyword (`tip`, `warning`, `info`) stays in English — Docusaurus uses it as a CSS class.

## Translating table headers

Both columns get translated; the divider row stays as-is:

```markdown
| KPI | What it measures |     →    | KPI | Что измеряется |
|-----|------------------|          |-----|----------------|
| **Sales target** | ... |          | **План продаж** | ... |
```

Right-aligned numeric columns: keep the `---:` divider intact.

## Adding a new locale

If you want to add, say, Karakalpak (`kaa`):

1. Update `docusaurus.config.js`:

```javascript
i18n: {
  defaultLocale: 'en',
  locales: ['en', 'ru', 'uz', 'kaa'],
  localeConfigs: {
    kaa: { label: "Qaraqalpaqsha", htmlLang: 'kaa' },
  },
},
```

2. Create the i18n tree:

```bash
mkdir -p i18n/kaa/docusaurus-plugin-content-docs/current
mkdir -p i18n/kaa/docusaurus-plugin-content-docs-guide/current
```

3. Either translate every page now (months of work), or copy EN content as stubs:

```bash
cp -r docs/* i18n/kaa/docusaurus-plugin-content-docs/current/
cp -r guide/* i18n/kaa/docusaurus-plugin-content-docs-guide/current/
```

4. Run `npm run build` — the new locale should compile if every referenced file exists.

5. Start translating one page at a time. Pages still containing EN content will display in English even though the URL shows `/kaa/...`.

## When to do a translation pass

| Trigger | What to do |
|---------|------------|
| A typo in EN | Fix in all 3 locales identically |
| A link target changed | Update all 3 locales |
| New section added to EN | Add matching translated section in RU + UZ |
| New full page in EN | Stub i18n locales with EN content, then translate properly |
| EN voice/structure rewritten | Re-translate from the new EN source |

## Quality bar

A good translation:
- **Reads naturally** — would a native speaker write it this way?
- **Matches the glossary** — no synonym drift across pages
- **Preserves all UI labels** — `**Войти**` stays `**Войти**`
- **Keeps the same headings** in the same order
- **Uses identical image references** — same filename, often a translated alt-text

## See also

- [Contributing →](./contributing) — workflow, build, PR checklist
- [Style guide →](./style-guide) — voice, terminology, MDX safety
- [Screenshot pipeline →](./screenshot-pipeline)
