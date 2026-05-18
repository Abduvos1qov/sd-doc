---
title: Agent (field sales) — start here
sidebar_position: 3
audience: Agent
summary: Field salesperson. Visits outlets, takes orders, collects payments — almost entirely from the mobile app.
topics: [role-landing]
---

# Welcome, Agent

You are role **4** — the field salesperson. You spend your day visiting outlets on a planned route, taking orders, collecting payments, and reporting back via the **sd-agents** mobile app. The web admin is mostly read-only for you; nearly everything you do flows through the phone.

Your `Agent.VAN_SELLING` flag decides your sub-type: **0** regular field agent, **1** van-selling (selling out of a vehicle full of stock), **2** seller (fixed point of sale), **3** system bot. The flag changes how stock and debt are handled — make sure you know yours.

## In your first 5 minutes

- [Agents module reference](../modules/agents) — what the system tracks about you.
- [Role — Agent (QA)](../quality/team/role-agent) — your full surface, written for QA.
- [Sync flow](../quality/mobile/sync-flow) — what happens when you tap *Sync*.

## Daily tasks

| Task | Where | Tutorial |
|------|-------|----------|
| Sync your agents-packet at start of day | Mobile app → Sync | [Sync flow](../quality/mobile/sync-flow) |
| Visit an outlet (check-in) | Mobile app → Route → Outlet | [Role — Agent](../quality/team/role-agent) |
| Create an order at the outlet | Mobile app → Outlet → New order | [Create order — mobile](../tutorials/create-order-mobile) |
| Add a bonus / discount on a line | Order screen → Line → Edit | [Bonuses](../quality/orders/bonuses), [Discounts](../quality/orders/discounts) |
| Scan a CIS code on a regulated SKU | Order screen → Scan | [CIS code check](../quality/orders/cis-code-check) |
| Take a payment from the outlet | Mobile app → Outlet → Payment | [Mobile payment](../quality/orders/mobile-payment) |
| Submit a visit photo / audit | Mobile app → Audit | [Visit audit](../quality/audit/visit-audit), [Photo reports](../quality/audit/photo-reports) |
| Complete a route or create an off-route visit | Mobile app → Route | [Role — Agent](../quality/team/role-agent) |

## Reference

- [Agents module](../modules/agents)
- [Orders module](../modules/orders) — what happens to your order after submit.
- [Mobile (sync, GPS, SMS)](../quality/mobile/index)
- [Audit module](../modules/audit-adt)
- [Agents-packet](../quality/team/agents-packet) — the bundle of rules pushed to your phone.

## Common gotchas

- **GUID double-submit guard.** Tapping *Submit* twice on flaky network: api4 deduplicates by client-generated GUID, but the older api3 channel relies on a 20-second `SyncLog` window — re-submits older than that **create a duplicate order**.
- **Out-of-zone visits are flagged.** If you check in farther than the geofence radius from the outlet, `GPS_STATUS = 1` flags the visit for review.
- **Van-seller debt path forks.** If your dealer's *debt per order* setting is on and you're van-selling, each order creates a *fresh debt row* instead of adding to a running balance. Different ledger shape.
- **Stock-check disabled is per-warehouse.** A warehouse with the toggle off skips the *"do you have enough?"* check at order time; sales there can go negative.
- **Bonus auto vs retro.** Auto-bonus = the system picks the free product; retro-bonus = *you* pick it on the phone. Confusing the two in support tickets causes wasted hours.

## Glossary terms you'll meet

- [Outlet](../concepts/outlet)
- [Visit](../concepts/visit)
- [AKB](../concepts/akb)
- [Price type](../concepts/price-type)
- [Bonus vs discount](../concepts/bonus-vs-discount)
- [Defect vs reject](../concepts/defect-vs-reject)
- [KPI](../concepts/kpi)
- [Filial](../concepts/filial)
