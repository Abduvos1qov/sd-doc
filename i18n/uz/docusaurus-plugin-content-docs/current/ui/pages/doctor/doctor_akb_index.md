---
title: "АКБ — Active Client Base plan"
audience: All sd-main developers, QA
summary: Admin page at /doctor/akb — manage the agent's Active Client Base plan
topics: [doctor, akb, page, ui]
---

# АКБ — Active Client Base plan

**URL**: `/doctor/akb` · **Module**: `doctor` · **Controller**: `AkbController::index` · **RBAC**: `operation.doctor.akb` (typical) · **Role harvested**: `admin`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Master view for the Active Client Base (АКБ) plan: how many distinct clients each agent must visit / sell to over the period. Admins create or edit AKB plans per supervisor/agent territory, then push them to the agents via "Share to agents" so they appear in mobile (`/api/v3/akb/*`).

## Fields

| Label | Name | Type | Required |
|---|---|---|---|
| Период / Месяц | period filter | select | yes |
| Супервайзер | filter | select | no |
| Агент | filter | select | no |
| План АКБ | `PLAN` (per agent) | numeric | yes (when sharing) |

## Grid columns

Each row is an agent's AKB plan; columns shown:

| # | Column |
|---|---|
| 1 | Супервайзер |
| 2 | Агент |
| 3 | Территория |
| 4 | Факт АКБ (previous) |
| 5 | План АКБ (current) |
| 6 | Расхождение |
| 7 | Действия |

## Actions

- Применить фильтр
- Поделиться с агентами — opens `share_to_agents.php` modal, pushes plan to selected agents
- Просмотр — opens `view.php` (single-agent breakdown)
- Сохранить
- Сбросить

## Backend route

- **Controller file**: `protected/modules/doctor/controllers/AkbController.php`
- **Action**: `actionIndex` (line 49) — renders `index` view; `actionView` (line 183) renders `view`; `actionShareToAgents` renders `share_to_agents`
- **Sibling AJAX actions**: `actionReturnAjax`, `actionReturnAjaxPageLoad`, `actionReturnAjaxView`
- **Required permission**: gated via `H::access('operation.doctor.akb')` in companion actions

## See also

- Module reference: [/modules/doctor](/docs/modules/doctor)
- KPI flow (visit → audit → KPI): [/flows/visit-audit-kpi](/docs/flows/visit-audit-kpi)
- Pages index: [/ui/pages/doctor](./index.md)
