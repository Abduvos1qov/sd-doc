---
title: "Рейтинги (public poll page)"
audience: All sd-main developers, QA
summary: Public unauthenticated page at /rating/poll?hash=… — clients submit ratings
topics: [rating, page, ui, public]
---

# Рейтинги (public poll page)

**URL**: `/rating/poll?hash=<hash>` · **Module**: `rating` · **Controller**: `PollController::index` · **RBAC**: none (public, hash-gated) · **Layout**: `//layouts/blank`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Public-facing poll page rendered without a login. The `hash` URL parameter encodes the rating template plus client identity (produced by `Rating::HashClient` server-side). Visitor sees the poll name and questions, clicks a star (1–5) per question, and optionally leaves a free-text comment. The page uses the blank layout (no admin chrome).

## Fields

| Label | Name | Type | Required |
|---|---|---|---|
| Star rating per question | `question.RESULT` (1–5) | click | yes |
| Оставить комментарий | `rating.COMMENT` | textarea | no |

## Grid columns

This page is a form, not a list. Each question renders as a list item with the star control:

| # | Field | Source |
|---|---|---|
| 1 | Question text | `question.CONTENT` |
| 2 | Current value | `question.RESULT` |
| 3 | Stars 1..5 | clickable rating control |

## Actions

- Click a star (1..5) per question — calls `poll.Vote(question, star)` which POSTs to `actionVote`
- Отправить — calls `poll.Comment()` which POSTs the comment to `actionComment`

Once any vote is recorded, a thank-you note appears at the top showing the aggregated average score (`poll.avg`).

## Backend route

- **Controller file**: `protected/modules/rating/controllers/PollController.php`
- **Action**: `actionIndex` — sets `layout = '//layouts/blank'` and renders `index` view
- **Sibling JSON endpoints**: `actionFetchRating`, `actionVote`, `actionComment` (all read the `hash` GET parameter)
- **Required permission**: none — public route; access is gated only by the hash being valid

## See also

- Module reference: [/modules/rating](/docs/modules/rating)
- Pages index: [/ui/pages/rating](./index.md)
