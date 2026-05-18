---
title: RFM — Recency, Frequency, Monetary
sidebar_position: 4
audience: All
summary: Customer-segmentation pattern that scores each outlet on how recently, how often, and how much they buy.
topics: [concept, reports, segmentation]
---

# RFM — Recency, Frequency, Monetary

> **TL;DR** — **RFM** scores every outlet on three numbers — how *Recently* they bought, how *Frequently* they buy, and how much *Money* they spend — and bins each into 1–5 segments. The result is a 555 = "best customer", 111 = "lapsed and trivial". sd-main computes this in the `report/rfm` controller.

## What it is

RFM is a marketing-industry segmentation method dating to the 1990s. It compresses a customer's transactional history into three integers (1–5 each):

- **Recency (R)** — *days since last purchase* (smaller is better).
- **Frequency (F)** — *order count over the period*.
- **Monetary (M)** — *total spend over the period*.

Each axis is **bucketed into quintiles**: the top-spending 20% of outlets get M=5, the next 20% M=4, and so on. Combine the three digits and you get codes like `555` (top-tier on every axis) or `111` (lapsed, infrequent, low-spend).

The pattern is universal — RFM has nothing SalesDoctor-specific; sd-main just packages it as a report so distribution managers can pivot it against their route.

## Why it matters

A bare list of clients tells a sales manager nothing about *which* clients to chase. RFM solves three concrete problems:

1. **Where to push the agent.** An R=1, F=5, M=5 client just stopped buying; visit them tomorrow.
2. **What to promote.** R=5, F=5, M=1 outlets are loyal but low-spend — push a larger SKU.
3. **What to drop.** R=1, F=1, M=1 outlets are dead weight; remove them from the route.

## How SalesDoctor models it

| Layer | Identifier | Where |
|---|---|---|
| Report controller | `RfmController` | `protected/modules/report/controllers/RfmController.php` |
| Web routes | `/report/rfm/index`, `/report/rfm/getData`, `/report/rfm/setSettings`, `/report/rfm/updateReport`, `/report/rfm/deleteReport` | 5 actions total |
| Index RBAC | `operation.reports.classificationRFM` | Other actions inherit access |
| Source data | Aggregations over `d0_order` filtered by period and filial | Grouped by `CLIENT_ID` |

The report is interactive: a manager can save settings (`setSettings`) — the bucket thresholds, the period, the included statuses — and persist a generated snapshot (`updateReport`).

## Example

A sample row from `/report/rfm/index`:

| Client | Last order | Orders | Revenue | R | F | M | Code |
|---|---|---|---|---|---|---|---|
| Korzinka Yunusabad-3 | 2 days ago | 18 | 24 800 000 | 5 | 5 | 5 | **555** |
| Magazin Yangiyer | 92 days ago | 1 | 240 000 | 1 | 1 | 1 | **111** |
| Aladdin Market | 11 days ago | 7 | 4 200 000 | 4 | 3 | 3 | **433** |

Reading the codes:

- **555** — high-value loyal customer; protect with bonus tier.
- **111** — lapsed and trivial; consider dropping from the route.
- **155** — high spender, but stopped buying — top-priority win-back.

## Common confusions

| Looks like | But actually |
|---|---|
| RFM code is a customer rating | The code is a *binning* of three independent metrics. Two outlets with code 543 may be very different in absolute revenue. |
| Higher F always means better | An outlet with F=5 but R=1 has gone cold despite history. Always read R alongside F. |
| AKB ≈ RFM | АКБ is a *count* (yes/no this period); RFM is a *segmentation* (how strong / how recent / how big). |
| RFM updates live | It's a snapshot. Re-run `updateReport` to refresh; values are not real-time. |

## Related concepts

- [AKB](./akb.md) — count of outlets that bought.
- [Outlet](./outlet.md)
- [KPI](./kpi.md)
- [Report module reference](../modules/report)
