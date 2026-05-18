---
sidebar_position: 2
title: Savdo va qarzlar
---

# Savdo va qarzlar

Eng ko'p ishlatiladigan ikki hisobot ikkita oddiy savolga javob beradi: **biz qancha sotdik?** va **bizga kim qarzdor?**

## Biz qancha sotdik?

### Qadam 1 — Agent savdo hisobotini oching

Menyudan **Отчеты → По агентам** (Hisobotlar → Agentlar bo'yicha) ni tanlang yoki to'g'ridan-to'g'ri `/report/agent` ni oching:

![Agent savdo hisoboti — filtrlar va jadval](/screens/guide/12-report-agent.png)

### Qadam 2 — Sanalar oralig'ini tanlang

Yuqori filtr qatorida:

- **Период** (Davr) — sana diapazonini tanlang (bugun / shu hafta / shu oy / boshqa)
- **Филиал** (Filial) — bitta ofisga toraytirish
- **Супервайзер** (Supervayzer) — bitta jamoaga toraytirish
- **Категория клиента** (Mijoz kategoriyasi) — A/B/C darajalari filtri

Agent hisoboti sahifasidagi filtrlar qatori shunday ko'rinadi:

![Hisobot filtrlar qatori — mavjud filtrlarning to'liq to'plami](/screens/guide/46-report-filter-strip.png)

Filtrlar birgalikda ishlaydi — har biri hisobotni yanada toraytiradi. O'zgartirgandan so'ng yangilash uchun **Сформировать** (Yaratish) tugmasini bosing.

### Qadam 3 — "Сформировать" (Yaratish) tugmasini bosing

Jadval har bir agentga bir qator bilan yangilanadi. Ustunlar:

- Jami savdo
- Buyurtmalar soni
- Tashrif buyurilgan mijozlar soni (OKB)
- Buyurtma bergan mijozlar soni (AKB)
- O'rtacha chek

### Qadam 4 — Bitta agentning ichiga kiring

Davr uchun uning buyurtmalari, tashriflari va fotosuratlarini ko'rish uchun agent qatorini bosing.

### Qadam 5 — Excel'ga eksport qiling

Yuqori o'ng burchakdagi **Excel** tugmasi ko'rayotgan jadvalingizni eksport qiladi — bir xil ustunlar, bir xil filtrlar.

## Bizga kim qarzdor?

### Qadam 1 — Mijoz to'lovlarini oching

Menyudan **Клиенты → Оплаты** (Mijozlar → To'lovlar) ni tanlang yoki to'g'ridan-to'g'ri `/clients/finans` ni oching:

![Mijoz to'lovlari va qarzlari](/screens/guide/13-client-payments.png)

Siz har bir mijozni joriy balansi bilan ko'rasiz — musbat qarz, nol esa toza degani.

### Qadam 2 — Yosh bo'yicha filtrlang

Yuqoridagi yosh guruhlari quyidagilarga e'tibor qaratishga imkon beradi:

- **7 kundan kam** — yangi qarz, odatda osongina qaytariladi
- **7–30 kun** — qo'ng'iroq qilish kerak
- **30+ kun** — keskinlashtirish kerak

### Qadam 3 — To'lovni qayd eting

Mijoz sizga to'laganda (naqd, bank o'tkazmasi yoki shaxsan):

1. Mijoz kartochkasini ochish uchun qatorini bosing
2. **+ Добавить оплату** (To'lov qo'shish) ni bosing
3. Kiriting:
   - **Сумма** (Summa)
   - **Тип** (Turi: naqd / karta / bank o'tkazmasi)
   - **Дата** (Sana)
   - **Касса** (Kassa) — sizning kassangiz
4. **Сохранить** ni bosing

Qarz darhol tushadi. Agar naqd pul ekspeditordan kelgan bo'lsa, kassir uni kun oxirida tasdiqlaydi.

### Qadam 4 — Ekspeditorlardan naqd pulni tasdiqlang (kassir jarayoni)

Yetkazib berishda naqd pul olsangiz:

1. **Платежи → На утверждение** (To'lovlar → Tasdiqlashga) ni oching
2. Har bir qator — ekspeditor bugun qayd etgan naqd to'lov
3. Naqd pulni sanang, **Утверждено** (Tasdiqlandi) ni belgilang
4. To'lovlar endi qarz hisobotida tushirilgan deb ko'rinadi

## Maslahatlar

- **Qarz hisobotini har hafta yurgizing** — 7 kungacha kichik qarzlar oson; 30 kundan eski qarzlar to'liq qaytib kelmaydi.
- **Qarzni hisobdan o'chirganda sababini doim qayd eting** — moliyachi keyinroq so'raganida, izoh sizni qutqaradi.
- **Yosh guruhlaridan foydalaning** qo'ng'iroqlarni tartiblash uchun — 30+ kun guruhidan boshlang.

---

**Keyingi:** [Onlayn buyurtmalar →](./online-orders)
