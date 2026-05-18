---
sidebar_position: 3
title: Navigating the app
---

# Finding your way around

SalesDoctor groups every feature into a small number of clear menus. Once you know where each menu lives, you'll never be more than two clicks from anywhere.

## Step 1 — Read the top bar

Along the top of every page:

![SalesDoctor dashboard with the top bar visible](/screens/guide/02-dashboard-home.webp)

- **Logo (top left)** — returns to the home dashboard
- **Notification bell** — new orders, finished deliveries, approval requests
- **Account menu (top right)** — language, password, sign out

## Step 2 — Read the side menu

The left-hand menu lists every major workspace:

| Menu | What's inside | Direct URL |
|------|---------------|-----------|
| **Планы** | Visit and sales planning | `/planning/monthly` |
| **Заявки** | Sales, returns, deliveries | `/orders/list` |
| **Склад** | Warehouses, stock, purchases | `/warehouse/list` |
| **Маркировка** | CIS / EDI compliance | `/markirovka/view/incomingInvoices` |
| **Клиенты** | Customer list, payments, debts | `/clients/client` |
| **Команда** | Auditors, supervisors, expeditors, users | `/team/auditor` |
| **Аудит 2** | Merchandising audit | `/audit/photoReport` |
| **Настройки** | Prices, currencies, branches | `/settings/diler` |

:::tip Menu items you don't see
If a menu group is missing for you, it usually means your role doesn't need it. An administrator can grant access via **Настройки → Доступ**.
:::

## Step 3 — Use direct URLs

Every page has a stable URL — bookmark frequently-used reports. Common ones:

| URL | What it opens |
|-----|---------------|
| `/dashboard/supervayzer` | Today's team dashboard |
| `/dashboard/kpi` | Monthly KPI dashboard |
| `/orders/list` | Orders list |
| `/orders/addOrder` | New-order form |
| `/clients/client` | Clients list |
| `/clients/finans` | Client payments & debts |
| `/report/agent` | Sales report by agent |
| `/report/customer` | Sales report by customer |

## Step 4 — Open in a new tab

`Ctrl + Click` (or `Cmd + Click` on a Mac) on any menu item opens it in a new browser tab. Useful when you want the dashboard open while working in another report.

## Step 5 — Change the language

Open your account menu (top right) → **Язык** (Language). Your choice is remembered for next sign-in. Supported: Русский, O'zbekcha, English.

## Pickers, search, and filters

Every list page in SalesDoctor follows the same three-layer pattern.

**1. A search box at the top right** — types a few characters and the table narrows in real time. Works on any text column (client name, agent name, login, product name, order number).

**2. A filter strip below the heading** — multi-select dropdowns. Clicking a dropdown opens a checkable list; pick one or many values. The grid refreshes immediately.

![Clients list filter panel expanded](/screens/guide/45-clients-filter-panel.webp)

**3. A picker dialog inside a form** — when the form needs you to pick an existing record (client, product, warehouse), it opens a paged table with its own search:

![Client picker — paged table with search](/screens/guide/40-client-picker.webp)

A few rules of thumb:

- The search is **substring** match — `мага` finds *Магазин Юлдуз*, *Магистраль*, *Гранд-Мага*.
- Filters **stack** — selecting Region = Tashkent AND Channel = supermarket narrows to outlets that match both.
- Filter state lives in the URL — copy the URL and a colleague gets your exact view.
- **Сбросить фильтр** (Reset filter) clears every filter at once.

## Tips

- **Stable URLs** — bookmark frequently used pages.
- **Browser back button** works everywhere — no in-app "back" needed.
- **Refresh after long idle** — if data looks stale, press `F5`.

---

**Next:** [Add agents →](./add-agents)
