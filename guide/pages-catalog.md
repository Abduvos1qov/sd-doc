---
sidebar_position: 100
title: Pages & forms catalog
---

# Every page, every form — full catalog

A single scrollable reference. Each section shows: a screenshot of the page, what it's for, what forms / actions it has, and which page you go to next from there.

Use the search at top right (or `Ctrl+F`) to find a specific page by name.

## How to read this catalog

Each catalog entry has:
- **Screenshot** — what you'll see when you open the URL
- **URL** — direct path (you can bookmark it)
- **What's on it** — primary fields, columns, action buttons
- **Where you go next** — typical follow-up clicks

All screenshots come from a real demo tenant. Numbers and names will differ in your account but the layout is the same.

---

## 1. Login & home

### 1.1 Login screen

URL: `/site/login`

![Login screen](/screens/guide/01-login-screen.png)

What's on it:
- **Логин** (Login) text field — usually your phone number or assigned username
- **Пароль** (Password) text field
- **Запомнить меня** (Remember me) checkbox — keeps you signed in on this browser
- **Войти** (Sign in) button
- Language switcher in the corner (RU / UZ)

Where you go next:
- **Sign in** as a supervisor / admin → supervisor home dashboard
- **Sign in** as an owner with multiple roles → role picker, then dashboard

### 1.2 Supervisor home dashboard

URL: `/dashboard/supervayzer`

![Supervisor home dashboard](/screens/guide/39-supervisor-dashboard-full.png)

What's on it:
- Headline KPI tiles across the top: **Продажи** (Sales), **Визиты** (Visits), **АКБ** (Active client base), **ОКБ** (General client base), **Долг** (Debt), **Заказы в ожидании** (Pending orders)
- Period selector (Сегодня / Вчера / Неделя / Месяц)
- Period chart strip — sales by day for the selected window
- Per-agent activity table — one row per agent with their day so far

Where you go next:
- **Click "Продажи" tile** → sales dashboard
- **Click "Долг" tile** → finance dashboard
- **Click "Визиты" tile** → visit report
- **Click an agent's name** → agent profile

### 1.3 Sales dashboard

URL: `/dashboard/sales`

![Sales dashboard](/screens/guide/34-dashboard-sales.png)

What's on it:
- Sales totals broken down by agent / region / product group
- Today vs last week comparison chart
- Top clients by spend
- Returns row at the bottom

Where you go next:
- **Click an agent in the chart** → agent sales report pre-filtered to that person
- **Click a product group** → product-level report

### 1.4 Finance dashboard

URL: `/dashboard/finans`

![Finance dashboard](/screens/guide/35-dashboard-finans.png)

What's on it:
- Total receivable headline number with aged buckets (less than 7 days / 7–30 / 30+ days)
- Today's payments by cashbox (cash / bank / card / Click / Payme)
- Top debtors list — biggest open balances

Where you go next:
- **Click a debtor** → client payments / debt page filtered to that client
- **Click a cashbox row** → payment approval queue for that cashbox

### 1.5 KPI dashboard (monthly)

URL: `/dashboard/kpi`

![KPI dashboard](/screens/guide/38-dashboard-kpi-full.png)

What's on it:
- One row per agent
- Progress bars per indicator: Sales / AKB / OKB / Visits / Photos / MML
- Plan vs fact percentages
- Colour coding: green = on track, amber = behind, red = far behind

Where you go next:
- **Click an agent row** → agent profile
- **Click an indicator header** → drill into that metric across the whole team

### 1.6 Billing dashboard (license usage)

URL: `/dashboard/billing`

What's on it:
- Current license balance
- Active seats vs purchased seats
- Renewal date
- Recent payments list

*(Screenshot pending — billing page requires a connected vendor host.)*

---

## 2. Orders

### 2.1 Orders list

URL: `/orders/list`

![Orders list](/screens/guide/03-orders-list.png)

What's on it:
- Filter strip across the top: **date range**, **status**, **agent**, **expeditor**, **warehouse**, **channel**, **client**, **payment method**
- Action buttons: **Добавить** (Add), **Накладные** (Invoices), **Групповая обработка** (Bulk processing), **Отчёты** (Reports), **Excel**
- Table columns: №, type, status, agent, client, balance, amount, debt, order date, ship date, delivery date, expeditor, warehouse
- Status colour pill at the start of each row
- Pagination at the bottom, page size selector

Where you go next:
- **Click row** → order detail page
- **Click "+ Добавить"** → new order form
- **Click "Накладные"** → invoice list
- **Tick checkboxes + "Групповая обработка"** → bulk-update modal (assign expeditor, change status, etc.)

### 2.2 New order form

URL: `/orders/addOrder`

![New order full form](/screens/guide/33-new-order-empty.png)

What's on it:
- Header block: **Client** picker, **Agent** dropdown, **Date** field, **Warehouse** dropdown, **Price type** dropdown, **Payment method** dropdown
- Product table: barcode/name search → quantity → price → discount → line total
- Add-row button beneath the product table
- Totals row at bottom: subtotal, VAT, discount, grand total
- Comment / notes field
- **Сохранить** (Save) and **Отмена** (Cancel) buttons

Where you go next:
- **Click the client field** → client picker opens
  - ![Client picker](/screens/guide/40-client-picker.png)
  - Searchable list, 10 rows per page
  - Search by name, phone, or INN
  - ![Client picker filtered](/screens/guide/41-client-picker-search.png)
- **Save** → returns to the orders list with the new order on top

### 2.3 Order rejects / returns

URL: `/orders/rejects`

![Order rejects](/screens/guide/25-orders-rejects.png)

What's on it:
- List of orders the expeditor or client refused
- Reason column (out of stock, wrong product, price disagreement, client absent, etc.)
- Action: **Восстановить** (Restore) to push back into picking queue

### 2.4 Order recovery

URL: `/orders/recovery`

![Order recovery](/screens/guide/26-orders-recovery.png)

What's on it:
- Orders that were cancelled or auto-archived and can still be revived
- Date of cancellation column
- Tick rows + **Восстановить** to bring them back

### 2.5 Live trips

URL: `/orders/view/trips`

![Live trips](/screens/guide/20-trips-view.png)

What's on it:
- One row per active expeditor trip
- Truck / driver / route name
- Stops planned vs stops completed
- Current location (last GPS ping)
- Estimated finish time

Where you go next:
- **Click a trip** → trip detail with stop-by-stop status

---

## 3. Clients

### 3.1 Clients list

URL: `/clients/client`

![Clients list](/screens/guide/05-clients-list.png)

What's on it:
- Top action row: **Добавить клиента**, **Импорт** (Excel import), **Экспорт**, **На карте** (On map)
- **Фильтры** link expands the filter panel:
  - ![Clients filter panel](/screens/guide/45-clients-filter-panel.png)
  - Region / channel / segment / agent / active flag / debt flag
- Table columns: name, type, region, address, phone, agent, last visit, balance
- Pagination at the bottom

Where you go next:
- **Click "+ Добавить клиента"** → new-client form (or have agents create in the mobile app while on visit)
- **Click "Импорт"** → Excel import page
  - ![Clients import](/screens/guide/32-clients-import.png)
  - Download template → fill in → upload → preview → confirm
- **Click row** → client profile (history, debt, photos, visits)

### 3.2 Client payments / debt

URL: `/clients/finans`

![Client payments](/screens/guide/13-client-payments.png)

What's on it:
- Client / agent / period filter strip
- Columns: client, total debt, overdue, last payment date, last payment amount, days since
- Sort by aged debt, by region, by agent
- Bulk SMS reminder button

Where you go next:
- **Click client** → client payment history
- **Bulk select + SMS** → SMS broadcast page pre-loaded with selected recipients

### 3.3 Clients on map

URL: `/clients/view/clientMap`

![Clients on map](/screens/guide/48-clients-on-map.png)

What's on it:
- Full-screen map (OpenStreetMap / Yandex)
- Each pin = one client
- Pin colour by status (active / inactive / debtor / no visit this month)
- Side filter panel: agent, region, segment
- Click pin → mini-card with client name, phone, agent

### 3.4 Agent route planning

URL: `/clients/agentRoute`

![Agent route](/screens/guide/49-agent-route.png)

What's on it:
- Agent dropdown at the top
- Map showing the agent's assigned clients
- Drag-to-reorder list of stops on the left
- Day-of-week tabs (Пн / Вт / Ср / Чт / Пт / Сб)
- Save plan button

### 3.5 Visit change history

URL: `/report/visitingHistory`

![Visit history](/screens/guide/50-visit-history.png)

What's on it:
- Audit log of every visit modification
- Who / when / what changed
- Useful for disputes ("the agent says they visited but the system says no")

---

## 4. Team (Команда)

### 4.1 Auditors

URL: `/team/auditor`

![Team auditors](/screens/guide/06-team-auditor.png)

What's on it:
- List of auditor accounts
- Columns: name, phone, region, last login, status
- Auditors run independent photo / shelf checks separately from sales agents

### 4.2 Agents

URL: `/staff/view/agent` (also reachable as `/agents/agent`)

![Agents list](/screens/guide/07-agents-list.png)

What's on it:
- Columns: name, phone, supervisor, region, # of clients, last login, status (active / blocked), last GPS ping
- Top action row: **Добавить агента**, **Excel**, **Фильтры**
- Bulk select + bulk-action button at the bottom

Where you go next:
- **Click "+ Добавить агента"** → add agent form
  - ![Add agent form](/screens/guide/29-add-agent-form.png)
  - Fields: full name, phone, password, supervisor, region, role, photo
- **Click a row** → agent profile
  - ![Agent detail](/screens/guide/47-agent-detail.png)
  - Tabs: overview, visits, sales, KPI, devices, change log

### 4.3 Supervisors

URL: `/team/supervisor`

![Supervisors list](/screens/guide/17-supervisors-list.png)

What's on it:
- Columns: name, phone, # of agents under them, region, last login

Where you go next:
- **Click "+ Добавить"** → `/team/supervisor/create`
  - ![Add supervisor form](/screens/guide/30-add-supervisor-form.png)

### 4.4 Expeditors

URL: `/staff/view/expeditor`

![Expeditors list](/screens/guide/19-expeditors-list.png)

What's on it:
- Columns: name, phone, truck/vehicle, warehouse, last trip, status
- Filter by warehouse / status

Where you go next:
- **Click "+ Добавить"** → `/staff/create/expeditor`
  - ![Add expeditor form](/screens/guide/31-add-expeditor-form.png)
  - Fields: full name, phone, password, vehicle, default warehouse

### 4.5 Users (generic)

URL: `/team/user`

![Users list](/screens/guide/18-users-list.png)

What's on it:
- All accounts regardless of role (admin / supervisor / agent / expeditor / cashier / auditor)
- Filter by role
- Useful when you need to find a person and don't know what role they have

---

## 5. Warehouse

### 5.1 Warehouses list

URL: `/warehouse/list`

![Warehouses list](/screens/guide/08-warehouses-list.png)

What's on it:
- One row per physical warehouse
- Columns: name, address, manager, default for shipments, total SKUs in stock
- Action: **Добавить склад** (Add warehouse)

### 5.2 Purchases (supplier receipts)

URL: `/warehouse/view/listPurchase`

![Purchases list](/screens/guide/09-purchases-list.png)

What's on it:
- Incoming-stock documents
- Columns: №, date, supplier, warehouse, line count, total amount, status
- Action: **Добавить приход** (Add receipt)

### 5.3 Stock balance report

URL: `/stock/report`

![Stock report](/screens/guide/10-stock-report.png)

What's on it:
- Per-warehouse, per-SKU snapshot of available stock
- Columns: SKU, name, on hand, reserved, available, cost, value
- Filter: warehouse, category, low-stock-only toggle

### 5.4 Inventory / equipment list

URL: `/inventory/list`

![Inventory list](/screens/guide/51-inventory-list.png)

What's on it:
- Branded equipment placed at clients (fridges, racks, freezers, signage)
- Columns: serial №, type, model, current client, install date, last audit
- Useful for trade-marketing teams

---

## 6. Planning

### 6.1 Monthly visit plan

URL: `/planning/monthly`

![Monthly planning](/screens/guide/11-planning-monthly.png)

What's on it:
- Calendar-grid view with agents on the left, days across the top
- Each cell shows planned visit count
- Drag-drop clients between days
- Toggle agent dropdown to switch staff

Where you go next:
- **Save** → mobile app picks up the new plan on next sync
- **Print** → printable PDF for the agent

---

## 7. Reports

### 7.1 Agent sales report

URL: `/report/agent`

![Agent report](/screens/guide/12-report-agent.png)

What's on it:
- Filter strip across the top:
  - ![Report filter strip](/screens/guide/46-report-filter-strip.png)
- Pivot table: agent × period
- Cells: order count, gross sales, returns, net sales, debt collected
- Totals row at the bottom

### 7.2 Customer sales report

URL: `/report/customer`

![Customer report](/screens/guide/23-report-customer.png)

What's on it:
- One row per client
- Columns: orders count, total spend, average ticket, last order date, balance
- Sort by spend to find your top customers
- Export to Excel for monthly review meetings

### 7.3 Visit coverage report

URL: `/report/visit`

![Visit coverage report](/screens/guide/37-report-visit.png)

What's on it:
- One row per agent
- Columns: planned visits, completed visits, % coverage, with-order %, photo %
- Drill down by clicking the agent's count

---

## 8. Audit (merchandising)

### 8.1 Photo report

URL: `/audit/photoReport`

![Photo report](/screens/guide/15-audit-photoreport.png)

What's on it:
- Grid of recent shelf photos taken by agents during visits
- Each tile: photo thumb, client name, agent, date/time, GPS pin icon
- Filter by agent, client, date range, category (shelf / facade / fridge)
- Click photo → full-size view with metadata sidebar

---

## 9. Markirovka (EDI / CIS)

### 9.1 Incoming invoices

URL: `/markirovka/view/incomingInvoices`

![Incoming EDI invoices](/screens/guide/24-markirovka-incoming.png)

What's on it:
- Inbox of EDI invoices received from suppliers (e.g. cigarette / pharma traceability)
- Columns: №, supplier, date, total, status (new / accepted / rejected)
- Bulk-accept button

### 9.2 Outgoing invoices

URL: `/markirovka/view/outgoingInvoices`

![Outgoing EDI invoices](/screens/guide/52-markirovka-outgoing.png)

What's on it:
- Sent EDI invoices to your customers
- Columns: №, client, date, total, status
- Resend / cancel actions

---

## 10. Online & SMS

### 10.1 Online orders inbox

URL: `/onlineOrder/order`

![Online orders](/screens/guide/16-online-orders.png)

What's on it:
- Orders captured outside the agent app — web shop, B2B portal, Telegram bot
- Columns: №, source, client, total, status (new / confirmed / in CRM)
- Action: **Принять** (Accept) → creates a regular order in the CRM

### 10.2 SMS broadcast log

URL: `/sms/view/list`

![SMS broadcast](/screens/guide/27-sms-broadcast.png)

What's on it:
- History of SMS campaigns sent from the CRM
- Columns: date, segment, recipient count, delivered, failed, template preview
- New broadcast button at the top

---

## 11. Payments & cashier

### 11.1 Payment approval queue

URL: `/payment/approval`

![Payment approval](/screens/guide/21-payment-approval.png)

What's on it:
- Payments collected by agents in the field, waiting for cashier confirmation
- Columns: date, agent, client, amount, method (cash / card / Click / Payme), receipt photo, status
- **Подтвердить** / **Отклонить** buttons per row
- Bulk-approve when you trust the agent's batch

---

## 12. Settings

### 12.1 Company profile

URL: `/settings/diler`

![Company profile settings](/screens/guide/14-settings-profile.png)

What's on it:
- Company name (Russian / Uzbek)
- INN, OKED, MFO, account numbers
- Logo upload
- Default contact phone / email
- Address
- Used as the header on invoices and receipts

### 12.2 Price types

URL: `/settings/priceType`

![Price types settings](/screens/guide/28-settings-price-type.png)

What's on it:
- List of price tiers (Опт / Розница / Спец / Акция / VIP)
- Each row: name, formula (markup % or fixed), is-default toggle
- Add / edit / delete actions

### 12.3 Payment methods / currency

URL: `/settings/currency`

![Payment methods](/screens/guide/53-settings-payment-type.png)

What's on it:
- Accepted payment methods (cash, bank transfer, card, Click, Payme, Apelsin)
- Per-method: name, default cashbox, active toggle
- Currency list with the base currency starred

---

## Common UI patterns

These widgets behave the same way everywhere in the CRM. Learn them once.

### Search box (top right of every list page)
- Substring match across the visible columns
- Live filtering as you type — no need to press Enter
- Press `Esc` to clear

### Filter strip (below page heading)
- Multi-select dropdowns
- Filters stack with each other — pick agent AND status AND date
- ![Status filter dropdown example](/screens/guide/44-status-filter-dropdown.png)

### Date range picker
- ![Date range picker](/screens/guide/42-date-range-picker.png)
- Two-month calendar opens when you click the date field
- Quick shortcuts: Сегодня / Вчера / Неделя / Месяц / Квартал
- Date type dropdown (Order date / Ship date / Delivery date)
  - ![Date type dropdown](/screens/guide/43-date-type-dropdown.png)

### "Сбросить фильтр" (Reset filter)
Always at the right end of the filter strip. One click to clear everything you've selected.

### Excel export
Every list page has an Excel button — exports exactly what you see (current filter, current sort, all rows across pages).

### Pagination + page size
Bottom-right of every table. Default page size is 25; raise to 100 if you scroll a lot. The size you pick is remembered per page.

### Bulk actions
Every list page has row checkboxes. Tick rows → action bar appears at the bottom with the operations available (assign, change status, send SMS, delete, etc.).

### Status pills
Coloured rounded labels. Same colour code across the whole CRM:
- Grey = draft / new
- Blue = in progress
- Green = done / paid / confirmed
- Amber = on hold / pending approval
- Red = cancelled / rejected / overdue

---

**Need a workflow walkthrough?** The pages above are reference views. For step-by-step "how to do X", use the section guides:
- [First login →](./getting-started/first-login)
- [Create your first order →](./daily-use/first-order)
- [Dashboard & KPI →](./reports/dashboard-kpi)
