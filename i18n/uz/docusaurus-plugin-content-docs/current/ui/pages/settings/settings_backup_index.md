---
title: "Zaxira / eksport"
audience: sd-main dasturchilari, QA
summary: Admin paneldagi jonli sahifa /settings/backup/index
topics: [settings, backup, export, page, ui]
---

# Zaxira / eksport

**URL**: `/settings/backup/index` · **Modul**: `settings` · **Kontroller**: `BackupController::index` · **RBAC**: `operation.settings.backup` · **Yigʻilgan rol**: `admin`

:::note Skrinshot tayyorlanmoqda — harvester'ni qayta ishga tushirish kerak:::

## Vazifasi

Markaziy eksport markazi. Har bir plitka tenant'ning hozirgi holatini CSV / JSON sifatida oqim qilib chiqaruvchi maʼlumotnoma eksport ishini ishga tushiradi; off-site zaxiralash, auditga topshirish va yangi oʻrnatishga bir martalik migratsiya uchun foydali. Endpoint'lar `BackupController::endpoints` dan keladi va toʻliq maʼlumotnoma kataloglarini (tovarlar, narxlar, mijozlar va h.k.) qamrab oladi.

## Plitkalar

- Endpoint'lar katalog'i (`endpoints`)
- Tovar (`product`)
- Tovar kategoriyasi (`productCategory`)
- Tovar case turi (`productCaseType`)
- Tovar kategoriyalar guruhi (`productCatGroup`)
- Tovar guruhi (`productGroup`)
- Tovar pastki kategoriyasi (`productSubCategory`)
- Narx turi (`priceType`)
- Narx (`price`)
- (va qolgan plitkalar — toʻliq roʻyxat kontroller manbasida)

## Amallar

- Tanlangan plitka uchun eksportni ishga tushirish
- Yaratilgan faylni yuklab olish

## Backend marshrut

- **Kontroller fayli**: `protected/modules/settings/controllers/BackupController.php` (41-qator)
- **Action turi**: inline (`$this->render('index', …)`)
- **Render qilinadigan view**: `views/backup/index.php`
- **Talab qilinadigan ruxsat**: `operation.settings.backup`

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/settings](/docs/modules/settings)
- Sozlamalar katalog'i: [/quality/settings-catalog](/docs/quality/settings-catalog)
