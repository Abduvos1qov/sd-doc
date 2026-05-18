---
title: "api-v4-online · Order"
sidebar_position: 1
---

# api-v4-online · `OrderController`

Endpoints for `OrderController` (`protected/modules/api4/controllers/OrderController.php`). 6 endpoint(s) — 2 Yii action-methods on the controller (`list`, `detail`, `updateComment`, `checkStatus`) plus 2 action classes wired through `actions()` for expeditor flows. Controller extends `BaseController` (Bearer auth).

## `GET /api4/order/list`

- **Controller**: `OrderController::actionList` (`OrderController.php:28`).
- **Auth**: BaseController auth. Non-role-10 users are pinned to their own agent ID (`agent_ids = [user.AGENT_ID]`); only role 10 (admin) may pass a custom `agent_ids` array.
- **Request (params)**: `client_id` (required), `from_date` (YYYY-MM-DD, default `1970-01-01`), `to_date` (YYYY-MM-DD, default `9999-12-30`), `agent_ids[]` (admin only), `unpaid` (boolean — when true, filters via `HAVING unpaid > 0`).
- **Response columns**: `id, agent_name, expeditor_name, summa, discount, unpaid, date, date_load, client_id, price_type_id, agent_id, trade_id, unconfirmed_summa` for delivered orders (`TYPE=1, STATUS=3`).
- **Side-effects**: None — read.
- **Gotchas**: `unpaid` is `ABS(ClientTransaction.SUMMA + COMPUTATION)` so partially-closed orders surface their remaining balance. `unconfirmed_summa` aggregates `PaymentDeliver.SUMMA` where `CONFIRM=0`. Returns `{success:false, message: '...'}` (HTTP 200) on date-format or client-not-found errors — caller must inspect the envelope. Sorted `DATE_LOAD DESC`.

## `GET /api4/order/detail`

- **Controller**: `OrderController::actionDetail` (`OrderController.php:122`).
- **Auth**: BaseController auth.
- **Request (params)**: `order_id` (required), `enable_bonus` (boolean — when true and order has `BONUS_ORDER_ID`, bonus rows are concatenated).
- **Response columns**: `product_cat_id, product_id, name, quantity, initial_quantity, pack_quantity, price, volume, is_bonus`. Sorted by product name.
- **Side-effects**: None.
- **Gotchas**: `quantity` is reduced by any pending defect-detail amount (`OrderDefectDetail` linked via `Order.CONTRACT_ID`, semicolon-separated). `is_bonus=true` rows have `price=0`. `initial_quantity` preserves the original line count for diffing. `pack_quantity` is forced to `1` when 0.

## `GET /api4/order/expeditor-order-list`

- **Controller**: `OrderController::actions['expeditor-order-list']` → `ExpeditorOrderList` (`protected/modules/api4/actions/expeditor/ExpeditorOrderList.php`).
- **Auth**: `authenticate()` + `authorize([User::ROLE_EXPEDITOR])`. GET only — POST returns 405.
- **Request (query)**: `date` (YYYY-MM-DD, required) — defines `[date 00:00:00, date 23:59:59]` window.
- **Response**: Composite envelope built across 6 internal builders — `orderList`, `orderDetail`, `orderBonusDetail`, `orderDefectDetail`, `orderReplaceDetail`, `orderBonus`. Each order is typed as one of `order` (TYPE=1), `refund` (TYPE=2), `replace` (TYPE=3).
- **Side-effects**: None — read-only.
- **Gotchas**: Date must be valid (`Validator::validateDate('Y-m-d')`) — HTTP 400 otherwise.

## `POST /api4/order/sync-expeditor-order`

- **Controller**: `OrderController::actions['sync-expeditor-order']` → `SyncExpeditorOrder` (`protected/modules/api4/actions/expeditor/SyncExpeditorOrder.php`).
- **Auth**: `authenticate()` + `authorize([User::ROLE_EXPEDITOR])`. POST only.
- **Request body (JSON)**: array of `{order_id, ...}` post-order entries plus device token / sync metadata expected by `checkSyncLog`.
- **Response**: Per-item array of `makeError`/`makeResult` envelopes. Skipped items get `ERROR_CODE_SYNC_PROCESSING` (PROCESSING sync-log) or short-circuit success (`SUCCESS` sync-log).
- **Side-effects**: Validates `expeditor_id` matches the caller's `AGENT_ID` (`ERROR_CODE_EXPEDITOR_IS_NOT_MATCH`). Validates order quantities (`ERROR_CODE_INVALID_QUANTITY_ORDER`). Builds bi-directional stock movements (`movementToExpeditor` / `movementFromExpeditor`). Sync log uses `sync-expeditor-order` action key.
- **Gotchas**: Missing `order_id` per item → `ERROR_CODE_MISSING_REQUIRED_PARAM` for that item only; other items in the batch still process. Sync-log replay safety — re-submitting the same item returns the original result rather than re-applying.

## `POST /api4/order/updateComment`

- **Controller**: `OrderController::actionUpdateComment` (`OrderController.php:233`).
- **Auth**: BaseController auth. Role 4 (agent) only — HTTP 400 with `'The role must be agent'` otherwise. JSON body required.
- **Request body (JSON)**: array of `{order_id, comment}` entries. Empty body → HTTP 400 `Empty body`.
- **Response**: `{success: true, result: [<updated_order_ids>]}` JSON (manual `echo`).
- **Side-effects**: Direct SQL `UPDATE Order SET COMMENT=:comment WHERE ORDER_ID=:order_id AND AGENT_ID=:agent_id`. Agent can only update comments on their own orders. `null` comment is coerced to empty string.
- **Gotchas**: Only `order_id`s whose update affected ≥ 1 row appear in `result` — unknown IDs or wrong-agent IDs are silently dropped. No transaction wrapping the batch.

## `GET /api4/order/checkStatus`

- **Controller**: `OrderController::actionCheckStatus` (`OrderController.php:267`).
- **Auth**: BaseController auth. GET only — explicit HTTP 405 with `Method not allowed. Use GET.` otherwise. Role 4 (agent) only — HTTP 403 otherwise.
- **Request (query)**: `date` (free-form `strtotime`-able; defaults to today). Invalid date → HTTP 400 `Invalid date`.
- **Response**: `{success: true, result: {order: [{order_id, status, client_id, summa, type, trade_id}, ...], payment: [{order_id, client_id, currency_id, summa, trade_id}, ...]}}`. Status/IDs are stringified, summa is float.
- **Side-effects**: None — pure read. Joins `Order × User` (ROLE=4) by `CREATE_BY` to filter to the agent's own work, plus `PaymentDeliver × User` for unconfirmed (`CONFIRM=0`) payments on the same day.
- **Gotchas**: The "agent" matching uses `User.AGENT_ID = :agent_id` on the order's `CREATE_BY` user, not the `Order.AGENT_ID` field — covers cases where a supervisor created the order on behalf of the agent. `date` resolution is by `Y-m-d` string after `strtotime`.

## `POST /api4/order/set-labelcodes` / `POST /api4/order/set-cises`

- **Controller**: `OrderController::actions['set-labelcodes' | 'set-cises']` → `SetOrderCises` (`protected/modules/api4/actions/markirovka/SetOrderCises.php`).
- **Auth**: `authenticate()` + `authorize([10, 20])` — admin/manager roles for markirovka (mandatory product labelling) flow.
- **Request**: query `order_id`; body — array of CIS code objects (raw, unvalidated).
- **Response**: Standard `sendResult`/`sendError` envelope.
- **Side-effects**: Persists the raw payload to `OrderCisesLog` for audit; downstream validators consume the log.
- **Gotchas**: Empty cises array returns localized `ERROR_CODE_INVALID_PARAM` (Russian/English/Uzbek messages). Missing order → `ERROR_CODE_DOCUMENT_NOT_FOUND`. Both aliases (`set-labelcodes`, `set-cises`) route to the same class — naming kept for backward compatibility.

## `GET /api4/order/get-labelcodes-status` / `GET /api4/order/get-cises-status`

- **Controller**: `OrderController::actions['get-labelcodes-status' | 'get-cises-status']` → `GetOrderCisesStatus` (`protected/modules/api4/actions/markirovka/GetOrderCisesStatus.php`).
- **Auth**: `authenticate()` + `authorize([10, 20])`.
- **Request (query)**: `order_id` (or legacy `id`).
- **Response**: `{id, status, status_text, status_color, editable}`. `status` ∈ `waiting_for_cis | waiting_for_send | signed | <error states from OrderEsf>`. `status_color` is a hex code intended for direct rendering in mobile UIs.
- **Side-effects**: None.
- **Gotchas**: When `OrderCises` is empty → `waiting_for_cis` + `editable=true`; when `OrderEsf` row missing → `waiting_for_send` + `editable=false`; signed ESF → `signed` + `editable=false`.

## See also

- [api-v4-online overview](./)
- [Authentication](../authentication.md)
- [Error codes](../error-codes.md)
