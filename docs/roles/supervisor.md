---
title: Supervisor — start here
sidebar_position: 4
audience: Supervisor
summary: Web-only manager of a team of agents. Watches their KPI, route adherence, and order quality.
topics: [role-landing]
---

# Welcome, Supervisor

You are role **8** (a.k.a. *супервайзер*). You manage a team of field agents, watch their KPI scorecards, review their visits, and approve their orders when they sit at the threshold of a manager-only action. You work entirely from the web admin — you don't have a phone app.

Your scope is your **team**, not the whole filial. You see the agents assigned to you, their clients, their orders, and their KPI rows. You can't edit RBAC, period close, or any global setting.

## In your first 5 minutes

- [QA glossary — People and roles](../quality/glossary) — role-by-role reference, including supervisor (role 8).
- [Agents module reference](../modules/agents) — the data layer for your team.
- [KPI setup and views](../quality/team/kpi-setup-and-views) — the screens you monitor daily.

## Daily tasks

| Task | Where in the admin | Tutorial |
|------|-------------------|----------|
| Review your team's visits today | `/adt/visit` | [Visit audit](../quality/audit/visit-audit) |
| Check today's orders by your agents | `/orders` (filter by your agents) | [Order list & history](../quality/orders/order-list-and-history) |
| Approve a manual order edit your agent flagged | `/orders/edit` | [Edit order](../quality/orders/edit-order) |
| Track team's KPI progress this month | `/team/kpi-new` | [KPI setup and views](../quality/team/kpi-setup-and-views) |
| Run an agent-level sales report | `/report/agent` | [Report — agent](../quality/report/report-agent) |
| Adjust an agent's route assignments | `/team/agent-route` | [Role — Agent](../quality/team/role-agent) |
| Push a config change to an agent's mobile | `/team/agents-packet` | [agents-packet](../quality/team/agents-packet) |
| Spot-check a client's debt and payment history | `/finans` | [Client debt view](../quality/finans/client-debt-view) |

## Reference

- [Agents module](../modules/agents)
- [Team module](../modules/team)
- [Reports module](../modules/report)
- [Audit module (ADT)](../modules/audit-adt)
- [RBAC permission matrix](../security/rbac)

## Common gotchas

- **Out-of-zone visits don't auto-reject.** A flagged `GPS_STATUS = 1` visit is **still a visit** — review it manually; the system doesn't undo the order.
- **Agents-packet read-modify-write hazard.** When two of you edit the same agent's packet concurrently, one overwrites the other silently. See [agents-packet](../quality/team/agents-packet#conflict-landmine--the-read-modify-write-hazard).
- **All-zero KPI deletes the row.** Don't clear all targets to "reset" — that deletes the agent's KPI row for the month.
- **Follow-sequence toggle changes agent flow.** Enabling *Follow sequence* on the packet forces visits in `SORT` order; agents lose the freedom to pick. Communicate the change before flipping it.
- **Re-opening an order resets debt.** If you re-open an agent's order to *New*, the debt and stock recalculate cascade — verify nothing else broke.

## Glossary terms you'll meet

- [Visit](../concepts/visit)
- [AKB](../concepts/akb)
- [KPI](../concepts/kpi)
- [Outlet](../concepts/outlet)
- [Defect vs reject](../concepts/defect-vs-reject)
- [Bonus vs discount](../concepts/bonus-vs-discount)
- [Period close](../concepts/period-close)
