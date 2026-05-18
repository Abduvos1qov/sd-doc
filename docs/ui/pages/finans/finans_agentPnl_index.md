---
title: "P&L по агентам"
audience: All sd-main developers, QA
summary: Live admin page at /finans/agentPnl/index
topics: [finans, page, ui, pnl, agents]
---

# P&L по агентам

**URL**: `/finans/agentPnl/index` (alias `/finans/agentPnl`) · **Module**: `finans` · **Controller**: `AgentPnlController::index` · **RBAC**: resolved via `User::checkAccess`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Vue 3 / Vuetify dashboard that breaks down the tenant P&L by sales agent. Selecting an agent (or "Сумма" for total) reveals an additional "По моделям" panel that shows the same numbers per sales-model document type. Data is loaded via `/finans/agentPnl/load`.

## Fields

| Label | Name | Type |
|---|---|---|
| Клиенты | `filterByClients` | multi-autocomplete |
| Категории продуктов | `filterByProdCats` | multi-autocomplete |
| Категории клиентов | `filterByClientsCats` | multi-autocomplete |
| Территории | `filterByCities` | multi-autocomplete |
| Документы | `filterByModelTypes` | multi-autocomplete |
| Склады | `filterByWarehouses` | multi-autocomplete |
| Период | `pickedDateRange` | date-range |

## Grid columns

`#by-agent-pnl` table:

| # | Column |
|---|---|
| 1 | Агент |
| 2 | Себестоимость |
| 3 | Выручка |
| 4 | Прибыль |

"По моделям" drill-down table (revealed once an agent is selected):

| # | Column |
|---|---|
| 1 | — (field-extraction pending — rendered via Vue from `byTypesPnls`) |

## Actions

- Загрузить (applies the current filter set)
- Выбрать всех (per autocomplete — Категории продуктов / Категории клиентов / Территории / Документы / Склады)
- Excel (per-panel — P&L, По моделям)
- Row click selects an agent and re-renders the "По моделям" panel

## Backend route

- **Controller file**: `protected/modules/finans/controllers/AgentPnlController.php` (line 20)
- **Action kind**: inline (one-liner: `$this->render('index')`)
- **View rendered**: `index`
- **Required permission**: routed through `User::checkAccess`

## See also

- Module reference: [/modules/finans](/docs/modules/finans)
- P&L summary: [/ui/pages/finans/finans_pnl_index](./finans_pnl_index)
