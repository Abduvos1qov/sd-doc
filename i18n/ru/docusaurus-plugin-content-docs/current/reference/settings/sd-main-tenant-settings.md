---
sidebar_position: 3
title: sd-main · tenant config
audience: [admin, integrator, devops]
summary: Per-tenant reference-data catalog — every table in sd-main whose rows shape runtime pricing, bonuses, discounts, branches, KPIs and visit plans for one dealer (DILER).
topics: [settings, reference-data, pricing, bonuses, kpi, filial, multi-tenant]
---

# sd-main per-tenant configuration catalog

This page enumerates the lookup and rule tables that live **inside a tenant database** and steer day-to-day behaviour: pricing, promos, branch layout, KPI calculations, visit schedules. Each tenant (one `DILER`) owns its own copy of these tables — they are not shared across dealers.

For platform-wide toggles see [Global server toggles](./index.md) and the [Settings module overview](../../modules/settings.md).

## 1. How tenant config is organised

sd-main stores configuration in three buckets:

1. **Lookup tables** — flat dictionaries (`Currency`, `Cashbox`, `Channel`, `Region`). One row per option. Edited via classic CRUD screens under per-entity paths such as `/settings/currency`, `/settings/channel` and so on.
2. **Rule tables** — multi-row JSON-like rules that the order engine evaluates per cart (`Bonus`, `Skidka`, `KpiTaskTemplate`). Each row has a date range, product/client filter and a value.
3. **Hierarchy tables** — anything tied to `Filial` (branch) inherits the per-branch behaviour mixin (`BaseFilial` / `FilialBehavior`). A row carries a `FILIAL` column and a request only sees rows for the current branch.

All tables include `ACTIVE` (Y or N), `TIMESTAMP_X`, `CREATE_BY`, `UPDATE_BY`, `SYNC` and `TIME` columns so the sd-cs sync pipeline can ship deltas. Soft-delete is the norm — `ACTIVE=N` rather than physical row removal.

A typical request path: order create reads `PriceType` plus `Price`, applies `Skidka` and `Bonus`, snapshots the result into `OrderDetail` and the bonus tables (`BonusOrder`, `SkidkaOrder`). Once snapshotted the order does not re-read the rule rows — changes to rules do not retroactively rewrite past orders.

## 2. Price types and prices

Drives every product price shown to the agent and every line total written to an order.

| Model | Table | Purpose |
| --- | --- | --- |
| `PriceType` | `{{price_type}}` | Header row — one per price list (e.g. "Wholesale UZS", "Retail UZS", "Dealer USD"). |
| `Price` | `{{price}}` | Per-product price under a given `PRICE_TYPE_ID`. |
| `OldPriceType` | `{{old_price_type}}` | Historical snapshot used by edit-existing-order flow. |
| `OldPrice` | `{{old_price}}` | Historical product prices keyed by `OLD_PRICE_TYPE_ID`. |
| `PriceTypeFilial` | `{{price_type_filial}}` | Maps which price types are visible in which branch. |

**CRUD UI:** `/settings/priceType/admin` (list), `/settings/priceType/update` (header), `/settings/prices/index` (per-product bulk grid). Controllers: `PriceTypeController.php`, `PricesController.php`.

**RBAC:** `operation.settings.priceType`. Per-product price grid is gated by `operation.settings.price` (legacy) and `operation.settings.changePrice` for the bulk-edit batch endpoint.

**Cross-module reads:** order create in `orders/EditController`, `vs/CreateOrderController`, the `api3/CatalogController`, the price markup engine `ProductPriceMarkup`, the `PriceService` component and `Catalog::getPriceList()`.

**Gotchas:**
- `TYPE=1` is purchase (закуп), `TYPE=2` is sale. Only sale price types are exposed to sales agents.
- `HAND_EDIT='Y'` means the price type is **manual** — the per-product `Price` table is bypassed and the operator types prices directly on the order line. See `PriceType::isManual()` and `PriceType::getPrices()` (returns empty when manual).
- `FOR_CLIENT='Y'` restricts the price type to clients that are explicitly linked (used for VIP price lists).
- `OLD_PRICE_TYPE` is the foreign key into `OldPriceType` — when a price changes, the old value is snapshotted there so editing an old order still sees the price it was created with.
- `DEALER_PRICE=1` flags the price type as the dealer's procurement price (only one allowed). Guarded by `FilialComponent::isOnlyFilial()` — non-head-office branches cannot create dealer price types.
- `MIN_PRICE_TYPE_ID` enforces a floor: when a manager prices an order, the line cannot dip below the price stored under the referenced price type.
- `VALYUTA_ID` overrides `CURRENCY` for display — useful when one tenant runs both UZS and USD price lists on the same currency code.

## 3. Currencies

Defines payment instruments and FX symbols.

| Model | Table | Purpose |
| --- | --- | --- |
| `Currency` | `{{currency}}` | Payment-method-flavoured currency (cash UZS, bank UZS, cash USD, card UZS, e-wallet). |
| `FilialCurrency` | `{{filial_currency}}` | FX rate per branch per day for multi-branch tenants. |

**CRUD UI:** `/settings/currency/admin`. Controller: `CurrencyController.php`.

**RBAC:** `operation.settings.currency`.

**Cross-module reads:** every finance flow (`clients/FinansController`, `clients/ComputationController`), the cashbox screens, order create (to map a chosen payment method to a price type), the sd-billing reconciliation.

**Gotchas:**
- `TYPE=1` is cash (`Наличный`), `TYPE=2` is non-cash (`Безналичный`). Drives the "valid cashboxes" filter and the bank-statement integration target.
- A `Currency` row is more like a **payment method** than a true ISO currency — you typically have `UZS cash`, `UZS bank`, `USD cash` as three rows even though only two ISO codes are involved.
- `CSS_CLASS` and `TITLE` show up directly in the agent UI on payment buttons.
- **Dealer-currency match constraint:** when a dealer is created the system pins their `CURRENCY_ID` to one of these rows. Every `PriceType` for that dealer must reference a `Currency` whose ISO `CODE` matches. Mixing UZS and USD price types under one dealer that is pinned to UZS will throw at order save.
- Edits are also gated by `FilialComponent::isOnlyFilial()` — only the head-office branch may add or rename currencies.

## 4. Cashboxes

Cash drawers and bank accounts that receive payments.

| Model | Table | Purpose |
| --- | --- | --- |
| `Cashbox` | `{{cashbox}}` | One row per till or account. |
| `CashboxDisplacement` | `{{cashbox_displacement}}` | Inter-cashbox transfers (paired entries). |

**CRUD UI:** built into the finance module (no dedicated `CashboxController` in settings — managed under `finans/cashboxDisplacement` and the `Cashbox` model is edited via embedded admin grids in `clients/FinansController`).

**RBAC:** finance role gates (role `6` is the kassir role). No standalone `operation.settings.cashbox` — visibility is filtered by the `KASSIR` column instead.

**Cross-module reads:** `clients/FinansController`, `clients/ShipperFinansController`, `clients/computation/*` views — they all call `Report::getSpravochnik('Cashbox', ['KASSIR' => ['IN' => [userId, '']]])` to filter the dropdown.

**Gotchas:**
- `KASSIR` carries a `USER_ID` (or comma-list). An empty string means "any kassir". A row whose `KASSIR=42` is invisible to every user except `USER_ID=42` — this is the cashbox-per-cashier UX.
- The `ACCESS_CASHBOX` user flag (set on the `User` row) is an override: a user with `ACCESS_CASHBOX=Y` sees every cashbox regardless of the `KASSIR` filter. Use it for finance managers who reconcile across cashiers.
- `CURRENCY` on a cashbox must match the currency of the transactions written to it. Period-close blocks mismatches.
- A cashbox is a `BaseFilial` model — each branch sees only its own rows.

## 5. Bonus rules (buy-X-get-Y promo engine)

The largest rule engine in sd-main. One `Bonus` row defines a promo; satellites describe scope and exclusions.

| Model | Table | Purpose |
| --- | --- | --- |
| `Bonus` | `{{bonus}}` | Promo header — type, trigger value, gift product list, date window. |
| `BonusRelation` | `{{bonus_relation}}` | "Buy X also counts toward bonus Y" cross-product references. |
| `BonusExclude` | `{{bonus_exclude}}` | Per-bonus client or product exclusion list. |
| `BonusLimit` | `{{bonus_limit}}` | Quota: max gift per client / per date / per agent. |
| `BonusFilial` | `{{bonus_filial}}` | Branch scoping for multi-branch tenants. |
| `BonusAgent` | `{{bonus_agent}}` | Restrict promo to a list of agents. |
| `BonusCity` | `{{bonus_city}}` | Restrict promo to a list of cities. |
| `BonusOrder`, `BonusOrderDetail`, `BonusOrderHistory` | snapshots | Materialised per-order results — written once when the cart is saved. |

**CRUD UI:** `/settings/bonus/admin`. Controller: `BonusController.php`.

**RBAC:** `operation.settings.bonus`.

**Cross-module reads:** order create (`orders/EditController::checkBonus`, `vs/CreateOrderController`), the mobile API `api3` and `api4` order endpoints, the bonus report under `report/Bonus*Controller`.

**`BONUS_TYPE` reference (literal values in `Bonus::$bonusTypes`):**

1. quantity-based — sum quantity of trigger products
2. order-sum-based — sum sale value
3. volume-based — sum litres / kg
4. MML products (min per SKU)
5. MML products (max per SKU)
6. MML products (total)
7. MML category (min per SKU)
8. MML category (max per SKU)
9. MML category (total)
10. block bonus (whole block) — buy full case
11. block bonus (total) — sum across cases

**Gotchas:**
- `BONUS_PRODUCTS` is a comma-list of gift-product IDs — when several are listed the agent chooses one at checkout (or the engine auto-picks the cheapest, controlled by `MANUAL`).
- `IS_PUBLIC='Y'` means every client sees the promo; `IS_PUBLIC='N'` restricts to the clients listed in `BonusExclude` with the include flag flipped (semantic is "the exclude table acts as include-list when `IS_PUBLIC=N`" — a historical oddity).
- `ONLY_ONE_TIME=1` caps the promo to one trigger per order even if quantities allow several.
- `MAX_BONUS` caps the gift count per single order.
- `DATE_FROM` / `DATE_TO` are inclusive; orders with a `DATE` outside the window do not trigger.
- `MANUAL=Y` skips automatic gift selection — the engine surfaces the gift list and the agent picks manually. Used for "buy two beers get a free glass — choose colour".
- `BogO` flag exists for the legacy buy-one-get-one shortcut.
- `PARENT` chains bonuses (gift of one bonus becomes trigger of another).

## 6. Discount rules (Skidka)

Sister engine to bonus — same shape, but the outcome is a price reduction instead of a gift.

| Model | Table | Purpose |
| --- | --- | --- |
| `Skidka` | `{{skidka}}` | Discount header. |
| `SkidkaRelation` | `{{skidka_relation}}` | Cross-product trigger map. |
| `SkidkaExclude` | `{{skidka_exclude}}` | Excluded products or clients. |
| `SkidkaBudget` | `{{skidka_budget}}` | Per-promo budget envelope. |
| `SkidkaFilial`, `SkidkaAgent`, `SkidkaStore` | scoping | Restrict to branches, agents or warehouses. |
| `SkidkaManual`, `SkidkaManualAgent`, `SkidkaManualFilial` | manager-grant | Discounts a supervisor grants to a specific client. |
| `SkidkaOrder` | snapshot | Materialised per-order discount lines. |

**CRUD UI:** `/settings/skidka/admin` (rule-based), `/settings/skidkaManual/admin` (manual grants). Controllers: `SkidkaController.php`, `SkidkaManualController.php`.

**RBAC:** `operation.settings.skidka` and `operation.settings.skidkaManual`.

**Cross-module reads:** order create flows, the discount audit report, the cashbox reconciler.

**`SKIDKA_TYPE` reference (literal values in `Skidka::$skidka`):**

1. quantity-based
2. order-sum-based
3. volume-based
4 / 14 / 6. MML product (min count / min sum / total count)
7 / 9. MML category (min / total)
10. kit discount

**Gotchas:**
- `SKIDKA` is either an absolute amount or a percentage depending on the row's `CALC_TYPE`.
- `BUDGET` is enforced cumulatively — once `SkidkaBudget.SPENT` exceeds `BUDGET` the discount stops triggering.
- `MIN_SKU` enforces a unique-SKU floor (the cart must contain at least N distinct products for a kit discount to trigger).
- `NUM_CATEGORIES` is the category-floor counterpart for category-based MML rules.
- `IS_PUBLIC` semantics mirror `Bonus` (see above).
- Manager-granted manual discounts on `SkidkaManual` bypass the rule table entirely — they are applied directly to a single client's next N orders and never auto-expire by date.

## 7. Trade types, channels and outlets

Lookups that classify clients and route products.

| Model | Table | Purpose |
| --- | --- | --- |
| `TradeDirection` | `{{trade_direction}}` | Catalog grouping for the product tree (e.g. food, beverage, household). Used to split price lists by line of business. |
| `ClientChannel` | `{{client_channel}}` | Channel-of-trade classification (HoReCa, traditional, modern, B2B). Drives MML and bonus filtering. |
| `ClientCategory` | `{{client_category}}` | Free-form category tag stack — used in pricing rules and segmentation reports. |
| `ClientClass` | `{{client_class}}` | Class (A / B / C). Used in the AKB segmentation report. |
| `ClientType` | `{{client_type}}` | Type (juridical, individual). |
| `OutletPlan`, `OutletFact` | `{{outlet_plan}}`, `{{outlet_fact}}` | Per-outlet target vs. actual sales for the period. |

**CRUD UI:** `/settings/tradeDirection`, `/settings/channel`, `/settings/clientCategory`, `/settings/clientClass`, `/settings/clientType`. Controllers: `TradeDirectionController.php`, `ChannelController.php`, `ClientCategoryController.php`, `ClientClassController.php`, `ClientTypeController.php`.

**RBAC:** `operation.settings.tradeDirection`, `operation.settings.channel`, `operation.settings.clientCategory`, `operation.settings.clientClass`, `operation.settings.clientType`.

**Cross-module reads:** every report that segments by channel/category, `Bonus` and `Skidka` rule matchers, the planning module's outlet target screens.

**Gotchas:**
- `TradeDirection` IDs are referenced from `Product.TRADE_ID` — moving products between trade directions silently changes which catalog page shows them on the mobile app.
- `ClientChannel` is also referenced by bonus/skidka rules as a CSV string in `CLIENT_CHANNEL`. Renaming the ID column is therefore destructive — always add a new row and re-link rather than mutating an ID.
- `ClientCategory` and `ClientClass` are independent — a single client carries both. Reports often join them.

## 8. Filial (branch) and geographic hierarchy

| Model | Table | Purpose |
| --- | --- | --- |
| `Filial` | `{{filial}}` | The branch row itself: `id`, `domain`, `is_main`, `prefix`, `xml_id`. |
| `FilialDetail` | `{{filial_detail}}` | Address, contact and tax-ID fields per branch. |
| `Region` | `{{region}}` | Region table — top-level geographic node. |
| `City` | `{{city}}` | City table; foreign-key into `Region`. |
| `StructureFilial` | `{{structure_filial}}` | Hierarchical tree wiring a branch into a parent branch (head office, satellite). |
| `ProductFilial`, `FilialProduct` | per-branch product enable/disable | One row per (branch, product) where the product is available. |
| `RoyaltyFilial` | `{{royalty_filial}}` | Inter-branch royalty share rate. |

**CRUD UI:** branch management is in the `staff` or `filial` admin module (not a settings sub-page); city and region under `/settings/city`, `/settings/region`. Controllers: `RegionController.php`, `CityController.php`.

**RBAC:** `operation.settings.region`, `operation.settings.city`. Editing `Filial` requires being on the head-office branch (`FilialComponent::isOnlyFilial()`).

**Cross-module reads:** **every** filial-aware model. `FilialBehavior` injects a `WHERE FILIAL=:current` clause into every read on tables that opt in. `FilialComponent::current()` resolves the active branch from the request domain (`sales.acme.uz` vs `tashkent.acme.uz`).

**Gotchas:**
- `is_main=1` marks the head office. Many edit operations are restricted to this branch (currencies, dealer price types, dealer creation).
- `domain` is the subdomain used to discriminate which branch a request belongs to. Misconfiguring DNS leaks rows across branches.
- `prefix` is used in `XML_ID` generation and the sd-cs replication keys — never edit a live branch's prefix.
- City and region are referenced by clients (`Client.REGION`, `Client.CITY`), bonuses (`BonusCity`), territories (`Territory`) and the route-planning module. Removing a region with linked clients silently breaks reports.

## 9. Order substatuses

Free-form sub-state tags that augment the seven canonical order statuses.

**Storage:** `upload/status_config.txt` (JSON file under the web root). Read at runtime via `ServerSettings::substatuses()` which caches it for the request:

```php
// protected/models/ServerSettings.php
public static function substatuses(): array {
    if (is_null(self::$_substatuses)) {
        $filepath = $_SERVER['DOCUMENT_ROOT'] . "/upload/status_config.txt";
        if (file_exists($filepath)) {
            self::$_substatuses = json_decode(file_get_contents($filepath), true);
        }
        if (is_null(self::$_substatuses)) self::$_substatuses = [];
    }
    return self::$_substatuses;
}
```

**CRUD UI:** `/settings/params/index` — the dynamic-params screen exposes a JSON editor backed by `GetSubstatusesAction` and `SaveDynamicParamAction`.

**RBAC:** `operation.settings.params`.

**Cross-module reads:** `orders/EditController`, `orders/OrdersController`, the `order-status.php` view layout, the sale-detail report.

**Gotchas:**
- It is a file, not a table — sd-cs sync skips it. Each tenant maintains its own copy and a fresh tenant ships with an empty array.
- Adding a substatus requires the parent status to exist already — the JSON shape is keyed by parent `STATUS` ID with an array of label strings (see the code block above and the literal `upload/status_config.txt` sample shipped with each tenant).
- The mobile app caches the list per session — a substatus rename takes effect only after the agent re-syncs.
- Substatus changes do not trigger status hooks (no royalty calc, no notification fan-out). They are purely a UI label.

## 10. Tax and VAT settings

sd-main does not maintain a dedicated tax-rate dictionary table. Instead VAT is stored **per product** and the client tax-ID is stored on the client.

| Column | Lives on | Meaning |
| --- | --- | --- |
| `Product.VAT_RATE` | `{{product}}` | Percentage VAT rate for this SKU. NULL means VAT-exempt. |
| `Product.EXCISE_RATE`, `Product.EXCISE_RATE_TYPE` | `{{product}}` | Excise duty rate and "percent vs. absolute" flag. |
| `Product.IKPU`, `Product.IKPU_PACK_CODE`, `Product.IKPU_UNIT_CODE` | `{{product}}` | Uzbek fiscal classifier (IKPU / MXIK). |
| `Product.ETTN_CODE`, `Product.GTIN` | `{{product}}` | E-waybill and global trade item number. |
| `Client.CODE_NDS` | `{{client}}` | The client's NDS (VAT) registration ID. |

**CRUD UI:** product card under `/settings/product/update` — fields surface in the "Fiscal" tab. Controller action: `settings/SaveProductAction`.

**RBAC:** `operation.settings.product`.

**Cross-module reads:** the OFD (fiscal-data operator) integration writes receipts using `Product.VAT_RATE`; the e-waybill exporter reads `ETTN_CODE` and `IKPU`; `api4/PaymeGoCheckAction` and `PaymeGoPayAction` echo VAT into the Payme payload.

**Gotchas:**
- `VAT_RATE` is a decimal column — an empty string written from the UI is rejected (see `application.log` errors). Always coerce to `null` or a numeric.
- A tenant that flips from VAT-registered to non-registered must zero out every product's `VAT_RATE`; the OFD integration will otherwise emit a tax line.
- `Client.CODE_NDS` is informational only — it does not drive whether an order is VAT-bearing.

## 11. MML — Must-Match List

The per-channel mandatory-product list. sd-main does not ship a dedicated `Mml*` model in 2026 — MML is encoded as a flag on the product plus a category attribute, then evaluated by bonus and skidka types 4-9.

| Column | Lives on | Meaning |
| --- | --- | --- |
| `Product.IS_MML` | `{{product}}` | Y/N flag — this SKU is part of the MML basket. |
| `Product.POWER_SKU` | `{{product}}` | High-priority SKU within the MML basket. |
| `Bonus.BONUS_TYPE in (4..9)` | rule | MML-evaluating bonus shapes. |
| `Skidka.SKIDKA_TYPE in (4, 6, 7, 9, 14)` | rule | MML-evaluating discount shapes. |

**CRUD UI:** product card flag (`/settings/product/update`); rule rows under `/settings/bonus/admin` and `/settings/skidka/admin`.

**RBAC:** same as Section 5 and Section 6.

**Cross-module reads:** the store-check audit module (`audit/StorecheckController` and `adt/StoreCheckController`) — it lists MML SKUs the agent must verify on shelf. The webapp catalogue (`onlineOrder/WebappBotController`) groups MML at the top.

**Gotchas:**
- An MML rule type 4 (min count) **blocks the bonus** when the basket holds fewer than `VALUE` MML units. Use with care — it is "all or nothing".
- MML category rules (7, 9) read the category from `Product.PRODUCT_CAT_ID` not the dedicated category tag. Re-categorising a product invalidates audit history.
- The mobile-app sync does not push the MML list as a separate dictionary; it reconstructs it on the fly by filtering `Product.IS_MML='Y'`.

## 12. KPI templates

Reusable formula templates for the bonus-pool calculation.

| Model | Table | Purpose |
| --- | --- | --- |
| `KpiTaskTemplate` | `{{kpi_task_template}}` | One formula row — metric, weight, target, payout curve. |
| `KpiTaskTemplateGroup` | `{{kpi_task_template_group}}` | Bundle of templates assigned to a role or agent pool. |
| `KpiTask` | `{{kpi_task}}` | Per-agent per-period instance of a template (created when a period opens). |
| `Kpi`, `KpiGroup`, `KpiGroupLink` | legacy KPI tables | Older flat KPI tables — being phased out in favour of the template engine. |
| `ExpeditorKpiSetup`, `ExpeditorKpiJob` | expeditor variant | Separate KPI configuration for delivery drivers (paid per drop). |

**CRUD UI:** `/settings/kpi*` admin pages. The template designer is a SPA living under `modules/settings/views/kpi*`.

**RBAC:** `operation.settings.kpi`.

**Cross-module reads:** the dashboard `kpi/*` controllers, the period-close batch job (period close instantiates a `KpiTask` from every active template), the payroll exporter.

**Gotchas:**
- Templates are versioned by `TIMESTAMP_X` — editing a template after the period opens does not retroactively change running `KpiTask` rows.
- The bonus pool formula is encoded as a JSON `formula` field on the template (parsed by the KPI evaluator). Mis-quoted JSON silently zeroes out an agent's payout.
- A template can target a "role + branch + city" intersection — leaving a column blank means "all values match", which is often unintended.
- The expeditor KPI is a separate stack (`ExpeditorKpiSetup`) because delivery drivers do not have per-period targets — they are paid per drop.

## 13. Visit plan

Weekly visit schedules — which agent visits which client on which weekday.

| Model | Table | Purpose |
| --- | --- | --- |
| `Plan` | `{{plan}}` | Header — name, month, year, completion target. |
| `PlanProduct` | `{{plan_product}}` | Product-mix target per plan (push these SKUs first). |
| `AgentPlan` | `{{agent_plan}}` | Per-agent weekly recurrence — which clients on which weekday. |
| `OutletPlan` | `{{outlet_plan}}` | Per-outlet monthly target volume (sales target). |
| `OutletFact` | `{{outlet_fact}}` | Actual sales — populated by the order processor at period close. |
| `DoPlanning` (obsolete) | — | Legacy planning model, kept only for read-only history. |

**CRUD UI:** `/planning/plan` and `/planning/outlet`. (Legacy `/settings/plan` is `.obsolete`.) Controllers: `planning/OutletController`, route-planning screens.

**RBAC:** `operation.planning.plan`, `operation.planning.outlet`.

**Cross-module reads:** the GPS module compares the agent's actual route against the plan; the daily-report engine flags missed visits; the manager dashboard shows fact-vs-plan deltas.

**Gotchas:**
- `Plan.PLAN` is a comma-list of client IDs scheduled for the period. Editing a live plan mid-month renumbers visit-sequence indices the mobile app caches.
- `AgentPlan` carries weekday flags as a bitfield string — bit 1 is Monday, bit 7 is Sunday. The mobile app expects exactly seven characters; shorter strings are treated as "no plan" and the client list disappears from the agent's screen.
- `OutletPlan` is set at the start of the month and frozen on period-close. Changing it mid-month corrupts the dashboard's fact-vs-plan ratio.

## 13a. Bonus vs Skidka — when to use which

Both engines look near-identical on disk. The rule of thumb sd-main operators use in practice:

- Pick **Bonus** when the trigger consumes inventory: "buy 10 bottles, get 1 free". The free unit goes onto the order as a zero-priced line and is decremented from stock.
- Pick **Skidka** when nothing is gifted, only money: "buy 10 bottles, get 5 percent off". The discount is applied to the existing line — no extra stock movement.
- Pick **Skidka type 10** (kit) over **Bonus type 10** (block) when the multi-product trigger does not gift a separate SKU.
- A manager who wants to override pricing for one client (e.g. a strategic deal) should use `SkidkaManual` — not edit `Skidka` — so the override does not leak into other clients.

The materialised tables `BonusOrder` and `SkidkaOrder` carry an audit trail of which rule fired and what the engine computed. They are the first place to look when an agent complains about a "missing gift" or "wrong discount".

## 14. Migration tips (Excel and fresh-tenant seed)

When you bulk-load these tables (Excel import, `Smartup` sync, or `Smartup5x` from a sister tenant) keep this order:

1. **Filial first.** Create the branch row and its `FilialDetail` before anything else. Bad branch wiring corrupts every subsequent insert because `FilialBehavior` filters reads by the active branch.
2. **Region then City then Territory.** Foreign-key chain. Cities reference regions; clients reference cities.
3. **Currency, then PriceType, then Price.** PriceType requires a currency; Price requires a price type and a product.
4. **TradeDirection then Product.** Products reference a trade direction.
5. **ClientCategory, ClientClass, ClientChannel, ClientType.** All four must exist before clients are imported (clients reference all four).
6. **Cashbox before Currency edits and before any finance import.** Cashbox creation is gated by currency.
7. **Bonus and Skidka last.** Both reference product, client, currency, channel and city — they must be imported after every lookup is in place.
8. **KPI templates and Visit plans last of all.** They reference agents (users) and clients which should already be loaded.

Recommended sanity checks after a bulk load:

- Run `Catalog::warmupAll()` to rebuild the cached product list — without this the mobile app sees stale price types.
- Re-run `FilialComponent::invalidateCache()` after any `Filial` insert so the domain-to-branch resolver picks up the new row.
- Open `/settings/priceType/admin` and confirm every active price type has at least one row in `Price` — empty price types silently fall back to manual mode in the mobile UI.
- Run a dry order from the admin panel and confirm `Bonus`, `Skidka` and `MML` shapes evaluate as expected. Materialised tables (`BonusOrder`, `SkidkaOrder`) reveal which rules fired.
- Sync a single agent device against the tenant and confirm `status_config.txt` substatuses load — a missing file silently disables the substatus dropdown rather than throwing.
- Open the period-close screen and confirm one `KpiTask` row per agent per active template was generated.

Finally — when **seeding a new tenant** prefer cloning a known-good template tenant via the `Smartup5x` cross-tenant copier rather than crafting these tables by hand. The copier preserves all foreign-key references and re-prefixes `XML_ID` columns automatically. Hand-built tenants typically miss the `BonusOrder` / `SkidkaOrder` materialised tables which the runtime expects to exist (empty is fine, missing is not).

## 15. Quick-reference table — controllers and access strings

| Group | Controller | Admin URL | Access string |
| --- | --- | --- | --- |
| Price types | `PriceTypeController` | `/settings/priceType/admin` | `operation.settings.priceType` |
| Prices (per product) | `PricesController` | `/settings/prices/index` | `operation.settings.price`, `operation.settings.changePrice` |
| Currencies | `CurrencyController` | `/settings/currency/admin` | `operation.settings.currency` |
| Cashboxes | (embedded in `clients/FinansController`) | `/clients/finans/*` | role-gated by `KASSIR`, `ACCESS_CASHBOX` flag |
| Bonuses | `BonusController` | `/settings/bonus/admin` | `operation.settings.bonus` |
| Discounts (rule) | `SkidkaController` | `/settings/skidka/admin` | `operation.settings.skidka` |
| Discounts (manual) | `SkidkaManualController` | `/settings/skidkaManual/admin` | `operation.settings.skidkaManual` |
| Trade direction | `TradeDirectionController` | `/settings/tradeDirection/admin` | `operation.settings.tradeDirection` |
| Client channel | `ChannelController` | `/settings/channel/admin` | `operation.settings.channel` |
| Client category | `ClientCategoryController` | `/settings/clientCategory/admin` | `operation.settings.clientCategory` |
| Client class | `ClientClassController` | `/settings/clientClass/admin` | `operation.settings.clientClass` |
| Client type | `ClientTypeController` | `/settings/clientType/admin` | `operation.settings.clientType` |
| Region | `RegionController` | `/settings/region/admin` | `operation.settings.region` |
| City | `CityController` | `/settings/city/admin` | `operation.settings.city` |
| Filial | filial admin (staff module) | `/staff/filial/*` | head-office branch only |
| Substatuses | `ParamsController` (params SPA) | `/settings/params/index` | `operation.settings.params` |
| Product (VAT, IKPU) | `ProductController` and `ViewController` | `/settings/product/update` | `operation.settings.product` |
| Bonus / Skidka (MML) | `BonusController`, `SkidkaController` | as above | as above |
| KPI templates | `kpi/*` controllers | `/settings/kpi/*` | `operation.settings.kpi` |
| Visit plan | `planning/OutletController` (and route planner) | `/planning/outlet/*` | `operation.planning.plan`, `operation.planning.outlet` |

## Related references

- [Settings module overview](../../modules/settings.md)
- [Global server toggles](./index.md)
- [Filial concept](../../concepts/filial.md)
- [Period close mechanics](../../concepts/period-close.md)
- [KPI period close mechanics](../../concepts/period-close.md)
