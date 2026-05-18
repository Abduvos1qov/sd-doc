---
sidebar_position: 7
title: Add clients
---

# Add clients

A **client** in SalesDoctor is anywhere you sell goods — a shop, restaurant, kiosk, supermarket. Every order, debt, visit and KPI traces back to a client, so this list is the heart of your system.

## Step 1 — Open the clients list

From the menu choose **Клиенты → Все клиенты** (Clients → All clients), or open `/clients/client` directly:

![Clients list — search bar, filters, and table](/screens/guide/05-clients-list.png)

The list shows every client with their phone, address, channel, and credit balance.

## Step 2 — Filter or search for an existing client

Before adding a duplicate, search by name or phone in the top search box. If the client already exists, click their row to open and edit.

## Step 3 — Click "Add client"

Click the **+ Добавить** (Add) button at the top right.

## Step 4 — Fill in the basic information

| Field | What to enter |
|-------|---------------|
| **Название** | Official name of the shop or business |
| **Телефон** | Working number (used for SMS and order confirmations) |
| **Адрес** | Street address the agent can read off the door |
| **Регион / Территория** | Geographic placement |
| **Канал** | Type of outlet — shop, supermarket, restaurant, café |
| **Тип цены** | Which price list this client buys at |
| **Агент** | Agent responsible for visiting this client |

## Step 5 — Add location (recommended)

If an agent is at the shop right now, the **mobile app** captures the GPS location with one tap. From the web, you can paste latitude/longitude or click on the map.

Good GPS makes visit verification automatic later.

## Step 6 — Set trading conditions (optional)

- **Тип оплаты** — cash on delivery, on credit, or bank transfer
- **Кредитный лимит** — maximum the shop can owe you at any time

## Step 7 — Save

Click **Сохранить** (Save). The client appears in the list immediately and is available for new orders.

## Bulk-add many clients

If you have an existing list in Excel, use the import page at `/clients/client/import`:

![Clients Excel import](/screens/guide/32-clients-import.png)

Download the template, fill it in, upload it back, and every row becomes a client in one pass.

## When clients are added from the field

Most clients get added by agents while visiting. The agent taps **+ Добавить клиента** on their phone, the location is captured automatically, and the new client shows up in the office within seconds.

:::tip Clean names
"Магазин 'Yulduz', ул. Навои 10" reads better than "MAGAZIN YULDUZ NAVOI 10". The cleaner the name, the easier it is to search.
:::

---

**Next:** [Set up warehouses →](./set-up-warehouses)
