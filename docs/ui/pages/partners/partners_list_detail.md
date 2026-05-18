---
title: "Партнёр — детализация транзакций"
audience: All sd-main developers, QA
summary: Admin page at /partners/list/detail/client/<USER_ID> — single-partner ledger
topics: [partners, finans, page, ui]
---

# Партнёр — детализация транзакций

**URL**: `/partners/list/detail/client/<USER_ID>` · **Module**: `partners` · **Controller**: `ListController::detail` · **RBAC**: module-level · **Role harvested**: `admin`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Per-partner transaction ledger. Header shows the partner's name and the current `ClientFinans.BALANS` for every currency (positive = credit/green, negative = debt/red). Body shows every `ClientTransaction` for that partner ordered by `DATE DESC, TIMESTAMP_X DESC`, with running settlement status. Same Долг / Оплата modals as the parent transactions page are mounted at the bottom for quick entry.

## Fields (modal forms — same as parent transactions page)

| Label | Name | Type | Required |
|---|---|---|---|
| Партнёр | `PARTNER_ID` | pre-filled from URL | yes |
| Тип | `TYPE` | 2 = долг, 3 = оплата | yes |
| Дата | `DATE` | date | yes |
| Срок | `DATE_EXP` | date (only Долг modal) | no |
| Сумма по валюте | `SUMMA[<CURRENCY_ID>]` | numeric | at least one |
| Курс валют | `CURRENCY_RATE` | numeric | no |
| Конвертация | `CONVERTATION` | numeric | no |
| Комиссионный | `COMISSION` | numeric | no |
| Комментарии | `COMMENT` | textarea | no |

## Grid columns

| # | Column | Source |
|---|---|---|
| 1 | Дата | `ClientTransaction.DATE` (formatted d.m.Y) |
| 2 | Тип | "Долг" if `SUMMA < 0` else "Оплата" |
| 3 | Долг | `SUMMA` if negative, with currency symbol |
| 4 | Оплата | `SUMMA` if positive, with currency symbol |
| 5 | Комментарии | `COMMENT` |
| 6 | Расчёт | "Оплата" (green), "Расчёт" (green) or "Неоплачено (еще осталось …)" (red) — derived from `STATUS` and remaining `COMPUTATION` |

The header shows a card per currency with the running `ClientFinans.BALANS`.

## Actions

- Обратно к списку партнёров — back to `/partners/list/transaction`
- Долг — same modal as parent page; POSTs to `actionDetail`
- Оплата — same modal as parent page; POSTs to `actionDetail`
- DataTable export buttons

## Backend route

- **Controller file**: `protected/modules/partners/controllers/ListController.php`
- **Action**: `actionDetail` (line 330) — also processes POST submissions, then renders `transaction_detail` view
- **Required permission**: module-level
- **Same `isContragent()` toggle** as the parent transactions page for choosing between `ClientFinans::correct` and `ClientTransaction::correct_finans`

## See also

- Module reference: [/modules/partners](/docs/modules/partners)
- Parent transactions list: [/ui/pages/partners/partners_list_transaction](./partners_list_transaction.md)
