---
sidebar_position: 3
title: Asosiy obyektlar
audience: Backend engineers, QA, Data engineers, Integrators, BI / reporting team
summary: sd-main ning eng muhim 30 jadvali uchun per-table chuqur havola. Har bir bo'lim model fayli yo'lini, jadval nomini, birlamchi kalitni, asosiy tashqi kalit aloqalarini, ustun ro'yxatini turi va maqsadi bilan, indekslarni va qaysi controller / cron job satrni yozishi va o'qishini tushuntiradi. `schema-reference.md` (umumiy DB statistikasi + 306 modelning indeksi) bilan birga ma'lumot qatlami uchun yagona haqiqat manbasi sifatida foydalaning.
topics: [schema, models, tables, columns, foreign-keys, indexes, sd-main, base-filial, multi-tenant]
---

# Asosiy obyektlar

Bu sahifa sd-main ning eng yuklangan 30 ta jadvali uchun **per-table
chuqur tahlil**dir. Agar sizga umumiy DB ko'rinishi (sanoqlar, engine
/ charset taqsimoti, to'liq 306 model indeksi) kerak bo'lsa, avval
`docs/data/schema-reference.md` ni oching. Bu sahifa har bir
hisobotda, har bir sync so'rovida va har bir davr yopilishida
uchraydigan 30 ta jadval uchun chuqurroq boradi.

## Bu sahifani qanday o'qish kerak

Har bir H2 bo'limi bir xil shaklga ega:

- **Source line** — model fayli yo'li, `tableName()` / `filialTable()`
  qiymati, birlamchi kalit.
- **Ustunlar** — `@property` docblock-da hujjatlangan har bir ustun,
  live MySQL sxemasiga qarshi tekshirilgan. Tur ustuni PHP turini
  ko'rsatadi; live DB turi qavslar ichida qo'shilgan, qachonki bu
  ma'lumot bersa (masalan, `int (TINYINT)`, `string (varchar 32)`).
- **Indekslar** — jadvalda ular bo'lganida live sxemadan no-trivial
  indekslar. Bir ustunli PK indekslari tashlab ketilgan.
- **Aloqalar** — model `relations()` e'lon qilgan narsalar va boshqa
  modellardan o'qish vaqtida muhim bo'lgan orqaga havolalar.
- **Read / write surface** — qaysi controllerlar, harakatlar, cron
  jobs va API satrga yozadi va qaysi hisobotlar / endpointlar uni
  o'qiydi.
- **Gotchas** — nozik xatti-harakatlar, eskirgan ustunlar,
  soft-delete vs hard-delete, ikki yozuv juftliklari va boshqalar.
  Jadvalga tegishdan oldin bularni o'qing.

## `BaseFilial` va per-filial jadval prefiksi

Asosiy klass `BaseFilial` (`protected/models/BaseFilial.php` da) —
per-tenant bo'linmalar mexanikasi. `BaseFilial` ni kengaytiradigan
model o'zining mantiqiy jadval nomini `filialTable()` orqali e'lon
qiladi (masalan, `return '{{order}}'`). Ish vaqtida `tableName()`
placeholder ni `d0_fN_order` ga qayta yozadi, bu yerda `fN` —
`FilialComponent::getFilialPrefix()` qaytaradigan faol filial
prefiksi. `f0_` prefiksi umumiy / ildiz filial-ni ifodalaydi — ko'p
master-data jadvallari u yerda yashaydi.

`CActiveRecord` ni to'g'ridan-to'g'ri kengaytiradigan model
(masalan, `Product`, `PriceType`, `Filial`, `Bonus`, `Skidka`) —
**filial-shared**: butun tenant bo'ylab bitta satr mavjud.

`BaseFilial::isCommon` bayrog'i per-filial modelga faqat ildiz
filial-ga tegishi kerak bo'lgan so'rovlar uchun qayta yozishni chetlab
o'tishga imkon beradi. Agar jadvalning har bir per-filial nusxasini
sanab chiqishingiz kerak bo'lsa, `BaseFilial::allTables()` ni o'qing
(davr yopilish engine va cross-filial hisobotlar tomonidan
ishlatiladi).

`{{tableName}}` sintaksisi (Yii jadval placeholder) Yii DB qatlami
tomonidan sozlangan jadval prefiksini (`d0_`) kiritish uchun qayta
ishlanadi. `BaseFilial` modeli uchun placeholder shuningdek
`BaseFilial::getFilialTable()` tomonidan kiritilgan filial prefiksini
ham oladi.

---

## `Order`

Source: `protected/models/Order.php`. Extends `BaseFilial`. `filialTable()`
returns `{{order}}`, resolves to `d0_fN_order`. Primary key `ORDER_ID`
(varchar UUID-like). Live DB: 59 columns.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `ORDER_ID` | string | PK. UUID-like, shuningdek cross-filial sync ID sifatida ishlatiladi. |
| `DILER_ID` | string | Tenant bo'linmasi (legacy "dealer"); `Diler` modeliga qarang. |
| `CLIENT_ID` | string | `Client.CLIENT_ID` ga FK. |
| `AGENT_ID` | string | `Agent.AGENT_ID` ga FK. Web / B2B portal buyurtmalari uchun NULL. |
| `CLIENT_CAT` | string | Submit vaqtida denormallashtirilgan mijoz kategoriyasi. |
| `CITY_ID` | string | `City` ga FK. |
| `PRICE_TYPE` | string | `PriceType.PRICE_TYPE_ID` ga FK. Submit vaqtida narx ro'yxatini qulflaydi. |
| `OLD_PRICE_TYPE` | string | Migratsiyadan oldingi price-list ID; legacy. |
| `COUNT` | float | `OrderDetail.COUNT` yig'indisi (yetkazib berilgan units). |
| `SUMMA` | float | Chegirmadan keyingi total, `CURRENCY` da. |
| `DISCOUNT` | float | Buyurtma bo'yicha `OrderDetail.DISCOUNT` yig'indisi. |
| `DATE` | datetime | Submitted-at. Birinchi save da o'rnatiladi, hech qachon qayta yozilmaydi. |
| `STATUS` | int (TINYINT) | Makro holat: 1 Yangi, 2 Jo'natilgan, 3 Yetkazib berilgan, 4 Qaytarilgan, 5 Bekor qilingan, 6 Tahrirlanmoqda, 7 New (second-sale variant). |
| `SUB_STATUS` | int | `STATUS` ichidagi nozik UI qadam. |
| `DOB_STATUS` | string | Omborda yig'ish sub-statusi: NULL boshlanmagan, `picking`, `picked`. `STATUS` dan mustaqil. |
| `DATE_LOAD` | datetime | Buyurtma trip ga yuklanganda. |
| `DATE_DELIVERED` | datetime | Ekspeditor yetkazib berishni tasdiqlaganda. |
| `DATE_CANCEL` | datetime | `STATUS=5` bo'lganda. |
| `DATE_STATUS` | datetime | Oxirgi status o'tishi; SLA kuzatuvi uchun ishlatiladi. |
| `DEBT` | float | Outstanding receivable; `ClientTransaction` net dan oynalanadi. |
| `REPLACE_ID` | string | Bo'sh bo'lmasa, bu buyurtma boshqa buyurtmani almashtiradi. |
| `DEFECT_ID` | string | Bo'sh bo'lmasa, bu buyurtmaning defect-return parent. |
| `BONUS_ORDER_ID` | string | `BonusOrder` ga FK (auto-generated promo line). |
| `BONUS_TYPE` | string | `-1` avto-bonus, `-2` bonusni o'tkazib yuborish, `d0_*` qo'lda BONUS_ID. |
| `TIMESTAMP_X` | datetime | Oxirgi DB-side yozuv; trigger-managed. |
| `COMMENT` | string | Agent free-text. |
| `ID` | int | Faqat sync tartiblash uchun surrogate auto-increment. PK EMAS. |
| `TRADE_ID` | int | `TradeDirection` ga FK. |
| `ACTIVE` | char(1) | `Y` faol, `N` soft-deleted. Hard delete kamdan-kam. |
| `SYNC` | string | Mobile clientlar uchun sync ledger flag. |
| `TIME` | int | Submit vaqtidagi mobile client soati (epoch). |
| `VOLUME` | float | Kubometr (trip rejalashtirish uchun). |
| `SKIDKA` | int | Submit vaqtidagi chegirma rejimi snapshot. |
| `CURRENCY` | string | `Currency.CURRENCY_ID` ga FK. |
| `CURRENCY_SYMBOL` | string | Denormallashtirilgan display symbol. |
| `UNIT` | string | `Unit.UNIT_ID` ga FK (base UOM). |
| `UNIT_SYMBOL` | string | Denormallashtirilgan UOM symbol. |
| `EXPEDITOR` | string | Tayinlangan `Expeditor.EXPEDITOR_ID`. Trip tayinlanishigacha NULL. |
| `TYPE` | string | 1 Order, 2 Shelf-return, 3 Exchange. |
| `CONTRACT_ID` | string | Shartnoma faol bo'lsa `ContractClient.ID` ga FK. |
| `COMMENT_2` | string | Ichki manager izohi. |
| `CONSIGNMENT` | string | Consignment ref (legacy 1C integration). |
| `CONSIG_DATE` | datetime | Consignment sanasi. |
| `XML_ID` | string | Tashqi 1C / ERP ID. |
| `REAL_ID` | string | Server reconciliation gacha mobile client lokal ID. |
| `STORE_ID` | string | Manba ombor `Store.STORE_ID`. |
| `DEFECT` | string | Defect-flag column (legacy). |
| `CREATE_BY` / `CREATE_AT` | string / datetime | Audit. |
| `UPDATE_BY` / `UPDATE_AT` | string / datetime | Audit. |
| `SOURCE` | string | mobile / web / online / import. |
| `STOCKMAN_ID` | string | Picker `User.USER_ID`. |
| `CISES_STATUS` | int | Buyurtmaning CIS kodlari uchun markirovka (Honest Sign) holati. |

### Indekslar

`d0_order` — sd-main da o'qish bo'yicha eng yuklangan jadval. Live
sxema `CLIENT_ID`, `AGENT_ID`, `DATE`, `STATUS`, `STORE_ID`,
`EXPEDITOR`, `XML_ID` bo'yicha non-unique indekslarni e'lon qiladi,
plus `ORDER_ID` da PK.

### Aloqalar

| Name | Type | Target |
|------|------|--------|
| `Diler` | BELONGS_TO | `Diler` on `DILER_ID` |
| `Client` | BELONGS_TO | `Client` on `CLIENT_ID` |
| `Agent` | HAS_ONE | `Agent` on `AGENT_ID` |
| `City` | HAS_ONE | `City` on `CITY_ID` |
| `Unit` | HAS_ONE | `Unit` on `UNIT` to `UNIT_ID` |
| `Currency` | HAS_ONE | `Currency` on `CURRENCY` to `CURRENCY_ID` |
| `PriceType` | HAS_ONE | `PriceType` on `PRICE_TYPE` to `PRICE_TYPE_ID` |
| `Visit` | HAS_ONE | `Visiting` on `DILER_ID` |
| `Debt` | HAS_ONE | `DebtFinans` on `ORDER_ID` |
| `OrderDetail` | HAS_MANY | `OrderDetail` on `ORDER_ID` |
| `Contragent` | BELONGS_TO | conditional, faqat `ServerSettings::isContragent()` bo'lganda |

### Read / write surface

Yozuv: `OrderController::actionSave`, mobile API v1 / v2 / v3 (agent
submit, expeditor confirm), omborda yig'ish moduli, defect-return
flow (`OrderDefectController`), bonus engine
(`BonusComponent::generate` auto-bonus child orders ishlab chiqaradi),
1C import job. O'qish: har bir report dashboard, `OrdersReport`,
davr yopilish engine, `Trip` planner, KPI engine, `OutletFact`
aggregator.

### Gotchas

- `ORDER_ID` client-side da GUID sifatida yaratiladi; mobile
  `REAL_ID` bilan submit qiladi, shunda server offline-write
  reconciliation dan keyin map qila oladi.
- `STATUS=3` (Yetkazib berilgan) buyurtmani avtomatik ravishda
  to'lamaydi. Finans ledger alohida `ClientTransaction` ni talab
  qiladi (write `TRANS_TYPE = order`) — `docs/concepts/order-lifecycle.md`
  dagi buyurtma finans to'lov hayotiy davrini ko'ring.
- `BONUS_TYPE` overloaded: `-1` engine tomonidan ishlab chiqarilgan
  auto-bonus, `-2` bonusni o'tkazib yuborish, har qanday boshqa qiymat
  tanlangan qo'lda bonus uchun `BONUS_ID`.
- `DOB_STATUS` ('picking', 'picked') `STATUS` dan **mustaqil**.
  Manager tasdiqlashidan oldin ombor yig'gan bo'lsa, satr `STATUS=1
  New` va `DOB_STATUS=picked` bo'lishi mumkin.
- Soft delete `ACTIVE='N'` dan foydalanadi; downstream hisobotlar
  `ACTIVE='Y'` bo'yicha filtr qilishi kerak.

---

## `OrderDetail`

Source: `protected/models/OrderDetail.php`. Extends `BaseFilial`.
`filialTable()` returns `{{order_detail}}`, resolves to
`d0_fN_order_detail`. Primary key `ORDER_DET_ID`. Live DB: 29 columns.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `ORDER_DET_ID` | string | PK (UUID-like). |
| `ORDER_ID` | string | `Order.ORDER_ID` ga FK. |
| `DILER_ID` | string | Tenant bo'linmasi. |
| `CLIENT_ID` | string | Ota buyurtmadan denormallashtirilgan. |
| `CLIENT_CAT` | string | `Client.CLIENT_CAT` dan denormallashtirilgan. |
| `CITY_ID` | string | Otadan denormallashtirilgan. |
| `STORE_ID` | string | Ushbu satr uchun manba ombor. |
| `PRODUCT_CAT` | string | `ProductCategory` ga FK. |
| `PRODUCT` | string | `Product.PRODUCT_ID` ga FK. |
| `COUNT` | float | Buyurtma qilingan units. |
| `PRICE` | float | Submit vaqtidagi birlik narxi `CURRENCY` da. |
| `SUMMA` | float | `COUNT * PRICE - DISCOUNT`. |
| `DISCOUNT` | float | Qo'llanilgan line-level chegirma. |
| `DISCOUNT_ID` | string | Chegirma bergan `Skidka` qoidasiga FK. |
| `SKIDKA_MANUAL_ID` | string | Manager-override discount qo'llanilgan bo'lsa `SkidkaManual` ga FK. |
| `VOLUME` | float | Satr uchun kubometr. |
| `CURRENCY` | string | `PRICE` valyutasi. |
| `CURRENCY_SYMBOL` | string | Denormallashtirilgan. |
| `UNIT` | string | Satr darajasidagi UOM. |
| `UNIT_SYMBOL` | string | UOM display symbol. |
| `DEFECT` | float | Yetkazib berishda rad etilgan units soni (defect-return flow tomonidan ishlatiladi). |
| `COMMENT` | string | Free-text. |
| `ID` | int | Surrogate auto-increment. |
| `ACTIVE` | char(1) | Soft-delete flag. |
| `SYNC` | string | Sync ledger. |
| `TIMESTAMP_X` | datetime | Trigger-managed. |
| `CREATE_BY` / `UPDATE_BY` | string | Audit user. |

### Aloqalar

| Name | Type | Target |
|------|------|--------|
| `Order` | BELONGS_TO | `Order` on `ORDER_ID` |
| `Product` | BELONGS_TO | `Product` on `PRODUCT` to `PRODUCT_ID` |
| `Unit` | HAS_ONE | `Unit` on `UNIT` to `UNIT_ID` |
| `Currency` | HAS_ONE | `Currency` on `CURRENCY` to `CURRENCY_ID` |

### Read / write surface

Yozuv: `Order` bilan bir xil controllerlar — har bir order saqlash
`OrderDetail` da batch insert / update ga fan-out qiladi. O'qish:
sales-by-product hisobotlari, AKB kalkulyator, bonus engine (kirish
to'plami), defect-return flow (`DEFECT > 0` satrlarni mos keladi).

### Gotchas

- `DEFECT` ustuni order da emas, **satrda**. Buyurtma uchun jami
  defect ni hisoblash uchun `OrderDetail.DEFECT * PRICE` ni
  yig'ing.
- Buyurtma satri audit trail `OrderDetailHistory` da (28 ustun) —
  har qanday non-cosmetic tahrir `ORDER_DET_ID` bo'yicha kalitlangan
  history satrini yaratadi.
- Satr `STORE_ID` order `STORE_ID` dan farq qilishi mumkin, multi-store
  yig'ish yoqilganda (kamdan-kam; server setting tomonidan boshqariladi).

---

## `OrderHistory`

Source: `protected/models/OrderHistory.php`. Extends `BaseFilial`.
`filialTable()` returns `{{order_history}}`, resolves to
`d0_fN_order_history`. Primary key `ID` (auto-increment). Live DB: 38 columns.

### Ustunlar

`Order` ustunlarining katta qismini oynalantiradi (`ORDER_ID`,
`DILER_ID`, `CLIENT_ID`, `AGENT_ID`, `CLIENT_CAT`, `CITY_ID`,
`PRICE_TYPE`, `COUNT`, `SUMMA`, `DATE`, `STATUS`, `DATE_LOAD`,
`DATE_DELIVERED`, `DATE_CANCEL`, `DATE_STATUS`, `DEBT`, `TIMESTAMP_X`,
`COMMENT`, `ACTIVE`, `SYNC`, `TIME`, `VOLUME`, `CURRENCY`,
`CURRENCY_SYMBOL`, `UNIT`, `UNIT_SYMBOL`, `DISCOUNT`, `EXPEDITOR`,
`TYPE`, `CONSIGNMENT`, `CONSIG_DATE`, `DEFECT`, `XML_ID`, `CREATE_BY`,
`UPDATE_BY`, `CREATE_AT`, `UPDATE_AT`). `ID` auto-increment PK
qo'shadi va har bir satrni `ORDER_ID` orqali jonli `Order` ga
bog'laydi.

### Read / write surface

Yozuv: `Order::afterSave()` har bir o'tishda satrni `OrderHistory` ga
snapshot qiladi. O'qish: order-history UI, audit hisobotlari,
support tomonidan ishlatiladigan "kim-nima-qachon-o'zgartirdi" view.

### Gotchas

- Bu **append-only** log. DB-maintenance dan tashqari tahrirlar yoki
  o'chirishlar ruxsat etilmaydi.
- `OrderDetailHistory` (singildosh jadval) satr o'zgarishlari uchun
  bir xil rolni o'ynaydi.
- History satri `ORDER_ID` orqali emas, autoincrement `ID` orqali
  kalitlangan, shuning uchun bitta buyurtmada o'nlab satrlar bo'lishi
  mumkin.

---

## `Client`

Source: `protected/models/Client.php`. Extends `BaseFilial`.
`filialTable()` returns `{{client}}`, resolves to `d0_fN_client`.
Primary key `CLIENT_ID`. Live DB: 58 columns.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `CLIENT_ID` | string | PK (UUID-like). |
| `DILER_ID` | string | Tenant bo'linmasi. |
| `TEL` | string | Asosiy telefon (bir nechta telefonlar `ClientPhones` da yashaydi). |
| `FIRM_NAME` | string | Huquqiy nom. |
| `NAME` | string | Display name. |
| `ADRESS` | string | Free-text manzil (legacy spelling ga e'tibor bering). |
| `CLIENT_CAT` | string | `ClientCategory.CLIENT_CAT_ID` ga FK. |
| `ORIENT` | string | Navigatsiya uchun belgi. |
| `REGION` | string | `Region` ga FK. |
| `CITY` | string | `City.CITY_ID` ga FK. |
| `CONTACT_PERSON` | string | Free-text. |
| `FORM_SOB` | string | Mulkchilik shakli kodi. |
| `BALANS` | float | Kesh qilingan running balance — `ClientTransaction` dan tunda qayta hisoblanadi. |
| `PRICE_TYPE_ID` | string | `PriceType` ga FK. Default price list. |
| `BONUS_ID` | string | `Bonus` ga FK. Faol bonus dasturi. |
| `DISCOUNT_ID` | string | `Skidka` ga FK. Faol chegirma qoidasi. |
| `DATE_EXP` | datetime | Oxirgi expedition / yetkazib berish sanasi — trip flow tomonidan yangilanadi. |
| `LON`, `LAT` | float | Agent tashrifi vaqtida geofencing uchun geo. |
| `ALLOW_CONSIG` | int | 1 bo'lsa consignment savdolari ruxsat etilgan. |
| `ALLOW_KREDIT` | int | 1 bo'lsa kredit savdolari ruxsat etilgan. |
| `XML_ID` | string | Tashqi 1C / ERP ID. |
| `BAR_CODE` | string | Loyalty barcode. |
| `EXPEDITOR` | string | Default `Expeditor.EXPEDITOR_ID`. |
| `PHOTO` | string | Savdo nuqtasining foto URL. |
| `ACCOUNT`, `BANK`, `MFO`, `OKED` | string | Faktura.uz invoices uchun bank ma'lumotlari. |
| `CODE_NDS`, `NSP_CODE` | string | Soliq registratsiya kodlari. |
| `PINF` | string | Shaxsiy identifikatsiya raqami (O'zbekiston). |
| `CONTRACT` | string | Contract reference code. |
| `CONTRACT_DATE` | datetime | Shartnoma faollashtirish sanasi. |
| `CHANNEL` | string | `ClientChannel.ID` ga FK. |
| `CLASS` | string | `ClientClass.ID` ga FK. |
| `NEED_TO_AUDIT` | string | `Y` keyingi tashrifda audit ni triggerlaydi. |
| `TYPE` | int | Mijoz turi kodi (B2B / B2C / chain / etc.). |
| `SALES_CAT` | string | `SalesCategory` ga FK. |
| `CODE_2` | string | Ba'zi 1C integratsiyalari tomonidan ishlatiladigan ikkinchi kod. |
| `CONTRAGENT` | string | Contragent rejimi yoqilganda `Contragent.CLIENT_ID` ga FK. |
| `TGIS_ID` | string | Soliq tizimi tashqi kaliti. |
| `ACTIVE` | char(1) | Soft-delete flag. |
| `APPROVED` | int | 0 pending, 1 tasdiqlangan (yangi savdo nuqtasini tasdiqlash workflow). |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Indekslar

`d0_client` da 58 ustun bor. Live indekslar: `CITY`, `CLIENT_CAT`,
`XML_ID`, `EXPEDITOR`, `CHANNEL`, plus `CLIENT_ID` da PK.

### Aloqalar

Model o'zi `relations()` ni e'lon qilmaydi, lekin har bir moliyaviy
va order modeli unga havola qiladi. Cross-table joinlar `CLIENT_ID`
orqali o'tadi.

### Read / write surface

Yozuv: `ClientController::actionSave`, mobile API new-outlet flow,
`ClientPending` tasdiqlash flow (`APPROVED=0` 1 ga o'tganda), 1C /
Faktura sync, KPI engine (`NEED_TO_AUDIT` ni yangilaydi). O'qish:
amalda har bir hisobot.

### Gotchas

- `BALANS` bu **kesh**; haqiqat `ClientTransaction` da. Agar u
  drift qilsa, `ClientFinans::recompute` ni ishga tushiring.
- `ADRESS` ustuni legacy spelling va bu haqiqiy DB ustun nomi.
  `ADDRESS` ga qayta nomlamang.
- `APPROVED=0` mijozlar dalada agentlar tomonidan yaratilishi mumkin,
  lekin manager tasdiqlamaguncha invoicing hisobotlarida ko'rinmaydi.

---

## `ClientTransaction`

Source: `protected/models/ClientTransaction.php`. Extends `BaseFilial`.
`filialTable()` returns `{{client_transaction}}`, resolves to
`d0_fN_client_transaction`. Primary key `CLIENT_TRANS_ID`. Live DB: 40 columns.

Bu sd-main ning **kanonik finans ledger**. Har bir order, payment,
defect, qo'lda tuzatish, transfer va bonus pul effekti kamida bir
qator shu yerga post qiladi.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `CLIENT_TRANS_ID` | string | PK (UUID-like). |
| `DILER_ID` | string | Tenant bo'linmasi. |
| `CLIENT_ID` | string | `Client` ga FK. |
| `SUMMA` | float | `CURRENCY` da signed amount. Musbat bizga mijoz qarzini oshiradi (sotuv); manfiy uni kamaytiradi (to'lov). |
| `IDEN` | string | Cross-row guruhlash uchun identity tag. |
| `DATE` | datetime | Effektiv biznes sanasi (row creation EMAS). |
| `DATE_EXP` | datetime | Receivables uchun kutilgan yopilish sanasi. |
| `COMMENT` | string | Free-text. |
| `TIMESTAMP_X` | datetime | Trigger-managed oxirgi yozuv. |
| `TYPE` | string | High-level type: cash, card, transfer, defect, adjust, bonus. |
| `TRANS_TYPE` | string | Origin event: `order`, `payment`, `defect_return`, `bonus`, `manual`. |
| `STATUS` | string | Posting state — confirm-on-delivery flow uchun tegishli. |
| `CURRENCY` | string | `Currency.CURRENCY_ID` ga FK. |
| `CURRENCY_SYMBOL` | string | Display symbol. |
| `CURRENCY_RATE` | float | Posting vaqtidagi FX kurs snapshot. |
| `CONVERTATION` | float | Asosiy valyutaga konvertatsiya qilingan summa. |
| `COMISSION` | float | Bank/processor komissiyasi ushlangan. |
| `COMPUTATION` | float | Hisobotlar uchun summa — `SUMMA` + `CONVERTATION` dan olingan. |
| `EXPEDITOR` | string | Cash to'plagan ekspeditor (agar bo'lsa). |
| `AGENT_ID` | string | Satrni yaratgan agent (agar bo'lsa). |
| `USER_ID` | string | Satrni yaratgan office user (agar bo'lsa). |
| `HISTORY` | string | Tahrir tarixi bilan JSON blob. |
| `CASHBOX` | string | `Cashbox.ID` ga FK. |
| `OFD_ID` | string | Fiscal device cheque ID. |
| `DATE_CLOSE` | datetime | Closure date (period-close mexanika). |
| `STORE_ID` | string | Manba ombor / kassir. |
| `XML_ID` | string | Tashqi 1C ID. |
| `CONFIRM_ID` | string | Pending satr tasdiqlanganda o'rnatiladi. |
| `CONFIRM_USER` | string | Tasdiqlovchi user. |
| `ONLINE_PAYMENT_ID` | int | Payme / Click / etc orqali post qilinganda `OnlinePayment` ga FK. |
| `ACTIVE` | char(1) | Soft-delete. |
| `SYNC` | string | Sync ledger. |
| `CREATE_BY` / `CREATE_AT` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Yozuv: order-save (`order` turidagi bir satr), payment flow
(`PaymentDeliver`, `Cashbox` UI, online-payment webhooks),
defect-return (`OrderDefectController`), buxgalter tomonidan qo'lda
tuzatish (`FinansController::actionEdit`), bonus engine (bonus pul
sifatida materialashganda), period-close (`DATE_CLOSE` ni yozadi).
O'qish: har bir finans hisobot, mijoz balans vidjeti, sd-cs va
sd-billing aggregatorlari.

### Gotchas

- `SUMMA` belgisi konventsiyasi: **musbat = mijoz bizga qarz,
  manfiy = biz mijozga qarzdorimiz**. Qarzni musbat raqam sifatida
  ko'rsatuvchi hisobotlar display oldidan negate qilmasligi kerak.
- `STATUS='pending'` satr (confirm-on-delivery flow) ekspeditor
  tasdiqlamaguncha va satr confirmed ga o'tmaguncha mijoz balansida
  hisobga olinmaydi. Xom satrlarni soddalik bilan aggregate
  qilmang.
- `Cashbox.KASSIR` lookup user orqali; bu satrdagi `CASHBOX` cashbox
  ID orqali — ularni aralashtirib yubormang.
- `ClientTransactionHistory` (32 ust.) satrga tahrirlarning
  append-only tarixini saqlaydi.

---

## `Agent`

Source: `protected/models/Agent.php`. Extends `BaseFilial`.
`filialTable()` returns `{{agent}}`, resolves to `d0_fN_agent`. Primary
key `AGENT_ID`. Live DB: 29 columns.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `AGENT_ID` | string | PK. |
| `FIO` | string | Full name. |
| `TEL` | string | Telefon. |
| `PASSPORT_COPY` | string | Pasport skani URL. |
| `DATE_BIRTH` | datetime | Birthday. |
| `ADDRESS` | string | Free-text. |
| `PHOTO` | string | Profile photo URL. |
| `DILER_ID` | int | Tenant bo'linmasi. |
| `EMAIL` | string | Email. |
| `ACTIVE` | char(1) | `Y` / `N`. |
| `VAN_SELLING` | int | 1 bo'lsa van-selling yoqilgan (mobile expeditor flow). |
| `AUDIT` | string | `Y` bo'lsa agent audit qiladi. |
| `SYNC` | string | Sync ledger. |
| `XML_ID` | string | Tashqi ID. |
| `FILTER` | string | Agentning outlet ko'rinish scoping uchun JSON filter. |
| `APP_VERSION` | string | Oxirgi xabar berilgan mobile app versiyasi. |
| `DEVICE_MODEL` | string | Oxirgi xabar berilgan qurilma modeli. |
| `LAST_SYNC_TIME` | datetime | Bu userdan oxirgi muvaffaqiyatli sync push. |
| `IP_ADDRESS` | string | Oxirgi sync IP. |
| `CASHBOX` | string | `Cashbox.ID` ga FK — agentning default cashbox. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Aloqalar

Model `User` ga `AGENT_ID = USER.AGENT_ID` bo'yicha HAS_ONE ni e'lon
qiladi, shunda API qatlami credentials va role ni resolve qilishi
mumkin.

### Read / write surface

Yozuv: `AgentController` admin UI, RBAC role-assignment, har bir sync
da mobile app metadata pings. O'qish: visit moduli, KPI engine,
sales-by-agent report, trip planner.

### Gotchas

- `Agent` bu **biznes identifikatsiyasi**. Login (`User`) — `AGENT_ID`
  orqali join qilingan alohida satr. Login ni o'chirib qo'yish
  `User.ACTIVE='N'` ni anglatadi, `Agent.ACTIVE='N'` ni emas.
- `FILTER` — JSON; ruxsat etilgan qiymatlar `AgentFilter` helper
  da hujjatlangan.
- `LAST_SYNC_TIME` — sd-cs central console "offline > 24h"
  agentlarni aniqlash uchun o'qiydigan narsa.

---

## `Supervayzer`

Source: `protected/models/Supervayzer.php`. Extends `BaseFilial`.
`filialTable()` returns `{{supervayzer}}`, resolves to
`d0_fN_supervayzer`. Primary key `SV_AGENT_ID`. Live DB: 11 columns.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `SV_AGENT_ID` | string | PK. |
| `USER_ID` | string | `User.USER_ID` ga FK (login). |
| `DILER_ID` | string | Tenant bo'linmasi. |
| `AGENT_ID` | string | `Agent.AGENT_ID` ga FK — nazorat qilinadigan bo'ysunuvchi agent. |
| `POSITION_ID` | int | Position lookup ga FK. |
| `XML_ID` | string | Tashqi ID. |
| `ACTIVE`, `SYNC`, `TIME`, `TIMESTAMP_X`, `ID` | – | Standart audit / sync. |

### Read / write surface

Yozuv: `SupervayzerController` admin UI. O'qish: supervisor-scoped
report filterlari, KPI engine (supervisor barcha bo'ysunuvchi agent
KPI-larini meros qilib oladi).

### Gotchas

- Bir supervisor ko'p agentlarni nazorat qilishi mumkin — bir xil
  `USER_ID` va turli xil `AGENT_ID` bilan ko'p satrlar.
- Supervisor satrini o'chirish hech qayerda log qilinmaydi — audit
  trail kerak bo'lsa `model_log` orqali diff qiling.
- Supervisor roli boshqa supervisor-larning ma'lumotlarini KO'RMAYDI,
  agar `ServerSettings::isCrossSupervayzer()` yoqilmagan bo'lsa.

---

## `Expeditor`

Source: `protected/models/Expeditor.php`. Extends `BaseFilial`.
`filialTable()` returns `{{expeditor}}`, resolves to `d0_fN_expeditor`.
Primary key `EXPEDITOR_ID`. Live DB: 28 columns.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `EXPEDITOR_ID` | string | PK. |
| `FIO` | string | Full name. |
| `TEL` | string | Telefon. |
| `AUTONUM` | string | Mashina raqami. |
| `AUTOBRAND` | string | Mashina brendi. |
| `DILER_ID` | string | Tenant bo'linmasi. |
| `PASSPORT_COPY` | string | Skan URL. |
| `DATE_BIRTH` | datetime | Birthday. |
| `ADDRESS` | string | Free-text. |
| `PHOTO` | string | Photo URL. |
| `CITY_ID` | string | `City` ga FK. |
| `EMAIL` | string | Email. |
| `PINFL` | string | Tax / passport identifier. |
| `ADD_FILTER` | string | JSON qo'shimcha scoping filter. |
| `DEFECT_STORE` | string | `Store.STORE_ID` ga FK — bu ekspeditor defective tovarni qaytaradigan ombor. |
| `XML_ID` | string | Tashqi ID. |
| `ACTIVE`, `SYNC`, `TIMESTAMP_X`, `TIME`, `ID` | – | Standart. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Yozuv: `ExpeditorController`, trip-assignment job, mobile expeditor
app sync da. O'qish: trip planner (`Trip`), expeditor KPI engine
(`ExpeditorKpiJob`, `ExpeditorKpiSetup`), ekspeditor yuklash hisobotlari
(`ExpeditorLoad`, `ExpeditorLoadDetail`).

### Gotchas

- Login (`User.EXPEDITOR_ID`) `Expeditor` satriga map bo'lishi mumkin,
  va `Cashbox` odatda trip vaqtida biriktiriladi.
- `DEFECT_STORE` standart bo'yicha belgilangan karantin ombori;
  defect deb belgilangan orderlar manager qaytadan stock qilmaguncha
  u yerga qaytadi.

---

## `User`

Source: `protected/models/User.php`. Extends `BaseFilial`.
`filialTable()` returns `{{user}}`, resolves to `d0_fN_user`. Primary
key `USER_ID`. Live DB: 22 columns. Authentication / role-bearer
satri; `Agent`, `Expeditor`, `Supervayzer`, `Auditor` dan biri yoki
hech biri (back-office user) bilan juftlangan.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `USER_ID` | int | PK (autoincrement). |
| `NAME` | string | Display name. |
| `EMAIL` | string | Email. |
| `DILER_ID` | int | Tenant bo'linmasi. |
| `AGENT_ID` | int | `Agent.AGENT_ID` ga FK (role = agent bo'lganda). |
| `EXPEDITOR_ID` | string | `Expeditor.EXPEDITOR_ID` ga FK (role = expeditor bo'lganda). |
| `ROLE` | int | Role kodi (cross-references `authassignment`). |
| `LOGIN` | string | Login. |
| `PASSWORD` | string | bcrypt hash. |
| `CODE` | string | Recovery code. |
| `XML_ID` | string | Tashqi ID. |
| `PAY` | int | Pay-period flag. |
| `TEL` | string | Telefon. |
| `ACTIVE` | char(1) | Soft-delete. Loginni o'chirib qo'yadi. |
| `DIVICE_ID` | string | Oxirgi qurilma identifikatori (legacy spelling ga e'tibor bering). |
| `SYNC` | string | Sync ledger. |

### Read / write surface

Yozuv: `UserController`, mobile registration flow, password reset.
O'qish: har bir authenticated controller
(`Yii::app()->user->getUser()`), RBAC checker, license counter.

### Gotchas

- Haqiqiy permission grant `authassignment` va `authitem` da, `User`
  da emas. `ROLE` — denormalised hint.
- Legacy ustun nomi `DIVICE_ID` (xato) — migratsiyalarni yozishda
  saqlang.
- `ACTIVE='N'` keyingi so'rovda darhol login ni bloklaydi, ochiq
  mobile sync sessiyasi ham.

---

## `Product`

Source: `protected/models/Product.php`. `CActiveRecord` ni
to'g'ridan-to'g'ri kengaytiradi — **filial-shared** master satr.
`tableName()` returns `d0_product`. Primary key `PRODUCT_ID`. Live
DB: 50+ columns.

### Ustunlar (tanlangan)

| Column | Type | Maqsad |
|--------|------|--------|
| `PRODUCT_ID` | string | PK. |
| `TRADE_ID` | int | `TradeDirection` ga FK. |
| `PRODUCT_CAT_ID` | string | `ProductCategory` ga FK. |
| `NAME` | string | Display name. |
| `SORT` | int | Display order. |
| `VOLUME` | float | Birlik uchun kubometr. |
| `PACK_QUANTITY` | float | Pack uchun units. |
| `SAP_CODE` | string | ERP kodi. |
| `BAR_CODE` | string | EAN / UPC. |
| `IKPU` | string | O'zbekistan soliq tasniflash kodi. |
| `IKPU_PACK_CODE`, `IKPU_UNIT_CODE` | string | Variant IKPU kodlari. |
| `GTIN` | string | Global trade item number. |
| `ETTN_CODE` | string | ETTN / e-waybill kodi. |
| `VAT_RATE` | float | Output VAT %. |
| `EXCISE_RATE`, `EXCISE_RATE_TYPE` | float / int | Aksiz. |
| `TARA_ID` | string | `Tara` ga FK (tara depozit). |
| `WEIGHT` | float | Birlik uchun vazn. |
| `BLOCKS_IN_BOX` | int | Pack hierarchy info. |
| `SHELF_LIFE` | int | Kunlar. |
| `PHOTO` | string | Rasm URL. |
| `UNIT_ID` | string | `Unit` ga FK. |
| `PACK` | int | Pack-mode flag. |
| `SEGMENT`, `BRAND`, `PRODUCER` | int | Catalog dimensions. |
| `PROPERTY`, `PROPERTY1`, `PROPERTY2` | int | Free-form classification. |
| `BY_BLOCK` | string | 1 bo'lsa savdolar bloklarda bo'lishi kerak. |
| `CASE_TYPE_ID` | int | Case-pack type. |
| `IS_MML` | string | 1 bo'lsa "must-have" majburiy ro'yxat qismi. |
| `IS_OUR`, `IS_LOCAL` | string | Ownership / locality flags. |
| `CS_PRODUCT`, `CS_ID`, `CS_CAT_ID` | string / int | Cross-system catalog binding. |
| `XML_ID` | string | Tashqi ERP ID. |
| `DESCRIPTION` | string | Free-text. |
| `ACTIVE`, `SYNC`, `TIME`, `TIMESTAMP_X` | – | Standart. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Yozuv: `ProductController`, 1C import, Faktura.uz sync (IKPU).
O'qish: har bir catalog screen, har bir order line, har bir audit
(`AdtAudit`, `AudProduct`), har bir stock query.

### Gotchas

- `Product` filial-shared. Mahsulotni filialga cheklash uchun
  `ProductFilial` (= `d0_filial_product`) dan foydalaning.
- IKPU kodlari va aksiz O'zbekiston soliq qonunchiligi bo'yicha
  invoiceable mahsulotlar uchun majburiy; IKPU yo'qligi ESF
  submission ni bloklaydi.
- `BLOCKS_IN_BOX`, `PACK_QUANTITY`, `BY_BLOCK` o'zaro ta'sir qiladi:
  qoidalar uchun `docs/concepts/tara.md` ni o'qing.

---

## `ProductPriceMarkup`

Source: `protected/models/ProductPriceMarkup.php`. Extends
`CActiveRecord`. `tableName()` returns `d0_product_subcategory`
(jadval nomi misnomer; model per-product markup qoidalarini boshqaradi).
Primary key `ID`. Filial-shared.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `ID` | int | PK. |
| `PRODUCT` | string | `Product.PRODUCT_ID` ga FK. |
| `PRICE_TYPE` | string | Target price type. |
| `BASE_PRICE_TYPE` | string | Source price type. |
| `MARKUP` | float | Ko'paytirgich (`1.20` = +20%). |
| `ROUND_METHOD` | int | 0 nearest, 1 up, 2 down. |
| `ROUND_ACCURACY` | float | Yumaloqlash qadami (100, 500, 1000 va h.k.). |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Yozuv: `PriceTypeController::actionMarkup`, price-recalc cron.
O'qish: order submit (markup qoidasi faol bo'lsa `OrderDetail.PRICE`
ni hisoblaydi), price-list eksport.

### Gotchas

- Yalang'och `Product` satri narxlarni SAQLAMAYDI. Narxlar markup
  qoida + base price-type dan keladi, yoki to'g'ridan-to'g'ri
  `OldPrice` / o'xshash jadvallarga yuklanadi.
- `ROUND_ACCURACY` ning standart qiymatlari tenant-bog'liq — hech
  qachon 1000 deb taxmin qilmang.

---

## `PriceType`

Source: `protected/models/PriceType.php`. Extends `CActiveRecord` —
filial-shared. `tableName()` returns `d0_price_type`. Primary key
`PRICE_TYPE_ID`.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `PRICE_TYPE_ID` | string | PK. |
| `NAME` | string | Display name. |
| `CURRENCY` | string | `Currency` ga FK. |
| `PARENT` | string | Ixtiyoriy ota PriceType (markup chains). |
| `TYPE` | string | Sales / purchase / contract. |
| `FOR_CLIENT` | int | 1 bo'lsa mijozlarga ko'rinadi. |
| `OLD_PRICE_TYPE` | string | Legacy ID. |
| `FILIAL` | int | Ixtiyoriy filial scoping. |
| `DILER` | string | Tenant bo'linmasi. |
| `DESCRIPTION` | string | Free-text. |
| `SORT` | int | Display order. |
| `VALYUTA_ID` | int | `Valyuta` ga FK (currency alt). |
| `DEALER_PRICE` | int | 1 bo'lsa bu dealer-tier price. |
| `HAND_EDIT` | string | Y bo'lsa qo'lda override qilingan. |
| `XML_ID` | string | Tashqi ID. |
| `ACTIVE`, `SYNC`, `TIMESTAMP_X`, `TIME` | – | Standart. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Yozuv: `PriceTypeController`, 1C import. O'qish: mijozning default
(`Client.PRICE_TYPE_ID`), order submit, narxlarni ko'rsatadigan har
bir hisobot.

### Gotchas

- Mijoz order-submit da boshqa price type ni tanlash orqali default
  ni override qilishi mumkin — mobile app da faqat `FOR_CLIENT=1`
  bo'lgan price typelar tanlanadi.
- `PARENT` price-type chaining ni yoqadi; tsikllar insert da
  aniqlanmaydi va markup engine ni deadlock qiladi.
- `PriceTypeFilial` price type ni muayyan filiallar bilan
  cheklaydigan bog'lovchi modeldir.

---

## `Stock` (operatsion stock — `WarehouseDetail` ga ham qarang)

sd-main da `Stock` kontseptsiyasi bitta jadval emas. Uchta bog'liq
jadval bor:

- `d0_fN_warehouse_detail` — per-warehouse per-product on-hand satr.
  Model `WarehouseDetail`. **Bu kanonik "stock" jadval.**
- `d0_fN_store_detail` — van-selling flow uchun per-store per-product
  oyna (`Store` + `StoreDetail`).
- `d0_stock_exp` — ekspeditorning yuk mashinasi on-hand. Model
  `StockExp`.

Bu hujjatning eski versiyasidagi yuza `Stock` reference quyidagi uch
bo'lim bilan almashtirildi.

### `WarehouseDetail`

Source: `protected/models/WarehouseDetail.php`. Extends `BaseFilial`.
`filialTable()` returns `{{warehouse_detail}}`. PK `WAREHOUSE_DETAIL_ID`.
Live DB: 14 columns.

| Column | Type | Maqsad |
|--------|------|--------|
| `WAREHOUSE_DETAIL_ID` | string | PK. |
| `WAREHOUSE_ID` | string | `Warehouse` ga FK. |
| `STORE_ID` | string | `Store` ga FK (warehouse store bilan o'ralganda). |
| `PRODUCT_CAT_ID` | string | `ProductCategory` ga FK. |
| `PRODUCT_ID` | string | `Product` ga FK. |
| `TYPE` | string | Stock type / status. |
| `IDEN` | string | Guruhlash uchun identity tag. |
| `COUNT` | int | On-hand units. `Store.NEGATIVE_COUNT='Y'` bo'lsa manfiy bo'lishi mumkin. |
| `DILER_ID` | string | Tenant bo'linmasi. |
| `ACTIVE`, `SYNC`, `TIME`, `TIMESTAMP_X`, `ID` | – | Standart. |

### `StoreDetail`

Source: `protected/models/StoreDetail.php`. Extends `BaseFilial`.
`filialTable()` returns `{{store_detail}}`. PK `STORE_DETAIL_ID`.

`STORE_DETAIL_ID`, `STORE_ID`, `PRODUCT_CAT_ID`, `PRODUCT_ID`,
`COUNT`, `DILER_ID`, `TIMESTAMP_X`, `ACTIVE`, `SYNC`. Van-selling flow
tomonidan ishlatiladigan `Store` modeliga moslashtirilgan
`WarehouseDetail` oynasi.

### `StockExp`

Source: `protected/models/StockExp.php`. Extends `BaseFilial`.
`filialTable()` returns `{{stock_exp}}`. PK `ID`.

| Column | Type | Maqsad |
|--------|------|--------|
| `ID` | string | PK. |
| `PRODUCT_ID` | string | FK. |
| `CLIENT_ID` | string | FK (mijozga consignment, VS / mobile sale tomonidan ishlatiladi). |
| `AGENT_ID` | string | FK. |
| `USER_ID` | string | FK. |
| `COUNT` | float | Units. |
| `DATE` | datetime | Event date. |
| `DATE_PRO`, `DATE_EXP` | datetime | Manufacture / expiry. |
| `COMMENT` | string | Free-text. |
| `ACTIVE`, `SYNC`, `TIMESTAMP_X`, `TIME` | – | Standart. |
| `CREATE_BY` / `CREATE_AT` / `UPDATE_BY` / `UPDATE_AT` | – | Audit. |

### Gotchas

- Ikkita stock jadval (`WarehouseDetail` + `StoreDetail`)
  `StoreLog` triggerlari / job tomonidan sinxron saqlanadi. Drift
  qayta sync ni talab qiladi.
- `Store.NEGATIVE_COUNT='Y'` bo'lganda manfiy stock ruxsat etilgan;
  ko'p hisobotlar manfiylarni jim filtr qiladi.
- `StockExp` satrlari faol trip vaqtidagi ekspeditor yuk mashinasi
  inventarizatsiyasi. Trip yopilishida `ExpeditorLoad` orqali
  reconcile qiling.

---

## `Warehouse`

Source: `protected/models/Warehouse.php`. Extends `BaseFilial`.
`filialTable()` returns `{{warehouse}}`, resolves to `d0_fN_warehouse`.
Primary key `WAREHOUSE_ID`. Live DB: 14 columns.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `WAREHOUSE_ID` | string | PK. |
| `DILER_ID` | string | Tenant bo'linmasi. |
| `TYPE` | string | Saqlash turi. |
| `TYPE_LIMIT` | string | Ruxsat etilgan product-type filter. |
| `NAME` | string | Display name. |
| `IDEN` | string | Identity tag. |
| `COUNT` | int | Snapshot. |
| `CONDITION` | string | Free-text (masalan, cold-storage). |
| `COMMENT` | string | Free-text. |
| `ACTIVE`, `SYNC`, `TIME`, `TIMESTAMP_X`, `ID` | – | Standart. |

### Read / write surface

Yozuv: `WarehouseController`, 1C import. O'qish: stock-on-hand
queries, trip planner (`STORE_ID -> WAREHOUSE_ID` zanjiridan
tanlash), inventory module (`Inventory*`).

### Gotchas

- `Warehouse` ≠ `Store`. `Store` (model `Store`, table `d0_store`) —
  bu **vending** birligi (cash register / POS yoki ekspeditor van).
  `Warehouse` — bu **storage** birligi, ikkisi farq qilganda
  `WarehouseLocation` orqali map qilinadi.
- `WarehouseDetail` mahsulot bo'yicha haqiqiy on-hand ni olib yuradi.

---

## `Visit`

Source: `protected/models/Visit.php`. Extends `BaseFilial`.
`filialTable()` returns `{{visit}}`. Primary key composite (`ID`,
`DATE`). Live DB: 28 columns.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `ID` | int | PK qismi (autoincrement). |
| `DATE` | datetime | PK qismi; tashrif boshlanish vaqti. |
| `AGENT_ID` | string | `Agent` ga FK. |
| `USER_ID` | string | `User` ga FK. |
| `CLIENT_ID` | string | `Client` ga FK. |
| `VISITED` | char(1) | `Y` bo'lsa check-in bo'lgan. |
| `ORDER` | char(1) | `Y` bo'lsa order joylashtirilgan. |
| `REJECT` | char(1) | `Y` bo'lsa rejection / no-buy sababi log qilingan. |
| `PHOTO` | char(1) | `Y` bo'lsa foto biriktirilgan. |
| `AUDIT` | char(1) | `Y` bo'lsa audit qilingan. |
| `LON`, `LAT` | float | Check-in geo koordinatalari. |
| `DISTANCE` | float | Outletdan metrlar, save da server-side hisoblangan. |
| `GPS_STATUS` | int | GPS sifati: 0 disabled, 1 ok, 2 stale, 3 mock. |
| `CHECK_IN_TIME` | datetime | Mobile-side check-in vaqti. |
| `CHECK_OUT_TIME` | datetime | Check-out vaqti. |
| `PLANED` | char(1) | `Y` bo'lsa tashrif rejada edi. |
| `STORE_CHECK` | char(1) | `Y` bo'lsa shelf check bajarilgan. |
| `PAYMENT`, `DELIVERY`, `POLL`, `ORDER_REPLACE`, `ORDER_DEFECT` | char(1) | Per-step completion flags. |
| `SYNC_TIME` | datetime | Sync tugaganida. |
| `DAY` | date | Tez guruhlash uchun kesilgan `DATE`. |
| `POSITION_ID` | string | Tashrif vaqtidagi role / position. |
| `ROLE` | string | Role text. |

### Read / write surface

Yozuv: mobile API check-in + check-out + step-completion endpointlari.
O'qish: visit dashboard, KPI engine, audit module, outlet-fact
aggregator.

### Gotchas

- `GPS_STATUS=3` (mock GPS) potentsial fraud ni flaglaydi — ko'p
  hisobotlar bu filtr qiladi va tashrif KPI ga hisoblanmaydi.
- Composite PK shuni anglatadiki, bir xil mijozga bir xil `DATE`
  sekundida ikki tashrif to'qnashadi. Mobile retry-lar noyob
  vaqtlardan foydalanishi kerak.
- `DISTANCE` `Client.LON / LAT` dan server-tomondan hisoblangan; geo
  koordinatalarisiz outletlar har doim 0 hisobot beradi.

---

## `Gps`

Source: `protected/models/Gps.php`. Extends `BaseFilial`.
`filialTable()` returns `{{gps}}`. PK composite (`ID`, `DATE`). Live
DB: 20 columns.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `ID` | int | PK qismi (autoincrement). |
| `DATE` | datetime | PK qismi. |
| `AGENT_ID` | string | `Agent` ga FK. |
| `USER_ID` | string | `User` ga FK. |
| `TYPE` | string | Event type. |
| `ORDER_ID` | string | Ping order ga bog'langan bo'lsa `Order` ga FK. |
| `CLIENT_ID` | string | Ping tashrifga bog'langan bo'lsa `Client` ga FK. |
| `LAT`, `LON` | float | Koordinatalar. |
| `BATTERY` | int | Ping vaqtidagi battery %. |
| `PROVIDER` | string | `gps` / `network` / `fused`. |
| `SIGNAL` | int | Signal kuchi. |
| `MODE` | string | Mobile activity mode. |
| `INTERNET_STATUS` | int | Connectivity. |
| `GPS_STATUS` | int | Mock-detection. |
| `MOB_TIMESTAMP` | string | Ping da client soati. |
| `TIMESTAMP_X` | datetime | Server qabuli. |
| `DAY` | date | Indekslash uchun kesilgan sana. |
| `DEVICE` | string | Device identifier. |

### Read / write surface

Yozuv: mobile sync (yuqori volume — faol soatlarda har necha
sekundda ping). O'qish: GPS-history view, fraud detection (mock GPS),
trip replay tool.

### Gotchas

- Bu **eng yuqori volumeli per-tenant jadval**. Scaling out dan
  oldin partitioning ni rejalashtiring — `DATE` composite-PK to'g'ri
  o'q.
- Eski satrlar period-close job tomonidan alohida cold jadvalga
  arxivlanadi; agar 90 kundan eski o'qisangiz, arxivga maqsad qiling.
- Qurilma soatlari drift qilganda `MOB_TIMESTAMP` haqiqat manbasi
  vaqti; `TIMESTAMP_X` server arrival.

---

## `Trip`

Source: `protected/models/Trip.php`. Extends `BaseFilial`.
`filialTable()` returns `{{trip}}`. Primary key `ID`. Live DB da
trip-line many-to-many uchun singildosh `TripOrder` modeli bor.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `ID` | int | PK. |
| `CAR_ID` | int | `Car` ga FK. |
| `COURIER_ID` | string | `Expeditor.EXPEDITOR_ID` ga FK (courier roli). |
| `EXPEDITOR_ID` | string | `Expeditor.EXPEDITOR_ID` ga FK (tayinlangan expeditor). |
| `STORE_ID` | string | `Store.STORE_ID` ga FK (origin). |
| `DATE` | datetime | Rejalashtirilgan jo'natilish. |
| `STATUS` | int | 1 waiting, 2 active, 3 done, 4 cancelled. |
| `ACTIVE` | char(1) | Soft delete. |

### `TripOrder`

PK `ID`. Ustunlar `TRIP_ID`, `ORDER_ID`, `SORT`. Trips va orders
o'rtasidagi many-to-many aniq tartib bilan.

### Read / write surface

Yozuv: trip-planner UI, ekspeditor mobile app departure / arrival
da. O'qish: ekspeditor view, trip-progress dashboard.

### Gotchas

- `COURIER_ID` va `EXPEDITOR_ID` alohida rollar — courier haydashi
  mumkin, ekspeditor cash yig'ish uchun mas'ul bo'lgan paytda.
- To'liq state machine uchun `docs/concepts/trip-lifecycle.md` ga
  qarang.

---

## `Payment` (sd-main payment satri)

sd-main da "payment" bitta jadval emas. Tegishli jadvallar:

- `d0_fN_payment_deliver` — ekspeditor tomonidan tortib olingan
  confirm-on-delivery payment. Model `PaymentDeliver`.
- `d0_fN_payment_transfer` — cashboxes / filiallar o'rtasidagi
  multi-step transfer. Model `PaymentTransfer`.
- `d0_fN_payment_displacement` — ichki displacement ledger. Model
  `PaymentDisplacement`.

sd-billing `Payment` (boshqa sxemada) bog'liq emas; aralashtirib
yubormang.

---

## `PaymentDeliver`

Source: `protected/models/PaymentDeliver.php`. Extends `BaseFilial`.
`filialTable()` returns `{{payment_deliver}}`. PK `ID`. Live DB: 23 columns.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `ID` | int | PK. |
| `CLIENT_ID` | string | `Client` ga FK. |
| `ORDER_ID` | string | `Order` ga FK. |
| `SUMMA` | float | Paid amount. |
| `CURRENCY` | string | `Currency` ga FK. |
| `DATE` | datetime | Payment date. |
| `USER_ID` | string | Kassir user (agar bo'lsa). |
| `AGENT_ID` | string | Yig'uvchi agent (agar bo'lsa). |
| `TRADE_ID` | string | `TradeDirection` ga FK. |
| `TERM` | string | Payment terms / kanal. |
| `CONFIRM` | string | Confirmation status. |
| `COMMENT` | string | Free-text. |
| `CREATE_BY` / `UPDATE_BY` / `CREATE_AT` / `UPDATE_AT` | – | Audit. |

### Read / write surface

Yozuv: ekspeditor mobile API yetkazib berishni tasdiqlashda, kassir
UI. O'qish: order debt reconciliation, daily-cash report.

### Gotchas

- `PaymentDeliver` satri manager tasdiqlaganda `payment` turidagi
  tegishli `ClientTransaction` ni post qilish uchun **triggerdir**.
  Shu paytgacha u pending state da o'tiradi.
- `CONFIRM='Y'` tegishli `ClientTransaction.STATUS` ni confirmed ga
  o'tkazadigan narsa.

---

## `PaymentTransfer`

Source: `protected/models/PaymentTransfer.php`. Extends `BaseFilial`.
`filialTable()` returns `{{payment_transfer}}`. PK
`PAYMENT_TRANSFER_ID`. Live DB: 13 columns.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `PAYMENT_TRANSFER_ID` | string | PK. |
| `DOCUMENT_ID` | string | Source document ID (ko'pincha ota transfer yoki order). |
| `OPERATION_ID` | int | 1 sending, 2 receiving. |
| `FILIAL_ID` | int | Satr tegishli bo'lgan filial. |
| `CURRENCY_ID` | string | `Currency` ga FK. |
| `SUMMA` | float | Transfer amount. |
| `STATUS` | int | 1 new, 2 pending, 3 accepted, 4 rejected, 5 cancelled. |
| `COMMENT` | string | Free-text. |
| `CREATE_AT` / `CREATE_BY` / `UPDATE_AT` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Yozuv: cross-filial transfer UI, reconciliation cron. O'qish: finans
dashboard, transfer-status modal.

### Gotchas

- Har bir transfer odatda **ikki satr** sifatida yashaydi: source
  filialda `OPERATION_ID=1` sending satr, destination filialda
  `OPERATION_ID=2` receiving satr. Transfer bajarilgan deb hisoblanish
  uchun ikkalasi ham `STATUS=3` ga yetishi kerak.
- `STATUS=4` (rejected) `ClientTransaction` da qo'lda tuzatish
  qilinmaguncha pulni limbda qoldiradi.

---

## `Cashbox`

Source: `protected/models/Cashbox.php`. Extends `BaseFilial`.
`filialTable()` returns `{{cashbox}}`. PK `ID`. Live DB: 15 columns.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `ID` | int | PK. |
| `NAME` | string | Display name. |
| `CURRENCY` | string | `Currency` ga FK. |
| `KASSIR` | string | Kassir uchun `User.USER_ID` ga FK. |
| `SORT` | int | Display order. |
| `XML_ID` | string | Tashqi ID. |
| `ACTIVE`, `SYNC`, `TIMESTAMP_X`, `TIME` | – | Standart. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Yozuv: `CashboxController`. O'qish: cash bilan bog'liq har bir
`ClientTransaction`, daily cash close, sd-billing ning cashbox
aggregatori.

### Gotchas

- `CashboxDisplacement` (`d0_cashbox_displacement`) cashbox-lar
  o'rtasidagi harakatni yozadi; closing balance running sumdan keladi.
- `Cashbox` satri `BaseFilial` orqali filial-scoped. Filiallar
  o'rtasida ID-larni ulashmang.

---

## `AdtAuditResult`

Source: `protected/models/AdtAuditResult.php`. Extends `BaseFilial`.
`filialTable()` returns `{{adt_audit_result}}`. PK `ID`. Live DB: 12 columns.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `ID` | int | PK. |
| `VISIT_ID` | int | `Visit.ID` ga FK. |
| `DATE` | datetime | Audit timestamp. |
| `CLIENT_ID` | string | `Client` ga FK. |
| `POSITION_ID` | int | Audit vaqtidagi role / position. |
| `AUDIT_ID` | int | `AdtAudit.ID` ga FK. |
| `USER_ID` | string | `User` ga FK. |
| `CREATE_AT` / `UPDATE_AT` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Yozuv: agentning mobile audit qadami orqali audit moduli. O'qish:
audit dashboard, KPI engine, photo-report cross-references.

### Gotchas

- `AdtAuditResult` auditning **sarlavhasi**. Per-SKU satrlar
  `AdtAuditResultData` ga boradi.
- Bu v2 audit engine ("ADT"). Eski `AuditStorchekCat` / `Auditor`
  jadvallari v1 engine uchun. Birga mavjud.

---

## `AdtAuditResultData`

Source: `protected/models/AdtAuditResultData.php`. Extends
`BaseFilial`. `filialTable()` returns `{{adt_audit_result_data}}`.
PK `ID`. Live DB: 12 columns.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `ID` | int | PK. |
| `RESULT_ID` | int | `AdtAuditResult.ID` ga FK. |
| `PRODUCT_ID` | int | `Product` ga FK. |
| `PRICE` | float | Observed shelf price. |
| `FACE` | int | Facing count. |
| `SOLD` | int | Oxirgi tashrifdan beri xabar berilgan sold-out count. |
| `STORE` | int | Kuzatilgan shelf-stock. |
| `AVAILABLE` | bool | TRUE bo'lsa SKU javonda. |
| `OUT_OF_STOCK` | bool | TRUE bo'lsa javon bo'sh. |
| `CREATE_AT` / `UPDATE_AT` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Yozuv: parent bilan bir xil. O'qish: shelf-share report, OOS report,
KPI engine.

### Gotchas

- Edge case-lar tufayli `AVAILABLE` ham, `OUT_OF_STOCK` ham mavjud —
  SKU `AVAILABLE=false` bo'lishi mumkin (listed emas), bu
  `AVAILABLE=true && OUT_OF_STOCK=true` (listed, lekin bo'sh) dan
  farq qiladi.
- Audit SKU OOS bo'lsa ham narxni yozishi mumkin — `PRICE` oxirgi
  ko'rilgan shelf price.

---

## `KpiTask`

Source: `protected/models/KpiTask.php`. Extends `BaseFilial`.
`filialTable()` returns `{{kpi_task}}`. PK `KPI_TASK_ID`. Live DB: 58 columns.

KPI engine satri. Bir `KpiTask` row = bitta agentga (yoki scope)
sanalar oynasiga tayinlangan KPI.

### Ustunlar (tanlangan)

| Column | Type | Maqsad |
|--------|------|--------|
| `KPI_TASK_ID` | string | PK. |
| `KPI_ID` | string | `Kpi` ga FK (KPI master). |
| `DILER_ID` | string | Tenant bo'linmasi. |
| `NAME` | string | Display name. |
| `SORT` | int | Display order. |
| `TASK_TYPE` | string | Task code (sales-sum, AKB, OOS, etc.). |
| `VALUE` | float | Target / threshold value. |
| `DATE_TYPE` | string | Day / week / month / quarter. |
| `STATUS` | string | Active / paused. |
| `PRODUCT_ID`, `PRODUCT_CAT` | string | Ixtiyoriy product / category scoping. |
| `CLIENT_CAT`, `CLIENT_CLASS`, `CITY_ID`, `AGENT` | string | Ixtiyoriy dimensional scoping. |
| `CURRENCY` | string | `Currency` ga FK. |
| `KPI_SHARE` | float | Agentning umumiyidagi bu KPI ning vazni. |
| `BONUS_TYPE` | string | Bonus payout mode. |
| `BONUS` | float | Threshold ga yetganda bonus amount. |
| `MARK`, `MARK2..MARK5` | int | Threshold marks. |
| `MARK2_KPI_SHARE`, `MARK2_BONUS_SHARE`, … `MARK5_*` | int | Har bir bosqichdagi ulush. |
| `ACTIVE`, `SYNC`, `TIME`, `TIMESTAMP_X` | – | Standart. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Yozuv: KPI admin UI, KPI templating job. O'qish: KPI dashboard,
payroll, agentning mobile dashboard "tasks" paneli.

### Gotchas

- `KpiTask` — **per-period** — agent uchun period bo'yicha bitta
  satr. Template (`KpiTaskTemplate` ga qarang) — bu satrlarni ishlab
  chiqarish uchun klonlanadigan narsa.
- `MARK2..MARK5` zinapoyasi tiered bonus payout ni kodlaydi —
  yuqoriroq marks katta `MARK*_BONUS_SHARE` ni ochadi. Qayta
  hisoblash o'rniga `KpiCalculator` da ladder helper dan foydalaning.

---

## `KpiTaskTemplate`

Source: `protected/models/KpiTaskTemplate.php`. Extends `BaseFilial`.
`filialTable()` returns `{{kpi_task_template}}`. PK `ID`. Live DB: 62 columns.

`KpiTask` ustunlarini oynalantiradi, lekin template satri — bu
period-realised task emas, design-time spetsifikatsiya. Templates har
bir period boshida template-instantiation job tomonidan
`KpiTask`-satrlarga klonlanadi. `KpiTask` ga nisbatan qo'shimcha
ustunlar `MIN_SUM`, `NEW_CLIENTS`, `REPLACEMENTS`, `SUPERVISER`,
`ACCESS_TO_OTHERS`, `ACCESS_TO_USE`, `MAX_BONUS` ni o'z ichiga oladi —
design-time knobs.

### Read / write surface

Yozuv: KPI admin UI. O'qish: period-instantiation cron — keyingi
period uchun `KpiTask`-satrlarni ishlab chiqaradi.

### Gotchas

- Templates `KpiTaskTemplateGroup` da yashaydi (kichik guruh jadvali);
  template ni qayta guruhlash allaqachon faol `KpiTask`-satrlarni
  qayta instantsiya qilmaydi.

---

## `KpiTaskTemplateGroup`

Source: `protected/models/KpiTaskTemplateGroup.php`. Extends
`CActiveRecord`. `tableName()` returns `d0_kpi_task_template_group`.
PK `ID`. Live DB: 10 columns.

Yengil grouping jadval — name, description, sort order, audit. Admin
UI da KPI templates ni tashkil etish uchun ishlatiladi.

---

## `Plan`

Source: `protected/models/Plan.php`. Extends `BaseFilial`.
`filialTable()` returns `{{plan}}`. PK `PLAN_ID`. Live DB: 12 columns.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `PLAN_ID` | int | PK. |
| `DILER_ID` | int | Tenant bo'linmasi. |
| `PLAN` | string | Plan payload (ko'pincha sub-planlarning JSON-i). |
| `NAME` | string | Display name. |
| `MONTH`, `YEAR` | int | Period. |
| `PLAN_COMPLETED` | string | Kesh qilingan completion %. |
| `TIMESTAMP_X` | datetime | Standart. |
| `ACTIVE` | char(1) | Soft delete. |
| `SYNC` | string | Sync. |

### `PlanProduct`

Per-product plan satrlari uchun singildosh jadval. PK `ID`. 13 ustun,
shu jumladan `PLAN_ID`, `PRODUCT_ID`, `COUNT`, `SUMMA`.

### Read / write surface

Yozuv: planning admin UI, plan-import job. O'qish: KPI engine,
sales-vs-plan dashboard, payroll calculator.

### Gotchas

- `Plan` `BaseFilial` orqali filial-scoped, shuning uchun
  cross-filial rejalashtirish filial uchun bitta satr yozishni
  anglatadi.
- `PLAN_COMPLETED` kesh har soatda qayta hisoblanadi; live SLA uchun
  unga tayanmang.

---

## `Bonus`

Source: `protected/models/Bonus.php`. Extends `CActiveRecord` —
filial-shared. `tableName()` returns `d0_bonus`. PK `BONUS_ID`. Live
DB: 36 columns. Buy-X-get-Y promo engine satri.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `BONUS_ID` | string | PK. |
| `DILER_ID` | string | Tenant bo'linmasi. |
| `NAME` | string | Display name. |
| `BONUS_TYPE` | int | Type code (gift, discount, free SKU, etc.). |
| `PRODUCT` | string | Trigger product IDs (CSV / JSON). |
| `CURRENCY` | string | FK. |
| `CLIENT_TYPE`, `CLIENT_CHANNEL`, `CLIENT_CAT` | string | Client scoping. |
| `PRICE_TYPE` | string | `PriceType` ga FK. |
| `BONUS_PRODUCTS` | string | Gift / bonus product IDs. |
| `BONUS` | string | Bonus payload (count / pct / amount). |
| `PARENT` | string | Parent bonus chain. |
| `VALUE` | string | Trigger threshold (count or sum). |
| `AGENT_ID` | string | Ixtiyoriy agent scoping. |
| `CITY` | string | Ixtiyoriy city scoping. |
| `MIN_COUNT`, `MAX_COUNT` | string | Trigger ranges. |
| `DATE`, `DATE_FROM`, `DATE_TO` | datetime | Active window. |
| `IS_PUBLIC` | string | Public-listing flag. |
| `ONLY_ONE_TIME` | int | 1 = bir mijozga bir martalik almashtirish. |
| `MAX_BONUS` | int | Payout cap. |
| `MANUAL` | string | Manual / auto flag. |
| `ACTIVE`, `SYNC`, `TIME`, `ID` | – | Standart. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Yozuv: bonus admin UI. O'qish: order-submit engine — har bir order
bonus qoidalarini ishga tushiradi va child `BonusOrder` satrini
ishlab chiqarishi mumkin.

### Gotchas

- Trigger maydonlari (`PRODUCT`, `MIN_COUNT`, etc.) string-encoded
  — CSV deb taxmin qilishdan oldin `BonusComponent` dagi parsing
  helper ni o'qing.
- Bonus **avtomatik** bo'lishi mumkin (`MANUAL=N`, engine uni
  qoniqarli orderlarda qo'llaydi) yoki **qo'lda** (agent submit da
  bonus ni tanlaydi).
- Shuningdek qarang: `BonusOrder`, `BonusOrderDetail`,
  `BonusOrderHistory`, `BonusRelation`, `BonusAgent`, `BonusCity`,
  `BonusExclude`, `BonusFilial`, `BonusLimit` — bonus engine ko'p
  satellit jadvallarga fan-out qiladi.

---

## `BonusRelation`

Source: `protected/models/BonusRelation.php`. Extends `CActiveRecord`.
`tableName()` returns `d0_bonus_relation`. PK `ID`. Live DB: 7 columns.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `ID` | int | PK. |
| `PARENT_ID` | string | Ota `BONUS_ID`. |
| `RELATED_BONUS_ID` | string | Related child `BONUS_ID`. |
| audit columns | – | Standart. |

### Gotchas

- Bu jadval bonus **zanjirlarini** kodlaydi — X sotib olish bonus
  B1 ga, bu o'z navbatida qo'shimcha shartlar bajarilsa B2 ga
  qoniqadi. Insert vaqtida tsikllar yaratilmasligi kerak.

---

## `Skidka`

Source: `protected/models/Skidka.php`. Extends `CActiveRecord` —
filial-shared. `tableName()` returns `d0_skidka`. PK `SKIDKA_ID`.
Live DB: 37 columns. Discount-rule engine satri. Singildosh jadvallar:
`SkidkaAgent`, `SkidkaBudget`, `SkidkaExclude`, `SkidkaFilial`,
`SkidkaManual`, `SkidkaOrder`, `SkidkaRelation`, `SkidkaStore`.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `SKIDKA_ID` | string | PK. |
| `NAME` | string | Display name. |
| `DILER_ID` | string | Tenant. |
| `SKIDKA_TYPE` | int | Type code (% off, fixed, threshold etc.). |
| `PRODUCT` | string | Trigger products. |
| `CLIENT_CAT`, `CLIENT_TYPE`, `CLIENT_CHANNEL`, `CITY` | string | Scoping. |
| `CURRENCY` | string | FK. |
| `VALUE` | float | Threshold value. |
| `SKIDKA` | float | Discount value (percent or amount). |
| `PARENT` | string | Parent chain. |
| `DATE_FROM`, `DATE_TO` | datetime | Active window. |
| `BUDGET` | float | Barcha almashtirishlar bo'yicha hard cap. |
| `COMMENT` | string | Free-text. |
| `IS_PUBLIC` | string | Mijozlarga ko'rinadi. |
| `ONLY_ONE_TIME` | int | 1 = bir martalik almashtirish. |
| `NUM_CATEGORIES` | int | Cross-category threshold support. |
| `ACTIVE`, `SYNC`, `TIME`, `ID`, `TIMESTAMP_X` | – | Standart. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Yozuv: discount admin UI. O'qish: order-submit engine — qoidani
qo'llaydi va `SkidkaOrder` satrini post qiladi. Qo'lda override-lar
`SkidkaManual` orqali boradi.

### Gotchas

- `SkidkaManual` satri manager bir martalik chegirma qo'llaganda
  yaratiladi — uning o'z PK va byudjeti bor.
- `BUDGET` hard cap. Byudjet sarflangach keyingi qoniqarli orderlar
  chegirmani olmaydi; `SkidkaBudget` running total orqali tasdiqlang.

---

## `Filial`

Source: `protected/models/Filial.php`. Extends `CActiveRecord` —
**emas** `BaseFilial` (bu prefikslarni belgilaydigan ildiz jadval).
`tableName()` returns `d0_filial`. PK `id`. Live DB: 8 columns.

### Ustunlar

| Column | Type | Maqsad |
|--------|------|--------|
| `id` | int | PK. |
| `domain` | string | Tenant domain assignment. |
| `is_main` | int | 1 bo'lsa root filial. |
| `prefix` | string | Per-filial jadval prefiksi (`f0`, `f1`, …). |
| `xml_id` | string | Tashqi ID. |

### Read / write surface

Yozuv: tenant onboarding flow (kamdan-kam; odatda tenant uchun bir
marta). O'qish: har bir so'rovda `FilialComponent`, har bir
`BaseFilial` avlodi.

### Gotchas

- Satrlar mavjud bo'lganidan keyin `prefix` ni o'zgartirish har bir
  per-filial table lookup ni buzadi. Har doim yangi filial yarating;
  hech qachon qayta prefiks qo'ymang.
- `is_main=1` tenant uchun aniq bir marta paydo bo'lishi kerak; root
  filial — `Bonus`, `Skidka`, `Product`, `PriceType` va h.k.
  yashaydigan joy.

---

## `ClientCategory`

Source: `protected/models/ClientCategory.php`. Extends
`CActiveRecord` — filial-shared. `tableName()` returns
`d0_client_category`. PK `CLIENT_CAT_ID`. Live DB: 15 columns.

### Ustunlar

`CLIENT_CAT_ID`, `NAME`, `DESCRIPTION`, `SORT`, `XML_ID`, `ACTIVE`,
`SYNC`, `CREATE_AT`, `UPDATE_AT`, `CREATE_BY`, `UPDATE_BY`,
`TIMESTAMP_X`, `ID`.

### Read / write surface

Yozuv: directory admin UI, 1C import. O'qish: hisobotlar bo'yicha
filterlar (`Client.CLIENT_CAT`, `Order.CLIENT_CAT`, KPI scoping).

### Gotchas

- Kategoriyani o'chirish kaskad qilmaydi — orphaned `CLIENT_CAT`
  havolalari jim ravishda hisobotlarda bo'sh joinlarni qaytaradi.

---

## `ClientChannel`

Source: `protected/models/ClientChannel.php`. Extends `CActiveRecord`.
`tableName()` returns `d0_client_channel`. PK `ID`. Live DB: 8 columns.

### Ustunlar

`ID`, `NAME`, `XML_ID`, `CREATE_BY`, `UPDATE_BY`, `CREATE_AT`,
`UPDATE_AT`.

### Read / write surface

Yozuv: directory admin. O'qish: `Client.CHANNEL`, bonuslarda
(`Bonus.CLIENT_CHANNEL`) va chegirmalarda (`Skidka.CLIENT_CHANNEL`)
scoping.

### Gotchas

- `ClientChannel` va `ClientClass` — alohida dimensions; aralashtirib
  yubormang.

---

## `Contract` / `ContractClient`

Status: kod bazasidagi `Contract.php` va `ContractClient.php` model
sinflari **deprecated** (`.obsolete` ga qayta nomlangan), lekin live
jadval `d0_contract` (16 ustun, InnoDB / utf8mb3, Yii modeli yo'q)
hali ham hisobotlar va Faktura / Didox integratsiyasi tomonidan
so'raladi. Yangi kod uchun shartnoma ma'lumotlari `Contragent`
oilasida yashaydi (`d0_contragent`, `d0_contragent_history`,
`d0_contragent_log`).

### `d0_contract` (legacy, modelsiz)

`Order.CONTRACT_ID` ga cross-reference. Orqaga moslik uchun DAO
orqali to'g'ridan-to'g'ri o'qiladi. Yangi ishlar `Contragent` modeliga
maqsad qilishi kerak.

### `d0_contragent` (joriy)

Model `Contragent` (`protected/models/Contragent.php`). 39 ustun. PK
`CLIENT_ID`. `Client` ga bog'langan huquqiy ravishda tashkil etilgan
kontragentni saqlaydi (`ServerSettings::isContragent()` yoqilganda).
Bank ma'lumotlari, IKPU defaults, contract anchor data ni olib yuradi
va bu Faktura.uz va Didox invoice qurish uchun ishlatiladigan
manba satr.

### Gotchas

- `Contract.php.obsolete` ni kengaytirmang. Yangi ustunlar
  `Contragent` ga boradi.
- `Client` da 1:1 `Contragent` oyna bo'lishi mumkin (contragent
  rejimi yoqilganda) yoki yo'q — order kod
  `ServerSettings::isContragent()` orqali join haqida defensivdir.

---

## Domain guruhlash

Yuqorida hujjatlangan 30 jadval domen bo'yicha guruhlangan. Domen-dan
tegishli bo'limga sakrash uchun bu indeks-dan foydalaning.

| Domen | Jadvallar |
|-------|-----------|
| Orders | `Order`, `OrderDetail`, `OrderHistory` |
| Catalog | `Product`, `PriceType`, `ProductPriceMarkup` |
| Stock | `WarehouseDetail`, `Warehouse`, `StockExp` ("Stock" bo'lim ostida) |
| Clients | `Client`, `ClientCategory`, `ClientChannel`, `Contract` / `Contragent` |
| Finans | `ClientTransaction`, `PaymentDeliver`, `PaymentTransfer`, `Cashbox` |
| Team | `Agent`, `Supervayzer`, `Expeditor`, `User` |
| Visits & GPS | `Visit`, `Gps`, `Trip` (+ `TripOrder`) |
| Audit | `AdtAuditResult`, `AdtAuditResultData` |
| KPI | `KpiTask`, `KpiTaskTemplate`, `KpiTaskTemplateGroup`, `Plan` |
| Promo | `Bonus`, `BonusRelation`, `Skidka` |
| Tenant | `Filial` |

Ustun sanoqlari, PK va live-DB cross-checks bilan **306 modelning
to'liq indeksi** uchun `docs/data/schema-reference.md` ga qarang.
Yuqori darajadagi flowlar (order → finans, visit → KPI) uchun
`docs/architecture/diagrams.md` ostidagi diagrammalarni va
`docs/concepts/` ostidagi kontseptsiya hujjatlarini ko'ring.
