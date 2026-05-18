---
sidebar_position: 2
title: Tashriflar va auditlar
---

# Tashriflar va auditlar

**Tashrif** shunchaki buyurtma emas. Agent do'konda turganida u javon fotosuratlarini ham olib, savol-javoblarga javob berib va narxlarni tasdiqlab oladi. Bularning hammasi birga **audit** deyiladi — va bu har bir savdo nuqtasidagi brendingiz mavjudligini boshqarish uchun oltindan qimmat.

## Agent telefonda nima qiladi

| Qadam | Nima sodir bo'ladi |
|-------|--------------------|
| **1. Do'konga yetib boring** | Mobil ilova GPS'ni avtomatik oladi va tashrifni boshlangan deb belgilaydi |
| **2. Buyurtma oling** | Mahsulotlarni tanlaydi, miqdorlarni belgilaydi, narxlar avtomatik to'ldiriladi |
| **3. Javonlarni suratga oling** | Ilova qoidalarni ko'rsatadi (markazda, aniq fokusda) |
| **4. Belgilangan joylarni suratga oling** | Muzlatgich, kassa, kirish — siz sozlagan narsalar |
| **5. Savol-javoblarga javob bering** | Ha/yo'q, ko'p tanlovli yoki qisqa matn |
| **6. Do'kon narxlarini tasdiqlang** | Tezkor narx auditi |
| **7. "Готово" ni bosing** | Tashrif yopildi, ma'lumotlar ofisga sinxronlanadi |

Butun jarayon har bir do'konda 2–3 daqiqa oladi.

## Qadam 1 — Fotohisobotni oching (ofisda)

Menyudan **Аудит → Фотоотчет** (Audit → Fotohisobot) ni tanlang yoki to'g'ridan-to'g'ri `/audit/photoReport` ni oching:

![Fotohisobot — bugun har bir agent olgan har bir surat](/screens/guide/15-audit-photoreport.png)

## Qadam 2 — Filtrlarni qo'llang

Yuqori filtr qatori:

- **Дата** (Sana) — bitta kun yoki diapazon
- **Агент** (Agent) — bir yoki bir nechta
- **Клиент** (Mijoz) — aniq savdo nuqtasiga kiring
- **Тип фото** (Surat turi) — muzlatgich / javon / kirish va h.k.

## Qadam 3 — Bitta suratni ko'rib chiqing

Kattalashtirish uchun suratni bosing. Tafsilot ko'rinishidan siz quyidagilarni qila olasiz:

- **Tasdiqlash** — surat yaxshi, agent KPI uchun ball oladi
- **Rad etish** — surat noaniq yoki noto'g'ri burchakdan; agent ilovada izoh oladi va surat hisobga olinmaydi
- **Izoh qo'shish** — agent uchun tushuntirish

## Qadam 4 — Tendensiyalarni aniqlang

Vaqt o'tishi bilan javon ko'rinishi qanday o'zgarayotganini ko'rish uchun sana diapazoni slayderidan foydalaning. Tez-tez kuzatiladigan narsalar:

- Raqobatchilar faolligi (yangi posterlar, yangi muzlatgichlar)
- Qoldiq tugashi signallari (sizning mahsulotingiz turishi kerak bo'lgan bo'sh javon)
- Narx siljishlari (do'kon juda past yoki juda yuqori narx qo'ymoqda)

## Auditlar nima uchun muhim

| Auditsiz | Audit bilan |
|----------|-------------|
| Faqat qancha sotganingizni ko'rasiz | *Nima uchun* sotganingizni (yoki sotmaganingizni) ko'rasiz |
| Marketing o'zgarishlari sezilmay qoladi | Yangi poster keyingi fotohisobotda paydo bo'ladi |
| Raqobatchilar jimgina javon joyini egallaydi | Siz buni xuddi shu hafta sezasiz |
| "Men buni hech qachon olmaganman" deb bahslar bo'ladi | Surat masalani ikki soniyada hal qiladi |

## Maslahatlar

- **Kichikdan boshlang** — uch yoki to'rtta surat turi yetarli. Bir tashrifga 20 ta surat so'ramang; sifat tushadi.
- **"Yaxshi" nima ekanini aniqlang** — jamoa bilan bitta a'lo darajadagi suratni baham ko'ring, ular shunga mos keladi.
- **Rad etish izohlaridan izchil foydalaning** — bir haftadan keyin jamoadagi surat sifati sezilarli darajada yaxshilanadi.

---

**Keyingi:** [Ekspeditor yetkazib berishi →](./expeditor-delivery)
