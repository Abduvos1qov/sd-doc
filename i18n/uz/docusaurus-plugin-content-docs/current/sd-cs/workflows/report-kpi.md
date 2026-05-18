---
sidebar_position: 8
title: report · KPI
---

# KPI report

## Purpose

Answers *"this month, how much did every sales agent earn — and how is
that bonus broken down across every individual KPI task they were
assigned to (sales, AKB, OKB, payment collection, MML, visits,
defects)?"* The KPI report is the single source of truth for monthly
payroll across all dealer filials; HQ uses it to validate the bonus
numbers each filial pushes to its agents.

## Who uses it

| Role | What they do here |
|------|-------------------|
| Country / HR manager | Validates monthly payroll for every agent across all filials |
| Regional supervisor | Inspects agent performance against KPI marks (1–7) |
| Finance manager | Audits the fix-salary plus bonus total before disbursement |

The `getData` endpoint is in `KpiController::$allowedActions` (line 5)
and bypasses the page-level access check; `actionIndex` is gated by
RBAC under the standard `report.kpi.*` access keys.

## Where it lives

| | |
|---|---|
| URL | `/report/kpi` |
| Controller | [`protected/modules/report/controllers/KpiController.php`](https://github.com/salesdoctor/sd-cs/blob/master/protected/modules/report/controllers/KpiController.php) (640 lines) |
| Index view | `protected/modules/report/views/kpi/index.php` |
| Connection | `Yii::app()->dealer` (the `b_*` warehouse) |
| Saved-report code | *not used* |

Per-filial models read here: `Kpi`, `KpiTask`, `KpiTaskTemplate`,
`Order`, `OrderDetail`, `OrderDefectDetail`, `Client`, `Visiting`,
`ClientTransaction`, `Supervayzer`, `User`, `Agent` — all addressed
via `setFilial($prefix)`.

Dealer-global models read here: `KpiTaskTemplateGroup`
(`d0_kpi_task_template_group`), `Product` (`d0_product`).

## Workflow

```mermaid
sequenceDiagram
  autonumber
  participant U as HR manager
  participant W as sd-cs · /report/kpi
  participant CS as cs3_demo
  participant BD as b_demo (per-filial)

  U->>W: GET /report/kpi
  W-->>U: render filter form (period, filial_id[], task)
  U->>W: POST /report/kpi/getData (period, filial_id[], task)
  W->>BD: d0_kpi_task_template_group (active='Y')
  Note over W: build $filInfo[prefix] → [template_id, …] map
  W->>CS: cs_user_filial (visible filials via getOwnModels)
  loop for each visible filial fN
    W->>BD: d0_fN_kpi (month, year)
    W->>BD: d0_fN_supervayzer JOIN d0_fN_user
    W->>BD: d0_fN_kpi_task WHERE KPI_ID IN (…)
    loop for each KPI template
      W->>BD: SELECT … FROM d0_fN_order, d0_fN_order_detail (sales-shape)
      W->>BD: or … d0_fN_visiting / d0_fN_client_transaction / d0_fN_order_defect_detail
    end
    Note over W: compute PERSENTAGE, FORECAST, BONUS, MARK<br/>per agent × template; apply MARKn share,<br/>AUDIT_SHARE, MAX_BONUS cap, perTaskStage rule
  end
  W-->>U: streamed JSON [{}, agentRows…, totals, groups]
```

1. User opens `/report/kpi` and picks a year-month (`date`), optional
   filial scope (`filial_id`), and optional KPI-task filter (`task`).
2. Server loads all active `KpiTaskTemplateGroup` rows. The
   `KPI_TASK_TEMPLATE_ID` column is a CSV of `prefix-templateId`
   pairs; the controller explodes it into `$filInfo[prefix] = […]`,
   which drives the per-filial loop.
3. For every visible filial:
   - Loads `d0_fN_kpi` rows for the selected month/year — these are
     the agent-to-team assignments plus `FIX_SALARY`.
   - Loads the supervisor map (`d0_fN_supervayzer ⋈ d0_fN_user`).
   - Loads matching `d0_fN_kpi_task` rows — each task is one
     `{TEMPLATE_ID, VALUE, AUDIT_SHARE}` row per agent.
   - For each distinct `TEMPLATE_ID` the server dispatches to one of
     ten SQL shapes based on the template's `TASK_TYPE`.
4. After all SQL completes, PHP computes for every (agent, template):
   - `DONE` — the raw metric value (volume / count / summa / AKB /
     OKB / NEW_AKB / etc.).
   - `PERSENTAGE = DONE / VALUE × 100`.
   - `FORECAST` — end-of-month extrapolation based on
     `KpiTaskTemplate::WorkingDays($month, $year, $prefix)`.
   - `MARK` — the 1-to-7 grade based on `MARK1…MARK7` thresholds.
   - `BONUS` — computed via the `BONUS_TYPE` switch (sales, summa,
     bonusPersentage, perVolume, payment, perTaskStage); clamped by
     `MAX_BONUS`, scaled by `AUDIT_SHARE / 100`.
5. The response is streamed as a JSON array — first an empty
   placeholder, then one object per (filial, agent), then a grand
   total, then the list of `KpiTaskTemplateGroup` rows for column
   headers. Inactive agents are dropped unless they have at least
   one non-zero result for the period.

## Rules

- **Period defaults** — `params->date` is `YYYY-MM`; if absent, the
  current month is used. `startDate` / `endDate` override the
  month-window (formatted to `Y-m-d 00:00:00` / `Y-m-d 23:59:59`).
- **`$date_from_before`** — the previous calendar month, used by the
  `ACTIVATE` shape to find clients that were *not* buying in the
  prior period.
- **Aggregation type** branches on `kpi_task.TASK_TYPE`:
  - `count` / `volume` / `summa` / `AKB` → grouped order-detail
    aggregation, with optional `MIN_SUM` (HAVING `SUMMA >= MIN_SUM`)
    and optional `NEW_CLIENTS` filter (only clients created in the
    current month).
  - `blok` → adds `SUM(COUNT / PACK_QUANTITY)` and joins `d0_product`.
  - `PEN_DEFECT_*` → reads `d0_fN_order_defect_detail` for `TYPE = 2`
    (penalty) orders; `bonusPersentage` is negated.
  - `NEW_AKB` → distinct clients whose `c.TIMESTAMP_X` falls inside
    the period.
  - `OKB` → `COUNT(DISTINCT v.CLIENT_ID)` from `d0_fN_visiting`
    joined with `d0_fN_client (ACTIVE='Y')`.
  - `MML_AKB` / `MML_PRODUCT` → match-min-list shapes that require
    the client to have bought across *all* listed categories /
    products in the period.
  - `ACTIVATE` → clients buying in this period but not in
    `$date_from_before … $date_from`.
  - `CLIENT_PAYMENT` / `CLIENT_VISITING` → reads
    `d0_fN_client_transaction` with `TRANS_TYPE = 3`.
  - `SUCCESS_VISITS` → groups by `(AGENT_ID, DATE(order.DATE))` so
    one order day counts as one visit; supports `MIN_SUM`.
- **MARK ladder**: each template carries `MARK1…MARK7` thresholds.
  The first threshold the `PERSENTAGE` falls below wins; below all
  seven, mark 7 is applied. `MARKn_BONUS_SHARE` / `MARKn_KPI_SHARE`
  scale the bonus and the KPI weight.
- **`BONUS_TYPE`**:
  - `sales` / `payment` → `BONUS/100 × DONE_SUMMA`.
  - `summa` → flat `BONUS`.
  - `bonusPersentage` → `BONUS × PERSENTAGE/100`.
  - `perVolume` → `BONUS × DONE`.
  - `perTaskStage` → piecewise integral over MARK1…MARK7 bands.
- **`AUDIT_SHARE`** (default 100) — multiplied into the final
  `BONUS` after all other adjustments.
- **`MAX_BONUS`** caps the per-template bonus when set on
  `KpiTaskTemplate`.
- **Per-filial KPI summary** — `Total[agent]["PERSENTAGE"]`
  accumulates only on the first occurrence of each template
  (`check[agent][id] == 1`). Then the base-KPI MARK ladder is
  applied to set the agent-level mark and message.
- **Active filter**: an agent with `ACTIVE = 'N'` is included only
  if at least one of their template results is non-zero in the
  period. Fix-salary is always counted into the agent row when shown.

## Data sources

| Schema | Table | Why it's read |
|--------|-------|---------------|
| `cs3_demo` | `cs_user_filial` | Filial-visibility ACL for non-admins |
| `b_demo` | `d0_filial` | Tenant registry — provides prefix and `active` |
| `b_demo` | `d0_kpi_task_template_group` | Column-grouping for the result grid |
| `b_demo` | `d0_product` | Joined for `PACK_QUANTITY` in `blok` shape |
| `b_demo` | `d0_fN_kpi` | Per-month agent-to-team binding + `FIX_SALARY` |
| `b_demo` | `d0_fN_kpi_task` | Per-template plan value, `AUDIT_SHARE`, filters |
| `b_demo` | `d0_fN_kpi_task_template` | `MIN_SUM`, `NEW_CLIENTS`, `MAX_BONUS`, MARK ladder |
| `b_demo` | `d0_fN_order` / `d0_fN_order_detail` | Sales-shape SQL source |
| `b_demo` | `d0_fN_order_defect_detail` | `PEN_DEFECT_*` shape source |
| `b_demo` | `d0_fN_visiting` | `OKB` / `CLIENT_VISITING` shape source |
| `b_demo` | `d0_fN_client` | `NEW_AKB` / `OKB` filter, `c.TIMESTAMP_X` |
| `b_demo` | `d0_fN_client_transaction` | `CLIENT_PAYMENT` / `CLIENT_VISITING` source |
| `b_demo` | `d0_fN_supervayzer`, `d0_fN_user`, `d0_fN_agent` | Supervisor + agent names |

For the column reference, see [data schemes](../data-schemes.md).

## Gotchas

- **Response is streamed, not JSON-encoded as one blob.** The
  controller `echo`es `"["`, then `","+json_encode(...)` per row,
  finally `"]"`. Front-end clients must `JSON.parse` the full text
  once the response ends — partial reads will not parse.
- **10 SQL shapes × N filials × N templates.** Each filial executes
  one SQL per template plus three reference queries. A 20-filial
  org with 12 templates per filial runs 240+ queries per call;
  caching is not implemented.
- **`KpiTaskTemplateGroup.KPI_TASK_TEMPLATE_ID` is a CSV column.**
  Format: `{prefix}-{templateId},…`. A template missing from this
  CSV will never appear in the report, even if `d0_fN_kpi_task` has
  matching rows.
- **`SUCCESS_VISITS` counts visit-days, not visits.** The SQL groups
  by `DATE(o.DATE)` so two orders on the same calendar day count
  once. A `MIN_SUM` template further drops low-value days.
- **`OKB` shape ignores the date range entirely.** It counts
  `(agent, client)` from `d0_fN_visiting` filtered only by
  `d0_fN_client.ACTIVE = 'Y'`. Combining `OKB` with sales templates
  in the same report shows inconsistent denominators.
- **`baseKpi[MARK*]` uses undefined PHP constants.** They resolve to
  string literals `"MARK1"…"MARK7"` via PHP's notice-tolerant
  scalar fallback. Do not refactor without preserving this.

## See also

- [sd-cs architecture](../architecture.md) — two-DB model and
  `setFilial()` mechanism.
- [KPI concept](../../concepts/kpi.md) — how marks, shares and bonus
  types compose into a monthly payout.
- [report · Agent](./report-agent.md) — same `getOwnModels()` loop,
  optimised for per-agent productivity rather than payroll.
- [`KpiController.php` source](https://github.com/salesdoctor/sd-cs/blob/master/protected/modules/report/controllers/KpiController.php) — the full controller (640 lines).
