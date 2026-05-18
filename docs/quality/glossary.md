---
sidebar_position: 0
title: QA glossary
audience: QA
---

# QA glossary — the words you'll meet

> **Why this exists.** Every QA workflow page leans on a handful of domain-specific words (filial, expeditor, retro-bonus, AKB, CIS code, …). They're not optional vocabulary — bug reports and test cases use them constantly.
>
> **How to use it.** Each entry below has a one-sentence plain-English definition plus a link to the **full concept page** (in `docs/concepts/`) for the long explanation, and a "see also" link to the QA workflow that uses it.

This page used to hold all definitions inline. The long-form explanations now live in the [Concepts](../concepts/filial) section — one page per concept — so they can be linked from anywhere. Use the index below as the fast lookup.

---

## Core concepts (deep-dive pages)

| Concept | One-line | Full page |
|---|---|---|
| **Filial** | A branch / sub-company under one dealer; the multi-tenant scope on most rows. | [Concept — Filial](../concepts/filial) |
| **Outlet** | The physical shop the agent visits (= `Client` row in `d0_client`). | [Concept — Outlet](../concepts/outlet) |
| **АКБ** | Count of outlets that *actually bought* this period. | [Concept — AKB](../concepts/akb) |
| **RFM** | Recency / Frequency / Monetary 1–5 segmentation. | [Concept — RFM](../concepts/rfm) |
| **Defect vs reject** | Per-line return on a delivered order vs whole-order refusal. Different tables. | [Concept — Defect vs reject](../concepts/defect-vs-reject) |
| **Period close** | The cut-off that freezes editing on older orders. | [Concept — Period close](../concepts/period-close) |
| **Price type** | Named price list chosen per order. | [Concept — Price type](../concepts/price-type) |
| **Bonus vs discount** | Free product vs price reduction — different ledger effects. | [Concept — Bonus vs discount](../concepts/bonus-vs-discount) |
| **KPI** | Plan-vs-actual targets per person per month, seven bonus tiers. | [Concept — KPI](../concepts/kpi) |
| **Visit** | One agent's call at one outlet, includes check-in and check-out. | [Concept — Visit](../concepts/visit) |

---

## 1. People and roles

Each role has a dedicated landing page in `docs/roles/`.

| Term | Plain meaning | Landing page |
|---|---|---|
| **Role number** | Every user account has a numeric role: **1** admin, **2** manager, **3** operator, **4** field agent, **5** operations, **6** cashier, **8** supervisor, **9** key-account, **10** expeditor, **11** merchandiser. | [Team overview](./team/index.md#glossary--terms-and-role-numbers-qa-will-see) |
| **Admin** | Top-level web-admin user; sees everything. Role 1. | [Role — Admin](../roles/admin) |
| **Manager** | The office-based approver / overseer. Role 2. | [Role — Manager](../roles/manager) |
| **Operator** | The office-based clerk who builds orders on the web. Role 3. | — |
| **Agent (field agent)** | A salesperson who visits clients and submits orders from a mobile phone. Role 4. | [Role — Agent](../roles/agent) |
| **Cashier** | Approves payments; reconciles cashboxes. Role 6. | [Role — Cashier](../roles/cashier) |
| **Supervisor** | Web-only manager of a team of agents. Role 8. | [Role — Supervisor](../roles/supervisor) |
| **Key-account manager** | Web-admin user scoped to large B2B clients. Role 9. | — |
| **Expeditor** | The driver who delivers orders and collects cash. Role 10. | [Role — Expeditor](../roles/expeditor) |
| **Merchandiser** | Mobile user with a lightweight feature set — usually just visits and audits. Role 11. | — |
| **Agent type** | Stored as `Agent.VAN_SELLING`. **0** regular · **1** van-selling · **2** seller · **3** system bot. | [Role — Agent (QA)](./team/role-agent.md) |
| **Van-selling agent** | Sells direct from a vehicle; the van is their personal warehouse. | [Role — Agent (QA)](./team/role-agent.md) |
| **Seller** | Works from a fixed location, not a route. | [Role — Agent (QA)](./team/role-agent.md) |

---

## 2. Organisation and scoping

| Term | Plain meaning | See also |
|---|---|---|
| **Dealer** | One customer of the SalesDoctor platform. One dealer = one isolated database. | [Multi-tenancy](../architecture/multi-tenancy) |
| **Filial** | A branch under a dealer. See concept page. | [Concept — Filial](../concepts/filial) |
| **Tenant** | Synonym for *dealer* in technical contexts. | — |
| **Trade direction** | A business segment / channel (HoReCa, Pharmacy, …). | [Discounts](./orders/discounts.md) |
| **City** | Geographic scoping field on the client and order. | — |
| **Subscription cap** | Licence limit on active agents per dealer. | [Create-edit agent](./team/create-edit-agent.md) |
| **License / licence** | The dealer's paid subscription file. | — |

---

## 3. The order lifecycle

| Term | Plain meaning | See also |
|---|---|---|
| **Status** | **New (1)**, **Shipped (2)**, **Delivered (3)**, **Returned (4)**, **Cancelled (5)**. | [Status transitions](./orders/status-transitions.md) |
| **Sub-status** | Finer-grained label on top of status. | [Status transitions](./orders/status-transitions.md) |
| **Order type** | **1** Sale, **2** Recovery / shelf-return, **3** Defect order. | [Orders overview](./orders/index.md) |
| **Close date** | See concept page. | [Concept — Period close](../concepts/period-close) |
| **Re-open** | Moving an order back to *New*. Cascading side-effects. | [Status transitions](./orders/status-transitions.md) |

---

## 4. Money, pricing, bonuses

| Term | Plain meaning | See also |
|---|---|---|
| **Price type** | See concept page. | [Concept — Price type](../concepts/price-type) |
| **Manual price override** | Operator types a per-unit price directly. | [Discounts](./orders/discounts.md) |
| **Per-line discount** | Discount on one specific line. | [Discounts](./orders/discounts.md) |
| **Header discount (auto-discount)** | Order-level discount from a rule. | [Discounts](./orders/discounts.md) |
| **Bonus order** | See concept page. | [Concept — Bonus vs discount](../concepts/bonus-vs-discount) |
| **Auto-bonus** | System picks free SKUs. | [Bonuses](./orders/bonuses.md) |
| **Retro-bonus** | Agent picks free SKUs on the phone. | [Bonuses](./orders/bonuses.md) |
| **Debt** | Running customer balance. | [Mobile payment](./orders/mobile-payment.md) |
| **Cashbox** | A named till / payment channel. | [Mobile payment](./orders/mobile-payment.md) |
| **TRANS_TYPE** | **1** invoice, **3** payment receipt. | [Mobile payment](./orders/mobile-payment.md) |
| **Debt path fork** | Van-seller debt with the *debt-per-order* setting on. | [Status transitions](./orders/status-transitions.md) |

---

## 5. Stock, warehouses, defects, visits

| Term | Plain meaning | See also |
|---|---|---|
| **Warehouse (store)** | A physical place stock is held. | — |
| **Defect store** | Where defective / returned goods are parked. | [Partial defect](./orders/partial-defect.md) |
| **Van warehouse** | A van-selling agent's personal warehouse. | [Role — Agent](./team/role-agent.md) |
| **Defect (entity)** | Per-line defect on a delivered order. See concept. | [Concept — Defect vs reject](../concepts/defect-vs-reject) |
| **Reject** | Whole-order rejection. See concept. | [Concept — Defect vs reject](../concepts/defect-vs-reject) |
| **Visit** | See concept page. | [Concept — Visit](../concepts/visit) |
| **Route (visiting)** | Outlets an agent visits on a given weekday. | [Role — Agent](./team/role-agent.md) |
| **DAY / WEEK_TYPE / WEEK_POSITION** | Weekday-of-occurrence fields on route entries. | — |
| **Geofence radius / Out of zone** | Acceptable GPS distance at check-in; failures are flagged. | [Role — Agent](./team/role-agent.md) |
| **OKB** | Total clients visited or assigned (vs АКБ). | [Concept — AKB](../concepts/akb) |

---

## 6. Mobile app, packets, sync

| Term | Plain meaning | See also |
|---|---|---|
| **sd-agents app / Driver app** | The mobile apps for agent and expeditor. | [Role — Agent](./team/role-agent.md), [Role — Expeditor](./team/role-expeditor.md) |
| **agents-packet (AgentPaket)** | Config bundle pushed to the agent app. | [agents-packet](./team/agents-packet.md) |
| **expeditor-packet (ExpeditorPaket)** | Same idea for the driver app. | [expeditor-packet](./team/expeditor-packet.md) |
| **SETTINGS blob** | JSON column on a packet — every toggle. | [agents-packet](./team/agents-packet.md) |
| **Read-modify-write hazard** | Concurrent packet edits can clobber. | [agents-packet](./team/agents-packet.md#conflict-landmine--the-read-modify-write-hazard) |
| **Sync** | Mobile app re-fetching config and data. | [agents-packet](./team/agents-packet.md) |
| **PRODUCT_ID restriction** | Per-agent product list. | [Product distribution](./team/product-distribution.md) |
| **GUID / SyncLog** | Order-duplicate guards for api4 / api3. | [Create order — mobile](./orders/create-order-mobile.md) |

---

## 7. CIS / regulated goods (XTrace)

| Term | Plain meaning | See also |
|---|---|---|
| **CIS code** | A unique mark printed on regulated goods. | [CIS code check](./orders/cis-code-check.md) |
| **XTrace / Aslbelgisi** | State tracking system. | [CIS code check](./orders/cis-code-check.md) |
| **GTIN** | Product code printed alongside the CIS code. | [CIS code check](./orders/cis-code-check.md) |
| **CIS status** | Waiting · OK · Invalid · Quantity mismatch. | [CIS code check](./orders/cis-code-check.md) |

---

## 8. KPI

See [Concept — KPI](../concepts/kpi) for the data model. The detail-level rows below remain here for quick reference.

| Term | Plain meaning | See also |
|---|---|---|
| **KpiTaskTemplate** | Definition of one measurable metric. | [KPI setup](./team/kpi-setup-and-views.md) |
| **Kpi (a row)** | One person's KPI for one month. | [KPI setup](./team/kpi-setup-and-views.md) |
| **KpiTask** | Per-template target on a Kpi row. | [KPI setup](./team/kpi-setup-and-views.md) |
| **FIX_SALARY** | Fixed monthly salary base. | [KPI setup](./team/kpi-setup-and-views.md) |
| **MARK1..7** | Seven bonus-tier thresholds. | [KPI setup](./team/kpi-setup-and-views.md) |
| **All-zero deletion** | Clearing every target deletes the row. | [KPI setup](./team/kpi-setup-and-views.md) |
| **KPI v1 vs v2** | **v2 is current** (`KpiNewController`). | [KPI setup](./team/kpi-setup-and-views.md) |

---

## 9. Notifications, integrations, audit trail

| Term | Plain meaning | See also |
|---|---|---|
| **Telegram alert** | Order events sent to a dealer-configured channel. | [Create order — web](./orders/create-order-web.md) |
| **SDIntegration** | Deferred export call to external systems. | — |
| **Faktura.uz / Didox / 1C** | External invoicing integrations. | — |
| **Order history** | One row per field change on each order. | [Order list & history](./orders/order-list-and-history.md) |
| **AfterResponse** | Deferred-side-effects mechanism. | — |

---

## 10. UI labels — Russian to English

The web admin is in Russian by default. The same word in this guide:

| Russian label | English equivalent |
|---|---|
| Команда | Team module |
| Агенты | Agents |
| Супервайзеры | Supervisors |
| Экспедиторы | Expeditors |
| Торговая команда | Sales team |
| Распределение товаров | Product distribution |
| Задачи | Tasks |
| KPI установка | KPI setup |
| Заявки | Orders |
| Касса | Cashbox / Till |
| Финансы | Finance |
| Склад | Stock |
| Клиенты | Clients |
| Планы | Plans |
| Аудит | Audit |
| Настройки | Settings |
| Отчёты | Reports |

---

## How to keep this glossary useful

When you write a new test plan and the terminology trips you up:

1. **Look up the concept page first** (links above) — it has the data model and the failure modes.
2. **If it's not in the concepts list**, search this page. The detail rows below each section still hold a one-liner.
3. **If a definition is wrong or out of date**, edit it directly.

One concept → one page → linked from everywhere.
