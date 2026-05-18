---
sidebar_position: 4
title: Agent qo'shish
---

# Savdo agentlaringizni qo'shing

Savdo **agentlari** — bu mijozlarga tashrif buyurib, buyurtma oladigan odamlar. Har bir agentga shaxsiy login kerak, shunda tashriflar va buyurtmalar to'g'ri qayd etiladi.

## Qadam 1 — Agentlar ro'yxatini oching

Menyudan **Команда → Агенты** (Jamoa → Agentlar) ni tanlang yoki to'g'ridan-to'g'ri `/agents/agent` ni oching:

![Agentlar ro'yxati — sahifaning tepasida amal tugmalari](/screens/guide/07-agents-list.png)

Ro'yxat jamoangizdagi har bir agentni telefoni, supervayzeri va faol holati bilan ko'rsatadi.

## Qadam 2 — "Agent qo'shish" tugmasini bosing

Ro'yxatning yuqori o'ng burchagida **+ Добавить агента** tugmasini toping. Forma ochiladi:

![Agent qo'shish formasi — barcha maydonlar](/screens/guide/29-add-agent-form.png)

## Qadam 3 — Formani to'ldiring

| Maydon | Nimani kiritish kerak |
|--------|----------------------|
| **Логин** | Qisqa login nomi (masalan, `agent.askar`) — agent shu bilan mobil ilovaga kiradi |
| **Пароль** | Agentga beradigan parol |
| **ФИО** | Hujjatlarda ko'rinishi kerak bo'lgan to'liq ism |
| **Телефон** | Ishlaydigan mobil raqam — SMS va parolni tiklash uchun |
| **Филиал** | Bu agent qaysi filial / ofisga tegishli |
| **Супервайзер** | Bu agentni kim nazorat qiladi (keyinroq o'zgartirilishi mumkin) |
| **Активен** | Yoniq qoldiring. Agent jamoadan ketganda o'chiring. |

## Qadam 4 — Saqlang

**Сохранить** (Saqlash) tugmasini bosing. Agent darhol ro'yxatda paydo bo'ladi va yangi login-parol bilan mobil ilovaga kira oladi.

## Qadam 5 — Marshrut yoki KPI rejasini sozlash (ixtiyoriy)

Agent profilidan endi quyidagilarni qilishingiz mumkin:

- **Haftalik tashrif marshrutini belgilash** — qarang [Tashriflarni rejalashtirish](../daily-use/plan-visits)
- **Oy uchun KPI maqsadlarini belgilash** — savdo, AKB, tashriflar — qarang [Boshqaruv paneli va KPI](../reports/dashboard-kpi)

## Qadam 6 — Agent profilini oching

Profilni ochish uchun ro'yxatdagi agent ismini bosing:

![Agent profili — KPI, marshrut va tarix bo'limlari](/screens/guide/47-agent-detail.png)

Bu yerda quyidagilarni qila olasiz:
- Telefon, login va supervayzerni o'zgartirish
- **KPI** bo'limini ochib oylik maqsadlarni belgilash
- **Marshrut** bo'limini ochib tashriflar rejasini sozlash
- Oxirgi sinxronizatsiya vaqti va qurilma ma'lumotini ko'rish

## Agent jamoadan ketganda

Akkauntni o'chirmang — bu uning tashrif va buyurtma tarixini o'chiradi. Buning o'rniga:

1. Agent profilini oching.
2. **Активен** ni o'chiring va saqlang.

Agent endi tizimga kira olmaydi, lekin uning barcha o'tmishdagi ma'lumotlari hisobotlarda ko'rinib turaveradi.

:::tip Bitta agent, bitta login
Har bir agentning shaxsiy logini bo'lishi kerak. Ikki kishi bitta loginni ulashishi buyurtmalar noto'g'ri kishi nomidan yozilishiga olib keladi.
:::

---

**Keyingi:** [Supervayzer qo'shish →](./add-supervisors)
