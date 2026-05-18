---
sidebar_position: 3
title: Track orders
---

# Track orders through the day

After an order is created, it moves through clear stages. Knowing where every order is right now helps you spot problems early — a van still not loaded at noon, a client who refused half the order, a payment not collected.

## Step 1 — Open the orders list

From the menu choose **Заявки → Список заявок**, or open `/orders/list` directly:

![Orders list with status column](/screens/guide/03-orders-list.webp)

Each row is an order. The **Статус** column tells you which stage it's in.

## Step 2 — Read the statuses

| Status | Meaning |
|--------|---------|
| **Новая** | Just placed. Nothing has shipped yet. |
| **Загружена** | Goods are on the expeditor's van and on the way. |
| **Доставлена** | Client has received the goods. Payment may still be pending. |
| **Возврат частичный** | Client refused some items; the rest was accepted. |
| **Возврат полный** | The entire order was refused. |
| **Отменена** | Killed before delivery. |

## Filter the list

The orders list has three filter levers at the top.

### By date range

Click the date field to open a two-month calendar:

![Date range picker open](/screens/guide/42-date-range-picker.webp)

Pick the start and end dates, then click anywhere outside to apply.

### By date type

The dropdown to the left of the date field switches which date the range applies to:

![Date type dropdown — order date, ship date, delivery date](/screens/guide/43-date-type-dropdown.webp)

- **Дата заявки** — when the order was placed
- **Дата отгрузки** — when the goods left the warehouse
- **Дата доставки** — when the client received the goods

### By status (and the rest of the filter strip)

The filter strip below the heading has many dropdowns — status, order type, client category, territory, supervisor, agent, expeditor, price type, channel, warehouse, product category:

![Order status filter dropdown opened](/screens/guide/44-status-filter-dropdown.webp)

Click any dropdown to multi-select values. The grid below refreshes as you change filters.

Click **Сбросить фильтр** (Reset filter) at the right end of the strip to clear everything at once.

## Step 3 — Drill into one order

Click any order row to open its full details:

- All product lines with prices
- Who created it (agent, web user, or online portal)
- Who is delivering it
- Photos taken at delivery
- Payment status

## Step 4 — Watch the live trips view

For a per-van picture, open **Заявки → Рейсы** (Trips):

![Trips view](/screens/guide/20-trips-view.webp)

You see every expeditor's trip with stops, money carried, and anomalies.

## Handling problems

### Partial refusal at the door

When a client refuses some items, your expeditor records it in the mobile app. The system automatically:

- Removes the refused items from the invoice
- Returns the goods to your defect warehouse
- Adjusts the amount the client owes

The change shows up on the dashboard within seconds. See refusals filtered separately at `/orders/rejects`:

![Order rejects / returns list](/screens/guide/25-orders-rejects.webp)

### Full refusal

Same flow, the entire order is rejected. The van brings everything back.

### Recovering a cancelled order

If an order was cancelled by mistake, you can restore it from `/orders/recovery`:

![Order recovery view](/screens/guide/26-orders-recovery.webp)

1. Find the cancelled order
2. Click **Восстановить** (Restore)
3. The order returns to its previous status and goods are reserved again

## Step 5 — Close the day

At end of day:

- Check that no orders are still **Загружена** (Loaded) — they didn't reach the client
- Confirm the expeditor has returned with the right stock and money
- Approve any pending payments (see [Sales & debts](../reports/sales-and-debts))

## Tips

- **Don't edit a delivered order** unless absolutely necessary — it confuses the client and your accountant.
- **Use the comment field** for anything unusual — when finance asks next week, the comment saves you.
- **Watch repeat refusals** at one client — that's a signal something is off (price, channel mismatch, stale relationship).

---

**Next:** [Agent mobile app →](../mobile/agent-app)
