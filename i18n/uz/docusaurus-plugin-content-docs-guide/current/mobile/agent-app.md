---
sidebar_position: 1
title: Agentning mobil ilovasi
---

# Agentlar telefonida nimani ko'radi

Savdo agentlaringiz deyarli barcha ishlarini telefondan bajaradi. SalesDoctor mobil ilovasi bitta vazifa uchun yaratilgan: mijozlarga tashrif buyurish, buyurtma olish va ofisga xabar berish — hatto internet zaif yoki umuman bo'lmasa ham.

## Ilovani olish

Agentlar **SalesDoctor** ni Play Store yoki App Store'dan yuklab oladi. O'rnatgandan keyin ular [Agent qo'shish](../getting-started/add-agents) bo'limida yaratgan login va parol bilan kiradi.

## Agent kuni qanday ko'rinadi

| Qadam | Agent telefonda nima qiladi |
|-------|----------------------------|
| **1. Marshrutni oching** | Bugungi ro'yxatdagi birinchi mijozni bosadi |
| **2. Do'konga yetib boring** | Ilova GPS'ni avtomatik oladi; tashrif boshlanadi |
| **3. Buyurtma oling** | Mahsulotlarni tanlaydi, miqdorlarni belgilaydi — narxlar avtomatik to'ldiriladi |
| **4. (Ixtiyoriy) Audit** | Javon fotosuratlarini oladi, savol-javoblarga javob beradi |
| **5. Tashrifni yoping** | **Готово** ni bosadi. Tashrifga to'sqinlik qilsa, sababni tanlaydi |

Agar signal bo'lsa, buyurtma darhol ofisga sinxronlanadi — yoki navbatda turadi va telefon onlaynga qaytganda sinxronlanadi.

## Ular ishlayotganda ofisda nimani ko'rasiz

Boshqaruv panelingizda real vaqtda quyidagilarni ko'rasiz:

![Jonli jamoa jarayoni bilan boshqaruv paneli](/screens/guide/02-dashboard-home.png)

- Har bir agent xaritada qayerda
- Qaysi mijozlarga borgan
- Qaysi mijozlarni o'tkazib yuborgan (sababi bilan)
- Bugun rasmiylashtirilgan har bir buyurtma

## Oflayn ishlash

Ilova quyidagilarning nusxasini telefonning o'zida saqlaydi:

- Agent marshruti
- Har bir mijoz tafsilotlari va narx ro'yxati
- Rasm va qoldiq bilan har bir mahsulot
- Bugun olingan har bir buyurtma

Shuning uchun signal bo'lmasa ham agent buyurtma olishni davom ettira oladi. Qopalanish qaytgan zahoti hammasi avtomatik sinxronlanadi.

## Qadam 1 — Sinxronizatsiya holatini tekshiring (ofisda)

Sinxronizatsiyani tasdiqlash uchun maxsus ekran kerak emas — agentning buyurtmasi tushgan zahoti `/orders/list` da paydo bo'ladi. Agar kutilgan buyurtmalarni ko'rmasangiz, agent telefoni qoplama tashqarisidadir.

## Qadam 2 — KPI jarayonini kuzating

Har bir agentning oylik jarayonini ko'rish uchun `/dashboard/kpi` ni oching:

![Oylik KPI boshqaruv paneli](/screens/guide/22-dashboard-kpi.png)

Jarayon chiziqlari agent telefonida ko'radigan narsa bilan mos keladi — ular real vaqtda har bir maqsaddan qancha uzoq ekanini biladi.

## Maslahatlar

- **Bir qurilmaga bitta login** — ilova agentni haftalar davomida tizimda ushlab turadi.
- **Telefonni kechasi quvvatlang** — GPS + mobil ma'lumotlar messenjer ilovalaridan tezroq batareyani sarflaydi.
- **Ilovani yangilang** taklif qilinganda — har oyda muhim yangi imkoniyatlar keladi.

---

**Keyingi:** [Tashriflar va auditlar →](./visit-and-audit)
