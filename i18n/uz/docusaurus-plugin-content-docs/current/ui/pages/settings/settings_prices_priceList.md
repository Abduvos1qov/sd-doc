---
title: "Narxlar roʻyxati"
audience: sd-main dasturchilari, QA
summary: Admin paneldagi jonli sahifa /settings/prices/priceList
topics: [settings, price, page, ui]
---

# Narxlar roʻyxati

**URL**: `/settings/prices/priceList` · **Modul**: `settings` · **Kontroller**: `PricesController::priceList` · **RBAC**: `operation.settings.prices` · **Yigʻilgan rol**: `admin`

:::note Skrinshot tayyorlanmoqda — harvester'ni qayta ishga tushirish kerak:::

## Vazifasi

Tahrirlanishi mumkin boʻlgan haqiqiy narxlar roʻyxati. Har bir tovar uchun bitta qator va har bir `priceType` uchun bitta ustun bilan render qilinadi; har bir katak inline tahrirlanadi. Saqlashda narxlar `actionSave` (bitta qator), `actionMultiSave` (ommaviy) yoki `actionSaveWithout` (chiqarib tashlangan tovarlar) orqali POST qilinadi. Jadval ustama tarqatishni (tanlangan asosiy ustunga foiz qoʻllash) va musbat ombor qoldig'i bor qatorlarni ajratib koʻrsatuvchi ombor qoplamini qoʻllab-quvvatlaydi.

## Jadval ustunlari

| № | Ustun |
|---|---|
| 1 | Tovar kodi |
| 2 | Tovar nomi |
| 3 | Kategoriya |
| 4 | Brend |
| 5 | Birlik |
| 6 | Ombor qoldig'i (qoplama yoqilganda) |
| 7+ | Har bir faol narx turi uchun bittadan ustun |

## Amallar

- Katakni inline tahrirlash
- Tanlangan qatorlarni ommaviy tahrirlash
- Ustamani qoʻllash (`actionMarkup`)
- Ombor qoplamasini yoqish/oʻchirish (`actionStock`)
- Kategoriya / brend / qidiruv boʻyicha filtrlash
- Excel'ga eksport
- Excel importini ochish

## Backend marshrut

- **Kontroller fayli**: `protected/modules/settings/controllers/PricesController.php` (191-qator)
- **Action turi**: inline (`$this->render('priceList')`)
- **Render qilinadigan view**: `views/prices/priceList.php`
- **Talab qilinadigan ruxsat**: `operation.settings.prices`
- **Saqlash endpoint'lari**: `save`, `multiSave`, `saveWithout`

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/settings](/docs/modules/settings)
- Narxlar bosh sahifasi: [`/settings/prices/index`](./settings_prices_index)
- Excel import: [`/settings/prices/importExcel`](./settings_prices_importExcel)
- Narx turlari: [`/settings/priceType/index`](./settings_priceType_index)
