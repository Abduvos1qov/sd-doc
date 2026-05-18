---
sidebar_position: 9
title: sd-billing — RBAC reference
audience: [engineering, qa, ops]
summary: Complete role catalog, operation strings, cashbox/country scopes, and the matrix of who can do what in sd-billing.
topics: [security, rbac, sd-billing, roles, access-control]
---

# sd-billing — RBAC reference

This page is the authoritative reference for **roles, permissions, and scope rules** in the **sd-billing** codebase. Everything here is sourced directly from the live PHP — no inference, no guessing.

## How RBAC works in sd-billing

sd-billing uses a **three-layer model**:

1. **Role constant** — every user has a single `ROLE` column on `tbl_user`, with values matching constants on `User.php` (e.g. `ROLE_ADMIN = 3`).
2. **Operation grant** — for non-admin roles, a per-user grant lives in `tbl_access_users` keyed by `(user_id, operations)` with a bitmask `access` column (SHOW=4, CREATE=1, UPDATE=2, DELETE=8). Operations are dotted strings such as `operation.dealer.payment`.
3. **Scope flags** — orthogonal boolean/relational restrictions on top of the role: `ACCESS_CASHBOX` (cashbox-all-or-own), and `tbl_user_country` (country whitelist for managers/sales/key-account).

### Source of truth

| Layer | File | What's in it |
| --- | --- | --- |
| Role constants | `protected/models/User.php` | `ROLE_ADMIN = 3` … `ROLE_PARTNER = 10` |
| Role hierarchy (legacy Yii AuthManager, mostly unused at runtime) | `protected/config/auth.php` | Yii `CAuthItem` tree, present but the runtime checks bypass it |
| Permission check | `protected/components/Access.php` | `Access::check`, `Access::has`, `Access::like`, `Access::operation` |
| Per-user grants table | `tbl_access_users` (via `AccessUser` model) | `(user_id, operations, access)` rows |
| Operation catalogue | `tbl_access_operations` (via `AccessOperation` model) | List of operation strings shown in the UI |
| User-side wrapper | `protected/components/WebUser.php` | `isAdmin()`, `isManager()`, `isSale()`, `isPartner()`, `accessAllCashbox()` |
| Country scope rows | `tbl_user_country` (via `UserCountry` model) | Per-user country allowlist used by `User::getCountryIds()` |

### How `Access::check` resolves

`Access::check($operation, $type_access)` in `protected/components/Access.php`:

1. If `Yii::app()->user->isGuest` → return `false` (and the wrapper throws 403).
2. If `Yii::app()->user->isAdmin()` → return `true`. **Admin always wins.**
3. Otherwise look up `(user_id, operations)` in `tbl_access_users` and AND the stored access bitmask with the requested action.

So **the role determines whether the per-user grant table is consulted at all**: admins skip it entirely; everyone else needs an explicit row.

```php
const DELETE = 8;   // 1000
const SHOW   = 4;   // 0100
const UPDATE = 2;   // 0010
const CREATE = 1;   // 0001
```

The bitmask is stored as a single integer per `(user_id, operation)` row, so a value of `7` means SHOW+UPDATE+CREATE.

## Role catalog

There are **8 production roles** plus two legacy super-admin tiers that appear only in `auth.php` (`1` Super Administrator, `2` Administrator Filial — these are not used by the runtime checks, only by `isSuperAdmin()` which reads `IS_ADMIN` from the user row).

### ROLE_ADMIN (id 3)

- **Label**: "Администратор"
- **Source**: `User::ROLE_ADMIN = 3`, `User::isAdmin()`.
- **Power**: bypasses every `Access::check`. The first thing `Access::has`, `Access::like`, and `Access::operation` all do is `if (Yii::app()->user->isAdmin()) return true;`.
- **Cashbox scope**: all cashboxes (the `accessAllCashbox()` check is also bypassed because admins see everything via the access-bypass paths).
- **Country scope**: none — admins see all countries (see `BlacklistListAction::getCountryIds()` and `DealerListAction::getCountries()` which short-circuit on `isAdmin`).
- **Module access**: every module. UI affordances also unhide for admins (search the views for `Yii::app()->user->isAdmin()` — over 40 hits).

### ROLE_MANAGER (id 4)

- **Label**: "Менеджер"
- **Source**: `User::ROLE_MANAGER = 4`, `User::isManager()`.
- **Cashbox scope**: only own cashbox unless `ACCESS_CASHBOX = 1` flag is set. See `WebUser::getCashbox()` — if `accessAllCashbox()` returns true, the condition drops the `USER_ID = X` filter.
- **Country scope**: limited to the country IDs in `tbl_user_country`. Methods that consume this: `User::getCountryIds()`, then `DealerListAction::getCountries()`, `BlacklistListAction::getCountryIds()`, etc.
- **Module access**: dashboard, dealer, payment, subscription, report (subset), bonus (subset). Everything else needs an explicit grant.

### ROLE_OPERATOR (id 5)

- **Label**: "Оператор"
- **Source**: `User::ROLE_OPERATOR = 5`.
- **Cashbox scope**: own cashbox only (the `ACCESS_CASHBOX` flag flips this same as for manager).
- **Country scope**: same country-restriction model as manager — controlled by `tbl_user_country` rows.
- **Module access**: cashbox operations and payment by default. Reports require explicit grants.

### ROLE_API (id 6)

- **Label**: "API"
- **Source**: `User::ROLE_API = 6`.
- **Note**: not a human role — these users authenticate via token (`User::generateToken`, `TOKEN` column) and exist to feed external integrations. They live outside the `Access` check pathway because most API endpoints check the token, not the role.
- **Notable usage**: `DealerController` filters out `ROLE_API` users from salesman lists; `FixController` uses `ROLE_API` and `ROLE_ADMIN` constants in raw SQL to gate fix operations.

### ROLE_SALE (id 7)

- **Label**: "Продавец"
- **Source**: `User::ROLE_SALE = 7`, `User::isSale()`.
- **Cashbox scope**: own cashbox only.
- **Country scope**: limited via `tbl_user_country`.
- **Module access**: their own dealers (the `salesman` SQL pattern, see `DilerController` and `DealerController::actionIndex`). When a sale user creates a dealer, the dealer is auto-assigned to them (`DilerController:287`: `if (Yii::app()->user->isSale() && $model->isNewRecord) ...`).
- **Visibility rule in salesman lists**: queries explicitly include `ROLE = :role_sale` so sales appear in the dropdown of "assign salesman".

### ROLE_MENTOR (id 8)

- **Label**: "Ментор"
- **Source**: `User::ROLE_MENTOR = 8`.
- **Inherits from**: in `auth.php`, role `8` is a child of role `7` (Sale). Practically: mentor-specific gates check `ROLE != User::ROLE_MENTOR` in `MentorController::actionIndex`, `actionView`, `actionUpdate` (`/protected/modules/bonus/controllers/MentorController.php:140,196,250`).
- **Module access**: bonus (mentor KPI views), reports they were granted.
- **Cashbox scope**: own cashbox unless `ACCESS_CASHBOX`.
- **Country scope**: `tbl_user_country` rows.

### ROLE_KEY_ACCOUNT (id 9)

- **Label**: "Ключевой менеджер"
- **Source**: `User::ROLE_KEY_ACCOUNT = 9`.
- **Inherits from**: in `auth.php` role `9` is a child of role `4` (Manager).
- **Cashbox scope**: own cashbox unless `ACCESS_CASHBOX`.
- **Country scope**: filtered via `tbl_user_country`; queries that build salesman dropdowns include `ROLE = :role_key_account` so key accounts show up alongside sales (see `DealerController:97`).
- **Module access**: dealer (their assigned dealers), `report.key_account` specifically, plus standard manager-level reports they are granted.

### ROLE_PARTNER (id 10)

- **Label**: "Партнер"
- **Source**: `User::ROLE_PARTNER = 10`, `User::isPartner()`.
- **Cashbox scope**: own cashbox only.
- **Country scope**: limited via `tbl_user_country`.
- **Module access**: only the `partner/*` module (dealer list, subscription report, payment list).
- **Hard gates in partner module**: `DealerCreateAction`, `DealerUpdateAction`, `DealerGetAction` all start with `if (!$this->user->isPartner()) { throw new CHttpException(403); }` — these endpoints explicitly **require** partner role rather than checking an operation grant. `PartnerAccessService::filter()` further scopes partner queries to their own dealer assignments.

### Legacy super-admin tiers (IS_ADMIN column)

- `IS_ADMIN = 1` on the user row triggers `User::isSuperAdmin()`. This is **not a separate ROLE value** — it's an orthogonal flag, and several places check `isAdmin() || isSuperAdmin()` together (e.g. `BlacklistListAction:87`, `DealerListAction:30`, `DealerCreateAction:214`, `DealerUpdateAction:237`, `SubscriptionListAction:126`).
- The Yii AuthManager tree in `auth.php` still names roles `1` (Super Administrator) and `2` (Administrator Filial) but these IDs do not correspond to runtime `ROLE` values; they are legacy from when `CAuthManager` was used and remain orphaned.

## Scope semantics

### Cashbox scope — `ACCESS_CASHBOX` flag

`User.php:119`:

```php
public function accessAllCashbox()
{
    return $this->ACCESS_CASHBOX == 1;
}
```

`WebUser::getCashbox()` (`components/WebUser.php:91`) builds the cashbox list:

- Default condition: `IS_DELETED = 0 AND USER_ID = <currentUserId>` (own cashbox only).
- If `accessAllCashbox()` is true: condition drops the `USER_ID = X` filter, so the user sees **every** non-deleted cashbox.

**The flag bypasses role-based cashbox isolation entirely.** It's a per-user override that lets you give one operator full cashbox visibility without changing their role. There is no per-cashbox grant — it's binary.

Cashbox-CRUD controllers (`Cashbox`, `CashDesk`, `Transfer`, `FlowType`, `ComingType`, `Consumption`) are wrapped in `accessRules() { roles => array(3) }` — i.e. only role 3 (admin) can manage cashbox definitions. The `ACCESS_CASHBOX` flag controls **operating** scope, not configuration.

### Country scope — `tbl_user_country`

`User::getCountryIds()` returns the country IDs for the current user from `tbl_user_country`. The pattern across actions:

```php
private function getCountryIds()
{
    if (Yii::app()->user->isAdmin() || Yii::app()->user->isSuperAdmin()) {
        return null; // means "no filter"
    }
    return $user->getCountryIds();
}
```

Found verbatim in `BlacklistListAction.php:87`, `DealerCreateAction.php:214`, `DealerUpdateAction.php:237`, `SubscriptionListAction.php:159`. **If you add a new manager/sale/key-account-visible report, copy this pattern.**

Practical implications:

- A manager with no rows in `tbl_user_country` sees **no dealers**, not all dealers. The empty array is treated as "your scope is empty", not "no restriction".
- Admin/super-admin always sees all countries (no filter applied).
- Partners are filtered through `PartnerAccessService` instead — they see only dealers they created.

### Per-cashbox isolation pattern in queries

Operator/manager/sale cashbox queries typically join on `USER_ID = :currentUserId` unless `accessAllCashbox()` returns true. **There is no `cashbox.id IN (allowed list)` mechanism** — it's all-or-own.

## Operations × roles matrix

Operation strings extracted by `grep -roE 'Access::(check|has|like)\([^,)]+' protected/modules/`. Every row is a real string used in the codebase. Columns marked "grant" mean the role must have an explicit row in `tbl_access_users` with the appropriate bitmask. "auto" means the action is reachable without a grant (admin bypass, or the controller hard-codes the role check elsewhere).

Legend: A = Admin (auto), M = Manager, O = Operator, S = Sale, KA = Key Account, ME = Mentor, P = Partner, API = API.

| Operation | A | M | O | S | KA | ME | P | API | Module |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `operation.access.index` | auto | grant | grant | grant | grant | grant | n/a | n/a | access |
| `operation.dealer.index` | auto | grant | grant | grant | grant | grant | n/a | n/a | dashboard |
| `operation.dealer.payment` | auto | grant | grant | grant | grant | grant | n/a | n/a | operation/payment |
| `operation.dealer.subscription` | auto | grant | grant | grant | grant | grant | n/a | n/a | dashboard/subscrip |
| `operation.dealer.settlement` | auto | grant | grant | grant | grant | grant | n/a | n/a | dashboard |
| `operation.dealer.package.index` | auto | grant | grant | grant | grant | grant | n/a | n/a | operation/relation |
| `operation.dealer.blacklist` | auto | grant | grant | grant | grant | grant | n/a | n/a | operation/view |
| `operation.dealer.change.creditdate` | auto | grant | grant | grant | grant | grant | n/a | n/a | dashboard |
| `operation.dealer.change.sales` | auto | grant | grant | grant | grant | grant | n/a | n/a | dashboard |
| `operation.dealer.contact` | auto | grant | grant | grant | grant | grant | n/a | n/a | dashboard |
| `operation.dealer.creditdate` | auto | grant | grant | grant | grant | grant | n/a | n/a | dashboard |
| `operation.dealer.creditsumma` | auto | grant | grant | grant | grant | grant | n/a | n/a | dashboard |
| `operation.dealer.min.license` | auto | grant | grant | grant | grant | grant | n/a | n/a | dashboard |
| `operation.dealer.min.summa` | auto | grant | grant | grant | grant | grant | n/a | n/a | dashboard |
| `operation.dealer.monthly` | auto | grant | grant | grant | grant | grant | n/a | n/a | dashboard |
| `operation.package.index` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | operation/package |
| `operation.package.smpro` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | operation |
| `operation.subscription.smpro` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | operation |
| `operation.tariff.index` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | operation/view |
| `operation.partner.dealer` | auto | n/a | n/a | n/a | n/a | n/a | hard-role | n/a | partner |
| `operation.partner.report.subscription` | auto | n/a | n/a | n/a | n/a | n/a | hard-role | n/a | partner |
| `operation.notification.index` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | notification |
| `operation.tally.index` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | notification |
| `operation.bonus.index3` | auto | grant | n/a | grant | grant | grant | n/a | n/a | bonus |
| `operation.bonus.plansales` | auto | grant | n/a | grant | grant | grant | n/a | n/a | bonus/plansales |
| `operation.bonus.quarters` | auto | grant | n/a | grant | grant | grant | n/a | n/a | bonus/quarters |
| `operation.bonus.team` | auto | grant | n/a | grant | grant | grant | n/a | n/a | bonus/team |
| `operation.month.mentor` | auto | grant | n/a | n/a | n/a | hard-role | n/a | n/a | bonus/mentor |
| `operation.kpi.leader` | auto | grant | n/a | grant | grant | n/a | n/a | n/a | bonus/kpileader |
| `operation.report.active.customers` | auto | grant | n/a | grant | grant | grant | n/a | n/a | report |
| `operation.report.churn.index` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | report |
| `operation.report.churn.detail` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | report |
| `operation.report.client.report` | auto | grant | n/a | grant | grant | grant | n/a | n/a | report |
| `operation.report.clients.by.packages` | auto | grant | n/a | grant | grant | n/a | n/a | n/a | report |
| `operation.report.count` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | report |
| `operation.report.dealer.report` | auto | grant | n/a | grant | grant | grant | n/a | n/a | report |
| `operation.report.debt.detail` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | report |
| `operation.report.debt.month` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | report |
| `operation.report.debt.cashlasss` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | report |
| `operation.report.detail.bydiler` | auto | grant | n/a | grant | grant | n/a | n/a | n/a | report |
| `operation.report.key_account` | auto | grant | n/a | n/a | hard-role | n/a | n/a | n/a | report |
| `operation.report.pivot` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | report |
| `operation.report.plan.sales` | auto | grant | n/a | grant | grant | n/a | n/a | n/a | report |
| `operation.report.region` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | report |
| `operation.report.summa` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | report |
| `operation.report.statistic.potential-churn` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | report |
| `opreation.report.tactical-up-sell` (sic) | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | report |
| `report.tgBot.index` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | report |
| `operation.chart.index` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | dashboard/chart |
| `operation.chart.table` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | dashboard/chart |
| `operation.revenue.index` | auto | grant | n/a | n/a | grant | n/a | n/a | n/a | dashboard/revenue |
| `operation.dashboard.fixBalance` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | dashboard |
| `operation.dashboard.fixBalances` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | dashboard |
| `operation.distributor.distribute` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | dashboard/distr |
| `operation.distributor.revise` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | dashboard/distr |
| `operation.distr.payment` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | dashboard/distr |
| `operation.fix.index` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | dashboard/fix |
| `operation.fix.run` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | dashboard/fix |
| `operation.fix.run.action` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | dashboard/fix |
| `operation.fix.add.operation` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | dashboard/fix |
| `operation.fix.add.types` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | dashboard/fix |
| `operation.fix.check.server` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | dashboard/fix |
| `operation.fix.check.server.status` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | dashboard/fix |
| `operation.fix.give.discount` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | dashboard/fix |
| `operation.fix.remove.billing.access` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | dashboard/fix |
| `operation.fix.write.server` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | dashboard/fix |
| `operation.fix.write.visit` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | dashboard/fix |
| `operation.server.index` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | dashboard/server |
| `operation.setting.city` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | setting |
| `operation.setting.classification` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | setting |
| `operation.setting.country` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | setting |
| `operation.setting.currency` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | setting |
| `operation.setting.cause` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | setting |
| `operation.setting.systemlog` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | setting |
| `operation.setting.user` | auto | grant | n/a | n/a | n/a | n/a | n/a | n/a | setting |

Notes on the matrix:

- "auto" = `Access::has` short-circuits to `true` because of the `isAdmin()` early-return.
- "grant" = the role is technically permitted to perform the operation **if and only if** the per-user grant row in `tbl_access_users` carries the right bit. In other words: the role is the gating layer above; the grant is the gating layer below.
- "hard-role" = the controller/action bypasses the operation grant and checks the role directly (e.g. `if (!$this->user->isPartner()) throw 403` in partner actions; `ROLE != User::ROLE_MENTOR` in `MentorController`).
- "n/a" = the role typically wouldn't have this in their UI menu and there's no recorded grant pattern for it.
- Operator (role 5) shows mostly "n/a" because operators are scoped to cashbox/payment work and most other operations aren't granted to them in practice. They **can** be granted if an admin checks the box in the access UI.

## Gotchas

### 1. Admin bypass is total and very early

`Access::has`, `Access::like`, `Access::operation`, and `Access::check` all start with the same check:

```php
if (Yii::app()->user->isAdmin()) {
    return true;
}
```

This means **no operation row in `tbl_access_users` is ever consulted for admins**. If you write a regression test for access control, use a non-admin user — testing with an admin will pass everything regardless of grants.

### 2. `ACCESS_CASHBOX` is a single-bit override

A user with `ROLE = ROLE_OPERATOR` and `ACCESS_CASHBOX = 1` will see all cashboxes, but their reports, dealer lists, and other queries still respect their role. The flag only affects `WebUser::getCashbox()`. Don't confuse "operator with cashbox-all" with "admin-lite".

### 3. The country whitelist is closed-by-default for non-admins

`User::getCountryIds()` returns an empty array if the user has no `tbl_user_country` rows. Many actions then use this array directly in an `IN (...)` clause. Some implementations of the country-filter pattern produce a SQL syntax error or `WHERE ... IN ()` (always false) when the array is empty — meaning a non-admin user with no countries assigned will see **nothing**, not "everything". Always set at least one country row when provisioning a manager/sale/key-account.

### 4. `auth.php` is misleading

The Yii `CAuthManager` tree in `protected/config/auth.php` looks like a clean role hierarchy with proper inheritance. **It is not consulted by the runtime access checks.** The actual gate is `Access::operation()` reading `tbl_access_users`. The tree exists for the legacy `CWebUser::checkAccess()` mechanism and a few accessRules in old controllers.

### 5. `IS_ADMIN` is independent of `ROLE`

A user can have `ROLE = ROLE_MANAGER` and `IS_ADMIN = 1`. In that case `isAdmin()` returns false (it checks `ROLE`) but `isSuperAdmin()` returns true. The compound check `isAdmin() || isSuperAdmin()` is used in over a dozen places — make sure you use that pattern when you want "any admin variant", not just `isAdmin()`.

### 6. accessRules on cashbox controllers hard-code `array(3)`

Controllers under `protected/modules/cashbox/controllers/` (`Cashbox`, `CashDesk`, `Transfer`, `FlowType`, `ComingType`, `Consumption`) use the legacy Yii `accessRules()` with `'roles' => array(3)` instead of `Access::check`. This means:

- Only `ROLE = 3` (admin) can reach those controllers; the operation grant table is irrelevant here.
- These checks bypass `Access::has` entirely, so you can't grant a non-admin cashbox-config access via the per-user grant UI.

### 7. Operator + `ACCESS_CASHBOX = 1` does **not** equal admin for cashbox ops

Even if an operator has `ACCESS_CASHBOX = 1`, they cannot reach `cashbox/cashbox/create`, `cashbox/transfer/*`, or `cashbox/flowType/*` — those are gated by `accessRules() roles => array(3)` (admin only). The flag only affects which cashboxes show up in selectors and reports.

### 8. Partner actions bypass operation grants

The partner module checks `if (!$this->user->isPartner()) throw 403` at the top of action methods rather than calling `Access::check`. This means:

- A grant of `operation.partner.dealer` to a non-partner user **does nothing** — they still hit the role check first.
- Admins bypass everything, so admins can still call partner endpoints (this is intentional for support).

### 9. Mentor role is enforced both ways

`MentorController` checks `if ($mentor->ROLE != User::ROLE_MENTOR)` on the **target** user being viewed/updated, not the acting user. So a manager can view the mentor view of a mentor, but cannot view it of a non-mentor. The acting-user check is `Access::check('operation.month.mentor', Access::SHOW)`.

### 10. `Access::like` does prefix matching with SQL `LIKE`

`Access::like('operation.report')` returns true if the user has any grant whose `operations LIKE 'operation.report%'`. Useful for "show the Reports menu if user has any report at all", but it does a raw string interpolation (`'{$operation}%'`) — never pass user input to it. The codebase only ever passes static prefixes.

## See also

- [/docs/sd-billing/modules/access](/docs/sd-billing/modules/access) — the access-management UI and how grants are edited.
- [/docs/sd-billing/auth-and-access](/docs/sd-billing/auth-and-access) — login flow, sessions, token-based API auth.
- [/docs/sd-billing/workflows/operation-payment](/docs/sd-billing/workflows/operation-payment) — concrete example of how `Access::check('operation.dealer.payment', Access::*)` gates the four CRUD verbs in one controller.
- [/docs/security/rbac](/docs/security/rbac) — cross-project RBAC overview.
- [/docs/security/data-isolation](/docs/security/data-isolation) — how country/dealer/filial scoping interacts with role-based access across the three projects.
