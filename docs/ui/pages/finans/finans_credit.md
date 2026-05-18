---
title: "Приходы"
audience: All sd-main developers, QA
summary: Live admin page at /finans/consumption/credit
topics: [finans, page, ui]
---

# Приходы

**URL**: `/finans/consumption/credit` · **Module**: `finans` · **Controller**: `ConsumptionController::credit` · **RBAC**: `operation.finans.credit`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Income (Приходы) register, mirrors the expense screen but for cash receipts. Rows that originate from a cashbox displacement are flagged and can only be cancelled, not edited.

## Fields

Add/Edit modal (modal-update / modal-consum):

| Label | Name | Type | Required |
|---|---|---|---|
| Фонд | `cat_parent` | select | yes |
| Статья прихода | `cat_child` | select | yes |
| Сумма | `summa` | numeric | yes |
| Дата | `date` | date | yes |
| не учитывать в PNL | `exclude_pnl` | checkbox | no |
| Валюта | `currency` | select | yes |
| Касса | `cashbox` | select | yes |
| Комментарий | `comment` | textarea | no |

Filter bar:

| Label | Name | Type |
|---|---|---|
| Фонд | `parent[]` | multi-select |
| Статья расхода | `child[]` | multi-select |
| Валюта | `currency[]` | multi-select |
| Период | `datestart` / `endstart` | date-range |

## Grid columns

| # | Column |
|---|---|
| 1 | (checkbox) |
| 2 | Фонд |
| 3 | Статья прихода |
| 4 | Касса |
| 5 | Сумма |
| 6 | Валюта |
| 7 | Дата |
| 8 | Комментарий |
| 9 | (actions) |

## Actions

- Добавить (requires `operation.finans.editcredit`)
- Фильтр
- Экспортировать оплаты (ПКО) (only when country code is KG)
- Изменить (per-row, requires `operation.finans.editcredit`, only for non-displacement entries)
- Удалить (per-row, requires `operation.finans.deletecredit`)
- Отменить (per-row for displacement-sourced entries, requires `operation.finans.cashboxdisplacementCancel`)
- Итоги по приходам

## Backend route

- **Controller file**: `protected/modules/finans/controllers/ConsumptionController.php` (line 173)
- **Action kind**: inline
- **View rendered**: `credit`
- **Required permission**: `operation.finans.credit`

## See also

- Module reference: [/modules/finans](/docs/modules/finans)
- QA workflows: [/quality/finans](/docs/quality/finans/finans-qa)
