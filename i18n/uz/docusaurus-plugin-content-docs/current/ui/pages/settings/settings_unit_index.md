---
title: "Oʻlchov birliklari"
audience: sd-main dasturchilari, QA
summary: Admin paneldagi jonli sahifa /settings/unit/index
topics: [settings, product, page, ui]
---

# Oʻlchov birliklari

**URL**: `/settings/unit/index` · **Modul**: `settings` · **Kontroller**: `UnitController::index` · **RBAC**: `operation.settings.unit` · **Yigʻilgan rol**: `admin`

:::note Skrinshot tayyorlanmoqda — harvester'ni qayta ishga tushirish kerak:::

## Vazifasi

Oʻlchov birliklari maʼlumotnomasi. Har bir tovarning asosiy birligi bor (dona, kg, litr) va u qadoqlarda sotilishi mumkin (10 dona = 1 quti). Birliklar miqdorlarni koʻrsatish uchun ombor, finans va hisobotlarda ham ishlatiladi. Birliklar oʻrtasidagi konvertatsiya koeffitsiyentlari shu jadvalda emas, `Product` qatorida saqlanadi — bu ekran faqat birlik nomlarini va qisqa yorliqlarni kataloglaydi.

## Jadval ustunlari

| № | Ustun |
|---|---|
| 1 | ID |
| 2 | Nomi |
| 3 | Qisqa yorliq |
| 4 | Tartib |
| 5 | Faol |

## Amallar

- Birlik qoʻshish
- Birlikni tahrirlash (`updateAjax`)
- Faollikni oʻzgartirish

## Backend marshrut

- **Kontroller fayli**: `protected/modules/settings/controllers/UnitController.php` (46-qator)
- **Action turi**: inline (`$this->render('admingrid_diler', …)`)
- **Render qilinadigan view**: `views/unit/admingrid_diler.php`
- **Talab qilinadigan ruxsat**: `operation.settings.unit`
- **Qoʻshni endpoint'lar**: `getData`, `getUpdatedRow`, `updateAjax`

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/settings](/docs/modules/settings)
- Tovar masteri: [`/settings/product/index`](./settings_product_index)
- Tara / qadoqlash: [/concepts/tara-packaging](/docs/concepts/tara-packaging)
