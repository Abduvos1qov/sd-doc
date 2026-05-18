---
title: "Valyutalar"
audience: sd-main dasturchilari, QA
summary: Admin paneldagi jonli sahifa /settings/currency/index
topics: [settings, currency, page, ui]
---

# Valyutalar

**URL**: `/settings/currency/index` · **Modul**: `settings` · **Kontroller**: `CurrencyController::index` · **RBAC**: `operation.settings.currency` · **Yigʻilgan rol**: `admin`

:::note Skrinshot tayyorlanmoqda — harvester'ni qayta ishga tushirish kerak:::

## Vazifasi

Valyutalar va ularning kunlik kurslarini boshqarish uchun CRUD jadvali. Finans va buyurtmalar tomonidan asosiy valyuta (odatda `UZS`) va kotirovka valyutalari (`USD`, `RUB`) oʻrtasidagi konvertatsiya uchun foydalaniladi. Integratsiya yoqilgan boʻlsa, kurs Oʻzbekiston Markaziy banki feed'idan avtomatik ravishda olinadi; qoʻlda kiritilgan oʻzgartirishlar feed'ni bekor qiladi.

## Jadval ustunlari

| № | Ustun |
|---|---|
| 1 | ISO kod |
| 2 | Nomi |
| 3 | Belgisi |
| 4 | Asosiyga kursi |
| 5 | Amal qilish sanasi |
| 6 | Manba (feed / qoʻlda) |
| 7 | Faol |

## Amallar

- Valyuta qoʻshish
- Valyutani tahrirlash
- Sana boʻyicha kursni tahrirlash (modal — `updateAjax`)
- Faollikni oʻzgartirish
- Feed'dan yangilash

## Backend marshrut

- **Kontroller fayli**: `protected/modules/settings/controllers/CurrencyController.php` (41-qator)
- **Action turi**: inline (`$this->render('admingrid_diler', …)`)
- **Render qilinadigan view**: `views/currency/admingrid_diler.php`
- **Talab qilinadigan ruxsat**: `operation.settings.currency`
- **Qoʻshni endpoint'lar**: `getData`, `getUpdatedRow`, `updateAjax`

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/settings](/docs/modules/settings)
- Koʻp valyutali yaxlitlash: [/concepts/multi-currency-rounding](/docs/concepts/multi-currency-rounding)
