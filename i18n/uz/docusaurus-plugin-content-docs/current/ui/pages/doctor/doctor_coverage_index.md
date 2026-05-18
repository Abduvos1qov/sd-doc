---
title: "Coverage planning"
audience: All sd-main developers, QA
summary: Admin page at /doctor/coverage — set client-coverage targets per agent/supervisor
topics: [doctor, coverage, page, ui]
---

# Coverage planning

**URL**: `/doctor/coverage` · **Module**: `doctor` · **Controller**: `CoverageController::index` · **RBAC**: `operation.doctor.outlet` (typical) · **Role harvested**: `admin`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Defines the coverage plan — how many of the client base each agent must physically visit per period — and pushes those targets to agents and supervisors. Includes a recommendation engine (`actionRecommend`) that suggests plan values based on history.

## Fields

| Label | Name | Type | Required |
|---|---|---|---|
| Период | filter | select | yes |
| Регион | filter | select | no |
| Категория клиента | filter | select | no |
| Супервайзер | filter | select | no |
| План покрытия | `PLAN` | numeric | yes (per agent on submit) |

The render call passes `Spravochnik`, `region`, and `last_plan` to the `index` view.

## Grid columns

| # | Column |
|---|---|
| 1 | Регион |
| 2 | Супервайзер |
| 3 | Агент |
| 4 | АКБ |
| 5 | Факт (предыдущий период) |
| 6 | План (текущий период) |
| 7 | Рекомендация |
| 8 | Действия |

## Actions

- Применить фильтр
- Рекомендовать (calls `actionRecommend`)
- Поделиться с агентами — `actionShareToAgents` opens `share_to_agents`
- Сохранить
- Сбросить

## Backend route

- **Controller file**: `protected/modules/doctor/controllers/CoverageController.php`
- **Actions**: `actionIndex` (line 48), `actionShareToAgents` (line 137), `actionReturnAjaxAgent`, `actionReturnAjaxSpv`, `actionRecommend`, `actionAgentAjax`, `actionSpvAjax`
- **Required permission**: `operation.doctor.outlet` (or coverage-specific RBAC node)

## See also

- Module reference: [/modules/doctor](/docs/modules/doctor)
- Pages index: [/ui/pages/doctor](./index.md)
