---
title: "api-v3-mobile · Order"
sidebar_position: 1
---

# api-v3-mobile · `OrderController`

Per-action reference for `protected/modules/api3/controllers/OrderController.php` (4 actions). The **agent (ROLE=4) mobile app** uses this to draft, post and update orders.

## Common contract

- **Base URL pattern**: `POST /api3/order/<actionName>` (Yii camel-case).
- **Auth**: `deviceToken` from `HTTP_DEVICETOKEN` header. `User::userByDeviceToken($token)` (any role with matching token). After lookup the controller calls `UserIdentity` to start a Yii session.
- **Response envelope**: raw JSON, varies per action.

---

## actionPostDraft

`POST /api3/order/postDraft` — persist the user's order draft to the server (a backup of the basket).

**Request**: arbitrary JSON body (the draft); also pulls `HTTP_DEVICETOKEN`.

**Response**: `{ status:'ok' }`.

**Side effects**: writes `DOCUMENT_ROOT/upload/draft/Agent-<AGENT_ID>-Draft.txt`. Overwrites any previous draft for the same agent.

**Gotchas**: stored unencrypted; one draft per agent (latest wins).

## actionGetDraft

`GET /api3/order/getDraft` — read the saved draft.

**Response**: the raw file contents (JSON) or `"[]"` when no draft exists.

## actionPost

`POST /api3/order/post?forceDate=true|false` — sync one or more orders created on mobile.

**Request** (JSON array): `[{ id (mobile UUID), clientId, type:'order'|'refund'|'replace', createdAt (ms), shipmentDate (ms)?, storeId, tradeId, paymentTypeId, contractId?, orderNoteId?, draft, comment, products:[{productId,totalItems,price,discount,...}], bonusProductList?, ... }]`.

**Response** (array): per-order `{ id, status:int (0=error,1=success,2=warning,3=info), orderId?, message?, …full order DTO when synched (`fullResponse()`) }`.

**Side effects** — extensive. Per order:
- Dedupe via `SyncLog` keyed by `(DAY, DEVICE_TOKEN, MOBILE_ORDER_ID)` (TTL ~120s); re-entrant calls during processing return `sleep(1); die()`. Successful syncs are remembered so retries echo the existing `orderId`.
- Creates `Order` (TYPE=1) / `OrderDefect` (TYPE=2) / `OrderReplace` (TYPE=3) + their `*Detail` rows + `BonusOrderDetail`.
- Applies `Skidka` (discount engine) — manual or auto depending on `paymentTypeId`/contract.
- Looks up `Price`/`OldPrice` per product+price-type for missing rows.
- Computes `DATE_LOAD` from `shipmentDate` or `ServerSettings::setAutoDateLoad()` (today+N days at 09:00).
- For paid-at-order flows: writes `ClientTransaction` (TRANS_TYPE=3), calls `TransactionClosed::setting_new`, `ClientFinans::correct` (or `ClientTransaction::correct` in contragent mode).
- Reconstructs `Client` from `upload/dublicate/<id>-deleted` JSON when the client was soft-deleted client-side.
- Fires `TelegramReport::notEnough` (deferred via `AfterResponse::run`) when stock is short.
- Logs errors via `ErrorReporter::sendMessage` for `[api3/order/post]`.

**Gotchas**:
- `forceDate=true` honours `createdAt` even for cross-day orders; otherwise an out-of-day order date is bumped to today 01:00.
- Empty input → `[{ status:0, message:'Empty Order' }]`.
- Looks for soft-deleted clients in `upload/dublicate/`; if not found, the order is rejected.
- Order types: 1=order, 2=return-from-shelf, 3=replace.

## actionUpdate

`POST /api3/order/update?orderId=…` — limited edit of an order after it has been synched (comment, consignment flag, shipmentDate, orderNoteId, cancel).

**Request** (JSON): `{ orderId, post:{ comment, consignation, consignationDate, shipmentDate, orderNoteId, orderStatus:'cancel' } }`.

**Response**: `{ orderId, status:int, message, info?, order:{ comment, consignation }, modelError? }`.

**Status codes** (returned in body, not HTTP):
- `0` Access denied
- `1` Can edit (no changes applied)
- `2` Saved
- `3` Save error
- `4` Order not found

**Gotchas**:
- Full edit only when `Order.STATUS=1 AND UPDATE_BY=currentUser`.
- When `agent.config.order.editCommentAfterSync` is true, comment-only edits are allowed after sync — but rejected once `STATUS in (2,3)` (loaded/delivered).
- `orderStatus='cancel'` sets `Order.STATUS=4`.
- Logs the raw input to `Order_Update.txt` in document root.

## See also

- [api-v3-mobile overview](./)
- [Authentication](../authentication.md)
- [Error codes](../error-codes.md)
