---
title: Expeditor (delivery) — start here
sidebar_position: 6
audience: Expeditor
summary: Driver who delivers orders, collects cash and CIS-coded SKUs, and brings back defects.
topics: [role-landing]
---

# Welcome, Expeditor

You are role **10** — the driver. You load a route of orders, drive to each outlet, hand over the goods, collect the payment if the client pays at the door, mark defective lines if anything is broken, and bring back the rejected stock. You work mostly from the **driver** mobile app (same codebase as sd-agents but a different build).

Your cashbox is your till. Every cash payment you collect lands in it; the cashier reconciles it against the ledger.

## In your first 5 minutes

- [Role — Expeditor (QA)](../quality/team/role-expeditor) — your full surface, with the data tables called out.
- [Agents module reference](../modules/agents) — expeditors share the `Agent` table with sales agents (different `VAN_SELLING` value).
- [Defect vs reject](../concepts/defect-vs-reject) — know which is which **before** you mark goods at the door.

## Daily tasks

| Task | Where | Tutorial |
|------|-------|----------|
| Sync your expeditor-packet | Driver app → Sync | [expeditor-packet](../quality/team/expeditor-packet) |
| See the orders assigned to you for the route | Driver app → Today | [Role — Expeditor](../quality/team/role-expeditor) |
| Mark an order *Delivered* (3) | Driver app → Order → Delivered | [Status transitions](../quality/orders/status-transitions) |
| Record a per-line defect at the door | Driver app → Order → Line → Defect | [Partial defect](../quality/orders/partial-defect) |
| Record a whole-order refusal | Driver app → Order → Reject | [Whole-order return](../quality/orders/whole-return) |
| Take a cash payment | Driver app → Payment | [Mobile payment](../quality/orders/mobile-payment) |
| Scan a CIS code | Driver app → Scan | [CIS code check](../quality/orders/cis-code-check) |
| Hand over the cashbox to the cashier | Web → cashbox screen | [Cashbox balance](../quality/finans/cashbox-balance) |

## Reference

- [Agents module](../modules/agents)
- [Orders module](../modules/orders)
- [Payment module](../modules/payment)
- [Stock — defect and van-stock (QA)](../quality/stock/defect-and-van-stock)
- [Audit module](../modules/audit-adt)
- [RBAC permission matrix](../security/rbac)

## Common gotchas

- **Defect needs a defect store to move stock.** Without a `DEFECT_STORE` configured on your expeditor record, declaring a defect records the count but **no stock moves anywhere**. The discrepancy surfaces in next month's inventory.
- **Partial defect only valid on STATUS 2 or 3.** Trying to mark a defect on a *Cancelled* or *Returned* order silently fails.
- **Whole-return ≠ 100% partial defect.** They use different code paths and different audit tables. See [Defect vs reject](../concepts/defect-vs-reject).
- **Cashbox currency must match the order.** Multi-currency mismatches reconcile wrong — verify the order's `PRICE_TYPE` currency before accepting cash.
- **CIS code mismatch blocks delivery.** XTrace validation can return *codes invalid* or *quantity mismatch* — both block the *Delivered* status transition.

## Glossary terms you'll meet

- [Defect vs reject](../concepts/defect-vs-reject)
- [Outlet](../concepts/outlet)
- [Visit](../concepts/visit) — every delivery is inside a visit.
- [Price type](../concepts/price-type)
- [Period close](../concepts/period-close)
- [KPI](../concepts/kpi)
- [Filial](../concepts/filial)
