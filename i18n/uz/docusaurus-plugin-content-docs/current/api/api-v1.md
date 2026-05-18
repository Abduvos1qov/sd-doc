---
sidebar_position: 3
title: API v1 (eski)
---

# API v1 — `api` moduli

Hamkor integratsiyalari va bir martalik konnektorlar uchun eski API.
Faqat texnik xizmat ko'rsatish — **bu yerga yangi endpointlar qo'shmang**,
o'rniga v4 dan foydalaning.

## Yuza

```
protected/modules/api/controllers/
```

Faol kontrollerlar (`*.obsolete` bo'lmaganlar):

- `Json1CController` — 1C JSON sinxronizatsiyasi
- `BillingController` — billing webhooklari
- `LicenseController` — litsenziya tekshiruvlari
- `NotificationController` — push ro'yxatga olish
- `OperatorController` / `Operator2Controller` — operator tomonidagi yordamchilar
- `OrderController` — hamkor buyurtma yaratish
- `PushController` — FCM/APNS dispetcheri
- `R2Controller` — ikkinchi avlod o'qish
- `SdController`, `SalesdocController`, `Mef1cController`,
  `IdokonController`, `IkromController`, `NavruzController`,
  `ZarqandController`, `NeonController`, `OnlineOrderController`,
  `OnlineOrder3Controller`, `PradataController`, `SmartUpController`,
  `StockController`, `TelegramBotController`, `V2Controller`,
  `V4Controller`, `CronVisitController`, `ScheduledSmsController`,
  `AnalyticsController`, `ApiLogController`, `CislinkController`,
  `CleannerController`, `ConstructionController`, `DemoCronController`,
  `DisabledChatsController`, `Json1CController`.

(Zamonaviy yuzalar uchun API v3 / v4 sahifalariga qarang.)

## Auth

Asosan URL yoki POST tanasidagi **umumiy maxfiy kalit**, har bir endpoint
uchun farq qiladi. Ba'zilari HTTP basic dan foydalanadi. Global token
sxemasi yo'q.

## Format

JSON. Bir nechta endpoint XML qabul qiladi (`xml1c`, `pradata`).

## Tavsiya etilgan migratsiya

Agar bugun integratsiya qilayotgan bo'lsangiz: [API v4](./api-v4-online/)
ni afzal ko'ring. Agar mavjud v1 iste'molchisi uchun funksiya
qo'shayotgan bo'lsangiz, platforma jamoasiga murojaat qiling — ko'plab v1
endpointlari ishdan chiqarish uchun rejalashtirilgan.
