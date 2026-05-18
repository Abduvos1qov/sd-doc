---
title: "Расходы"
audience: All sd-main developers, QA
summary: Live admin page at /finans/consumption/index
topics: [finans, page, ui]
---

# Расходы

**URL**: `/finans/consumption/index` (alias `/finans/consumption`) · **Module**: `finans` · **Controller**: `ConsumptionController::index` · **RBAC**: `operation.finans.consumption`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Main expense (Расходы) register for the tenant. Lists all consumption entries with filters by fund, expense article, cashbox and currency, and lets authorized users add, edit or delete a row. The `legend` tag of the view reads "Расходы".

## Fields

Add/Edit modal (modal-update / modal-consum):

| Label | Name | Type | Required |
|---|---|---|---|
| Фонд | `cat_parent` | select | yes |
| Статья расхода | `cat_child` | select | yes |
| Дата | `date` | datetime | yes |
| не учитывать в PNL | `exclude_pnl` | checkbox | no |
| Сумма | `summa` | numeric | yes |
| Валюта | `currency` | select | yes |
| Касса | `cashbox` | select | yes |
| Комментарий | `comment` | textarea | no |

Filter bar:

| Label | Name | Type |
|---|---|---|
| Фонд | `parent[]` | multi-select |
| Статья расхода | `child[]` | multi-select |
| Касса | `cashbox[]` | multi-select |
| Валюта | `currency[]` | multi-select |
| Тип даты (Дата расхода / Дата создания) | `dateType` | select |
| Период | `datestart` / `endstart` | date-range |

## Grid columns

| # | Column |
|---|---|
| 1 | (checkbox) |
| 2 | ИД |
| 3 | Фонд |
| 4 | Статья расхода |
| 5 | Касса |
| 6 | Сумма |
| 7 | Валюта |
| 8 | Дата расхода |
| 9 | Дата создания |
| 10 | Дата изменения |
| 11 | Кто добавил |
| 12 | Кто изменил |
| 13 | Операционные расходы |
| 14 | Комментарий |
| 15 | Код |
| 16 | (actions) |

## Actions

- Добавить (opens add modal — requires `operation.finans.addconsumption`)
- Добавить категории (links to `/finans/consumption/category`)
- История (links to `/finans/consumption/history`)
- Экспортировать РКО / Экспортировать РКО (A5) (only when formal currency is "сом")
- Фильтр
- Изменить (per-row, requires `operation.finans.editconsumption`)
- Удалить (per-row, requires `operation.finans.deleteconsumption`)
- Итоги по расходам

## Backend route

- **Controller file**: `protected/modules/finans/controllers/ConsumptionController.php` (line 37)
- **Action kind**: inline
- **View rendered**: `index`
- **Required permission**: `operation.finans.consumption`

## See also

- Module reference: [/modules/finans](/docs/modules/finans)
- QA workflows: [/quality/finans](/docs/quality/finans/finans-qa)
- Page-to-module map: [/quality/page-to-module-map](/docs/quality/page-to-module-map)
