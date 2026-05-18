---
title: "api-v3-mobile · Client"
sidebar_position: 1
---

# api-v3-mobile · `ClientController`

Per-action reference for `protected/modules/api3/controllers/ClientController.php` (17 actions). Used primarily by the **agent (ROLE=4) mobile app** for client master, balances, debt and photo management.

## Common contract

- **Base URL pattern**: `POST /api3/client/<actionName>` (Yii camel-case mapping).
- **Auth**: `deviceToken` either as `HTTP_DEVICETOKEN` header or `$_REQUEST['deviceToken']`. Validated via `User::userByDeviceToken($token)` (NO role filter — any role with a matching token authenticates). A few endpoints further check `User.ROLE == 4` (agent) for write paths.
- **Response envelope**: raw JSON (object or array). Some endpoints return `{ status:'ok'|'error', message, ... }`; others return arrays directly. No global wrapper.

---

## actionPending

`GET/POST /api3/client/pending?deviceToken=…&limit=20&offset=0` — paginated list of clients pending registration (created via mobile, awaiting back-office activation).

**Response**: `{ status:'ok'|'error', data:[{name,firm_name,days}], meta:{limit,offset,count}, message? }`.

**Gotchas**: scope is `ClientPending.CREATE_BY = currentUser`. 401-equivalent `{ status:'error', message:'Invalid deviceToken' }` when token resolution fails.

## actionSendNotification

`POST /api3/client/sendNotification` — manual trigger for a Telegram notification.

**Request** (JSON): `{ data: { type:'pending_clients' } }`.

**Response**: `{ status, message }`.

**Side effects**: when `type=pending_clients`, calls `TelegramReport::notifyPendingClients()`.

## actionIndex

`GET/POST /api3/client/index?u=merch|...` — route entry for the client list.

**Behaviour**: dispatches to `ClientVersion4()` when `u=merch` (auditor flow), else `ClientVersion5()` (agent flow).

**Response (v4 — merch)** (array): `[{ client_id, dayOfWeeks:[{day,type,position}], tel, firm_name, name, clientCategory, adress, orient, region, city, contact_person, xml_id, form_sob, comment, client_channel, price_type:[id,...], sort, lat, lon, allowConsig, allowKredit, balans:[{summa,symbol}] }]` joined to `VisitingAud` for the auditor's plan.

**Response (v5 — agent)**: same general shape, joined to `Visiting` and `Agent` config. See source from line 2214 onward.

## actionToptrending

`GET /api3/client/toptrending?clientId=…&from=…&to=…&apiVersion=…` — top + trending products for one client (last 90 days by default).

**Response**: `{ status:'OK', top:[{quantity,name}], trending:[{quantity,name}] }`.

**Gotchas**: `from`/`to` are ms epoch; only orders with `STATUS in (2,3)`; `trending` covers only the most recent ~4 orders.

## actionSpravochnik

`GET /api3/client/spravochnik?deviceToken=…` — directory bundle for client-creation forms.

**Response**: `{ city:[{name,id,regionId,active,order}], clientCategory:[{name,id,active,order}], client_channel:[{name,id}], clientTypes:[{id,name,active,color}], tags:[{id,name,active}] }`.

## actionAddClient

`POST /api3/client/addClient?u=merch|...` — create or update client(s) from the field.

**Request**: large JSON array (`addClientVersion1` for non-merch, `addClientVersion2` for merch). Per client: `{ client_id (mobile UUID), name, firm_name, category, city, channel, typeId, contact_person, orient, address, form_sob, tel, lat, lon, bar_code, comment, visitDays, agentId, photo? (base64), … }`.

**Response** (array): `[{ id, customer_id, status, errors? }]` mapping mobile id → server client id.

**Side effects**: writes `Client` (or revives soft-deleted), `Visiting`/`VisitingAud`, `ClientPhoto`. Writes `SyncLog` for deduplication across retries. Clears `Cache::clearCache(['Client','VisitingAud'])`.

**Gotchas**: `u=merch` path also touches `Auditor` association via `VisitingAud`. Failed save → response has `status=0` and `errors=[…]`.

## actionInventory

`POST /api3/client/inventory?deviceToken=…` — equipment/inventory items at this agent's clients.

**Response** (array): `[{ id, name, model, serialNo, invNo, type:{id,name}, clientId, dateFrom, dateTo, active, comment, photo:[{id,url}] }]`.

**Gotchas**: filters by `InventoryHistory.CLIENT_ID IN (visiting clients of user.AGENT_ID)` AND `DATE_TO IS NULL OR > NOW()`.

## actionTransactions

`GET /api3/client/transactions?clientId=…&deviceToken=…` — client transaction ledger (last per default order).

**Response** (array): `[{ date (epoch), dateExpire?, type:int (TRANS_TYPE), typeText:'Заказ'|'Долг'|'Оплата'|'Возврат с полки'|'Обмен', summa, currency, comment, consignment, closed:bool, payed? }]`.

**Gotchas**: `ServerSettings::isContragent()` true → `clientId` is mapped to `Client.CONTRAGENT`. Filter is `TRANS_TYPE in (1,2,3,8,9)` AND `TYPE=1`.

## actionDebitor

`GET /api3/client/debitor?deviceToken=…&city=…&days=…&trade=…&to=…` — debtor list with filters.

**Response**: `{ result:[{clientId,name,firm_name,balans,dateExpire,detail?:[{payment,balans}]}], filter:{city:[{id,name}], days:[{key,name}]} }`.

**Gotchas**: `days` filter is `Visiting.DAY IN (…)`. `to` is ms epoch (cutoff date). Contragent mode aggregates by `CURRENCY`.

## actionRevise

`GET /api3/client/revise?client_id=…&from=…&to=…&trade_id=…&deviceToken=…` — reconciliation act for one client.

**Response**: `{ oborot:{debt,credit}, total:{balans, detail:[{payment,balans}]}, …per-row breakdown… }`.

**Gotchas**: when `params.customRevise` is set and `upload/Revises/<clientId>_revise.txt` exists, that pre-baked file is returned verbatim — bypasses the live computation. `from`/`to` are ms epoch. Contragent mode swaps `client_id` → `CONTRAGENT`.

## actionOrderDebt

`GET /api3/client/orderDebt?deviceToken=…&store=…&currency=…&city=…&to=…&trade=…` — per-client open order debt.

**Response**: `{ result:[{clientId,name,firm_name,order_balans,balans,undistrubuted}], filter:{city, currency, store} }`.

**Gotchas**: open debt = `SUM(SUMMA+COMPUTATION) < 0` from `ClientTransaction` (TRANS_TYPE=1, `SUMMA<0`). Filtered to `t.AGENT_ID = user.AGENT_ID`.

## actionOrders

`GET /api3/client/orders?client_id=…&from=…&to=…&limit=200&offset=0` — order list for one client.

**Request**: `deviceToken` via header `HTTP_DEVICETOKEN`; `client_id` (or `clientId`) required; date range up to 62 days.

**Response** (array): `[{ order_id, store_id, bonus, editable, client_id, client_name, date (ms), date_load (ms), manual_discount, payment_type_id, payment_title, price_type_id, type:'order'|'refund'|'replace', discount, summa, comment, agent, agent_name, trade_id, update_at, status, sale_products:[{ category_id, subcategory_id, volume, product_id, product_name, count, pack_quantity, price, discount, total_sum, type:'order'|'bonus'|'replace', bonus_condition? }], return_products:[{…,type:'defect'}], bonus_ids? }]`.

**Gotchas**: 401 if token invalid; 400 if `client_id` missing or range > 62 days. `limit` clamped to [1, 500].

## actionReviseDebt

`GET /api3/client/reviseDebt?client_id=…&from=…&to=…&deviceToken=…` — debt-only reconciliation slice.

**Response**: similar to `actionRevise` but filtered to debt rows; structure includes per-store + per-currency aggregates. Refer to source line 1771 for exact keys.

## actionAvatar

`POST /api3/client/avatar` (multipart/form-encoded) — upload a client storefront photo.

**Request** (POST form): `client_id`, `photo` (base64 or raw), `base64` (flag), `is_main`, `id` (mobile id).

**Response**: `{ id, url, client_id, mobile_id, status:'ok', file_size }` (empty `{}` on dedupe hit).

**Side effects**: writes `/upload/profilPhoto/<clientId>-<microtime>.jpg`; inserts `ClientPhoto`; clears MAIN on siblings when `is_main` or this is the first photo. Works for both `Client` and `ClientPending` (pending clients use ID lookup).

## actionDelete

`POST /api3/client/delete?deviceToken=…` — delete a `ClientPhoto`.

**Request**: `photo_id` (POST).

**Response**: `{ status:'ok' }`.

**Gotchas**: gated to `User.ROLE == 4` (agent). If deleted photo was MAIN=1, the most recent remaining photo is promoted.

## actionSetMain

`POST /api3/client/setMain?deviceToken=…` — promote a photo to MAIN.

**Request**: `photo_id` (POST).

**Response**: `{ status:'ok' }`.

**Gotchas**: gated to `User.ROLE == 4`. Sets `MAIN=0` on all sibling photos.

## actionDayTransactions

`GET /api3/client/dayTransactions?deviceToken=…` — today's transactions across the agent's clients.

**Response** (array): `[{ clientId, summa, tradeId, currency, type:int (1=order, 2=refund-ish, 3=uncomplete-payment, 4=replace), time, orderId, date, agentId }]`.

**Gotchas**: today is `date('Y-m-d 00:00:00')` — server timezone. Type mapping in source: TRANS_TYPE=3 → 2; TRANS_TYPE=2 → 4; positive SUMMA → 4. Also pulls uncomplete payments (`PaymentDeliver.TYPE=2 AND CONFIRM=0`) as type=3. Contragent-mode joins `Client.CONTRAGENT`.

## See also

- [api-v3-mobile overview](./)
- [Authentication](../authentication.md)
- [Error codes](../error-codes.md)
