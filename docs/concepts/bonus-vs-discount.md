---
title: Bonus vs discount
sidebar_position: 8
audience: All
summary: A bonus is free product; a discount is a price reduction. Different tables, different ledger effects.
topics: [concept, orders, pricing]
---

# Bonus vs discount

> **TL;DR** — A **discount** reduces the *unit price* of a line (the client pays less). A **bonus** delivers a *separate "sister" order* of free product (the client pays the same but gets more). Bonuses are tracked as their own order row, linked back via `BONUS_ORDER_ID`. Discounts modify the main order's line totals.

## What it is

Both are promotional incentives, but the data model and ledger consequence differ.

**Discount**

- Lives **on the main order**.
- Either a **per-line** discount (modifies one line's unit price) or a **header** discount (modifies the order subtotal).
- `Order.DISCOUNT` is the order-level sum; `OrderDetail.DISCOUNT` is per-line.
- Reduces the **revenue** that lands in the ledger.
- Two flavours: **auto-discount** (system picks a matching rule) and **manual-discount** (operator/agent types it).

**Bonus**

- Lives in a **separate `BonusOrder` row** in `d0_bonus_order`, linked back to the main order via `BONUS_ORDER_ID` on `d0_order`.
- Carries its own line items in `d0_bonus_order_detail`.
- Travels alongside the main order through delivery, but carries **zero monetary value** in the ledger.
- Three flavours: **auto-bonus** (system picks the free SKUs), **retro-bonus** (the agent picks them on the mobile app), and **manual edit** (operator edits the bonus order from the web after the main order is saved).

See [Orders module reference](../modules/orders#bonuses) for the linkage.

## Why it matters

The choice between bonus and discount carries strategic weight:

| Choice | Effect on revenue | Effect on stock | Effect on customer perception |
|---|---|---|---|
| Discount | Lower revenue per unit sold | Same units shipped | "Lower price" |
| Bonus | Same revenue per unit sold | Extra units shipped | "Free product" |

For accounting, bonuses are *cost of promotion* (free stock), not revenue erosion. For QA, **a returned/rejected main order must also cancel its bonus** — orphan bonus orders are a common bug.

## How SalesDoctor models it

| Layer | Discount | Bonus |
|---|---|---|
| Order-level field | `Order.DISCOUNT` | `Order.BONUS_ORDER_ID` |
| Line-level field | `OrderDetail.DISCOUNT` | (lines on `d0_bonus_order_detail`) |
| Separate header row | None | `BonusOrder` (`d0_bonus_order`) |
| Separate line table | None | `d0_bonus_order_detail` |
| Rule tables | `d0_skidka` (manual), auto-discount rule tables | `d0_bonus_agent`, `d0_bonus_filial`, etc. |
| QA workflow | [Discounts](../quality/orders/discounts) | [Bonuses](../quality/orders/bonuses) |
| Settings | [Discount rules](../quality/settings/discount-rules) | [Bonus rules](../quality/settings/bonus-rules) |

`BonusOrder` columns: `BONUS_ORDER_ID, ORDER_ID, DILER_ID, CLIENT_ID, CLIENT_CAT, AGENT_ID, COUNT, VOLUME, CITY_ID, DATE, DATE_LOAD, STATUS, EXPEDITOR, COMMENT, ...` (22 columns).

## Example

**Discount** — 5% off a 1 000 000 UZS order:

```sql
UPDATE d0_order SET DISCOUNT = 50000, SUMMA = 950000 WHERE ORDER_ID = 50321;
```

The ledger sees 950 000 UZS as revenue.

**Bonus** — buy 100 bottles, get 5 free:

```sql
-- Main order untouched (still 100 bottles @ 10 000 = 1 000 000 UZS)
INSERT INTO d0_bonus_order (ORDER_ID, CLIENT_ID, AGENT_ID, COUNT, ...)
VALUES (50321, 14823, 42, 5, ...);
-- And 5 free bottles in d0_bonus_order_detail
UPDATE d0_order SET BONUS_ORDER_ID = LAST_INSERT_ID() WHERE ORDER_ID = 50321;
```

The ledger sees 1 000 000 UZS as revenue; the warehouse ships 105 bottles.

## Common confusions

| Looks like | But actually |
|---|---|
| Bonus reduces price | No — bonus adds free product. Revenue stays the same. |
| Free product is a discounted line | A bonus is its **own order** linked to the main one. Don't expect to find the free SKU on the main order's `OrderDetail`. |
| Cancelling main order cancels bonus automatically | The cascade *should* happen, but it's a frequent bug source — verify the bonus is also cancelled. |
| Retro-bonus = retroactive | Retro-bonus = the **agent picks the free SKUs** at order time (vs auto-bonus where the system does). Not "applied later". |

## Related concepts

- [Price type](./price-type.md) — discount and bonus rules can filter by price type.
- [Defect vs reject](./defect-vs-reject.md) — what happens to the bonus when the main is rejected.
- [Bonuses — QA workflow](../quality/orders/bonuses)
- [Discounts — QA workflow](../quality/orders/discounts)
- [Orders module reference](../modules/orders)
