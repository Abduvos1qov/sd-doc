---
sidebar_position: 7
title: Mijoz qo'shish
---

# Mijoz qo'shish

SalesDoctor'da **mijoz** — bu siz tovar sotadigan istalgan joy — do'kon, restoran, kiosk, supermarket. Har bir buyurtma, qarz, tashrif va KPI mijozga bog'lanadi, shuning uchun bu ro'yxat tizimingizning yuragidir.

## Qadam 1 — Mijozlar ro'yxatini oching

Menyudan **Клиенты → Все клиенты** (Mijozlar → Barcha mijozlar) ni tanlang yoki to'g'ridan-to'g'ri `/clients/client` ni oching:

![Mijozlar ro'yxati — qidiruv qatori, filtrlar va jadval](/screens/guide/05-clients-list.png)

Ro'yxat har bir mijozni telefoni, manzili, kanali va kredit balansi bilan ko'rsatadi.

## Qadam 2 — Mavjud mijozni filtrlash yoki qidirish

Takroriy yozuv qo'shishdan oldin yuqori qidiruv maydonchasida ism yoki telefon bo'yicha qidiring. Agar mijoz allaqachon mavjud bo'lsa, ochish va tahrirlash uchun uning qatorini bosing.

## Qadam 3 — "Mijoz qo'shish" tugmasini bosing

Yuqori o'ng burchakdagi **+ Добавить** (Qo'shish) tugmasini bosing.

## Qadam 4 — Asosiy ma'lumotlarni to'ldiring

| Maydon | Nimani kiritish kerak |
|--------|----------------------|
| **Название** | Do'kon yoki biznesning rasmiy nomi |
| **Телефон** | Ishlaydigan raqam (SMS va buyurtma tasdiqlari uchun) |
| **Адрес** | Agent eshikdan o'qiy oladigan ko'cha manzili |
| **Регион / Территория** | Geografik joylashuv |
| **Канал** | Savdo nuqtasi turi — do'kon, supermarket, restoran, kafe |
| **Тип цены** | Bu mijoz qaysi narx ro'yxati bo'yicha sotib oladi |
| **Агент** | Bu mijozga tashrif buyuradigan mas'ul agent |

## Qadam 5 — Joylashuv qo'shing (tavsiya etiladi)

Agar agent hozir do'konda bo'lsa, **mobil ilova** GPS joylashuvini bir tegish bilan oladi. Vebdan kenglik/uzunlik koordinatalarini joylashtirishingiz yoki xaritada bosishingiz mumkin.

Yaxshi GPS keyinroq tashrifni avtomatik tekshirishga imkon beradi.

## Qadam 6 — Savdo shartlarini belgilang (ixtiyoriy)

- **Тип оплаты** — yetkazib berishda naqd, kreditga yoki bank o'tkazmasi
- **Кредитный лимит** — do'kon bir vaqtning o'zida qarzdor bo'la oladigan maksimal summa

## Qadam 7 — Saqlang

**Сохранить** (Saqlash) tugmasini bosing. Mijoz darhol ro'yxatda paydo bo'ladi va yangi buyurtmalar uchun mavjud bo'ladi.

## Bir nechta mijozni bir vaqtda qo'shish

Agar sizda Excel'da mavjud ro'yxat bo'lsa, `/clients/client/import` manzilidagi import sahifasidan foydalaning:

![Mijozlarni Excel orqali import qilish](/screens/guide/32-clients-import.png)

Shablonni yuklab oling, to'ldiring va orqaga yuklang — har bir qator bir o'tishda mijozga aylanadi.

## Mijozlar maydondan qo'shilganda

Mijozlarning ko'pchiligi agentlar tashrif paytida qo'shadi. Agent telefonida **+ Добавить клиента** ni bosadi, joylashuv avtomatik tarzda olinadi va yangi mijoz bir necha soniyada ofisda paydo bo'ladi.

:::tip Toza nomlar
"Магазин 'Yulduz', ул. Навои 10" "MAGAZIN YULDUZ NAVOI 10" ga qaraganda yaxshiroq o'qiladi. Nom qancha toza bo'lsa, qidirish shuncha oson.
:::

---

**Keyingi:** [Omborlarni sozlash →](./set-up-warehouses)
