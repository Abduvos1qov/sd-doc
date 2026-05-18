---
title: "Narxlar bosh sahifasi"
audience: sd-main dasturchilari, QA
summary: Admin paneldagi jonli sahifa /settings/prices/index
topics: [settings, price, page, ui]
---

# Narxlar bosh sahifasi

**URL**: `/settings/prices/index` · **Modul**: `settings` · **Kontroller**: `PricesController::index` · **RBAC**: `operation.settings.prices` · **Yigʻilgan rol**: `admin`

:::note Skrinshot tayyorlanmoqda — harvester'ni qayta ishga tushirish kerak:::

## Vazifasi

Narxlar roʻyxatini boshqarish uchun kirish sahifasi. Foydalanuvchi tahrirlash mumkin boʻlgan narxlar roʻyxatiga oʻtishdan oldin narx turini, amal qilish sanasini va qamrovni (hudud / brend / kategoriya) tanlaydi. Sahifaning oʻzi faqat `views/prices/index.php` qobig'ini render qiladi; jadvalning asosiy mantig'i [Narxlar roʻyxati](./settings_prices_priceList) sahifasida joylashgan.

## Amallar

- Narx turini tanlash (turlar `PriceTypeController` dan yuklanadi)
- Amal qilish sanasini tanlash (standart — bugun)
- Qamrov filtrlarini tanlash
- Narxlar roʻyxatini ochish
- Excel import dialogini ochish

## Backend marshrut

- **Kontroller fayli**: `protected/modules/settings/controllers/PricesController.php` (7-qator)
- **Action turi**: inline (`$this->render('index')`)
- **Render qilinadigan view**: `views/prices/index.php`
- **Talab qilinadigan ruxsat**: `operation.settings.prices`
- **Qoʻshni write endpoint'lar**: `save`, `multiSave`, `saveWithout`, `config`, `markup`, `stock`

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/settings](/docs/modules/settings)
- Narxlar roʻyxati: [`/settings/prices/priceList`](./settings_prices_priceList)
- Import: [`/settings/prices/importExcel`](./settings_prices_importExcel)
- Narx turlari: [`/settings/priceType/index`](./settings_priceType_index)
