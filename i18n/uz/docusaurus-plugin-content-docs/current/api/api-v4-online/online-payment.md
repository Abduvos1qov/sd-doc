---
title: "api-v4-online · OnlinePayment"
sidebar_position: 1
---

# api-v4-online · `OnlinePaymentController`

Endpoints for `OnlinePaymentController` (`protected/modules/api4/controllers/OnlinePaymentController.php`). 8 action(s). Provides the list of enabled online-payment providers plus per-provider check/pay/QR endpoints used by mobile clients and bank callbacks. All actions are wired through `actions()` and dispatched to classes under `protected/modules/api4/actions/online-payment/`.

## `GET /api4/onlinePayment/list`

- **Controller**: `actions['list']` → `ListAction` (`protected/modules/api4/actions/online-payment/ListAction.php`).
- **Auth**: `authenticate()` + `authorize()` — any authenticated user.
- **Request**: No parameters.
- **Response**: `sendResult(['payme'])` — array of provider codes. Currently `payme` is added only when `ServerSettings::countryCode() === 'UZ'`; otherwise the array is empty.
- **Side-effects**: None.
- **Gotchas**: The list is country-gated, not feature-flagged per tenant. Even if Optima/Odengi/Kaspi credentials are configured, only `payme` (in UZ) appears here — those providers are reached by direct URL callbacks from the bank.

## `POST /api4/onlinePayment/payme-pay`

- **Controller**: `actions['payme-pay']` → `PaymeGoPayAction` (`.../online-payment/PaymeGoPayAction.php`).
- **Auth**: `authenticate()` + `authorize()`.
- **Request body (JSON)**: `token` (Payme card token), `order_id`, `amount` (in tiyin), `old` (boolean), `order_items[]` (for `old=false`: `{product_id, quantity}` list used to enforce client/server sync).
- **Response**: `sendResult({id: <PAYME_TRANSACTION_ID>, fiscal_items: [...]})`.
- **Side-effects**: Validates `Yii::app()->params['paycom']` credentials; loads the order (must be `TYPE=1`, `STATUS=3` — delivered); rejects if a paid `ClientPaymeTransaction` or settled `TransactionClosed` already covers `SUMMA`. Builds fiscal items (validates IKPU via `Validator::checkIKPU`, computes per-item discount = `round(price*qty) - round(100*summa)`). Calls Payme `receipts.create` then `receipts.pay`; on success persists `ClientPaymeTransaction`, `OnlinePayment` (SERVICE_TYPE_PAYME), `ClientTransaction` (TRANS_TYPE=3, TYPE=1, COMMENT="Оплата через Payme GO"), runs `ClientFinans::correct`, auto-creates the missing order client-transaction if absent, and closes via `TransactionClosed::closeTransaction`.
- **Gotchas**: `amount` is verified server-side against the fiscal-item sum; mismatch → `ERROR_CODE_PAYCOM_AMOUNT`. Missing IKPU/VAT on any product → localized `ERROR_CODE_PAYCOM_ERROR`. On any failure after `receipts.create` succeeds, the action calls `receipts.cancel` to undo the Payme-side receipt. URL switches between `checkout.test.paycom.uz` and `checkout.paycom.uz` based on `paycom.development`.

## `POST /api4/onlinePayment/payme-check`

- **Controller**: `actions['payme-check']` → `PaymeGoCheckAction` (`.../online-payment/PaymeGoCheckAction.php`).
- **Auth**: `authenticate()` + `authorize()`.
- **Request body (JSON)**: `order_id`, `old` (boolean), `order_items[]` (when `old=false`).
- **Response**: `sendResult({amount, fiscal_items})` — `amount` in tiyin (`round(100 * summa)` summed), `fiscal_items` is the same fiscal structure that `payme-pay` will send.
- **Side-effects**: None — read-only pre-flight before `payme-pay`. Same order/status/payment guards as `payme-pay` (delivered, not already paid, not partially paid by `PaymentDeliver`).
- **Gotchas**: This is the "dry run" — if `payme-check` succeeds, `payme-pay` will use the same fiscal items and amount. Sync drift (`order_items` count not matching DB) → "Заказ не синхронизирован".

## `POST /api4/onlinePayment/odengi-pay`

- **Controller**: `actions['odengi-pay']` → `OdengiPayAction` (`.../online-payment/OdengiPayAction.php`).
- **Auth**: None at the Yii layer — authentication is hash-based (`hash_hmac('md5', ...)` of `trans_id:::status_pay:::site_id:::order_id:::amount:::currency:::mktime:::test` keyed by `Yii::app()->params['odengi']['passw']`). This is a server-to-server callback endpoint, not user-facing.
- **Request body (JSON, from O!Деньги)**: `trans_id`, `status_pay`, `site_id`, `order_id`, `amount`, `currency`, `mktime`, `account_id`, `test`, `hash`.
- **Response**: None (`exit()` after work). Errors are logged via `Logger::logError` to `odengi.runstart` and dated dump files under `/upload/odengi/YYYY-MM-DD/`.
- **Side-effects**: Validates hash → saves `ClientOdengiTransaction` → creates `OnlinePayment` (SERVICE_TYPE_ODENGI, `amount/100`) → creates `ClientTransaction` (TRANS_TYPE=3, TYPE=1, CASHBOX=1, COMMENT="Оплата через O!Деньги"), runs `ClientFinans::correct`, auto-creates the order's debit `ClientTransaction` if missing, calls `TransactionClosed::closeTransaction`, fires `notifyClient()`.
- **Gotchas**: Order must be `TYPE=1`. The integration is auto-disabled unless `Yii::app()->params['odengi']['passw']` is set (`odengiExtensionIsOn` flag). The handler also supports a `"<prefix>::<orderId>"` form in `order_id` for testing. No DB transaction wrapping — each save can fail independently and the run will `exit()` mid-flow.

## `GET /api4/onlinePayment/optima-qr`

- **Controller**: `actions['optima-qr']` → `OptimaQRAction` (`.../online-payment/OptimaQRAction.php`).
- **Auth**: None — public. Order is referenced via `orderId` query param and only summed for QR generation.
- **Request (query/REQUEST)**: `orderId` (required), `version` (`v1` default, `v2` enables `legalPartyId`/`salePointCode`/`cashCode` requisite), `test` (use the test bank endpoint).
- **Response**: Plain text — a `data:image/png;base64,...` URI (no JSON wrapper). On error, HTTP 500 with a plain-text message.
- **Side-effects**: HTTP POST to `https://api.optimabusiness.kg` (or `test-ob.optimabank.kg`) `/api/v1/generate/qr` or `/api/v2/generate/qr` with the Optima X-API-KEY token from `Yii::app()->params['optima']`. No DB writes.
- **Gotchas**: Missing/zero `SUMMA` rejected as "Сумма заявки должна быть больше нуля". v2 requires the extra fields in `params['optima']`. If `params['optimaConfigs']['payerClientType']` is set, it is included in the request body.

## `POST /api4/onlinePayment/optima-pay`

- **Controller**: `actions['optima-pay']` → `OptimaPayAction` (`.../online-payment/OptimaPayAction.php`).
- **Auth**: HTTP Basic via header `Authorization: Basic <base64(optimabank:q*)>wW?X^^m3oC1])>` — hardcoded credentials checked against the constant in the action. Server-to-server callback from Optima Bank.
- **Request (query + body)**: query `orderId`; JSON body `{transactionId, status, sum, note ([host, orderId]), transactionProcessedDateTime, payerClientType?}`.
- **Response**: JSON `{message, transactionId, receievedAt}` on success; HTTP 4xx/5xx with `{error, details}` on validation/processing failure.
- **Side-effects**: Wraps everything in a DB transaction (`Yii::app()->db->beginTransaction()`). On success: `ClientOptimaTransaction` → `OnlinePayment` (SERVICE_TYPE_OPTIMA) → `ClientTransaction` (TRANS_TYPE=3, COMMENT="Оплата через Optima Bank") → `ClientFinans::correct` → debit auto-create → `TransactionClosed::closeTransaction`. `notifyClient()` fires only after commit. Maintains a per-request log buffer flushed to `runtime/optima/optima-YYYY-MM-DD.log`.
- **Gotchas**: `note[0]` must equal `$_SERVER['HTTP_HOST']` — protects against cross-tenant callbacks on shared infra. `note[1]` is the actual order ID. `payerClientType` is validated against `params['optimaConfigs']['payerClientType']` when configured. Order must be `TYPE=1` and `sum > 0`.

## `POST /api4/onlinePayment/kaspi-check`

- **Controller**: `actions['kaspi-check']` → `KaspiCheckAction` (extends `KaspiBaseAction`).
- **Auth**: Kaspi-specific (handled by `KaspiBaseAction::prepare()` — IP allow-list and shared-secret check). Not the standard `authenticate()` flow.
- **Request (Kaspi callback format)**: `txn_id`, `account` (order_id), `command=check`.
- **Response**: Kaspi-compliant JSON `{result, txn_id, comment, account, fullDocAmount, tradePointRfoCode, bin, nds_percentage, products: [{id, nameRu, nameKz, unitNameRu, unitNameKz, unitPrice, unitCount, fullCost, barCode, gtin}, ...]}`. Errors return `{txn_id, result: <kaspi_code>}` where kaspi_code is `1` for config errors, `5` for generic.
- **Side-effects**: Read-only. Calls `KaspiService::checkPayment($order_id)` which throws `KaspiException` if order is already paid/invalid. Resolves merchant `bin`/`tradePointRfoCode` from the `Diler` record matching `Yii::app()->params['kaspi_diler_id']` (or order's DILER_ID).
- **Gotchas**: BIN and tradePointRfoCode have whitespace stripped via `preg_replace('/\\s+/', '', ...)`. Only `unitCount > 0` line items are returned. Missing `kaspi_diler_id` config → KaspiException with result=1.

## `POST /api4/onlinePayment/kaspi-pay`

- **Controller**: `actions['kaspi-pay']` → `KaspiPayAction` (extends `KaspiBaseAction`).
- **Auth**: Same as `kaspi-check` — `KaspiBaseAction::prepare()` (IP allow-list + shared secret).
- **Request (Kaspi callback format)**: `txn_id`, `txn_date`, `account` (order_id), `accountType?`, `fullDocAmountFact`, `command=pay`.
- **Response**: Kaspi-compliant JSON `{result, command:'pay', account, txn_id, txn_date, fullDocAmountFact, products: [{id, factSellUnitCount, factSellFullCost}, ...]}`. On error: `{txn_id, result: <code>}` where `3` = duplicate `KASPI_TRANS_ID` (SQLSTATE 23000 / errno 1062), `5` = anything else.
- **Side-effects**: Single DB transaction wrapping `saveKaspiTransaction` → `saveOnlinePayment` → `saveClientTransaction` (TRANS_TYPE=3, CASHBOX=`kaspi_cashbox_id` or 1, COMMENT="Оплата через Kaspi.kz") → `closeOrderDebt` (auto-create order debit if missing) → `TransactionClosed::closeTransaction` → commit. `notifyClient()` is fired only after commit; failures there are logged but don't roll back.
- **Gotchas**: Server recomputes the canonical amount as `int(round(SUMMA*100))/100` and compares to Kaspi's `fullDocAmountFact`; mismatch raises `KaspiException(code=5)`. `ClientFinans::correct` stays inside the transaction (balance state). Duplicate-key detection is by SQLSTATE/error code rather than message string (locale-resilient).

## See also

- [api-v4-online overview](./)
- [Authentication](../authentication.md)
- [Error codes](../error-codes.md)
