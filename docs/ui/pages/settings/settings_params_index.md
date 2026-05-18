---
title: "Global params"
audience: All sd-main developers, QA
summary: Live admin page at /settings/params/index
topics: [settings, params, page, ui]
---

# Global params

**URL**: `/settings/params/index` · **Module**: `settings` · **Controller**: `ParamsController::index` · **RBAC**: `operation.settings.params` · **Role harvested**: `admin`

:::note Screenshot pending — harvester re-run needed:::

## Purpose

Raw key / value editor for the global params table. Unlike the Settings home page (which groups params into curated tabs), this screen lets a super-admin inspect or edit any param row — including server-toggles like `showAllRbacFunctions`, `enableOnlineOrder`, `payme.merchantId`, etc. Use this only when you know the param key — the curated tabs are safer for everyday work.

## Grid columns

| # | Column |
|---|---|
| 1 | Param key |
| 2 | Value |
| 3 | Group |
| 4 | Description |
| 5 | Updated at |
| 6 | Updated by |

## Actions

- Edit value inline
- Add new param row
- Delete param row (rarely used — usually we keep the row and set value to empty)

## Backend route

- **Controller file**: `protected/modules/settings/controllers/ParamsController.php` (line 5)
- **Action kind**: inline (`$this->render('index')`)
- **View rendered**: `views/params/index.php`
- **Required permission**: `operation.settings.params`

## See also

- Module reference: [/modules/settings](/docs/modules/settings)
- Settings catalog: [/quality/settings-catalog](/docs/quality/settings-catalog)
- Settings home: [`/settings/settings/index`](./settings_settings_index)
