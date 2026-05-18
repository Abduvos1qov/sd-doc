---
title: Trip lifecycle
sidebar_position: 11
audience: All
summary: A Trip is one delivery run (car + courier + expeditor + ordered list of orders). It moves through 4 states — waiting, active, done, cancelled — and auto-completes when every order it carries is delivered.
topics: [concept, orders, delivery, expeditor]
---

# Trip lifecycle

> **TL;DR** — A **Trip** packages a vehicle, a courier, an expeditor, and a sorted list of `Order` rows for one delivery run. It starts as **waiting** when the dispatcher builds it, becomes **active** once the courier is dispatched, and auto-flips to **done** the moment every order on the trip has reached `STATUS=3` (Delivered). **Cancelled** is a manual abandonment. State writes are concentrated in three places — never invented anywhere else.

## What it is

The Trip is sd-main's *delivery container* — the connective tissue between the Orders module (which makes orders) and the Expeditor module (which carries them). One trip = one truck-and-driver outing on one calendar day.

A trip has:

- A **car** (`CAR_ID` → `{{car}}`) — the physical vehicle.
- A **courier** and an **expeditor** (both `EXPEDITOR_ID`-typed FKs to `{{expeditor}}`) — the people. Often the same person, sometimes split.
- A **store** (`STORE_ID`) — which warehouse the trip loads from.
- A **date** (`DATE`) — the run date.
- A **status** (`STATUS`) — the lifecycle position documented here.
- A **sorted order list** in `{{trip_orders}}` (one row per order, `SORT` column for stop order).

Each `{{order}}` row is mirrored back to the trip via legacy columns `TRIP_NUMBER` and `EXPEDITOR` so mobile (api3/api4) and the on-map view stay consistent without joining `{{trip_orders}}`.

## State diagram

```mermaid
stateDiagram-v2
    [*] --> waiting : TripSaveAction (create)
    waiting --> active : TripSaveAction (status patch)
    waiting --> cancelled : TripSaveAction (status patch)
    active --> done : Trip::finishIfAllDelivered\nlast order reaches STATUS=3
    active --> cancelled : TripSaveAction (status patch)
    done --> [*]
    cancelled --> [*]
```

## Transitions

| From | → To | Trigger | Actor | Side-effects |
|---|---|---|---|---|
| *(none)* | **waiting** | `POST /orders/trip/save` with no `id` (create) | Operator / Operations (RBAC `operation.orders.update`) | New Trip row; `STATUS = 1`; `ACTIVE = 'Y'`; `trip_orders` rows inserted from `orderIds[]`; each linked `{{order}}.TRIP_NUMBER` stamped with the trip id, `{{order}}.EXPEDITOR` stamped with the trip's expeditor. |
| **waiting** | **active** | `POST /orders/trip/save` with `id` + `status: "active"` | Operator / Operations / dispatcher | `STATUS = 2`. Any `orderIds` change re-syncs `{{trip_orders}}` and re-stamps `{{order}}.TRIP_NUMBER` / `EXPEDITOR`. Removed orders have `TRIP_NUMBER = 0` and `EXPEDITOR = ''` reset. (Stock decrement / picking is governed by the Order's own `DOB_STATUS` — not by this transition.) |
| **waiting** | **cancelled** | `POST /orders/trip/save` with `status: "cancelled"` | Operator / Operations | `STATUS = 4`. Orders stay on the trip rows by default — operator must explicitly empty `orderIds` to detach them. |
| **active** | **done** | `Trip::finishIfAllDelivered($orderId)` from `Order::afterSave` on the real `1→3` or `2→3` transition of the *last* pending order | System (Order status change side-effect) | `STATUS = 3` via `$trip->save(false)` (validation skipped). Guard reads: trip has no remaining orders with `STATUS != 3`. Idempotent — re-saving a STATUS=3 order does not re-fire because the parent `Order::afterSave` only calls the helper on `oldStatus !== 3`. |
| **active** | **cancelled** | `POST /orders/trip/save` with `status: "cancelled"` | Operator / Operations | `STATUS = 4`. (Already-delivered orders on the trip keep their `STATUS=3` — cancelling the trip does *not* roll back the order statuses.) |
| **done** | *(any)* | — | — | Terminal. `finishIfAllDelivered` short-circuits if `STATUS` is already `3` or `4`. |
| **cancelled** | *(any)* | — | — | Terminal under current code. (No re-open path implemented.) |

## How orders attach to a trip

`{{trip_orders}}` has a `UNIQUE` constraint on `ORDER_ID` — **one order can be on at most one trip at a time**. The pool of attachable orders (`TripQuery::unassignedOrderIds`) is:

- `o.TYPE = 1` (sale)
- `o.ACTIVE = 'Y'`
- `o.STATUS IN (1, 2)` — New or Shipped only. Delivered / Returned / Cancelled orders are never re-routed.
- `o.DOB_STATUS IN ('picking', 'picked')` — must be in warehouse engagement.
- not already on any trip.

A `TripSaveAction` rewrite with a colliding `ORDER_ID` rolls back the transaction and returns HTTP 409.

## How `finishIfAllDelivered` actually works

```
On every Order save where STATUS becomes 3 and was not previously 3:
  1. Look up the trip via {{trip_orders}}.ORDER_ID → TRIP_ID.
  2. If no trip, no-op.
  3. Count orders on that trip where STATUS != 3.
  4. If any pending, no-op.
  5. Re-read the Trip row.
  6. If STATUS is already 3 (done) or 4 (cancelled), no-op.
  7. Otherwise UPDATE {{trips}} SET STATUS = 3.
```

The helper is deliberately cheap (two indexed reads + at most one UPDATE on the low-contention `{{trips}}` table) so it stays off the deadlock-sensitive `store_detail` write path.

## Where it's used

Modules that read or branch on trip status:

| Module | What it does with `STATUS` |
|---|---|
| `orders/trip/*` actions (`TripSaveAction`, `TripDeleteAction`, `TripAvailableOrdersAction`) | The write surface. Save/delete + return unassigned orders. |
| `components/TripQuery.php` | Read-side helpers — `tripHeaders`, `unassignedOrderIds`, etc. |
| `orders/views/trips/list/_map-sidebar.php` | UI badge — paints waiting/active/done/cancelled chips on the map. |
| `models/Order.php::afterSave` | Triggers `finishIfAllDelivered` on `1/2→3`. |
| Expeditor mobile (api3/api4) | Reads the legacy `{{order}}.TRIP_NUMBER` + `EXPEDITOR` columns — trip rows are *not* sent to mobile; the expeditor sees orders grouped by `EXPEDITOR` only. |
| `modules/pay/components/PaymeHelper`, `modules/pay/controllers/ClickController` | Read Trip rows when reconciling online-payment trip-level summaries. |
| Van-stock (`modules/vs/*`) | Aligns the expeditor's stock packet with the orders mirrored by `{{order}}.TRIP_NUMBER`. The van-stock model itself has its own lifecycle; it does **not** read `{{trips}}.STATUS` directly. |

## Edge cases and gotchas

- **No `STATUS = 1 → 3` or `1 → 4` from the API.** The save action accepts any value, but `Trip::statusFromCode` only maps the four known codes; anything else falls back to `STATUS_WAITING`. Status-only patches still re-stamp orders (idempotent), so a status-only call is safe to retry.
- **`finishIfAllDelivered` skips done and cancelled.** A cancelled trip whose orders later become delivered will *not* be flipped to done — the cancellation sticks.
- **Cancelling does not unstamp orders.** `TripSaveAction` with `status: "cancelled"` leaves `{{trip_orders}}` rows and `{{order}}.TRIP_NUMBER` in place. Only `TripDeleteAction` clears those.
- **`save(false)` in the auto-finish path.** Validation is skipped on purpose — the helper trusts its own guards. Any validation rule added later that should run on done-time auto-completion must be invoked manually.
- **No `done → anything` undo.** If a delivered order is later re-opened to *New* (allowed per [order status transitions](../quality/orders/status-transitions)), the parent trip stays at `done`. Re-delivering that order will *not* re-fire `finishIfAllDelivered` because the trip is already terminal.
- **Order date filter is per-day.** `TripQuery::unassignedOrderIds($date)` scopes by `DATE(o.DATE) = :date` — the dispatcher builds today's trips from today's orders. A picking order from yesterday is invisible unless `$date` is omitted.

## See also

- [Order status transitions](../quality/orders/status-transitions) — the upstream state machine whose `1/2→3` move drives the auto-finish.
- [Visit lifecycle](./visit-lifecycle.md) — adjacent field-side state machine (agent visits, not deliveries).
- [Payment lifecycle](./payment-lifecycle.md) — what happens to the money attached to a delivered trip.
- [Period close](./period-close.md) — closed-period orders cannot have their status changed, so a trip with closed-period orders cannot auto-complete via re-saves of those orders.
- Code: `protected/models/Trip.php`, `protected/components/TripQuery.php`, `protected/modules/orders/actions/trip/*.php`.
