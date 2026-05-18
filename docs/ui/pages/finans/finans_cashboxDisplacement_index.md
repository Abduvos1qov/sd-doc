---
title: "Перемещение между кассами"
audience: All sd-main developers, QA
summary: Live admin page at /finans/cashboxDisplacement/index
topics: [finans, page, ui, cashbox]
---

# Перемещение между кассами

**URL**: `/finans/cashboxDisplacement/index` · **Module**: `finans` · **Controller**: `CashboxDisplacementController::index` · **RBAC**: `operation.finans.cashboxdisplacement`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Cashbox-to-cashbox displacement screen — register and reverse transfers of cash between the tenant's cashboxes, with optional currency conversion (`cashDispWithCurrs` param).

## Fields

Filter bar:

| Label | Name | Type |
|---|---|---|
| Валюта | `currency[]` | multi-select |
| Из кассы | `cashboxfrom[]` | multi-select |
| В кассу | `cashboxto[]` | multi-select |
| Кто создал | `user[]` | multi-select |
| Период | `datestart` / `endstart` | date-range |

Create modal (modal-add):

| Label | Name | Type | Required |
|---|---|---|---|
| Перемещение из | `cashbox_from` | select | yes |
| Из валюты | `currency_from` | select | conditional (`cashDispWithCurrs`) |
| Перемещение в | `cashbox_to` | select | yes |
| В валюту | `currency_to` | select | conditional (`cashDispWithCurrs`) |
| Дата | `datetime` | datetime | yes |
| Валюта | `currency` | select | conditional (single-currency mode) |
| Курс (из) | `currency_from_rate` | numeric | conditional |
| Курс (в) | `currency_to_rate` | numeric | conditional |
| Сумма (из) | `summa_from` | numeric | yes |
| Сумма (в) | `summa_to` | numeric | conditional |
| Комментарии | `comment` | textarea | no |

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
| 9 | (actions) |

## Actions

- Создать (opens add modal — requires `operation.finans.cashboxdisplacementAdd`)
- Фильтр
- Отмена (per-row, requires `operation.finans.cashboxdisplacementCancel`; shows "Отменено" if already cancelled)
- Закрыть / Да / Нет (modal footers)

## Backend route

- **Controller file**: `protected/modules/finans/controllers/CashboxDisplacementController.php` (line 21)
- **Action kind**: inline
- **View rendered**: `index`
- **Required permission**: `operation.finans.cashboxdisplacement`

## See also

- Module reference: [/modules/finans](/docs/modules/finans)
- History variant: [/ui/pages/finans/finans_cashboxDisplacement_view](./finans_cashboxDisplacement_view)
