---
title: "api-v3-mobile · Stock"
sidebar_position: 1
---

# api-v3-mobile · `StockController`

Per-action reference for `protected/modules/api3/controllers/StockController.php` (4 actions). Used by **agents** (ROLE=4) for client-shelf stock surveys and by **expeditors** (ROLE=10) for "what's left on the truck" lookups.

## Common contract

- **Base URL pattern**: `POST /api3/stock/<actionName>`.
- **Auth**: `deviceToken` from `HTTP_DEVICETOKEN` header. `User::userByDeviceToken($token)` (no role gate at lookup; role-specific behaviour inside).
- **Response envelope**: raw JSON (array or object).

---

## actionPost

`POST /api3/stock/post?apiVersion=…` — submit a stock-check (shelf inventory) for one client.

**Request** (JSON array): `[{ id, clientId, createdAt (ms), longitude, latitude, products:[{productId, totalItems}] }]`.

**Response** (array): `[{ id, status:1 }, …]` or `[{ id, status:0, errors:[…] }]`.

**Side effects**:
- Inserts one `ClientStock` row per product (`COUNT = totalItems`, hard-coded `DILER_ID='d0_1'`).
- When `Agent.config.visiting.stock` is enabled, upserts `Visit` for `(agent, client, date)`: `VISITED=1`, `STORE_CHECK=1`, fills `LAT`/`LON` from request when missing, widens `CHECK_IN_TIME`/`CHECK_OUT_TIME`.
- When `Agent.config.visiting.radius_visit` is set, validates `Visit` via `GpsService::isRequiredRadiusVisit` — if outside radius, `VISITED` is forced back to 0.

**Gotchas**: also dumps the response to `responce.txt` in document root. Date is derived from `createdAt/1000` (server local).

## actionGet

`POST /api3/stock/get` — last 10 historical stock-checks for one client (excluding today's by same user).

**Request** (JSON): `{ clientId }`.

**Response** (array): `[{ time (ms), date, total, details:[{productId, productName, categoryId, totalItems}] }]`.

**Gotchas**: hard-capped at 10 distinct time-points. Today's submission by the same user is filtered out (so the UI doesn't show what they just typed). Products missing from the `Product` directory get `productName="None"`.

## actionLeft

`POST /api3/stock/left` — "what's left" lookup.

**Request** (JSON): `{ storeId, products:[{productId}], isOnly?:bool }`.

**Response**: `{ storeId, products:[{ productId, count }] }`.

**Behaviour**:
- **Expeditor (ROLE=10)** with `Expeditor.DEFECT_STORE` set: computes today's net by joining `Exchange` (TYPE in (3,4)) and `Excretion` for the defect store; `count = SUM(Exchange.COUNT * OPERATION * -1) - SUM(ABS(Excretion.COUNT))`. `isOnly=true` further filters to the products listed in the body.
- **Other roles / no defect store**: reads `StoreDetail` directly for `(storeId, productId)` pairs.

**Gotchas**: when ROLE=10 and `DEFECT_STORE` is empty, falls through to the generic `StoreDetail` path. `storeId` in the response is `Expeditor.DEFECT_STORE` for expeditors, else the request's `storeId`.

## actionForecast

`POST /api3/stock/forecast` — naive sell-out forecast per client+trade for the agent.

**Request** (JSON array): `[{ clientId, tradeId }]`.

**Response** (array): `[{ tradeId, tradeName, clientId, agentId, today, date (last stock-check date), days (since last check), detail:[{ productId, count }] }]`.

**Gotchas**:
- Only runs for `User.ROLE == 4`. Other roles get `[]`.
- Formula per product: `count = floor(coefficient * SALE - leftover)` from `ClientStock` joined to `Product`/`TradeDirection`. Negative or zero forecasts are dropped.
- `coefficient` defaults to `1.5`; overridden by `Distr::getFile('leftover_coefficient')` (JSON file with `{coefficient: n}`).
- Window is the last 7 days of `ClientStock` ordered ascending (so the first row sets `lastDate`).

## See also

- [api-v3-mobile overview](./)
- [Authentication](../authentication.md)
- [Error codes](../error-codes.md)
