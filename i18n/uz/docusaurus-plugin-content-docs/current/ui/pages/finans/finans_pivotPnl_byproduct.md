---
title: "P&L по товарам"
audience: All sd-main developers, QA
summary: Live admin page at /finans/pivotPnl/byproduct
topics: [finans, page, ui, pnl, pivot]
---

# P&L по товарам

**URL**: `/finans/pivotPnl/byproduct` (default for `/finans/pivotPnl?type=product`) · **Module**: `finans` · **Controller**: `PivotPnlController::loadByProduct` (renders `byproduct.php`) · **RBAC**: resolved via `User::checkAccess`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

WebDataRocks-backed pivot of cost / revenue / profit data sliced by product. Users can pick predefined or custom-saved report templates ("Текущий шаблон") and persist their own slices via `/finans/pivotPnl/saveReport`.

## Fields

| Label | Name | Type |
|---|---|---|
| Документы прихода | `filterByPurchaseModel` | multi-autocomplete |
| Документы расхода | `filterBySalesModel` | multi-autocomplete |
| Движения | `filterByProfit` | autocomplete |
| Период | `pickedDateRange` | date-range |
| Название отчёта | `newReportName` | text (save modal) |

## Grid columns

| # | Column |
|---|---|
| 1 | — (pivot grid rendered by WebDataRocks; rows, columns, measures defined by the active report template) |

field-extraction pending — the displayed columns vary per template; see `actionReportTemplates` for available templates.

## Actions

- Загрузить (`loadFilteredPnls`)
- Выберите отчёт для просмотра (open-report dialog)
- Сохранить (save report modal — submits to `/finans/pivotPnl/saveReport`)
- Изменить название (edit icon next to current template)
- Удалить отчёт (delete icon — `/finans/pivotPnl/deleteReport`)
- Отменить / Закрыть (modal footers)
- WDR toolbar: Save, Open, Export to Excel / HTML / CSV / PDF, Charts

## Backend route

- **Controller file**: `protected/modules/finans/controllers/PivotPnlController.php` (line 126; `actionLoadByProduct`)
- **Action kind**: inline
- **View rendered**: `byproduct`
- **Required permission**: routed through `User::checkAccess`

## See also

- Module reference: [/modules/finans](/docs/modules/finans)
- P&L summary: [/ui/pages/finans/finans_pnl_index](./finans_pnl_index)
- Agent drill-down: [/ui/pages/finans/finans_agentPnl_index](./finans_agentPnl_index)
