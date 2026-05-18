---
title: KPI (sales / expeditor)
sidebar_position: 9
audience: All
summary: Plan-vs-actual targets per agent / expeditor / supervisor — bonus tiers, monthly evaluation.
topics: [concept, kpi, team]
---

# KPI — Key Performance Indicators

> **TL;DR** — A **KPI** in SalesDoctor is one person's monthly target on one measurable thing (orders count, АКБ, revenue, visit %, defect %, …). Each target has seven **bonus tiers**: hitting tier 5 might pay 100%, tier 7 might pay 120%. v2 of the KPI plumbing (`KpiNewController`) is current; v1 is legacy.

## What it is

A KPI in this system has three layers:

1. **`KpiTaskTemplate`** — a *definition* of one measurable thing. *"Sales sum in UZS"*, *"АКБ"*, *"Number of visits"*. It carries a `TASK_TYPE`, optional filters (product, category, city, price type), and seven threshold values (`MARK`, `MARK2`, …, `MARK7`) with paired percentages.
2. **`Kpi`** — one *person's* KPI for one month. Carries `TEAM_TYPE` (agent / supervisor / expeditor), `TEAM` (the person's id), `DATE_FROM`, `DATE_TO`, and a `FIX_SALARY` base.
3. **`KpiTask`** — a child of `Kpi`, holding the *target value* for one template (e.g. *"Agent X must do 50 000 000 UZS in sales in May"*).

A monthly KPI for one agent is therefore one `Kpi` row plus several `KpiTask` rows — one per measurable thing.

## Why it matters

KPIs are how the dealer pays variable compensation. Every month:

- The system runs the actuals (visits done, AKB achieved, revenue, defect %).
- It compares actuals to the targets in `KpiTask.VALUE`.
- It looks up the bonus tier on the matching `KpiTaskTemplate` (which `MARK` did the actual exceed?).
- It computes the variable pay-out.

KPIs are also a *forcing function* on field behaviour: an agent whose visit % target is 80% is incentivised to follow the route.

## How SalesDoctor models it

| Layer | Identifier | Where |
|---|---|---|
| Template | `KpiTaskTemplate` (`d0_kpi_task_template`, 56 cols) | Definition of one metric |
| Per-person plan | `Kpi` (`d0_kpi`, 31 cols) | One row per person per month |
| Per-task target | `KpiTask` (`d0_kpi_task`, 42 cols) | One row per metric on that plan |
| v2 controller | `KpiNewController` | Current implementation |
| v1 controller | (legacy) | Test plans should target v2 |
| QA workflow | [KPI setup and views](../quality/team/kpi-setup-and-views) | Operator guide |

Key columns on `Kpi`: `KPI_ID, DILER_ID, NAME, KPI_TYPE, TEAM_TYPE, FIX_SALARY, TEAM, DATE_FROM, DATE_TO, MARK, MARK2..MARK7, ...`.

## Example

Canonical KPI metrics that appear out of the box:

| TASK_TYPE | What it measures |
|---|---|
| Orders count | Number of non-cancelled orders the agent took |
| Revenue (SUMMA) | Sum of `Order.SUMMA` in the period |
| АКБ | Distinct outlets with at least one paid order |
| Visit % | Visits done / visits planned |
| Defect % | Lines flagged as defect / lines delivered |
| Cash collected | Sum of payments collected (for expeditors) |

A sample tier table on one `KpiTaskTemplate`:

| Threshold | Value | Payout |
|---|---|---|
| MARK | 30 000 000 | 50% |
| MARK2 | 40 000 000 | 75% |
| MARK3 | 50 000 000 | 100% |
| MARK4 | 55 000 000 | 105% |
| MARK5 | 60 000 000 | 110% |
| MARK6 | 70 000 000 | 115% |
| MARK7 | 80 000 000 | 120% |

If the agent does 52 000 000 UZS in May, they cross MARK3 → 100% of the bonus on this task.

## Common confusions

| Looks like | But actually |
|---|---|
| One Kpi = one metric | One `Kpi` row is one person-month; the metrics live in child `KpiTask` rows. |
| Templates apply to everyone | Templates are *catalog entries*; only when copied into a person's `KpiTask` row do they become a target. |
| Clearing targets is harmless | If *every* target on a month is cleared, the system **deletes** the `Kpi` row and its children. See *all-zero deletion* in the glossary. |
| KPI v1 and v2 are interchangeable | Test against **v2** (`KpiNewController`) unless chasing a v1-only regression. |

## Related concepts

- [AKB](./akb.md) — a canonical KPI metric.
- [Visit](./visit.md)
- [Outlet](./outlet.md)
- [KPI setup and views — QA workflow](../quality/team/kpi-setup-and-views)
- [Dashboard module](../modules/dashboard)
- [Agents module](../modules/agents)
