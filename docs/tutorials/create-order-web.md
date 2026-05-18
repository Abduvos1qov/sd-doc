---
title: Create your first order from the web admin
sidebar_position: 1
audience: End users (operator | manager)
summary: Pick a client, add one product line, save the order, and find it on the orders list.
topics: [tutorial, how-to, orders]
---

# Create your first order from the web admin

**You will**: Issue a brand-new order to an existing client, add a single product line, and confirm it appears on the orders grid. By the end you will know the canonical web order-entry flow that operators use every day.
**You need**: A user with role 1, 2, 3, 5 or 9 (RBAC: `operation.orders.create`); at least one active client in your filial; at least one product on an active price type.
**Time**: ~5 minutes
**Hard parts**:
- The page filters in your filial by default — picking the wrong **Агент** silently narrows the client list.
- Stock is **reserved at save** (not at submit) — if another operator is in flight you can be beaten to the inventory.

## Step 1 — Open the new-order page

Open the admin and go to **Orders → Add order** (URL: `/orders/view/createOrder`).

![Annotated screenshot of the create-order page](/screens/annotated/orders_view_createOrder.annotated.png)

1. Pick the **Агент** in ① — this scopes the visible clients/routes to that agent.
2. Optionally narrow further with **Территория** (②), **Категория клиентов** (③) and **Дни посещений** (④).
3. The data grid (⑤) refreshes with the candidate clients you can write an order to.

If the grid is empty, your role is probably scoped to a different filial — check the top-right filial picker first.

## Step 2 — Pick a client and start the order

1. Click any client row in the grid (⑤). The line-entry pane opens.
2. The price type defaults to the client's assigned price (`d0_client.PRICE_TYPE_ID`). If you need a different one, override it before you add lines — switching the price type after adding lines re-prices everything.

## Step 3 — Add one product line

1. Type the product name or barcode into the search box at the top of the line table.
2. Set the **Кол-во** (count) field. Stock checks run on blur; if you ask for more than `r_storeProduct.COUNT - RESERVED`, the field turns red and **Save** stays disabled.
3. Hit **Add** (or press **Enter**) to materialize the line.

The header subtotal and final price update live as you type.

## Step 4 — Save and verify

1. Press **Save**. The request goes to `POST /orders/addOrder/create`.
2. You are redirected to `/orders/list`. Look for the topmost row — `ORDER_ID` is sequential and the status will be **New** (or **Draft** if your tenant requires manager approval).
3. Click the order to open the editor. The single line you added should be present, and `RESERVED` on the source store-product row should now reflect your quantity.

## What just happened (under the hood)

The save call hits `AddOrderController::actionCreate` (route `/orders/addOrder/create`, RBAC `operation.orders.create`). Inside a DB transaction the controller writes one row to `d0_order` (header) and one to `d0_order_product` (line), increments `r_storeProduct.RESERVED`, and appends an entry to `d0_order_status_history`. If the tenant has `enableApproveOrders=1` the order lands in status `0` (Draft) instead of `1` (New), waiting on a manager approve. See [orders module reference](/docs/modules/orders) for the full status machine.

## Common mistakes

- **Wrong filial selected**: the top-right filial dropdown silently filters everything. The order will save but to a filial you didn't intend, and your KPI/dashboard reports won't show it where you expect.
- **Adding lines before picking the price type**: re-pricing after the fact is correct but surprising — operators panic when the header total jumps.
- **Saving with `RESERVED` warnings on a line**: the front-end blocks save, but the count message is in small grey text under the field. Look at the line, not the toolbar.

## Next steps

- Already comfortable with the desktop flow? Read [Create an order from the mobile agent app](./create-order-mobile.md).
- Need to register the cash payment after delivery? See [Register a payment from an agent](./register-payment.md).
- Full reference of every status and column: [orders module](/docs/modules/orders).
