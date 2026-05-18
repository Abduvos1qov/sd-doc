---
sidebar_position: 7
title: partner module
audience: [engineering, partners, hq-admin]
summary: Partner self-service portal. Five controllers and eight actions let users with ROLE_PARTNER see and lightly manage their assigned dealers, plus read subscription, payment, and report data scoped to the dealers they own (via Diler.SALE_ID).
topics: [sd-billing, partner, self-service, rbac, dealer]
---

# sd-billing `partner` module

The `partner` module is the self-service portal for sales partners. A partner is a billing user with `ROLE = ROLE_PARTNER`. When such a user logs in, the global `PartnerAccessService::checkAccess` filter restricts them to this module plus the `directory` module, the `dashboard/dashboard/index` landing page, and `site/*` for login and logout. Anything outside that whitelist throws `CHttpException(403)`.

The portal shows the partner only the dealers they own. Ownership is tracked by `Diler.SALE_ID` - the foreign key on the dealer row that points back to the partner's `User.USER_ID`. Every list query in this module filters on that column when `Yii::app()->user->isPartner()` is true; admin viewers see all dealers whose `SALE_ID` belongs to any partner-role user.

Five controllers, eight actions. The same kebab-case action-class pattern used elsewhere in sd-billing: controllers declare routes in `actions()` and delegate to standalone classes under `application.modules.partner.actions.*`.

## Key features

| Feature | What it does | Scoping |
|---|---|---|
| Dealer self-management | List, get, create, update a dealer assigned to the partner | `Diler.SALE_ID = current_user.USER_ID` for partners; all SALE_ID-owned dealers for admins |
| Dealer subscription view | Per-dealer subscription list rendered in the partner UI | dealer must belong to the calling partner |
| Dealer payment view | Per-dealer payment history | dealer must belong to the calling partner |
| Subscription report | Subscription roll-up across all the partner's dealers | filtered by SALE_ID joined dealers |
| Hard-coded route allowlist | Partner-role users cannot navigate outside this module + a small whitelist | enforced globally by `PartnerAccessService` |

## Folder

```
protected/modules/partner/
  controllers/
    DealerController.php          (4 routes, extends VController)
    SubscriptionController.php    (1 route + 1 inline view action)
    PaymentController.php         (1 route + 1 inline view action)
    ReportController.php          (1 route)
    ViewController.php            (2 inline view actions)
  actions/
    dealer/
      DealerListAction.php
      DealerGetAction.php
      DealerCreateAction.php
      DealerUpdateAction.php
    subscription/
      DealerSubscriptionListAction.php
    payment/
      DealerPaymentListAction.php
    report/
      SubscriptionListAction.php
  views/
    payment/dealer.php
    subscription/dealer.php
    view/dealer.php
    view/subscription.php

# Out of module but load-bearing
protected/components/PartnerAccessService.php       # global filter
protected/components/VController.php                # redirects guests to /site/login
```

`VController::init()` does one thing: if the user is a guest, redirect to `/site/login`. `DealerController` extends it; the rest extend the plain `Controller`. The `Controller` filter chain still runs `PartnerAccessService::checkAccess`, so the practical difference is just the guest redirect.

## Controllers

| Controller | Purpose | Actions | Auth |
|---|---|---|---|
| `DealerController` | Partner-scoped dealer CRUD | `list`, `get`, `create`, `update` (all via `actions()` map) | `authorize([], ['operation.partner.dealer', Access::SHOW or CREATE or UPDATE])` per action; partner-only branches by `Yii::app()->user->isPartner()` |
| `SubscriptionController` | Dealer subscription data | `dealer-subscription-list` (AJAX) + `actionDealer` (render view) | `operation.partner.dealer` SHOW |
| `PaymentController` | Dealer payment data | `dealer-payment-list` (AJAX) + `actionDealer` (render view) | `operation.partner.dealer` SHOW |
| `ReportController` | Cross-dealer report | `subscription-list` (AJAX) | `operation.partner.report.subscription` SHOW |
| `ViewController` | Render entry pages | `actionSubscription`, `actionDealer` | `Access::check('operation.partner.report.subscription' / 'operation.partner.dealer', Access::SHOW)` |

### `DealerController` routes

All four routes are POST-by-default-XHR endpoints registered in `actions()`. Each action class extends `ApiAction` and starts with `$this->authenticate()` then `$this->authorize(...)`.

| Route | Action class | Method | What it does |
|---|---|---|---|
| `list` | `DealerListAction` | GET | Returns the dealer list. Partner branch filters by `dil.SALE_ID = current_user.USER_ID`. Admin branch returns dealers whose `SALE_ID` belongs to any user with `ROLE = ROLE_PARTNER`. Result includes `user_role` so the UI can hide partner-only actions for admins |
| `get` | `DealerGetAction` | GET | One-dealer detail. Refuses unless the caller is a partner (or admin elsewhere) - `if (!$this->user->isPartner()) { ... }` is the first gate inside the action |
| `create` | `DealerCreateAction` | POST | Insert a `Diler` row with `SALE_ID = current_user.USER_ID`. Same partner-only gate |
| `update` | `DealerUpdateAction` | POST | Update fields on an existing dealer. Partner-only gate. Caller must own the dealer via `SALE_ID` |

The returned dealer row carries `id, name, host, domain, partner_name, balance, city_id, currency_id, active_to, status, credit_amount, credit_date, min_license, created_at, updated_at`. `partner_name` is the joined `User.NAME` for `SALE_ID` - useful only in the admin branch.

### `SubscriptionController` actions

| Route or action | Method | What it does |
|---|---|---|
| `dealer-subscription-list` | XHR | `DealerSubscriptionListAction`. Returns subscription rows for one dealer. Caller must own the dealer (partner branch) or be admin |
| `actionDealer` | GET | Renders `subscription/dealer.php` - the per-dealer subscription view shell |

### `PaymentController` actions

| Route or action | Method | What it does |
|---|---|---|
| `dealer-payment-list` | XHR | `DealerPaymentListAction`. Returns payment rows for one dealer. Same ownership gate |
| `actionDealer` | GET | Renders `payment/dealer.php` |

### `ReportController` actions

| Route | Method | What it does |
|---|---|---|
| `subscription-list` | XHR | `SubscriptionListAction`. Cross-dealer subscription report. Partner branch joins to `Diler` and filters on `SALE_ID = current_user`. Gated by `operation.partner.report.subscription` SHOW |

### `ViewController` actions

| Action | What it does |
|---|---|
| `actionSubscription` | Renders the partner subscription-report page shell. `Access::check('operation.partner.report.subscription', Access::SHOW)` |
| `actionDealer` | Renders the partner dealer-list page shell. `Access::check('operation.partner.dealer', Access::SHOW)` |

## Partner request flow

```mermaid
sequenceDiagram
  participant U as Partner browser
  participant Site as site/login
  participant Filt as PartnerAccessService.checkAccess
  participant V as ViewController.dealer
  participant Api as DealerController.list
  participant DB as billing DB

  U->>Site: POST credentials
  Site-->>U: cookie session
  U->>V: GET /partner/view/dealer
  V->>Filt: filter chain
  Filt-->>V: allow (module = partner)
  V-->>U: render dealer.php

  U->>Api: GET /partner/dealer/list
  Api->>Filt: filter chain
  Filt-->>Api: allow
  Api->>Api: authenticate + authorize(operation.partner.dealer, SHOW)
  Api->>DB: SELECT FROM d0_diler WHERE SALE_ID = :user_id
  DB-->>Api: rows
  Api-->>U: JSON { dealers, user_role }

  U->>Api: POST /partner/dashboard/dashboard/index (try to escape)
  Api->>Filt: filter chain
  Filt-->>U: HTTP 403 (only dashboard/dashboard/index is whitelisted; other dashboard sub-paths are denied)
```

The `PartnerAccessService::checkAccess` filter is the load-bearing piece. It checks `Yii::app()->user->getUser()->isPartner()` and then matches the current `module/controller/action` against the allowlist:

- `module === 'partner'` - allow
- `module === 'directory'` - allow
- `controllerId === 'site'` - allow
- `module === 'dashboard' && controllerId === 'dashboard' && actionId === 'index'` - allow
- anything else - throw `CHttpException(403)`

## Cross-module touchpoints

- **`access` module** owns the permission keys checked here: `operation.partner.dealer`, `operation.partner.report.subscription`. The role default for `ROLE_PARTNER` must grant SHOW on these, otherwise partners cannot use their own portal. See [access module](./access.md).
- **`directory` module** is allowlisted by `PartnerAccessService` because the partner UI needs to look up cities, currencies, distributors. Without that allowlist the dropdowns 403.
- **`dashboard` module** - only the `dashboard/dashboard/index` route is reachable. A partner clicking any other dashboard link gets HTTP 403.
- **`operation` module** owns the `Subscription`, `Payment`, `Diler` tables that this module reads from. Mutations from partner-side `DealerCreateAction` and `DealerUpdateAction` write directly to `d0_diler`. There is no operation-side validation between the two.
- **`api` module** is not used by the partner portal directly, but the dealers visible to a partner are the same `Diler` rows synced through `api/LicenseController`.

## Gotchas

- **`SALE_ID` is the only ownership key.** If `SALE_ID` is null or points to a non-partner user, the dealer never shows up in a partner list - and never shows up in the admin branch either (which filters by `SALE_ID IN (...partner users)`). New dealers added outside this module need their `SALE_ID` set explicitly.
- **The global filter was historically commented out.** See [modules overview](../modules.md) - `PartnerAccessService::checkAccess` was previously bypassed in the base controller, leaving partner-role users free to navigate the whole admin app. Verify the call site is live before depending on it.
- **`DealerCreateAction` writes `SALE_ID = current_user.USER_ID`.** An admin calling `create` on behalf of a partner still gets the admin's USER_ID stamped. To assign a dealer to a specific partner, pass `sale_id` explicitly or update post-create.
- **Subscription and payment lists trust the dealer id from the request.** The ownership check is "is the caller a partner" but not always "does the caller own dealer X". Confirm in `DealerSubscriptionListAction` and `DealerPaymentListAction` that the `dealer_id` parameter is matched against `SALE_ID` before relying on the scoping.
- **`ViewController::actionSubscription` and `actionDealer` use `Access::check`.** The AJAX controllers use `authorize` (from `ApiAction`). The two paths read the same permission keys but the failure modes differ - `Access::check` throws `CHttpException(403)`, `authorize` returns a JSON `{success: false, ...}`.
- **`DealerController` extends `VController`, the others extend `Controller`.** `VController::init` redirects guests to `/site/login`; the others rely on the filter chain. Inconsistent inheritance means guest behavior differs by URL path.
- **`directory` allowlist is broad.** A partner can read every directory the `directory` module exposes - cities, currencies, distributors, package types. If any directory exposes sensitive data via its API endpoints, partners can read it.

## See also

- [Modules overview](../modules.md) - the `partner` section explains the role and the historical filter status
- [access module](./access.md) - permission keys gated here
- [Auth and access](../auth-and-access.md) - how `ROLE_PARTNER` and `User.SALE_ID` get assigned
- [Security landmines](../security-landmines.md) - filter-bypass historical issue
- [Operation subscription workflow](../workflows/operation-subscription.md) - the source of truth for the subscription rows shown here
- [Operation payment workflow](../workflows/operation-payment.md) - same for payments
