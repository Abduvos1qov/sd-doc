---
title: "Движения денежных средств — детальный отчёт"
audience: All sd-main developers, QA
summary: Live admin page at /finans/consumption/pivot
topics: [finans, page, ui, pivot]
---

# Движения денежных средств (pivot)

**URL**: `/finans/consumption/pivot` · **Module**: `finans` · **Controller**: `ConsumptionController::pivot` · **RBAC**: `operation.finans.consumption`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

WebDataRocks-driven interactive pivot of the cash-flow data behind the `/finans/consumption/report` page. Lets the user save/load custom templates and reorganise rows, columns and measures live.

## Fields

| Label | Name | Type | Required |
|---|---|---|---|
| Название отчёта | `report_name` | text | yes (on save) |
| Период / catalog selectors | — | field-extraction pending (rendered inside `pivotFilter.php`) | — |

## Grid columns

| # | Column |
|---|---|
| 1 | — (pivot grid; columns and rows are user-configurable via WebDataRocks toolbar) |

field-extraction pending — pivot dimensions and measures are configured by the WDR slice on the client.

## Actions

- Изменить название (отчёта)
- Сохранить изменения
- Удалить отчёт
- Выберите отчёт для просмотра (open-report modal)
- Введите название отчёта (save-report modal)
- WDR toolbar: Save, Open, Export to Excel / HTML / CSV / PDF, Charts

## Backend route

- **Controller file**: `protected/modules/finans/controllers/ConsumptionController.php` (line 684)
- **Action kind**: inline
- **View rendered**: `pivot`
- **Required permission**: `operation.finans.consumption`

## See also

- Module reference: [/modules/finans](/docs/modules/finans)
- Tabular cash flow: [/ui/pages/finans/finans_report](./finans_report)
