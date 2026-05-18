---
title: "api-v4-online · Get"
sidebar_position: 1
---

# api-v4-online · `GetController`

Endpoints for `GetController` (`protected/modules/api4/controllers/GetController.php`). Read-only fetchers for van-sell exchange/return line items. Wired as a single Yii action class.

## `GET /api4/get/vs-items`

- **Controller**: `GetController::actions['vs-items']` → `GetVsItemsAction` (`protected/modules/api4/actions/GetVsItemsAction.php`).
- **Auth**: `authenticate()` + `authorize([4])` — agent only. Agent must be van-sell (`Agent::isVanSelling()` true and `getVanWarehouse()` non-empty), otherwise HTTP 403.
- **Request (query)**: `id` (VsExchange or VsReturn primary key), `type` (`order` for exchange / `return` for return — anything else → `ERROR_CODE_MISSING_REQUIRED_PARAM`), `response_type` (`json` returns associative rows; anything else gets the tabular `[columns, ...rows]` shape via `ArrayHelper::tabularData`), `request_id`.
- **Response**: List of items `{product_id, product_name, category_id, category_name, quantity, price, summa}` joined against `Product` and `ProductCategory`. Wrapped in the standard `sendResult` envelope.
- **Side-effects**: None — pure read.
- **Gotchas**: `type=order` reads `VsExchangeDetails` (keyed on `VS_EXCHANGE_ID`); `type=return` reads `VsReturnDetails` (keyed on `VS_RETURN_ID`). Missing document on either branch raises `ERROR_CODE_DOCUMENT_NOT_FOUND` with both `id` and `type` in the payload — handy for client-side disambiguation.

## See also

- [api-v4-online overview](./)
- [Authentication](../authentication.md)
- [Error codes](../error-codes.md)
