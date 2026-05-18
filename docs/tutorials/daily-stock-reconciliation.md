---
title: Daily stock reconciliation (warehouse)
sidebar_position: 10
audience: End users (warehouse keeper | admin)
summary: Open the warehouse list, run the reconciliation report, flag discrepancies, and post corrections.
topics: [tutorial, how-to, warehouse, stock, inventory]
---

# Daily stock reconciliation (warehouse)

**You will**: Open the warehouse list, scope to today's working warehouse, run the on-hand-vs-system reconciliation, identify discrepancies, and post the per-SKU corrections that bring the system in line with reality. By the end you will know the standard end-of-day warehouse close procedure.
**You need**: A user with role 10 (warehouse keeper) or 1/9 (admin) with `operation.stock.update`; physical counts for any SKUs you suspect of drift (a stocktake sheet, ideally).
**Time**: ~15 minutes depending on warehouse size
**Hard parts**:
- "Stock" is split between `r_storeProduct.COUNT` (total) and `r_storeProduct.RESERVED` (held for unfulfilled orders) — a discrepancy can be on either field.
- Corrections post **immediately** as ledger entries. There is no preview. Always re-count before correcting.

## Step 1 — Open the warehouse list

Navigate to **Warehouse → List** (URL: `/warehouse/list`).

![Annotated screenshot of the warehouse list](/screens/annotated/warehouse_list.annotated.png)

1. Set **Активность** (①) to **Активные** to hide deprecated warehouses.
2. Optionally scope by **Агенты** (②) if you only care about an agent's truck stock.
3. **Способ оплаты** (③) is rarely needed here — leave default.
4. The data grid (④) shows every warehouse with last-movement timestamp and on-hand totals.

Click the warehouse row you are closing for today.

## Step 2 — Run the reconciliation report

Inside the warehouse detail page, find **Отчёты → Сверка остатков** (Reconciliation report) — or use the URL pattern `/warehouse/list/reconcile?id=<warehouseId>`.

The report lists every SKU in this warehouse with three columns:

| Column | Meaning |
|---|---|
| **Системный остаток** | `r_storeProduct.COUNT` for the SKU in this warehouse |
| **Зарезервировано** | `r_storeProduct.RESERVED` (units held for unfulfilled orders) |
| **Доступно** | `COUNT - RESERVED` |

Print or export this list — you will compare it to your physical count.

## Step 3 — Spot discrepancies

For each SKU on the report, write down the **physical count** next to the system count.

A "discrepancy" is any row where physical ≠ system. Common causes:

- **Physical \< system**: shrinkage, breakage, untracked sample-outs, or a mis-counted past receipt.
- **Physical \> system**: a return that never got posted, or an incoming invoice that was posted twice.
- **Both off by an exact small number**: usually a defect that posted to the wrong warehouse.

Flag the rows that need a correction.

## Step 4 — Post corrections

For each flagged SKU:

1. From the warehouse detail page, click **+ Коррекция** (or navigate to **Stock → Excretion** at `/stock/excretion`).
2. Pick the SKU.
3. Enter the **adjustment delta** — positive to add units, negative to remove. (Some tenants ask for the new absolute count and compute the delta; check your form labels.)
4. Pick the **Причина** (Reason) from the configured list: shrinkage, breakage, miscount, found-in-aisle, etc.
5. Add a comment.
6. Save. This calls `POST /stock/excretion/create`, which inside one transaction:
   - Updates `r_storeProduct.COUNT` by the delta.
   - Inserts a row into `d0_stock_movement` with `TYPE=correction` and your reason code.

## Step 5 — Verify

1. Re-run the reconciliation report from step 2. The corrected rows should now match physical.
2. Open the **Stock report** at `/stock/report` and filter by today's date and the reason code. Each correction should appear with your username and timestamp.
3. Sum the corrections by reason — if shrinkage is high every day, escalate to the manager.

## What just happened (under the hood)

The reconciliation page is read-only over `r_storeProduct` joined to `r_product`. Corrections go through `StockExcretionController::actionCreate` (route `/stock/excretion/create`, RBAC `operation.stock.update`) which writes to `r_storeProduct` and `d0_stock_movement` inside one transaction. The full audit trail is queryable via the [stock module's report endpoints](/docs/modules/stock) and the [inventory module](/docs/modules/inventory) for the periodic full-stocktake flow. See also [warehouse module](/docs/modules/warehouse) for warehouse vs store-vs-truck terminology.

## Common mistakes

- **Confusing COUNT with COUNT - RESERVED**: agents have already pre-reserved units against pending orders. If you correct using "available" instead of "total", you will under-count.
- **Posting corrections in the wrong direction**: a delta is from system to physical, not the other way round. If system says 100 and you counted 95, the delta is **-5**, not +5.
- **Forgetting a reason code**: rows with empty reason cannot be summed by category in the monthly shrinkage report — they all land in "misc".
- **Reconciling while orders are still being submitted**: if mobile agents are still posting orders to this warehouse, RESERVED is moving while you count. Either freeze new orders for the close window, or pick a quiet hour.

## Next steps

- Schedule the periodic full stocktake: [inventory module](/docs/modules/inventory).
- Receive the next incoming invoice cleanly: [Enable Markirovka for a product](./configure-markirovka.md) (the incoming-invoice flow there is the same flow used for non-CIS receipts).
- Full warehouse reference: [warehouse module](/docs/modules/warehouse), [stock module](/docs/modules/stock).
