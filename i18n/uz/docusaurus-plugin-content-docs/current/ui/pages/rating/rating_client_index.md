---
title: "Список клиентов (Rating)"
audience: All sd-main developers, QA
summary: Admin page at /rating/client — browse client-level ratings
topics: [rating, page, ui]
---

# Список клиентов (Rating)

**URL**: `/rating/client` · **Module**: `rating` · **Controller**: `ClientController::index` · **RBAC**: module-level · **Role harvested**: `admin`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Lists every client that has at least one rating record, with their aggregated vote count, comment count, average rating, and a per-client "Get link" button to share a poll URL. Used by supervisors to see who already responded and what their overall sentiment looks like.

## Fields (filter row)

| Label | Name | Type | Required |
|---|---|---|---|
| Быстрый поиск | `q` | text | no |

The top-right summary panel shows the cumulative `COMMENT_COUNT`, `VOTE_COUNT`, and `VOTE_AVG` across all clients.

## Grid columns

| # | Column | Source |
|---|---|---|
| 1 | (link button) | per-row action — `client.GetLink(CLIENT_ID)` |
| 2 | Код | `CLIENT_ID` |
| 3 | Название | `NAME` |
| 4 | Менеджер | `AGENT` |
| 5 | Комментарии | `COMMENT_COUNT` |
| 6 | Ответов | `VOTE_COUNT` |
| 7 | Оценка | `VOTE_AVG` (1–5 stars) |

## Actions

- Найти (form submit, populates `client.q`)
- Получить ссылку (per row) — opens `_formClientLink` modal
- Открыть рейтинги клиента (click on комментариев / ответов / оценка badges) — opens `_viewClientRatings` modal

## Backend route

- **Controller file**: `protected/modules/rating/controllers/ClientController.php`
- **Action**: `actionIndex` — renders `index` view
- **Sibling JSON endpoints**: `actionFetchClient`, `actionFetchRating`, `actionFetchRatingAll`, `actionFetchTotal`
- **Required permission**: module-level access

## See also

- Module reference: [/modules/rating](/docs/modules/rating)
- Pages index: [/ui/pages/rating](./index.md)
