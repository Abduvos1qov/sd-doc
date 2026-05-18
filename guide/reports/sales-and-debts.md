---
sidebar_position: 2
title: Sales & debts
---

# Sales and debts

Two of the most-used reports answer two simple questions: **how much have we sold?** and **who still owes us money?**

## How much have we sold?

### Step 1 — Open the agent sales report

From the menu choose **Отчеты → По агентам** (Reports → By agent), or open `/report/agent` directly:

![Agent sales report — filters + table](/screens/guide/12-report-agent.webp)

### Step 2 — Pick a date range

The top filter strip has:

- **Период** (Period) — pick a date range (today / this week / this month / custom)
- **Филиал** (Branch) — narrow to one office
- **Супервайзер** (Supervisor) — narrow to one team
- **Категория клиента** (Client category) — A/B/C tier filter

The filter strip looks like this on the agent report page:

![Report filter strip — full set of available filters](/screens/guide/46-report-filter-strip.webp)

Filters work together — each one further narrows the report. Click **Сформировать** (Generate) to refresh after changing them.

### Step 3 — Click "Сформировать" (Generate)

The table refreshes with one row per agent. Columns include:

- Total sales
- Order count
- Number of visited clients (OKB)
- Number of clients who ordered (AKB)
- Average bill

### Step 4 — Drill into one agent

Click an agent's row to see their orders, visits, and photos for the period.

### Step 5 — Export to Excel

The **Excel** button at the top right exports the table you see — same columns, same filters.

## Who owes us money?

### Step 1 — Open client payments

From the menu choose **Клиенты → Оплаты** (Clients → Payments), or open `/clients/finans` directly:

![Client payments and debts](/screens/guide/13-client-payments.webp)

You see every client with their current balance — positive means debt, zero means clear.

### Step 2 — Filter by age

The age buckets at the top let you focus on:

- **Less than 7 days** — fresh debt, usually easy to recover
- **7–30 days** — needs a phone call
- **30+ days** — needs to escalate

### Step 3 — Record a payment

When a client pays you (cash, bank transfer, or in person):

1. Click the client's row to open their card
2. Click **+ Добавить оплату** (Add payment)
3. Enter:
   - **Сумма** (Amount)
   - **Тип** (Type: cash / card / bank transfer)
   - **Дата** (Date)
   - **Касса** (Cashbox) — your register
4. Click **Сохранить**

The debt drops immediately. If the cash came from an expeditor, the cashier approves it at end-of-day.

### Step 4 — Approve cash from expeditors (cashier flow)

If your business takes cash at delivery:

1. Open **Платежи → На утверждение** (Payments → Pending)
2. Each row is a cash payment an expeditor recorded today
3. Count the cash, tick **Утверждено** (Approved)
4. The payments now show up in the debt report as cleared

## Tips

- **Run the debt report weekly** — small debts under 7 days are easy; debts older than 30 days rarely come back in full.
- **Always record a reason** when writing off a debt — when finance asks later, the comment saves you.
- **Use aged buckets** to prioritise calls — start with the 30+ days bucket.

---

**Next:** [Online orders →](./online-orders)
