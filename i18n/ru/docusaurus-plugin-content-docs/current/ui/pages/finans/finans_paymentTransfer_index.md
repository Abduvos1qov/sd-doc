---
title: "Перевод денежных средств между филиалами"
audience: All sd-main developers, QA
summary: Live admin page at /finans/paymentTransfer/index
topics: [finans, page, ui, transfer]
---

# Перевод денежных средств между филиалами

**URL**: `/finans/paymentTransfer/index` · **Module**: `finans` · **Controller**: `PaymentTransferController::index` · **RBAC**: `operation.finans.paymenttransfer` (resolved via `User::checkAccess`)

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Vue 3 / Vuetify screen for inter-branch (filial) payment transfers. Composed of partials — `main-header`, `main-table`, `table-filters`, `create-modal` — and several useXxx composables for state. Supports a request → accept / reject / cancel state machine.

## Fields

Filters partial (`table-filters.php`):

| Label | Name | Type |
|---|---|---|
| Филиалы | `filial_ids` | multi-select |
| Способ оплаты | `currency_ids` | multi-select |
| Операции | `direction_ids` | multi-select |
| Статус | `status` | select |
| Период | filter-by-date | date-range |

Create modal (`create-modal.php`):

field-extraction pending — modal renders via the `useCatalog` / `useCashboxCashier` composables; visible inputs include filial / cashbox-cashier / direction / currency / sum / комментарий.

## Grid columns

`main-table.php` v-data-table, columns defined in `tableHeaders`:

| # | Column |
|---|---|
| 1 | Документ ИД |
| 2 | Операции |
| 3 | Филиалы |
| 4 | Способ оплаты |
| 5 | Сумма |
| 6 | Комментарий |
| 7 | Причина отказа |
| 8 | Статус |
| 9 | Дата создания |
| 10 | Создал |
| 11 | Дата изменения |
| 12 | Изменил |

## Actions

- Сделать перевод (opens create modal)
- Принять (per-row, accepts a pending transfer)
- Отклонить (per-row, opens "Причина отказа" prompt)
- Отменить (per-row, opens cancel confirmation)
- Распределение денег (modal — money allocation across cashboxes)
- Excel export (exportFileName = "Перевод денежных средств между филиалами")

## Backend route

- **Controller file**: `protected/modules/finans/controllers/PaymentTransferController.php` (line 23)
- **Action kind**: inline
- **View rendered**: `index` (composes the partials listed in Purpose)
- **Required permission**: routed through `User::checkAccess($module, $controller, $action)`

## See also

- Module reference: [/modules/finans](/docs/modules/finans)
- Branch / filial directory: [/modules/branches](/docs/modules/branches)
