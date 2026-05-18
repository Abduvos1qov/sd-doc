---
title: "Narxlarni import qilish (Excel)"
audience: sd-main dasturchilari, QA
summary: Admin paneldagi jonli sahifa /settings/prices/importExcel
topics: [settings, price, import, page, ui]
---

# Narxlarni import qilish (Excel)

**URL**: `/settings/prices/importExcel` · **Modul**: `settings` · **Kontroller**: `PricesController::importExcel` · **RBAC**: `operation.settings.prices` · **Yigʻilgan rol**: `admin`

:::note Skrinshot tayyorlanmoqda — harvester'ni qayta ishga tushirish kerak:::

## Vazifasi

Excel jadvalidan narxlarni ommaviy yuklash. Narx turi va amal qilish sanasini tanlang, faylni yuklang (A ustun — tovar kodi, B ustun — narx), farqni koʻrib chiqing va tasdiqlang. Mos kelmagan tovar kodlari ajratib koʻrsatiladi va tasdiqlashda oʻtkazib yuboriladi. `priceList` ning katakli tahrirlovchisidan farqli oʻlaroq, ushbu endpoint katta kitoblarni bir tranzaksiyada qabul qiladi va yetkazib beruvchilardan oylik narx yangilanishlari uchun rasmiy yoʻldir.

## Maydonlar

| Yorliq | Nomi | Turi | Majburiy |
|---|---|---|---|
| Narx turi | `priceTypeId` | select | ha |
| Amal qilish sanasi | `dateStart` | sana | ha |
| Fayl | `file` | xlsx upload | ha |
| Boʻsh katak deb hisoblash | `emptyMode` | select (skip / zero) | yoʻq |

## Amallar

- Yuklash va koʻrib chiqish
- Tasdiqlash va saqlash
- Bekor qilish va qayta yuklash

## Backend marshrut

- **Kontroller fayli**: `protected/modules/settings/controllers/PricesController.php` (196-qator)
- **Action turi**: inline (`$this->render('import-prices')`)
- **Render qilinadigan view**: `views/prices/import-prices.php`
- **Talab qilinadigan ruxsat**: `operation.settings.prices`

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/settings](/docs/modules/settings)
- Narxlar roʻyxati: [`/settings/prices/priceList`](./settings_prices_priceList)
- Narxlar bosh sahifasi: [`/settings/prices/index`](./settings_prices_index)
