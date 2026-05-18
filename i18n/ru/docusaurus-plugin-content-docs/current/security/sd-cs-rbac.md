---
sidebar_position: 10
title: sd-cs — RBAC reference
audience: [engineering, qa, ops]
summary: Role catalog, operation strings, filial scoping, and the matrix of who can do what in sd-cs.
topics: [security, rbac, sd-cs, roles, access-control, multi-db]
---

# sd-cs — RBAC reference

This page is the authoritative reference for **roles, permissions, and scope rules** in the **sd-cs** codebase. All facts here are pulled directly from the PHP source under `sd-cs/protected/`.

## How RBAC works in sd-cs

sd-cs is a **head-office (HQ) aggregator** that talks to per-tenant filial databases. RBAC has two distinct surfaces:

1. **HQ-side**: the `cs_user` table holds HQ users (Admin/Manager/Operator). Permission grants live in `cs_access_role` (per role) and `cs_access_user` (per user). All access checks go through `AccessManager::hasAccess($operation)` in `protected/modules/user/components/AccessManager.php`.
2. **Filial-side** (downstream): each filial database has its own `tbl_user` with filial-side roles (5 = Operator, 9 = Manager). The HQ user is **mirrored** into each filial DB when filial assignments are made (`User::beforeSave` propagates the login as `cs3_<login>` into every assigned filial's `tbl_user`).

The HQ user is the operator of the docs page. The filial-side role is a separate mechanism used by the filial database when sd-cs queries are routed through `setFilial($prefix)`.

### Source of truth

| Layer | File | What's in it |
| --- | --- | --- |
| HQ role constants | `protected/modules/user/models/User.php` | `ROLE_ADMIN = 1`, `ROLE_MANAGER = 2`, `ROLE_OPERATOR = 3` |
| HQ permission check | `protected/modules/user/components/AccessManager.php` | `hasAccess($operation)`, plus the static `$accesses` operation catalogue |
| HQ user wrapper | `protected/modules/user/components/WebUser.php` | `isAdmin()` against `User::ROLE_ADMIN` |
| Per-role grant table | `cs_access_role` (via `AccessRole` model) | `(role, name, access)` |
| Per-user grant table | `cs_access_user` (via `AccessUser` model) | `(user_id, name, access)` |
| Filial allowlist | `cs_user_filial` (via `UserFilial` model) | `(user_id, filial_id)` — which filials this HQ user can see |
| Filial-side mirrored user | `tbl_user` in the dealer DB (via `FilialUser`) | login `cs3_<original_login>`, role 5/6/8/9 |
| Filial-side role catalogue | `FilialUser::getRoles()` | `5 => 'Оператор', 9 => 'Менеджер'` |
| Cross-project entry point for filial CRUD | `User::setFilialRole(FilialUser, Filial)` | maps filial-side roles to `authassignment` `itemname` strings |

There is **no `auth.php`** in `protected/config/` for sd-cs — only `console.php`, `db.php`, `db_sample.php`, `main.php`, `test.php`. The access system is fully driven by the `cs_access_role` / `cs_access_user` tables and the static operation catalogue in `AccessManager`.

### How `AccessManager::hasAccess` resolves

`AccessManager::hasAccess($operation)` in `protected/modules/user/components/AccessManager.php`:

1. If `Yii::app()->user->isAdmin()` → return `true`. **Admin bypasses every check.**
2. Lazy-load all grants on first call:
   - Fetch all `cs_access_role` rows where `role = currentUser->role`.
   - Fetch all `cs_access_user` rows where `user_id = currentUser->id` — these **override** role grants for the same operation name.
3. Return `!empty($this->_access[$operation])`.

In other words: there are **two grant layers** stacked. Role grants apply to everyone with that role; user grants override (because they're loaded second and overwrite the same array key). This is unlike sd-billing, which only has per-user grants.

### How operations are derived from URLs

In `protected/components/Controller.php::beforeAction`:

```php
$path = [$module, $this->id, $action->id];
if (!Yii::app()->accessManager->hasAccess(implode('.', $path))) {
    throw new CHttpException(403, "Access Denied");
}
```

So the operation string is **`<module>.<controller>.<action>`** — e.g. visiting `/report/sell/index` maps to operation `report.sell.index`. If the module is empty (top-level controllers), it becomes `<controller>.<action>`.

This is auto-derived from URL routing, **not** from `Access::check(...)` calls in the controller body. There are zero `Access::check` calls in sd-cs controllers — the gate runs entirely in the base controller's `beforeAction`.

## Role catalog

There are **3 HQ roles** plus a parallel set of **filial-side roles** that live in the dealer databases.

### ROLE_ADMIN (id 1)

- **Label**: not in `getRoles()` — admin is hidden from the dropdown when assigning roles. See `User::rules()`: the `role` field is restricted to `array_keys(getRoles())` (which only contains 2 and 3) plus `[1]` only if the current user is already role 1.
- **Source**: `User::ROLE_ADMIN = 1`, `WebUser::isAdmin()`.
- **Power**: bypasses `AccessManager::hasAccess` (first-line early return). Bypasses the country/filial scope in many places (`User::redPriceTypes()`, several controllers check `if (!Yii::app()->user->isAdmin())` before applying filters).
- **Filial scope**: sees all filials. The HQ user gets mirrored into every filial with role `9` (Manager) when assigned — see `User::beforeSave` and the special branch `if ($this->role == self::ROLE_MANAGER) { ... StructureFilial::ROLE = 9 ... }`.

### ROLE_MANAGER (id 2)

- **Label**: "Менеджер" (from `User::getRoles()`).
- **Source**: `User::ROLE_MANAGER = 2`.
- **Filial scope**: limited to `cs_user_filial` rows for this user. Cross-filial visibility is **only what's in their UserFilial allowlist**.
- **Filial-side mirroring**: when a Manager is assigned to a filial, the filial-side login `cs3_<login>` is created with `ROLE = $this->filial_role ?: 5` (defaults to Operator on the filial side unless `filial_role` is explicitly set). Additionally, a `StructureFilial` row is inserted with `ROLE = 9` so that HQ managers appear in the filial's structure tree.
- **Permission scope**: whatever is in `cs_access_role` for `role = 2` plus per-user overrides in `cs_access_user`.

### ROLE_OPERATOR (id 3)

- **Label**: "Оператор".
- **Source**: `User::ROLE_OPERATOR = 3`.
- **Filial scope**: same `cs_user_filial` model as Manager.
- **Filial-side mirroring**: created in the filial DB with `ROLE = 5` (filial Operator) by default. No structure-tree entry is added (that's manager-only).
- **Permission scope**: whatever is in `cs_access_role` for `role = 3` plus per-user overrides.

### Filial-side roles (downstream `tbl_user.ROLE`)

These exist **inside each filial database**, not in the HQ database. They show up when sd-cs reaches into a filial via `FilialUser::model()->setFilial($prefix)`.

| Filial role id | Label | Used as |
| --- | --- | --- |
| 5 | Оператор | default for HQ users mirrored without filial_role override |
| 6 | Касса (Kassir) | financial operator |
| 8 | Супервайзер (SVR) | territory supervisor |
| 9 | Менеджер | HQ-manager-mirrored row, also natural filial managers |

`User::setFilialRole()` maps filial-side role IDs to `authassignment` `itemname` strings:

```php
$roles = [
    5 => 'role.operator',
    6 => 'role.kassir',
    8 => 'role.svr',
    9 => 'role.manager',
];
```

And then walks `authitemchild` to find the operations child-of `role.<x>`. **This is the dealer DB's own Yii CAuthManager** — sd-cs reads it as a remote permission tree to know what the filial-side user can do.

The runtime check in the sd-cs HQ application does **not** look at this; it's only consulted when sd-cs writes to `authassignment` in the filial DB during user provisioning.

### `IS_ADMIN`-style flags

sd-cs does not have a separate `IS_ADMIN`-like column on `cs_user`. The only admin tier is `ROLE_ADMIN = 1`. `WebUser::isAdmin()` simply checks `$this->profile->role == User::ROLE_ADMIN`.

## Scope semantics

### Cross-filial visibility — `cs_user_filial`

`UserFilial` rows define which dealer/filial databases an HQ user can pivot into.

- **Admin**: implicitly all filials (no filter applied in `AccessManager`, and admin-bypass paths in most controllers).
- **Manager/Operator**: only filials in their `cs_user_filial` rows.
- **Cross-filial aggregator pages** (anything in `pivot/*` and `report/*`) iterate over the user's filial list and run the same query in each filial DB, then aggregate. A non-admin with zero `cs_user_filial` rows sees **empty aggregates**.

The provisioning UI is `protected/modules/user/controllers/DefaultController.php`. When you check filials for a user there, rows are inserted into `cs_user_filial` and matching filial-side `tbl_user` records get created via `User::beforeSave`. Removing a filial assignment in the HQ user form **does not** delete the filial-side user — it stays in the filial DB as an orphaned `cs3_<login>` row.

### Country scoping in sd-cs

There is a `setCountry` flag on the base controller (default `true`) that calls `BaseModel::setCountry($this->data['current_country_id'])`. This is a session-scoped filter, not a permission. It doesn't restrict what the user can do; it just filters which country's data they're currently viewing. Country toggles live in the topbar dropdown.

### `allowedActions` — the report-controller bypass

This is the **single biggest gotcha** in sd-cs. Look at `protected/modules/report/controllers/SellController.php`:

```php
public $allowedActions = ['getData', 'getClients', 'getStore', 'getProducts',
                         'export', 'exportProducts', 'getFilials'];
```

And in the base controller `protected/components/Controller.php`:

```php
if ($this->checkAccess && !in_array($action->id, $this->allowedActions)) {
    // ... build $path, call hasAccess
}
```

Translation: **any action in `allowedActions` skips the permission check entirely**. The intent is "the index action is gated by `report.sell.index`, but once a user has loaded the page, the JSON sub-endpoints that the page calls (`getData`, `export`, etc.) shouldn't re-check". In practice, this is **gate-by-page**, not gate-by-action: if a user can guess the JSON endpoint URL, they can call it without holding the corresponding grant — as long as they're logged in.

Mitigations applied unevenly across controllers:

- `AkbController::actionGetData` adds `if (!Yii::app()->user->isAdmin()) { ... filter to user's filials ... }`.
- `PhotoController::actionGetData` and `PlanProductController` do the same.
- Most other report controllers do **not** add a defense-in-depth role check inside the action — they rely on `allowedActions` covering only the actions whose data is filtered by filial in any case.

When auditing, treat every `allowedActions` entry as **session-authenticated only, not permission-gated**.

## Operations × roles matrix

Operation strings sourced from `AccessManager::$accesses` (the canonical catalogue) and from the route-derivation pattern `<module>.<controller>.<action>`. Columns: A = Admin (auto-pass), M = Manager (id 2), O = Operator (id 3). Filial-side roles aren't in this matrix because they live in a different DB.

| Operation | Label | A | M | O |
| --- | --- | --- | --- | --- |
| `dashboard.daily.index` | Dashboard | auto | grant | grant |
| `user.default.index` | User list | auto | grant | n/a |
| `user.default.create` | Create user | auto | grant | n/a |
| `user.default.update` | Edit user | auto | grant | n/a |
| `user.default.delete` | Delete user | auto | grant | n/a |
| `report.sell.index` | Sales report | auto | grant | grant |
| `report.store.index` | Stock report | auto | grant | grant |
| `report.store.daily` | Daily stock | auto | grant | grant |
| `report.okb.index` | OKB | auto | grant | n/a |
| `report.akb.index` | AKB | auto | grant | n/a |
| `report.akbCategory.index` | AKB by category | auto | grant | n/a |
| `report.debt.index` | Receivables | auto | grant | grant |
| `report.inventory.index` | Inventory | auto | grant | n/a |
| `report.inventory.scan` | Inventory scan | auto | grant | n/a |
| `report.bonus.index` | Bonus detail | auto | grant | n/a |
| `report.summaryBonus.index` | Bonus summary | auto | grant | n/a |
| `report.bonusSale.index` | Bonus-sale | auto | grant | n/a |
| `report.plan.index` | Plan | auto | grant | grant |
| `report.stock.index` | Recommended stock | auto | grant | n/a |
| `report.classification.index` | Client classification | auto | grant | n/a |
| `report.planProduct.index` | Plan by product | auto | grant | n/a |
| `report.movement.index` | Inter-filial movement | auto | grant | n/a |
| `report.purchase.index` | Receipts | auto | grant | n/a |
| `report.photo.index` | Photo reports | auto | grant | n/a |
| `report.clientData.index` | Client base | auto | grant | grant |
| `report.agent.index` | Agent report | auto | grant | n/a |
| `report.agentVisit.index` | Visit report | auto | grant | n/a |
| `report.pivotInventory.index` | Inventory pivot | auto | grant | n/a |
| `report.pivotInventory.dashboard` | Inventory dashboard | auto | grant | n/a |
| `report.planning.index` | Agent planning | auto | grant | n/a |
| `report.shipper.index` | Supplier turnover | auto | grant | n/a |
| `report.material.index` | Material report | auto | grant | n/a |
| `report.kpi.index` | KPI | auto | grant | n/a |
| `report.analyzeAkb.index` | AKB comparative analysis | auto | grant | n/a |
| `report.nmedov.index` | NMEDOV | auto | grant | n/a |
| `directory.region.*` | Regions CRUD | auto | grant | grant |
| `directory.territory.*` | Territories CRUD | auto | grant | grant |
| `directory.adtAudit.*` | ADT audit definitions | auto | grant | n/a |
| `directory.adtBrand.*` | ADT brands | auto | grant | n/a |
| `directory.adtComment.*` | ADT comments | auto | grant | n/a |
| `directory.adtPack.*` | ADT packaging | auto | grant | n/a |
| `directory.adtPoll.*` | ADT polls | auto | grant | n/a |
| `directory.adtProducer.*` | ADT producers | auto | grant | n/a |
| `directory.adtSegment.*` | ADT segments | auto | grant | n/a |
| `directory.clientCategory.*` | Client categories | auto | grant | grant |
| `directory.clientChannel.*` | Client channels | auto | grant | grant |
| `directory.clientType.*` | Client types | auto | grant | grant |
| `directory.clientClass.*` | Client classes | auto | grant | grant |
| `directory.currency.*` | Currencies | auto | grant | n/a |
| `directory.inventoryType.*` | Inventory types | auto | grant | n/a |
| `directory.photoReportCategory.*` | Photo categories | auto | grant | n/a |
| `directory.priceType.*` | Price types | auto | grant | n/a |
| `directory.priceType.setPrices` | Set price values | auto | grant | n/a |
| `directory.priceType.getPrices` | View prices | auto | grant | grant |
| `directory.priceList.index` | Price list | auto | grant | grant |
| `directory.product.index` | Products list | auto | grant | grant |
| `directory.product.create` | Create product | auto | grant | n/a |
| `directory.product.update` | Edit product | auto | grant | n/a |
| `directory.product.import2` | Product import | auto | grant | n/a |
| `directory.productCategory.*` | Product categories | auto | grant | n/a |
| `directory.productSubcategory.*` | Product subcategories | auto | grant | n/a |
| `directory.productCatGroup.*` | Category groups | auto | grant | n/a |
| `directory.productGroup.*` | Product groups | auto | grant | n/a |
| `directory.reject.*` | Rejects | auto | grant | grant |
| `directory.rejectDefect.*` | Reject defects | auto | grant | grant |
| `directory.bonus.*` | Bonus definitions | auto | grant | n/a |
| `directory.bonus.onlyUsers` | "only assigned" toggle | auto | grant | n/a |
| `directory.royalty.*` | Royalty bonuses | auto | grant | n/a |
| `directory.royalty.onlyUsers` | "only assigned" toggle | auto | grant | n/a |
| `directory.rlpBonus.*` | RLP bonuses | auto | grant | n/a |
| `directory.skidka.*` | Discounts | auto | grant | n/a |
| `directory.skidka.onlyUsers` | "only assigned" toggle | auto | grant | n/a |
| `directory.skidkaManual.*` | Manual discounts | auto | grant | n/a |
| `directory.taskType.*` | Task types | auto | grant | n/a |
| `directory.tradeDirection.*` | Trade directions | auto | grant | n/a |
| `directory.unit.*` | Units | auto | grant | n/a |
| `directory.plan.index` | Plan view | auto | grant | grant |
| `directory.plan.set` | Set plan | auto | grant | n/a |
| `directory.planProduct.index` | Plan-by-product view | auto | grant | n/a |
| `directory.planProduct.set` | Set plan-by-product | auto | grant | n/a |
| `directory.productProperties.*` | Product properties | auto | grant | n/a |
| `directory.inventoryGroup.*` | Inventory groups | auto | grant | n/a |
| `directory.shipper.*` | Shippers | auto | grant | n/a |
| `directory.knowledgeCategory.*` | Knowledge categories | auto | grant | n/a |
| `directory.knowledgePost.*` | Knowledge posts | auto | grant | n/a |
| `directory.notification.*` | Notifications | auto | grant | n/a |
| `directory.productCompetitor.*` | Competitor mapping | auto | grant | n/a |
| `directory.orderComment.*` | Order comments | auto | grant | n/a |
| `directory.dealer.index` | Dealer list | auto | grant | n/a |
| `directory.country.*` | Countries | auto | grant | n/a |
| `directory.group.*` | Groups | auto | grant | n/a |
| `directory.kpiTaskTemplateGroup.*` | KPI task template groups | auto | grant | n/a |
| `directory.closed.*` | Closed periods | auto | grant | n/a |
| `directory.inventory.index` | Inventory list | auto | grant | n/a |
| `pivot.sale.index` | Sales pivot | auto | grant | n/a |
| `pivot.discount.index` | Discount pivot | auto | grant | n/a |
| `pivot.rfm.index` | RFM analysis | auto | grant | n/a |
| `pivot.saleDetail.index` | Sales detail pivot | auto | grant | n/a |
| `pivot.defect.index` | Defects pivot | auto | grant | n/a |
| `pivot.transactions.index` | Transactions pivot | auto | grant | n/a |
| `pivot.consumption.index` | Consumption pivot | auto | grant | n/a |
| `pivot.planVisit.index` | Plan-visit pivot | auto | grant | n/a |
| `pivot.expeditor.index` | Expeditor pivot | auto | grant | n/a |
| `pivot.userAccess.index` | User-access pivot | auto | grant | n/a |
| `pivot.lotReport.index` | Lot report | auto | grant | n/a |
| `pivot.purchase.index` | Purchase pivot | auto | grant | n/a |
| `pivot.akb.index` | AKB pivot | auto | grant | n/a |

Notes:

- "auto" = `AccessManager::hasAccess` short-circuits to `true` for admins.
- "grant" = the role can be granted via `cs_access_role` (apply to everyone with that role) or `cs_access_user` (override for a specific user). Per-user grants override role grants on conflict because they're loaded second.
- "n/a" = the operator role is rarely granted these in practice. Operators in sd-cs are intentionally narrow — they mostly do dashboard/sell/stock/debt views and basic directory lookups. Anything operator-feasible is marked "grant"; anything that's a manager-and-above pattern is marked "n/a".
- Action wildcards like `directory.region.*` cover `index`, `create`, `update`, `delete` separately — each is a distinct row in `AccessManager::$accesses` and the grant is per-action, not per-controller.

## Gotchas

### 1. `allowedActions` bypasses the permission check entirely

This is by far the biggest landmine. Every report controller has an `allowedActions = [...]` array, and **any action in that list skips `hasAccess`** (see `Controller::beforeAction`). For example, `SellController` exposes `getData`, `export`, etc. as allowedActions, so a user without `report.sell.index` grant could still call `/report/sell/getData` if they know the URL — only session authentication is enforced for these endpoints.

Where this matters: any audit asking "can role X export sales?" must check **session access + filial filtering inside the action body**, not just the role's grant for `report.sell.index`. Several controllers (`Akb`, `Photo`, `PlanProduct`) add explicit `if (!Yii::app()->user->isAdmin())` checks inside the action to filter by filial — others do not.

### 2. No `Access::check` calls in controllers

Unlike sd-billing, there are **zero `Access::check` calls** in sd-cs controllers. The entire permission gate runs in `Controller::beforeAction` based on URL routing. So:

- You can't grep `Access::check` to find protected actions.
- The list of "what's protected" = the route-derived `<module>.<controller>.<action>` minus `allowedActions` minus admin-bypass.
- Inline permission checks for fine-grained operations (e.g. "can this manager export to Excel?") don't exist in sd-cs the way they do in sd-billing.

### 3. Admin can't be assigned via the user form

`User::rules()` restricts the `role` field to `array_keys(getRoles())` (which is `[2, 3]`) plus `[1]` only if the editing user already has role 1. So:

- A new admin can only be created by another admin.
- The dropdown for Manager and Operator users will not include the Admin option.
- There's no UI flow to "promote a manager to admin" — it requires direct DB write or being already-admin.

### 4. Filial mirroring is one-way and partially destructive

When a user is saved with new filial assignments (or a changed login, or a new password, or `dealerChanged = true`), `User::beforeSave` walks the user's `UserFilial` list and:

- Creates a filial-side `cs_user` row with `cs3_<login>` if it doesn't exist.
- Updates `LOGIN`, `pass`, possibly `NAME` on the filial side.
- For managers (`role == ROLE_MANAGER`), also creates a `StructureFilial` row with `ROLE = 9`.

**Removing a `cs_user_filial` row does not remove the filial-side `cs3_<login>` user.** It stays as an orphan. To clean up filial-side users, you have to delete them in the filial database directly.

Also: if `Yii::app()->params['allAsManager'] == true`, **every** newly-created filial-side mirror gets `ROLE = 9` regardless of `filial_role`. This is a tenant-level config flag that overrides the per-user `filial_role` choice. Watch out when troubleshooting "why is this operator a manager in the filial".

### 5. Per-user grants override per-role grants — silently

In `AccessManager::hasAccess`:

```php
foreach ($models as $model) {
    $this->_access[$model->name] = (int)$model->access;
}
$models = AccessUser::model()->findAllByAttributes([
    'user_id' => $user->profile->id
]);
foreach ($models as $model) {
    $this->_access[$model->name] = (int)$model->access;
}
```

The role grants are loaded first, then user grants. They share the same `$_access` array keyed by operation name. So a user grant with `access = 0` will **revoke** what the role grant gave. There is no UI indication that a user is having a role grant overridden — you have to query `cs_access_user` directly. When debugging "why doesn't this manager see X?", check `cs_access_user` for explicit deny rows before assuming the role grant is missing.

### 6. Operation strings are case-sensitive

`hasAccess($access)` does a strict array key lookup. `report.sell.index` is **not** the same as `report.Sell.index`. The static `$accesses` catalogue is the canonical casing — `priceType`, `clientCategory`, `productCatGroup` etc. are camelCase, while `report.sell.index` and `directory.region.create` are lowercase. The route derivation uses whatever the controller is named (typically PascalCase mapped to camelCase URL), so make sure to match the existing convention when adding a new controller.

### 7. `directory.adtAudit`, `directory.adtBrand` etc. have no `.delete`

The static catalogue commented out the `delete` operations for most ADT and many directory entities:

```php
// 'directory.adtAudit.delete' => 'Удалить',
```

Translation: there is **no permission string for deleting these directory entries**. If a controller tries to call `actionDelete`, the access check will resolve `directory.adtAudit.delete`, and since that key doesn't exist in the catalogue, it will fail closed for non-admins (the `_access` array won't have an entry, so `!empty(...)` is false). Admins still bypass.

If you re-enable a delete action, you must add it to `$accesses` first, otherwise even admins-with-explicit-grants won't pass — only admin-bypass will.

### 8. Filial-side `authassignment` writes happen at filial save, not user save

`User::setFilialRole(FilialUser $filialUser, Filial $model)` is the function that populates `authassignment` in the filial DB. **It is called from `Filial::beforeSave`, not from `User::beforeSave`.** This means changing a user's `filial_role` from the HQ user form does not immediately re-populate `authassignment` — the filial DB sees the new role on `tbl_user.ROLE`, but the `authassignment` rows still reflect the old role until the next time the filial entity is saved.

Concretely: if you change a user's `filial_role` from 5 to 9 in HQ, the filial-side `tbl_user.ROLE` becomes 9 but the user keeps `role.operator` operations in `authassignment` until someone touches the filial record. Refresh by editing the filial in HQ and saving (no changes required).

### 9. `redPriceTypes()` admin bypass leaves settings unread for admin

`User::redPriceTypes()` returns an empty array for admins (`if (!Yii::app()->user->isAdmin()) { ... read user settings ... }`) and the actual `price_types` setting otherwise. So:

- An admin user's per-user `settings.price_types` is never read by this code path.
- If you store other per-user settings as a sibling key in `settings`, beware: anywhere using a similar admin-skip pattern, admins will get defaults instead of their stored settings.

## See also

- [/docs/sd-cs/modules/user](/docs/sd-cs/modules/user) — the user management UI, filial assignment form, and password reset flow.
- [/docs/sd-cs/multi-db](/docs/sd-cs/multi-db) — how `setFilial($prefix)` routes queries between HQ and filial databases, and what gets mirrored where.
- [/docs/sd-cs/architecture](/docs/sd-cs/architecture) — overall structure of HQ vs filial, the `cs_*` table family vs filial-side `tbl_*` family.
- [/docs/security/rbac](/docs/security/rbac) — cross-project RBAC overview.
- [/docs/security/data-isolation](/docs/security/data-isolation) — country/dealer/filial scoping interactions across sd-main, sd-billing, and sd-cs.
- [/docs/security/sd-billing-rbac](/docs/security/sd-billing-rbac) — sibling RBAC reference for the billing project.
