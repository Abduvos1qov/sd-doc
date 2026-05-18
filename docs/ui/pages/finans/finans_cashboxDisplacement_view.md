---
title: "История перемещений"
audience: All sd-main developers, QA
summary: Live admin page at /finans/cashboxDisplacement/view
topics: [finans, page, ui, cashbox]
---

# История перемещений

**URL**: `/finans/cashboxDisplacement/view` · **Module**: `finans` · **Controller**: `CashboxDisplacementController::view` (rendered through `actionIndex` with view `view`) · **RBAC**: `operation.finans.cashboxdisplacement`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Vue 3 / Vuetify re-implementation of the cashbox displacement screen — a date-ranged history with per-row cancellation. Used as the "back from cashbox balance" workflow (the page header has a back-button to `/clients/finans/cashboxBalans`).

## Fields

Filter row (v-select):

| Label | Name | Type |
|---|---|---|
| Перемещение из | `filters.CB_FROM` | select |
| Перемещение к | `filters.CB_TO` | select |
| Валюта | `filters.CURRENCY` | select |
| Кто добавил | `filters.CREATE_BY` | select |
| Действие | `filters.STATUS` | select (Действующий / Отменен) |
| Период | `dateRange` | date-range |

## Grid columns

| # | Column |
|---|---|
| 1 | ИД |
| 2 | Дата |
| 3 | Перемещение из |
| 4 | Перемещение к |
| 5 | Сумма |
| 6 | Валюта |
| 7 | Кто добавил |
| 8 | Комментарий |
| 9 | Дата создания |
| 10 | Действие |

## Actions

- (Back arrow) — navigates to `/clients/finans/cashboxBalans`
- Сбросить фильтры
- Отменить (per-row, requires `operation.finans.cashboxdisplacementCancel`)
- Отменено (read-only when status === '2')

## Backend route

- **Controller file**: `protected/modules/finans/controllers/CashboxDisplacementController.php` (line 25, view rendered by `actionIndex`)
- **Action kind**: inline (renders `view` instead of `index`)
- **View rendered**: `view`
- **Required permission**: `operation.finans.cashboxdisplacement`

## See also

- Module reference: [/modules/finans](/docs/modules/finans)
- Legacy variant: [/ui/pages/finans/finans_cashboxDisplacement_index](./finans_cashboxDisplacement_index)
