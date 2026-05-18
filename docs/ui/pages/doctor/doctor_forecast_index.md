---
title: "Forecast"
audience: All sd-main developers, QA
summary: Admin page at /doctor/forecast — outlet-level sales forecast
topics: [doctor, forecast, page, ui]
---

# Forecast

**URL**: `/doctor/forecast` · **Module**: `doctor` · **Controller**: `ForecastController::index` · **RBAC**: `operation.doctor.outlet` · **Role harvested**: `admin`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Outlet-level sales forecast. Shows for every outlet the historical sales volume, a computed forecast for the next period, and per-category breakdown. A v2 layout (`actionIndex2` → `index_new.php`) is available for the refactored view, and `actionDetail` opens a deep dive for a single outlet.

## Fields

| Label | Name | Type | Required |
|---|---|---|---|
| Период | filter | select | yes |
| Категория продуктов | filter | select | no |
| Регион | filter | select | no |
| Супервайзер | filter | select | no |
| Агент | filter | select | no |
| Outlet | filter | select | no |

## Grid columns

| # | Column |
|---|---|
| 1 | Outlet |
| 2 | Регион |
| 3 | Категория клиента |
| 4 | Факт (период −2) |
| 5 | Факт (период −1) |
| 6 | Прогноз (текущий) |
| 7 | План |
| 8 | Расхождение |
| 9 | Действия |

## Actions

- Применить фильтр
- Детализация (`actionDetail` → `detail.php`)
- Просмотр (`actionIndex2` → `index_new.php`)
- Volume категории (`actionVolumeCategory` → `volume_category.php`)
- Excel export

## Backend route

- **Controller file**: `protected/modules/doctor/controllers/ForecastController.php`
- **Actions**: `actionIndex` (line 45), `actionIndex2` (line 368), `actionDetail` (line 713), `actionDetailAjax`, `actionVolumeCategory`, `actionTest`
- **Required permission**: `H::access('operation.doctor.outlet')`

## See also

- Module reference: [/modules/doctor](/docs/modules/doctor)
- Pages index: [/ui/pages/doctor](./index.md)
