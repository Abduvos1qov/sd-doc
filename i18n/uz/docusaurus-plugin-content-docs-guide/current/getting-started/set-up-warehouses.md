---
sidebar_position: 8
title: Omborlarni sozlash
---

# Omborlaringizni sozlang

**Ombor** — bu siz qoldiq saqlaydigan istalgan joy — asosiy ombor, kichik filial, ekspeditor mashinasi. Sotilgan har bir mahsulot birligi har qanday vaqtda aniq bir omborda bo'ladi.

## Qadam 1 — Omborlar ro'yxatini oching

Menyudan **Склад → Склады** (Ombor → Omborlar) ni tanlang yoki to'g'ridan-to'g'ri `/warehouse/list` ni oching:

![Omborlar ro'yxati — barcha filiallar va turlari](/screens/guide/08-warehouses-list.png)

Ro'yxat har bir omborni turi, mas'ul shaxsi va joriy qoldiq qiymati bilan ko'rsatadi.

## Qadam 2 — Sizga qanday turlar kerakligini hal qiling

Distribyutsiya bilan shug'ullanadigan biznesning ko'pchiligi quyidagilarga ega:

| Tur | Misol nom | Maqsadi |
|-----|-----------|---------|
| **Asosiy** | "Markaziy ombor" | Yetkazib beruvchilardan qabul qiladi |
| **Filial** | "Toshkent filiali" | Hududiy ofisdagi qoldiq |
| **Mashina qoldig'i** | "Mashina #07" | Ekspeditor olib yurgan tovar |
| **Brak** | "Qaytarimlar / shikastlangan" | Mijozdan qaytgan va qayta sotib bo'lmaydigan tovar |

## Qadam 3 — "Ombor qo'shish" tugmasini bosing

Yuqori o'ng burchakdagi **+ Добавить** tugmasini bosing.

## Qadam 4 — Formani to'ldiring

| Maydon | Nimani kiritish kerak |
|--------|----------------------|
| **Название** | Jamoangiz taniydigan nom |
| **Тип** | Asosiy / Filial / Mashina / Brak |
| **Ответственный** | Kirim va ko'chirishlarga qo'l qo'ya oladigan jamoa a'zosi |
| **Адрес** | Jismoniy manzil (mashinalar uchun "Mashina #07" deb yozing) |

## Qadam 5 — Saqlang

**Сохранить** tugmasini bosing. Ombor darhol ro'yxatda paydo bo'ladi. Endi unga **Поступления** (Kirimlar) orqali tovar kiritishingiz mumkin — keyingi bo'limda batafsil.

## Har bir ombordan nima qila olasiz

Kartochkasini ochish uchun istalgan ombor qatorini bosing:

- **Joriy qoldiq** — har bir mahsulot, har biri qancha, qiymati
- **Harakatlar** — har bir kirim, sotuv, boshqa omborga ko'chirish
- **Inventarizatsiya** — javonlardagi haqiqiy holat tizimda ko'rsatilgan bilan solishtiriladi

## Maslahatlar

- **Boshlash uchun bitta asosiy ombor yetarli** — keyinroq qo'shishingiz mumkin.
- **Alohida "brak" ombor** oy oxiri balansini ancha osonlashtiradi.
- **Ombor turini ishlatishni boshlagandan keyin o'zgartirmang** — buning o'rniga yangisini yarating.

---

**Keyingi:** [Qoldiq va kirimlar →](./stock-and-purchases)
