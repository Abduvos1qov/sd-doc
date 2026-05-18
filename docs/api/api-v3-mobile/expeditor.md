---
title: "api-v3-mobile · Expeditor"
sidebar_position: 1
---

# api-v3-mobile · `ExpeditorController`

Per-action reference for `protected/modules/api3/controllers/ExpeditorController.php` (33 actions). Used by the **expeditor (driver/courier) mobile app** for load → deliver → return → payment flows.

## Common contract

- **Base URL pattern**: `POST /api3/expeditor/<actionName>` (Yii camel-case mapping; `actionPostOrder` → `/api3/expeditor/postOrder`). Body is JSON via `php://input`; some legacy endpoints also read `$_REQUEST` / `$_POST`.
- **Auth**: HTTP header `deviceToken: <token>` (read from `$_SERVER['HTTP_DEVICETOKEN']`; some endpoints fall back to `$_REQUEST['deviceToken']`). The controller calls `User::userByDeviceToken($token, 10)` — token must match a row where `ROLE=10` (Ekspeditor). After lookup the controller starts a Yii session via `UserIdentity`.
- **No envelope** — responses are raw JSON (array or object), not wrapped with `success`/`httpStatus`. Errors are signalled by HTTP status (401/402/429) or by `status`/`ok` keys in the body.
- **License gate**: many actions check `user->PAY != 1` or `hasSystemActive(4)` and 401/402 if expired.

---

## actionLogin

`POST /api3/expeditor/login` — only public endpoint.

**Request**: `login`, `password`, `deviceToken` (can also come from `HTTP_DEVICETOKEN` header or `$_REQUEST`).

**Response**: `{ success, fio, user_id, role, support, tg_support }` or `{ success:false, error }`.

**Side effects**: appends `deviceToken` to `User.DEVICE_TOKEN` (rolling 4-token window).

**Gotchas**: only `ROLE=10`. Fails for `PAY=0`, expired license, bad credentials, or empty token.

## actionAkt

`POST /api3/expeditor/akt` — client reconciliation act (mutual settlement).

**Request**: `clientId`, optional `dateFrom`, `dateTo`, `tradeId`.

**Response**: `{ start:{debt,credit,dateFrom}, transactions:[{date,type,paymentId,tradeName,comment,debt|credit}], rev:{debt,credit}, total:{debt,credit} }`.

**Gotchas**: when `ServerSettings::isContragent()` is true, `clientId` is mapped to `Client.CONTRAGENT` before the reconciliation call.

## actionPostOrder

`POST /api3/expeditor/postOrder` — the central delivery sync. Posts the result of an expedited order (DONE / partial / REJECT).

**Request** (JSON array): each item `{ id, orderId, clientId, status:"DONE"|"REJECT", dateDelivered (ms), consignation, consignationDate, discountType:"manual"|"auto", postProductList:[{productId,soldCount,price,orderType?}], bonusProductList, isBonusCalculated, payment:[{amount,...}], note_id, comment, deviceInfo:{latitude,longitude,batteryLevel,carrierName,cellularLevel,networkType,networkStatus,gpsStatus,device} }`.

**Response** (array): per order `{ id, orderId, clientId, status, ok, message?, lastOperation? }`.

**Side effects** — heavy. Per order:
- Validates `Order.STATUS=2` and `EXPEDITOR=user.AGENT_ID`.
- Sets `Order.STATUS=3` (delivered) or `4` (rejected); updates `Order.SUMMA`, `DISCOUNT`, `COUNT`, `DEFECT`, `HAS_PAID`, `PAID_AMOUNT`, `CONSIGNMENT`, `CONSIG_DATE`, `DATE_DELIVERED`, `DATE_STATUS`.
- For TYPE=1 (order): adjusts `OrderDetail` per product (creates new rows for items not in original); recalculates manual/auto discounts via `Skidka::findSkidka`/`findManualSkidka`; recreates `BonusOrderDetail` when `isBonusCalculated`.
- For TYPE=2 (defect/return): adjusts `OrderDefectDetail`.
- For TYPE=3 (replace): pulls both `OrderReplaceDetail` + `OrderDefectDetail`.
- Calls `StoreDetail::exchange_expeditor` to move stock between order store and `Expeditor.DEFECT_STORE`.
- Writes `SyncLog` with `STATUS='expOrderWait' / 'expOrderSuccess'` for offline retry-dedupe (TTL ~120s).
- Sends Telegram order-change report.
- Calls `expeditorLaodConfirm` REST when `Yii::app()->params['expeditorLoadNeo']['api']` set.
- Records visit via private `setVisit()` (Visit + GpsAdt rows).

**Gotchas**: dedupe is **per-deviceToken + day + mobileOrderId** in `SyncLog`. Concurrent retries within 120s sleep+die. Status codes: `1`=ok, `0`=order not found, `2`=server-side modified, `3`=status changed. Client `d0_0` is the "on-board" pseudo-client (TYPE=4).

## actionCalculateBonus

`POST /api3/expeditor/calculateBonus` — recalculates which bonus rule + quantity to apply for a given delivered basket.

**Request**: `{ order_products:[{product_id,delivered_count,price}], bonus_products:[{bonus_id,max_count}] }`.

**Response** (array): `[{ bonusId, newBonusId, bonusQuantity, detail:[{bonus,productId}] }]`.

**Gotchas**: uses `BonusCalculator::getBonusExpeditor`. Handles BOGO (`bogo` flag) vs regular bonuses differently — BOGO returns per-product splits; regular splits the total quantity across `Bonus.PRODUCT` CSV (random distribution via `splitBonusByProducts`).

## actionPostPayment

`POST /api3/expeditor/postPayment` — record cash/non-cash payments collected on delivery.

**Request** (JSON array): `[{ id, uniqueId, clientId, summa, currency, tradeId, comment, orderId?, date (ms), ... }]`.

**Response** (array): `[{ id, clientId, status, ok, message? }]`.

**Side effects**: writes `PaymentDeliver`, calls cashbox flow (`Cashbox` from expeditor config), updates client balance.

**Gotchas**: dedupes by `(USER_ID, uniqueId)` to prevent duplicates from offline retries.

## actionClient

`POST /api3/expeditor/client` — clients with an order or visit today (legacy single-page).

**Response** (array): `[{ client_id, dayOfWeeks, tel, firmName, name, clientCategory, adress, orient, city, contactPerson, formSob, comment, sort, lat, lon, qrCode, allowConsig, allowKredit, balansTotal, dateExp, hasOrder, photo, balans:[{summa,paymentType}], visits:[{agentId,day}], agents:[], images:[], photo_avatar }]`.

## actionClientNew

`POST /api3/expeditor/clientNew` — newer client list (extra fields).

**Response**: same shape as `client` with extensions per source.

## actionClientOne

`POST /api3/expeditor/clientOne` — paginated client sync, supports incremental sync.

**Request**: `{ lastSyncTime (ms), page, limit }` (defaults page=1, limit=50).

**Response**: `{ page, limit, total, current, time, date, date2, items:[{ client_id, dayOfWeeks, tel, phones:[], firmName, name, clientCategory, adress, orient, city, class, contactPerson, formSob, comment, lat, lon, qrCode, allowConsig, allowKredit, balansTotal, dateExp, hasOrder, balans:[{summa,paymentType,tradeId}], initialBalance, visits, agents, images, photo_avatar }] }`.

**Gotchas**: `lastSyncTime` is interpreted as `lastSyncTime/1000 - 3600` (1-hour overlap window). When `ServerSettings::isContragent()` true, balance is aggregated per contragent and propagated to all linked clients. `config.options.trade` filters which `STORE_ID` (trade direction) balances are returned.

## actionClientConfig

`POST /api3/expeditor/clientConfig` — per-client config (consignment period).

**Response**: `{ columns:['client_id','consignment_period'], data:[[clientId,days],…] }`.

## actionClientIds

`POST /api3/expeditor/clientIds` — bare client ID list (used to detect deletions client-side).

**Response** (array): `[{ clientId }]`.

## actionSpravochnik

`POST /api3/expeditor/spravochnik` — directory bundle (only entities referenced by today's orders).

**Response**: `{ paymentType:[{id,name,title,active,getPayment}], priceType:[{id,paymentTypeId,name,active,products:[{productId,price}]}], clientCategory, city, class, product:[{id,name,categoryId,subCategoryId,volume,packQuantity,photo,active}], productCategory, agent:[{id,name,active,phone_number}], trade, productSubCategory }`.

**Gotchas**: `product` list is filtered to PIDs referenced in today's `Order` + `BonusOrderDetail` + `OrderDefectDetail` + `OrderReplaceDetail`. `trade` is filtered by `Expeditor.config.options.trade`.

## actionConfig

`GET/POST /api3/expeditor/config` — expeditor feature flags + GPS config + server time.

**Request**: optional `version=v2`, `deviceModel`, `appVersion` (last two recorded to `Expeditor` row).

**Response** (v2): full `Expeditor::getConfigForApp()` output plus `server:{time,date}`, `phoneNumber`, `features:['labelcode',...]`, `options.currencies` (auto-filled from active `Currency` if empty).

**Response** (legacy/v1): `{ paymentByOrder, payment, options, order, server, gps:{minBatteryLevel,alwaysOn,tracking,interval,minDistance,accuracy}, features }`.

**Side effects**: updates `Expeditor.DEVICE_MODEL`, `APP_VERSION`, `LAST_SYNC_TIME`.

**Gotchas**: 401/402 on license expiry depending on `version`. 401 if expeditor row missing.

## actionBonusList

`POST /api3/expeditor/bonusList` — bonus rules referenced by today's orders.

**Request**: optional `day` (date string).

**Response** (array): `[{ bonusId, name, products:string[]|null }]`.

## actionOrder

`POST /api3/expeditor/order` — today's loaded orders for this expeditor (active trip).

**Request**: optional `day`.

**Response** (array): each order `{ order_id, store_id, bonus, editable, clientId, date (ms), dateLoad (ms), manualDiscount, paymentTypeId, paymentTitle, priceTypeId, type:"order"|"refund"|"replace", discount, summa, consignment, consignmentDate, comment, note_id, agent, tradeId, updateAt, urgent, products:[…] (filled later) }`.

**Gotchas**: filtered to `Order.STATUS=2 AND EXPEDITOR=current` for the day; further restricted to the lowest `TRIP_NUMBER` via private `findActualTrip` so the app only loads one trip at a time. `editable=false` when `TYPE != 1`.

## actionOrderList

`POST /api3/expeditor/orderList` — broader order list (history + status snake_case keys, used by newer UI).

**Request**: `from`, `to` (date strings, default today).

**Response** (array): `[{ order_id, store_id, bonus, client_id, client_name, date, date_load, manual_discount, payment_type_id, payment_title, price_type_id, type, discount, summa, comment, agent, agent_name, trade_id, update_at, status, sale_products:[{ category_id, subcategory_id, volume, product_id, product_name, count, pack_quantity, price, discount, total_sum, type:"order"|"bonus"|"replace", bonus_condition? }], return_products:[{…,type:"defect"}], bonus_ids? }]`.

**Gotchas**: empty array when `user` not found by token (no error). No trip filter (unlike `actionOrder`).

## actionGps

`POST /api3/expeditor/gps` — batch background GPS pings.

**Request** (JSON array): `[{ id, timestamp, latitude, longitude, batteryLevel, carrierName, cellularLevel, networkType, networkStatus, gpsStatus, deviceName, checkCurrentLocation? }]`.

**Response** (array): `[{ id, status:bool }]`.

**Side effects**: writes `GpsAdt` (TYPE='track') per ping; persists `webroot/log/gpsExp/<USER_ID>.json` with the last ping.

**Gotchas**: rate-limited via `checkLatestQueryTime` — single-ping bodies sent within 10s of the previous one return `429`. Multi-ping bodies bypass throttle. `checkCurrentLocation=true` also bypasses.

## actionTransactions

`GET /api3/expeditor/transactions?clientId=…` — last 20 client transactions.

**Response**: array of transactions (see source — wrapper around `Report::getSpravochnikResult('ClientTransaction')` for `TYPE=1`, `TRANS_TYPE in (1,2,3)`).

## actionReasons

`POST /api3/expeditor/reasons` — RejectDefect reasons.

**Response** (array): `[{ id, name, active }]`. If empty table, returns a single fallback `[{id:0, name:'Магазин закрыт', active:'Y'}]`.

## actionPostClient

`POST /api3/expeditor/postClient` — update a client's coordinates from the field.

**Request** (JSON): `{ ClientId, lat, lon }`.

**Response**: `{ ClientId, status:true }`.

## actionHistory

`GET /api3/expeditor/history?clientId=…&from=…&to=…` — client order history.

**Response** (array): `[{ client_id, message, created_at (ms), price_type_id, paymentType:{currency_title,price_type_id,name}, syncTimestamp, draft, isCustomerRejected, syncErrors, type:'order', consignment, status, totalPrice, totalItems, products:[{productId,productName,categoryId,categoryName,totalItems,totalPrice}] }]`.

**Gotchas**: default range is the last 90 days. `from`/`to` are seconds-epoch when provided (note: in ms divided by 1000 inside).

## actionToptrending

`GET /api3/expeditor/toptrending?clientId=…&from=…&to=…` — top + trending products for a client.

**Response**: `{ status, top:[{quantity,name}], trending:[{quantity,name}] }`.

**Gotchas**: only orders with `STATUS in (2,3)`. `trending` is the last ~4 orders only.

## actionSetPhoto

`POST /api3/expeditor/setPhoto` — upload a client photo-report image.

**Request** (POST form): `customerId`, `categoryId`, `createdAt` (ms), `photo` (raw or base64), `base64` (flag).

**Response** (array): `[{ createAt, status:'ok'|'fail', url, prId, messages?:{uz,ru,en} }]`.

**Side effects**: writes `/upload/photo/<YYYYMM>/img-<customerId>-<createdAt>.jpg` (compresses >1.5MB); inserts `PhotoReport`; sends `TelegramReport::expeditorPhotoReport`.

## actionInventory

`POST /api3/expeditor/inventory` — inventory items at this expeditor's clients.

**Response** (array): `[{ id, name, model, serialNo, invNo, type:{id,name}, clientId, dateFrom, dateTo, active, comment, photo:[{id,url}] }]`.

## actionPendingOrders

`POST /api3/expeditor/pendingOrders` — orders loaded but not delivered within window.

**Request**: `{ fromDate, toDate, territories:[CITY_ID] }` (default: last 4 days, configurable via `params.expeditorPendingOrderDays`).

**Response**: `{ status:bool, orders:{ columns:['id','order_id','client','agent','summa','date','date_load','type','currency'], data:[[…]] } }`.

## actionOrderUpdateDateLoad

`POST /api3/expeditor/orderUpdateDateLoad` — bump `DATE_LOAD` to today 09:00 for given order ids.

**Request** (JSON array): `[orderId, orderId, …]`.

**Response**: `{ status:bool, error?:[{key,text}] }` (localized error messages).

## actionCalculateDiscount

`POST /api3/expeditor/calculateDiscount` — recalculate discount for a modified order on the fly.

**Request** (JSON): `{ orderId, date, priceTypeId, agent, clientId, postProductList:[{productId,soldCount,price}] }`.

**Response**: `{ discount:[{productId,totalDiscount,detail:[…]}] }` (or `{status:false,error:[{key,text}]}`).

**Side effects**: pure compute via `Skidka::findSkidkaMobile`.

## actionOnBoard

`POST /api3/expeditor/onBoard` — products currently on the truck (left over after deliveries).

**Response** (array): `[{ productId, name, price, volume, tradeId, categoryId, packQuantity, subCategoryId, count }]`.

**Gotchas**: aggregates `Order.STATUS in (3,4)` for the day. `STATUS=3` (delivered) counts `OrderDetail.DEFECT`; `STATUS=4` (rejected) counts `DEFECT+COUNT`. Returns 0 entries when nothing remains.

## actionReport

`POST /api3/expeditor/report` — end-of-day expedition report (deliveries, returns, defects, replaces, on-board, tare).

**Response**: `{ column:[<keys>], data:[{ column:[…], data:[[…]] }, …] }` — column-oriented per category. Categories include `loadProducts`, `returnProducts`, `deliveredProducts`, `unsyncedProducts`, `onBoardProducts`, `defectProducts`, `replaceProducts`, `additionalLoadProducts`, `leftProducts`, `returnTares`.

**Gotchas**: when `params.expeditorLoadNeo.api` is on, control is forwarded to private `expeditorLoad()` (different DTO). Aggregates current calendar day only.

## actionDebtsOnClient

`POST /api3/expeditor/debtsOnClient` — clients with overdue / open debt.

**Request** (JSON): `{ currency:[…], type:'all'|'mine', deliveredDate (ms), consignDate (ms), territories:[CITY_ID], debt:minAmount }`.

**Response**: `{ column:['clientId','clientName','clientPhoto','debt','unDistrubuted','balance'], data:[[…]] }`.

**Gotchas**: `type='all'` removes the expeditor filter; `type='mine'` restricts to current user.

## actionDebtsOnOrder

`POST /api3/expeditor/debtsOnOrder` — overdue orders for one client.

**Request**: `{ clientId, currency, type, deliveredDate, consignDate, territories, debt }`.

**Response**: `{ column:['orderId','summa','paid','debt','deleviredDate','consignDate','tradeId','unConfirmed'], data:[[…]] }`.

## actionClientTara

`POST /api3/expeditor/clientTara` — outstanding tare (returnable packaging) per client.

**Request** (JSON): optional `{ clientId }`.

**Response**: `{ column:['count','clientId','taraId','name'], data:[[…]], status, error }`.

**Gotchas**: filtered by `TaraDocumentDetail.OWNER_TYPE=2` (client owner).

## actionPayments

`GET /api3/expeditor/payments?from=…&to=…&types=0,1,2` — payment-deliver history.

**Request**: `from`, `to` (ISO date), `types` (CSV of `PaymentDeliver.CONFIRM` values 0/1/2).

**Response**: `{ status, result:[ [<header row>], [<value row>], … ] }` — first inner array is column names, rest are values. Columns: `client_id, client_name, territory_id, territory_name, address, currency_id, currency_name, trade_id, trade_name, summa, type, date, comment`.

**Gotchas**: filtered to `pd.USER_ID = current`. Empty array on errors / no token (status=false). Strips HTML from `comment`.

## actionGetOrderNotes

`POST /api3/expeditor/getOrderNotes` — selectable order-note dictionary.

**Response**: `{ status, result:[{note_id, note_name}], error? }` from `OrderComment` (ACTIVE='Y', ordered by SORT).

## See also

- [api-v3-mobile overview](./)
- [Authentication](../authentication.md)
- [Error codes](../error-codes.md)
