---
sidebar_position: 10
title: Chegirmalar, bonuslar va katalog
---

# Chegirmalar, bonuslar va katalogni sozlash

Narx mantiqi uchta joyda joylashgan: **chegirma qoidalari** (Скидки), **bonus qoidalari** (Бонусы) va **mahsulot katalogi** (unda narxlar, brendlar va toifalar saqlanadi).

## 1-qadam — Chegirma qoidalarini sozlash

**Настройки → Скидки** (Sozlamalar → Chegirmalar) yoki `/settings/skidka` ni oching:

![Chegirma qoidalari ro'yxati](/screens/guide/54-settings-discounts.png)

Har bir qoida quyidagilarni belgilaydi: kim chegirma oladi (mijoz toifasi, kanal, agent), nimaga (mahsulot / toifa) va qancha (% yoki qat'iy summa).

Qoida yaratish uchun **+ Добавить** tugmasini bosing. Tipik holatlar:
- "Supermarket kanalidagi barcha mijozlar uchun Ichimliklar toifasiga 5% chegirma"
- "Mijoz toifasi = A bo'lsa, qat'iy 10 000 so'm chegirma"
- "Agentga shaxsiy limit — X agentida bu oy uchun 50 000 so'm chegirma byudjeti bor"

## 2-qadam — Bonus qoidalarini sozlash (sotib ol-X-ol-Y)

**Настройки → Бонусы** (Sozlamalar → Bonuslar) yoki `/settings/bonus` ni oching:

![Bonus qoidalari ro'yxati](/screens/guide/55-settings-bonus.png)

Bonus qoidalari "X mahsulotidan N dona sotib ol — Y mahsulotidan M dona tekin ol" sxemasi bo'yicha ishlaydi. Misollar:
- "10 dona Coca-Cola 0,5l sotib ol — 1 dona tekin ol"
- "X Brendining mahsulotini 100 000 so'mga sotib ol — sovg'a sifatida poster ol"
- "Ichimliklar toifasidan 5 dona sotib ol — Gazaklar toifasidan 1 dona tekin ol"

Ikkala turdagi qoidalar buyurtmani rasmiylashtirish vaqtida avtomatik qo'llaniladi — agentlar bugun qaysi aksiya amal qilishini eslab qolishlari shart emas.

## 3-qadam — Sotuv kanallari

**Настройки → Канал сбыта** (Sozlamalar → Sotuv kanali) yoki `/settings/channel` ni oching:

![Sotuv kanallari](/screens/guide/56-settings-channel.png)

Kanallar mijozlarni tasniflaydi: kichik do'kon / supermarket / restoran / kiosk / kafe va h.k. Kanal:
- Chegirma va bonuslarning qo'llanilishini belgilaydi (yuqoriga qarang)
- Hisobotlarni filtrlaydi
- Tashriflar chastotasini belgilaydi (ba'zi kanallar haftada bir marta, boshqalari ikki haftada bir marta tashrif buyuriladi)

Biznesingizga kerakli kanallarni qo'shing — odatda 4–8 ta yetarli.

## 4-qadam — Brendlar

**Настройки → Бренд** (Sozlamalar → Brend) yoki `/settings/brand` ni oching:

![Brendlar](/screens/guide/58-settings-brand.png)

**Brend** — bu yagona logotip va marketing identifikatsiyasiga ega mahsulotlar oilasi (masalan, "Coca-Cola", "Nestlé Nesquik"). Brend:
- Katalogdagi mahsulotlarni guruhlaydi
- Hisobotlarni kesib o'tadi ("brendlar bo'yicha")
- MML qoidalarini belgilaydi ("must-match list" — har bir do'konda X Brendining kamida 3 SKU si bo'lishi kerak)

## 5-qadam — Mahsulotlar katalogi

**Настройки → Товары** (Sozlamalar → Mahsulotlar) yoki `/settings/product` ni oching:

![Mahsulotlar katalogi](/screens/guide/57-settings-products.png)

Har bir mahsulotga quyidagilar kerak:
- Nomi (ruscha, agar kerak bo'lsa, o'zbekcha)
- Brend
- Toifa (oziq-ovqat / ichimliklar / gigiena / va h.k.)
- O'lchov birligi (dona, quti, kg, litr)
- Shtrix-kod (mobilda skanerlash uchun)
- Standart narx (har bir narx turi uchun)

Excel orqali ommaviy import qo'llab-quvvatlanadi — administrator buni dastlabki sozlash vaqtida bir marta bajaradi.

## Maslahatlar

- **Oddiydan boshlang** — 50 emas, 5–10 chegirma qoidasini belgilang. Murakkab narxlash hammani chalkashtirib yuboradi.
- **Bir toifaga bitta bonus** — bir xil mahsulotda bir-biriga zid bonuslar matematik tortishuvlarni keltirib chiqaradi.
- **Brend nomlarining izchilligi** — "Coca-Cola" vs "Coca Cola" vs "CocaCola" hisobotlarda uchta turli brend bo'lib hisoblanadi.

---

**Keyingisi:** [Birinchi buyurtmangizni yarating →](../daily-use/first-order)
