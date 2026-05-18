---
sidebar_position: 3
title: Ilovada harakatlanish
---

# Yo'lingizni topish

SalesDoctor har bir funksiyani oz sonli aniq menyularga guruhlaydi. Har bir menyu qayerda joylashganini bilsangiz, hech qachon istalgan joydan ikki bosishdan uzoq bo'lmaysiz.

## Qadam 1 — Yuqori panelni ko'ring

Har bir sahifaning tepasida:

![SalesDoctor boshqaruv paneli, yuqori panel ko'rinadi](/screens/guide/02-dashboard-home.png)

- **Logotip (yuqori chap)** — asosiy boshqaruv paneliga qaytaradi
- **Bildirishnoma qo'ng'irog'i** — yangi buyurtmalar, yakunlangan yetkazib berishlar, tasdiqlash so'rovlari
- **Akkaunt menyusi (yuqori o'ng)** — til, parol, chiqish

## Qadam 2 — Yon menyuni ko'ring

Chap menyu har bir asosiy ish maydonchasini sanab beradi:

| Menyu | Ichida nima bor | To'g'ridan-to'g'ri URL |
|-------|-----------------|------------------------|
| **Планы** | Tashriflar va savdo rejalashtirish | `/planning/monthly` |
| **Заявки** | Savdo, qaytarishlar, yetkazib berishlar | `/orders/list` |
| **Склад** | Omborlar, qoldiq, kirimlar | `/warehouse/list` |
| **Маркировка** | CIS / EDI talablari | `/markirovka/view/incomingInvoices` |
| **Клиенты** | Mijozlar ro'yxati, to'lovlar, qarzlar | `/clients/client` |
| **Команда** | Auditorlar, supervayzerlar, ekspeditorlar, foydalanuvchilar | `/team/auditor` |
| **Аудит 2** | Merchandayzing auditi | `/audit/photoReport` |
| **Настройки** | Narxlar, valyutalar, filiallar | `/settings/diler` |

:::tip Ko'rinmayotgan menyu bandlari
Agar menyu guruhi sizga ko'rinmasa, bu odatda roliingiz uchun zarur emasligini bildiradi. Administrator **Настройки → Доступ** orqali kirishni berishi mumkin.
:::

## Qadam 3 — To'g'ridan-to'g'ri URL'lardan foydalaning

Har bir sahifaning barqaror URL'i bor — tez-tez ishlatiladigan hisobotlarni xatcho'p qiling. Eng keng tarqalganlari:

| URL | Nimani ochadi |
|-----|---------------|
| `/dashboard/supervayzer` | Jamoaning bugungi boshqaruv paneli |
| `/dashboard/kpi` | Oylik KPI boshqaruv paneli |
| `/orders/list` | Buyurtmalar ro'yxati |
| `/orders/addOrder` | Yangi buyurtma formasi |
| `/clients/client` | Mijozlar ro'yxati |
| `/clients/finans` | Mijoz to'lovlari va qarzlari |
| `/report/agent` | Agent bo'yicha savdo hisoboti |
| `/report/customer` | Mijoz bo'yicha savdo hisoboti |

## Qadam 4 — Yangi yorliqda oching

Istalgan menyu bandida `Ctrl + Click` (Mac'da `Cmd + Click`) uni yangi brauzer yorlig'ida ochadi. Boshqaruv panelini ochiq ushlab boshqa hisobotda ishlamoqchi bo'lganda foydali.

## Qadam 5 — Tilni o'zgartiring

Akkaunt menyusini oching (yuqori o'ng) → **Язык** (Til). Tanlovingiz keyingi kirishda eslab qolinadi. Qo'llab-quvvatlanadiganlar: Русский, O'zbekcha, English.

## Qidiruv, filtrlar va yozuv tanlash

SalesDoctor'dagi har bir ro'yxat sahifasi bir xil uch qatlamli sxema bo'yicha qurilgan.

**1. Yuqori o'ngdagi qidiruv maydoni** — bir nechta belgi tering va jadval real vaqtda toraytiriladi. Istalgan matnli ustun bo'yicha ishlaydi (mijoz nomi, agent ismi, login, mahsulot nomi, buyurtma raqami).

**2. Sarlavha ostidagi filtrlar paneli** — ko'p tanlovli ochiluvchi ro'yxatlar. Ochiluvchi ro'yxatni bossangiz, belgilanadigan ro'yxat ochiladi; bir yoki bir nechta qiymatni tanlang. Jadval darhol yangilanadi.

![Mijozlar ro'yxatining yoyilgan filtrlar paneli](/screens/guide/45-clients-filter-panel.png)

**3. Forma ichidagi tanlash oynasi** — forma mavjud yozuvni (mijoz, mahsulot, ombor) tanlashni talab qilganda, o'z qidiruv maydoniga ega sahifalangan jadval ochiladi:

![Mijoz tanlash oynasi — qidiruvli sahifalangan jadval](/screens/guide/40-client-picker.png)

Bir nechta qoidalar:

- Qidiruv **qism-satr** bo'yicha mos keladi — `мага` *Магазин Юлдуз*, *Магистраль*, *Гранд-Мага*'ni topadi.
- Filtrlar **birlashadi** — Hudud = Toshkent VA Kanal = supermarket tanlanganda ikkala shartga mos keladigan nuqtalargacha toraytiriladi.
- Filtr holati URL'da saqlanadi — URL'ni nusxalab bering va hamkasbingiz aynan sizning ko'rinishingizni oladi.
- **Сбросить фильтр** (Filtrni tashlash) barcha filtrlarni bir vaqtda tozalaydi.

## Maslahatlar

- **Barqaror URL'lar** — tez-tez ishlatiladigan sahifalarni xatcho'p qiling.
- **Brauzerning orqaga tugmasi** hamma joyda ishlaydi — ilova ichida alohida "orqaga" tugmasiga ehtiyoj yo'q.
- **Uzoq turgandan keyin yangilang** — ma'lumot eskirgan ko'rinsa, `F5` bosing.

---

**Keyingi:** [Agent qo'shish →](./add-agents)
