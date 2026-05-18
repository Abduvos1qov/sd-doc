---
sidebar_position: 3
title: Основные сущности
audience: Backend engineers, QA, Data engineers, Integrators, BI / reporting team
summary: Подробный per-table справочник по 30 ключевым таблицам sd-main. Каждая секция описывает файл модели, имя таблицы, первичный ключ, основные связи по внешним ключам, колонки с типом и назначением, индексы, и какие контроллеры / cron-задачи пишут и читают строку. Используйте вместе с `schema-reference.md` (общие статистики БД + индекс 306 моделей) как единый источник истины для слоя данных.
topics: [schema, models, tables, columns, foreign-keys, indexes, sd-main, base-filial, multi-tenant]
---

# Основные сущности

Эта страница — **углублённый per-table разбор** для 30 самых
нагруженных таблиц sd-main. Сначала откройте
`docs/data/schema-reference.md`, если вам нужна общая картина БД
(подсчёты, распределение engine / charset, полный индекс 306
моделей). На этой странице мы идём глубже для 30 таблиц, которые
встречаются в каждом отчёте, в каждом sync-запросе, и в каждом
закрытии периода.

## Как читать эту страницу

Каждая H2-секция имеет одинаковую форму:

- **Source line** — путь к файлу модели, значение `tableName()` /
  `filialTable()`, первичный ключ.
- **Колонки** — каждая колонка, задокументированная в docblock
  `@property`, перепроверенная по live-схеме MySQL. Колонка типа
  показывает PHP-тип; live-тип БД добавлен в скобках, где это даёт
  информацию (например, `int (TINYINT)`, `string (varchar 32)`).
- **Индексы** — нетривиальные индексы из live-схемы, когда у таблицы
  они есть. Индексы PK по одной колонке опущены.
- **Связи** — то, что объявляет `relations()` модели, плюс важные
  обратные ссылки от других моделей.
- **Read / write surface** — какие контроллеры, действия, cron-задачи
  и API пишут в строку, и какие отчёты / endpoints её читают.
- **Gotchas** — тонкие моменты поведения, устаревшие колонки,
  soft-delete vs hard-delete, пары двойного учёта и т.п. Прочитайте
  это перед тем, как трогать таблицу.

## `BaseFilial` и per-filial префикс таблицы

Базовый класс `BaseFilial` (в `protected/models/BaseFilial.php`) —
механика per-tenant подразделений. Модель, расширяющая `BaseFilial`,
объявляет своё логическое имя таблицы через `filialTable()` (например,
`return '{{order}}'`). В рантайме `tableName()` переписывает
плейсхолдер в `d0_fN_order`, где `fN` — активный filial-префикс,
возвращаемый `FilialComponent::getFilialPrefix()`. Префикс `f0_`
представляет общий / корневой filial — большинство master-data таблиц
живут там.

Модель, расширяющая `CActiveRecord` напрямую (например, `Product`,
`PriceType`, `Filial`, `Bonus`, `Skidka`), — **filial-shared**:
существует ровно одна строка на весь тенант.

Флаг `BaseFilial::isCommon` позволяет per-filial модели обойти
переписывание для запросов, которые должны попадать только в корневой
filial. Читайте `BaseFilial::allTables()`, если нужно перечислить
каждую per-filial копию таблицы (используется engine закрытия периода
и cross-filial отчётами).

Синтаксис `{{tableName}}` (плейсхолдер таблицы Yii) обрабатывается
DB-слоем Yii, чтобы внедрить настроенный префикс таблицы (`d0_`). Для
модели `BaseFilial` плейсхолдер также получает filial-префикс,
внедряемый `BaseFilial::getFilialTable()`.

---

## `Order`

Source: `protected/models/Order.php`. Extends `BaseFilial`. `filialTable()`
returns `{{order}}`, resolves to `d0_fN_order`. Primary key `ORDER_ID`
(varchar UUID-like). Live DB: 59 columns.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `ORDER_ID` | string | PK. UUID-like, также используется как cross-filial sync ID. |
| `DILER_ID` | string | Tenant subdivision (legacy "dealer"); см. модель `Diler`. |
| `CLIENT_ID` | string | FK на `Client.CLIENT_ID`. |
| `AGENT_ID` | string | FK на `Agent.AGENT_ID`. NULL для web / B2B-портал заказов. |
| `CLIENT_CAT` | string | Денормализованная категория клиента на момент submit. |
| `CITY_ID` | string | FK на `City`. |
| `PRICE_TYPE` | string | FK на `PriceType.PRICE_TYPE_ID`. Фиксирует прайс-лист на момент submit. |
| `OLD_PRICE_TYPE` | string | Pre-migration price-list ID; legacy. |
| `COUNT` | float | Сумма `OrderDetail.COUNT` (доставленные units). |
| `SUMMA` | float | Total после скидки, в `CURRENCY`. |
| `DISCOUNT` | float | Сумма `OrderDetail.DISCOUNT` по заказу. |
| `DATE` | datetime | Submitted-at. Ставится на первом save, никогда не перезаписывается. |
| `STATUS` | int (TINYINT) | Макро-состояние: 1 Новый, 2 Отгружен, 3 Доставлен, 4 Возврат, 5 Отменён, 6 Редактируется, 7 New (second-sale вариант). |
| `SUB_STATUS` | int | Тонкий UI-шаг внутри `STATUS`. |
| `DOB_STATUS` | string | Под-статус сборки на складе: NULL не начат, `picking`, `picked`. Независим от `STATUS`. |
| `DATE_LOAD` | datetime | Когда заказ был загружен в trip. |
| `DATE_DELIVERED` | datetime | Когда экспедитор подтвердил доставку. |
| `DATE_CANCEL` | datetime | Когда `STATUS=5`. |
| `DATE_STATUS` | datetime | Последний переход статуса; используется для отслеживания SLA. |
| `DEBT` | float | Outstanding receivable; зеркалится из net `ClientTransaction`. |
| `REPLACE_ID` | string | Если непустой, этот заказ заменяет другой заказ. |
| `DEFECT_ID` | string | Если непустой, defect-return родитель этого заказа. |
| `BONUS_ORDER_ID` | string | FK на `BonusOrder` (auto-generated promo line). |
| `BONUS_TYPE` | string | `-1` авто-бонус, `-2` пропуск бонуса, `d0_*` ручной BONUS_ID. |
| `TIMESTAMP_X` | datetime | Последняя DB-side запись; trigger-managed. |
| `COMMENT` | string | Free-text агента. |
| `ID` | int | Surrogate auto-increment только для упорядочивания sync. НЕ PK. |
| `TRADE_ID` | int | FK на `TradeDirection`. |
| `ACTIVE` | char(1) | `Y` active, `N` soft-deleted. Hard delete — редкость. |
| `SYNC` | string | Sync ledger flag для мобильных клиентов. |
| `TIME` | int | Часы мобильного клиента на submit (epoch). |
| `VOLUME` | float | Кубометры (для планирования trip). |
| `SKIDKA` | int | Snapshot режима скидки на submit. |
| `CURRENCY` | string | FK на `Currency.CURRENCY_ID`. |
| `CURRENCY_SYMBOL` | string | Денормализованный display symbol. |
| `UNIT` | string | FK на `Unit.UNIT_ID` (base UOM). |
| `UNIT_SYMBOL` | string | Денормализованный UOM symbol. |
| `EXPEDITOR` | string | Назначенный `Expeditor.EXPEDITOR_ID`. NULL до назначения trip. |
| `TYPE` | string | 1 Order, 2 Shelf-return, 3 Exchange. |
| `CONTRACT_ID` | string | FK на `ContractClient.ID` если контракт активен. |
| `COMMENT_2` | string | Внутренний комментарий менеджера. |
| `CONSIGNMENT` | string | Consignment ref (legacy 1C интеграция). |
| `CONSIG_DATE` | datetime | Дата консигнации. |
| `XML_ID` | string | Внешний 1C / ERP ID. |
| `REAL_ID` | string | Локальный ID мобильного клиента до reconciliation сервером. |
| `STORE_ID` | string | Source warehouse `Store.STORE_ID`. |
| `DEFECT` | string | Defect-flag column (legacy). |
| `CREATE_BY` / `CREATE_AT` | string / datetime | Audit. |
| `UPDATE_BY` / `UPDATE_AT` | string / datetime | Audit. |
| `SOURCE` | string | mobile / web / online / import. |
| `STOCKMAN_ID` | string | Picker `User.USER_ID`. |
| `CISES_STATUS` | int | Состояние markirovka (Honest Sign) для CIS кодов заказа. |

### Индексы

`d0_order` — самая нагруженная по чтению таблица в sd-main. Live-схема
объявляет non-unique индексы по `CLIENT_ID`, `AGENT_ID`, `DATE`,
`STATUS`, `STORE_ID`, `EXPEDITOR`, `XML_ID`, плюс PK на `ORDER_ID`.

### Связи

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
| `Contragent` | BELONGS_TO | conditional, только когда `ServerSettings::isContragent()` |

### Read / write surface

Запись: `OrderController::actionSave`, мобильный API v1 / v2 / v3
(submit агента, confirm экспедитора), модуль сборки на складе,
defect-return flow (`OrderDefectController`), bonus engine
(`BonusComponent::generate` производит auto-bonus child orders), 1C
import job. Чтение: каждый report dashboard, `OrdersReport`, engine
закрытия периода, планировщик `Trip`, KPI engine, агрегатор
`OutletFact`.

### Gotchas

- `ORDER_ID` генерируется client-side как GUID; мобильный submit с
  `REAL_ID`, чтобы сервер мог замапить после offline-write
  reconciliation.
- `STATUS=3` (Доставлен) НЕ оплачивает автоматически заказ.
  Финансовый ledger требует отдельной `ClientTransaction` (write
  `TRANS_TYPE = order`) — см. lifecycle оплаты заказа в
  `docs/concepts/order-lifecycle.md`.
- `BONUS_TYPE` перегружен: `-1` означает auto-bonus, сгенерированный
  engine, `-2` означает пропустить бонус, любое другое значение — это
  `BONUS_ID` выбранного ручного бонуса.
- `DOB_STATUS` ('picking', 'picked') **независим** от `STATUS`. Строка
  может быть `STATUS=1 New` и `DOB_STATUS=picked`, если склад собрал
  до того, как менеджер одобрил.
- Soft delete использует `ACTIVE='N'`; downstream отчёты должны
  фильтровать по `ACTIVE='Y'`.

---

## `OrderDetail`

Source: `protected/models/OrderDetail.php`. Extends `BaseFilial`.
`filialTable()` returns `{{order_detail}}`, resolves to
`d0_fN_order_detail`. Primary key `ORDER_DET_ID`. Live DB: 29 columns.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `ORDER_DET_ID` | string | PK (UUID-like). |
| `ORDER_ID` | string | FK на `Order.ORDER_ID`. |
| `DILER_ID` | string | Tenant subdivision. |
| `CLIENT_ID` | string | Денормализовано из родительского order. |
| `CLIENT_CAT` | string | Денормализовано из `Client.CLIENT_CAT`. |
| `CITY_ID` | string | Денормализовано из родителя. |
| `STORE_ID` | string | Source warehouse для этой строки. |
| `PRODUCT_CAT` | string | FK на `ProductCategory`. |
| `PRODUCT` | string | FK на `Product.PRODUCT_ID`. |
| `COUNT` | float | Заказанные units. |
| `PRICE` | float | Цена за единицу на submit в `CURRENCY`. |
| `SUMMA` | float | `COUNT * PRICE - DISCOUNT`. |
| `DISCOUNT` | float | Применённая line-level скидка. |
| `DISCOUNT_ID` | string | FK на правило `Skidka`, давшее скидку. |
| `SKIDKA_MANUAL_ID` | string | FK на `SkidkaManual` если применён manager-override discount. |
| `VOLUME` | float | Кубометры для строки. |
| `CURRENCY` | string | Валюта `PRICE`. |
| `CURRENCY_SYMBOL` | string | Денормализовано. |
| `UNIT` | string | UOM на уровне строки. |
| `UNIT_SYMBOL` | string | UOM display symbol. |
| `DEFECT` | float | Кол-во units, отклонённых при доставке (используется defect-return flow). |
| `COMMENT` | string | Free-text. |
| `ID` | int | Surrogate auto-increment. |
| `ACTIVE` | char(1) | Soft-delete flag. |
| `SYNC` | string | Sync ledger. |
| `TIMESTAMP_X` | datetime | Trigger-managed. |
| `CREATE_BY` / `UPDATE_BY` | string | Audit user. |

### Связи

| Name | Type | Target |
|------|------|--------|
| `Order` | BELONGS_TO | `Order` on `ORDER_ID` |
| `Product` | BELONGS_TO | `Product` on `PRODUCT` to `PRODUCT_ID` |
| `Unit` | HAS_ONE | `Unit` on `UNIT` to `UNIT_ID` |
| `Currency` | HAS_ONE | `Currency` on `CURRENCY` to `CURRENCY_ID` |

### Read / write surface

Запись: те же контроллеры, что и `Order` — каждое сохранение order
фан-аутится в batch insert / update по `OrderDetail`. Чтение:
sales-by-product отчёты, AKB-калькулятор, bonus engine (входной
набор), defect-return flow (матчит `DEFECT > 0` строки).

### Gotchas

- Колонка `DEFECT` находится на **строке**, не на order. Чтобы
  посчитать общий defect по order, суммируйте `OrderDetail.DEFECT * PRICE`.
- Audit trail для строки заказа в `OrderDetailHistory` (28 колонок) —
  любая non-cosmetic правка создаёт history-строку, ключ
  `ORDER_DET_ID`.
- `STORE_ID` на строке может отличаться от `STORE_ID` order, когда
  включена multi-store сборка (редко; контролируется server-setting).

---

## `OrderHistory`

Source: `protected/models/OrderHistory.php`. Extends `BaseFilial`.
`filialTable()` returns `{{order_history}}`, resolves to
`d0_fN_order_history`. Primary key `ID` (auto-increment). Live DB: 38 columns.

### Колонки

Зеркалит основную массу колонок `Order` (`ORDER_ID`, `DILER_ID`,
`CLIENT_ID`, `AGENT_ID`, `CLIENT_CAT`, `CITY_ID`, `PRICE_TYPE`,
`COUNT`, `SUMMA`, `DATE`, `STATUS`, `DATE_LOAD`, `DATE_DELIVERED`,
`DATE_CANCEL`, `DATE_STATUS`, `DEBT`, `TIMESTAMP_X`, `COMMENT`,
`ACTIVE`, `SYNC`, `TIME`, `VOLUME`, `CURRENCY`, `CURRENCY_SYMBOL`,
`UNIT`, `UNIT_SYMBOL`, `DISCOUNT`, `EXPEDITOR`, `TYPE`, `CONSIGNMENT`,
`CONSIG_DATE`, `DEFECT`, `XML_ID`, `CREATE_BY`, `UPDATE_BY`,
`CREATE_AT`, `UPDATE_AT`). Добавляет `ID` auto-increment PK и
связывает каждую строку обратно с живым `Order` через `ORDER_ID`.

### Read / write surface

Запись: `Order::afterSave()` снепшотит строку в `OrderHistory` на
каждом переходе. Чтение: order-history UI, audit-отчёты,
"кто-что-когда-изменил" вид, используемый support.

### Gotchas

- Это **append-only** лог. Правки или удаления вне DB-maintenance
  запрещены.
- `OrderDetailHistory` (sister-таблица) играет ту же роль для
  изменений строк.
- History-строка ключевана по autoincrement `ID`, не по `ORDER_ID`,
  поэтому у одного order могут быть десятки строк.

---

## `Client`

Source: `protected/models/Client.php`. Extends `BaseFilial`.
`filialTable()` returns `{{client}}`, resolves to `d0_fN_client`.
Primary key `CLIENT_ID`. Live DB: 58 columns.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `CLIENT_ID` | string | PK (UUID-like). |
| `DILER_ID` | string | Tenant subdivision. |
| `TEL` | string | Основной телефон (множественные телефоны в `ClientPhones`). |
| `FIRM_NAME` | string | Юридическое название. |
| `NAME` | string | Display name. |
| `ADRESS` | string | Free-text адрес (обратите внимание на legacy spelling). |
| `CLIENT_CAT` | string | FK на `ClientCategory.CLIENT_CAT_ID`. |
| `ORIENT` | string | Ориентир для навигации. |
| `REGION` | string | FK на `Region`. |
| `CITY` | string | FK на `City.CITY_ID`. |
| `CONTACT_PERSON` | string | Free-text. |
| `FORM_SOB` | string | Код формы собственности. |
| `BALANS` | float | Кэшированный running balance — пересчитывается ночью из `ClientTransaction`. |
| `PRICE_TYPE_ID` | string | FK на `PriceType`. Default price list. |
| `BONUS_ID` | string | FK на `Bonus`. Активная bonus-программа. |
| `DISCOUNT_ID` | string | FK на `Skidka`. Активное правило скидки. |
| `DATE_EXP` | datetime | Дата последней expedition / доставки — обновляется trip flow. |
| `LON`, `LAT` | float | Geo для геофенсинга во время визита агента. |
| `ALLOW_CONSIG` | int | 1 если разрешены consignment продажи. |
| `ALLOW_KREDIT` | int | 1 если разрешены кредитные продажи. |
| `XML_ID` | string | Внешний 1C / ERP ID. |
| `BAR_CODE` | string | Лояльность barcode. |
| `EXPEDITOR` | string | Default `Expeditor.EXPEDITOR_ID`. |
| `PHOTO` | string | URL фото торговой точки. |
| `ACCOUNT`, `BANK`, `MFO`, `OKED` | string | Банковские реквизиты для Faktura.uz invoices. |
| `CODE_NDS`, `NSP_CODE` | string | Налоговые регистрационные коды. |
| `PINF` | string | Личный идентификационный номер (Узбекистан). |
| `CONTRACT` | string | Contract reference code. |
| `CONTRACT_DATE` | datetime | Дата активации контракта. |
| `CHANNEL` | string | FK на `ClientChannel.ID`. |
| `CLASS` | string | FK на `ClientClass.ID`. |
| `NEED_TO_AUDIT` | string | `Y` триггерит audit на следующем визите. |
| `TYPE` | int | Код типа клиента (B2B / B2C / chain / etc.). |
| `SALES_CAT` | string | FK на `SalesCategory`. |
| `CODE_2` | string | Secondary code для некоторых 1C интеграций. |
| `CONTRAGENT` | string | FK на `Contragent.CLIENT_ID` когда включён contragent mode. |
| `TGIS_ID` | string | Внешний ключ налоговой системы. |
| `ACTIVE` | char(1) | Soft-delete flag. |
| `APPROVED` | int | 0 pending, 1 approved (workflow одобрения новой точки). |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Индексы

`d0_client` имеет 58 колонок. Live-индексы: `CITY`, `CLIENT_CAT`,
`XML_ID`, `EXPEDITOR`, `CHANNEL`, плюс PK на `CLIENT_ID`.

### Связи

Модель сама не объявляет `relations()`, но на неё ссылается каждая
финансовая и order-модель. Cross-table joins идут через `CLIENT_ID`.

### Read / write surface

Запись: `ClientController::actionSave`, мобильный API new-outlet flow,
`ClientPending` approval flow (когда `APPROVED=0` переходит в 1), 1C /
Faktura sync, KPI engine (обновляет `NEED_TO_AUDIT`). Чтение:
практически каждый отчёт.

### Gotchas

- `BALANS` — это **кэш**; правда в `ClientTransaction`. Запустите
  `ClientFinans::recompute`, если оно расходится.
- Колонка `ADRESS` — legacy spelling, и это реально имя колонки в БД.
  Не переименовывайте в `ADDRESS`.
- `APPROVED=0` клиенты могут быть созданы агентами в поле, но не
  появляются в invoicing отчётах, пока менеджер не одобрит.

---

## `ClientTransaction`

Source: `protected/models/ClientTransaction.php`. Extends `BaseFilial`.
`filialTable()` returns `{{client_transaction}}`, resolves to
`d0_fN_client_transaction`. Primary key `CLIENT_TRANS_ID`. Live DB: 40 columns.

Это **канонический финансовый ledger** sd-main. Каждый order, payment,
defect, ручная корректировка, transfer и денежный эффект бонуса
постит как минимум одну строку сюда.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `CLIENT_TRANS_ID` | string | PK (UUID-like). |
| `DILER_ID` | string | Tenant subdivision. |
| `CLIENT_ID` | string | FK на `Client`. |
| `SUMMA` | float | Signed amount в `CURRENCY`. Положительное увеличивает долг клиента нам (продажа); отрицательное уменьшает его (оплата). |
| `IDEN` | string | Identity tag для cross-row группировки. |
| `DATE` | datetime | Эффективная бизнес-дата (НЕ row creation). |
| `DATE_EXP` | datetime | Ожидаемая дата закрытия receivables. |
| `COMMENT` | string | Free-text. |
| `TIMESTAMP_X` | datetime | Trigger-managed последняя запись. |
| `TYPE` | string | High-level type: cash, card, transfer, defect, adjust, bonus. |
| `TRANS_TYPE` | string | Origin event: `order`, `payment`, `defect_return`, `bonus`, `manual`. |
| `STATUS` | string | Posting state — релевантно для confirm-on-delivery flow. |
| `CURRENCY` | string | FK на `Currency.CURRENCY_ID`. |
| `CURRENCY_SYMBOL` | string | Display symbol. |
| `CURRENCY_RATE` | float | Snapshot FX-курса на посте. |
| `CONVERTATION` | float | Сумма в базовой валюте после конвертации. |
| `COMISSION` | float | Bank/processor commission удержана. |
| `COMPUTATION` | float | Сумма для отчётов — производная от `SUMMA` + `CONVERTATION`. |
| `EXPEDITOR` | string | Экспедитор, собравший cash (если есть). |
| `AGENT_ID` | string | Агент, создавший строку (если есть). |
| `USER_ID` | string | Office user, создавший строку (если есть). |
| `HISTORY` | string | JSON blob с историей правок. |
| `CASHBOX` | string | FK на `Cashbox.ID`. |
| `OFD_ID` | string | Fiscal device cheque ID. |
| `DATE_CLOSE` | datetime | Closure date (механика period-close). |
| `STORE_ID` | string | Source warehouse / cashier. |
| `XML_ID` | string | External 1C ID. |
| `CONFIRM_ID` | string | Ставится, когда pending-строка подтверждена. |
| `CONFIRM_USER` | string | Подтверждающий user. |
| `ONLINE_PAYMENT_ID` | int | FK на `OnlinePayment`, когда post через Payme / Click / etc. |
| `ACTIVE` | char(1) | Soft-delete. |
| `SYNC` | string | Sync ledger. |
| `CREATE_BY` / `CREATE_AT` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Запись: order-save (одна строка типа `order`), payment flow
(`PaymentDeliver`, `Cashbox` UI, online-payment webhooks),
defect-return (`OrderDefectController`), ручная корректировка
бухгалтером (`FinansController::actionEdit`), bonus engine (когда
бонус материализуется как деньги), period-close (пишет `DATE_CLOSE`).
Чтение: каждый finans-отчёт, виджет баланса клиента, агрегаторы sd-cs
и sd-billing.

### Gotchas

- Соглашение о знаке `SUMMA`: **положительное = клиент должен нам,
  отрицательное = мы должны клиенту**. Отчёты, показывающие долг как
  положительное число, не должны negate перед display.
- Строка `STATUS='pending'` (confirm-on-delivery flow) НЕ считается в
  балансе клиента, пока экспедитор не подтвердит и строка не
  переключится в confirmed. Не агрегируйте сырые строки наивно.
- Lookup `Cashbox.KASSIR` — по user; `CASHBOX` на этой строке — по
  cashbox ID. Не путайте.
- `ClientTransactionHistory` (32 кол.) держит append-only историю
  правок строки.

---

## `Agent`

Source: `protected/models/Agent.php`. Extends `BaseFilial`.
`filialTable()` returns `{{agent}}`, resolves to `d0_fN_agent`. Primary
key `AGENT_ID`. Live DB: 29 columns.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `AGENT_ID` | string | PK. |
| `FIO` | string | Full name. |
| `TEL` | string | Телефон. |
| `PASSPORT_COPY` | string | URL скана паспорта. |
| `DATE_BIRTH` | datetime | Birthday. |
| `ADDRESS` | string | Free-text. |
| `PHOTO` | string | URL profile photo. |
| `DILER_ID` | int | Tenant subdivision. |
| `EMAIL` | string | Email. |
| `ACTIVE` | char(1) | `Y` / `N`. |
| `VAN_SELLING` | int | 1 если включён van-selling (mobile expeditor flow). |
| `AUDIT` | string | `Y` если агент делает аудиты. |
| `SYNC` | string | Sync ledger. |
| `XML_ID` | string | External ID. |
| `FILTER` | string | JSON filter scoping видимости outlets агента. |
| `APP_VERSION` | string | Последняя зарепортированная версия мобильного app. |
| `DEVICE_MODEL` | string | Последняя модель устройства. |
| `LAST_SYNC_TIME` | datetime | Последний успешный sync push от этого user. |
| `IP_ADDRESS` | string | Последний sync IP. |
| `CASHBOX` | string | FK на `Cashbox.ID` — default cashbox агента. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Связи

Модель объявляет HAS_ONE на `User` по `AGENT_ID = USER.AGENT_ID`,
чтобы API layer мог резолвить credentials и role.

### Read / write surface

Запись: admin UI `AgentController`, RBAC role-assignment, metadata
ping мобильного app на каждом sync. Чтение: visit-модуль, KPI engine,
sales-by-agent report, trip planner.

### Gotchas

- `Agent` — **бизнес-идентичность**. Логин (`User`) — отдельная
  строка, join по `AGENT_ID`. Отключение логина — это
  `User.ACTIVE='N'`, не `Agent.ACTIVE='N'`.
- `FILTER` — JSON; легальные значения задокументированы в
  `AgentFilter` helper.
- `LAST_SYNC_TIME` — то, что sd-cs central console читает, чтобы
  обнаружить "offline > 24h" агентов.

---

## `Supervayzer`

Source: `protected/models/Supervayzer.php`. Extends `BaseFilial`.
`filialTable()` returns `{{supervayzer}}`, resolves to
`d0_fN_supervayzer`. Primary key `SV_AGENT_ID`. Live DB: 11 columns.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `SV_AGENT_ID` | string | PK. |
| `USER_ID` | string | FK на `User.USER_ID` (логин). |
| `DILER_ID` | string | Tenant subdivision. |
| `AGENT_ID` | string | FK на `Agent.AGENT_ID` — подчинённый агент. |
| `POSITION_ID` | int | FK на position lookup. |
| `XML_ID` | string | External ID. |
| `ACTIVE`, `SYNC`, `TIME`, `TIMESTAMP_X`, `ID` | – | Стандартный audit / sync. |

### Read / write surface

Запись: admin UI `SupervayzerController`. Чтение: supervisor-scoped
report filters, KPI engine (supervisor наследует все KPI подчинённых
агентов).

### Gotchas

- Один супервайзер может вести многих агентов — много строк с одним
  `USER_ID` и разными `AGENT_ID`.
- Удаление supervisor-строки нигде не логируется — diff через
  `model_log`, если нужен audit trail.
- Роль supervisor НЕ видит данные других supervisor'ов, если не
  включён `ServerSettings::isCrossSupervayzer()`.

---

## `Expeditor`

Source: `protected/models/Expeditor.php`. Extends `BaseFilial`.
`filialTable()` returns `{{expeditor}}`, resolves to `d0_fN_expeditor`.
Primary key `EXPEDITOR_ID`. Live DB: 28 columns.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `EXPEDITOR_ID` | string | PK. |
| `FIO` | string | Full name. |
| `TEL` | string | Телефон. |
| `AUTONUM` | string | Номер машины. |
| `AUTOBRAND` | string | Марка машины. |
| `DILER_ID` | string | Tenant subdivision. |
| `PASSPORT_COPY` | string | URL скана. |
| `DATE_BIRTH` | datetime | Birthday. |
| `ADDRESS` | string | Free-text. |
| `PHOTO` | string | URL фото. |
| `CITY_ID` | string | FK на `City`. |
| `EMAIL` | string | Email. |
| `PINFL` | string | Tax / passport identifier. |
| `ADD_FILTER` | string | JSON дополнительный scoping filter. |
| `DEFECT_STORE` | string | FK на `Store.STORE_ID` — склад, куда экспедитор возвращает дефектный товар. |
| `XML_ID` | string | External ID. |
| `ACTIVE`, `SYNC`, `TIMESTAMP_X`, `TIME`, `ID` | – | Стандарт. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Запись: `ExpeditorController`, trip-assignment job, мобильный
expeditor app на sync. Чтение: trip planner (`Trip`), expeditor KPI
engine (`ExpeditorKpiJob`, `ExpeditorKpiSetup`), отчёты загрузки
экспедитора (`ExpeditorLoad`, `ExpeditorLoadDetail`).

### Gotchas

- Логин (`User.EXPEDITOR_ID`) может мапиться на `Expeditor`-строку, и
  `Cashbox` обычно прикрепляется на момент trip.
- `DEFECT_STORE` по умолчанию — designated карантин-склад; orders,
  помеченные как defect, возвращаются туда, пока менеджер не
  восстановит сток.

---

## `User`

Source: `protected/models/User.php`. Extends `BaseFilial`.
`filialTable()` returns `{{user}}`, resolves to `d0_fN_user`. Primary
key `USER_ID`. Live DB: 22 columns. Authentication / role-bearer row;
паруется с одним из `Agent`, `Expeditor`, `Supervayzer`, `Auditor`,
или ни с кем (back-office user).

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `USER_ID` | int | PK (autoincrement). |
| `NAME` | string | Display name. |
| `EMAIL` | string | Email. |
| `DILER_ID` | int | Tenant subdivision. |
| `AGENT_ID` | int | FK на `Agent.AGENT_ID` (когда role = agent). |
| `EXPEDITOR_ID` | string | FK на `Expeditor.EXPEDITOR_ID` (когда role = expeditor). |
| `ROLE` | int | Код роли (cross-references `authassignment`). |
| `LOGIN` | string | Логин. |
| `PASSWORD` | string | bcrypt hash. |
| `CODE` | string | Recovery code. |
| `XML_ID` | string | External ID. |
| `PAY` | int | Pay-period flag. |
| `TEL` | string | Телефон. |
| `ACTIVE` | char(1) | Soft-delete. Отключает login. |
| `DIVICE_ID` | string | Последний device identifier (обратите внимание на legacy spelling). |
| `SYNC` | string | Sync ledger. |

### Read / write surface

Запись: `UserController`, мобильный registration flow, password reset.
Чтение: каждый authenticated controller
(`Yii::app()->user->getUser()`), RBAC checker, license counter.

### Gotchas

- Реальный permission grant живёт в `authassignment` и `authitem`, не
  в `User`. `ROLE` — denormalised hint.
- Legacy имя колонки — `DIVICE_ID` (опечатка) — сохраняйте при
  написании миграций.
- `ACTIVE='N'` сразу же блокирует login на следующем запросе, включая
  открытую mobile sync session.

---

## `Product`

Source: `protected/models/Product.php`. Extends `CActiveRecord`
напрямую — **filial-shared** master row. `tableName()` returns
`d0_product`. Primary key `PRODUCT_ID`. Live DB: 50+ columns.

### Колонки (избранные)

| Column | Type | Назначение |
|--------|------|------------|
| `PRODUCT_ID` | string | PK. |
| `TRADE_ID` | int | FK на `TradeDirection`. |
| `PRODUCT_CAT_ID` | string | FK на `ProductCategory`. |
| `NAME` | string | Display name. |
| `SORT` | int | Display order. |
| `VOLUME` | float | Кубометры за единицу. |
| `PACK_QUANTITY` | float | Units per pack. |
| `SAP_CODE` | string | ERP code. |
| `BAR_CODE` | string | EAN / UPC. |
| `IKPU` | string | Узбекский налоговый код классификации. |
| `IKPU_PACK_CODE`, `IKPU_UNIT_CODE` | string | Variant IKPU codes. |
| `GTIN` | string | Global trade item number. |
| `ETTN_CODE` | string | ETTN / e-waybill code. |
| `VAT_RATE` | float | Output VAT %. |
| `EXCISE_RATE`, `EXCISE_RATE_TYPE` | float / int | Акциз. |
| `TARA_ID` | string | FK на `Tara` (тара depozit). |
| `WEIGHT` | float | Вес за единицу. |
| `BLOCKS_IN_BOX` | int | Pack hierarchy info. |
| `SHELF_LIFE` | int | Дни. |
| `PHOTO` | string | URL картинки. |
| `UNIT_ID` | string | FK на `Unit`. |
| `PACK` | int | Pack-mode flag. |
| `SEGMENT`, `BRAND`, `PRODUCER` | int | Catalog dimensions. |
| `PROPERTY`, `PROPERTY1`, `PROPERTY2` | int | Free-form classification. |
| `BY_BLOCK` | string | 1 если продажи должны быть в блоках. |
| `CASE_TYPE_ID` | int | Case-pack type. |
| `IS_MML` | string | 1 если часть "must-have" обязательного списка. |
| `IS_OUR`, `IS_LOCAL` | string | Ownership / locality flags. |
| `CS_PRODUCT`, `CS_ID`, `CS_CAT_ID` | string / int | Cross-system catalog binding. |
| `XML_ID` | string | Внешний ERP ID. |
| `DESCRIPTION` | string | Free-text. |
| `ACTIVE`, `SYNC`, `TIME`, `TIMESTAMP_X` | – | Стандарт. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Запись: `ProductController`, 1C import, Faktura.uz sync (IKPU).
Чтение: каждый catalog screen, каждая строка order, каждый аудит
(`AdtAudit`, `AudProduct`), каждый stock query.

### Gotchas

- `Product` — filial-shared. Чтобы ограничить продукт filial'ом,
  используйте `ProductFilial` (= `d0_filial_product`).
- IKPU-коды и акциз обязательны для invoiceable продуктов по
  налоговому законодательству Узбекистана; отсутствие IKPU блокирует
  ESF submission.
- `BLOCKS_IN_BOX`, `PACK_QUANTITY`, `BY_BLOCK` взаимодействуют:
  правила в `docs/concepts/tara.md`.

---

## `ProductPriceMarkup`

Source: `protected/models/ProductPriceMarkup.php`. Extends
`CActiveRecord`. `tableName()` returns `d0_product_subcategory` (имя
таблицы — misnomer; модель работает с правилами per-product markup).
Primary key `ID`. Filial-shared.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `ID` | int | PK. |
| `PRODUCT` | string | FK на `Product.PRODUCT_ID`. |
| `PRICE_TYPE` | string | Target price type. |
| `BASE_PRICE_TYPE` | string | Source price type. |
| `MARKUP` | float | Множитель (`1.20` = +20%). |
| `ROUND_METHOD` | int | 0 nearest, 1 up, 2 down. |
| `ROUND_ACCURACY` | float | Round step (100, 500, 1000 и т.д.). |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Запись: `PriceTypeController::actionMarkup`, price-recalc cron.
Чтение: order submit (вычисляет `OrderDetail.PRICE`, если активно
правило markup), экспорт price-list.

### Gotchas

- Голая `Product`-строка НЕ хранит цены. Цены приходят либо из
  markup-правила + base price-type, либо загружаются напрямую в
  `OldPrice` / похожие таблицы.
- Default значения `ROUND_ACCURACY` tenant-зависимы — никогда не
  предполагайте 1000.

---

## `PriceType`

Source: `protected/models/PriceType.php`. Extends `CActiveRecord` —
filial-shared. `tableName()` returns `d0_price_type`. Primary key
`PRICE_TYPE_ID`.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `PRICE_TYPE_ID` | string | PK. |
| `NAME` | string | Display name. |
| `CURRENCY` | string | FK на `Currency`. |
| `PARENT` | string | Опциональный родитель PriceType (markup chains). |
| `TYPE` | string | Sales / purchase / contract. |
| `FOR_CLIENT` | int | 1 если виден клиентам. |
| `OLD_PRICE_TYPE` | string | Legacy ID. |
| `FILIAL` | int | Опциональное filial scoping. |
| `DILER` | string | Tenant subdivision. |
| `DESCRIPTION` | string | Free-text. |
| `SORT` | int | Display order. |
| `VALYUTA_ID` | int | FK на `Valyuta` (currency alt). |
| `DEALER_PRICE` | int | 1 если это dealer-tier price. |
| `HAND_EDIT` | string | Y если перебито вручную. |
| `XML_ID` | string | External ID. |
| `ACTIVE`, `SYNC`, `TIMESTAMP_X`, `TIME` | – | Стандарт. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Запись: `PriceTypeController`, 1C import. Чтение: default клиента
(`Client.PRICE_TYPE_ID`), order submit, каждый отчёт, показывающий
цены.

### Gotchas

- Клиент может переопределить default на order-submit, выбрав другой
  price type — выбираемы в мобильном app только те, где
  `FOR_CLIENT=1`.
- `PARENT` включает chaining price-type; циклы не детектируются на
  insert и заблокируют markup engine.
- `PriceTypeFilial` — связующая модель, ограничивающая price type
  конкретными filial'ами.

---

## `Stock` (операционный сток — см. также `WarehouseDetail`)

Концепция `Stock` в sd-main — это не одна таблица. Есть три связанных
таблицы:

- `d0_fN_warehouse_detail` — per-warehouse per-product on-hand
  строка. Модель `WarehouseDetail`. **Это каноническая "stock"
  таблица.**
- `d0_fN_store_detail` — per-store per-product зеркало для
  van-selling flow (`Store` + `StoreDetail`).
- `d0_stock_exp` — on-hand загрузки грузовика экспедитора. Модель
  `StockExp`.

Поверхностный `Stock` reference в старой версии этого doc был заменён
тремя секциями ниже.

### `WarehouseDetail`

Source: `protected/models/WarehouseDetail.php`. Extends `BaseFilial`.
`filialTable()` returns `{{warehouse_detail}}`. PK `WAREHOUSE_DETAIL_ID`.
Live DB: 14 columns.

| Column | Type | Назначение |
|--------|------|------------|
| `WAREHOUSE_DETAIL_ID` | string | PK. |
| `WAREHOUSE_ID` | string | FK на `Warehouse`. |
| `STORE_ID` | string | FK на `Store` (когда warehouse обёрнут store'ом). |
| `PRODUCT_CAT_ID` | string | FK на `ProductCategory`. |
| `PRODUCT_ID` | string | FK на `Product`. |
| `TYPE` | string | Stock type / status. |
| `IDEN` | string | Identity tag для группировки. |
| `COUNT` | int | On-hand units. Может быть отрицательным, если `Store.NEGATIVE_COUNT='Y'`. |
| `DILER_ID` | string | Tenant subdivision. |
| `ACTIVE`, `SYNC`, `TIME`, `TIMESTAMP_X`, `ID` | – | Стандарт. |

### `StoreDetail`

Source: `protected/models/StoreDetail.php`. Extends `BaseFilial`.
`filialTable()` returns `{{store_detail}}`. PK `STORE_DETAIL_ID`.

`STORE_DETAIL_ID`, `STORE_ID`, `PRODUCT_CAT_ID`, `PRODUCT_ID`,
`COUNT`, `DILER_ID`, `TIMESTAMP_X`, `ACTIVE`, `SYNC`. Зеркало
`WarehouseDetail`, выровненное с моделью `Store`, используемой
van-selling flow.

### `StockExp`

Source: `protected/models/StockExp.php`. Extends `BaseFilial`.
`filialTable()` returns `{{stock_exp}}`. PK `ID`.

| Column | Type | Назначение |
|--------|------|------------|
| `ID` | string | PK. |
| `PRODUCT_ID` | string | FK. |
| `CLIENT_ID` | string | FK (consignment клиенту, используется VS / mobile sale). |
| `AGENT_ID` | string | FK. |
| `USER_ID` | string | FK. |
| `COUNT` | float | Units. |
| `DATE` | datetime | Event date. |
| `DATE_PRO`, `DATE_EXP` | datetime | Manufacture / expiry. |
| `COMMENT` | string | Free-text. |
| `ACTIVE`, `SYNC`, `TIMESTAMP_X`, `TIME` | – | Стандарт. |
| `CREATE_BY` / `CREATE_AT` / `UPDATE_BY` / `UPDATE_AT` | – | Audit. |

### Gotchas

- Две stock-таблицы (`WarehouseDetail` + `StoreDetail`) держатся
  синхронно триггерами / job'ом `StoreLog`. Расхождение требует
  ре-синка.
- Negative stock разрешён, когда `Store.NEGATIVE_COUNT='Y'`; многие
  отчёты тихо фильтруют negatives.
- Строки `StockExp` — инвентарь грузовика экспедитора во время
  активного trip. Реконсиляция через `ExpeditorLoad` на закрытии
  trip.

---

## `Warehouse`

Source: `protected/models/Warehouse.php`. Extends `BaseFilial`.
`filialTable()` returns `{{warehouse}}`, resolves to `d0_fN_warehouse`.
Primary key `WAREHOUSE_ID`. Live DB: 14 columns.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `WAREHOUSE_ID` | string | PK. |
| `DILER_ID` | string | Tenant subdivision. |
| `TYPE` | string | Storage type. |
| `TYPE_LIMIT` | string | Allowed product-type filter. |
| `NAME` | string | Display name. |
| `IDEN` | string | Identity tag. |
| `COUNT` | int | Snapshot. |
| `CONDITION` | string | Free-text (напр. cold-storage). |
| `COMMENT` | string | Free-text. |
| `ACTIVE`, `SYNC`, `TIME`, `TIMESTAMP_X`, `ID` | – | Стандарт. |

### Read / write surface

Запись: `WarehouseController`, 1C import. Чтение: stock-on-hand
queries, trip planner (выбор из цепочки `STORE_ID -> WAREHOUSE_ID`),
inventory module (`Inventory*`).

### Gotchas

- `Warehouse` ≠ `Store`. `Store` (model `Store`, table `d0_store`) —
  это **vending** unit (cash register / POS или van экспедитора).
  `Warehouse` — это **storage** unit, мапится через
  `WarehouseLocation`, когда они расходятся.
- `WarehouseDetail` носит реальный on-hand по продукту.

---

## `Visit`

Source: `protected/models/Visit.php`. Extends `BaseFilial`.
`filialTable()` returns `{{visit}}`. Primary key composite (`ID`,
`DATE`). Live DB: 28 columns.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `ID` | int | Часть PK (autoincrement). |
| `DATE` | datetime | Часть PK; время начала визита. |
| `AGENT_ID` | string | FK на `Agent`. |
| `USER_ID` | string | FK на `User`. |
| `CLIENT_ID` | string | FK на `Client`. |
| `VISITED` | char(1) | `Y` если был check-in. |
| `ORDER` | char(1) | `Y` если был размещён order. |
| `REJECT` | char(1) | `Y` если залогирована причина rejection / no-buy. |
| `PHOTO` | char(1) | `Y` если приложено фото. |
| `AUDIT` | char(1) | `Y` если был аудит. |
| `LON`, `LAT` | float | Координаты check-in. |
| `DISTANCE` | float | Метры от outlet, server-side computed на save. |
| `GPS_STATUS` | int | GPS quality: 0 disabled, 1 ok, 2 stale, 3 mock. |
| `CHECK_IN_TIME` | datetime | Mobile-side check-in момент. |
| `CHECK_OUT_TIME` | datetime | Check-out момент. |
| `PLANED` | char(1) | `Y` если визит был в плане. |
| `STORE_CHECK` | char(1) | `Y` если выполнен shelf check. |
| `PAYMENT`, `DELIVERY`, `POLL`, `ORDER_REPLACE`, `ORDER_DEFECT` | char(1) | Per-step completion flags. |
| `SYNC_TIME` | datetime | Когда sync завершён. |
| `DAY` | date | Усечённый `DATE` для быстрой группировки. |
| `POSITION_ID` | string | Role / position на момент визита. |
| `ROLE` | string | Role text. |

### Read / write surface

Запись: мобильный API check-in + check-out + step-completion
endpoints. Чтение: visit dashboard, KPI engine, audit module,
outlet-fact aggregator.

### Gotchas

- `GPS_STATUS=3` (mock GPS) флагует потенциальный fraud — многие
  отчёты фильтруют это, и визит не идёт в KPI.
- Composite PK означает, что два визита одному клиенту в одну `DATE`
  секунду коллизируют. Mobile retries должны использовать уникальные
  timestamps.
- `DISTANCE` server-computed из `Client.LON / LAT`; outlets без geo
  координат всегда репортят 0.

---

## `Gps`

Source: `protected/models/Gps.php`. Extends `BaseFilial`.
`filialTable()` returns `{{gps}}`. PK composite (`ID`, `DATE`). Live
DB: 20 columns.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `ID` | int | Часть PK (autoincrement). |
| `DATE` | datetime | Часть PK. |
| `AGENT_ID` | string | FK на `Agent`. |
| `USER_ID` | string | FK на `User`. |
| `TYPE` | string | Event type. |
| `ORDER_ID` | string | FK на `Order` если ping привязан к order. |
| `CLIENT_ID` | string | FK на `Client` если ping привязан к visit. |
| `LAT`, `LON` | float | Координаты. |
| `BATTERY` | int | Battery % на момент ping. |
| `PROVIDER` | string | `gps` / `network` / `fused`. |
| `SIGNAL` | int | Сила сигнала. |
| `MODE` | string | Mobile activity mode. |
| `INTERNET_STATUS` | int | Connectivity. |
| `GPS_STATUS` | int | Mock-detection. |
| `MOB_TIMESTAMP` | string | Часы клиента на момент ping. |
| `TIMESTAMP_X` | datetime | Серверный receipt. |
| `DAY` | date | Усечённая дата для индексации. |
| `DEVICE` | string | Device identifier. |

### Read / write surface

Запись: mobile sync (высокий volume — ping каждые несколько секунд во
время активных часов). Чтение: GPS-history view, fraud detection
(mock GPS), trip replay tool.

### Gotchas

- Это **самая высоконагруженная per-tenant таблица**. Планируйте
  partitioning перед scaling out — composite-PK `DATE` — правильная
  ось.
- Старые строки архивируются в отдельную холодную таблицу job'ом
  period-close; если читаете старше 90д, целитесь в архив.
- `MOB_TIMESTAMP` — источник правды времени, когда часы устройств
  дрейфуют; `TIMESTAMP_X` — серверное arrival.

---

## `Trip`

Source: `protected/models/Trip.php`. Extends `BaseFilial`.
`filialTable()` returns `{{trip}}`. Primary key `ID`. В live DB
sister-модель `TripOrder` для many-to-many trip-line.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `ID` | int | PK. |
| `CAR_ID` | int | FK на `Car`. |
| `COURIER_ID` | string | FK на `Expeditor.EXPEDITOR_ID` (роль courier). |
| `EXPEDITOR_ID` | string | FK на `Expeditor.EXPEDITOR_ID` (assigned expeditor). |
| `STORE_ID` | string | FK на `Store.STORE_ID` (origin). |
| `DATE` | datetime | Planned departure. |
| `STATUS` | int | 1 waiting, 2 active, 3 done, 4 cancelled. |
| `ACTIVE` | char(1) | Soft delete. |

### `TripOrder`

PK `ID`. Колонки `TRIP_ID`, `ORDER_ID`, `SORT`. Many-to-many между
trips и orders с явным порядком.

### Read / write surface

Запись: UI trip-planner, expeditor mobile app на departure / arrival.
Чтение: expeditor view, trip-progress dashboard.

### Gotchas

- `COURIER_ID` и `EXPEDITOR_ID` — отдельные роли — courier может
  водить, пока expeditor отвечает за сбор cash.
- Полный state machine — см. `docs/concepts/trip-lifecycle.md`.

---

## `Payment` (sd-main payment row)

В sd-main "payment" — это не одна таблица. Релевантные таблицы:

- `d0_fN_payment_deliver` — confirm-on-delivery payment, captured
  экспедитором. Модель `PaymentDeliver`.
- `d0_fN_payment_transfer` — multi-step transfer между cashboxes /
  filials. Модель `PaymentTransfer`.
- `d0_fN_payment_displacement` — internal displacement ledger.
  Модель `PaymentDisplacement`.

sd-billing `Payment` (в другой схеме) не связан; не путайте.

---

## `PaymentDeliver`

Source: `protected/models/PaymentDeliver.php`. Extends `BaseFilial`.
`filialTable()` returns `{{payment_deliver}}`. PK `ID`. Live DB: 23 columns.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `ID` | int | PK. |
| `CLIENT_ID` | string | FK на `Client`. |
| `ORDER_ID` | string | FK на `Order`. |
| `SUMMA` | float | Paid amount. |
| `CURRENCY` | string | FK на `Currency`. |
| `DATE` | datetime | Payment date. |
| `USER_ID` | string | Кассир user (если есть). |
| `AGENT_ID` | string | Собирающий агент (если есть). |
| `TRADE_ID` | string | FK на `TradeDirection`. |
| `TERM` | string | Payment terms / канал. |
| `CONFIRM` | string | Confirmation status. |
| `COMMENT` | string | Free-text. |
| `CREATE_BY` / `UPDATE_BY` / `CREATE_AT` / `UPDATE_AT` | – | Audit. |

### Read / write surface

Запись: expeditor mobile API при confirm доставки, cashier UI.
Чтение: order debt reconciliation, daily-cash report.

### Gotchas

- Строка `PaymentDeliver` — **триггер** для post связанной
  `ClientTransaction` типа `payment`, когда менеджер подтверждает. До
  этого она в pending state.
- `CONFIRM='Y'` — то, что переключает связанный
  `ClientTransaction.STATUS` в confirmed.

---

## `PaymentTransfer`

Source: `protected/models/PaymentTransfer.php`. Extends `BaseFilial`.
`filialTable()` returns `{{payment_transfer}}`. PK
`PAYMENT_TRANSFER_ID`. Live DB: 13 columns.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `PAYMENT_TRANSFER_ID` | string | PK. |
| `DOCUMENT_ID` | string | Source document ID (часто родительский transfer или order). |
| `OPERATION_ID` | int | 1 sending, 2 receiving. |
| `FILIAL_ID` | int | Filial, к которому относится строка. |
| `CURRENCY_ID` | string | FK на `Currency`. |
| `SUMMA` | float | Transfer amount. |
| `STATUS` | int | 1 new, 2 pending, 3 accepted, 4 rejected, 5 cancelled. |
| `COMMENT` | string | Free-text. |
| `CREATE_AT` / `CREATE_BY` / `UPDATE_AT` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Запись: UI cross-filial transfer, reconciliation cron. Чтение:
finans dashboard, transfer-status modal.

### Gotchas

- Каждый transfer обычно живёт как **две строки**: `OPERATION_ID=1`
  sending в source filial, `OPERATION_ID=2` receiving в destination
  filial. Обе должны достичь `STATUS=3`, чтобы transfer считался
  завершённым.
- `STATUS=4` (rejected) оставляет деньги в лимбе, пока не сделана
  ручная корректировка в `ClientTransaction`.

---

## `Cashbox`

Source: `protected/models/Cashbox.php`. Extends `BaseFilial`.
`filialTable()` returns `{{cashbox}}`. PK `ID`. Live DB: 15 columns.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `ID` | int | PK. |
| `NAME` | string | Display name. |
| `CURRENCY` | string | FK на `Currency`. |
| `KASSIR` | string | FK на `User.USER_ID` кассира. |
| `SORT` | int | Display order. |
| `XML_ID` | string | External ID. |
| `ACTIVE`, `SYNC`, `TIMESTAMP_X`, `TIME` | – | Стандарт. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Запись: `CashboxController`. Чтение: каждая `ClientTransaction` с
cash, daily cash close, агрегатор cashbox sd-billing.

### Gotchas

- `CashboxDisplacement` (`d0_cashbox_displacement`) записывает
  движение между cashboxes; closing balance — running sum.
- Строка `Cashbox` filial-scoped через `BaseFilial`. Не шарьте ID
  между filials.

---

## `AdtAuditResult`

Source: `protected/models/AdtAuditResult.php`. Extends `BaseFilial`.
`filialTable()` returns `{{adt_audit_result}}`. PK `ID`. Live DB: 12 columns.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `ID` | int | PK. |
| `VISIT_ID` | int | FK на `Visit.ID`. |
| `DATE` | datetime | Audit timestamp. |
| `CLIENT_ID` | string | FK на `Client`. |
| `POSITION_ID` | int | Role / position на момент аудита. |
| `AUDIT_ID` | int | FK на `AdtAudit.ID`. |
| `USER_ID` | string | FK на `User`. |
| `CREATE_AT` / `UPDATE_AT` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Запись: audit module через step аудита в мобильном app агента.
Чтение: audit dashboard, KPI engine, cross-references photo-report.

### Gotchas

- `AdtAuditResult` — **заголовок** аудита. Per-SKU строки в
  `AdtAuditResultData`.
- Это v2 audit engine ("ADT"). Старые таблицы `AuditStorchekCat` /
  `Auditor` — для v1 engine. Сосуществуют.

---

## `AdtAuditResultData`

Source: `protected/models/AdtAuditResultData.php`. Extends
`BaseFilial`. `filialTable()` returns `{{adt_audit_result_data}}`.
PK `ID`. Live DB: 12 columns.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `ID` | int | PK. |
| `RESULT_ID` | int | FK на `AdtAuditResult.ID`. |
| `PRODUCT_ID` | int | FK на `Product`. |
| `PRICE` | float | Observed shelf price. |
| `FACE` | int | Facing count. |
| `SOLD` | int | Reported sold-out count с прошлого визита. |
| `STORE` | int | Наблюдаемый shelf-stock. |
| `AVAILABLE` | bool | TRUE если SKU на полке. |
| `OUT_OF_STOCK` | bool | TRUE если полка пуста. |
| `CREATE_AT` / `UPDATE_AT` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Запись: то же, что и parent. Чтение: shelf-share report, OOS report,
KPI engine.

### Gotchas

- И `AVAILABLE`, и `OUT_OF_STOCK` существуют из-за edge cases — SKU
  может быть `AVAILABLE=false` (не листед), что отличается от
  `AVAILABLE=true && OUT_OF_STOCK=true` (листед, но пуст).
- Аудит может записать цену, даже если SKU OOS — `PRICE` это
  последняя видимая shelf price.

---

## `KpiTask`

Source: `protected/models/KpiTask.php`. Extends `BaseFilial`.
`filialTable()` returns `{{kpi_task}}`. PK `KPI_TASK_ID`. Live DB: 58 columns.

Строка KPI engine. Одна `KpiTask` row = один KPI, назначенный агенту
(или scope) на окно дат.

### Колонки (избранные)

| Column | Type | Назначение |
|--------|------|------------|
| `KPI_TASK_ID` | string | PK. |
| `KPI_ID` | string | FK на `Kpi` (KPI master). |
| `DILER_ID` | string | Tenant subdivision. |
| `NAME` | string | Display name. |
| `SORT` | int | Display order. |
| `TASK_TYPE` | string | Task code (sales-sum, AKB, OOS, etc.). |
| `VALUE` | float | Target / threshold value. |
| `DATE_TYPE` | string | Day / week / month / quarter. |
| `STATUS` | string | Active / paused. |
| `PRODUCT_ID`, `PRODUCT_CAT` | string | Опциональный product / category scoping. |
| `CLIENT_CAT`, `CLIENT_CLASS`, `CITY_ID`, `AGENT` | string | Опциональный dimensional scoping. |
| `CURRENCY` | string | FK на `Currency`. |
| `KPI_SHARE` | float | Вес этого KPI в total агента. |
| `BONUS_TYPE` | string | Bonus payout mode. |
| `BONUS` | float | Bonus amount при достижении порога. |
| `MARK`, `MARK2..MARK5` | int | Threshold marks. |
| `MARK2_KPI_SHARE`, `MARK2_BONUS_SHARE`, … `MARK5_*` | int | Share на каждом пороге. |
| `ACTIVE`, `SYNC`, `TIME`, `TIMESTAMP_X` | – | Стандарт. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Запись: KPI admin UI, job KPI templating. Чтение: KPI dashboard,
payroll, панель "tasks" мобильного dashboard агента.

### Gotchas

- `KpiTask` — **per-period** — одна строка на период на агента.
  Template (см. `KpiTaskTemplate`) — то, что клонируется для создания
  этих строк.
- Лестница `MARK2..MARK5` кодирует tiered bonus payout — более
  высокие marks разблокируют более крупные `MARK*_BONUS_SHARE`.
  Используйте ladder helper в `KpiCalculator` вместо пересчёта.

---

## `KpiTaskTemplate`

Source: `protected/models/KpiTaskTemplate.php`. Extends `BaseFilial`.
`filialTable()` returns `{{kpi_task_template}}`. PK `ID`. Live DB: 62 columns.

Зеркалит колонки `KpiTask`, но template-строка — это design-time
спецификация, а не period-realised task. Templates клонируются в
`KpiTask`-строки job'ом template-instantiation на старте каждого
периода. Дополнительные колонки по сравнению с `KpiTask` включают
`MIN_SUM`, `NEW_CLIENTS`, `REPLACEMENTS`, `SUPERVISER`,
`ACCESS_TO_OTHERS`, `ACCESS_TO_USE`, `MAX_BONUS` — design-time knobs.

### Read / write surface

Запись: KPI admin UI. Чтение: cron period-instantiation — продьюсит
`KpiTask`-строки для следующего периода.

### Gotchas

- Templates живут в `KpiTaskTemplateGroup` (небольшая grouping table);
  re-grouping template НЕ ре-инстанциирует уже активные
  `KpiTask`-строки.

---

## `KpiTaskTemplateGroup`

Source: `protected/models/KpiTaskTemplateGroup.php`. Extends
`CActiveRecord`. `tableName()` returns `d0_kpi_task_template_group`.
PK `ID`. Live DB: 10 columns.

Lightweight grouping таблица — name, description, sort order, audit.
Используется для организации KPI templates в admin UI.

---

## `Plan`

Source: `protected/models/Plan.php`. Extends `BaseFilial`.
`filialTable()` returns `{{plan}}`. PK `PLAN_ID`. Live DB: 12 columns.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `PLAN_ID` | int | PK. |
| `DILER_ID` | int | Tenant subdivision. |
| `PLAN` | string | Plan payload (часто JSON sub-планов). |
| `NAME` | string | Display name. |
| `MONTH`, `YEAR` | int | Период. |
| `PLAN_COMPLETED` | string | Кэшированный completion %. |
| `TIMESTAMP_X` | datetime | Стандарт. |
| `ACTIVE` | char(1) | Soft delete. |
| `SYNC` | string | Sync. |

### `PlanProduct`

Sister-таблица для per-product plan строк. PK `ID`. 13 колонок,
включая `PLAN_ID`, `PRODUCT_ID`, `COUNT`, `SUMMA`.

### Read / write surface

Запись: planning admin UI, plan-import job. Чтение: KPI engine,
sales-vs-plan dashboard, payroll calculator.

### Gotchas

- `Plan` filial-scoped через `BaseFilial`, поэтому cross-filial
  planning означает запись одной строки на filial.
- Кэш `PLAN_COMPLETED` пересчитывается ежечасно; не полагайтесь на
  него для live SLA.

---

## `Bonus`

Source: `protected/models/Bonus.php`. Extends `CActiveRecord` —
filial-shared. `tableName()` returns `d0_bonus`. PK `BONUS_ID`. Live
DB: 36 columns. Buy-X-get-Y promo engine row.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `BONUS_ID` | string | PK. |
| `DILER_ID` | string | Tenant subdivision. |
| `NAME` | string | Display name. |
| `BONUS_TYPE` | int | Type code (gift, discount, free SKU, etc.). |
| `PRODUCT` | string | Trigger product IDs (CSV / JSON). |
| `CURRENCY` | string | FK. |
| `CLIENT_TYPE`, `CLIENT_CHANNEL`, `CLIENT_CAT` | string | Client scoping. |
| `PRICE_TYPE` | string | FK на `PriceType`. |
| `BONUS_PRODUCTS` | string | Gift / bonus product IDs. |
| `BONUS` | string | Bonus payload (count / pct / amount). |
| `PARENT` | string | Parent bonus chain. |
| `VALUE` | string | Trigger threshold (count or sum). |
| `AGENT_ID` | string | Опциональный agent scoping. |
| `CITY` | string | Опциональный city scoping. |
| `MIN_COUNT`, `MAX_COUNT` | string | Trigger ranges. |
| `DATE`, `DATE_FROM`, `DATE_TO` | datetime | Active window. |
| `IS_PUBLIC` | string | Public-listing flag. |
| `ONLY_ONE_TIME` | int | 1 = single redemption per client. |
| `MAX_BONUS` | int | Cap на payout. |
| `MANUAL` | string | Manual / auto flag. |
| `ACTIVE`, `SYNC`, `TIME`, `ID` | – | Стандарт. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Запись: bonus admin UI. Чтение: order-submit engine — каждый order
прогоняет bonus-правила и может породить child `BonusOrder`-строку.

### Gotchas

- Trigger-поля (`PRODUCT`, `MIN_COUNT`, etc.) string-encoded —
  прочитайте parsing helper в `BonusComponent`, прежде чем
  предполагать CSV.
- Bonus может быть **автоматическим** (`MANUAL=N`, engine применяет
  его на qualifying orders) или **ручным** (агент выбирает bonus на
  submit).
- См. также `BonusOrder`, `BonusOrderDetail`, `BonusOrderHistory`,
  `BonusRelation`, `BonusAgent`, `BonusCity`, `BonusExclude`,
  `BonusFilial`, `BonusLimit` — bonus engine фан-аутится в множество
  satellite-таблиц.

---

## `BonusRelation`

Source: `protected/models/BonusRelation.php`. Extends `CActiveRecord`.
`tableName()` returns `d0_bonus_relation`. PK `ID`. Live DB: 7 columns.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `ID` | int | PK. |
| `PARENT_ID` | string | Родительский `BONUS_ID`. |
| `RELATED_BONUS_ID` | string | Related child `BONUS_ID`. |
| audit columns | – | Стандарт. |

### Gotchas

- Эта таблица кодирует **цепи** бонусов — покупка X qualifies для
  bonus B1, который в свою очередь qualifies для B2, если выполнены
  доп. условия. Циклы нельзя создавать на insert.

---

## `Skidka`

Source: `protected/models/Skidka.php`. Extends `CActiveRecord` —
filial-shared. `tableName()` returns `d0_skidka`. PK `SKIDKA_ID`. Live
DB: 37 columns. Discount-rule engine row. Sister-таблицы:
`SkidkaAgent`, `SkidkaBudget`, `SkidkaExclude`, `SkidkaFilial`,
`SkidkaManual`, `SkidkaOrder`, `SkidkaRelation`, `SkidkaStore`.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
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
| `BUDGET` | float | Hard cap across all redemptions. |
| `COMMENT` | string | Free-text. |
| `IS_PUBLIC` | string | Виден клиентам. |
| `ONLY_ONE_TIME` | int | 1 = single redemption. |
| `NUM_CATEGORIES` | int | Cross-category threshold support. |
| `ACTIVE`, `SYNC`, `TIME`, `ID`, `TIMESTAMP_X` | – | Стандарт. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Запись: discount admin UI. Чтение: order-submit engine — применяет
правило и постит `SkidkaOrder`-строку. Ручные перебивания идут через
`SkidkaManual`.

### Gotchas

- Строка `SkidkaManual` создаётся, когда менеджер применяет
  one-off скидку — у неё свой PK и budget.
- `BUDGET` — hard cap. Последующие qualifying orders не получат
  скидку, если budget исчерпан; проверяйте через running total
  `SkidkaBudget`.

---

## `Filial`

Source: `protected/models/Filial.php`. Extends `CActiveRecord` —
**не** `BaseFilial` (это корневая таблица, определяющая префиксы).
`tableName()` returns `d0_filial`. PK `id`. Live DB: 8 columns.

### Колонки

| Column | Type | Назначение |
|--------|------|------------|
| `id` | int | PK. |
| `domain` | string | Tenant domain assignment. |
| `is_main` | int | 1 если root filial. |
| `prefix` | string | Per-filial префикс таблицы (`f0`, `f1`, …). |
| `xml_id` | string | External ID. |

### Read / write surface

Запись: tenant onboarding flow (редко; обычно один раз на тенант).
Чтение: `FilialComponent` на каждом запросе, каждый потомок
`BaseFilial`.

### Gotchas

- Изменение `prefix` после того, как строки существуют, ломает
  каждый per-filial table lookup. Всегда создавайте новый filial;
  никогда не re-prefix.
- `is_main=1` должен появляться ровно один раз на тенант; root
  filial — где живут `Bonus`, `Skidka`, `Product`, `PriceType` и т.д.

---

## `ClientCategory`

Source: `protected/models/ClientCategory.php`. Extends
`CActiveRecord` — filial-shared. `tableName()` returns
`d0_client_category`. PK `CLIENT_CAT_ID`. Live DB: 15 columns.

### Колонки

`CLIENT_CAT_ID`, `NAME`, `DESCRIPTION`, `SORT`, `XML_ID`, `ACTIVE`,
`SYNC`, `CREATE_AT`, `UPDATE_AT`, `CREATE_BY`, `UPDATE_BY`,
`TIMESTAMP_X`, `ID`.

### Read / write surface

Запись: directory admin UI, 1C import. Чтение: фильтры по отчётам
(`Client.CLIENT_CAT`, `Order.CLIENT_CAT`, KPI scoping).

### Gotchas

- Удаление категории не каскадит — orphaned `CLIENT_CAT` references
  тихо возвращают пустые joins в отчётах.

---

## `ClientChannel`

Source: `protected/models/ClientChannel.php`. Extends `CActiveRecord`.
`tableName()` returns `d0_client_channel`. PK `ID`. Live DB: 8 columns.

### Колонки

`ID`, `NAME`, `XML_ID`, `CREATE_BY`, `UPDATE_BY`, `CREATE_AT`,
`UPDATE_AT`.

### Read / write surface

Запись: directory admin. Чтение: `Client.CHANNEL`, scoping на бонусах
(`Bonus.CLIENT_CHANNEL`) и скидках (`Skidka.CLIENT_CHANNEL`).

### Gotchas

- `ClientChannel` и `ClientClass` — разные dimensions; не путайте.

---

## `Contract` / `ContractClient`

Status: классы модели `Contract.php` и `ContractClient.php`
**deprecated** в кодовой базе (переименованы в `.obsolete`), но live
table `d0_contract` (16 колонок, InnoDB / utf8mb3, без Yii-модели)
всё ещё запрашивается отчётами и интеграцией Faktura / Didox. Данные
контрактов для нового кода живут вместо этого в семействе `Contragent`
(`d0_contragent`, `d0_contragent_history`, `d0_contragent_log`).

### `d0_contract` (legacy, без модели)

Cross-references `Order.CONTRACT_ID`. Читается напрямую через DAO для
обратной совместимости. Новые работы должны целиться в модель
`Contragent`.

### `d0_contragent` (current)

Модель `Contragent` (`protected/models/Contragent.php`). 39 колонок.
PK `CLIENT_ID`. Хранит юридически оформленного контрагента,
связанного с `Client` (когда включён `ServerSettings::isContragent()`).
Несёт банковские реквизиты, IKPU defaults, contract anchor data, и
это source-строка, которую Faktura.uz и Didox используют для построения
invoices.

### Gotchas

- Не extend'ите `Contract.php.obsolete`. Новые колонки идут на
  `Contragent`.
- У `Client` может быть 1:1 `Contragent` зеркало (когда включён
  contragent mode) или нет — order-код defensive о join через
  `ServerSettings::isContragent()`.

---

## Доменные группировки

30 таблиц, задокументированных выше, сгруппированы по доменам.
Используйте этот индекс, чтобы перепрыгнуть от домена к
соответствующей секции.

| Домен | Таблицы |
|-------|---------|
| Orders | `Order`, `OrderDetail`, `OrderHistory` |
| Catalog | `Product`, `PriceType`, `ProductPriceMarkup` |
| Stock | `WarehouseDetail`, `Warehouse`, `StockExp` (под секцией "Stock") |
| Clients | `Client`, `ClientCategory`, `ClientChannel`, `Contract` / `Contragent` |
| Finans | `ClientTransaction`, `PaymentDeliver`, `PaymentTransfer`, `Cashbox` |
| Team | `Agent`, `Supervayzer`, `Expeditor`, `User` |
| Visits & GPS | `Visit`, `Gps`, `Trip` (+ `TripOrder`) |
| Audit | `AdtAuditResult`, `AdtAuditResultData` |
| KPI | `KpiTask`, `KpiTaskTemplate`, `KpiTaskTemplateGroup`, `Plan` |
| Promo | `Bonus`, `BonusRelation`, `Skidka` |
| Tenant | `Filial` |

Для **полного индекса 306 моделей** с подсчётами колонок, PK и live-DB
cross-checks, см. `docs/data/schema-reference.md`. Для flows
высокого уровня (order → finans, visit → KPI) — см. диаграммы под
`docs/architecture/diagrams.md` и concept-доки под `docs/concepts/`.
