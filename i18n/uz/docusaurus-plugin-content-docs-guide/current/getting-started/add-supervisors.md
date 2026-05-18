---
sidebar_position: 5
title: Supervayzer qo'shish
---

# Supervayzer qo'shish

**Supervayzer** bir guruh agentni nazorat qiladi. U boshqaruv panelida jamoa ishini jonli kuzatadi, maxsus narxlarni tasdiqlaydi va jamoa kunlik hisobotlarini ko'rib chiqadi.

## Qadam 1 — Supervayzerlar ro'yxatini oching

Menyudan **Команда → Супервайзеры** (Jamoa → Supervayzerlar) ni tanlang yoki to'g'ridan-to'g'ri `/team/supervisor` ni oching:

![Supervayzerlar ro'yxati](/screens/guide/17-supervisors-list.png)

Ro'yxat har bir supervayzerni telefoni, filiali va unga qaragan agentlar bilan ko'rsatadi.

## Qadam 2 — "Supervayzer qo'shish" tugmasini bosing

Yuqori o'ng burchakdagi **+ Добавить** tugmasini bosing. `/team/supervisor/create` manzilidagi forma ochiladi:

![Supervayzer qo'shish formasi](/screens/guide/30-add-supervisor-form.png)

## Qadam 3 — Formani to'ldiring

| Maydon | Nimani kiritish kerak |
|--------|----------------------|
| **Логин** | Qisqa login nomi (masalan, `sup.olim`) |
| **Пароль** | U bilan baham ko'radigan parol |
| **ФИО** | To'liq ism |
| **Телефон** | Ishlaydigan mobil raqam |
| **Филиал** | U tegishli bo'lgan filial |
| **Агенты** | Bu supervayzerga qaraydigan agentlarni belgilang |

## Qadam 4 — Saqlang

**Сохранить** tugmasini bosing. Supervayzer xuddi shu veb-ilovaga darhol kira oladi.

## Supervayzer nimalar qila oladi

| Amal | Qayerda |
|------|---------|
| Jonli jamoa ishini kuzatish | Boshqaruv paneli |
| Maxsus narxlarni tasdiqlash | Kutilayotgan buyurtmalar bildirishnomasi |
| Kunlik hisobotlarni ko'rib chiqish | Hisobotlar → Agentlar bo'yicha |
| Tashrif fotosuratlarini ko'rish | Audit → Fotohisobot |
| Agent KPI'sini kuzatish | Boshqaruv paneli / KPI hisoboti |

## Qadam 5 — Agentni boshqa supervayzerga o'tkazing

Agentni boshqa supervayzerga ko'chirish uchun:

1. **Yangi** supervayzerning profilini oching
2. **Агенты** tanlovida agentni toping
3. Belgilang va saqlang

Agent darhol yangi supervayzerga hisobot beradi. O'tmishdagi tarix o'sha paytda agentni boshqargan kishida qoladi.

:::tip Bitta agentga bitta supervayzer
Agent bir vaqtning o'zida faqat bitta supervayzerga hisobot beradi. Agar bir jamoani ikki kishi nazorat qilishini xohlasangiz, ularga **Menejer** rolini bering — menejerlar barcha agentlarni bir vaqtda ko'radi.
:::

---

**Keyingi:** [Ekspeditor qo'shish →](./add-expeditors)
