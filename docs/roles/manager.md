---
title: Manager — start here
sidebar_position: 2
audience: Manager
summary: "Day-to-day operations: approve orders, supervise agents and expeditors, monitor KPI, watch the debt list."
topics: [role-landing]
---

# Welcome, Manager

You are role **2** — the office-based approver and overseer. You don't configure the platform (that's the admin) and you don't visit clients (that's the agent), but every operational decision flows through your screen. You approve edge-case orders, review KPI, monitor cash collection, and chase missing visits.

You have read access to almost everything in the dealer; your write access is scoped to operational rows (orders, plans, KPI). You can not edit RBAC, period close, or global toggles.

## In your first 5 minutes

- [Orders module reference](../modules/orders) — the lifecycle you'll spend most of your day on.
- [Dashboard module](../modules/dashboard) — the daily snapshot.
- [QA glossary](../quality/glossary) — the vocabulary every report uses.

## Daily tasks

| Task | Where in the admin | Tutorial |
|------|-------------------|----------|
| Approve a manually-created order | `/orders` | [Create an order on the web](../tutorials/create-order-web) |
| Edit an existing order's lines / status | `/orders/edit` | [Edit order](../quality/orders/edit-order) |
| Run a sales report | `/report/sale` | [Run a KPI report](../tutorials/run-kpi-report) |
| Run an АКБ / customer report | `/report/customer` | [Report — customer](../quality/report/report-customer) |
| Run an RFM segmentation | `/report/rfm` | [RFM](../concepts/rfm) |
| Set up monthly KPI targets per agent | `/team/kpi-new` | [KPI setup and views](../quality/team/kpi-setup-and-views) |
| Review agent visits and routes | `/adt/visit` | [Visit audit](../quality/audit/visit-audit) |
| Move stock between warehouses | `/vs/order` | [Stock transfer](../quality/stock/stock-transfer) |
| Watch client debt | `/finans` | [Client debt view](../quality/finans/client-debt-view) |

## Reference

- [Orders module](../modules/orders)
- [Agents module](../modules/agents)
- [Reports module](../modules/report)
- [Dashboard module](../modules/dashboard)
- [Finans (ledger)](../modules/finans)
- [RBAC permission matrix](../security/rbac)

## Common gotchas

- **Period close locks edits.** Once an order is past the close date you can't change status, lines, or totals — escalate to admin for a correction.
- **Re-opening an order cascades.** Moving an order back to *New* re-calculates debt, restores stock, and adds history rows. See [Status transitions](../quality/orders/status-transitions).
- **Whole-return vs partial defect are different flows.** A 100% defect is *not* a return; the order must move to STATUS=4 instead. See [Defect vs reject](../concepts/defect-vs-reject).
- **Bonus orders need explicit cancellation.** When you cancel a main order, verify the linked bonus order is also cancelled — orphan bonus orders are a known bug class.
- **KPI v1 and v2 coexist.** Use the v2 screens (`KpiNewController`) unless you have a v1-specific reason.

## Glossary terms you'll meet

- [AKB](../concepts/akb)
- [RFM](../concepts/rfm)
- [KPI](../concepts/kpi)
- [Defect vs reject](../concepts/defect-vs-reject)
- [Bonus vs discount](../concepts/bonus-vs-discount)
- [Period close](../concepts/period-close)
- [Outlet](../concepts/outlet)
- [Visit](../concepts/visit)
