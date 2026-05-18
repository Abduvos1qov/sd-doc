---
title: "Backup / export"
audience: All sd-main developers, QA
summary: Live admin page at /settings/backup/index
topics: [settings, backup, export, page, ui]
---

# Backup / export

**URL**: `/settings/backup/index` · **Module**: `settings` · **Controller**: `BackupController::index` · **RBAC**: `operation.settings.backup` · **Role harvested**: `admin`

:::note Screenshot pending — harvester re-run needed:::

## Purpose

Master export hub. Each tile triggers a per-directory export job that streams CSV / JSON of the live tenant state; downloads are useful for off-site backup, audit handoff and one-shot migration to a fresh installation. Endpoints come from `BackupController::endpoints` and cover the full reference catalog (products, prices, clients, etc.).

## Tiles

- Endpoints catalog (`endpoints`)
- Product (`product`)
- Product category (`productCategory`)
- Product case type (`productCaseType`)
- Product category group (`productCatGroup`)
- Product group (`productGroup`)
- Product sub-category (`productSubCategory`)
- Price type (`priceType`)
- Price (`price`)
- (and the remaining directory tiles — see controller source for the full list)

## Actions

- Run export for the chosen tile
- Download the produced file

## Backend route

- **Controller file**: `protected/modules/settings/controllers/BackupController.php` (line 41)
- **Action kind**: inline (`$this->render('index', …)`)
- **View rendered**: `views/backup/index.php`
- **Required permission**: `operation.settings.backup`

## See also

- Module reference: [/modules/settings](/docs/modules/settings)
- Settings catalog: [/quality/settings-catalog](/docs/quality/settings-catalog)
