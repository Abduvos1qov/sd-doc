---
title: "Список опросов"
audience: All sd-main developers, QA
summary: Admin page at /rating/index — manage polls and questions
topics: [rating, page, ui]
---

# Список опросов

**URL**: `/rating/index` · **Module**: `rating` · **Controller**: `IndexController::index` · **RBAC**: module-level (no explicit `H::access`) · **Role harvested**: `admin`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Admin-facing landing page for the Rating subsystem. Lists every poll template (Russian: "опрос") with its questions, star-vote tallies, and per-question average. Used to create polls, generate per-client share links, and review responses.

## Fields

This page is a configuration / management screen — it does not have an input form. The "create" and "edit" flows are launched via the **Создать опрос** button (top filter row) and the per-row dropdown items below, which open the `_formRating`, `_formQuestion`, `_formLink`, `_formClientLink` and `_viewVoters` partials in a modal.

| Modal | Source partial | Fields |
|---|---|---|
| Создать / Изменить опрос | `_formRating.php` | `NAME`, `CONTENT` |
| Добавить / Изменить вопрос | `_formQuestion.php` | `CONTENT` (per `RATING_ID`) |
| Получить ссылку | `_formLink.php` | `RATING_ID`, list of clients to attach |
| Привязать клиента | `_formClientLink.php` | `CLIENT_ID`, `RATING_ID` |
| Голоса | `_viewVoters.php` | read-only list of voters & comments |

## Grid columns

The poll list is a card-based render (not a tabular grid). Each rating card shows:

| # | Field | Source |
|---|---|---|
| 1 | Poll name | `rating.NAME` |
| 2 | Created at | `rating.CREATED_AT` (formatted via `dateFormat` filter) |
| 3 | Description | `rating.CONTENT` |
| 4 | Question text | `question.CONTENT` (one row per question) |
| 5 | Vote count | `question.VOTE_COUNT` |
| 6 | Average rating | `question.VOTE_AVG` (1–5 stars) |

## Actions

- Создать опрос
- Настройки (dropdown)
  - Изменить
  - Удалить
  - Добавить вопрос
  - Получить ссылку
- Per-question dropdown
  - Изменить
  - Удалить
- Голоса (click vote count badge to view voters)

## Backend route

- **Controller file**: `protected/modules/rating/controllers/IndexController.php`
- **Action**: `actionIndex` — renders `index` view
- **Sibling JSON endpoints**: `actionData`, `actionFetchRating`, `actionFetchClient`, `actionHashClient`, `actionUnHashClient`, `actionCreateUpdateRating`, `actionCreateUpdateQuestion`, `actionDeleteRating`, `actionDeleteQuestion`, `actionViewVoters`
- **Required permission**: module-level access (no explicit `H::access`); behaves as admin-only because the Yii route is gated by the access filter chain configured in `RatingModule`

## See also

- Module reference: [/modules/rating](/docs/modules/rating)
- Pages index: [/ui/pages/rating](./index.md)
