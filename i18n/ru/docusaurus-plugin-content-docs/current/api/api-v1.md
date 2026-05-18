---
sidebar_position: 3
title: API v1 (устаревший)
---

# API v1 — модуль `api`

Устаревший API для партнёрских интеграций и одноразовых коннекторов.
Только поддержка — **не добавляйте сюда новые эндпоинты**, используйте
вместо этого v4.

## Поверхность

```
protected/modules/api/controllers/
```

Активные контроллеры (не `*.obsolete`):

- `Json1CController` — JSON-синхронизация с 1C
- `BillingController` — биллинговые вебхуки
- `LicenseController` — проверки лицензии
- `NotificationController` — регистрация push
- `OperatorController` / `Operator2Controller` — вспомогательные методы для оператора
- `OrderController` — создание партнёрских заказов
- `PushController` — диспатчер FCM/APNS
- `R2Controller` — чтение второго поколения
- `SdController`, `SalesdocController`, `Mef1cController`,
  `IdokonController`, `IkromController`, `NavruzController`,
  `ZarqandController`, `NeonController`, `OnlineOrderController`,
  `OnlineOrder3Controller`, `PradataController`, `SmartUpController`,
  `StockController`, `TelegramBotController`, `V2Controller`,
  `V4Controller`, `CronVisitController`, `ScheduledSmsController`,
  `AnalyticsController`, `ApiLogController`, `CislinkController`,
  `CleannerController`, `ConstructionController`, `DemoCronController`,
  `DisabledChatsController`, `Json1CController`.

(Современные поверхности см. на страницах API v3 / v4.)

## Аутентификация

В основном **общий секрет** в URL или теле POST, разный по каждому
эндпоинту. Некоторые используют HTTP basic. Глобальной схемы токенов нет.

## Формат

JSON. Несколько эндпоинтов принимают XML (`xml1c`, `pradata`).

## Рекомендуемая миграция

Если интегрируетесь сегодня — предпочитайте
[API v4](./api-v4-online/). Если добавляете функцию для существующего
потребителя v1, свяжитесь с командой платформы — многие эндпоинты v1
запланированы на вывод из эксплуатации.
