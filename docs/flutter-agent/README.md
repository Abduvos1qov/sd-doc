---
title: Flutter agent docs
sidebar_position: 0
slug: /flutter-agent
---

# `app_salesdoctor_agent` — developer documentation

This is the developer documentation for the **SalesDoctor Agent** Flutter mobile app — the field-agent client used by Sales Doctor's distributors. It targets Android and iOS, ships at version 1.0.17+24 (May 2026), and contains roughly 1,700 Dart files split across `domain`, `data`, and `presentation` layers, with a Floor SQLite database at schema version 18.

## How to read these docs

Architecture and cross-cutting concerns are deep; per-feature coverage is a short catalog + five representative deep-dives. If you're new to the codebase:

1. Start with **[01-architecture](./01-architecture.md)** for the layer model, DI module order, and boot sequence.
2. Pick a path based on what you need to do (see the role table below).
3. When you start touching a specific feature, look it up in **[11-features-catalog](./11-features-catalog.md)**; if it's in the deep-dive set (sync, order/manage, client/list, main shell, client/oddment), read that doc too.

## By role

| If you're… | Read in this order |
|------------|---------------------|
| New to the codebase | [01-architecture](./01-architecture.md) → [04-presentation-layer](./04-presentation-layer.md) → [10-conventions](./10-conventions.md) → [12-feature-deep-dives/main-shell](./12-feature-deep-dives/main-shell.md) |
| Adding a new screen / feature | [10-conventions §Adding a new feature](./10-conventions.md#adding-a-new-feature) → [03-domain-layer](./03-domain-layer.md) → [04-presentation-layer](./04-presentation-layer.md) → [12-feature-deep-dives/client-oddment](./12-feature-deep-dives/client-oddment.md) |
| Working on sync | [07-synchronize](./07-synchronize.md) → [12-feature-deep-dives/sync](./12-feature-deep-dives/sync.md) → [05-database §Sync contract](./05-database.md#sync-contract--the-issync-column) |
| Working on the database | [05-database](./05-database.md) → [02-data-layer](./02-data-layer.md) |
| Debugging an error | [09-error-handling](./09-error-handling.md) → [02-data-layer §Interceptor stack](./02-data-layer.md#interceptor-stack) |
| Cross-feature communication issues | [06-streams-and-cross-feature](./06-streams-and-cross-feature.md) → [04-presentation-layer §StreamSubscription lifecycle](./04-presentation-layer.md#streamsubscription-lifecycle) |
| Navigation / shell / force-update | [08-navigation-and-shell](./08-navigation-and-shell.md) |

## What's in here

Cross-cutting:
- [01-architecture](./01-architecture.md) — layers, DI, boot, FlavorConfig
- [02-data-layer](./02-data-layer.md) — Dio, prefs, services, repository_impls
- [03-domain-layer](./03-domain-layer.md) — models, repositories, use cases, mappers
- [04-presentation-layer](./04-presentation-layer.md) — BLoC, pages, AutoRoute, FutureHandler
- [05-database](./05-database.md) — Floor schema, all migrations v1→v18
- [06-streams-and-cross-feature](./06-streams-and-cross-feature.md) — the 14 cross-feature stream controllers
- [07-synchronize](./07-synchronize.md) — full sync architecture (foreground + background)
- [08-navigation-and-shell](./08-navigation-and-shell.md) — App init, MainRoute tabs, deep-link, force-update
- [09-error-handling](./09-error-handling.md) — AppException hierarchy, interceptor, global listener
- [10-conventions](./10-conventions.md) — code style, performance rules, known issues

Features:
- [11-features-catalog](./11-features-catalog.md) — index of all ~30 features
- [12-feature-deep-dives/](./12-feature-deep-dives/main-shell.md) — five representative deep-dives:
  - [sync](./12-feature-deep-dives/sync.md)
  - [order/manage](./12-feature-deep-dives/order-manage.md)
  - [client/list](./12-feature-deep-dives/client-list.md)
  - [main shell + home](./12-feature-deep-dives/main-shell.md)
  - [client/oddment](./12-feature-deep-dives/client-oddment.md)

## Doc conventions

- File paths are shown verbatim: `lib/presentation/features/order/manage/order_manage_page.dart`.
- Line numbers are cited inline when they illuminate a specific contract: `lib/main.dart:99-117`.
- Code blocks are usually verbatim excerpts; when they're not, the file path above the block points to the real source.
- Mermaid diagrams render in this Docusaurus site (`@docusaurus/theme-mermaid` is configured in `docusaurus.config.js`).
- Cross-references between docs use relative links so they survive moves and locale switches.

## Keeping these docs alive

Update them when:

- The DB schema version changes — re-summarize the new migration in [05-database](./05-database.md).
- A new feature is added — append a row to [11-features-catalog](./11-features-catalog.md). If the feature reshapes a cross-cutting concern, update the corresponding doc.
- The sync chain gains or loses a step — update [07-synchronize §The chain, in order](./07-synchronize.md#the-chain-in-order) and bump the `PercentageCalculator(29)` discussion if applicable.
- A `BaseStreamController` is added — append it to [06-streams-and-cross-feature](./06-streams-and-cross-feature.md).
- The known-issues list in [10-conventions](./10-conventions.md) changes — sync with `CLAUDE.md`.

The orchestration rules in the repo's `CLAUDE.md` (top of the source tree) take precedence over anything written here. If you find disagreement, `CLAUDE.md` is authoritative; fix the docs.

## Source-of-truth links

- The repo: `/Users/abdulbosit/SD-Projects/sd_agent_flutter/` (or `app_salesdoctor_agent` in your remote)
- The orchestrator: `CLAUDE.md` at the repo root
- The agent prompt library: `.claude/agents/*.md`
- The skills library: `.claude/skills/*` (e.g. `/review-flutter`, `/translate`, `/db-migration`, `/fix-leaks`)
