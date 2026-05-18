---
sidebar_position: 100
title: Sahifalar va formalar katalogi
---

# Har bir sahifa, har bir forma — to'liq katalog

Bitta varaqlanadigan ma'lumotnoma. Har bir bo'limda ko'rsatiladi: sahifa skrinshoti, u nima uchun, qanday formalar / amallar bor va u yerdan keyin qaysi sahifaga o'tasiz.

Muayyan sahifani nomi bo'yicha topish uchun yuqori o'ng burchakdagi qidiruvdan (yoki `Ctrl+F`) foydalaning.

## Ushbu katalogni qanday o'qish kerak

Har bir katalog yozuvida quyidagilar bor:
- **Skrinshot** — URL'ni ochganingizda ko'radigan narsa
- **Manzil** — to'g'ridan-to'g'ri yo'l (xatcho'p qilib qo'yishingiz mumkin)
- **Sahifada nima bor** — asosiy maydonlar, ustunlar, amal tugmalari
- **Keyin qayerga borasiz** — odatiy keyingi bosishlar

Barcha skrinshotlar haqiqiy demo tenantdan olingan. Hisobingizda raqamlar va nomlar farq qiladi, lekin tartib bir xil.

---

## 1. Kirish va bosh sahifa

### 1.1 Kirish ekrani

Manzil: `/site/login`

![Login screen](/screens/guide/01-login-screen.webp)

Sahifada nima bor:
- **Логин** (Login) matn maydoni — odatda telefon raqamingiz yoki tayinlangan foydalanuvchi nomingiz
- **Пароль** (Parol) matn maydoni
- **Запомнить меня** (Meni eslab qol) belgilash katakchasi — sizni shu brauzerda tizimga kirgan holda saqlaydi
- **Войти** (Kirish) tugmasi
- Burchakda til almashtirgich (RU / UZ)

Keyin qayerga borasiz:
- Supervayzer / admin sifatida **Войти** → supervayzer bosh boshqaruv paneli
- Bir nechta roli bo'lgan egasi sifatida **Войти** → rol tanlash, keyin boshqaruv paneli

### 1.2 Supervayzer bosh boshqaruv paneli

Manzil: `/dashboard/supervayzer`

![Supervisor home dashboard](/screens/guide/39-supervisor-dashboard-full.webp)

Sahifada nima bor:
- Yuqoridagi asosiy KPI plitalari: **Продажи** (Sotuvlar), **Визиты** (Tashriflar), **АКБ** (Faol mijozlar bazasi), **ОКБ** (Umumiy mijozlar bazasi), **Долг** (Qarz), **Заказы в ожидании** (Kutilayotgan buyurtmalar)
- Davr tanlagich (Сегодня / Вчера / Неделя / Месяц)
- Davr diagrammasi qatori — tanlangan oraliqdagi kunlik sotuvlar
- Har bir agent bo'yicha faollik jadvali — har bir agent uchun bir qator bilan bugungi kuni

Keyin qayerga borasiz:
- **"Продажи" plitasini bosing** → sotuvlar boshqaruv paneli
- **"Долг" plitasini bosing** → moliya boshqaruv paneli
- **"Визиты" plitasini bosing** → tashrif hisoboti
- **Agent ismini bosing** → agent profili

### 1.3 Sotuvlar boshqaruv paneli

Manzil: `/dashboard/sales`

![Sales dashboard](/screens/guide/34-dashboard-sales.webp)

Sahifada nima bor:
- Agent / mintaqa / mahsulot guruhi bo'yicha taqsimlangan sotuvlar yig'indilari
- Bugun va o'tgan hafta solishtirish diagrammasi
- Xarajat bo'yicha eng yaxshi mijozlar
- Pastda qaytarishlar qatori

Keyin qayerga borasiz:
- **Diagrammadagi agentni bosing** → o'sha shaxsga oldindan filtrlangan agent sotuvlar hisoboti
- **Mahsulot guruhini bosing** → mahsulot darajasidagi hisobot

### 1.4 Moliya boshqaruv paneli

Manzil: `/dashboard/finans`

![Finance dashboard](/screens/guide/35-dashboard-finans.webp)

Sahifada nima bor:
- Yoshga qarab guruhlangan asosiy debitorlik raqami (7 kundan kam / 7–30 / 30+ kun)
- Bugungi to'lovlar kassa bo'yicha (naqd / bank / karta / Click / Payme)
- Eng yirik qarzdorlar ro'yxati — eng katta ochiq qoldiqlar

Keyin qayerga borasiz:
- **Qarzdorni bosing** → o'sha mijozga filtrlangan mijoz to'lovlari / qarz sahifasi
- **Kassa qatorini bosing** → o'sha kassa uchun to'lovni tasdiqlash navbati

### 1.5 KPI boshqaruv paneli (oylik)

Manzil: `/dashboard/kpi`

![KPI dashboard](/screens/guide/38-dashboard-kpi-full.webp)

Sahifada nima bor:
- Har bir agent uchun bitta qator
- Ko'rsatkich bo'yicha progress satrlari: Sotuvlar / AKB / OKB / Tashriflar / Suratlar / MML
- Reja va fakt foizlari
- Rang kodlash: yashil = rejada, sariq = orqada, qizil = juda orqada

Keyin qayerga borasiz:
- **Agent qatorini bosing** → agent profili
- **Ko'rsatkich sarlavhasini bosing** → butun jamoa bo'yicha o'sha metrikaga kirib boring

### 1.6 Hisob-kitob boshqaruv paneli (litsenziyadan foydalanish)

Manzil: `/dashboard/billing`

Sahifada nima bor:
- Joriy litsenziya balansi
- Faol o'rinlar va sotib olingan o'rinlar
- Yangilash sanasi
- So'nggi to'lovlar ro'yxati

*(Skrinshot mavjud emas — billing sahifasi vendor xostiga ulanishni talab qiladi.)*

---

## 2. Buyurtmalar

### 2.1 Buyurtmalar ro'yxati

Manzil: `/orders/list`

![Orders list](/screens/guide/03-orders-list.webp)

Sahifada nima bor:
- Yuqoridagi filtr qatori: **sana oralig'i**, **holat**, **agent**, **ekspeditor**, **ombor**, **kanal**, **mijoz**, **to'lov usuli**
- Amal tugmalari: **Добавить** (Qo'shish), **Накладные** (Yo'l varaqalari), **Групповая обработка** (Guruhli ishlov berish), **Отчёты** (Hisobotlar), **Excel**
- Jadval ustunlari: №, tur, holat, agent, mijoz, qoldiq, summa, qarz, buyurtma sanasi, jo'natish sanasi, yetkazib berish sanasi, ekspeditor, ombor
- Har bir qator boshida holat rangli pilyula
- Pastda sahifalash, sahifa o'lchami tanlagichi

Keyin qayerga borasiz:
- **Qatorni bosing** → buyurtma tafsilotlari sahifasi
- **"+ Добавить" tugmasini bosing** → yangi buyurtma formasi
- **"Накладные" tugmasini bosing** → yo'l varaqalari ro'yxati
- **Belgilash katakchalarini belgilang + "Групповая обработка"** → guruhli yangilash modali (ekspeditor tayinlash, holatni o'zgartirish va h.k.)

### 2.2 Yangi buyurtma formasi

Manzil: `/orders/addOrder`

![New order full form](/screens/guide/33-new-order-empty.webp)

Sahifada nima bor:
- Sarlavha bloki: **Mijoz** tanlagichi, **Agent** ochiluvchi ro'yxati, **Sana** maydoni, **Ombor** ochiluvchi ro'yxati, **Narx turi** ochiluvchi ro'yxati, **To'lov usuli** ochiluvchi ro'yxati
- Mahsulot jadvali: shtrix-kod/nom qidiruv → miqdor → narx → chegirma → qator jami
- Mahsulot jadvali ostida qator qo'shish tugmasi
- Pastda jami qatori: oraliq jami, QQS, chegirma, umumiy jami
- Izoh / qaydlar maydoni
- **Сохранить** (Saqlash) va **Отмена** (Bekor qilish) tugmalari

Keyin qayerga borasiz:
- **Mijoz maydonini bosing** → mijoz tanlagichi ochiladi
  - ![Client picker](/screens/guide/40-client-picker.webp)
  - Qidirilishi mumkin bo'lgan ro'yxat, sahifaga 10 ta qator
  - Nomi, telefoni yoki INN bo'yicha qidiring
  - ![Client picker filtered](/screens/guide/41-client-picker-search.webp)
- **Сохранить** → yangi buyurtma yuqorida bilan buyurtmalar ro'yxatiga qaytadi

### 2.3 Buyurtma rad etishlari / qaytarishlari

Manzil: `/orders/rejects`

![Order rejects](/screens/guide/25-orders-rejects.webp)

Sahifada nima bor:
- Ekspeditor yoki mijoz rad etgan buyurtmalar ro'yxati
- Sabab ustuni (omborda yo'q, noto'g'ri mahsulot, narx kelishmovchiligi, mijoz yo'q va h.k.)
- Amal: yig'ish navbatiga qaytarish uchun **Восстановить** (Tiklash)

### 2.4 Buyurtmani tiklash

Manzil: `/orders/recovery`

![Order recovery](/screens/guide/26-orders-recovery.webp)

Sahifada nima bor:
- Bekor qilingan yoki avto-arxivlangan, lekin hali tiklanishi mumkin bo'lgan buyurtmalar
- Bekor qilish sanasi ustuni
- Qatorlarni belgilang + ularni qaytarish uchun **Восстановить**

### 2.5 Jonli reyslar

Manzil: `/orders/view/trips`

![Live trips](/screens/guide/20-trips-view.webp)

Sahifada nima bor:
- Har bir faol ekspeditor reysi uchun bitta qator
- Yuk mashinasi / haydovchi / marshrut nomi
- Rejalashtirilgan to'xtashlar va bajarilgan to'xtashlar
- Joriy joylashuv (oxirgi GPS signali)
- Taxminiy tugash vaqti

Keyin qayerga borasiz:
- **Reysni bosing** → to'xtash-to'xtash holati bilan reys tafsilotlari

---

## 3. Mijozlar

### 3.1 Mijozlar ro'yxati

Manzil: `/clients/client`

![Clients list](/screens/guide/05-clients-list.webp)

Sahifada nima bor:
- Yuqori amal qatori: **Добавить клиента**, **Импорт** (Excel import), **Экспорт**, **На карте** (Xaritada)
- **Фильтры** havolasi filtr panelini kengaytiradi:
  - ![Clients filter panel](/screens/guide/45-clients-filter-panel.webp)
  - Mintaqa / kanal / segment / agent / faollik bayrog'i / qarz bayrog'i
- Jadval ustunlari: nom, tur, mintaqa, manzil, telefon, agent, oxirgi tashrif, qoldiq
- Pastda sahifalash

Keyin qayerga borasiz:
- **"+ Добавить клиента" tugmasini bosing** → yangi mijoz formasi (yoki agentlarga tashrif vaqtida mobil ilovada yaratish topshirig'i)
- **"Импорт" tugmasini bosing** → Excel import sahifasi
  - ![Clients import](/screens/guide/32-clients-import.webp)
  - Shablonni yuklab oling → to'ldiring → yuklang → oldindan ko'rishni ko'ring → tasdiqlang
- **Qatorni bosing** → mijoz profili (tarix, qarz, suratlar, tashriflar)

### 3.2 Mijoz to'lovlari / qarz

Manzil: `/clients/finans`

![Client payments](/screens/guide/13-client-payments.webp)

Sahifada nima bor:
- Mijoz / agent / davr filtr qatori
- Ustunlar: mijoz, umumiy qarz, muddati o'tgan, oxirgi to'lov sanasi, oxirgi to'lov summasi, o'tgan kunlar
- Yoshga qarab qarz, mintaqa, agent bo'yicha saralash
- Guruhli SMS eslatma tugmasi

Keyin qayerga borasiz:
- **Mijozni bosing** → mijoz to'lov tarixi
- **Guruhli tanlash + SMS** → tanlangan oluvchilar bilan oldindan yuklangan SMS tarqatish sahifasi

### 3.3 Mijozlar xaritada

Manzil: `/clients/view/clientMap`

![Clients on map](/screens/guide/48-clients-on-map.webp)

Sahifada nima bor:
- To'liq ekranli xarita (OpenStreetMap / Yandex)
- Har bir belgi = bitta mijoz
- Holat bo'yicha belgi rangi (faol / nofaol / qarzdor / shu oy tashrif yo'q)
- Yon filtr paneli: agent, mintaqa, segment
- Belgini bosing → mijoz nomi, telefon, agent bilan mini-kartochka

### 3.4 Agent marshruti rejalashtirish

Manzil: `/clients/agentRoute`

![Agent route](/screens/guide/49-agent-route.webp)

Sahifada nima bor:
- Yuqorida agent ochiluvchi ro'yxati
- Agentga tayinlangan mijozlarni ko'rsatuvchi xarita
- Chap tomonda to'xtashlarni sudrab tartibga solinadigan ro'yxat
- Hafta kunlari yorliqlari (Пн / Вт / Ср / Чт / Пт / Сб)
- Rejani saqlash tugmasi

### 3.5 Tashrif o'zgarishlar tarixi

Manzil: `/report/visitingHistory`

![Visit history](/screens/guide/50-visit-history.webp)

Sahifada nima bor:
- Har bir tashrif o'zgartirishi auditi
- Kim / qachon / nima o'zgardi
- Nizolar uchun foydali ("agent tashrif buyurdi deydi, lekin tizim yo'q deydi")

### 3.6 Tasdiqlanmagan mijozlar (tasdiqlash navbati)

Manzil: `/clients/approval`

![Unconfirmed clients](/screens/guide/62-clients-approval.webp)

Dalada qo'shilgan yangi mijozlar faollashishidan oldin shu yerda sizning ko'rib chiqishingizni kutadi.

---

## 4. Jamoa (Команда)

### 4.1 Auditorlar

Manzil: `/team/auditor`

![Team auditors](/screens/guide/06-team-auditor.webp)

Sahifada nima bor:
- Auditor hisoblari ro'yxati
- Ustunlar: nom, telefon, mintaqa, oxirgi kirish, holat
- Auditorlar sotuv agentlaridan alohida mustaqil surat / javon tekshiruvlarini o'tkazadi

### 4.2 Agentlar

Manzil: `/staff/view/agent` (shuningdek `/agents/agent` orqali kirish mumkin)

![Agents list](/screens/guide/07-agents-list.webp)

Sahifada nima bor:
- Ustunlar: nom, telefon, supervayzer, mintaqa, mijozlar soni, oxirgi kirish, holat (faol / bloklangan), oxirgi GPS signali
- Yuqori amal qatori: **Добавить агента**, **Excel**, **Фильтры**
- Pastda guruhli tanlash + guruhli amal tugmasi

Keyin qayerga borasiz:
- **"+ Добавить агента" tugmasini bosing** → agent qo'shish formasi
  - ![Add agent form](/screens/guide/29-add-agent-form.webp)
  - Maydonlar: to'liq ism, telefon, parol, supervayzer, mintaqa, rol, surat
- **Qatorni bosing** → agent profili
  - ![Agent detail](/screens/guide/47-agent-detail.webp)
  - Yorliqlar: umumiy ko'rinish, tashriflar, sotuvlar, KPI, qurilmalar, o'zgarishlar jurnali

### 4.3 Supervayzerlar

Manzil: `/team/supervisor`

![Supervisors list](/screens/guide/17-supervisors-list.webp)

Sahifada nima bor:
- Ustunlar: nom, telefon, ularning qo'l ostidagi agentlar soni, mintaqa, oxirgi kirish

Keyin qayerga borasiz:
- **"+ Добавить" tugmasini bosing** → `/team/supervisor/create`
  - ![Add supervisor form](/screens/guide/30-add-supervisor-form.webp)

### 4.4 Ekspeditorlar

Manzil: `/staff/view/expeditor`

![Expeditors list](/screens/guide/19-expeditors-list.webp)

Sahifada nima bor:
- Ustunlar: nom, telefon, yuk mashinasi/transport, ombor, oxirgi reys, holat
- Ombor / holat bo'yicha filtrlash

Keyin qayerga borasiz:
- **"+ Добавить" tugmasini bosing** → `/staff/create/expeditor`
  - ![Add expeditor form](/screens/guide/31-add-expeditor-form.webp)
  - Maydonlar: to'liq ism, telefon, parol, transport, standart ombor

### 4.5 Foydalanuvchilar (umumiy)

Manzil: `/team/user`

![Users list](/screens/guide/18-users-list.webp)

Sahifada nima bor:
- Rolga qaramay barcha hisoblar (admin / supervayzer / agent / ekspeditor / kassir / auditor)
- Rol bo'yicha filtrlash
- Odamni topishingiz kerak bo'lganda va ularning roli noma'lum bo'lganda foydali

---

## 5. Ombor

### 5.1 Omborlar ro'yxati

Manzil: `/warehouse/list`

![Warehouses list](/screens/guide/08-warehouses-list.webp)

Sahifada nima bor:
- Har bir jismoniy ombor uchun bitta qator
- Ustunlar: nom, manzil, menejer, jo'natmalar uchun standart, omborda jami SKU
- Amal: **Добавить склад** (Ombor qo'shish)

### 5.2 Xaridlar (yetkazib beruvchi qabullari)

Manzil: `/warehouse/view/listPurchase`

![Purchases list](/screens/guide/09-purchases-list.webp)

Sahifada nima bor:
- Kiruvchi tovar hujjatlari
- Ustunlar: №, sana, yetkazib beruvchi, ombor, qator soni, umumiy summa, holat
- Amal: **Добавить приход** (Qabul qo'shish)

### 5.3 Tovar qoldig'i hisoboti

Manzil: `/stock/report`

![Stock report](/screens/guide/10-stock-report.webp)

Sahifada nima bor:
- Har bir ombor, har bir SKU bo'yicha mavjud zaxiraning snapshoti
- Ustunlar: SKU, nom, qo'lda, zaxiraga olingan, mavjud, narx, qiymat
- Filtr: ombor, kategoriya, faqat kam zaxira o'tkazgichi

### 5.4 Inventar / jihozlar ro'yxati

Manzil: `/inventory/list`

![Inventory list](/screens/guide/51-inventory-list.webp)

Sahifada nima bor:
- Mijozlarga joylashtirilgan brendli jihozlar (muzlatkichlar, javonlar, vitrinalar, belgilar)
- Ustunlar: seriya №, tur, model, joriy mijoz, o'rnatish sanasi, oxirgi audit
- Savdo-marketing jamoalari uchun foydali

### 5.5 Ombordan hisobdan chiqarish

Manzil: `/stock/excretion`

![Stock write-off list](/screens/guide/63-stock-write-off.webp)

Shikastlangan, muddati o'tgan yoki noto'g'ri hisoblangan tovarni inventardan olib tashlash.

---

## 6. Rejalashtirish

### 6.1 Oylik tashrif rejasi

Manzil: `/planning/monthly`

![Monthly planning](/screens/guide/11-planning-monthly.webp)

Sahifada nima bor:
- Chapda agentlar, yuqorida kunlar bilan kalendar-jadval ko'rinishi
- Har bir katak rejalashtirilgan tashriflar sonini ko'rsatadi
- Kunlar o'rtasida mijozlarni sudrab tashlash
- Xodimlarni almashtirish uchun agent ochiluvchi ro'yxatini o'zgartiring

Keyin qayerga borasiz:
- **Saqlash** → mobil ilova keyingi sinxronizatsiyada yangi rejani oladi
- **Chop etish** → agent uchun chop etiladigan PDF

### 6.2 Savdo nuqtasi bo'yicha rejalashtirish

Manzil: `/planning/outlet`

![Per-outlet planning](/screens/guide/65-planning-outlet.webp)

Har bir mijoz uchun tashrif kunlarini tanlash (agentga yo'naltirilgan oylik ko'rinishdan farqli o'laroq).

---

## 7. Hisobotlar

### 7.1 Agent sotuvlar hisoboti

Manzil: `/report/agent`

![Agent report](/screens/guide/12-report-agent.webp)

Sahifada nima bor:
- Yuqoridagi filtr qatori:
  - ![Report filter strip](/screens/guide/46-report-filter-strip.webp)
- Pivot jadvali: agent × davr
- Kataklar: buyurtmalar soni, yalpi sotuvlar, qaytarishlar, sof sotuvlar, yig'ilgan qarz
- Pastda jami qatori

### 7.2 Mijoz sotuvlar hisoboti

Manzil: `/report/customer`

![Customer report](/screens/guide/23-report-customer.webp)

Sahifada nima bor:
- Har bir mijoz uchun bitta qator
- Ustunlar: buyurtmalar soni, umumiy xarajat, o'rtacha chek, oxirgi buyurtma sanasi, qoldiq
- Eng yaxshi mijozlaringizni topish uchun xarajat bo'yicha saralang
- Oylik tahlil yig'ilishlari uchun Excel'ga eksport qiling

### 7.3 Tashrif qamrovi hisoboti

Manzil: `/report/visit`

![Visit coverage report](/screens/guide/37-report-visit.webp)

Sahifada nima bor:
- Har bir agent uchun bitta qator
- Ustunlar: rejalashtirilgan tashriflar, bajarilgan tashriflar, % qamrov, buyurtma bilan %, surat %
- Agent sonini bosish orqali kirib boring

### 7.4 Sotuv tafsiloti hisoboti

Manzil: `/report/saleDetail`

![Sale detail report](/screens/guide/60-report-saledetail.webp)

Har bir sotuvning qator-qator tafsiloti — agent, mijoz, mahsulot, miqdor, narx, chegirma, jami.

### 7.5 Ekspeditor samaradorligi hisoboti

Manzil: `/report/expeditor`

![Expeditor performance](/screens/guide/61-report-expeditor.webp)

Kuniga bajarilgan to'xtashlar, yig'ilgan pul, qaytarilgan tovarlar, marshrutdan og'ishlar.

---

## 8. Audit (merchandayzing)

### 8.1 Surat hisoboti

Manzil: `/audit/photoReport`

![Photo report](/screens/guide/15-audit-photoreport.webp)

Sahifada nima bor:
- Tashriflar paytida agentlar tomonidan olingan oxirgi javon suratlari jadvali
- Har bir plitka: surat eskizi, mijoz nomi, agent, sana/vaqt, GPS belgisi
- Agent, mijoz, sana oralig'i, kategoriya (javon / fasad / muzlatkich) bo'yicha filtrlash
- Suratni bosing → metama'lumotlar yon panellari bilan to'liq o'lchamli ko'rinish

### 8.2 Audit (ADT)

Manzil: `/adt/audit`

![ADT audit](/screens/guide/59-adt-audit.webp)

Audit v2 ko'rinishi — faqat surat hisobotidan kengroq: javon o'lchovlari va raqobatchi tekshiruvlarini ham o'z ichiga oladi.

### 8.3 So'rovnoma savollari

Manzil: `/audit/poll`

![Audit poll](/screens/guide/64-audit-poll.webp)

Tashriflar paytida agentlar so'rovnomalari uchun savollar banki.

---

## 9. Markirovka (EDI / CIS)

### 9.1 Kiruvchi yo'l varaqalari

Manzil: `/markirovka/view/incomingInvoices`

![Incoming EDI invoices](/screens/guide/24-markirovka-incoming.webp)

Sahifada nima bor:
- Yetkazib beruvchilardan olingan EDI yo'l varaqalari kiruvchi qutisi (masalan, sigaret / farma kuzatuv)
- Ustunlar: №, yetkazib beruvchi, sana, jami, holat (yangi / qabul qilingan / rad etilgan)
- Guruhli qabul qilish tugmasi

### 9.2 Chiquvchi yo'l varaqalari

Manzil: `/markirovka/view/outgoingInvoices`

![Outgoing EDI invoices](/screens/guide/52-markirovka-outgoing.webp)

Sahifada nima bor:
- Mijozlaringizga jo'natilgan EDI yo'l varaqalari
- Ustunlar: №, mijoz, sana, jami, holat
- Qayta jo'natish / bekor qilish amallari

---

## 10. Onlayn va SMS

### 10.1 Onlayn buyurtmalar kiruvchi qutisi

Manzil: `/onlineOrder/order`

![Online orders](/screens/guide/16-online-orders.webp)

Sahifada nima bor:
- Agent ilovasidan tashqarida olingan buyurtmalar — veb-do'kon, B2B portal, Telegram bot
- Ustunlar: №, manba, mijoz, jami, holat (yangi / tasdiqlangan / CRM'da)
- Amal: **Принять** (Qabul qilish) → CRM'da odatiy buyurtma yaratadi

### 10.2 SMS tarqatish jurnali

Manzil: `/sms/view/list`

![SMS broadcast](/screens/guide/27-sms-broadcast.webp)

Sahifada nima bor:
- CRM'dan yuborilgan SMS kampaniyalarining tarixi
- Ustunlar: sana, segment, oluvchilar soni, yetkazib berilgan, muvaffaqiyatsiz, shablon ko'rinishi
- Yuqorida yangi tarqatish tugmasi

---

## 11. To'lovlar va kassir

### 11.1 To'lovni tasdiqlash navbati

Manzil: `/payment/approval`

![Payment approval](/screens/guide/21-payment-approval.webp)

Sahifada nima bor:
- Dala sharoitida agentlar tomonidan yig'ilgan, kassir tasdig'ini kutayotgan to'lovlar
- Ustunlar: sana, agent, mijoz, summa, usul (naqd / karta / Click / Payme), kvitansiya surati, holat
- Har bir qator uchun **Подтвердить** / **Отклонить** tugmalari
- Agentning to'plamiga ishonganingizda guruhli tasdiqlash

---

## 12. Sozlamalar

### 12.1 Kompaniya profili

Manzil: `/settings/diler`

![Company profile settings](/screens/guide/14-settings-profile.webp)

Sahifada nima bor:
- Kompaniya nomi (rus / o'zbek)
- INN, OKED, MFO, hisob raqamlari
- Logotip yuklash
- Standart aloqa telefoni / elektron pochta
- Manzil
- Yo'l varaqalari va kvitansiyalarda sarlavha sifatida ishlatiladi

### 12.2 Narx turlari

Manzil: `/settings/priceType`

![Price types settings](/screens/guide/28-settings-price-type.webp)

Sahifada nima bor:
- Narx darajalari ro'yxati (Опт / Розница / Спец / Акция / VIP)
- Har bir qator: nom, formula (markup % yoki belgilangan), standart bo'lish o'tkazgichi
- Qo'shish / tahrirlash / o'chirish amallari

### 12.3 To'lov usullari / valyuta

Manzil: `/settings/currency`

![Payment methods](/screens/guide/53-settings-payment-type.webp)

Sahifada nima bor:
- Qabul qilinadigan to'lov usullari (naqd, bank o'tkazmasi, karta, Click, Payme, Apelsin)
- Har bir usul uchun: nom, standart kassa, faol o'tkazgich
- Asosiy valyuta yulduzcha bilan belgilangan valyutalar ro'yxati

### 12.4 Chegirma qoidalari

Manzil: `/settings/skidka`

![Discount rules list](/screens/guide/54-settings-discounts.webp)

Sahifada nima bor:
- Har bir faol chegirma qoidasi uchun bitta qator
- Filtrlar: mijoz kategoriyasi, kanal, agent, mahsulot / kategoriya
- Ustunlar: qoida nomi, qo'llaniladigan ob'ekt, miqdor (% yoki belgilangan), amal qilish muddati

Keyin qayerga borasiz:
- **"+ Добавить" tugmasini bosing** → yangi chegirma qoidasi formasi

### 12.5 Bonus qoidalari

Manzil: `/settings/bonus`

![Bonus rules list](/screens/guide/55-settings-bonus.webp)

Sahifada nima bor:
- "X dan N ta sotib oling, Y dan M ta oling" qoidalari
- Mahsulot, brend, kategoriya bo'yicha filtrlar

### 12.6 Sotuv kanallari

Manzil: `/settings/channel`

![Sales channels](/screens/guide/56-settings-channel.webp)

### 12.7 Brendlar

Manzil: `/settings/brand`

![Brands](/screens/guide/58-settings-brand.webp)

### 12.8 Mahsulotlar katalogi

Manzil: `/settings/product`

![Products catalog](/screens/guide/57-settings-products.webp)

---

## Umumiy UI andozalari

Ushbu vidjetlar CRM bo'ylab har joyda bir xil ishlaydi. Ularni bir marta o'rganing.

### Qidiruv qutisi (har bir ro'yxat sahifasining yuqori o'ngida)
- Ko'rinadigan ustunlar bo'yicha qism satr mosligi
- Yozayotganingizda jonli filtrlash — Enter bosish shart emas
- Tozalash uchun `Esc` bosing

### Filtr qatori (sahifa sarlavhasi ostida)
- Ko'p tanlovli ochiluvchi ro'yxatlar
- Filtrlar bir-biri bilan birikadi — agent VA holat VA sana tanlang
- ![Status filter dropdown example](/screens/guide/44-status-filter-dropdown.webp)

### Sana oralig'i tanlagichi
- ![Date range picker](/screens/guide/42-date-range-picker.webp)
- Sana maydonini bosganingizda ikki oylik kalendar ochiladi
- Tezkor yorliqlar: Сегодня / Вчера / Неделя / Месяц / Квартал
- Sana turi ochiluvchi ro'yxati (Buyurtma sanasi / Jo'natish sanasi / Yetkazib berish sanasi)
  - ![Date type dropdown](/screens/guide/43-date-type-dropdown.webp)

### "Сбросить фильтр" (Filtrlarni tashlash)
Doim filtr qatorining o'ng tomonida. Tanlaganlarning hammasini tozalash uchun bir marta bosing.

### Excel eksport
Har bir ro'yxat sahifasida Excel tugmasi bor — siz ko'rgan narsani aniq eksport qiladi (joriy filtr, joriy saralash, barcha sahifalar bo'ylab barcha qatorlar).

### Sahifalash + sahifa o'lchami
Har bir jadvalning past o'ng tomonida. Standart sahifa o'lchami 25; ko'p o'tib chiqsangiz, 100'ga oshiring. Tanlagan o'lchamingiz har bir sahifa uchun eslab qolinadi.

### Guruhli amallar
Har bir ro'yxat sahifasida qator belgilash katakchalari bor. Qatorlarni belgilang → pastda mavjud amallar bilan amal paneli paydo bo'ladi (tayinlash, holatni o'zgartirish, SMS yuborish, o'chirish va h.k.).

### Holat pilyulalari
Rangli yumaloqlangan yorliqlar. Butun CRM bo'ylab bir xil rang kodi:
- Kulrang = qoralama / yangi
- Ko'k = jarayonda
- Yashil = bajarildi / to'langan / tasdiqlangan
- Sariq = kutilmoqda / tasdiqni kutmoqda
- Qizil = bekor qilingan / rad etilgan / muddati o'tgan

---

**Ish jarayoni bo'yicha qo'llanmaga muhtojmisiz?** Yuqoridagi sahifalar — ma'lumotnoma ko'rinishlari. "X'ni qanday bajarish kerak" bo'yicha bosqichma-bosqich yo'riqnoma uchun bo'lim qo'llanmalaridan foydalaning:
- [Birinchi kirish →](./getting-started/first-login)
- [Birinchi buyurtmangizni yarating →](./daily-use/first-order)
- [Boshqaruv paneli va KPI →](./reports/dashboard-kpi)
