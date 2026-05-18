---
sidebar_position: 9
title: Qoldiq va kirimlar
---

# Qoldiq va kirimlar

Omborlar yaratilgandan keyin ularga tovar joylash kerak. Ushbu sahifa kundalik ikkita vazifani qamrab oladi: yetkazib beruvchidan **kirimni qabul qilish** va istalgan ombordagi **qoldiqni tekshirish**.

## Yetkazib beruvchidan qoldiqni qabul qilish

### Qadam 1 — Kirimlar ro'yxatini oching

Menyudan **Склад → Поступления** (Ombor → Kirimlar) ni tanlang yoki to'g'ridan-to'g'ri `/warehouse/view/listPurchase` ni oching:

![Kirimlar ro'yxati — yetkazib beruvchining har bir kirimi](/screens/guide/09-purchases-list.webp)

Siz har bir yetkazib beruvchining kirimini — sana, yetkazib beruvchi, ombor, umumiy summa, holatini ko'rasiz.

### Qadam 2 — "Kirim qo'shish" tugmasini bosing

Yuqori o'ng burchakda **+ Добавить** (yoki **+ Новое поступление**) ni bosing.

### Qadam 3 — Sarlavhani to'ldiring

- **Поставщик** (Yetkazib beruvchi) — ro'yxatdan tanlang (yoki yangisini qo'shing)
- **Склад** (Ombor) — tovar qayerga boradi
- **Дата** — yetkazib berish sanasi
- **Номер документа** — yetkazib beruvchining hujjat raqami (qog'oz bilan mos keladi)

### Qadam 4 — Mahsulotlarni qator-qator qo'shing

Yetkazib berishdagi har bir mahsulot uchun:

- Mahsulot nomini yozing yoki shtrix-kodini skanerlang
- **Qabul qilingan miqdorni** kiriting
- **To'langan narxni** kiriting (birlik uchun)

### Qadam 5 — Tasdiqlang

**Сохранить и подтвердить** (Saqlash va tasdiqlash) tugmasini bosing. Qoldiq darhol mavjud bo'ladi — agentlar bu mahsulotlarni buyurtmalarga qo'shishi mumkin.

:::tip Hujjat raqami mos bo'lsin
Sizning kirim hujjatingizdagi raqam yetkazib beruvchining hujjat raqamiga mos kelishi kerak. Yetkazib berish bo'yicha bahs bo'lsa, ikkala tarafda bir xil raqamlar suhbatni soddalashtiradi.
:::

## Qoldiqni tekshirish

### Qadam 1 — Qoldiq hisobotini oching

**Склад → Остатки** (Ombor → Qoldiqlar) ni tanlang yoki to'g'ridan-to'g'ri `/stock/report` ni oching:

![Qoldiq hisoboti — mahsulotlar × omborlar](/screens/guide/10-stock-report.webp)

### Qadam 2 — Filtrlarni qo'llang

Quyidagilar bo'yicha filtrlang:

- **Ombor** — faqat bitta joy
- **Mahsulot guruhi** — faqat bitta kategoriya (ichimliklar, oziq-ovqat va h.k.)
- **Past qoldiq** — siz belgilagan chegaradan past mahsulotlar

### Qadam 3 — Excel'ga eksport (ixtiyoriy)

Yuqori o'ng burchakdagi **Excel** tugmasi ekrandagi ma'lumotlarni xuddi shunday eksport qiladi — bir xil ustunlar, bir xil filtrlar.

## Brak va qaytarimlarni qayd etish

Mahsulot mijozdan shikastlangan, muddati o'tgan yoki rad etilgan holda qaytsa, ekspeditor uni mobil ilovada qayd etadi. Tizim avtomatik tarzda:

1. Tovarlarni **brak omboriga** qaytaradi
2. Mijoz balansini moslashtiradi (qaytarish kerak bo'lsa)
3. Buyurtmani yangilaydi, shunda hisobotlar qaytarimni aks ettiradi

## Omborlar o'rtasida ko'chirishlar

Tovarni ko'chirish uchun (masalan, asosiy ombor → mashina qoldig'i):

1. **Склад → Перемещения** (Ombor → Ko'chirishlar) ni oching
2. **+ Новое перемещение** ni bosing
3. **Manba** va **maqsadli** omborlarni tanlang
4. Mahsulotlar va miqdorlarni qo'shing
5. **Сохранить**

Ikkala ombor qoldig'i ham darhol yangilanadi.

## Maslahatlar

- **Kirimlarni kelgan kuni tasdiqlang** — tasdiqlanmagan qoldiq agentlarga ko'rinmaydi.
- **Hisobini bera olmaydigan mashinaga ko'chirmang** — tovar mashinaga tushganda, u ekspeditorning mas'uliyatida.
- **Asosiy omborda haftalik inventarizatsiya** nomuvofiqliklarni erta aniqlaydi.

---

**Keyingi:** [Birinchi buyurtmangizni yarating →](../daily-use/first-order)
