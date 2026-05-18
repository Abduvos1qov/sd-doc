---
title: "Движения денежных средств"
audience: All sd-main developers, QA
summary: Live admin page at /finans/consumption/report
topics: [finans, page, ui, cashflow]
---

# Движения денежных средств

**URL**: `/finans/consumption/report` · **Module**: `finans` · **Controller**: `ConsumptionController::report` · **RBAC**: `operation.finans.consumptionReport`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Cash flow report (Движения денежных средств). Shows starting balance, all Приход lines drilled down by fund/article/client, all Расход lines, plus client payouts, and the ending balance — one column per currency plus a total column.

## Fields

| Label | Name | Type |
|---|---|---|
| Касса | `cashbox` | select (single) |
| Тип даты (Дата платежа / Дата изменения) | `date_type` | select |
| Период | `datestart` / `endstart` | date-range |

## Grid columns

| # | Column |
|---|---|
| 1 | Статья движения денежных средств |
| 2..N | (one column per active currency) |
| N+1 | Общий итог |

Row sections rendered in order:

- Остаток на начало периода
- Приход — Оплата клиента → (per client breakdown)
- Приход — Прочие приходы (касса) → (per fund / per article)
- Расход → (per fund / per article)
- Выплата клиенту → (per client breakdown)
- Остаток на конец периода
- Сумма оборотов за период (tfoot)

## Actions

- Фильтр
- Детальный отчет (pivot) — links to `/finans/consumption/pivot`
- Download to Excel (exceljs export)

## Backend route

- **Controller file**: `protected/modules/finans/controllers/ConsumptionController.php` (line 344)
- **Action kind**: inline
- **View rendered**: `report`
- **Required permission**: `operation.finans.consumptionReport`

## See also

- Module reference: [/modules/finans](/docs/modules/finans)
- Pivot variant: [/ui/pages/finans/finans_pivot](./finans_pivot)
