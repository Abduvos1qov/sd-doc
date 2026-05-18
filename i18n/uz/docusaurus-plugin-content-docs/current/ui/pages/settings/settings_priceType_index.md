---
title: "Narx turlari"
audience: sd-main dasturchilari, QA
summary: Admin paneldagi jonli sahifa /settings/priceType/index
topics: [settings, price, page, ui]
---

# Narx turlari

**URL**: `/settings/priceType/index` · **Modul**: `settings` · **Kontroller**: `PriceTypeController::index` · **RBAC**: `operation.settings.priceType` · **Yigʻilgan rol**: `admin`

:::note Skrinshot tayyorlanmoqda — harvester'ni qayta ishga tushirish kerak:::

## Vazifasi

Narx turlari uchun CRUD jadvali. *Narx turi* — narxlashning kanal darajasidagi oʻlchami (chakana / ulgurji / partner / aksiya va h.k.); har bir `Price` qatori `(productId, priceTypeId, dateStart)` uchligi bilan kalitlangan, shuning uchun yangi tur qoʻshish darhol barcha narxlar roʻyxati koʻrinishlarida yangi ustun yaratadi.

## Jadval ustunlari

| № | Ustun |
|---|---|
| 1 | ID |
| 2 | Nomi (i18n) |
| 3 | Qisqa kod |
| 4 | Tartib |
| 5 | Standart bayrog'i |
| 6 | Faol |
| 7 | Yangilangan |

## Amallar

- Narx turini qoʻshish (modal — `createAjax`)
- Narx turini tahrirlash (modal — `updateAjax`)
- Faollikni oʻzgartirish
- Tartibni oʻzgartirish (drag dastasi)

## Backend marshrut

- **Kontroller fayli**: `protected/modules/settings/controllers/PriceTypeController.php` (47-qator)
- **Action turi**: inline (`$this->render('admingrid_diler', …)`)
- **Render qilinadigan view**: `views/priceType/admingrid_diler.php`
- **Talab qilinadigan ruxsat**: `operation.settings.priceType`
- **Qoʻshni endpoint'lar**: `getData`, `getUpdatedRow`, `createAjax`, `updateAjax`

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/settings](/docs/modules/settings)
- Narxlar: [`/settings/prices/index`](./settings_prices_index)
- Narxlar roʻyxati: [`/settings/prices/priceList`](./settings_prices_priceList)
