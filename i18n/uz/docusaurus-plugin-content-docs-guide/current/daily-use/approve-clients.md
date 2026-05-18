---
sidebar_position: 4
title: Yangi mijozlarni tasdiqlash
---

# Yangi qoʻshilgan mijozlarni tasdiqlash

Agent tashrif chogʻida mobil ilovadan yangi mijoz qoʻshganda, mijoz toʻgʻridan-toʻgʻri faol mijozlar roʻyxatiga emas, **tasdiqlash navbatiga** tushadi. Bu nazorat dubl, xato yozuv va oʻylab topilgan mijozlarni hisobotlaringizga kirib ketishidan oldin ushlaydi.

## 1-qadam — Tasdiqlash navbatini oching

Mijozlar roʻyxatida **Неподтвержденные клиенты** (Tasdiqlanmagan mijozlar) tugmasini bosing yoki toʻgʻridan-toʻgʻri `/clients/approval` manzilini oching:

![Tasdiqlanmagan mijozlar navbati](/screens/guide/62-clients-approval.webp)

Har bir qator — agent dalada yaratgan, ammo siz hali tekshirmagan mijoz.

## 2-qadam — Har bir yozuvni oʻqing

Odatda koʻrsatiladigan ustunlar:
- **Дата создания** (Yaratilgan sana) — agent yuborgan vaqt
- **Агент** (Agent) — kim yaratdi
- **Название** (Nomi) — nima yozgani
- **Телефон** (Telefon)
- **Адрес** (Manzil)
- **Координаты** (GPS koordinatalar) — avtomatik olinadi
- **Действия** (Amallar) — tasdiqlash / rad etish / birlashtirish

## 3-qadam — Muammolarni qidiring

Tasdiqlashdan oldin tekshiring:
- **Dublikatlar** — bir xil telefon yoki manzilli mijoz allaqachon bormi?
- **Xato yozuvlar** — «Магазин Юлдуз» va «Магазин Юлдус»
- **Oʻylab topilgan mijozlar** — GPS dala oʻrtasida, telefon yoʻq, umumiy nom
- **Notoʻgʻri kanal/hudud** — agent notoʻgʻri toifani tanlagan

Tepa qismidagi qidiruv oynasi bir xil telefon yoki nomli mijoz borligini soniyalarda tekshiradi.

## 4-qadam — Tasdiqlash, rad etish yoki birlashtirish

| Amal | Qachon foydalanish |
|--------|-------------|
| **Подтвердить** (Tasdiqlash) | Hammasi toʻgʻri, dubl topilmadi. Mijoz faol boʻladi. |
| **Отклонить** (Rad etish) | Oʻylab topilgan yoki tekshirib boʻlmaydi. Sababi bilan agentga qaytadi. |
| **Объединить** (Birlashtirish) | Mavjud mijoz bilan bir xil doʻkon. Birlashtiradi; mavjud mijoz yangi GPS va qoʻshimcha maydonlarni oʻziga oladi. |

Tasdiqlash — bir bosish, qator navbatdan yoʻqoladi.

## 5-qadam — Ommaviy tasdiqlash

Ishonchli agent 20 ta yaxshi toʻldirilgan mijoz yuborgan boʻlsa, hammasini bir vaqtda tanlab tasdiqlash mumkin:
1. Tanlash ustunidagi katakchalarga belgi qoʻying
2. Yuqoridagi **Групповая обработка → Подтвердить** tugmasini bosing

## Qachon tasdiqlash, qachon kutish kerak

| Vaziyat | Nima qilish kerak |
|-----------|-----------|
| Yaxshi obroʻli agent, oddiy koʻrinishdagi yozuv | Tasdiqlash |
| GPS doʻkonni shu yaqindagi oʻxshash nomli katta koʻchada koʻrsatmoqda | Avval qidiring; dubl boʻlsa birlashtiring |
| GPS koordinatalari turar joy binosi yoki boʻsh dalani koʻrsatmoqda | Rad eting va agentdan sababini soʻrang |
| Bir xil nom 3+ marta turli agentlardan kelyapti | Birlashtiring yoki rad eting — faqat bittasi haqiqiy |

## Maslahatlar

- **Har kunlik tekshirish** — toʻgʻri ritm: kechiktirsangiz navbat oʻsadi; tez-tez tekshirsangiz yarim toʻldirilgan yozuvlarga vaqt sarflaysiz.
- **Agentlarni GPS funksiyasidan foydalanishga oʻrgating** — koordinatalar tekshiruvni ancha tezlashtiradi.
- **Kanal va toifalarni oldindan belgilang**, agentlar mijoz yarata boshlashidan oldin — aks holda taxmin qilishadi.

---

**Keyingi:** [Mobil agent ilovasi →](../mobile/agent-app)
