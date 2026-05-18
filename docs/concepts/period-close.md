---
title: Period close
sidebar_position: 6
audience: All
summary: The monthly cut-off that freezes ledger and order history so reports stay reproducible.
topics: [concept, settings, finance]
---

# Period close

> **TL;DR** — **Period close** is the operation that locks all data older than the close date so reports and balances are stable. After close, an order's status, totals, and lines can no longer be edited. The close date is dealer-configured and rolls forward.

## What it is

In any ledger-based system, *something* has to declare "the books for September are final" — otherwise yesterday's closing balance changes every time someone fixes a typo. In SalesDoctor that something is **the close day** (in the Russian UI: *Закрытие дня* / *Close day*).

Two related ideas:

- **Rolling close** — a configurable number of days back from today (default 21 days). Anything older becomes read-only.
- **Hard close** — an admin explicitly closes a specific month so no edit reopens it.

After close:
- Order **status**, **totals**, **lines** cannot be modified.
- Manual ledger corrections to closed periods require a special admin path.
- Reports for closed periods are guaranteed reproducible.

## Why it matters

Without period close, every reporter is shooting at a moving target. A revenue report for "last month" run twice will return different numbers because someone restored a cancelled order, or an expeditor declared a defect retroactively, or an admin manually corrected a debt.

Closing is *the* mechanism that lets:

- The dealer's accountant trust the monthly report.
- KPI bonuses paid in October not get clawed back because of a September edit.
- Audit trails be meaningful (an edit *attempt* on a closed period is rejected, not silently applied).

Trade-off: the field staff lose the ability to fix mistakes silently and must instead file a correction with the trail visible.

## How SalesDoctor models it

| Layer | Identifier | Where |
|---|---|---|
| Admin UI | Settings → Close day | `/settings/closed` (see [page-to-module map](../quality/page-to-module-map)) |
| QA workflow | [Server toggles and period close](../quality/settings/server-toggles-and-period-close) | Full operator guide |
| Module | `settings` | [Settings module](../modules/settings-access-staff) |
| RBAC | Admin (role 1) only | Manager (role 2) cannot edit |
| Effect on | Orders, defects, payments, ledger, KPI freeze | Cross-module |
| Cross-references | [Settlement](../quality/finans/settlement), [Manual correction](../quality/finans/manual-correction) | Finance interactions |

The close-day field is on the dealer's parameter set, not on `Filial` — but it's enforced per filial because each filial closes on its own calendar.

## Example

If today is 2026-05-15 and the dealer's close-day setting is **21 days**:

| Order date | Effect |
|---|---|
| 2026-05-14 | Editable |
| 2026-04-25 | Editable (within 21-day rolling window) |
| 2026-04-23 | **Locked** — older than 21 days |
| 2026-03-01 | **Locked** |

Attempting to change `STATUS` on the 2026-03-01 order returns a validation error like *"Order is in closed period — cannot edit"*.

## Common confusions

| Looks like | But actually |
|---|---|
| A separate database snapshot | Close is a *flag check*, not a snapshot — the data stays in the same tables. Reports re-read live rows. |
| Cancel = close | An order's `STATUS=5` (Cancelled) is per-order; close is per-period. A cancelled order in a closed period is **doubly locked**. |
| Close stops new orders | New orders post fine — only the **older** rows freeze. |
| The lock is per-filial | The *setting* is per-dealer; the *enforcement* is per-filial — each filial's close date is evaluated against its own `DATE` rows. |

## Related concepts

- [Defect vs reject](./defect-vs-reject.md) — defects on closed orders are rejected.
- [KPI](./kpi.md) — once a month is closed, KPI scores are final.
- [Server toggles and period close — QA](../quality/settings/server-toggles-and-period-close)
- [Settings module reference](../modules/settings-access-staff)
- [sd-main landmines](../security/sd-main-landmines)
