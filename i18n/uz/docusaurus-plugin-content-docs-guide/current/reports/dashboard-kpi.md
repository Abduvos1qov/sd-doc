---
sidebar_position: 1
title: Boshqaruv paneli va KPI
---

# Boshqaruv paneli va KPI

Boshqaruv paneli — biznesingiz puls'i: kunning eng muhim raqamlari bir joyda. Bir necha hafta real ish ma'lumotlaridan keyin boshqaruv paneli biznes qanday borayotganini ko'rishning eng yaxshi vositasiga aylanadi. **Har bir plitka bosiladi** va batafsil ko'rinishni ochadi.

## Qadam 1 — Bosh boshqaruv panelini oching

Menyudan **logotip** (yuqori chap) tugmasini bosing yoki to'g'ridan-to'g'ri `/dashboard/supervayzer`ni oching:

![Supervayzer bosh boshqaruv paneli — KPI plitkalari va agentlar jadvali](/screens/guide/39-supervisor-dashboard-full.webp)

Sahifa uch zonadan iborat:

1. **Yuqoridagi plitkalar** — bugungi eng muhim raqamlar
2. **O'rta grafiklar** — davr bo'yicha dinamika (tashriflar, sotuv, qaytarish)
3. **Pastdagi agentlar jadvali** — har bir agentning kun davomidagi natijasi

## Qadam 2 — "Продажи" (Sotuv) plitkasini oching

**Sotuv** plitkasini bosing (yoki to'g'ridan-to'g'ri `/dashboard/sales`). Sotuvga oid boshqaruv paneli ochiladi:

![Sotuv batafsil — agent, mintaqa va mahsulot guruhi bo'yicha](/screens/guide/34-dashboard-sales.webp)

Quyidagilarni ko'rasiz:
- **Agent**, **mintaqa**, **mahsulot guruhi** bo'yicha sotuv yig'indilari
- **Grafiklar qatori** — bugun va o'tgan haftaning shu kuni taqqoslangan holatda
- **Top mijozlar** xarid hajmi bo'yicha
- **Qaytarishlar** alohida qator — nima qaytganini bilish ham, nima ketganini bilish kabi muhim

## Qadam 3 — "Финансы" (Qarz / Moliya) plitkasini oching

**Qarz** plitkasini bosing (yoki `/dashboard/finans`):

![Moliya batafsil — qarzlar, tushumlar, kassa yig'indilari](/screens/guide/35-dashboard-finans.webp)

Bu ekranda jamlangan:
- **Umumiy debet qarz** — mijozlar sizga qancha qarzdor, muddati bo'yicha bo'lingan
- **Bugungi tushumlar** — kassa va to'lov usuli bo'yicha
- **Qarz yosh guruhlari** — 7 kungacha, 7–30 kun, 30+ kun
- **Top qarzdorlar** — bugungi qo'ng'iroqlar ro'yxati

Istalgan qatorni bosish mijozning to'liq tranzaksiya tarixini ochadi.

## Qadam 4 — "Визиты" (Tashriflar) plitkasini oching

**Tashriflar** plitkasini bosing yoki `/report/visit`'ni oching:

![Tashriflar hisoboti — agent bo'yicha qamrov xaritasi](/screens/guide/37-report-visit.webp)

Tashriflar hisoboti bir vaqtning o'zida ikkita savolga javob beradi:
- **Qamrov** — rejalashtirilgan mijozlarning qanchasiga agent yetib bordi
- **Sifat** — qancha turdi, nima qayd etdi (buyurtma, foto), kimni o'tkazib yubordi (sabab bilan)

## Qadam 5 — Oylik KPI boshqaruv panelini oching

Butun jamoa uchun oylik ko'rinishni ko'rish uchun `/dashboard/kpi`'ni oching:

![Oylik KPI boshqaruv paneli — har bir agent uchun progress satrlari](/screens/guide/38-dashboard-kpi-full.webp)

Bu agentlar bo'yicha oylik progress ekrani. Har agentning o'z qatori, har bir ko'rsatkich uchun progress satri.

## Qadam 6 — Har bir KPI nimani anglatadi

KPI boshqaruv panelidagi tipik ko'rsatkichlar:

| KPI | Nimani o'lchaydi |
|-----|------------------|
| **Sotuv rejasi** | Agent oyda buyurtmalarda qancha pul keltirishi kerak |
| **AKB** | Agent qancha faol mijozni saqlayapti |
| **OKB** | Agent umuman qancha mijozga borib chiqqan |
| **Tashriflar rejasi** | Kunlik yoki oylik tashriflar soni |
| **MML** | "Must-Match List" — har do'konda bo'lishi shart bo'lgan mahsulotlar |
| **Foto reja** | Tashrif boshiga audit fotolari soni |

2–3 ko'rsatkich yetarli — ko'p qo'yish e'tiborni tarqatadi.

## Qadam 7 — Agentga maqsad qo'ying

1. Agent profilini oching (**Команда → Агенты** → ismini bosing)
2. **KPI** yorlig'ini oching
3. Har bir ko'rsatkich uchun **oyga maqsadni** belgilang
4. **Сохранить** tugmasini bosing

Agent darhol mobil ilovaning bosh ekranida o'z maqsadini va progress satrini ko'radi.

## Oy oxiri bonus hisobi

Agar bonuslar KPI'ga bog'lansa:

1. Oy oxirgi ish kunida KPI raqamlari muzlatiladi
2. Har bir agentning bonusi siz qo'ygan maqsadlarga nisbatan hisoblanadi
3. Natija KPI hisobotida paydo bo'ladi — moliya bo'limi maoshga olib boradi

## Maslahatlar

- **Agent boshqarsa oladigan KPI'larni tanlang** — agar omborda mahsulot doim qolmasa, past sotuv uchun jazolash agentlarning motivatsiyasini buzadi.
- **Ikki-uch KPI — tepa chegara** — beshtadan ko'p ko'rsatkich e'tiborni tarqatadi.
- **KPI'ni agentning telefon bosh ekranida ko'rsating** — shu narsaning o'zi xulqni o'zgartiradi.
- **Hamma narsani bosing** — boshqaruv panelidagi har bir raqam batafsil hisobotga olib boradi. Raqam qaerdan kelganini bilmoqchi bo'lsangiz, ustiga bosing.

---

**Keyingisi:** [Sotuv va qarzlar →](./sales-and-debts)
