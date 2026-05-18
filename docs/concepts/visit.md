---
title: Visit (vs check-in)
sidebar_position: 10
audience: All
summary: A Visit is the planned/actual sales call to one outlet. A check-in is a single GPS event inside that visit.
topics: [concept, mobile, audit]
---

# Visit — agent's call at one outlet

> **TL;DR** — A **Visit** is one row recording that an agent went to one outlet on one date. It carries the planned-vs-actual flag, the check-in/check-out timestamps, the GPS pin, and links to what happened (orders, audit, payment, delivery). A **check-in** is a *single GPS event* inside the visit — a visit has at most one check-in and at most one check-out.

## What it is

A visit is the atomic unit of field activity. Every interaction between an agent and an outlet is "inside a visit":

- The agent **plans** to visit an outlet today (per the route).
- The agent **checks in** when they arrive (the mobile app sends GPS coordinates).
- During the visit, the agent may do any of: take an order, complete an audit form, take a payment, accept a return, photograph the shelf.
- The agent **checks out** when leaving.

Internally one `Visit` row covers the entire call — start, end, and outcomes. Don't confuse it with low-level GPS pings: those flood in continuously throughout the day; visits are the bracketed events.

## Why it matters

Visits drive the visibility layer that the supervisor and the dealer look at:

- **Coverage** — did the agent visit the outlets they should have? (`PLANED` = yes/no)
- **Productivity** — what did the visit produce? (`ORDER`, `AUDIT`, `PAYMENT`, `DELIVERY` flags)
- **Trust** — was the GPS pin near the outlet? (`DISTANCE`, `GPS_STATUS`)
- **АКБ** computation joins to `d0_order` but visits give the OKB / conversion view.

For QA: every audit-module test and every order-from-mobile test happens inside a Visit context.

## How SalesDoctor models it

| Layer | Identifier | Where |
|---|---|---|
| Table | `d0_visit` | Model `Visit` (`Visit.php`) |
| Parent | `BaseFilial` | Auto-scoped |
| Mobile endpoint | `/api3/visit/index`, `/api3/visit/post`, `/api3/visit/postCheck` | Agent app submission |
| Web view | `/adt/visit/index`, `/adt/visit/detail`, `/adt/visit/view`, `/adt/visit/updateAudit`, `/adt/visit/updatePoll` | Audit / ADT module |
| QA workflow | [Visit audit](../quality/audit/visit-audit) | Operator guide |

Key columns on `d0_visit` (27 total):

```
ID, AGENT_ID, USER_ID, CLIENT_ID, DATE,
VISITED, ORDER, REJECT, PHOTO, AUDIT,
LON, LAT, DISTANCE, GPS_STATUS,
CHECK_IN_TIME, CHECK_OUT_TIME,
PLANED, STORE_CHECK, PAYMENT, DELIVERY, ...
```

The outcome flags (`ORDER`, `REJECT`, `PHOTO`, `AUDIT`, `PAYMENT`, `DELIVERY`, `STORE_CHECK`) are independent booleans — a single visit can produce all of them.

## Example

A productive visit looks like this:

| ID | AGENT_ID | CLIENT_ID | DATE | PLANED | VISITED | ORDER | AUDIT | CHECK_IN_TIME | CHECK_OUT_TIME | LAT | LON | DISTANCE | GPS_STATUS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8821 | 42 | 14823 | 2026-05-15 | 1 | 1 | 1 | 1 | 09:14 | 09:38 | 41.3625 | 69.2871 | 18 m | 0 (ok) |

An off-route visit:

| ID | AGENT_ID | CLIENT_ID | DATE | PLANED | VISITED | ORDER | DISTANCE | GPS_STATUS |
|---|---|---|---|---|---|---|---|---|
| 8822 | 42 | 14844 | 2026-05-15 | 0 | 1 | 0 | 412 m | 1 (out of zone) |

`PLANED = 0` means the agent visited an outlet that was not on today's route; `GPS_STATUS = 1` flags an out-of-zone check-in (the agent stood farther from the outlet than the configured geofence radius).

## Common confusions

| Looks like | But actually |
|---|---|
| Visit = check-in | A visit contains *one* check-in and *one* check-out. They're columns on the same row, not separate events. |
| GPS pings = visits | Background GPS pings are stored elsewhere (the GPS modules) at high frequency. The visit only records the *check-in* coordinate. |
| Reject on a visit = order reject | `Visit.REJECT` = "visited but no order taken". Distinct from order-level reject (status 4). |
| Audit = visit | An audit-module form is **filled inside a visit** but is a separate row in the audit tables (AFacing / AuditResult). The visit's `AUDIT = 1` is just the boolean flag. |

## Related concepts

- [Outlet](./outlet.md)
- [AKB](./akb.md)
- [Defect vs reject](./defect-vs-reject.md)
- [Audit module (ADT)](../modules/audit-adt)
- [Visit audit — QA workflow](../quality/audit/visit-audit)
- [GPS tracking — QA workflow](../quality/mobile/gps-tracking)
