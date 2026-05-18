---
title: "api-v3-mobile · Auditor"
sidebar_position: 1
---

# api-v3-mobile · `AuditorController`

Per-action reference for `protected/modules/api3/controllers/AuditorController.php` (41 actions). Used by the **field auditor / merchandiser / supervisor / sales-manager** mobile app.

## Common contract

- **Base URL pattern**: `POST /api3/auditor/<actionName>` (Yii camel-case mapping — `actionClientsV2` → `/api3/auditor/clientsV2`). All endpoints accept a JSON body (`Content-Type: application/json`); when missing, the controller falls back to `$_POST`.
- **Auth envelope** — every non-login endpoint reads three fields from the request body via `auth()` + `checkToken()`:
  - `userId` → `User.USER_ID` (must exist, `ACTIVE != 'N'`)
  - `positionId` → `StructureFilial.ID` (must exist, `ACTIVE != 'N'`, must belong to `userId`)
  - `deviceToken` → must already be present in `User.DEVICE_TOKEN` JSON array (issued by `actionLogin`).
- **Role gate**: only `User.ROLE` in `[8 Супервайзер, 9 Менеджер, 11 Мерчандайзер/Auditor]` can log in. Many endpoints further branch by role (see notes).
- **Response envelope**: every reply is wrapped in `{ ..., success: bool, httpStatus: int }`. String payloads become `{ message, success, httpStatus }`. Errors use status 400/401/402/403/405 with `success=false`.

---

## actionLogin

`POST /api3/auditor/login` — only public endpoint (no `auth()`).

**Request** (JSON body): `login`, `password` (plaintext, server md5s), `deviceToken`.

**Response**: `{ name, userId, role, support, tg_support }`.

**Side effects**: appends `deviceToken` to `User.DEVICE_TOKEN` JSON array (keeps last 4 tokens). Logs the user into the Yii session.

**Gotchas**: returns 401 for wrong creds, expired license (`hasSystemActive(4)` false), role ∉ {8,9,11}, supervisor with `PAY=0`. `deviceToken` is mandatory — empty token = 401.

## actionProfile

`POST /api3/auditor/profile` — returns positions (StructureFilial) the user can act as.

**Request**: `userId`, `deviceToken`.

**Response**: `{ profiles: [{ positionId, name, role, roleName, support, tg_support }] }`.

## actionConfig

`POST /api3/auditor/config` — server-side feature flags + photo/map config for the app.

**Request**: standard auth + optional `deviceModel`, `appVersion` (recorded back to `User`).

**Response**: `{ config: { <group>: {<key>: value}, server: { time, date, time_zone, time_zone_offset }, clientRequiredFields, photo: { maxWidth, maxHeight, compress }, yandexMapKey } }`.

**Side effects**: updates `User.DEVICE_MODEL`, `APP_VERSION`, `LAST_SYNC_TIME`. Caps photo size to 1000px/80% compression when `params.photoHighQuality` is off, else 1800/90.

**Gotchas**: Yandex map key is randomly picked from a 13-key pool.

## actionClients

`POST /api3/auditor/clients` — full client master, route plan and inventory for the position.

**Request**: standard auth only.

**Response**: `{ clients: [{ id, name, firm_name, tel, category, address, orient, region, channel, city, contact_person, form_sob, comment, lon, lat, bar_code, balance, typeId, needToAudit, agents:[{agentId,agentName}], inventory:[…], photos, photoAvatar, photoList, visitDays }] }`.

**Gotchas**: branches by `position.ROLE` — auditor (`11`) sees only clients in `VisitingAud` they own; supervisor (`8`) sees their position's agents' clients; manager (`9`) sees all active clients. Balance is read from `Contragent.BALANS` when `ServerSettings::isContragent()` else `Client.BALANS`.

## actionClientsV2

`POST /api3/auditor/clientsV2` — column-oriented variant of `clients` (smaller wire size).

**Request**: standard auth.

**Response**: `{ data: { avatars:{columns,data}, inventories:{columns,data}, clients:{columns,data} } }` where each `columns` is the ordered key list and `data` is array-of-arrays.

**Gotchas**: same role branching as `clients`. The avatar list is filtered to clients this auditor actually has in their route.

## actionClientsV3

`POST /api3/auditor/clientsV3` — same shape as `clientsV2` plus per-agent `visitDays` (column 23 becomes `[{agentId, days:"1/3/5"}]`).

**Request**: standard auth.

**Response**: `{ data: { avatars, inventories, clients } }` (`clients.columns[23]` is `agentVisitDays[]`).

## actionClientCategory

`POST /api3/auditor/clientCategory` — directory.

**Response**: `{ categories: [{ id, name }] }` from `ClientCategory` (ACTIVE='Y').

## actionTerritory

`POST /api3/auditor/territory` — directory.

**Response**: `{ territories: [{ id, name }] }` from `City` (ACTIVE='Y').

## actionChannel

`POST /api3/auditor/channel` — directory.

**Response**: `{ channels: [{ id, name }] }` from `ClientChannel`.

## actionClientType

`POST /api3/auditor/clientType` — directory.

**Response**: `{ types: [{ id, name }] }` from `ClientType` (ACTIVE='Y').

## actionComment

`POST /api3/auditor/comment` — preset reject/visit comment list.

**Response**: `{ comments: [{ id, name }] }` from `AdtComment` ordered by `SORT`.

## actionAgent

`POST /api3/auditor/agent` — agents this position can supervise / report on.

**Response**: `{ agents: [{ id, name }] }` where `id` is `USER_ID` and `name` is `Agent.FIO`.

**Gotchas**: ROLE=9 manager and ROLE=11 auditor see **all** ROLE=4 users; ROLE=8 supervisor sees only agents joined through `Supervayzer.USER_ID = currentUser`.

## actionAgentsV2

`POST /api3/auditor/agentsV2` — column-oriented agents (id = `AGENT_ID` not `USER_ID`).

**Response**: `{ agents: { columns:['id','name','userId'], data:[[id,name,userId], …] } }`.

**Gotchas**: ROLE=11 auditor's agent list is further filtered to agents who visit clients in this auditor's `VisitingAud` plan.

## actionPosition

`POST /api3/auditor/position` — list of other positions the user could switch to. **Only filled for supervisors (ROLE=8)** — others get empty.

**Response**: `{ positions: [{ id, name }] }`.

## actionAudit

`POST /api3/auditor/audit` — audit (SKU check) templates assigned to this auditor.

**Response**: `{ audits: [{ id, name, required, face_check, price_check, sold_check, store_check, face_required, price_required, sold_required, store_required, is_public, products:[{ id, name, brand, category, pack, producer, is_our, is_local, weight, volume, order, photo }] }] }`.

**Gotchas**: UNION across `Product` (is_our=Y) and `ProductCompetitor` (is_our=N). Filtered by `AdtAuditUsers.AUDITOR_ID = position.ID`.

## actionPoll

`POST /api3/auditor/poll` — polls assigned to this auditor.

**Response**: `{ polls: [{ id, name, required, description, questions: [{ id, name, type, sort, description, is_required, systemName, variants:[{id,name,is_our}] }] }] }`.

## actionPhoto

`POST /api3/auditor/photo` — photo-report category tree.

**Response**: `{ photos: [{ pr_cat_id, name, parent }] }` from `ParentPhotoReport` (ACTIVE=1, SORT).

## actionSetphoto

`POST /api3/auditor/setphoto` — upload one photo-report image (binary body).

**Request**: `clientId`, `categoryId`, `date` (ms), `checkInTime` (ms), `lat`, `lon`, raw `photo` bytes.

**Response**: `'Success'` or `{ message:'Photo is failed', messages:{uz,ru,en} }` (405).

**Side effects**: writes `DOCUMENT_ROOT/upload/photo/<YYYYMM>/<DD>/img-<clientId>-<date>.jpg`; compresses if >1.5MB; creates `PhotoReport`, sets `Visit.PHOTO=1`; on `.salesdoc.io` also creates `/bk/<host>/upload/photo` backup folder; fires `TelegramReport::merchandiserPhotoReport` and `firstVisitSvr` (if first visit of the day).

**Gotchas**: dedupes by URL — re-upload of an existing path is a no-op DB-wise.

## actionAvatar

`POST /api3/auditor/avatar` — upload a client storefront photo (avatar).

**Request**: `clientId`, `photo` (raw or base64 when `Content-Type: application/json`).

**Response**: `{ data: { id, clientId, main, url } }` on first upload, else `'Success'`.

**Side effects**: writes to `/upload/profilPhoto/<clientId>-<ts>.jpg`, inserts `ClientPhoto` (MAIN=1 if first, else MAIN=0).

## actionDeleteAvatar

`POST /api3/auditor/deleteAvatar` — delete a `ClientPhoto`.

**Request**: `photoId`.

**Response**: `'Success'` or 405.

**Gotchas**: only ROLE in `[8, 11]` (supervisor, auditor) may delete.

## actionSetMainAvatar

`POST /api3/auditor/setMainAvatar` — promote a photo to MAIN=1 (clears others on same client).

**Request**: `photoId`.

**Gotchas**: same ROLE gate as `deleteAvatar`.

## actionSetphoto2

Commented out in source. Treat as deprecated / removed.

## actionAuditResult

`POST /api3/auditor/auditResult` — batch submit audit answers.

**Request**: `data: [{ auditId, clientId, checkInTime, checkOutTime, lat, lon, products:[{ id, price, face, sold, store|remaining, available, firmBug }] }]`, plus auth fields.

**Response**: `'Success'` or 400 with exception text.

**Side effects**: opens a DB transaction; for each entry creates `Visit` (AUDIT=1, STORE_CHECK=1), `AdtAuditResult`, and `AdtAuditResultData` per product (including products NOT submitted — saved with AVAILABLE=0, OUT_OF_STOCK=0); sends `firstVisitSvr` telegram on first visit.

**Gotchas**: dedupes by `TOKEN = deviceToken + '_' + date` + `AUDIT_ID` + `CLIENT_ID` + DATE — second sync is silently skipped per audit row.

## actionPollResult

`POST /api3/auditor/pollResult` — batch submit poll answers.

**Request**: `data:[{ pollId, clientId, checkInTime, checkOutTime, lat, lon, answers:[{ questionId, variantId, value }] }]`.

**Response**: `'Success'` or 400.

**Side effects**: transactional; creates `Visit` (POLL=1), `AdtPollResult`, `AdtPollResultData`; sends `firstVisitSvr` on first visit.

**Gotchas**: 400 if `questionId` doesn't belong to `pollId`. Booleans coerced to int.

## actionCommentResult

`POST /api3/auditor/commentResult` — submit visit-reject comments.

**Request**: `data:[{ commentId, clientId, checkInTime, ... }]`.

**Response**: `'Success'` or 400.

**Side effects**: creates `AdtCommentResult` + `Visit` (REJECT=1 when no AUDIT/POLL). Dedupe by client+date+visit.

## actionNoteResult

`POST /api3/auditor/noteResult` — free-text note per visit.

**Request**: `data:[{ clientId, note, checkInTime, ... }]`.

**Side effects**: creates `AdtNoteResult` + `Visit` (REJECT=1 when no AUDIT/POLL).

## actionSetClient

`POST /api3/auditor/setClient` — create or update client(s) from the field.

**Request**: `data:[{ id (local UUID for new), name, firm_name, category, city, channel, typeId, contact_person, orient, address, form_sob, tel, lat, lon, bar_code, comment, needToAudit, visitDays:"1/3/5", agentId, agentData:[{agentId,days}], detachAgents:[], imageListToUpload:[base64] }]`.

**Response**: `{ item: { <localId>: <serverClientId> } }` — map of input ids to server PKs.

**Side effects**: writes `Client`, `ClientPhoto`, replaces `Visiting` / `VisitingAud` rows for the new day plan, writes a `SyncLog` row for offline dedupe (keyed by `DEVICE_TOKEN + DAY + MOBILE_ORDER_ID`). Hard-codes `DILER_ID = 'd0_1'` for new records.

**Gotchas**: client `id` is the **mobile-side** id; the response maps it to the server PK. Agent `agentData` is capped at 3 entries (`count($visitsToCreate) <= 3`). Resync of the same `id` returns the already-mapped server id from `SyncLog`.

## actionCheckIn

`POST /api3/auditor/checkIn` — record GPS-tracked client visit(s).

**Request**: `data:[{ clientId, checkInTime, checkOutTime, date, lat, lon, battery, provider, signal, mode, internetStatus, gpsStatus, device }]`.

**Side effects**: upserts `Visit` (VISITED=1, computes `DISTANCE` to client + `GPS_STATUS` 1/2/4/5/10), upserts one `GpsAdt` (TYPE='visit') per visit. Sends `firstVisitSvr` telegram on first visit of the day.

**Gotchas**: `GPS_STATUS` semantics — `1`=no client coords, `2`=no visit coords, `4`=client moved today, `5`=too far (>MIN_GPS_DISTANCE), `10`=success.

## actionGpsTrack

`POST /api3/auditor/gpsTrack` — bulk-push background GPS pings.

**Request**: `data:[{ timestamp, latitude, longitude, batteryLevel, carrierName, cellularLevel, networkType, networkStatus, gpsStatus, deviceName }]`.

**Side effects**: inserts `GpsAdt` rows (TYPE='track') only for pings between 08:00 and 20:00 server-local time. Outside hours = silently dropped.

## actionTaskType

`POST /api3/auditor/taskType` — directory.

**Response**: `{ taskType: [{ id, name }] }`.

## actionTask

`POST /api3/auditor/task` — list tasks where user is from or to.

**Response**: `{ task: [{ id, name, agentId, deadline (ms), clientId, photo, imageResult, status, typeId, comment }] }`.

## actionTask2

`POST /api3/auditor/task2` — same as `task` but joins user→agent and adds `taskTo`, `taskFrom`, `commentResult`.

**Response**: `{ task: [{ id, name, agentId, taskTo, taskFrom, deadline, clientId, photo, imageResult, status, typeId, comment, commentResult }] }`.

## actionSettask

`POST /api3/auditor/settask` — batch create/update tasks.

**Request**: `data:[{ id?, name, agentId, typeId, clientId, comment, commentResult?, photo (base64), imageResult (base64), date (ms), deadline (ms), status }]`.

**Response**: `'Success'` or 400.

**Side effects**: writes `Tasks`, persists images to `/upload/photoTask/<YYYYMM>/`. Tracks edits via `TaskLog` (sets `TaskLog::$user`). Dedupes new tasks by (TASK_FROM, TASK_TO, NAME, TYPE_ID, CLIENT_ID, DATE_DO, DATE_CREATE).

**Gotchas**: `agentId` is mapped to `User.USER_ID` via `Agent.AGENT_ID` lookup; unknown agents skip the row.

## actionGetDaily

`POST /api3/auditor/getDaily` — supervisor/manager daily KPI dashboard.

**Request**: `data: { date (ms) }` (defaults to today).

**Response**: `{ sale:[{category_id,name,agentId,agentName,sum,volume,count}], visit:[{agentId,agentName,planned,fact,not_planned,akb,reject,not_visited,photo}], visits:{ visit:{percent,plan_visit,plan_visited,no_plan_visit,style}, order:{…}, photo:{…}, gps:{…} } }`.

**Gotchas**: 403 if `position.ROLE ∉ [8,9]`. Each `visits.*.style` is a presentation hint `{background,color}` driven by the percent (red→green ladder).

## actionGpsVisit

`POST /api3/auditor/gpsVisit` — GPS-validated visit totals per agent.

**Request**: optional `date` (ms).

**Response**: `{ plan:[{agentId,name,plan,plan_visited,plan_gps_visited,plan_gps_no_visited,plan_gps_unknown}], no_plan:[{agentId,name,no_plan_visited,no_plan_gps_visited,no_plan_gps_unknown,no_plan_gps_no_visited}], total:{…aggregated…} }`.

**Gotchas**: 403 if role ∉ [8,9]. Empty arrays when the supervisor has no agents attached.

## actionGpsVisitBy

`POST /api3/auditor/gpsVisitBy` — drill-down for a single agent (or `agentId="all"`).

**Request**: `agentId` (string or `"all"`), `planed` (0/1), optional `date`.

**Response**: `{ column:["agent_name","date","client_name","status","note"], data:[[…]] }`.

**Gotchas**: 403 if role ∉ [8,9] or if `agentId`/`planed` missing.

## actionTotal

`POST /api3/auditor/total` — visit roll-up for THIS auditor's day.

**Request**: `date` (YYYY-MM-DD string — validated by `Distr::validateDateFormat`).

**Response**: `{ total:{plan,visited,noplan,left}, detail:[{id,name,audit,photo,poll}] }`.

**Gotchas**: filters `Visit.ROLE=11` AND `POSITION_ID=current`. Returns 403 for missing/invalid date.

## actionGetSell

`POST /api3/auditor/getSell` — agent sales by category over a date range.

**Request**: `from`, `to` (both ms epoch).

**Response**: `{ sell:[{category_id,name,agentId,agentName,sum,volume,count}] }`.

**Gotchas**: only orders with STATUS in `[2,3]` (loaded/delivered) and `DATE_LOAD` inside range. 403 if role ∉ [8,9].

## actionGetSummary

`POST /api3/auditor/getSummary` — order summary by agent over a date range.

**Request**: `from`, `to` (ms), optional `lang` (`ru`|`uz`), `status` (int[], default `[2,3]`), `bydate` (`"date"` or `"load"`, default load).

**Response**: `{ summary:{summa,volume,count,akb}, status:[{id,name}], agents:{ columns:['agentId','name','summa','volume','count','akb'], data:[[…]] } }`.

**Gotchas**: 403 if role ∉ [8,9]. Hard-codes `DILER_ID='d0_1'`. Numeric fields are stringified (rounded to 3dp).

## actionDetailSummary

`POST /api3/auditor/detailSummary` — per-order list for one agent.

**Request**: `agentId` (required, else 403), `from`, `to` (ms), optional `lang`, `status`, `bydate`.

**Response**: `{ columns:['date','dateload','client_name','count','summa','price_type','status'], status:[{id,name}], data:[[…]] }`.

**Gotchas**: 403 if role ∉ [8,9] or `agentId` empty.

## actionClientBalance

`POST /api3/auditor/clientBalance` — client balances across currencies for this supervisor's agents.

**Response**: `{ client:['clientId','name','address','avatar','territory_id','category_id','currencies'], currency:['curId','name','title','balance'], data:[[clientId,name,[ [curId,name,title,balance], … ] (json-stringified), avatar, address, territoryId, categoryId], …] }`.

**Gotchas**: 403 if role ∉ [8,9]. When `ServerSettings::isContragent()` true, reads from `Contragent` table instead of `Client`. `currencies` cell is **a JSON-encoded string**, not a nested array — clients must `JSON.parse` it.

## See also

- [api-v3-mobile overview](./)
- [Authentication](../authentication.md)
- [Error codes](../error-codes.md)
