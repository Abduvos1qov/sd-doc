---
title: "Brendlar"
audience: sd-main dasturchilari, QA
summary: Admin paneldagi jonli sahifa /settings/brand/index
topics: [settings, product, page, ui]
---

# Brendlar

**URL**: `/settings/brand/index` · **Modul**: `settings` · **Kontroller**: `BrandController::index` · **RBAC**: `operation.settings.brand` · **Yigʻilgan rol**: `admin`

:::note Skrinshot tayyorlanmoqda — harvester'ni qayta ishga tushirish kerak:::

## Vazifasi

Brendlar uchun sodda CRUD jadvali. Har bir `Product` qatori bitta `Brand` ga ishora qiladi. Brendlar bir nechta hisobotlarda ham ishlatiladi va buyurtmalar paneli, KPI ekranlari va narxlar roʻyxatida filtr sifatida xizmat qiladi, shuning uchun tovarlar ishora qilayotgan brendni oʻchirish kontroller tomonidan bloklanadi.

## Jadval ustunlari

| № | Ustun |
|---|---|
| 1 | ID |
| 2 | Nomi |
| 3 | Ishlab chiqaruvchi |
| 4 | Tartib |
| 5 | Faol |
| 6 | Yangilangan |

## Amallar

- Brend qoʻshish
- Brendni tahrirlash (`update`)
- Saqlash (`save`)
- Faollikni oʻzgartirish

## Backend marshrut

- **Kontroller fayli**: `protected/modules/settings/controllers/BrandController.php` (35-qator)
- **Action turi**: inline (`$this->render('admingrid_diler')`)
- **Render qilinadigan view**: `views/brand/admingrid_diler.php`
- **Talab qilinadigan ruxsat**: `operation.settings.brand`
- **Qoʻshni endpoint'lar**: `getData`, `save`, `update`

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/settings](/docs/modules/settings)
- Tovar masteri: [`/settings/product/index`](./settings_product_index)
- Ishlab chiqaruvchilar: `/settings/producer/index`
