---
sidebar_position: 3
title: Ekspeditor yetkazib berishi
---

# Ekspeditor yetkazib berish jarayoni

Ekspeditor — mijozlarga tovar olib boruvchi shaxs. Uning kuni **reys** atrofida quriladi — ma'lum yuk, kutilgan marshrut va omborga qaytish vaqti bilan rejalashtirilgan to'xtashlar to'plami.

## Ekspeditor telefonda nima qiladi

| Qadam | Nima sodir bo'ladi |
|-------|--------------------|
| **1. Ertalab — yukni olish** | Bugungi reysni ochadi, mashinaga ortilgan tovarni tasdiqlaydi |
| **2. Yo'lda — yetkazish** | Har bir to'xtashda: buyurtmani ochadi, tushiradi, mijoz imzo qo'yadi, to'lovni qayd etadi |
| **3. Qaytarimlarni boshqaring** | Rad etilgan tovarlar mashinada qoladi; qisman rad etishlar hujjatni moslashtiradi |
| **4. Kun oxiri — qaytish** | Sotilmagan tovarni omborga tashlaydi, naqd pulni kassirga topshiradi |

## Qadam 1 — Reysni ofisda jonli kuzating

**Заявки → Рейсы** ni oching (`/orders/view/trips`):

![Reyslar ko'rinishi — har bir faol yetkazib berish](/screens/guide/20-trips-view.webp)

Siz bugun chiqib ketgan barcha ekspeditorlarni quyidagilar bilan ko'rasiz:

- Yakunlangan to'xtashlar va rejalashtirilgan
- Mashinada ayni paytda turgan naqd pul
- Oxirgi GPS pozitsiyasi
- G'ayrioddiyliklar (uzun to'xtash, marshrutdan chiqish, o'tkazib yuborish)

## Qadam 2 — Kontekst uchun buyurtmalar ro'yxatini ko'ring

`/orders/list` da **Сегодняшние** (Bugungi) bo'yicha filtrlang va ekspeditor bo'yicha guruhlang — kim nimani yetkazayotganini ko'rish uchun:

![Ekspeditor bo'yicha bugungi buyurtmalar](/screens/guide/03-orders-list.webp)

## Qadam 3 — Kun oxirida naqd pulni tasdiqlang

Ekspeditor qaytganda u naqd pulni kassirga topshiradi. Kassir `/payment/approval` ni ochadi:

![To'lovni tasdiqlash navbati](/screens/guide/21-payment-approval.webp)

Har bir qator — ekspeditor bugun qayd etgan to'lov. Kassir:

1. O'sha buyurtma uchun naqd pulni sanaydi
2. Mos kelsa **Утверждено** (Tasdiqlandi) ni belgilaydi
3. To'lov endi qarz hisobotida tushirilgan deb ko'rinadi

## Qadam 4 — Reysni yoping

Ekspeditorning barcha buyurtmalari Yetkazilgan yoki Qaytarilgan bo'lgach va barcha naqd pul tasdiqlangach, reys **Завершён** (Yopilgan) holatiga o'tadi. U jonli reyslar ko'rinishidan g'oyib bo'ladi.

## Uchta keng tarqalgan to'lov turi

| Turi | Ekspeditor nima qiladi |
|------|------------------------|
| **Yetkazib berishda naqd** | Eshikda naqd pulni sanaydi, ilovada qabul qilganini belgilaydi |
| **Yetkazib berishda karta** | Karta to'lovini qabul qiladi (biznesingiz qo'llab-quvvatlasa) |
| **Kreditga** | Buyurtmani "keyinroq to'lanadi" deb belgilaydi — qarz darhol yangilanadi |

Naqd va karta yig'indilari telefonda real vaqtda hisoblanadi, shuning uchun ekspeditor doim qancha pul ko'tarayotganini biladi.

## Maslahatlar

- **Yuk tarkibini kun davomida o'zgartirmang** — yo'lga chiqqan mashinaga buyurtma qo'shish — bahslarning eng keng tarqalgan manbai.
- **Ekspeditorga quvvat bankasini bering** — marshrut o'rtasida o'lgan telefon — yomon yangilik.
- **Bir mashina, bir kun, bir reys** — agar ikkita reys kerak bo'lsa, ikkinchisini boshlashdan oldin birinchisini toza yoping.

---

**Keyingi:** [Boshqaruv paneli va KPI →](../reports/dashboard-kpi)
