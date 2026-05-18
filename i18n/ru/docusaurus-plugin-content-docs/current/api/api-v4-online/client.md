---
title: "api-v4-online · Client"
sidebar_position: 1
---

# api-v4-online · `ClientController`

Endpoints for `ClientController` (`protected/modules/api4/controllers/ClientController.php`). 10 action(s). The controller body is empty — every endpoint is wired through `actions()` to a class under `protected/modules/api4/actions/{client|agent|expeditor}/`. All actions extend `ApiAction` and require `authenticate()`; many also call `authorize()` with a role allowlist and only accept `GET`.

## `GET /api4/client/balance`

- **Controller**: `actions['balance']` → `ClientBalance` (`protected/modules/api4/actions/client/ClientBalance.php`).
- **Auth**: `authenticate()` (no `authorize` — open to any authenticated user). GET only — HTTP 405 otherwise.
- **Request**: No body. Standard `response_type` query (`json` returns associative rows; otherwise tabular `[columns, ...rows]`).
- **Response**: Rows `{client_id, balance, trade_id, payment_type_id, currency_symbol}` summing `ClientTransaction.SUMMA` where `TRANS_TYPE != 4`, grouped by client × store × currency.
- **Side-effects**: None.
- **Gotchas**: Three branches by role: agent (`User.ROLE_AGENT`) sees only clients in `Visiting`/`VisitingMonth` for their `AGENT_ID`; expeditor (`User.ROLE_EXPEDITOR`) sees only clients attached via `Client.EXPEDITOR` or `VisitExp`; everyone else gets all clients. Contragent mode (`ServerSettings::isContragent()`) flips the join to read transactions via `Client.CONTRAGENT` instead of `Client.CLIENT_ID`. `startFinans` from `Yii::app()->params` clips the date window when present.

## `GET /api4/client/initial-balance`

- **Controller**: `actions['initial-balance']` → `ClientInitialBalance` (`.../client/ClientInitialBalance.php`).
- **Auth**: `authenticate()`. GET only.
- **Request (params)**: `start_of_day` (`today` default, or `yesterday`) — picks the cutoff `:initial_date`.
- **Response**: Same shape as `/client/balance` but the SUM is restricted to `DATE < :initial_date OR TRANS_TYPE = 6` — i.e. opening balance only.
- **Side-effects**: None.
- **Gotchas**: `start_of_day='today'` actually uses `strtotime('tomorrow')` as the cutoff so that all of today's transactions are *included*; `start_of_day='yesterday'` uses `strtotime('today')` (i.e. midnight) — read the code carefully. Agent role is filtered by `Visiting`/`VisitingMonth` membership; other roles get all clients. Contragent mode toggles the join the same way as `/client/balance`.

## `GET /api4/client/image-list`

- **Controller**: `actions['image-list']` → `ClientImageList` (`.../client/ClientImageList.php`).
- **Auth**: `authenticate()`. GET only.
- **Request**: No params.
- **Response**: `{id, client_id, url, is_main}` for clients in `Visiting`/`VisitingMonth` for the calling user's `AGENT_ID`. `is_main` is bool. Tabular envelope when `response_type != 'json'`.
- **Side-effects**: None.
- **Gotchas**: Uses `:agent_id = user.AGENT_ID` for non-agent users too, so callers without an agent record get an empty list. No active flag filter on `ClientPhoto`.

## `GET /api4/client/tara-count`

- **Controller**: `actions['tara-count']` → `ClientTaraCount` (`.../client/ClientTaraCount.php`).
- **Auth**: `authenticate()` + implicit "must have an Agent" (404 if `Agent::findByPk(user.AGENT_ID)` returns null). GET only.
- **Request**: No params.
- **Response**: `{client_id, tara_id, tara_count}` summed from `TaraClient` where `STATUS=2` (active tara at client), restricted to the agent's visiting clients.
- **Side-effects**: None.
- **Gotchas**: `tara_count` and `tara_id` are cast to int. Status filter `2` is hard-coded — other tara states (issued, returned, etc.) are not surfaced.

## `GET /api4/client/sales-category-list`

- **Controller**: `actions['sales-category-list']` → `ClientSalesCategoryList` (`.../client/ClientSalesCategoryList.php`).
- **Auth**: `authenticate()`. GET only.
- **Request**: No params.
- **Response**: Flat `{client_id, category_id}` rows from `SalesCategory` — no filter applied (all rows for the tenant). Tabular when `response_type != 'json'`.
- **Side-effects**: None.
- **Gotchas**: No role-based scoping — agents see the same payload as admins. Can be a heavy response on tenants with many clients × categories.

## `GET /api4/client/config`

- **Controller**: `actions['config']` → `ClientConfig` (`.../client/ClientConfig.php`).
- **Auth**: `authenticate()`. GET only. 404 if calling user has no `Agent`.
- **Request**: No params.
- **Response**: Array of `{client_id, config: {...}}` where `config` is a per-client, mobile-app-shaped merge of `ClientPaket::mainConfig()` × `getCompanyConfig()` × the per-client `paket.SETTINGS` JSON overlay, processed through `getConfigForApp()` (resolves SELECT/TEXT/CHECKBOX/TIMEPICKER/SINGLE_SELECT/INTEGER value types).
- **Side-effects**: None — read only, but the action is expensive: batch-loads `ClientPaket` for all visiting clients, then computes `mainConfig`/`companyConfig` once and reuses (avoids N+1).
- **Gotchas**: When `ServerSettings::appConfig()` is false, returns `[]`. `order.maxDebtDay` is expanded to `order.maxDebDate` (only when client has a non-zero `DATE_EXP` and negative `BALANS`). Per-trade `maxDebtDay` becomes `maxDebDate` using the earliest unsettled trade-debt expiry. `payment.consignmentPeriod` defaults to `7` days. `order.maxSumma` is nulled if `<= minSumma`.

## `GET /api4/client/agent-visit-day-list`

- **Controller**: `actions['agent-visit-day-list']` → `AgentVisitDayList` (`.../agent/AgentVisitDayList.php`).
- **Auth**: `authenticate()` + `authorize([User::ROLE_AGENT])`. GET only. 404 if calling user has no `Agent`.
- **Request**: No params.
- **Response**: `{client_id, day, sort, week_type, week_position}` for the agent. Combines `Visiting` (weekday-based) and `VisitingMonth` (monthly day — sort/week_type/week_position forced to 0). Sorted by `client_id, day, sort`.
- **Side-effects**: None.
- **Gotchas**: Rows with `day < 1` are dropped post-fetch (defensive: legacy data may have 0 or negative `DAY`). All numeric fields cast to int.

## `GET /api4/client/agent-client-list`

- **Controller**: `actions['agent-client-list']` → `AgentClientList` (`.../agent/AgentClientList.php`).
- **Auth**: `authenticate()` + `authorize([User::ROLE_AGENT])`. GET only.
- **Request (params)**: `type` — `visit` (default — only clients with any visit scheduled) or `all` (all active clients). Standard `response_type`.
- **Response**: Wide row: `client_id, company_name, client_name, phone_number, client_category_id, client_type_id, address, landmark, city_id, region_id, contact_person, latitude, longitude, barcode, create_time, inn, client_code, comment, client_channel_id, sort, account, bank, mfo, oked, pinfl, contract_number, contract_date, balance, is_allow_consignment, is_allow_credit, price_type_ids, points, follow_visit_rules, is_today_visiting_day, date_expire`.
- **Side-effects**: None — reads from `Client` (+ `Contragent` when `ServerSettings::isContragent()`) and computes today's visiting status from week-type / week-position rules in PHP.
- **Gotchas**: `is_today_visiting_day` is computed from `Visiting.WEEK_TYPE` (every-week / odd / even / once-per-month) and `Visiting.WEEK_POSITION` (Nth weekday in month, including `WEEK_POSITION_LAST`) plus `VisitingMonth` exact matches. `points` comes from `RoyaltyTransaction` sum. `follow_visit_rules` is the agent's packet `visit_rules` filter (apply_mode: `all/include/exclude`) over `client_city/client_category/client_types/client_channels/client_classes`. `latitude/longitude == 0` are nulled. `client_name` falls back to `'no-name'`. `date_expire` comes from `Client.DATE_EXP` (or `Contragent.DATE_EXP` in contragent mode).

## `GET /api4/client/expeditor-client-list`

- **Controller**: `actions['expeditor-client-list']` → `ExpeditorClientList` (`.../expeditor/ExpeditorClientList.php`).
- **Auth**: `authenticate()` + `authorize([User::ROLE_EXPEDITOR])`. GET only.
- **Request (params)**: `type` — `all` (default for online API — attached clients plus today's order clients) or `order` (only today's order clients).
- **Response**: Client rows scoped to the expeditor: clients with `Client.EXPEDITOR = AGENT_ID`, or attached via `VisitExp`, or having an in-flight order today (`STATUS IN (2,3,4)`, `DATE_LOAD = today`).
- **Side-effects**: None.
- **Gotchas**: The `today` filter uses MySQL `DATE()` and the server's clock — no timezone parameter. Inline interpolation of `AGENT_ID` is safe here because it comes from the authenticated user record.

## `GET /api4/client/expeditor-client-agents`

- **Controller**: `actions['expeditor-client-agents']` → `ExpeditorClientAgents` (`.../expeditor/ExpeditorClientAgents.php`).
- **Auth**: `authenticate()` + `authorize([User::ROLE_EXPEDITOR])`. GET only.
- **Request (params)**: `client_id?`, `agent_id?` (filters).
- **Response**: Returns the set of agents associated with each of the expeditor's clients — used for picking who to credit on a delivery payment.
- **Side-effects**: None.
- **Gotchas**: Same expeditor-scoping logic as `/client/expeditor-client-list` (attached via `EXPEDITOR`, `VisitExp`, or today's open order). Empty client set → empty response (no error). `client_id` filter narrows to a single client; `agent_id` further narrows the returned agents.

## See also

- [api-v4-online overview](./)
- [Authentication](../authentication.md)
- [Error codes](../error-codes.md)
