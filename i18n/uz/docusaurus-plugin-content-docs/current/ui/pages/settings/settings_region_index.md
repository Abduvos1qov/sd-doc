---
title: "Mintaqalar"
audience: sd-main dasturchilari, QA
summary: Admin paneldagi jonli sahifa /settings/region/index
topics: [settings, geo, page, ui]
---

# Mintaqalar

**URL**: `/settings/region/index` · **Modul**: `settings` · **Kontroller**: `RegionController::index` · **RBAC**: `operation.settings.region` · **Yigʻilgan rol**: `admin`

:::note Skrinshot tayyorlanmoqda — harvester'ni qayta ishga tushirish kerak:::

## Vazifasi

Mintaqalar maʼlumotnomasi — `City` ustidagi yirikroq geografik daraja. KPI / sotuv hisobotlarida hudud oʻlchamini belgilaydi va odatda supervayzer qamroviga mos keladi. Tenant'larning koʻpchiligi bu yerga Oʻzbekistonning 14 viloyati va Toshkent shahrini joylashtirgan.

## Jadval ustunlari

| № | Ustun |
|---|---|
| 1 | ID |
| 2 | Nomi |
| 3 | Kod |
| 4 | Tartib |
| 5 | Faol |

## Amallar

- Mintaqa qoʻshish
- Mintaqani tahrirlash (`updateAjax`)
- Ommaviy oʻchirish (`ajaxMassDelete`)
- Faollikni oʻzgartirish

## Backend marshrut

- **Kontroller fayli**: `protected/modules/settings/controllers/RegionController.php` (38-qator)
- **Action turi**: inline (`$this->render('admin', …)` qobiq + `_ajaxmassdelete`)
- **Render qilinadigan view**: `views/region/admin.php`
- **Talab qilinadigan ruxsat**: `operation.settings.region`
- **Qoʻshni endpoint'lar**: `updateAjax`, `ajaxMassDelete`

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/settings](/docs/modules/settings)
- Shaharlar: [`/settings/city/index`](./settings_city_index)
