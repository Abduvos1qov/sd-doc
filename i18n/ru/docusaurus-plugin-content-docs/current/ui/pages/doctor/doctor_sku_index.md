---
title: "SKU plan"
audience: All sd-main developers, QA
summary: Admin page at /doctor/sku — set per-SKU sales targets per agent
topics: [doctor, sku, page, ui]
---

# SKU plan

**URL**: `/doctor/sku` · **Module**: `doctor` · **Controller**: `SkuController::index` · **RBAC**: `operation.doctor.skuPlan` · **Role harvested**: `admin`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Sets per-SKU sales targets (must-stock list, focus SKUs) for every agent. Per agent the admin picks the SKUs that count toward the plan; the agent's mobile app then tracks fact vs plan and the daily/period summary feeds the supervisor dashboard.

## Fields

| Label | Name | Type | Required |
|---|---|---|---|
| Период | filter | select | yes |
| Категория продуктов | filter | select | no |
| Регион | filter | select | no |
| Супервайзер | filter | select | no |
| Агент | filter | select | no |
| SKU list | multi-select | checkbox/select | yes |

## Grid columns

| # | Column |
|---|---|
| 1 | Агент |
| 2 | Территория |
| 3 | Количество SKU в плане |
| 4 | Факт (предыдущий период) |
| 5 | Расхождение |
| 6 | Действия |

## Actions

- Применить фильтр
- Просмотр (`actionView` → `view.php`)
- Поделиться с агентами (`actionShareToAgents` → `share_to_agents.php`)
- Сохранить
- Сбросить

## Backend route

- **Controller file**: `protected/modules/doctor/controllers/SkuController.php`
- **Actions**: `actionIndex` (line 49), `actionView` (line 138), `actionReturnAjax`, `actionReturnAjaxPageLoad`, `actionReturnAjaxView`
- **Required permission**: `H::access('operation.doctor.skuPlan')`

## See also

- Module reference: [/modules/doctor](/docs/modules/doctor)
- Pages index: [/ui/pages/doctor](./index.md)
