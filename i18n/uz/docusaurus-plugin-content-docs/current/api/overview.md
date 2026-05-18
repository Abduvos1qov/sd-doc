---
sidebar_position: 1
title: API umumiy ko'rinishi
---

# API umumiy ko'rinishi

Mavjud **to'rtta versiyalangan API yuzasi**, har biri alohida Yii moduli:

| Versiya | Modul | Auditoriya | Holati |
|---------|-------|-----------|--------|
| **v1** | `api` | Eski server-server, hamkor integratsiyalari | Texnik xizmat ko'rsatish |
| **v2** | `api2` | Eski mobil mijozlar | Muzlatilgan |
| **v3** | `api3` | **Joriy mobil agent ilovasi** | Faol |
| **v4** | `api4` | **B2B / onlayn buyurtma portali / yangi mobil mijozlar** | Faol |

URL'lar `/<module>/<controller>/<action>` shablonida. Misollar:

- `POST /api3/login/index`
- `GET  /api3/order/list`
- `POST /api4/order/create`
- `POST /api/json1c/import`

## Konvensiyalar

- **Transport**: faqat HTTPS (TLS Nginx'da tugaydi).
- **Auth**: token asosida (`api3` / `api4`); ba'zi v1 endpointlari uchun
  umumiy maxfiy kalit yoki basic auth. [Autentifikatsiya](./authentication.md) bo'limiga qarang.
- **Format**: JSON so'rov/javob. v1 da bir nechta XML endpointi bor
  (`xml1c`, `pradata`).
- **Sana/vaqt**: agar endpoint boshqacha ko'rsatmasa, UTC dagi ISO 8601.
- **Xatoliklar**: HTTP status + JSON tanasi
  ```json
  { "success": false, "error": "Описание ошибки", "code": "INVALID_TOKEN" }
  ```
- **Sahifalash**: query parametrlari `?page=N&limit=M`. Javob `total`,
  `page`, `limit` ni o'z ichiga oladi.
- **Til**: `?lang=ru|en|uz` foydalanuvchi standartini bekor qiladi.
- **Tezlik chegarasi**: gateway darajasida IP bo'yicha. Auth endpointlarida
  ilova darajasidagi tezlik chegarasi (`LoginController` muvaffaqiyatsiz
  urinishlarni cheklaydi).

## Versiyalash siyosati

- **v3 va v4 barqaror**. Buzg'unchi o'zgarishlar yangi endpoint sifatida
  chiqariladi, hech qachon joyida emas.
- **v1 va v2 muzlatilgan** — kontrollerlardagi `*.obsolete` fayllar
  arxeologiya uchun saqlangan olib tashlangan koddir.

## Qisqacha xarita

- [Autentifikatsiya](./authentication.md)
- [API v1 ma'lumotnomasi](./api-v1.md)
- [API v2 ma'lumotnomasi](./api-v2.md)
- [API v3 (mobil agent)](./api-v3-mobile/)
- [API v4 (onlayn / B2B)](./api-v4-online/)
- [Xatolik kodlari](./error-codes.md)
- [Webhooklar](./webhooks.md)
