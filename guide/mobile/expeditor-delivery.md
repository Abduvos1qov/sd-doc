---
sidebar_position: 3
title: Expeditor delivery
---

# Expeditor delivery flow

The expeditor is the person bringing goods to clients. Their day is built around the **trip** — a planned set of stops with a known load, an expected route, and an expected time back at the warehouse.

## What the expeditor does on the phone

| Step | What happens |
|------|--------------|
| **1. Morning — pick up load** | Open today's trip, confirm goods loaded into van |
| **2. On the road — deliver** | At each stop: open order, unload, client signs, record payment |
| **3. Handle returns** | Refused goods stay on the van; partial refusals adjust the invoice |
| **4. End of day — return** | Drop unsold goods at the warehouse, hand cash to cashier |

## Step 1 — Watch the live trip in the office

Open **Заявки → Рейсы** (`/orders/view/trips`):

![Trips view — every active delivery](/screens/guide/20-trips-view.png)

You see all expeditors out today with:

- Stops completed vs planned
- Cash currently on the van
- Last GPS position
- Anomalies (long stop, off-route, missed)

## Step 2 — Read the order list for context

From `/orders/list`, filter by **Сегодняшние** (Today) and group by expeditor to see who's delivering what:

![Today's orders by expeditor](/screens/guide/03-orders-list.png)

## Step 3 — Approve cash at end of day

When the expeditor returns, they hand cash to the cashier. The cashier opens `/payment/approval`:

![Payment approval queue](/screens/guide/21-payment-approval.png)

Each row is a payment the expeditor recorded today. The cashier:

1. Counts the cash for that order
2. Ticks **Утверждено** (Approved) if matching
3. The payment now shows up as cleared in the debt report

## Step 4 — Close the trip

Once all of an expeditor's orders are either Delivered or Returned, and all cash is approved, the trip moves to **Завершён** (Closed). You'll see it disappear from the live trips view.

## Three common payment patterns

| Pattern | What the expeditor does |
|---------|-------------------------|
| **Cash on delivery** | Counts cash at the door, marks it received in the app |
| **Card on delivery** | Accepts card payment (if your business supports it) |
| **On credit** | Marks the order as "to be paid later" — debt updates instantly |

The cash and card totals are tallied on the phone in real time, so the expeditor always knows what they're carrying.

## Tips

- **Don't change the load mid-day** — adding an order to a van already on the road is the most common source of disputes.
- **Give the expeditor a power bank** — a dead phone in the middle of a route is bad news.
- **One trip per van per day** — if you need two trips, close the first cleanly before starting the second.

---

**Next:** [Dashboard & KPI →](../reports/dashboard-kpi)
