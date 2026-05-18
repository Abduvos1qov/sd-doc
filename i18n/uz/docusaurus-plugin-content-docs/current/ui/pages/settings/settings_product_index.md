---
title: "Tovar masteri"
audience: sd-main dasturchilari, QA
summary: Admin paneldagi jonli sahifa /settings/product/index
topics: [settings, product, page, ui]
---

# Tovar masteri

**URL**: `/settings/product/index` · **Modul**: `settings` · **Kontroller**: `ProductController::index` · **RBAC**: `operation.settings.product` · **Yigʻilgan rol**: `admin`

:::note Skrinshot tayyorlanmoqda — harvester'ni qayta ishga tushirish kerak:::

## Vazifasi

Tovar master jadvali. Tenant sotadigan har bir SKU bu yerda roʻyxatdan oʻtkaziladi: kod, nom, kategoriya, brend, asosiy birlik, qadoqlash, soliq bayroqlari, surat, shtrix-kod, mahalliy kod, marka (Markirovka / CRPT) bayrog'i. Boshqa ekranlar ommaviy import, tartiblash, deaktivatsiya, tovar guruhlari, mahalliy kodlarni biriktirish va yangilashlarni qamrab oladi.

## Jadval ustunlari

| № | Ustun |
|---|---|
| 1 | ID |
| 2 | Kod |
| 3 | Nomi |
| 4 | Kategoriya |
| 5 | Pastki kategoriya |
| 6 | Brend |
| 7 | Ishlab chiqaruvchi |
| 8 | Asosiy birlik |
| 9 | Qadoqlash hajmi |
| 10 | Shtrix-kod |
| 11 | Mahalliy kod |
| 12 | Markirovka |
| 13 | Faol |
| 14 | Yaratilgan |

## Amallar

- Tovar qoʻshish (modal — `createAjax`)
- Tovarni tahrirlash (modal — `updateAjax`)
- Tovarni oʻchirish (`deleteProduct`, `checkDelete`)
- Ommaviy qoʻshish (`addProducts`)
- Excel'dan import (`import_xls`)
- Mahalliy kodlarni import qilish (`import_local_code`)
- Yangilanishlarni import qilish (`import_update`)
- Tartiblash (`sort_product`)
- Tanlanganlarni deaktivatsiya qilish (`deactivate`)
- Tovar guruhlari (`product_group`)
- Dublikatlarni tekshirish (`check`)

## Backend marshrut

- **Kontroller fayli**: `protected/modules/settings/controllers/ProductController.php` (65-qator)
- **Action turi**: inline (`$this->render('admingrid_diler', …)`)
- **Render qilinadigan view**: `views/product/admingrid_diler.php`
- **Talab qilinadigan ruxsat**: `operation.settings.product`
- **Qoʻshni endpoint'lar**: `getData`, `getUpdatedRow`, `getExtras`, `createAjax`, `updateAjax`, `deleteProduct`, `addProducts`

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/settings](/docs/modules/settings)
- Brendlar: [`/settings/brand/index`](./settings_brand_index)
- Birliklar: [`/settings/unit/index`](./settings_unit_index)
- Partiyalarni boshqarish: [/concepts/lot-management](/docs/concepts/lot-management)
