---
title: "Global parametrlar"
audience: sd-main dasturchilari, QA
summary: Admin paneldagi jonli sahifa /settings/params/index
topics: [settings, params, page, ui]
---

# Global parametrlar

**URL**: `/settings/params/index` · **Modul**: `settings` · **Kontroller**: `ParamsController::index` · **RBAC**: `operation.settings.params` · **Yigʻilgan rol**: `admin`

:::note Skrinshot tayyorlanmoqda — harvester'ni qayta ishga tushirish kerak:::

## Vazifasi

Global parametrlar jadvalining xom key / value muharriri. Sozlamalar bosh sahifasidan farqli oʻlaroq (u yerda parametrlar tartibli tablarda joylashgan), bu yerda super-admin har qanday qatorni koʻrishi yoki tahrirlashi mumkin — shu jumladan `showAllRbacFunctions`, `enableOnlineOrder`, `payme.merchantId` kabi server bayroqlari ham. Faqat parametr kalitini bilganingizda foydalaning — kundalik ish uchun tartibli tablar xavfsizroq.

## Jadval ustunlari

| № | Ustun |
|---|---|
| 1 | Parametr kaliti |
| 2 | Qiymat |
| 3 | Guruh |
| 4 | Tavsif |
| 5 | Yangilangan |
| 6 | Kim yangilagan |

## Amallar

- Qiymatni inline tahrirlash
- Yangi parametr qatorini qoʻshish
- Qatorni oʻchirish (kam ishlatiladi — odatda qatorni qoldirib qiymatni boʻsh qoldiramiz)

## Backend marshrut

- **Kontroller fayli**: `protected/modules/settings/controllers/ParamsController.php` (5-qator)
- **Action turi**: inline (`$this->render('index')`)
- **Render qilinadigan view**: `views/params/index.php`
- **Talab qilinadigan ruxsat**: `operation.settings.params`

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/settings](/docs/modules/settings)
- Sozlamalar katalog'i: [/quality/settings-catalog](/docs/quality/settings-catalog)
- Sozlamalar bosh sahifasi: [`/settings/settings/index`](./settings_settings_index)
