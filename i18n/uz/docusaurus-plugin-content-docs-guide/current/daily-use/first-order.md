---
sidebar_position: 1
title: Birinchi buyurtmangizni yarating
---

# Birinchi buyurtmangizni yarating

Endi sizda agentlar, mijozlar va qoldiq bor — buyurtma rasmiylashtirishga tayyorsiz. Buyurtmalar uch joydan keladi: **mobil ilova** (buyurtmalarning ko'pi), **veb-ilova** (ushbu sahifa) yoki **onlayn portal**.

## Qadam 1 — Buyurtmalar ro'yxatini oching

Menyudan **Заявки → Список заявок** (Buyurtmalar → Buyurtmalar ro'yxati) ni tanlang yoki to'g'ridan-to'g'ri `/orders/list` ni oching:

![Buyurtmalar ro'yxati — bugungi va so'nggi buyurtmalar](/screens/guide/03-orders-list.webp)

Har bir ustun filtrlash mumkin — holat, agent, mijoz, sana, ombor.

## Qadam 2 — "Yangi buyurtma" tugmasini bosing

Yuqori o'ng burchakdagi **+ Добавить** tugmasini bosing. Siz `/orders/addOrder` manzilidagi yangi buyurtma formasiga tushasiz:

![Yangi buyurtma formasi — sarlavhadan jadvalgacha to'liq ko'rinish](/screens/guide/33-new-order-empty.webp)

Forma uchta bo'lakdan iborat: **sarlavha** (mijoz, agent, sanalar), **mahsulotlar jadvali** va pastdagi **jami yig'indi qatori**.

## Qadam 3 — Mijozni tanlang

**Клиент** (Mijoz) maydonchasiga mijoz nomini yozishni boshlang. Takliflar 2–3 harfdan keyin paydo bo'ladi. To'g'risini tanlang.

Tizim avtomatik tarzda quyidagilarni to'ldiradi:

- **Тип цены** (Narx turi) — bu mijoz uchun narx ro'yxati
- **Условия оплаты** (To'lov shartlari)
- **Кредитный лимит** (Kredit limiti)

Mijoz tanlovi — bu sahifalangan jadval. Standart holatda sotuv qila oladigan barcha mijozlarning birinchi 10 tasi ko'rsatiladi:

![Mijoz tanlovi — barcha mijozlarning to'liq jadvali](/screens/guide/40-client-picker.webp)

Yuqoridagi **Поиск** (Qidiruv) maydoniga mijoz nomining istalgan qismini yozing. Jadval real vaqtda toraytiriladi:

![Mijoz tanlovi "мага" filtri bilan — torayagan ro'yxat](/screens/guide/41-client-picker-search.webp)

Tasdiqlash uchun qatorni bosing. Tanlov oynasi yopiladi va buyurtma formasi mahsulotlar jadvaliga o'tadi.

## Qadam 4 — Mahsulotlarni qo'shing

Har bir mahsulot uchun:

1. Mahsulot nomini yozing yoki shtrix-kodini skanerlang
2. **Количество** (miqdorni) belgilang
3. **Цена** (narx) narx ro'yxatidan avtomatik to'ldiriladi

Qatorlarni qo'shganda pastda joriy umumiy summa yangilanib boradi.

:::tip Chegirmalar va bonuslar
Administratoringiz chegirma qoidalari yoki "X olganga Y bepul" aksiyalarini sozlagan bo'lsa, ular avtomatik qo'llanadi. Chegirma jamida ko'rinadi — o'zingiz hech narsani hisoblash shart emas.
:::

## Qadam 5 — Yetkazib berish parametrlarini tanlang

- **Дата отгрузки** (Yetkazib berish sanasi) — tovar mijozga qachon yetishi kerak
- **Склад** (Ombor) — tovar qayerdan jo'natiladi (eng yaqini standart bo'ladi)
- **Экспедитор** (Ekspeditor) — kim yetkazib beradi (keyinroq biriktirish mumkin)

## Qadam 6 — Saqlang

**Сохранить** (Saqlash) tugmasini bosing. Buyurtma **Yangi** holatiga o'tadi va darhol buyurtmalar ro'yxatida paydo bo'ladi:

![Buyurtmalar ro'yxati eng tepada yangi buyurtma bilan](/screens/guide/03-orders-list.webp)

## Qadam 7 — Buyurtmani bosqichlar bo'ylab kuzating

Buyurtmalar ro'yxatidan yangi buyurtmangiz quyidagi bosqichlardan o'tadi:

1. **Yangi** — endigina yaratilgan
2. **Yuklangan** — ekspeditor mashinasida
3. **Yetkazilgan** — mijozga topshirilgan
4. **Yopilgan** — to'langan (yoki qarzga o'tkazilgan)

Tafsilotlarini, yetkazib berishda olingan fotosuratlarni va to'lov holatini ko'rish uchun istalgan bosqichda buyurtma qatorini bosishingiz mumkin.

## Maslahatlar

- **Katta buyurtmani saqlashdan oldin mijoz qarzini tekshiring** — yangi buyurtma mijozni kredit limitidan oshirsa, qizil ogohlantirish paydo bo'ladi.
- **Narxlarni qo'lda tahrir qilmang**, agar chegirma qoidalari talab qilmasa — narx ro'yxati haqiqat manbai.
- **Maxsus ko'rsatmalar uchun izoh qoldiring** ("orqa eshikni chaling", "Salimni so'rang").

---

**Keyingi:** [Tashriflarni rejalashtirish →](./plan-visits)
