---
sidebar_position: 1
title: Create your first order
---

# Create your first order

Now that you have agents, clients and stock, you're ready to capture an order. Orders come from three places: the **mobile app** (most orders), the **web app** (this page), or the **online portal**.

## Step 1 — Open the orders list

From the menu choose **Заявки → Список заявок** (Orders → Orders list), or open `/orders/list` directly:

![Orders list — today's and recent orders](/screens/guide/03-orders-list.png)

Every column is filterable — status, agent, client, date, warehouse.

## Step 2 — Click "Добавить"

Click the **+ Добавить** button at the top right. You'll land on the new-order form at `/orders/addOrder`:

![New order form — full view from top to product table](/screens/guide/33-new-order-empty.png)

The form has three sections: the **header** (client, agent, dates), the **product table**, and the **totals row** at the bottom.

## Step 3 — Pick the client

Start typing the client's name in the **Клиент** (Client) field. Suggestions appear after 2–3 letters. Pick the right one.

The system automatically fills in:

- **Тип цены** (Price type) — the price list for this client
- **Условия оплаты** (Payment terms)
- **Кредитный лимит** (Credit limit)

The client picker is a paged table — by default it shows the first 10 of every client you can sell to:

![Client picker — full table of all clients](/screens/guide/40-client-picker.png)

Type any part of the client's name in the **Поиск** (Search) box at the top. The table narrows in real time:

![Client picker with "мага" typed — narrowed list](/screens/guide/41-client-picker-search.png)

Click the row to confirm. The picker closes and the order form moves to the product table.

## Step 4 — Add products

For each product:

1. Type the product name or scan its barcode
2. Set the **количество** (quantity)
3. The **цена** (price) auto-fills from the price list

A running total updates at the bottom as you add lines.

:::tip Discounts and bonuses
If your administrator configured discount rules or buy-X-get-Y promotions, they apply automatically. You'll see the discount appear in the totals — you don't have to calculate anything yourself.
:::

## Step 5 — Pick delivery options

- **Дата отгрузки** (Delivery date) — when the goods should reach the client
- **Склад** (Warehouse) — where the goods will ship from (defaults to the nearest one)
- **Экспедитор** (Expeditor) — who will deliver (can be assigned later)

## Step 6 — Save

Click **Сохранить** (Save). The order moves to status **New** and shows up in the orders list immediately:

![Orders list with the new order at the top](/screens/guide/03-orders-list.png)

## Step 7 — Track the order through its stages

From the orders list, your new order moves through:

1. **New** — just placed
2. **Loaded** — on the expeditor's van
3. **Delivered** — received by the client
4. **Closed** — paid (or moved to debt)

You can click the order row at any stage to see its details, photos taken at delivery, payment status.

## Tips

- **Check the client's debt** before saving a large order — a red warning appears if the new order would push the client over their credit limit.
- **Don't manually edit prices** unless your discount rules require it — the price list is the source of truth.
- **Add a comment** for special instructions ("ring the back door", "ask for Salim").

---

**Next:** [Plan visits →](./plan-visits)
