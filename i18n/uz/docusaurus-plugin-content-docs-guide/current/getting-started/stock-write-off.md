---
sidebar_position: 11
title: Qoldiqlarni hisobdan chiqarish
---

# Qoldiqlarni hisobdan chiqarish

Ba'zida tovar sotilmasdan omborni tark etishi kerak bo'ladi — muddati o'tgan, singan, yo'lda yo'qolgan yoki inventarizatsiyadagi nomuvofiqlikni tuzatyapsiz. **Hisobdan chiqarish** ("Списание" / Excretion) — buni rasmiy tarzda olib tashlash usuli.

## 1-qadam — Hisobdan chiqarishlar ro'yxatini oching

Menyudan **Ombor → Hisobdan chiqarish** (Склад → Списания) ni tanlang yoki to'g'ridan-to'g'ri `/stock/excretion` ni oching:

![Hisobdan chiqarishlar ro'yxati](/screens/guide/63-stock-write-off.png)

Siz hozirgacha qilingan barcha hisobdan chiqarishlarni ko'rasiz — kim, qachon, qaysi ombordan, nimani va qanday sabab bilan hisobdan chiqargan.

## 2-qadam — "Hisobdan chiqarish qo'shish" tugmasini bosing

O'ng yuqori burchakdagi **+ Qo'shish** tugmasini bosing. Forma uchta bo'lim bilan ochiladi:

- **Sarlavha** — Ombor, sana, sabab toifasi (muddati o'tgan / shikastlangan / yo'qolgan / inventarizatsiya tuzatishi)
- **Tovarlar jadvali** — nima hisobdan chiqarilmoqda
- **Izoh** — erkin matnli tushuntirish (tavsiya etiladi)

## 3-qadam — Sarlavhani to'ldiring

| Maydon | Nima kiritiladi |
|--------|-----------------|
| **Ombor** | Tovar hozir qayerda (brak / asosiy / furgon) |
| **Sana** | Hisobdan chiqarish qachon sodir bo'lgan |
| **Sabab** | Tanlang: muddati o'tgan, shikastlangan, yo'qolgan, inventarizatsiya tuzatishi, o'g'irlik |
| **Mas'ul** | Hisobdan chiqarishni imzolagan shaxs |

## 4-qadam — Tovarlarni qo'shing

Har bir pozitsiya uchun:
- Tovarni tanlang (yoki shtrix-kodni skanerlang)
- Olib tashlanadigan **miqdorni** kiriting
- **Qiymat** tovarning tannarxidan avtomatik hisoblanadi

Formada hisobdan chiqarilayotgan qiymatning joriy yig'indisi ko'rinadi — moliyaviy hisobot uchun foydali.

## 5-qadam — Saqlang

**Saqlash** tugmasini bosing. Ombor qoldig'i darhol yangilanadi:
- Miqdor manba ombordan yo'qoladi
- Moliyaviy hisobotlarda hisobdan chiqarish satri paydo bo'ladi
- Tannarx P&L ga zarar sifatida tushadi

## Keng tarqalgan sabablar va ularning ma'nosi

| Sabab | Qachon ishlatiladi |
|-------|--------------------|
| **Muddati o'tgan** (Просрочка) | Yaroqlilik muddati tugagan. Eng keng tarqalgan sabab. |
| **Shikastlangan** (Поломка) | Jismoniy zarar — shisha singan, qadoq ezilgan |
| **Yo'qolgan** (Утеря) | Inventarizatsiya paytida topilmadi, qayta tiklash kutilmaydi |
| **Tuzatish** (Корректировка) | Tizimda N dona ko'rsatilgan, lekin javonda N−2 bor edi; bu hisobni tenglashtiradi |
| **O'g'irlik** (Кража) | Tasdiqlangan o'g'irlik — odatda politsiyaga arizaga qo'shiladi |

## 6-qadam — Hisobotlarga ta'sirini ko'rib chiqing

Saqlangandan so'ng hisobdan chiqarish quyidagilarda ko'rinadi:
- **Ombor qoldig'i** — miqdorlar endi hisobdan chiqarishdan keyingi qoldiqlarni aks ettiradi
- **P&L hisoboti** — hisobdan chiqarilgan tovarlar tannarxi "yo'qotishlar" ostida paydo bo'ladi
- **Sabab bo'yicha hisobdan chiqarish hisoboti** — toifalar bo'yicha taqsimot ("oyiga muddati o'tishi sababli qancha yo'qotamiz?")

## Maslahatlar

- **Har doim izoh qo'shing** — moliya bo'limi "nega o'tgan oyda 500 000 so'mlik pivo hisobdan chiqarilgan?" deb so'raganda, izoh sizni qutqaradi.
- **Hisobdan chiqarishni oylik tartibda** o'tkazing — biror narsani sezgan paytda emas. Muddati tugashidan bir kun oldin muddati o'tgan tovarni ushlash — bu allaqachon kech.
- **Alohida "brak" ombori** ([Omborlarni sozlash](./set-up-warehouses) da ko'rib chiqilgan) hisobdan chiqarishni tozaroq qiladi — yaroqsiz tovar mijozdan qaytgan paytdan boshlab o'sha yerda yashaydi, keyin haftada bir marta yagona operatsiya bilan hisobdan chiqariladi.

---

**Keyingi:** [Birinchi buyurtmangizni yarating →](../daily-use/first-order)
