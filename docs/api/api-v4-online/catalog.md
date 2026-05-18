---
title: "api-v4-online · Catalog"
sidebar_position: 1
---

# api-v4-online · `CatalogController`

Endpoints for `CatalogController` (`protected/modules/api4/controllers/CatalogController.php`). 23 action(s). All actions extend `BaseController`, return data through `$this->response($rows, $cols)` (which supports both JSON and tabular `[columns, ...rows]` envelopes), and honour per-user restriction filters (`getRestricted*ID()` from the base controller). The legacy `?timestamp=` query is rejected with HTTP 401 in `init()`.

## `GET /api4/catalog/products`

- **Controller**: `CatalogController::actionProducts` (`CatalogController.php:17`).
- **Auth**: BaseController auth (Bearer). Restricted product IDs are filtered out via `getRestrictedProductsID()`.
- **Request**: No body params. Response shape is driven by the global `response_type` query honoured by `BaseController::response`.
- **Response columns**: `id, name, category_id, subcategory_id, brand_id, trade_id, pack_quantity, box_quantity, bar_code, bar_codes, xml_id, sort, volume, weight, unit_id, is_mml, power_sku, by_block, image_id, part_number, description`.
- **Side-effects**: None. Reads from `Product` (filial-aware table name via `getFilialData`). `box_quantity` is multiplied by `pack_quantity` server-side, so the value is already in "single units per box". `bar_codes` is a JSON-encoded array of trimmed barcodes split by space, only when `bar_code` is non-empty.
- **Gotchas**: `pack_quantity <= 0` is forced to `1.0`; same for `box_quantity`. `is_mml`, `by_block` are normalised to `true/false`. `power_sku` is `== '1'` (string compare). `image_id` is `NULL` unless `PHOTO` is non-empty.

## `GET /api4/catalog/productCategories`

- **Controller**: `CatalogController::actionProductCategories` (`CatalogController.php:97`).
- **Auth**: BaseController auth. Filter via `getRestrictedProductCategoriesID()`.
- **Request**: No params.
- **Response columns**: `id, name, sort, unit_id`. Only `ACTIVE='Y'` rows.
- **Side-effects**: None.
- **Gotchas**: `sort` cast to int.

## `GET /api4/catalog/productSubcategories`

- **Controller**: `CatalogController::actionProductSubcategories` (`CatalogController.php:128`).
- **Auth**: BaseController. Filter via `getRestrictedProductSubcategoriesID()`.
- **Response columns**: `id, name, sort`. `ACTIVE='Y'` only.
- **Gotchas**: `sort` cast to int.

## `GET /api4/catalog/productBrands`

- **Controller**: `CatalogController::actionProductBrands` (`CatalogController.php:159`).
- **Auth**: BaseController. Filter via `getRestrictedProductBrandsID()`.
- **Response columns**: `id, name, sort` from `AdtBrands`. `ACTIVE='Y'` only.

## `GET /api4/catalog/trades`

- **Controller**: `CatalogController::actionTrades` (`CatalogController.php:190`).
- **Auth**: BaseController. Filter via `getRestrictedTradesID()`.
- **Response columns**: `id, name, description` from `TradeDirection`. `ACTIVE='Y'` only.

## `GET /api4/catalog/priceTypes`

- **Controller**: `CatalogController::actionPriceTypes` (`CatalogController.php:215`).
- **Auth**: BaseController auth. Role 4 (agent) gets a heavily filtered list.
- **Request (params)**: `all` (boolean) — when true, includes both purchase (`TYPE=1`) and selling (`TYPE=2`) price types; otherwise selling only.
- **Response columns**: `price_type_id, name, for_client, is_manual, type, currency_id, min_price_type_id`. Sorted by `SORT, NAME`.
- **Side-effects**: For role-4 agents the result also filters out manual-edit price types (`HAND_EDIT=0`) unless either `ServerSettings::allowManualPriceForVansell()` / `allowManualPriceForAgent()` is on, or the agent config flag `showEmptyProduct.enableManualPriceType.value == 1` is set.
- **Gotchas**: `for_client` is boolean (`== 1`). `is_manual` is `'Y'/'N'` after the CASE in SQL, then converted to bool. `type` becomes `'purchase'` (TYPE=1) or `'selling'` (TYPE=2).

## `GET /api4/catalog/paymentTypes`

- **Controller**: `CatalogController::actionPaymentTypes` (`CatalogController.php:279`).
- **Auth**: BaseController. Role 4 agents get filtered by `agent.agentPaymentCurrency.value` config.
- **Response columns**: `id, name, code, title` from `Currency` where `ACTIVE='Y'`.
- **Gotchas**: For agents, only currencies listed (comma-separated) in their packet config `agent.agentPaymentCurrency.value` are returned.

## `GET /api4/catalog/prices`

- **Controller**: `CatalogController::actionPrices` (`CatalogController.php:312`).
- **Auth**: BaseController. Filters via `getRestrictedPriceTypesID()` and `getRestrictedProductsID()`.
- **Response columns**: `price_type_id, product_id, price` joined `Price × PriceType × Product`, only selling (TYPE=2), both ACTIVE='Y'.
- **Side-effects**: When price types are restricted, the action additionally includes `MIN_PRICE_TYPE_ID` references so apps can compute floor prices.
- **Gotchas**: `price` cast to float. The MIN_PRICE_TYPE_ID expansion query unions in additional IDs so that prices for the floor-price reference are also returned.

## `GET /api4/catalog/productImage`

- **Controller**: `CatalogController::actionProductImage` (`CatalogController.php:372`).
- **Auth**: BaseController auth.
- **Request (params)**: `id` (image basename — `..`/path-traversal stripped via `basename()`), `thumb` (`true|false`; default `true`).
- **Response**: Raw image stream with `Content-Type` and `Content-Length` headers, `fpassthru`d to the client.
- **Side-effects**: When `thumb=true` and a 150×150 cached file does not exist at `upload/adtProduct/thumbs/150x150_<id>`, the action generates it via GD (`imagecreatefrompng/jpeg/webp`, `imagecopyresampled`) and writes it to disk. Sets HTTP 404 for missing/invalid images.
- **Gotchas**: `webp` resized result is encoded as JPEG. Output buffer is cleared (`ob_end_clean`) before streaming. Aspect-ratio preserving — the longer side is bound to 150.

## `GET /api4/catalog/warehouses`

- **Controller**: `CatalogController::actionWarehouses` (`CatalogController.php:420`).
- **Auth**: BaseController. Role 4 (agent) and role 8 (supervisor) get filtered down to attached warehouses.
- **Response columns**: `id, name, disable_stock_check, currencies_id` joined `Store × CreatedStores`, `STORE_TYPE=1`, `ACTIVE='Y'`. `currencies_id` is comma-separated (excluding `'0'`).
- **Gotchas**: Vansell agents see only their own van warehouses; non-vansell agents see all non-van warehouses plus those attached to their agent ID (`cs.AGENT_ID IN ('0', '<agent_id>')`). Supervisors see `0` plus all their subordinate agents' attached warehouses. `disable_stock_check` is bool.

## `GET /api4/catalog/notes`

- **Controller**: `CatalogController::actionNotes` (`CatalogController.php:489`).
- **Response columns**: `id, name, sort` from `OrderComment`, `ACTIVE='Y'`.

## `GET /api4/catalog/tara`

- **Controller**: `CatalogController::actionTara` (`CatalogController.php:511`).
- **Response columns**: `id, name, sort` from `Tara`, `ACTIVE='Y'`, sorted by `SORT`.

## `GET /api4/catalog/unit`

- **Controller**: `CatalogController::actionUnit` (`CatalogController.php:529`).
- **Response columns**: `id, name, code, title` from `Unit`, `ACTIVE='Y'`, sorted by `NAME`.

## `GET /api4/catalog/vsWarehouses`

- **Controller**: `CatalogController::actionVsWarehouses` (`CatalogController.php:548`).
- **Auth**: BaseController.
- **Response**: JSON via `$this->json($stores)` (bypasses the tabular envelope). Items `{id, name, type}` where `type` is one of `sale, virtual, return, reserve, none` mapped from `STORE_TYPE` 1/2/3/4. Only non-van warehouses (`VAN_SELLING=0`).
- **Gotchas**: Output format differs from the rest of the controller — always JSON object array.

## `GET /api4/catalog/clientCategories`

- **Controller**: `CatalogController::actionClientCategories` (`CatalogController.php:575`).
- **Response columns**: `id, name, sort` from `ClientCategory`, `ACTIVE='Y'`, sorted by `SORT`.

## `GET /api4/catalog/clientClassess`

- **Controller**: `CatalogController::actionClientClassess` (`CatalogController.php:592`).
- **Response columns**: `id, name` from `ClientClass`, `ACTIVE='Y'`, sorted by `NAME`. (Typo `clientClassess` is preserved from the original endpoint path.)

## `GET /api4/catalog/cities`

- **Controller**: `CatalogController::actionCities` (`CatalogController.php:608`).
- **Response columns**: `id, name, sort` from `City`, `ACTIVE='Y'`, sorted by `SORT`.

## `GET /api4/catalog/agents`

- **Controller**: `CatalogController::actionAgents` (`CatalogController.php:625`).
- **Response columns**: `id, name, tel` from `Agent`, `ACTIVE='Y'`, sorted by `FIO`. No filial/role restriction applied here.

## `GET /api4/catalog/reasons`

- **Controller**: `CatalogController::actionReasons` (`CatalogController.php:641`).
- **Response columns**: `id, name` from `RejectDefect`, `ACTIVE='Y'`. If the table is empty, a single fallback `[0, 'Магазин закрыт']` is injected so clients always have at least one reason.

## `GET /api4/catalog/photoCategories`

- **Controller**: `CatalogController::actionPhotoCategories` (`CatalogController.php:655`).
- **Auth**: BaseController. Restricted via `getRestrictedPhotoCategoriesID()` (NOT-IN filter — restricted IDs are excluded).
- **Response columns**: `id, name` from `ParentPhotoReport`, `ACTIVE='1'`, sorted by `SORT`.

## `GET /api4/catalog/images`

- **Controller**: `CatalogController::actionImages` (`CatalogController.php:680`).
- **Response columns**: `client_id, url, is_main` from `ClientPhoto`. Returns *all* client photos with no filter — large response on big tenants.

## `GET /api4/catalog/visiting`

- **Controller**: `CatalogController::actionVisiting` (`CatalogController.php:689`).
- **Response columns**: `client_id, agent_id, day` from `Visiting`. The whole table is dumped — caller filters client-side.

## `GET /api4/catalog/phoneNumbers`

- **Controller**: `CatalogController::actionPhoneNumbers` (`CatalogController.php:697`).
- **Response columns**: `client_id, phone_number` from `ClientPhones` where `PHONE != ''`.

## See also

- [api-v4-online overview](./)
- [Authentication](../authentication.md)
- [Error codes](../error-codes.md)
