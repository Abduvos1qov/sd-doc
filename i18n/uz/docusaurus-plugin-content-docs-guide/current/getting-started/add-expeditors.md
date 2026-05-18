---
sidebar_position: 6
title: Ekspeditor qo'shish
---

# Ekspeditor qo'shish

**Ekspeditor** mijozlarga buyurtmalarni yetkazib beradi — odatda mashinali haydovchi. Har kuni ertalab u mashinaga yuk ortadi, marshrut bo'ylab haydaydi, buyurtmalarni tushiradi va sotilmagan tovar yoki yig'ilgan pulni qaytarib olib keladi.

## Qadam 1 — Ekspeditorlar ro'yxatini oching

Menyudan **Команда → Экспедиторы** (Jamoa → Ekspeditorlar) ni tanlang yoki to'g'ridan-to'g'ri `/staff/view/expeditor` ni oching:

![Ekspeditorlar ro'yxati](/screens/guide/19-expeditors-list.webp)

Siz har bir ekspeditorni telefoni, biriktirilgan mashinasi va bugungi reys holati bilan ko'rasiz.

## Qadam 2 — "Ekspeditor qo'shish" tugmasini bosing

Yuqori o'ng burchakdagi **+ Добавить** tugmasini bosing. `/staff/create/expeditor` manzilidagi forma ochiladi:

![Ekspeditor qo'shish formasi](/screens/guide/31-add-expeditor-form.webp)

## Qadam 3 — Formani to'ldiring

| Maydon | Nimani kiritish kerak |
|--------|----------------------|
| **Логин** | Qisqa login nomi (masalan, `exp.rustam`) |
| **Пароль** | Baham ko'radigan parol |
| **ФИО** | To'liq ism |
| **Телефон** | Ishlaydigan mobil raqam |
| **Филиал** | Filial |
| **Машина** | Unga biriktirilgan mashina (ixtiyoriy, har kuni o'zgartirilishi mumkin) |

## Qadam 4 — Saqlang

**Сохранить** tugmasini bosing. Ekspeditor mobil ilovaga darhol kira oladi.

## Tipik ekspeditor kuni

| Vaqt | Nima sodir bo'ladi |
|------|--------------------|
| **Ertalab** | Omborda yuk olish — ilova bugungi buyurtmalarni ko'rsatadi, ekspeditor miqdorlarni tasdiqlaydi |
| **Yo'lda** | Har bir to'xtashda: tovarni topshirish, yetkazib berishni qayd etish, to'lov yig'ish, qaytarimlarni qayd etish |
| **Kun oxiri** | Sotilmagan tovarni qaytarish, naqd pulni kassirga topshirish — reys yopiladi |

Bularning hammasi sodir bo'lib turganida boshqaruv panelingizda jonli ko'rinib turadi.

## Qadam 5 — Reysni jonli kuzating

**Заявки → Рейсы** (Buyurtmalar → Reyslar) dan:

![Reyslar ko'rinishi — bugungi yetkazib berishlar](/screens/guide/20-trips-view.webp)

Har bir qator — bitta ekspeditorning reysi quyidagilar bilan:

- Yakunlangan to'xtashlar va rejalashtirilgan
- Mashinada ayni paytda turgan pul
- Oxirgi GPS signali
- Har qanday g'ayrioddiyliklar (uzun to'xtash, marshrutdan chiqish, o'tkazib yuborish)

## Maslahatlar

- **Bir ekspeditor — bir mashina — bir kun** eng toza sxemadir. Ikki ekspeditor bir mashinada yuk hisobini chalkashtiradi.
- **Agentlar va ekspeditorlar uchun loginlarni qayta ishlatmang**. Mobil ilova har bir rol uchun turli ekranlarni ko'rsatadi.
- **Faol bo'lmagan ekspeditorlar** — ekspeditor bo'shagan paytda (kasallik, ta'til, jamoadan ketish) profilda **Активен** ni o'chiring. Login ishlamay qoladi, lekin tarix qoladi.

---

**Keyingi:** [Mijoz qo'shish →](./add-clients)
