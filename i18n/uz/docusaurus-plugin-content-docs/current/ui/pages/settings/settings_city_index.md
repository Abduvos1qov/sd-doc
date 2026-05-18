---
title: "Shaharlar"
audience: sd-main dasturchilari, QA
summary: Admin paneldagi jonli sahifa /settings/city/index
topics: [settings, geo, page, ui]
---

# Shaharlar

**URL**: `/settings/city/index` · **Modul**: `settings` · **Kontroller**: `CityController::index` · **RBAC**: `operation.settings.city` · **Yigʻilgan rol**: `admin`

:::note Skrinshot tayyorlanmoqda — harvester'ni qayta ishga tushirish kerak:::

## Vazifasi

Shaharlar maʼlumotnomasi. Mijozlar, agentlar va omborlar uchun manzil darajasidagi granulyatsiya hamda KPI / sotuv hisobotlarida geografik filtr sifatida ishlatiladi. Har bir shahar `Region` ga biriktirilgan. Yangi tenant'ni qoʻlda emas, master jadvaldan toʻldirish uchun Excel import endpoint'i ham bor.

## Jadval ustunlari

| № | Ustun |
|---|---|
| 1 | ID |
| 2 | Nomi |
| 3 | Mintaqa |
| 4 | Pochta indeksi |
| 5 | Tartib |
| 6 | Faol |

## Amallar

- Shahar qoʻshish (modal — `createAjax`)
- Shaharni tahrirlash (modal — `updateAjax`)
- Excel'dan import (`importXls`)
- Faollikni oʻzgartirish

## Backend marshrut

- **Kontroller fayli**: `protected/modules/settings/controllers/CityController.php` (46-qator)
- **Action turi**: inline (`$this->render('admingrid_diler', …)`)
- **Render qilinadigan view**: `views/city/admingrid_diler.php`
- **Talab qilinadigan ruxsat**: `operation.settings.city`
- **Qoʻshni endpoint'lar**: `getData`, `getUpdatedRow`, `createAjax`, `updateAjax`, `importXls`

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/settings](/docs/modules/settings)
- Mintaqalar: [`/settings/region/index`](./settings_region_index)
