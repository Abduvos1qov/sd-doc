---
sidebar_position: 11
title: operation · Notification rules
---

# operation · Notification rules

## 1. Purpose

The Notification rules feature lets operators author broadcast messages
that are pushed from sd-billing to each dealer's sd-main instance —
news, alerts, warnings, and polls — and lets them target the broadcast
by distributor, dealer set, currency, and role. The rule itself
(`d0_notification`) is the editable template; delivery is recorded by
`d0_notification_sent` once the message has been accepted by a dealer's
sd-main. A separate but neighbouring system (`d0_notify_cron`) is the
async outbox used by **other** sd-billing features for one-off pushes
(Telegram messages, dealer license-cache invalidation, dealer
visit-write pings). Both are described here because they are the two
faces of "notification" in sd-billing.

---

## 2. Who uses it

| Role | Access key | Capability |
|------|-----------|------------|
| Admin (`IS_ADMIN = 1`) | `operation.notification.index` | Full CRUD + send + delete-from-dealer |
| Operator (ROLE = 5) | `operation.notification.index` | CRUD + send subject to bitmask |
| Manager (ROLE = 4) | `operation.notification.index` | Typically SHOW; CRUD only if granted |

Permission is checked via `Access::check('operation.notification.index', Access::SHOW/CREATE/UPDATE/DELETE)`. The `actionPost` (broadcast to one dealer), `actionDeleteOne`, and `actionCompleted` actions inherit the controller's session auth but do not re-check the bitmask — they are meant to be called by the operator's own browser as part of the multi-dealer send loop.

---

## 3. Where it lives

| Item | Path |
|------|------|
| Controller | `protected/modules/operation/controllers/NotificationController.php` |
| Notification model | `protected/models/Notification.php` |
| NotificationSent (dealer-delivery log) | `protected/modules/operation/models/NotificationSent.php` |
| Async outbox model | `protected/models/NotifyCron.php` |
| Cron drainer | `protected/commands/NotifyCommand.php` (runs as `php cron.php notify`) |
| Distributor HTTP helper | `protected/components/Distr.php` (`Distr::sendPost`) |

URL pattern (`operation/notification`):

```
GET    /operation/notification/index           (old view)
GET    /operation/notification/indexNew        (new Vue view)
GET    /operation/notification/form            (form page; ?id=N to edit)
POST   /operation/notification/getData
POST   /operation/notification/createOrUpdate
GET    /operation/notification/send?id=N       (send-progress UI)
POST   /operation/notification/post            (POST to one dealer)
POST   /operation/notification/deleteOne       (delete from one dealer)
GET    /operation/notification/delete?id=N     (delete-progress UI)
POST   /operation/notification/delete          (mark notification deleted)
POST   /operation/notification/completed       (mark notification fully sent)
```

---

## 4. Workflow

```mermaid
sequenceDiagram
  participant U as Operator
  participant FE as Browser (Vue)
  participant C as NotificationController
  participant DB as MySQL
  participant SD as Dealer sd-main

  U->>FE: Compose notification (title, preview, content, type, audience filters)
  FE->>C: POST actionCreateOrUpdate
  C->>DB: Resolve DISTR_IDS / DILER_IDS / CURRENCIES; INSERT Notification (STATUS=NEW)
  C-->>FE: success
  U->>FE: Open send view
  FE->>C: GET actionSend?id=N
  C->>DB: Resolve target dealers via DILER_IDS filter
  C-->>FE: list of {id, dealer} pairs
  loop per dealer
    FE->>C: POST actionPost {id, dealer}
    C->>SD: Distr::sendPost(dealer.DOMAIN + "/api/notification", payload)
    SD-->>C: {success: true/false}
    alt success
      C->>DB: UPSERT NotificationSent + makeProgress (STATUS=IN_PROCESS)
    end
    C-->>FE: {success, message}
  end
  FE->>C: POST actionCompleted
  C->>DB: UPDATE Notification SET STATUS = SENT
```

### 4a. Create / edit a rule (`actionCreateOrUpdate`)

1. Operator opens `/operation/notification/form` (new) or `/operation/notification/form?id=N` (edit).
2. Browser POSTs `title`, `preview`, `content`, `type`, `auto`, optional `currencies[]`, `distributors[]`, `dealers[]`, `roles[]`.
3. Controller resolves the audience filters:
   - `CURRENCIES`: semicolon-joined currency IDs (e.g. `"1;2;5"`).
   - `DISTR_IDS`: stored **inverted** — it is the set of distributors that should *not* receive the message. The controller queries `getDistributors("WHERE ID NOT IN (…)")` against the operator-supplied exclude list and saves the resulting include-list as `DISTR_IDS`.
   - `DILER_IDS`: when any of `currencies`, `dealers`, `distributors` is supplied, the controller queries the dealer table with the combined filter (`CURRENCY_ID IN (…) AND ID NOT IN (…) AND DISTR_ID NOT IN (…)`) and stores the resulting include-list of dealer IDs. Empty `DILER_IDS` means "all".
   - `ROLES`: semicolon-joined role IDs from `Notification::getRoles()` (admin / operator / cashier / supervisor / manager / warehouseman).
4. New records get `STATUS = STATUS_NEW (1)` and `CREATED_BY`. Updates stamp `UPDATED_BY`. The save runs in a transaction.

### 4b. Send a rule (`actionSend` → loop `actionPost`)

1. Operator opens the send-progress UI; browser GETs `actionSend?id=N`, which renders a list of target dealers.
2. For each dealer the browser POSTs `actionPost {id, dealer}`.
3. The controller validates the notification and dealer exist, the dealer is `isActive()`, and `DOMAIN` is non-empty.
4. It assembles a payload (`title`, `preview`, `detail`, `type`, `auto`, `from: "billing"`, `sync: notification.ID`, `roles`) and calls `Distr::sendPost("{DOMAIN}/api/notification", $data)`.
5. On `success: true` from sd-main, it upserts a `NotificationSent` row keyed by `(notification_id, dealer_id)`, stores the raw response in `NotificationSent.response`, and calls `Notification::makeProgress()` to flip `STATUS` to `STATUS_IN_PROCESS (2)`.
6. When the operator finishes the loop, the browser POSTs `actionCompleted` which sets `STATUS = STATUS_SENT (3)`.

### 4c. Delete a rule (`actionDeleteOne` → `actionDelete`)

`actionDeleteOne` sends a `{sync: ID}` payload to `{DOMAIN}/api/notification/delete` per dealer, removes the matching `NotificationSent` row on success, and flips status back to `IN_PROCESS`. After the loop, the operator POSTs `actionDelete`, which guards against deletion if any `NotificationSent` row still exists (`anySent != null`), and otherwise calls `Notification::deleteNotify()` to soft-delete (`IS_DELETED = 1`).

### 4d. The async outbox (`d0_notify_cron` / `NotifyCommand`)

A separate, controller-less queue table is used by **other** sd-billing features (not the rule editor). Three enum types live on `NotifyCron.type`:

| Constant | Value | Producer | Consumer |
|----------|-------|----------|----------|
| `TYPE_TELEGRAM` | `'telegram'` | `NotifyCron::create()` — Telegram-message senders across the app | `NotifyCommand::sendTelegram()` — calls `Telegram::queue('sendMessage', …)` via the configured bot's `api_url` |
| `TYPE_LICENSE_DELETE` | `'license_delete'` | `NotifyCron::createLicenseDelete()` — called by `Diler::deleteLicense()` after subscription / payment writes | `NotifyCommand::sendLicenseDelete()` — GET to the URL (typically `{DOMAIN}/api/billing/license`), expects `{status: true}` |
| `TYPE_VISIT_WRITE` | `'visit_write'` | `NotifyCron::createVisitWrite()` — called by `Diler::writeVisit()` | `NotifyCommand::sendVisitWrite()` — GET to the URL (typically `{DOMAIN}/api/cronVisit/write`), expects `{status: true}` |

`NotifyCommand::run()` (invoked as `php cron.php notify`) drains rows with `status = STATUS_DEFAULT (0)`, dispatches by type, sets `status = STATUS_RUN (1)` on success, and on failure stores the failure reason in `error_response` while keeping `status = STATUS_DEFAULT` so the row is retried on the next run.

---

## 5. Rules

- `Notification.STATUS` has three values: `STATUS_NEW (1)`, `STATUS_IN_PROCESS (2)`, `STATUS_SENT (3)`. The lifecycle is `NEW → IN_PROCESS` (any dealer accepted the payload) `→ SENT` (operator confirmed completion). Soft-deleted rules carry `IS_DELETED = 1`.
- `Notification.TYPE` is one of four constants from `Notification::getTypes()`: `TYPE_NEWS (1)`, `TYPE_ALERT (2)`, `TYPE_WARNING (3)`, `TYPE_TALLY (4)` (poll).
- `DISTR_IDS` semantics on the wire are **inverted** from the UI: the user picks distributors to *exclude*, the controller computes and persists the include-list.
- `DILER_IDS` empty string = "all"; non-empty = explicit include list.
- `getDealers()` filters `STATUS = 10` (active dealers only). Inactive or deleted dealers never receive broadcasts.
- A notification cannot be hard-deleted while any `NotificationSent` row exists; the soft-delete path (`deleteNotify`) is the only allowed removal once delivery has started.
- `actionPost` requires `Diler.isActive()` AND `Diler.DOMAIN` non-empty. Dealers without a `DOMAIN` (legacy or local-only tenants) cannot receive broadcasts.
- `NotifyCron.beforeSave()` defaults `type` to `TYPE_TELEGRAM` when empty. Direct inserts that bypass `beforeSave` may write a NULL type which the cron treats as Telegram.
- `NotifyCommand` treats Telegram `ok = false` responses as **delivered** (terminal failure, no retry) — these are permanent errors like "chat not found". Transport failures (`response === false`) keep `status = STATUS_DEFAULT` for the next retry.
- `NotifyCommand` log files are written to a single shared log key (`notify-command-errors`) via `BaseCommand::writeLog`.

---

## 6. Data sources

| Table | DB / connection | Why read |
|-------|-----------------|----------|
| `d0_notification` | sd-billing default DB | Primary rule entity — list, create, update, soft-delete |
| `d0_notification_sent` | sd-billing default DB | Delivery log — keyed by `(notification_id, dealer_id)`; guards delete |
| `d0_notify_cron` | sd-billing default DB | Async outbox for `telegram`, `license_delete`, `visit_write` types |
| `d0_notify_bot` | sd-billing default DB | Telegram bot configuration (`api_url`) used by `NotifyCommand::resolveApiUrl` |
| `d0_diler` | sd-billing default DB | Target audience resolution; `DOMAIN` + `isActive()` per-dealer dispatch checks |
| `d0_distributor` | sd-billing default DB | Distributor filter; inverted-include-list resolution |
| `d0_currency` | sd-billing default DB | Currency filter |

---

## 7. Gotchas

**Two systems share the word "notification".** `Notification` (rule editor with audience targeting) and `NotifyCron` (async outbox for one-off pushes) live in different tables, models, and lifecycles. They never share rows. Do not confuse `actionCreateOrUpdate` (rule editor) with `NotifyCron::createLicenseDelete()` (back-end utility used by `Diler::deleteLicense()`).

**`DISTR_IDS` is stored as the include-list, not the exclude-list.** The UI lets the operator pick distributors to *exclude*; the controller resolves that to the complement set against the full distributor table and saves the result. A NULL `DISTR_IDS` means "no filter applied". This makes reading the stored value confusing if you assumed it mirrored the UI selection.

**Sending is operator-driven, not auto-fan-out.** Creating a notification does **not** push it to any dealer. The send loop is a separate, manually-triggered UI flow in which the operator iterates over the resolved dealer list and the browser POSTs `actionPost` once per dealer. There is no background job that delivers `STATUS_NEW` notifications.

**`actionCompleted` is a manual flip.** `STATUS = STATUS_SENT (3)` is set when the operator clicks the completion button. There is no count-based check ("all dealers received") — the status is a human marker.

**The async outbox retries forever on transport failure.** `NotifyCron` rows whose dispatch fails at the network layer keep `status = STATUS_DEFAULT` and are re-attempted on every `php cron.php notify` tick. If a dealer's `DOMAIN` is dead, the row will retry indefinitely until manually removed. The `error_response` column holds the latest failure reason for diagnosis.

**`TYPE_LICENSE_DELETE` and `TYPE_VISIT_WRITE` reuse the `text` column as the target URL.** Both bypass `chat_id` and `bot_id` entirely and `text` is interpreted as a full URL. The `Telegram::queue` path is only used for `TYPE_TELEGRAM`.

---

## 8. See also

- [Subscription lifecycle](./operation-subscription.md) — calls `Diler::deleteLicense()` after writes, which enqueues a `TYPE_LICENSE_DELETE` row in the outbox.
- [Payment recording](./operation-payment.md) — also enqueues `TYPE_LICENSE_DELETE` rows on successful payment save.
- [License push to sd-main](./license-push.md) — the consumer side of the `TYPE_LICENSE_DELETE` enqueue.
- [Cron & settlement](../cron-and-settlement.md) — the `notify` cron command and the full schedule of background tasks.
- Source: `protected/modules/operation/controllers/NotificationController.php`, `protected/models/NotifyCron.php`, `protected/commands/NotifyCommand.php`
