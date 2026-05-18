---
title: "api-v4-online · Edit"
sidebar_position: 1
---

# api-v4-online · `EditController`

Endpoints for `EditController` (`protected/modules/api4/controllers/EditController.php`). Update existing van-sell returns, tasks, and task results created via the mobile/B2B API. All actions are wired as Yii action classes inside `controller->actions()` and require a Bearer token plus a registered device token.

## `POST /api4/edit/vs-return`

- **Controller**: `EditController::actions['vs-return']` → `EditVsReturnAction` (`protected/modules/api4/actions/EditVsReturnAction.php`).
- **Auth**: `authenticate()` + `authorize([4])` — agent role only. Agent must be van-sell (`Agent::isVanSelling()`) with a configured van warehouse, otherwise HTTP 403.
- **Request body (JSON)**: `id` (VsReturn ID), `mobile_uuid`, `request_id`, `create_at` (ISO date — re-validated through `Validator::formatISODate`), `price_type_id`, `comment?`, `products[]` (each `{product_id, count, price}`).
- **Response**: `{status: true, result: {return_id, added: true}}` on success; otherwise a `makeError`-shaped envelope.
- **Side-effects**: Replays sync-log guard (`edit-vs-return`); only edits a `VsReturn` whose `STATUS = NEW`; rewrites `VsReturnDetails`; re-runs `StoreDetail::VsExchange` movements both directions to reconcile stock deltas between `FROM_STORE_ID` and `TO_STORE_ID`.
- **Gotchas**: Manual-price toggle comes from the price type (`HAND_EDIT`), not the request. Out-of-stock detection runs against both source and destination warehouses; partial overlaps with the previous version of the document raise `ERROR_CODE_OUT_OF_STOCK` with per-line stock counts. Empty `products` after validation returns `ERROR_CODE_EMPTY_REQUEST_BODY`.

## `POST /api4/edit/task`

- **Controller**: `EditController::actions['task']` → `EditTaskAction` (`protected/modules/api4/actions/EditTaskAction.php`).
- **Auth**: `authenticate()` + `authorize()` (any role with a valid token).
- **Request body (JSON)**: array of task edits, each `{id, name, type_id, assignee_id?, deadline?, status, client_id?, comment?, comment_result?, photo? (base64), photo_result? (base64), color?, latitude?, longitude?, create_at, request_id}`.
- **Response**: array of per-item `makeResult({task_id})` or `makeError(...)` envelopes — one entry per input item.
- **Side-effects**: Decodes base64 photos into `/upload/photoTask/YYYYMM/task-*.{ext}` and `/upload/photoTask/YYYYMM/result-*.{ext}` (folder is auto-created). Updates `Tasks` row in place; resets `CONFIRM = 0` so supervisors must re-confirm; defaults `assignee_id` to the calling user if the supplied assignee is not role 4.
- **Gotchas**: Status is clamped to `0..5`; invalid values fall back to `Tasks::STATUS_CREATED`. Lat/lon are nulled if either is zero. `deadline` is re-parsed through `Validator::formatISODate`; bad dates yield `ERROR_CODE_INVALID_DATE_FORMAT`. Missing client → `ERROR_CODE_CLIENT_NOT_FOUND`.

## `POST /api4/edit/task-result`

- **Controller**: `EditController::actions['task-result']` → `EditTaskResultAction` (`protected/modules/api4/actions/EditTaskResultAction.php`).
- **Auth**: `authenticate()` + `authorize()` (any role).
- **Request body (JSON)**: array of `{task_id, status?, comment_result?, photo_result? (base64), create_at, client_id?, request_id}`.
- **Response**: array of `makeResult({task_id})` / `makeError(...)` envelopes — same one-per-item pattern as `/edit/task`.
- **Side-effects**: Same photo-on-disk persistence as `edit/task` (result image only). Updates `Tasks.STATUS`, `COMMENT_R`, `IMAGE_RESULT`; leaves the original task definition (name, type, deadline, assignee) untouched.
- **Gotchas**: Status is clamped to `0..5` and defaults to `Tasks::STATUS_EXECUTED` (not `STATUS_CREATED`). Missing `task_id` → `ERROR_CODE_DOCUMENT_NOT_FOUND` for that item only; other items in the batch still process.

## See also

- [api-v4-online overview](./)
- [Authentication](../authentication.md)
- [Error codes](../error-codes.md)
