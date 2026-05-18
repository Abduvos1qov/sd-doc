---
title: "Статьи и фонды расходов/приходов"
audience: All sd-main developers, QA
summary: Live admin page at /finans/consumption/category
topics: [finans, page, ui]
---

# Статьи и фонды расходов/приходов

**URL**: `/finans/consumption/category` · **Module**: `finans` · **Controller**: `ConsumptionController::category` · **RBAC**: `operation.finans.consumptionCategory`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Catalog manager for expense / income categories. Has two tabs — Статьи (articles, the child level) and Фонды (funds, the parent level). System-flagged rows are hidden; a fund or article that is referenced by any consumption row cannot be deleted.

## Fields

Fund add/edit modal (modal-parent / modal-parent_add):

| Label | Name | Type | Required |
|---|---|---|---|
| Название | `parent` | text | yes |
| Сортировка | `sort` | numeric | no |
| Активность | `active_parent` | checkbox | no |

Article add/edit modal (modal-child / modal-child_add):

| Label | Name | Type | Required |
|---|---|---|---|
| Фонд | `parent` | select | yes |
| Название | `child` (name) | text | yes |
| Сортировка | `sort` | numeric | no |
| Активность | `active_child` | checkbox | no |

Filter:

| Label | Name | Type |
|---|---|---|
| Активность (Активный / Неактивный) | `active_` | select |

## Grid columns

Tab Статьи (#stattable):

| # | Column |
|---|---|
| 1 | Фонд |
| 2 | Статья |
| 3 | Сортировка |
| 4 | Активность |
| 5 | (actions) |

Tab Фонды (#fondtable):

| # | Column |
|---|---|
| 1 | Фонд |
| 2 | Сортировка |
| 3 | Активность |
| 4 | (actions) |

## Actions

- Добавить новую статью
- Добавить новый фонд
- Изменить (per-row)
- Удалить (per-row, hidden when row is referenced)
- Закрыть / Добавить / Изменить (modal footers)

## Backend route

- **Controller file**: `protected/modules/finans/controllers/ConsumptionController.php` (line 270)
- **Action kind**: inline
- **View rendered**: `category`
- **Required permission**: `operation.finans.consumptionCategory`

## See also

- Module reference: [/modules/finans](/docs/modules/finans)
- Parent page: [/ui/pages/finans/finans_index](./finans_index)
