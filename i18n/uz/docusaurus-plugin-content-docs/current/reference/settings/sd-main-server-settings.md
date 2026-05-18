---
sidebar_position: 2
title: sd-main · server settings
audience: Backend engineers, DevOps, support, integration partners
summary: Exhaustive catalog of every runtime knob in sd-main that lives outside reference tables — the `ServerSettings` reader API, dynamic `params.json`, static `params.php`, top-level `main.php` overrides, and the small set of hardcoded constants that behave like configuration.
topics: [sd-main, settings, server-settings, params, params-json, feature-flags, toggles, configuration, runtime, ServerSettings]
---

# sd-main · server settings

This is the engineering-grade catalog of every runtime knob in `sd-main` that is **not** a reference-data table row. If you came looking for "where do I change the visit distance / money rounding / debt-on-order-create behaviour", this is the page.

For per-tenant reference data (price types, channels, bonus rules) see [sd-main · tenant config](./sd-main-tenant-settings.md). For the operator-facing UI flow see [Settings module](/docs/modules/settings).

## 1. How sd-main config layers work

sd-main resolves a single flat `Yii::app()->params[...]` array at boot. That array is the merge of four layers, in order of increasing precedence:

```mermaid
flowchart LR
  A[main_static.php<br/>shared scaffold] --> M[array_replace_recursive]
  B[main.php<br/>tenant overrides] --> M
  C[params.php<br/>static defaults + secrets] --> P[CMap::mergeArray]
  D[params.json<br/>dynamic UI-editable] --> P
  P --> M
  M --> R[Yii::app()-&gt;params]
```

Layer 1 — **`protected/config/main_static.php`** — Yii scaffolding: modules, components (db, redis, session, authManager, urlManager, log), `onBeginRequest` language router. Same on every tenant. Edit only on a release.

Layer 2 — **`protected/config/main.php`** — per-tenant overrides for `name`, `timeZone`, db credentials, and the `params` sub-array. Includes things like `team`, `vsAvailableStatus`, `excelFormat`, the demo `simulate_host` block.

Layer 3 — **`protected/config/params.php`** — static PHP-array params: `phone_numbers` per timezone, `billing` and `param_user` HTTP-basic credentials, `kaspi_kz_ip_address`, `trusted_proxies`. Edited by engineers, not by ops.

Layer 4 — **`protected/config/params.json`** — dynamic, runtime-editable from `/settings/view/general`. This is the file the `Settings → General params` UI writes. Anything in this file wins over `main.php` for keys that overlap.

In addition there is **`upload/status_config.txt`** — a sibling JSON file (not under `protected/`) that holds order substatus definitions, read by `ServerSettings::substatuses()`. Likewise **`upload/isContragent.txt`** is a one-line boolean cache used by `ServerSettings::isContragent()` after the first probe of `INFORMATION_SCHEMA.TABLES`.

And finally — a handful of **class constants** (`Visit::MIN_GPS_DISTANCE`, API page-size limits, traceIQ timeouts, FilialComponent cache TTL) act as configuration but cannot be changed at runtime; you change them in code on a release.

There is also a tenant-overlay file, **`protected/config/main_local.php`** — gitignored, loaded last with `array_replace_recursive`. This is where a tenant deployment overrides the db credentials, `name`, `timeZone` and any other layer-2 key without touching the in-repo `main.php`. If a docker-compose installation feels like it is "ignoring" your edits to `main.php`, check whether `main_local.php` is shadowing them.

```mermaid
flowchart TD
  Code[PHP code] -->|reads| SS[ServerSettings::xMethod()]
  SS -->|isset?| YP[Yii::app()-&gt;params key]
  YP -->|merged from| PJ[params.json dynamic]
  YP -->|merged from| PP[params.php static]
  YP -->|merged from| MP[main.php params block]
  SS -.->|file_get_contents| FS[upload/status_config.txt<br/>upload/isContragent.txt]
  SS -.->|reflection| CACHE[static prop cache<br/>per-request]
```

Caching: most `ServerSettings::xxx()` methods memoize into a private static property for the lifetime of the request. The substatus cache is the only one that callers ever clear — `ParamStoreService::saveSubstatuses` uses `ReflectionClass` to null out `ServerSettings::$_substatuses` after rewriting `status_config.txt`.

## 2. `ServerSettings` reader catalog

Every public static method in `protected/models/ServerSettings.php`. Source of truth lives at that path; the method body is the spec. Methods are alphabetical.

Notation in the "Reads from" column:
- `params['key']` means `Yii::app()->params['key']`
- File paths are relative to webroot

| Method | Reads from | Default | Scope | What it controls | Key consumers |
|--------|-----------|---------|-------|-------------------|---------------|
| `allowDisablingStockCheck` | `params['allowDisablingStockCheck']` (boolean, strict `=== true`) | `false` | tenant | Whether order pages may bypass the "is there stock?" guard | Order create flow, vansell stock checks |
| `allowManualPriceForAgent` | `params['allowManualPriceForAgent']` (boolval) | `false` | tenant | Agent-role mobile app may enter manual price types | api3, api4 order creation |
| `allowManualPriceForVansell` | `params['appAllowPriceTypes']` (boolval) | `false` | tenant | Vansell-role mobile app may switch price types on the road | api4 vansell actions |
| `appConfig` | `params['appConfig']` | `true` | tenant | Master toggle exposed to mobile config endpoint; falsy disables app-side feature flags | `api3/AppConfigController` family |
| `countryCode` | derived from `params['formalCurrency']` | `'UZ'` | tenant | Maps formal currency to ISO country (`сум`→UZ, `тенге`→KZ, `сом`→KG) for legal forms, fakturas, ESF | EsfService, factura generators, SMS templates |
| `enableDeleteConsumptionOfClientTransaction` | `params['enableDeleteConsumptionOfClientTransaction']` (boolval) | `false` | tenant | Allow deleting a `consumption` payment row that is the back-side of a client transaction | clients/FinansController |
| `enableDeleteConsumptionOfShipperPayment` | `params['enableDeleteConsumptionOfShipperPayment']` (boolval) | `false` | tenant | Allow deleting a `consumption` payment row attached to a shipper-side payment | finans payment deletion |
| `enableInventoryDeletion` | `params['enableInventoryDeletion']` (=== true) | `false` | tenant | Inventory documents can be deleted (not only voided) | inventory module |
| `enableLotManagement` | `params['enableLotManagement']` (=== true) | `false` | tenant | Lot/series/expiry tracking on Order, Purchase, Exchange, StoreCorrector, defects, refunds — switches the column set and join logic in 12+ models | Order.php, Purchase.php, OrderDetail.php, OrderDefectDetail.php, Exchange.php, StoreCorrector.php (47 call sites) |
| `enableOnWebExpeditorDefectStore` | `params['enableOnWebExpeditorDefectStore']` (boolval) | `false` | tenant | Show "expeditor defect store" UI on the web (normally mobile-only) | web defect handling |
| `enableVisitOrdering` | `params['enableVisitOrdering']` (boolval) | `false` | tenant | Order entry forced inside a visit (vs. ad-hoc) | api4 CreateOrderAction |
| `enableWriteExpToTransaction` | `params['enableWriteExpToTransaction']` (=== true) | `false` | tenant | When a shipper/expeditor settles, write the expeditor-side amount into a separate ClientTransaction row | shipper finance flow |
| `forKamilka` | `params['forKamilka']` | `false` | tenant | Vendor-specific behaviour flag (legacy client "Kamilka") — gates a handful of report formatting branches | Telegram report, custom reports |
| `hasAccessToDeleteOrders` | `params['enableDeleteOrders']` (=== true) | `false` | tenant | Operator may delete orders (not only cancel) | orders module |
| `hasAccessToDeletePurchase` | `params['enableDeletePurchase']` (=== true) | reads param directly, falls back to falsy | tenant | Operator may delete purchase docs | purchase module |
| `hasNotAccessToEditPurchase` | `params['disableEditPurchase']` (=== true) | reads param directly | tenant | Inverse-named guard — when true, purchase edit forms are read-only | purchase module |
| `integration($type)` | `params['integration-' + type]` (=== true) | `false` | tenant | Generic per-integration toggle. Used as `integration('idokon')`, `integration('1c')`, etc. | order detail page, integration UI |
| `isBonusEvaluationEnabled` | `params['enableBonusEvaluation']` (=== true) | `false` | tenant | Run the bonus-evaluation engine on order save | bonus module |
| `isContragent` | `upload/isContragent.txt` file flag, with auto-detect fallback that probes `INFORMATION_SCHEMA.TABLES` for the `contragent` table and writes the file | auto-detected, `false` if neither file nor table | tenant | Counterparty-style accounting model — every client has a parent contragent that owns the balance. Switches the entire finance + transaction codepath. **464 call sites** — the single most consequential toggle in the codebase | ClientTransaction.php, Client.php, Order.php, ClientFinans.php, OnlineOrder.php, Cache.php |
| `isDemo` | `params['isDemo']` (=== true) | `false` | tenant | Demo-tenant guards (suppress real SMS, billing, integrations) | top of various controllers |
| `isMarkupPerProductEnabled` | `params['enableMarkupPerProduct']` (=== true) | `false` | tenant | Show "markup per product" report in menu and compute its data | report module, SideMenu2 |
| `liteVersion` | `params['liteVersion']` (=== true) | `false` | tenant | Hide advanced menu items / reports for low-tier tenants | SideMenu2 |
| `maxDaysBetweenDateAndDateLoad` | `params['limitDayChangeDateload']` (intval, must be greater than 0) | `21` | tenant | Max days an order's `date_load` may differ from `date`. Forms reject changes outside this window | order date pickers |
| `maxSecondsBetweenDateAndDateLoad` | derived: `maxDaysBetweenDateAndDateLoad() * 86400` | derived | tenant | Same guard expressed in seconds for API request validation | api3/api4 order create/update |
| `rateAndFirm` | `params['rateAndFirm']` (=== true) | `false` | tenant | Render "rate and firm" (exchange-rate + legal-entity) selectors on finans pages | clients/finans views (21 sites) |
| `receptionByOrder` | `params['receptionByOrder']` | `false` | tenant | Reception document is built by referencing an order rather than free-form | warehouse reception |
| `roundingDecimalsMoney($default = 2)` | `params['roundingDecimalsMoney']`, fallback `params['numberFormat']` | `2` | tenant | Decimal places used by `Formatter::asMoney()`, `Formatter::asMoneyDown()`, every money output | Formatter.php (88 sites across reports, orders, finance) |
| `roundingDecimalsQuantity` | `params['roundingDecimalsQuantity']`, fallback `params['numberFormat']` | `2` | tenant | Decimal places for quantities (`Formatter::asNumber`) | Formatter, order/purchase detail views (38 sites) |
| `roundingDecimalsVolume` | `params['roundingDecimalsVolume']`, fallback `params['numberFormat']` | `2` | tenant | Decimal places for volumes/weights | Formatter, report exports (22 sites) |
| `scheduledReporterBySvr` | `params['scheduledReporterBySvr']` | `false` | tenant | Telegram reporter runs at the supervisor level rather than per-agent. Changes who receives Telegram digests | TelegramReport.php (25 sites) |
| `setAutoDateLoad` | `params['setAutoDateLoad']` (numeric, or legacy boolean true → 0) | `null` (= "do not auto-set") | tenant | Number of days added to current date when initializing `date_load` for a new order. `0`=today, `1`=tomorrow, `null`=do nothing | order create forms, api4 create actions |
| `setEnableLotManagement($enabled)` | setter only — writes the static cache | — | request | Test/CLI helper to force the lot-management toggle for the current request without touching `params.json` | unit-test helpers, batch jobs |
| `setLimitDublicateClients` | `params['setLimitDublicateClients']` | `null` | tenant | Max allowed duplicate-client matches per import batch — null disables the limiter | client import |
| `stateSave` | `params['stateSave']` (=== true) | `false` | tenant | Persist DataGrid/sort/filter state to the user's session — used in the orders/clients grids (28 sites) | views/widgets across modules |
| `stockModel` | `params['stockModel']` (must be `'FEFO'` or `'FIFO'`) | `'FEFO'` | tenant | Stock issuance order — First-Expiry-First-Out vs. First-In-First-Out. Drives lot-pick logic | stock allocation, vansell loading |
| `substatuses` | `upload/status_config.txt` (JSON) | `[]` | tenant | Custom sub-status labels keyed by main status (1..5) and substatus id (`status * 10 + n`) | order list, order detail, mobile API substatus picker |
| `updatePaymentDeliver` | `params['updatePaymentDeliver']` (=== true) | `false` | tenant | When a shipper closes a route, regenerate (overwrite) deliver-side payment rows | clients/finans payment_deliver.php |
| `useLocalCode1C` | `params['useLocalCode1C']` (=== true) | `false` | tenant | When syncing with 1C, key entities by `local_code` rather than 1C's `code` | sync module |
| `visitDistance` | `params['visitDistance']` (intval, must be `>50` and `<=250`) | `50` | tenant | Radius (meters) within which a visit counts as "on-site" for the GPS pin tick. Note the implementation rejects values `<=50`, so the effective floor is 51 | dashboard supervayzer, GPS reports |

The Formatter is the highest-leverage consumer — flipping `roundingDecimalsMoney` from 0 to 2 changes every printed price in every report, every Excel export, and every mobile API payload tenant-wide.

### Top consumers, by call frequency

A grep across `protected/` for `ServerSettings::<method>` returns roughly this distribution. The shape of the list is itself useful — it tells you which toggles to test most carefully before flipping.

| Method | Call sites (approx) | Comment |
|--------|---------------------|---------|
| `isContragent` | 464 | The single most pervasive flag — touches client, order, online-order, transaction, finance, cache layers |
| `roundingDecimalsMoney` | 88 | Reports, exports, money-print formatters |
| `enableLotManagement` | 47 | Branches every detail model (Order, Purchase, Exchange, Defect, Refund, Replace, StoreCorrector) |
| `roundingDecimalsQuantity` | 38 | Quantity output |
| `countryCode` | 33 | Legal forms (faktura, ESF), SMS templates |
| `stateSave` | 28 | Grid state persistence across orders/clients/finans/reports |
| `scheduledReporterBySvr` | 25 | Telegram digest routing |
| `roundingDecimalsVolume` | 22 | Volume output |
| `rateAndFirm` | 21 | Finans pages — rate/firm picker |
| `setAutoDateLoad` | 7 | Order create flow |
| `maxDaysBetweenDateAndDateLoad` | 6 | Order date validation |
| `stockModel` | 5 | Stock-pick logic |
| `hasAccessToDeleteOrders` | 4 | Delete-button guards |
| `enableInventoryDeletion` | 4 | Inventory delete guards |
| `enableDeleteConsumptionOfClientTransaction` | 3 | Finans payment deletion |
| `updatePaymentDeliver` | 3 | Shipper closeout |
| Others | 1–2 each | Niche features (forKamilka, liteVersion, isDemo, etc.) |

## 3. `params.json` — dynamic, UI-editable params

Source of truth: `protected/modules/settings/components/ParamStoreService.php::DEFAULT_PARAMS`. The settings page reads this array to render a form; on save it writes the user's choices to `protected/config/params.json`.

| Key | Type | Default | What it controls | Who edits | Risk |
|-----|------|---------|------------------|-----------|------|
| `team` | integer (1..10) | `3` | Agents that can be attached to a visit | Settings admin | low |
| `roundingDecimalsMoney` | integer (0..6) | `2` | Decimal places in money outputs (Formatter) | Settings admin | **high** — touches every price-bearing output |
| `roundingDecimalsQuantity` | integer (0..6) | `2` | Decimal places in quantity outputs | Settings admin | medium |
| `roundingDecimalsVolume` | integer (0..6) | `2` | Decimal places in volume/weight outputs | Settings admin | medium |
| `startFinans` | datetime (`Y-m-d H:i:s`) | unset | Finance is calculated only from this date onward. Used as a hard floor for P&L, balances, debts | Backend engineer | **high** — moving this changes all historical totals |
| `formalCurrency` | string | `сум` | Symbolic currency name shown in forms and reports; also drives `ServerSettings::countryCode()` | Settings admin | medium — country code drives fakturas |
| `disableOrderListV1` | boolean | `true` | Hide the legacy order list v1 from the menu | Settings admin | low |
| `enableMarkupPerProduct` | boolean | `true` | Show "markup per product" report in menu | Settings admin | low |
| `dailyKPI` | boolean | `true` | Show daily KPI in menu | Settings admin | low |
| `enableDeleteOrders` | boolean | `true` | Operators may delete orders | Settings admin | medium — irreversible deletes |
| `enableDeletePurchase` | boolean | `true` | Operators may delete purchases | Settings admin | medium |
| `visitDistance` | integer (50..250) | `50` | Visit GPS-tick distance threshold (meters). The reader rejects `<= 50`, so effective floor is 51 | Settings admin | low |
| `vsAvailableStatus` | selection (`1..4`) | `'3'` | At what order status the vansell mobile stock becomes visible (`1`=new, `2`=to-ship, `3`=released, `4`=done) | Settings admin | medium — changes when agents see stock |
| `newAddOrder` | boolean | `true` | Force the new order-creation page; redirects the legacy add-order URL | Settings admin | medium |
| `selectableShipper` | boolean | `true` | Shipper picker shown on inter-filial movement docs | Settings admin | low |
| `integration-idokon` | boolean | `false` | Enable the idokon integration block on the order page | Backend engineer | low |
| `setAutoDateLoad` | integer (0..365) | `1` | Days to add to today when initializing a new order's `date_load`. Set 0 for "today" | Settings admin | low |
| `leavePrice` | boolean | `false` | When the user switches to manual price-type, keep the original product price (do not reset) | Settings admin | low |
| `debtNewOrder` | boolean | `false` | If `true`, create the client-debt transaction at order creation (status 1); if `false`, only at delivery (status 3) — and vansell/seller orders auto-jump to delivered. **Changes the entire AR/cash flow timing** | Backend engineer | **high** |
| `salesdoc` | array | unset | SD integration — second server (set-order). Sub-keys: `username`, `password`, `server`, `chat_id`, `prefix` | Integrations engineer | medium |
| `salesdoc_status` | array | unset | SD integration — main server (set-status). Sub-keys: `username`, `password`, `server`, `chat_id`, `multi_server` | Integrations engineer | medium |
| `excelFormatCount` | selection (0/1/2) | `2` | Excel cell format for count columns: 0=plain float, 1=space-separated, 2=currency-style | Settings admin | low |
| `excelFormatVolume` | selection (0/1/2) | `2` | Excel cell format for volume columns | Settings admin | low |
| `excelFormatSum` | selection (0/1/2) | `2` | Excel cell format for sum columns | Settings admin | low |
| `enableInventoryDeletion` | boolean | `true` | Inventory docs may be deleted | Settings admin | medium |
| `disableEditPurchase` | boolean | `true` | Purchase forms are read-only | Settings admin | medium |
| `allowDisablingStockCheck` | boolean | `true` | Stock check may be bypassed when ordering | Settings admin | medium |
| `enablePurchaseDraft` | boolean | `false` | Purchase has a "draft" pre-state before being finalized | Settings admin | low |

On save, `ParamStoreService::save()` does three things in this order:
1. Splits the flat `excelFormatCount` / `excelFormatVolume` / `excelFormatSum` form fields into a nested `excelFormat.count|volume|summa` block.
2. Calls `updateMainConfig()` — see [Gotchas](#7-gotchas).
3. `json_encode` and `file_put_contents` to `params.json`.

Validation runs per type — integer min/max, string regex, datetime format, boolean strict — and returns a per-key error array. The settings UI displays each error inline.

### Keys that exist in `Yii::app()->params` but are not in `DEFAULT_PARAMS`

Some params are read by `ServerSettings` but are not listed in `ParamStoreService::DEFAULT_PARAMS`, so they cannot be edited through the settings UI. They must be set by editing `main.php` (or `main_local.php`) on the server.

| Key | Where read | Notes |
|-----|------------|-------|
| `limitDayChangeDateload` | `ServerSettings::maxDaysBetweenDateAndDateLoad` | Days window for `date_load` validation |
| `enableBonusEvaluation` | `ServerSettings::isBonusEvaluationEnabled` | Runs the bonus engine on order save |
| `enableDeleteConsumptionOfShipperPayment` | `ServerSettings::enableDeleteConsumptionOfShipperPayment` | Allow deleting shipper-payment consumption rows |
| `enableDeleteConsumptionOfClientTransaction` | `ServerSettings::enableDeleteConsumptionOfClientTransaction` | Same for client transactions |
| `enableOnWebExpeditorDefectStore` | `ServerSettings::enableOnWebExpeditorDefectStore` | Show expeditor defect store on web |
| `enableVisitOrdering` | `ServerSettings::enableVisitOrdering` | Require a visit before order entry |
| `enableWriteExpToTransaction` | `ServerSettings::enableWriteExpToTransaction` | Split expeditor amount into a separate ClientTransaction |
| `appAllowPriceTypes` | `ServerSettings::allowManualPriceForVansell` | Vansell may switch price types |
| `allowManualPriceForAgent` | `ServerSettings::allowManualPriceForAgent` | Agent may enter manual prices |
| `scheduledReporterBySvr` | `ServerSettings::scheduledReporterBySvr` | Telegram digest routing to supervisor |
| `stockModel` | `ServerSettings::stockModel` | `'FEFO'` or `'FIFO'` |
| `numberFormat` | All `roundingDecimals*` readers | Universal fallback for the three explicit keys |
| `updatePaymentDeliver` | `ServerSettings::updatePaymentDeliver` | Regenerate deliver payment rows on shipper close |
| `useLocalCode1C` | `ServerSettings::useLocalCode1C` | 1C sync keys by local_code |
| `rateAndFirm` | `ServerSettings::rateAndFirm` | Show rate/firm pickers on finans |
| `liteVersion` | `ServerSettings::liteVersion` | Hide advanced menu items |
| `isDemo` | `ServerSettings::isDemo` | Demo-tenant suppression flag |
| `appConfig` | `ServerSettings::appConfig` | Master config for mobile clients |
| `forKamilka` | `ServerSettings::forKamilka` | Vendor-specific switch |
| `largosir` | direct `params['largosir']` reads in `ZagruzGroupOverhead2.php` | Vendor-specific export layout |
| `telFormat` | `params['telFormat']` in `SupplierInoutReportHandler.php` | Phone-number format used by the supplier report |
| `dolgPoAgentam` | `params['dolgPoAgentam']` in `TopMenu.php` | Show "Debt by agents" link in top menu |
| `pnlStartDate`, `pnlUseMinusCorrectionPrice` | `Finans.php` | P&L floor date and correction-price toggle |
| `simulate_host.enable` | `Telegram.php` | When in simulator mode, route Telegram messages to no-op |

## 4. Static `params.php` keys

These keys are merged in at boot and are intended to be edited by engineers, not the UI.

| Key | Default value | What it controls |
|-----|---------------|------------------|
| `phone_numbers` | per-timezone map (`Asia/Tashkent`, `Asia/Almaty`, `Asia/Yekaterinburg`, `Asia/Dushanbe`, `Asia/Bishkek`) | Support phone numbers shown in the help footer; each timezone block has `sales`, `support`, `billing`, `tg_support` |
| `billing` | `username: billing`, password hash | HTTP-basic credentials for the billing-side webhook endpoints |
| `param_user` | `login: params`, password hash | Credentials for the legacy params endpoint used by external sync tools |
| `kaspi_kz_ip_address` | `194.187.247.152` | Source IP allowlist entry for incoming Kaspi (KZ) callbacks |
| `trusted_proxies` | `[]` | List of IPs whose `X-Forwarded-For` is honoured |
| `kaspi_basic_auth` | `null` | When set, used as the basic-auth header for outbound Kaspi calls |
| `internal_sms_token` | `null` | Bearer token for the internal SMS gateway; null disables the channel |

Additional behaviour: `params.php` is itself a thin shim — it reads `params.json` first, then merges it under the static defaults with `CMap::mergeArray`. Dynamic keys win.

### `main.php` top-level params

`protected/config/main.php` defines another `params` block (the per-tenant override layer). Keys observed in the in-repo sample:

| Key | Sample value | Notes |
|-----|--------------|-------|
| `limitDayChangeDateload` | `9999` | Read by `ServerSettings::maxDaysBetweenDateAndDateLoad()` |
| `disableOrderListV1` | `true` | Same key the UI writes — main.php value loses if params.json sets it |
| `enableMarkupPerProduct` | `true` | Same |
| `integration` | `true` | Master integration toggle (the generic version, not `integration-<type>`) |
| `vsAvailableStatus` | `3` | Vansell stock visibility threshold |
| `V21CstoreRezerv` | `24` | Legacy reservation window (hours) for V2 1C integration |
| `enableProductBox` | `true` | Show product-box (multi-unit packaging) UI |
| `enableDeleteOrders` | `true` | Same key the UI writes |
| `enableNewCreateOrder2` | `true` | Use the v2 create-order page |
| `enableOrderList2` | `true` | Use the v2 order-list page |
| `enableImportOrders` | `true` | Show the order-import widget |
| `allowDisablingStockCheck` | `true` | Same as the UI key |
| `numberFormat` | `2` | Global fallback for all rounding decimal readers |
| `team` | `7` | Same as UI key |
| `warehouse.by.currency` | `['d0_2','d0_3']` | Tables in which currency rate is held when rate-by-warehouse is in use |
| `adminEmail` | `a.bozorov@gmail.com` | Recipient for system-error emails |
| `dbPrefix` | `d0_` | Required by several legacy components even though the connection already carries it |
| `dbName` | `test200` | Sometimes used in raw `INFORMATION_SCHEMA` probes (e.g. `ServerSettings::isContragent`) |
| `newAddOrder` | `true` | Same as UI key |
| `enableFakturaUZ` | `true` | Show UZ faktura legal-form UI |
| `excelFormat` | `{count: 1, volume: 0, summa: 2}` | The merged sub-array assembled by `ParamStoreService::save` |
| `simulate_host` | block | Demo/simulator stand-in for the billing API — `enable`, `host`, `id`, `status`, `left_days`, `active_to`, `free_to`, `balans`, `credit_limit`, `credit_date`, plus a `subcription` matrix per role |

`main.php` also ships a `components.db` block with a default `mysql:host=db;dbname=sd_main` connection string, `username`/`password`/`tablePrefix`. In production this is overridden by `main_local.php` (gitignored), which is loaded last with `array_replace_recursive`.

`main_static.php` enumerates the loaded modules (`rating`, `access`, `audit`, `finans`, `planning`, `doctor`, `dashboard`, `stock`, `settings`, `orders`, `clients`, `agents`, `partners`, `api`, `api2`, `api3`, `api4`, `sync`, `inventory`, `report`, `gps`, `store`, `gps2`, `gps3`, `adt`, `team`, `pay`, `vs`, `onlineOrder`, `staff`, `sms`, `warehouse`, `markirovka`, `integration`, `payment`), the Redis layout (`redis_session` on DB 0, `queueRedis` on DB 1, `redis_app` on DB 2), session timeout (`7200` seconds via `CCacheHttpSession`), auth-manager caching (`600` seconds), the allowed UI languages (`ru`, `en`, `uz`, `tr`), and the default cookie language (`ru`). These are not "settings" in the everyday sense — change them only on a code release.

## 5. Hardcoded constants used as toggles

Constants in the codebase that act as configuration (i.e., a numeric/boolean threshold you would want to change on purpose), not state values like `STATUS_NEW`.

| Constant | Value | File | What it controls |
|----------|-------|------|------------------|
| `Visit::MIN_GPS_DISTANCE` | `100` | `protected/models/Visit.php` | Meters within which a visit point is considered "on-site" by the dashboard and the API. Distinct from `ServerSettings::visitDistance()` — the latter is used for tick rendering, this one for points/scoring (api3/api4 reject/replace/defect/create actions all check `distance <= MIN_GPS_DISTANCE` to assign `gps = 10` vs `5`) |
| `FilialComponent::CACHE_TTL` | `3600` | `protected/components/FilialComponent.php` | Per-filial cache lifetime (seconds) |
| `SaleDetailNewController::CACHE_TTL_SECONDS` | `300` | `protected/modules/report/controllers/SaleDetailNewController.php` | Sale-detail report cache window |
| `MustBuyRuleService::DEFAULT_CONFLICT_MODE` | `'sum'` | `protected/components/MustBuyRuleService.php` | Conflict resolution mode when two must-buy rules overlap (`sum` adds, others replace) |
| `MustBuyRuleService::DEFAULT_PRIORITY` | `100` | same | Default priority for new must-buy rules |
| `TraceIqProductService::TIMEOUT_CONNECT` | `10` | `protected/modules/integration/actions/traceiq/TraceIqProductService.php` | TraceIQ HTTP connect timeout (seconds) |
| `TraceIqProductService::TIMEOUT_REQUEST` | `30` | same | TraceIQ HTTP request timeout (seconds) |
| `V2Controller::DEFAULT_RES_LIMIT` | `1000` | `protected/modules/api/controllers/V2Controller.php` | Max records returned per v2 API response |
| `V2Controller::DEFAULT_REQ_LIMIT` | `250` | same | Max records accepted per v2 API request |
| `SdController::DEFAULT_RES_LIMIT` | `1000` | `protected/modules/api/controllers/SdController.php` | Same for sd-prefixed legacy endpoints |
| `SdController::DEFAULT_REQ_LIMIT` | `100` | same | — |
| `V4Controller::DEFAULT_RES_LIMIT` | `1000` | `protected/modules/api/controllers/V4Controller.php` | Same for v4 |
| `V4Controller::DEFAULT_REQ_LIMIT` | `100` | same | — |
| `AdtAudit::ADT_REQUIRED` `/` `ADT_NO_REQUIRED` | `1` `/` `0` | `protected/models/AdtAudit.php` | Whether ADT audit answers are required vs optional — referenced as feature gate in audit save logic |
| `Integration::SERVICE_*` | string keys | `protected/models/Integration.php` | Identifiers for `smartupx`, `iiko`, `traceiq`, `ibox` — used as `integration-<service>` parameter suffixes |

Status-code constants (`Order::STATUS_*`, `OnlineOrder::STATUS_NEW`, `VsReturn::STATUS_NEW`, `VsExchange::STATUS_DELIVERED`, `FilialMovementRequest::STATUS_DRAFT`) are state values, not configuration, and are deliberately not listed here.

## 6. How to change a dynamic param

The expected flow for tenant ops is:

1. Sign in as a user with the `params` permission (typically the tenant administrator role).
2. Navigate to **Settings → General params** (URL pattern: `/settings/view/general`).
3. The form is rendered from `ParamStoreService::DEFAULT_PARAMS`. Each row shows `name`, `description`, current value, and constraints (min/max, enum options, format).
4. Edit values, submit. Server-side validation runs from `ParamStoreService::validate`. Errors are returned per-key and rendered inline.
5. On success, `params.json` is rewritten atomically with `json_encode` + `file_put_contents`. The next request picks up the new values because `params.php` re-reads `params.json` on every boot.

Operator-side documentation: see [Settings module](/docs/modules/settings).

For substatuses specifically, the same controller exposes `saveSubstatuses` which writes to `upload/status_config.txt` and clears the `ServerSettings::$_substatuses` static cache via reflection. Without that cache flush, long-running PHP-FPM workers would keep serving the old substatus map for the lifetime of their process.

To add a brand-new dynamic param (engineering task):
1. Add an entry to `ParamStoreService::DEFAULT_PARAMS`.
2. If a reader is needed, add a static method to `ServerSettings` that wraps `Yii::app()->params['<key>']` with a memoized static property.
3. Document it in this catalog and in the operator guide.
4. Deploy. The settings page will pick up the new key automatically.

## 7. Gotchas

**`array_merge_recursive` vs `array_replace_recursive`.** Saving any dynamic param triggers `ParamStoreService::updateMainConfig()` (and `checkMainConfigMergeRecursive()`), which uses `token_get_all` to rewrite every occurrence of `array_merge_recursive` in `protected/config/main.php` into `array_replace_recursive`. The reason: `array_merge_recursive` *appends* values for the same key (so toggling a boolean key would leave you with `[true, false]` rather than `false`), while `array_replace_recursive` overwrites — which is what the merge semantics actually need. **Side effect:** every dynamic-param save mutates `main.php` on disk. If `main.php` is checked into git or version-pinned, expect a dirty working tree after using the settings UI. The patched form is the correct one.

**Static-cache clear on substatus save.** `ParamStoreService::saveSubstatuses` ends with:

```php
$reflection = new ReflectionClass('ServerSettings');
$property = $reflection->getProperty('_substatuses');
$property->setAccessible(true);
$property->setValue(null, null);
```

This is the only place in the codebase that resets a `ServerSettings` static cache mid-request. All the other readers will hold their first-read value for the lifetime of the request (and, under PHP-FPM, that lifetime is one HTTP request — across requests the static is fresh again). If you add a new file-backed reader, add an equivalent cache-flush wherever the file is written.

**`isContragent` writes a file on first probe.** The first call to `ServerSettings::isContragent()` on a fresh tenant queries `INFORMATION_SCHEMA.TABLES` to check whether the `contragent` table exists, and then writes the boolean answer to `upload/isContragent.txt`. Subsequent calls read the file. To force a re-probe (e.g. after migrating in or out of the contragent model), delete that file. **Caveat:** the table-name probe interpolates the database name into raw SQL — safe only because the database name is server-controlled, not user input.

**Substatus store lives outside `protected/`.** `upload/status_config.txt` is in `webroot/upload/`, the same directory as user uploads, photos, exports. It is loaded by `ServerSettings::substatuses()` via `$_SERVER['DOCUMENT_ROOT'] . "/upload/status_config.txt"`. If you copy a tenant's database to another environment without copying the `upload/` directory, the substatus labels reset to empty and every order shows raw numeric substatuses. Backup scripts must include `upload/` alongside the SQL dump.

**`debtNewOrder` is a behaviour-changer, not a flag.** Flipping `debtNewOrder` does not just toggle a UI element — when set to `false`, vansell/seller orders are auto-promoted to delivered status (3) on creation so that the debt transaction is generated at the same moment. The same order would otherwise sit in status 1 with no debt until the deliver step runs. Switching this flag mid-period leaves you with a mixed-shape order set and significantly different debt balances on subsequent reports. Only change this at a period boundary.

**`visitDistance` ignores values `<=50`.** The reader is `if ($t > 50 && $t <= 250) ... self::$_visitStatusDistance = $t;`. Set it to 50 and the default (also 50) is kept. Set it to 30 and the default (50) is kept. The minimum effective value is 51. This is intentional — sub-50m radii produce too many false negatives at urban tower accuracy — but it is non-obvious from the settings UI.

**`stockModel` only accepts two strings.** Anything other than `'FEFO'` or `'FIFO'` reverts to `'FEFO'`. The settings UI does not currently surface this knob, so it is engineer-edited.

**`numberFormat` is the legacy fallback.** Every `roundingDecimals*` reader falls back to `numberFormat` before its own default. If a tenant has `numberFormat: 0` and no explicit rounding overrides, every money/quantity/volume field rounds to a whole number. This is rarely what you want — set the three explicit keys instead.

**Reading `params.json` is filesystem-bound.** `params.json` is read on every boot of `params.php`. It is small (a few KB) so this is not a real performance concern, but if the file is *missing*, the static defaults from `main.php` take over silently — you do not get a warning. After a deploy, verify the file exists and is non-empty.

**`largosir` and other vendor flags bypass the catalog.** A handful of historical client-specific switches are read directly from `Yii::app()->params[...]` without going through `ServerSettings`. They were added under deadline pressure and never folded into the abstraction. Grep `protected/` for `params['<key>']` before assuming a behaviour is config-driven via this catalog.

**`integration` is two different keys.** `params['integration']` (a bare bool, set in `main.php`) is the legacy master switch. `params['integration-<service>']` is the per-service modern switch read by `ServerSettings::integration($type)`. Both forms coexist in some codepaths; in new code prefer the typed form.

**Redis cache prefix conventions.** `tenantContext` produces scoped cache instances with prefixes `t:{db}:...` (tenant-wide, shared across filials) and `t:{db}:f:{id}:...` (per-filial). The `redis_session` component additionally prepends `HTTP_HOST:` to its keys for subdomain isolation. If you ever need to flush a tenant's cache manually, scan for `t:{db}:*` on the `redis_app` DB (database 2 on the redis instance). Do not flush database 0 unless you intend to log every user out.

**Auth cache TTL.** `DbAuthManager.cachingDuration = 600` (10 minutes). Permission changes do not take effect immediately for users with an open session — they must wait up to ten minutes, or the cache must be cleared. The most common operator confusion ("I gave them the permission and they still cannot see the page") traces back to this.

**Session timeout.** `CCacheHttpSession.timeout = 7200` (2 hours). Mobile API tokens have their own lifetime independent of this.

**Cookie language defaults to Russian.** `onBeginRequest` in `main_static.php` defaults `lang` to `ru` when neither `$_GET['lang']` nor `$_COOKIE['lang']` is present. Allowed values: `ru`, `en`, `uz`, `tr`. Anything else is coerced to `ru`. The cookie is `httponly`, `samesite=Lax`, 30-day lifetime, secure when HTTPS.

## 8. See also

- [Settings catalog index](./index.md) — picker for the other settings surfaces (tenant config, sd-billing, sd-cs)
- [sd-main · tenant config](./sd-main-tenant-settings.md) — reference-data tables (price types, channels, bonus/discount rules)
- [Settings module guide](/docs/modules/settings) — operator-facing UI walkthrough
- [Glossary](/docs/quality/glossary) — definitions of `contragent`, `vansell`, `FEFO`, `filial`, `substatus`
- Source files (all under `/Users/jamshid/projects/salesdoctor/sd-main/protected/`):
  - `models/ServerSettings.php`
  - `modules/settings/components/ParamStoreService.php`
  - `controllers/ServerSettingsController.php`
  - `config/main.php`, `config/main_static.php`, `config/main_local.php`, `config/params.php`, `config/params.json`
  - `models/Visit.php` (`MIN_GPS_DISTANCE`)
  - `components/Formatter.php` (primary consumer of rounding-decimals readers)
