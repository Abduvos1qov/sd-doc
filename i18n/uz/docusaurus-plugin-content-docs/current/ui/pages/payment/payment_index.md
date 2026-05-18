---
title: "Подтверждение оплаты"
audience: All sd-main developers, QA
summary: Payment approval queue for finance staff at /payment/approval
topics: [payment, approval, page, ui]
---

# Подтверждение оплаты

**URL**: `/payment/approval` · **Module**: `payment` · **Controller**: `ApprovalController::index` · **RBAC**: `operation.clients.paymentApproval` · **Role harvested**: `admin`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Finance approval queue: cashiers and supervisors review unconfirmed `PaymentDeliver` records, edit amount or currency, then confirm (creates a `ClientTransaction` of `TRANS_TYPE=3`) or reject (sets `CONFIRM=2`). Filtered by date range and role-based slicing (agent, expeditor, cashier).

## Fields

Top-of-page filter strip (built dynamically by the `filter.store`):

| Label | Name | Type | Required |
|---|---|---|---|
| Период | `rangeOfDate` | date-range picker | no |
| Роль | `role` | select (single) | no |
| Плательщик | `user` | select (multi) | no |
| Агент | `agent` | select (multi) | no |
| Клиент | `client` | select (multi) | no |
| Территория | `city` | select (multi) | no |
| Способ оплаты | `currency` | select (multi) | no |
| Направление торговли | `trade` | select (multi) | no |
| Баланс виден / Баланс скрыт | `showClientBalance` | switch | no |

The "Изменить сумму" modal (`_edit-payment-summa.php`) exposes:

| Label | Name | Type | Required |
|---|---|---|---|
| Сумма | `summa` | number | yes |
| Способ оплаты | `currency_id` | select | yes |
| Комментарий | `comment` | text | no |

The "Подтверждение" modal (`_confirmation-modal.php`) collects per-payment overrides plus shared header fields:

| Label | Name | Type | Required |
|---|---|---|---|
| Дата подтверждения | `date` | date | yes |
| Использовать дату платежа | `date_pay` | checkbox | no |
| Касса | `cashbox` | select | no |
| Курс USD | `usd_rate` | number | when multi-currency |
| Фирма | `firm_id` | select | when multi-firm |

Field-extraction pending for any per-row inline editors not enumerated above.

## Grid columns

| # | Column |
|---|---|
| 1 | Дата оплаты |
| 2 | Роль |
| 3 | Плательщик |
| 4 | Статус оплаты |
| 5 | Агент |
| 6 | Клиент |
| 7 | Территория |
| 8 | Заказ |
| 9 | Сумма |
| 10 | Способ оплаты |
| 11 | Направление торговли |
| 12 | Комм. |
| 13 | Изменено |
| 14 | Подтверждено клиентом |
| 15 | Действия (only when `editPaymentDeliver` toggle is on) |

Footer row aggregates `Сумма` (sum of selected rows, or all visible rows if none selected) and labels the leading cell `Итоги`.

## Actions

- Загрузить (reload payments for the selected date range)
- Подтверждение (opens confirmation modal; requires `operation.clients.finansCreate`)
- Удалить оплаты (soft-delete: sets `CONFIRM=2`; requires `operation.clients.finansDelete`)
- Импорт оплат (visible only when role filter is `expeditor`) with sub-menu:
  - Импортировать оплаты (ИД)
  - Импортировать оплаты (КОД)
  - Импортировать оплаты (ИНН)
  - Импортировать оплаты (ПИНФЛ)
  - Импортировать оплаты (Расчётный счёт)
- Баланс виден / Баланс скрыт (toggle client-balance column)
- Изменить сумму (per-row; opens edit-payment-summa modal; visible when `editPaymentDeliver` server flag is enabled)
- Открепить отменённые заказы (appears when cancelled orders are present in the loaded set; calls `unlinkOrder`)
- Excel export (provided by `vue-data-table` toolbar)

## Backend route

- **Controller file**: `protected/modules/payment/controllers/ApprovalController.php` (line 5)
- **Action kind**: inline render
- **View rendered**: `index`
- **Required permission**: `operation.clients.paymentApproval`

Companion AJAX endpoints on the same controller (not user-facing pages):

| Endpoint | Method | Purpose |
|---|---|---|
| `/payment/approval/getData` | GET | Returns raw `PaymentDeliver` rows for the range |
| `/payment/approval/getOrders` | POST | Resolves linked `ClientTransaction` rows for a set of payments |
| `/payment/approval/getAccesses` | GET | Returns `{delete, update, list, editPaymentDeliver}` flags |
| `/payment/approval/updatePaymentDeliver` | POST | Persists edits from the "Изменить сумму" modal |
| `/payment/approval/save` | POST | Confirms payments; creates `ClientTransaction` rows |
| `/payment/approval/delete` | POST | Soft-deletes payments (`CONFIRM=2`) |
| `/payment/approval/unlinkOrder` | POST | Clears `ORDER_ID` for cancelled-order payments |

## See also

- Module reference: [/modules/payment](/docs/modules/payment)
- Cross-module flow: [order to finans to payment to stock](/docs/concepts/flows/order-to-finans-to-payment-to-stock)
- Routes inventory: [`static/data/routes.json`](/data/routes.json)
- Page-to-module map: [/quality/page-to-module-map](/docs/quality/page-to-module-map)
