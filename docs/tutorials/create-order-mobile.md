---
title: Create an order from the mobile agent app
sidebar_position: 2
audience: End users (field agent | sales rep)
summary: Check in at the outlet, capture a multi-line order on the phone, and submit it through api3.
topics: [tutorial, how-to, orders, mobile]
---

# Create an order from the mobile agent app

**You will**: Open the SalesDoctor mobile app at a customer outlet, check in via GPS, build an order line-by-line, and post it to the server with a single tap. By the end you will know how field agents submit ~90% of all orders in the system.
**You need**: A user with role `4` (agent), assigned to an active route that includes today's outlet; the SalesDoctor Android app signed in and synced; GPS permission **Always** granted on the device.
**Time**: ~3 minutes per order
**Hard parts**:
- If GPS accuracy is worse than `enableGpsAccuracy` (default 50 m), the check-in is rejected — agents in basements get stuck here.
- The submit endpoint accepts **partial** payloads; a flaky network leaves zombies — always wait for the green tick.

## Step 1 — Open the outlet from today's route

In the mobile app, open the **Маршрут** (route) tab. Today's planned visits are listed in visit order; outlets you have already visited show a checkmark badge.

1. Tap the outlet card.
2. The app calls `GET /api3/visit/start` with your current GPS coordinates.
3. If the device is within `RADIUS` metres of `d0_client.LAT/LON`, the server creates a `d0_visit` row and the **Sales** button becomes active. Otherwise you see "Вы слишком далеко от клиента" — walk closer.

## Step 2 — Build the order

Inside the visit, tap **Заказ** to open the order screen.

1. Pick a price type if more than one is configured for the client.
2. Tap **+ Товар** to open the product search. Type 2+ characters or scan the barcode.
3. For each product, set the count. The app shows live stock available from your assigned store (the truck) — you cannot oversell.
4. Apply a per-line discount if your role is allowed by `enableDiscount`.

The bottom bar shows running subtotal, discount, and final price. Bonus lines (if any rule matches) are appended automatically — they cannot be deleted but can be swapped for an alternative bonus SKU.

## Step 3 — Submit

Tap **Сохранить** at the top right.

1. The app calls `POST /api3/order/post` with the full payload (header + lines + photo evidence + GPS).
2. The button shows a spinner while the server runs validation. On success you see a green tick and return to the visit screen.
3. The order ID is now visible in the visit's order list with status **Новый**.

If your device is offline, the order is queued locally and re-tried on the next sync — but it is **not** posted to the server yet. Always confirm the green tick before leaving the outlet.

## Step 4 — Close the visit

1. Optionally take a "before"/"after" merchandising photo (this triggers the `audit` module's photo report).
2. Tap **Завершить визит**. The app calls `POST /api3/visit/end`; the server stamps `d0_visit.END_DATE` and the visit card flips to "completed" on the route.

## Step 5 — Verify on the web

Have a manager open `/orders/list` on the web admin and filter by today's date and your agent name. The order you just submitted should appear with status **Новый** (`STATUS=1`) and the correct outlet, lines, and GPS coordinates. The visit also appears in the [GPS module](/docs/modules/gps) tracking table.

## What just happened (under the hood)

`POST /api3/order/post` is handled by `OrderController::actionPost` in `protected/modules/api3/controllers/OrderController.php`. Inside one DB transaction the controller validates GPS distance vs `d0_client.LAT/LON`, writes `d0_order` (header), `d0_order_product` (lines), reserves stock on `r_storeProduct`, appends `d0_order_status_history`, and — if the tenant has Markirovka enabled — validates each CIS code against `m_codes`. The response includes the new `ORDER_ID` which the app caches for retry idempotency.

## Common mistakes

- **GPS rejected**: the agent is too far from the client's stored coordinates. Either move closer, or have a supervisor update `d0_client.LAT/LON` (some outlets get re-located but the admin record stays stale).
- **Submit hangs and you walk away**: do not. The local queue retries, but until the server returns 200 the order is *not real*. Cashiers and KPI counters do not see queued orders.
- **Over-sold from a stale truck stock**: the app caches stock for the day; if you have not synced in the morning, you will see yesterday's numbers. Pull-to-refresh before the first visit.

## Next steps

- Need to record a cash payment from the agent? Read [Register a payment from an agent](./register-payment.md).
- Configure markirovka so CIS codes get validated on submit: [Enable Markirovka for a product](./configure-markirovka.md).
- Full mobile API reference: [API v3 — Mobile agent](/docs/api/api-v3-mobile/index).
