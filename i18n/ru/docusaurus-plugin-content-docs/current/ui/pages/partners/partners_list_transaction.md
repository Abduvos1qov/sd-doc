---
title: "Транзакции партнёров"
audience: All sd-main developers, QA
summary: Admin page at /partners/list/transaction — partner balances and debt/payment entry
topics: [partners, finans, page, ui]
---

# Транзакции партнёров

**URL**: `/partners/list/transaction` · **Module**: `partners` · **Controller**: `ListController::transaction` · **RBAC**: module-level (same access filter as the partners list) · **Role harvested**: `admin`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Shows a per-partner balance grid across every active currency, with one column per currency. Per row the admin can launch two modals: **Долг** (record a new debt for the partner) and **Оплата** (record an incoming payment). Each submission inserts a `ClientTransaction` row, then either updates the matching `ClientFinans` balance (legacy mode) or calls `ClientTransaction::correct_finans` (contragent mode — toggled by `ServerSettings::isContragent()`).

## Fields (modal forms — Долг and Оплата)

| Label | Name | Type | Required |
|---|---|---|---|
| Партнёр | `PARTNER_ID` | select (pre-filled from row) | yes |
| Тип | `TYPE` | select (2 = долг, 3 = оплата) | yes |
| Дата | `DATE` | date (yyyy-mm-dd) | yes |
| Срок (only on Долг modal) | `DATE_EXP` | date | no |
| Сумма по валюте | `SUMMA[<CURRENCY_ID>]` | numeric (one input per currency) | at least one |
| Курс валют | `CURRENCY_RATE` | numeric | no |
| Конвертация | `CONVERTATION` | numeric | no |
| Комиссионный | `COMISSION` | numeric | no |
| Комментарии | `COMMENT` | textarea | no |

## Grid columns

| # | Column | Source |
|---|---|---|
| 1 | Название партнера | `User.NAME` (link to `/partners/list/Detail/client/<USER_ID>`) |
| 2..N | One column per currency | `ClientFinans.BALANS` for that currency (0 if none) |
| Last | Actions | "Долг" + "Оплата" buttons |

## Actions

- Долг (per row) — opens `#modal-responsive-vdolg`, posts to `actionTransaction` with `name=dolg` (creates `ClientTransaction` with negative summa, TYPE=2, TRANS_TYPE=2)
- Оплата (per row) — opens `#modal-responsive-vozvrat`, posts to `actionTransaction` with `name=vozvrat` (positive summa, TYPE=2, TRANS_TYPE=3)
- Excel export (DataTable buttons): pageLength, colvis, Excel
- Click partner name — navigates to per-partner detail page

## Backend route

- **Controller file**: `protected/modules/partners/controllers/ListController.php`
- **Action**: `actionTransaction` (line 261) — renders `transaction_list` view; same action also processes the modal POST submissions
- **Required permission**: module-level (inherits the access filter the controller sets in `accessRules`)
- **Server toggle**: `ServerSettings::isContragent()` switches finans-update path between legacy `ClientFinans::correct` and contragent-aware `ClientTransaction::correct_finans`

## See also

- Module reference: [/modules/partners](/docs/modules/partners)
- Partner detail page: [/ui/pages/partners/partners_list_detail](./partners_list_detail.md)
- Order → Finans → Payment → Stock flow: [/flows/order-finans-payment-stock](/docs/flows/order-finans-payment-stock)
