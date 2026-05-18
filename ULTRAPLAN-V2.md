# Ultraplan v2 — sd-docs

**Plan date:** 2026-05-18
**Predecessor:** 10-phase ultraplan (Phases 1–10, committed as `docs: full backfill from live demo + sd-main source (10-phase ultraplan)`) + Phases 11–21 (this session's backfill: audit, sd-main missing modules, API endpoint docs, sd-cs/sd-billing deep dives, cross-module flows, settings catalog, RBAC matrix, schema reference, UI pages wave 1) + Waves 1–6 (client onboarding guide: 24 pages × 3 locales, 52 real screenshots from `localhost:8080`, full RU + UZ translations).

**Current state (entering v2):**
- ~210 developer doc pages across sd-main / sd-cs / sd-billing
- 24 client guide pages × 3 locales = 72 published guide pages
- 1 master "Pages & forms catalog" × 3 locales
- 52 real screenshots from the live demo
- Build green on en/ru/uz at every commit
- Coverage estimate: ~95% of source-code surface; client guide is structurally complete

**v2 goal:** lift sd-docs from "comprehensive" to "production-grade, performant, automated, used."

---

## Big-picture tracks

| Track | Focus | Phases |
|-------|-------|--------|
| **1 — Polish** | Make what we have feel professional | 22, 23, 24 |
| **2 — Reach** | Make the dev docs usable in RU + UZ | 25 |
| **3 — Automation** | Prevent regressions, enforce quality | 26, 27, 28, 29 |
| **4 — Advanced** | Self-service for integrators + AI-assisted browsing | 30, 31, 32 |

---

## Phase 22 — Image performance pass

**Goal:** cut total guide page weight by 70%.

**Problem today:** 52 PNGs in `static/screens/guide/`, average ~150 KB each (~7.8 MB total). Some catalog pages embed 30+ images; landing page weight pushes 4 MB.

**Deliverable:**
- Run `oxipng -o 6` (or `imagemin-pngquant`) on every PNG in `static/screens/`. Target ≥60% size reduction without visible quality loss.
- Generate WebP variants alongside the PNGs (modern browsers auto-pick).
- Add `loading="lazy"` to non-hero images in `pages-catalog.md` (only the first 2–3 should eager-load).
- Verify Lighthouse Performance ≥90 on `/guide/welcome` and `/guide/pages-catalog`.

**Effort:** 1 session. Mostly tooling + spot-checks.

**Critical path:** unblocks Phase 23 (annotations work on the optimized source images).

---

## Phase 23 — Annotated screenshots

**Goal:** every Step N in the guide has a numbered circle / arrow / highlight box on the corresponding screenshot showing exactly where to click.

**Pipeline:**
- `scripts/annotate-screenshots.py` already exists (per git status at session start). Audit and extend it.
- Sidecar JSON in `static/data/callouts/` per image (already a pattern — see `audit_photoReport.json`, etc.).
- Each callout entry: `{ "step": 2, "x": 120, "y": 480, "label_en": "Click here", "label_ru": "...", "label_uz": "..." }`.
- Pillow / sharp renders the annotated PNG alongside the raw one.
- Guide pages reference the `.annotated.png` version.

**Deliverable:**
- Annotated versions of the 20 highest-impact screenshots (dashboards, add-X forms, order capture, payment approval, audit photo report).
- Per-locale captions baked into the annotation (so an arrow's label reads "Войти" for RU readers and "Kirish" for UZ readers).

**Effort:** 2 sessions. First session: pipeline + first 10 images. Second session: remaining 10 + per-locale captions.

**Critical path:** independent. Run in parallel with Phase 24.

---

## Phase 24 — Mobile app screenshot capture

**Goal:** the `/guide/mobile/` section currently uses web-side screenshots as substitutes for the phone UI. Replace with real mobile screenshots.

**Approach options:**
- **Option A:** Android Studio emulator + adb screenshot pipeline.
- **Option B:** Real device + `scrcpy` + screenshot script.
- **Option C:** Maintainer manually captures via the phone and drops files into `static/screens/guide/mobile/`.

**Capture list (15–20 shots):**
- Agent: login screen, today's route, client card, take order, audit photos, sync state, KPI progress.
- Expeditor: load confirm, trip stop list, deliver order, cash collection, end-of-day summary.
- Auditor: photo capture flow, poll questions, visit done.

**Deliverable:**
- 15–20 new mobile screenshots under `static/screens/guide/mobile/`.
- `mobile/agent-app.md`, `mobile/expeditor-delivery.md`, `mobile/visit-and-audit.md` rewritten to use these instead of web stand-ins. EN/RU/UZ.

**Effort:** 2 sessions if device access is available. 1 session per role flow.

**Critical path:** independent.

---

## Phase 25 — Developer docs i18n (Top 50)

**Goal:** dev docs `i18n/ru/` and `i18n/uz/` currently hold EN content as stubs. Translate the highest-traffic 50 pages to real Russian + Uzbek.

**Selection criteria for the Top 50:**
- All 3 project overview pages (sd-main / sd-cs / sd-billing)
- All concept pages (`docs/concepts/*`)
- All role pages (`docs/roles/*`)
- All cross-module flow pages (`docs/flows/*`)
- The 7 sd-cs module deep dives
- The 13 sd-billing module deep dives
- The settings catalog (5 pages)
- The RBAC matrix (4 pages)
- The page-to-module map

**Deliverable:**
- 50 EN pages × 2 locales = 100 fresh translations
- `i18n-glossary.json` in repo root with stable term mappings (agent/агент/agent, supervisor/супервайзер/supervayzer, etc.)
- Translator README

**Effort:** 3 sessions with parallel agents (proven pattern from this session: 8,500 words RU + 8,570 UZ in two sessions for the 22-page client guide).

**Critical path:** independent. Best done after Phase 28 (style/translator guide).

---

## Phase 26 — Cross-reference audit & link integrity

**Goal:** today every page is reachable from the sidebar, but cross-references between related pages are inconsistent. A reader on `flows/order-end-to-end.md` should always be able to jump to `modules/orders`, `modules/finans`, `modules/payment`, `concepts/payment-lifecycle`, etc.

**Approach:**
- Build a graph: each page → all concepts/modules/APIs it mentions.
- Compare against actual links in the markdown.
- Generate a "missing link" report.
- Add the missing "See also" entries.

**Deliverable:**
- A `scripts/cross-ref-audit.mjs` that produces the report.
- Apply 500+ missing cross-references via parallel edit agents.

**Effort:** 2 sessions. First: script + report. Second: apply fixes.

---

## Phase 27 — Docusaurus versioning

**Goal:** snapshot today's state as `v1.0`. Future breaking changes go under `next/`. Old URLs stay stable for clients linking to specific instructions.

**Steps:**
- `npm run docusaurus docs:version 1.0` (creates `versioned_docs/version-1.0/`, `versioned_sidebars/version-1.0-sidebars.json`).
- Same for the `guide` plugin instance.
- Update `docusaurus.config.js` to default to v1.0 and offer `next` as preview.
- Document the version-bump trigger: "any breaking UI change in sd-main warrants a new doc version."

**Deliverable:**
- Versioned doc snapshots.
- `docs/team/versioning.md` describing the process.

**Effort:** 1 session.

---

## Phase 28 — Contributor & style guide

**Goal:** anyone — a new engineer, a translator, a PM — can add or edit a page without ramping up.

**Pages to create under `docs/team/`:**
- `contributing.md` — how to fork, add a page, run the build locally, open a PR
- `style-guide.md` — voice, terminology, MDX-safety rules (no bare `<N`, no `{x}` outside backticks, etc.), screenshot conventions, file-naming rules
- `translating.md` — how to translate one page or set up a new locale; references the glossary from Phase 25
- `screenshot-pipeline.md` — how the harvester works, how to add a new annotated screenshot

**Deliverable:** 4 contributor reference pages.

**Effort:** 1 session.

**Critical path:** unblocks Phase 25 (translators need this) and Phase 29 (CI rules reference the style guide).

---

## Phase 29 — CI/CD setup

**Goal:** every PR is auto-built, tested for broken links, image size enforcement runs, and main auto-deploys to docs.salesdoc.io.

**Workflow files:**
- `.github/workflows/build.yml` — runs `npm run build` on every PR; fails on broken links or MDX errors
- `.github/workflows/deploy.yml` — on push to main, builds and deploys (Cloudflare Pages, Vercel, GitHub Pages, or your existing host)
- `.github/workflows/quality.yml` — `oxipng` size check, terminology lint (no untranslated EN strings in RU/UZ files), broken-image checker

**Deliverable:**
- 3 GitHub Actions workflows
- Build badge in README.md
- Slack/Telegram webhook on deploy success/failure

**Effort:** 1 session.

---

## Phase 30 — API try-it playground

**Goal:** integrators who use api/v3-mobile or api/v4-online stop emailing for code samples — the docs have working examples.

**Deliverables per controller page:**
- A `curl` example for each action (auth header, sample body, expected response)
- A Postman collection auto-generated from the same source
- For read-only safe endpoints: an embedded "Try it" widget that hits a sandbox instance and shows the response

**Effort:** 2 sessions. Largest: building the sandbox or pointing at the existing demo.

**Critical path:** dependent on a stable sandbox tenant URL.

---

## Phase 31 — Search & RAG

**Goal:** users ask the docs questions in natural language; an AI agent answers using only the doc content.

**Setup:**
- Keep `docusaurus-search-local` for the keyword search
- Add a vector index per locale (Pinecone / Weaviate / pgvector) over the rendered markdown
- A "/ask" widget at the top of every page that hits the same RAG layer the team already uses (per the earlier ecosystem note about feeding into a team RAG)

**Effort:** 2 sessions. Largest: embedding generation + endpoint.

---

## Phase 32 — Living feedback loop

**Goal:** the docs improve weekly based on real user signals.

**Components:**
- "Was this page helpful?" widget at the bottom of every page
- Anonymous feedback posts to a Telegram bot / webhook
- Monthly review meeting → top 3 problem pages get a fix sprint
- Public changelog of doc improvements (cross-link to `docs/changelog.md`)

**Effort:** 1 session for setup. Ongoing maintenance.

---

## Suggested sequence

```
Wave A (parallelizable, low-blocker)
├── Phase 22 — image perf
├── Phase 23 — annotated screenshots
└── Phase 24 — mobile capture

Wave B (depends on Wave A)
├── Phase 28 — contributor guide ◄── unblocks Phase 25
└── Phase 26 — cross-ref audit

Wave C (depends on Wave B)
├── Phase 25 — dev-docs i18n
└── Phase 27 — versioning

Wave D (depends on Wave C)
├── Phase 29 — CI/CD
├── Phase 30 — API playground
└── Phase 31 — search/RAG

Wave E (steady-state)
└── Phase 32 — feedback loop (ongoing)
```

**Time estimate:** 12–16 focused sessions to ship all 11 phases. Critical path is ~6 sessions (Phase 28 → 25 → 27 → 29).

---

## Where to start

If pushing further into the same session: **Phase 22 (image perf)** — high impact, bounded scope, can be measured (Lighthouse before/after). Tools needed: `oxipng` and `sharp` (npm).

If starting fresh tomorrow: **Phase 28 (contributor guide)** — unblocks two later phases and is a single-session win.

---

## State of the predecessor work (v1)

Status of the Phase 11–21 ultraplan + Waves 1–6:

| Phase | Status |
|-------|--------|
| 11 — Audit | ✅ |
| 12 — sd-main missing modules | ✅ |
| 13 — per-endpoint API docs | ✅ |
| 14 — sd-cs per-module | ✅ |
| 15 — sd-billing per-module | ✅ |
| 16 — cross-module flows | ✅ |
| 17 — state-machine concepts | ✅ |
| 18 — settings catalog | ✅ |
| 19 — RBAC matrix | ✅ |
| 20 — schema reference | ✅ |
| 21 — UI page wave 1 (10 modules, 59 pages) | ✅ |
| Wave 1 — `/guide` plugin instance + 23 onboarding pages | ✅ |
| Wave 2 — rewrite to step-by-step + 16 real screenshots | ✅ |
| Wave 3 — form modal captures (5 forms) | ✅ |
| Wave 4 — KPI drill-downs (5 screenshots) | ✅ |
| Wave 5 — dropdowns / pickers / search (7 screenshots) | ✅ |
| Wave 6 — detail views + master "Pages catalog" × 3 locales | ✅ |

Everything above builds green on en/ru/uz.
