---
sidebar_position: 9
title: Stock & purchases
---

# Stock and purchases

Once warehouses exist, you need to put goods into them. This page covers two everyday tasks: **receiving a purchase** from a supplier, and **checking what's on hand** in any warehouse.

## Receiving stock from a supplier

### Step 1 — Open the purchases list

From the menu choose **Склад → Поступления** (Warehouse → Purchases), or open `/warehouse/view/listPurchase` directly:

![Purchases list — every supplier receipt](/screens/guide/09-purchases-list.webp)

You see every supplier receipt — date, supplier, warehouse, total amount, status.

### Step 2 — Click "Add purchase"

Click **+ Добавить** (or **+ Новое поступление**) at the top right.

### Step 3 — Fill the header

- **Поставщик** (Supplier) — pick from the list (or add a new one)
- **Склад** (Warehouse) — where the goods go
- **Дата** — date the delivery arrived
- **Номер документа** — supplier's invoice number (match it to the paper)

### Step 4 — Add products line-by-line

For each product in the delivery:

- Type the product name or scan its barcode
- Enter the **quantity received**
- Enter the **price you paid** (per unit)

### Step 5 — Confirm

Click **Сохранить и подтвердить** (Save and confirm). The stock is immediately available — agents can include those products in orders.

:::tip Match the invoice
The number on your purchase document should match the supplier's invoice number. If you ever need to dispute a delivery, identical numbers on both sides make the conversation simple.
:::

## Checking what's in stock

### Step 1 — Open the stock report

Choose **Склад → Остатки** (Warehouse → Balances), or open `/stock/report` directly:

![Stock balance report — products × warehouses](/screens/guide/10-stock-report.webp)

### Step 2 — Apply filters

Filter by:

- **Warehouse** — only one location
- **Product group** — only one category (drinks, food, etc.)
- **Low stock** — only products below a threshold you set

### Step 3 — Export to Excel (optional)

The **Excel** button at the top right exports exactly what you see on screen — same columns, same filters.

## Recording defects & returns

When a product comes back from a client damaged, expired, or refused, the expeditor records it in the mobile app. The system automatically:

1. Adds the goods back to your **defect warehouse**
2. Adjusts the client's balance (if a refund is due)
3. Updates the order so reports reflect the return

## Transfers between warehouses

To move goods (e.g. main depot → van stock):

1. Open **Склад → Перемещения** (Warehouse → Transfers)
2. Click **+ Новое перемещение**
3. Pick the **source** and **destination** warehouses
4. Add products and quantities
5. **Сохранить**

Both warehouses' balances update immediately.

## Tips

- **Confirm purchases the same day** they arrive — unconfirmed stock is invisible to agents.
- **Don't transfer to a van you can't account for** — once goods are in the van, they're the expeditor's responsibility.
- **A weekly stocktake** in your main warehouse catches discrepancies early.

---

**Next:** [Create your first order →](../daily-use/first-order)
