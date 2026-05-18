---
title: Run an agent KPI report
sidebar_position: 4
audience: End users (manager | supervisor)
summary: Open the KPI dashboard, scope it to one agent and a date range, and export the result to Excel.
topics: [tutorial, how-to, dashboard, report]
---

# Run an agent KPI report

**You will**: Open the KPI dashboard, set a plan if it isn't set yet, scope the view to one agent and a date range, and export the resulting numbers to Excel. By the end you will know the canonical way managers do "agent of the month" reviews.
**You need**: A user with role 1, 2, 9 or supervisor role with `operation.dashboard.view`; at least one agent who has worked the period; plans configured in **Team → KPI setup** (or you can set one inline from this page).
**Time**: ~4 minutes
**Hard parts**:
- "No data" almost always means the agent has no plan for the period — not that there were no sales.
- Two different KPI tabs exist (`/dashboard/kpi` and `/dashboard/kpi2`) — they compute slightly differently. Pick one and stick to it.

## Step 1 — Open the dashboard

Navigate to **Dashboard → KPI** (URL: `/dashboard/kpi`).

![Annotated screenshot of the KPI dashboard](/screens/annotated/dashboard_kpi.annotated.png)

The page lands on today's snapshot for all agents in the current filial. If the grid says "План не установлен" everywhere, you are missing plans and need to fix that before the numbers mean anything.

1. Click **установите план** (①) at the top-left to jump to the plan setup screen if needed.

## Step 2 — Filter to the agent and date range

In the toolbar above the grid:

| Filter | What it does |
|---|---|
| **Агент** | One specific agent, or "Все" for the team |
| **Дата с / Дата по** | Period to evaluate; defaults to current month |
| **Категория клиента** | Optional — narrows to one client category (e.g. only A-class outlets) |
| **Территория** | Optional — narrows by route territory |

1. Pick the agent.
2. Set the start and end dates (the date pickers default to first/last of the current month — clicking the field opens a calendar).
3. Click **Применить** (Apply). The page reloads with the scoped numbers.

## Step 3 — Read the numbers

The grid shows one row per agent. Key columns:

| Column | Meaning | Healthy value |
|---|---|---|
| **План** | Sales target for the period (UZS) | from `d0_plan_agent` |
| **Факт** | Realised revenue (UZS) | from `d0_order` summed at `STATUS≥3` |
| **%** | Факт / План × 100 | 80-110% is normal |
| **АКБ план / факт** | Active client base | unique outlets visited |
| **Эфф. визита** | Visits with an order / total visits | 60-90% |
| **СКЮ** | Average SKUs per order | trend metric |

A red percentage is below plan; green is above. Click any row to drill into the agent's per-day breakdown.

## Step 4 — Export to Excel

1. Scroll to the toolbar above the grid.
2. Click **Экспорт в Excel** (or its filial-localized label).
3. The browser downloads `kpi_<date>.xlsx`. This calls `GET /dashboard/kpi/exportXls` server-side, which streams an XLSX matching the on-screen filters.

## Step 5 — Verify

1. Open the file. The header should match your filters; the rows should match the on-screen grid.
2. If you exported "all agents", sum the **Факт** column — it should equal what's on `/report/agent` for the same period (both pull from `d0_order`).

## What just happened (under the hood)

The dashboard page is served by `KpiController::actionIndex` (route `/dashboard/kpi/index`). It joins `d0_plan_agent` (the plan table) with aggregates over `d0_order` (filtered by status and agent), `d0_visit` (for AKB and visit-efficiency), and `d0_client` (for category and territory). Export goes through `actionExportXls`. The companion controller `KpiController::actionAjaxOrderDetails` (route `/dashboard/kpi/ajaxOrderDetails`) backs the drill-down popovers. See the [dashboard module](/docs/modules/dashboard) for the full set of KPI tabs and how they differ.

## Common mistakes

- **No plan = no row**: if an agent has zero rows in `d0_plan_agent` for the period, they vanish from the KPI grid even if they sold. Use **установите план** first.
- **Mixing kpi and kpi2**: the older `/dashboard/kpi` page uses calendar-day buckets; `/dashboard/kpi2` uses 4-week marketing weeks. Comparing the two with the same filters gives different totals.
- **Excel locale mismatch**: numbers may be exported with `,` decimal separator. If your Excel uses `.`, set the column format to numeric before summing.

## Next steps

- Build the agent so they show up here: [Create and activate an agent account](./setup-agent.md).
- Cross-check the totals with the agent report: [report module](/docs/modules/report).
- Full dashboard reference: [dashboard module](/docs/modules/dashboard).
