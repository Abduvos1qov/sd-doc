---
title: "P&L"
audience: All sd-main developers, QA
summary: Live admin page at /finans/pnl/index
topics: [finans, page, ui, pnl]
---

# P&L

**URL**: `/finans/pnl/index` (alias `/finans/pnl`) · **Module**: `finans` · **Controller**: `PnlController::index` · **RBAC**: `operation.finans.pnl`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Tenant Profit & Loss summary. Rolls up cost, revenue and gross profit for the selected period plus operating expenses, written-off bad debts and other cash receipts to produce an operating profit. Has two drill-down tables — "По статьям" (by sales model) and "По категории товаров" (by product category).

## Fields

| Label | Name | Type |
|---|---|---|
| Категории продуктов | `productCat[]` | multi-select |
| Склад | `warehouses[]` | multi-select |
| Период | `datestart` / `endstart` | date-range |
| Не учитывать прочие приходы | `minusOthers` | checkbox |

## Grid columns

P&L summary table:

| # | Column |
|---|---|
| 1 | Статья |
| 2 | Сумма |

Rows: Себестоимость, Выручка, Валовая прибыль, Операционные расходы (expandable), Списанные долги (expandable), Прочие приходы в кассу (expandable), Операционная прибыль.

По статьям table:

| # | Column |
|---|---|
| 1 | Статья |
| 2 | Себестоимость |
| 3 | Выручка |
| 4 | Валовая прибыль |

По категории товаров table:

| # | Column |
|---|---|
| 1 | Категория |
| 2 | Себестоимость |
| 3 | Выручка |
| 4 | Валовая прибыль |

## Actions

- Фильтр
- P&L по продажам — links to `/finans/agentPnl`
- P&L по товарам — links to `/finans/pivotPnl?type=product`
- EXCEL (per-panel exports — PNL, По статьям, По категории товаров)
- Click on "Операционные расходы" / "Списанные долги" / "Прочие приходы в кассу" — fetches details inline via `/finans/pnl/getConsumptions` and `/finans/pnl/getBadDebts`

## Backend route

- **Controller file**: `protected/modules/finans/controllers/PnlController.php` (line 32)
- **Action kind**: inline (data prepared in controller, view rendered at line 159)
- **View rendered**: `index`
- **Required permission**: `operation.finans.pnl`

## See also

- Module reference: [/modules/finans](/docs/modules/finans)
- Agent-level drilldown: [/ui/pages/finans/finans_agentPnl_index](./finans_agentPnl_index)
- Product-level pivot: [/ui/pages/finans/finans_pivotPnl_byproduct](./finans_pivotPnl_byproduct)
