---
sidebar_position: 3
title: Buyurtmalarni kuzatish
---

# Kun davomida buyurtmalarni kuzatish

Buyurtma yaratilgandan keyin u aniq bosqichlardan o'tadi. Har bir buyurtma hozir qaysi bosqichda ekanini bilish muammolarni erta aniqlashga yordam beradi — tushda hali yuk ortilmagan mashina, buyurtmaning yarmini rad etgan mijoz, olinmagan to'lov.

## Qadam 1 — Buyurtmalar ro'yxatini oching

Menyudan **Заявки → Список заявок** ni tanlang yoki to'g'ridan-to'g'ri `/orders/list` ni oching:

![Holat ustuni bilan buyurtmalar ro'yxati](/screens/guide/03-orders-list.webp)

Har bir qator — buyurtma. **Статус** ustuni qaysi bosqichda ekanini bildiradi.

## Qadam 2 — Holatlarni o'qing

| Holat | Ma'nosi |
|-------|---------|
| **Новая** | Endigina rasmiylashtirilgan. Hech narsa jo'natilmagan. |
| **Загружена** | Tovar ekspeditor mashinasida va yo'lda. |
| **Доставлена** | Mijoz tovarni qabul qilgan. To'lov hali kelmagan bo'lishi mumkin. |
| **Возврат частичный** | Mijoz ba'zi mahsulotlarni rad etgan; qolganini olgan. |
| **Возврат полный** | Butun buyurtma rad etilgan. |
| **Отменена** | Yetkazib berishdan oldin bekor qilingan. |

## Ro'yxatni filtrlash

Buyurtmalar ro'yxatining yuqori qismida uchta filtr richagi bor.

### Sana oralig'i bo'yicha

Ikki oylik taqvimni ochish uchun sana maydonini bosing:

![Sana oralig'i tanlovi ochiq](/screens/guide/42-date-range-picker.webp)

Boshlanish va tugash sanalarini tanlang, so'ng qo'llash uchun tashqi joyni bosing.

### Sana turi bo'yicha

Sana maydonidan chap tomondagi ochiluvchi ro'yxat oraliq qaysi sanaga qo'llanilishini almashtiradi:

![Sana turi ochiluvchi ro'yxati — buyurtma sanasi, jo'natma sanasi, yetkazib berish sanasi](/screens/guide/43-date-type-dropdown.webp)

- **Дата заявки** — buyurtma berilgan sana
- **Дата отгрузки** — tovar omborni tark etgan sana
- **Дата доставки** — mijoz tovarni qabul qilgan sana

### Holat bo'yicha (va qolgan filtr qatori)

Sarlavha ostidagi filtr qatorida ko'plab ochiluvchi ro'yxatlar bor — holat, buyurtma turi, mijoz toifasi, hudud, supervayzer, agent, ekspeditor, narx turi, kanal, ombor, mahsulot toifasi:

![Buyurtma holati filtri ochiluvchi ro'yxati ochilgan](/screens/guide/44-status-filter-dropdown.webp)

Bir nechta qiymatni tanlash uchun istalgan ochiluvchi ro'yxatni bosing. Quyidagi jadval filtrlarni o'zgartirganingizda yangilanadi.

Hammasini birdaniga tozalash uchun qator o'ng chetidagi **Сбросить фильтр** (Filtrni tiklash) ni bosing.

## Qadam 3 — Bitta buyurtmaning ichiga kiring

To'liq tafsilotlarini ochish uchun istalgan buyurtma qatorini bosing:

- Narxlar bilan barcha mahsulot qatorlari
- Kim yaratgan (agent, veb foydalanuvchi yoki onlayn portal)
- Kim yetkazib bermoqda
- Yetkazib berishda olingan fotosuratlar
- To'lov holati

## Qadam 4 — Reyslar jonli ko'rinishini kuzating

Har bir mashina bo'yicha umumiy ko'rinish uchun **Заявки → Рейсы** (Reyslar) ni oching:

![Reyslar ko'rinishi](/screens/guide/20-trips-view.webp)

Siz har bir ekspeditorning reysini to'xtashlari, ko'tarayotgan puli va g'ayrioddiyliklari bilan ko'rasiz.

## Muammolarni hal qilish

### Eshikda qisman rad etish

Mijoz ba'zi mahsulotlarni rad etganda ekspeditor uni mobil ilovada qayd etadi. Tizim avtomatik tarzda:

- Rad etilgan mahsulotlarni hujjatdan olib tashlaydi
- Tovarlarni brak omboriga qaytaradi
- Mijoz qarz summasini moslashtiradi

O'zgarish bir necha soniyada boshqaruv panelida ko'rinadi. Alohida filtrlangan rad etishlarni `/orders/rejects` da ko'ring:

![Buyurtma rad etishlari / qaytarishlar ro'yxati](/screens/guide/25-orders-rejects.webp)

### To'liq rad etish

Xuddi shu jarayon, butun buyurtma rad etiladi. Mashina hamma narsani qaytarib olib keladi.

### Bekor qilingan buyurtmani tiklash

Buyurtma xato bekor qilingan bo'lsa, uni `/orders/recovery` dan tiklashingiz mumkin:

![Buyurtmani tiklash ko'rinishi](/screens/guide/26-orders-recovery.webp)

1. Bekor qilingan buyurtmani toping
2. **Восстановить** (Tiklash) ni bosing
3. Buyurtma oldingi holatiga qaytadi va tovarlar qayta band qilinadi

## Qadam 5 — Kunni yoping

Kun oxirida:

- Hech bir buyurtma hali **Загружена** (Yuklangan) holatida emasligini tekshiring — ular mijozga yetib bormagan
- Ekspeditor to'g'ri qoldiq va pul bilan qaytganini tasdiqlang
- Kutilayotgan to'lovlarni tasdiqlang (qarang [Savdo va qarzlar](../reports/sales-and-debts))

## Maslahatlar

- **Yetkazilgan buyurtmani tahrir qilmang** — agar majburiy bo'lmasa, bu mijozni va buxgalteriyani chalkashtiradi.
- **Izoh maydonidan foydalaning** odatdan tashqari narsalar uchun — moliyachi keyingi hafta so'raganida, izoh sizni qutqaradi.
- **Bitta mijozda takrorlanadigan rad etishlarni kuzating** — bu biror nima noto'g'ri ekanligi haqidagi signal (narx, kanal mosligi, eskirgan munosabat).

---

**Keyingi:** [Agentning mobil ilovasi →](../mobile/agent-app)
