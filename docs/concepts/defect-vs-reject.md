---
title: Defect vs reject
sidebar_position: 5
audience: All
summary: A defect is a per-line return on a delivered order; a reject is a whole-order refusal. Different tables, different consequences.
topics: [concept, orders, delivery]
---

# Defect vs reject

> **TL;DR** — A **defect** is a *per-line* declaration that some items in a delivered order were damaged or unwanted. The order stays in *Delivered*. A **reject** (whole-order return) is when the client refuses the *entire* delivery; the order moves to status **Returned (4)**. They use **different code paths and different tables**.

## What it is

The two terms confuse operators, QA, and even developers because both are "the order didn't go through as expected" — but the data model is sharply split.

**Defect**

- Recorded line by line on a *Delivered* order.
- Written via `EditController::actionPartialDefect` (line 689 of `protected/modules/orders/controllers/EditController.php`).
- The order **stays at STATUS 2 or 3** (Shipped / Delivered).
- `OrderDetail.DEFECT` holds the defective quantity per line; `Order.DEFECT` is the order-level sum.
- A separate row is written to **`d0_defects`** (model `Defects`) for each line.
- If the expeditor has a configured `DEFECT_STORE`, `StoreDetail::exchange_expeditor` moves the quantity back to that warehouse.

**Reject (whole-order return)**

- The client refuses the *entire* delivery at the door.
- The status flips to **4 — Returned**.
- Every line is treated as defective; stock returns to the order's warehouse.
- **No** row in `d0_defects` for a pure reject — the order itself carries the return.
- Handled by the regular status-change flow, *not* by `actionPartialDefect`.

## Why it matters

The two paths differ in:

| Aspect | Defect | Reject |
|---|---|---|
| Order status | Stays Delivered (2/3) | Becomes Returned (4) |
| Affects revenue | Reduces line subtotal | Cancels the whole order revenue |
| Stock movement | To `DEFECT_STORE` (only if expeditor has one) | Back to order's `STORE_ID` |
| Audit row | `d0_defects` per line | None — recorded on `d0_order` |
| KPI | Counts toward defect % | Counts toward return rate |
| Bonus order | Stays attached | Cancelled with the parent |

QA test plans must explicitly cover *both* — using "defect" loosely is a recipe for missed scenarios. See [Partial defect QA](../quality/orders/partial-defect) and [Whole-order return QA](../quality/orders/whole-return).

## How SalesDoctor models it

| Layer | Defect | Reject |
|---|---|---|
| Table | `d0_defects` | `d0_order` (`STATUS=4`) |
| Model | `Defects` (`Defects.php`) | `Order` |
| Action | `EditController::actionPartialDefect` | Standard status-change controller |
| Stock helper | `StoreDetail::exchange_expeditor` to `DEFECT_STORE` | Stock returns to `Order.STORE_ID` |
| Allowed from | `STATUS = 2` or `3` only | Any later status (with re-open rules) |

`Defects` columns: `ID, ORDER_ID, COUNT, CLIENT_ID, STORE_ID, PRODUCT_ID, OP_DATE, TYPE, CREATE_BY, UPDATE_BY, CREATE_AT, UPDATE_AT` (12 columns).

## Example

**Defect** — out of 100 bottles delivered, 4 were broken:

```sql
INSERT INTO d0_defects (ORDER_ID, PRODUCT_ID, COUNT, CLIENT_ID, STORE_ID, OP_DATE, TYPE)
VALUES (50321, 998, 4, 14823, 7, NOW(), 1);

UPDATE d0_order_detail SET DEFECT = 4 WHERE ORDER_ID = 50321 AND PRODUCT_ID = 998;
UPDATE d0_order        SET DEFECT = DEFECT + 4 WHERE ORDER_ID = 50321;
-- STATUS stays 3 (Delivered)
```

**Reject** — the client refused all 100 bottles:

```sql
UPDATE d0_order SET STATUS = 4, DATE_STATUS = NOW() WHERE ORDER_ID = 50321;
-- All 100 bottles return to the order's warehouse via the status-change handler.
-- No row in d0_defects.
```

## Common confusions

| Looks like | But actually |
|---|---|
| "Whole-order defect" | There is no such thing as a 100% defect. If every line is bad, the operator should change the status to Returned. |
| `Order.TYPE = 2` (shelf-return) | A *different* concept again — a `TYPE=2` order is an originating *return* order, created from scratch. Not a defect, not a reject. |
| Audit module's defects | The `audit` module's `AFacing` / `AuditResult` record *merchandising surveys* (shelf placement), not delivery defects. Completely separate path. |
| Reject by the agent | If an *agent* refuses to take an order in (e.g. cash-flow check fails) the order is **Cancelled (5)**, not Returned (4). Different flag again. |

## Related concepts

- [Period close](./period-close.md) — neither defects nor rejects can be edited past the close date.
- [Partial defect — QA workflow](../quality/orders/partial-defect)
- [Whole-order return — QA workflow](../quality/orders/whole-return)
- [Orders module reference](../modules/orders)
- [Bonus vs discount](./bonus-vs-discount.md) — bonus orders attached to rejected parents.
