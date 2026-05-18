---
title: Enable Markirovka (CIS) for a product
sidebar_position: 6
audience: End users (admin | warehouse keeper)
summary: Flip a product to require CIS codes, assign its supplier code, and run a first incoming invoice.
topics: [tutorial, how-to, markirovka, stock]
---

# Enable Markirovka (CIS) for a product

**You will**: Mark a single product as a CIS-tracked SKU, attach its supplier code, and run a test incoming invoice so the codes land in the `m_codes` table ready to be used on outgoing orders. By the end you will know how to onboard a new Markirovka SKU end-to-end.
**You need**: A user with role 1 or 9 (admin) and `operation.markirovka.manage`; the supplier's CIS code for the SKU (a 14-digit GTIN or a tenant-specific scheme); an Excel/XML invoice from the supplier with the per-unit codes.
**Time**: ~10 minutes (most of it is uploading the file)
**Hard parts**:
- Setting `MARKIROVKA=1` retroactively does **not** stamp existing stock — only inbound after the flip is tracked.
- The supplier code must match exactly what their invoice files contain, otherwise the importer silently drops rows.

## Step 1 — Flip the product flag

1. Open **Store → Products** (URL: `/store/product/index`).
2. Search for the product by name or SKU. Click the row to edit.
3. Find the **Маркировка** (Markirovka) checkbox. Tick it. This writes `r_product.MARKIROVKA=1`.
4. While you are here, set the **Тип маркировки** to the right Customs scheme (Uzbek tobacco, beverages, dairy, etc) — different schemes use different code formats.
5. Save.

## Step 2 — Attach the supplier code

Some tenants store one supplier code per product (`r_product.SUPPLIER_CODE`); others use a per-supplier mapping table.

1. On the same product edit page, find **Код поставщика**.
2. Type the supplier's exact code. Match case and any leading zeros — the importer is strict.
3. Save.

If your tenant uses the per-supplier mapping, instead go to **Settings → Поставщики** and add a row to the mapping for `(SUPPLIER_ID, PRODUCT_ID, SUPPLIER_CODE)`.

## Step 3 — Run a test incoming invoice

Now upload an inbound invoice that contains this SKU.

Navigate to **Markirovka → Incoming invoices** (URL: `/markirovka/view/incomingInvoices`).

![Annotated screenshot of the incoming invoices grid](/screens/annotated/markirovka_view_incomingInvoices.annotated.png)

1. The data grid (①) lists every prior incoming invoice. Above it, click **+ Загрузить** to upload a new one.
2. Pick the supplier and the warehouse the goods are arriving at.
3. Upload the supplier's XML/Excel file. The importer parses it, matches each line by **supplier code** to your `r_product`, and writes:
   - One row to `m_incoming_invoice` (the header).
   - One row to `m_incoming_invoice_line` per SKU.
   - One row to `m_codes` per individual CIS code (could be hundreds).
4. The grid refreshes; your new invoice is at the top. Click it to see the line breakdown.

## Step 4 — Verify

1. Open the invoice. Each line shows expected count vs. parsed codes. Mismatches are flagged red.
2. Run `SELECT COUNT(*) FROM m_codes WHERE PRODUCT_ID=<your sku> AND STATUS=0;` — this is your unallocated CIS pool. Outgoing orders draw from this pool.
3. Now create a test outgoing order for this SKU on `/orders/view/createOrder` and check that the order's line auto-allocates a CIS code from the pool (the order line gets a `m_codes.ORDER_ID` reference and the code's status flips to `1=allocated`).

## What just happened (under the hood)

`r_product.MARKIROVKA=1` tells the system this SKU requires per-unit tracking. The incoming-invoice upload is handled by `IncomingInvoicesController::actionImport` (route `/markirovka/incomingInvoices/import`) — it parses the file, validates each code against the chosen scheme, and bulk-inserts into `m_codes`. On outgoing orders, `AddOrderController::actionCreate` (or `api3 OrderController::actionPost`) calls the markirovka service to allocate codes from the pool inside the same DB transaction as the order write — so if there are not enough codes, the order is rejected. See the [markirovka module](/docs/modules/markirovka) for the full scheme list and the [orders module](/docs/modules/orders) for how allocation interacts with order status.

## Common mistakes

- **Flipping `MARKIROVKA=1` mid-stock**: existing units already in `r_storeProduct` are **not** retro-coded. You will get "недостаточно кодов" the first time you try to sell them. Either zero out the stock and re-receive, or run the per-unit reconciliation script.
- **Wrong supplier code**: the file imports but every line is skipped because no row in `r_product` matches. Always check the line count after upload.
- **Wrong scheme**: tobacco codes are 29 chars, beverages are 36; choosing the wrong scheme makes the parser reject every line as invalid.

## Next steps

- Run the daily inventory check to make sure your pool counts match physical stock: [Daily stock reconciliation](./daily-stock-reconciliation.md).
- See the codes flow out on real orders: [Create your first order from the web admin](./create-order-web.md).
- Full reference: [markirovka module](/docs/modules/markirovka).
