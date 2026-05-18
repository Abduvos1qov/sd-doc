---
title: АКБ — Active Customer Base
sidebar_position: 3
audience: All
summary: KPI metric — count of outlets that actually purchased something inside the reporting period.
topics: [concept, kpi, reports]
---

# АКБ — Active Customer Base

> **TL;DR** — **АКБ** (Russian: *Активная Клиентская База*; English: Active Customer Base) is the count of unique outlets that placed at least one paid order inside the reporting period. It's the canonical "are we actually selling to our customers?" KPI in CIS-region distribution.

## What it is

АКБ is a **count of distinct outlet ids** that meet a "was active" predicate for a given period — usually:

> *An outlet is in AKB if it has at least one non-cancelled order with a positive total inside the date range.*

The metric is a Russian distribution-industry convention. The dual metric is **ОКБ** (*Общая Клиентская База* — total clients visited or assigned, regardless of purchase). The ratio `AKB / OKB` is the **conversion rate** of a route.

In sd-main:

- AKB is **computed on demand** — there is no `is_active` flag stored on `d0_client`.
- The canonical SQL lives in the `report/customer` module (`CustomerController` in `protected/modules/report/controllers/CustomerController.php`).

## Why it matters

A growing client list means little if half of those clients haven't bought anything in three months. АКБ is the metric a regional manager looks at first to answer:

- *Is my agent covering their route productively, or just driving around?*
- *Did the new bonus rule lift conversion, or just hand out free product to the same buyers?*
- *Which clients dropped off — and why?*

Because АКБ counts the **outlet** (not the order), big spenders and small ones each contribute one. Companion metrics (revenue, average order value) ride alongside it.

## How SalesDoctor models it

| Layer | Identifier | Where |
|---|---|---|
| Report controller | `CustomerController` | `protected/modules/report/controllers/CustomerController.php` |
| Web routes | `/report/customer/index`, `/report/customer/clientListAjaxAkb`, `/report/customer/clientListAjaxAkbOld` | RBAC `operation.reports.customer` |
| Helper endpoint | `/report/customer/getAkb`, `/report/customer/getOkb` | Numeric output for dashboards |
| Source data | `d0_order` filtered by `STATUS != 5`, `SUMMA > 0`, `DATE BETWEEN ?` | Joined to `d0_client` via `CLIENT_ID` |
| Pivot in sd-cs | `pivot-akb` | [Pivot — АКБ](../sd-cs/workflows/pivot-akb) |

The metric appears on the agent's KPI scorecard as a `KpiTaskTemplate` of `TASK_TYPE = AKB`.

## Example

Conceptual SQL for one filial, one month:

```sql
SELECT COUNT(DISTINCT o.CLIENT_ID) AS akb
FROM d0_order o
WHERE o.FILIAL_ID = :filial
  AND o.STATUS <> 5
  AND o.SUMMA > 0
  AND o.DATE BETWEEN :date_from AND :date_to;
```

A report row from `/report/customer/index`:

| Agent | ОКБ | АКБ | Conversion |
|---|---|---|---|
| Akmal U. | 84 | 61 | 73% |
| Dilshod K. | 102 | 47 | 46% |

## Common confusions

| Looks like | But actually |
|---|---|
| Total clients of the dealer | That's the **client list** (every row in `d0_client`), independent of any period. |
| ОКБ | ОКБ counts outlets *visited or assigned*; АКБ counts only those that *bought*. |
| Visits count | A visit without an order doesn't add to АКБ. |
| `Client.ACTIVE` flag | A soft-delete / archive flag — unrelated to whether the outlet bought this month. |

## Related concepts

- [Outlet](./outlet.md)
- [KPI](./kpi.md)
- [RFM](./rfm.md) — segmentation that uses recency + AKB-like signals.
- [Visit](./visit.md)
- [Pivot — АКБ in sd-cs](../sd-cs/workflows/pivot-akb)
