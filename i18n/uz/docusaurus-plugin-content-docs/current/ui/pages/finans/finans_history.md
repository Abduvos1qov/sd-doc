---
title: "История обновлений/удалений расходов"
audience: All sd-main developers, QA
summary: Live admin page at /finans/consumption/history
topics: [finans, page, ui, audit]
---

# История обновлений/удалений расходов

**URL**: `/finans/consumption/history` · **Module**: `finans` · **Controller**: `ConsumptionController::history` · **RBAC**: `operation.finans.consumption`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Audit log for consumption rows — shows every UPDATE, DELETE and CREATE event with old / new values rendered inline (red for removed, green for added). Useful for QA and reconciling reported numbers.

## Fields

Filter bar:

| Label | Name | Type |
|---|---|---|
| Период | `datestart` / `endstart` | date-range |
| Фонд | `parent[]` | multi-select |
| Статья расхода | `child[]` | multi-select |
| Касса | `cashbox[]` | multi-select |
| Способ оплаты (Валюта) | `currency[]` | multi-select |

## Grid columns

| # | Column |
|---|---|
| 1 | ИД |
| 2 | Тип действия (Обновление / Удаление / Создание) |
| 3 | Фонд |
| 4 | Статья расхода |
| 5 | Касса |
| 6 | Сумма |
| 7 | Валюта |
| 8 | Дата расхода |
| 9 | Дата изм. |
| 10 | Кто добавил |
| 11 | Кто изм. |
| 12 | Операционные |
| 13 | Тип (Приход / Расход) |
| 14 | Комментарий |

## Actions

- Фильтр
- (No mutations from this page — read-only audit view)

## Backend route

- **Controller file**: `protected/modules/finans/controllers/ConsumptionController.php` (line 924)
- **Action kind**: inline
- **View rendered**: `history`
- **Required permission**: `operation.finans.consumption`

## See also

- Module reference: [/modules/finans](/docs/modules/finans)
- Parent screen: [/ui/pages/finans/finans_index](./finans_index)
