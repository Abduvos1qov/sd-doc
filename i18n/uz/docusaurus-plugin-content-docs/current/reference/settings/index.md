---
sidebar_position: 1
title: Settings catalog
audience: Backend engineers, ops, support
summary: Every runtime toggle, feature flag and per-tenant setting across the three projects, grouped so you can find the right knob without grepping.
topics: [settings, toggles, feature-flags, params, server-settings, catalog]
---

# Settings catalog

Every project in the SalesDoctor ecosystem has several layers of configuration that change behaviour at runtime. This page is the index — pick the surface you need.

| Page | Surface | When to use |
|------|---------|-------------|
| [sd-main · server settings](./sd-main-server-settings.md) | Global / per-tenant flags read via `ServerSettings`, `Yii::app()->params`, and the dynamic `params.json` | You want to change how the whole tenant behaves — money rounding, visit distance, period-close enforcement, feature toggles |
| [sd-main · tenant config](./sd-main-tenant-settings.md) | Per-tenant reference data tables — price types, bonus/discount rules, cashboxes, channels, trade types | You want to add a new price list, configure a promotion, change channel definitions |
| [sd-billing · settings](./sd-billing-settings.md) | App-wide settings + reference data CRUD inside the billing platform | You manage the vendor side — currencies, classifications, cities, system log |
| [sd-cs · settings](./sd-cs-settings.md) | HQ control-plane settings — saved pivots, filial visibility, role defaults | You manage HQ users, regions, and saved-report layouts |

## Quick orientation

**Where does a setting actually live?**

- **Static config** — `protected/config/main.php`, `params.php`, `db.php`, `auth.php`. Changing requires a deploy.
- **Dynamic params** — `protected/config/params.json` (sd-main). Editable at runtime through the settings UI or the `SaveDynamicParamAction` API. No deploy required; takes effect on next request.
- **DB reference tables** — price types, currencies, bonus rules, channels. Edited through the standard CRUD UI. Takes effect immediately for new orders / new visits.
- **Per-user preferences** — datatable column orders, default filters. Stored in `tableControl`. Affect only the editing user.

**Who can change what?**

| Layer | Who can edit |
|-------|--------------|
| Static config | DevOps with shell access |
| Dynamic params | Tenant admin with the `operation.settings.params` operation |
| Reference tables | Tenant admin / power user (varies per table) |
| Per-user preferences | The user themselves |

## See also

- [`settings` module reference](/docs/modules/settings) — UI surface for the toggles below
- [Architecture / configuration](/docs/project/configuration) — file-by-file config breakdown
- [Period-close concept](/docs/concepts/period-close) — the most consequential setting
- [Security / RBAC](/docs/security/rbac) — the operation strings every gated setting checks against
