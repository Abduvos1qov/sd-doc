---
title: "Sozlamalar bosh sahifasi"
audience: sd-main dasturchilari, QA
summary: Admin paneldagi jonli sahifa /settings/settings/index
topics: [settings, page, ui]
---

# Sozlamalar bosh sahifasi

**URL**: `/settings/settings/index` · **Modul**: `settings` · **Kontroller**: `SettingsController::index` · **RBAC**: `operation.settings.access` · **Yigʻilgan rol**: `admin`

:::note Skrinshot tayyorlanmoqda — harvester'ni qayta ishga tushirish kerak:::

## Vazifasi

sd-main ning asosiy konfiguratsiya paneli. Tenant'ning har bir runtime parametri (narxlar roʻyxati qoidalari, buyurtma oqimi bayroqlari, balans va finans xulq-atvori, GPS chegaralari, audit sozlamalari, integratsiya kalitlari) bu yerda tablar boʻyicha guruhlangan. Saqlash `SettingsController::saveSettings` orqali POST qilinadi; kesh `actionTruncateCache` orqali tozalanadi.

## Joylashuv

- Yuqori: tablar — General · Orders · Prices · Stock · Finans · GPS · Audit · Integrations · UI · Telegram.
- Har bir tab: maydonlar guruhi (raqam, select, boolean, koʻp qatorli matn).
- Past: "Saqlash", "Boʻlimni tiklash", "Keshni tozalash".

## Amallar

- Sozlamalarni saqlash (`sd_params` / tenant jadvaliga yoziladi)
- Keshni tozalash (`/settings/settings/truncateCache`)
- Datatable sozlamalarini tozalash (`/settings/settings/deleteDatatableSettings`)
- Buyurtma sarlavhasini saqlash (`/settings/settings/saveHeaderOrders`)
- Bitta table-control yozuvini tozalash (`/settings/settings/truncateTableControl`)

## Backend marshrut

- **Kontroller fayli**: `protected/modules/settings/controllers/SettingsController.php` (38-qator)
- **Action turi**: inline
- **Render qilinadigan view**: `views/settings/index.php`
- **Talab qilinadigan ruxsat**: `operation.settings.access`
- **Qoʻshni write endpoint'lar**: `saveSettings`, `saveHeaderOrders`, `truncateCache`, `truncateTableControl`, `deleteDatatableSettings`

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/settings](/docs/modules/settings)
- Sozlamalar katalog'i: [/quality/settings-catalog](/docs/quality/settings-catalog)
- Parametrlar muharriri: [`/settings/params/index`](./settings_params_index)
