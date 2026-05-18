---
title: "Pay — страницы интерфейса"
sidebar_position: 1
---

# Pay — страницы интерфейса

Модуль **Pay** работает только как приёмник webhook'ов; **у него нет пользовательских административных страниц**.

Он публикует три точки обратного вызова, которые узбекские платёжные провайдеры используют для расчётов по онлайн-заказам, созданным через бот или витрину:

| Маршрут | Контроллер | Назначение |
|---|---|---|
| `/pay/payme/index` | `PaymeController::index` | Приём merchant API Payme (Paycom) — CheckPerformTransaction / CreateTransaction / PerformTransaction / CancelTransaction / CheckTransaction / GetStatement |
| `/pay/click/index` | `ClickController::index` | Click prepare / complete callback с проверкой подписи |
| `/pay/apelsin/index` | `ApelsinController::index` | Apelsin notify callback |

Каждое действие читает сырое тело POST-запроса, сохраняет его в отдельный лог-файл через `Distr::saveFile`, передаёт обработку соответствующему helper-классу (`PaymeHelper`, `ClickTransaction`, `ApelsinHelper`), обновляет связанный `OnlineOrder` (поле `PAY`, вызов `createTransaction()`) и возвращает JSON, ожидаемый провайдером.

GET-страниц с HTML, форм и таблиц здесь нет. Конфигурация (merchant ID, секретные ключи, учётные данные) хранится в глобальной таблице параметров — см. [справочник модуля Settings](/docs/modules/settings) и страницу [Params](../settings/settings_params_index).

## См. также

- Справочник модуля: [/modules/pay](/docs/modules/pay)
- Поток онлайн-заказа: [модель `OnlineOrder`](/docs/schema/online-order)
- Реестр маршрутов: [`static/data/routes.json`](/data/routes.json)
