---
title: "Pay — interfeys sahifalari"
sidebar_position: 1
---

# Pay — interfeys sahifalari

**Pay** moduli faqat webhook qabul qiluvchi quyi-tizim sifatida ishlaydi; **foydalanuvchi uchun admin sahifalari yoʻq**.

U Oʻzbekistondagi toʻlov provayderlari bot yoki vitrina orqali yaratilgan onlayn buyurtmalarni hisob-kitob qilish uchun ishlatadigan uchta tashqi callback endpoint'ini taqdim etadi:

| Marshrut | Kontroller | Vazifasi |
|---|---|---|
| `/pay/payme/index` | `PaymeController::index` | Payme (Paycom) merchant API qabul qiluvchi — CheckPerformTransaction / CreateTransaction / PerformTransaction / CancelTransaction / CheckTransaction / GetStatement |
| `/pay/click/index` | `ClickController::index` | Click prepare / complete callback (imzo tekshiriladi) |
| `/pay/apelsin/index` | `ApelsinController::index` | Apelsin notify callback |

Har bir action POST tanasini xom holatda oʻqiydi, `Distr::saveFile` orqali alohida log-faylga yozadi, mos helper sinfiga (`PaymeHelper`, `ClickTransaction`, `ApelsinHelper`) yuboradi, bogʻlangan `OnlineOrder` ni yangilaydi (`PAY` maydoni, `createTransaction()` chaqirig'i) va provayder kutgan JSON javobini qaytaradi.

GET orqali xizmat qiluvchi HTML sahifalar, formalar va grid'lar yoʻq. Konfiguratsiya (merchant ID, maxfiy kalitlar, login maʼlumotlari) global params jadvalida saqlanadi — [Settings moduli maʼlumotnomasi](/docs/modules/settings) va [Params sahifasi](../settings/settings_params_index) ga qarang.

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/pay](/docs/modules/pay)
- Onlayn buyurtma oqimi: [`OnlineOrder` modeli](/docs/schema/online-order)
- Marshrutlar reestri: [`static/data/routes.json`](/data/routes.json)
