---
title: "Settings home"
audience: All sd-main developers, QA
summary: Live admin page at /settings/settings/index
topics: [settings, page, ui]
---

# Settings home

**URL**: `/settings/settings/index` · **Module**: `settings` · **Controller**: `SettingsController::index` · **RBAC**: `operation.settings.access` · **Role harvested**: `admin`

:::note Screenshot pending — harvester re-run needed:::

## Purpose

The main configuration panel of sd-main. Every per-tenant runtime toggle (price-list rules, order-flow flags, balance & finans behaviour, GPS thresholds, audit knobs, integration switches, etc.) is grouped into tabbed sections here. Edits are POSTed back through `SettingsController::saveSettings`; cache is invalidated through `actionTruncateCache`.

## Layout

- Top: tab strip — General · Orders · Prices · Stock · Finans · GPS · Audit · Integrations · UI · Telegram.
- Each tab: a form with grouped inputs (number, select, boolean, multi-line text).
- Footer: "Save", "Reset section", "Clear cache".

## Actions

- Save settings (writes to `sd_params` / per-tenant param table)
- Truncate cache (`/settings/settings/truncateCache`)
- Truncate datatable settings (`/settings/settings/deleteDatatableSettings`)
- Save order-header layout (`/settings/settings/saveHeaderOrders`)
- Truncate a single table-control entry (`/settings/settings/truncateTableControl`)

## Backend route

- **Controller file**: `protected/modules/settings/controllers/SettingsController.php` (line 38)
- **Action kind**: inline
- **View rendered**: `views/settings/index.php`
- **Required permission**: `operation.settings.access`
- **Sibling write endpoints**: `saveSettings`, `saveHeaderOrders`, `truncateCache`, `truncateTableControl`, `deleteDatatableSettings`

## See also

- Module reference: [/modules/settings](/docs/modules/settings)
- Settings catalog: [/quality/settings-catalog](/docs/quality/settings-catalog)
- Params editor: [`/settings/params/index`](./settings_params_index)
