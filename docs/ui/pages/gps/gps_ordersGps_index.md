---
title: "Заказы GPS (orders audit)"
audience: All sd-main developers, QA
summary: Admin page at /gps/ordersGps — orders cross-referenced with GPS positions
topics: [gps, orders, page, ui, audit]
---

# Заказы GPS (orders audit)

**URL**: `/gps/ordersGps` · **Module**: `gps` · **Controller**: `OrdersGpsController::index` · **RBAC**: module-level · **Role harvested**: `admin`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Cross-reference of every order against the agent's GPS position when the order was created. Used by audit / supervisors to detect orders placed far from the actual outlet location.

## Fields (filter bar)

| Label | Name | Type | Required |
|---|---|---|---|
| Период (от / до) | filter | date range | yes |
| Агент | filter | select | no |
| Регион | filter | select | no |

## Grid columns

| # | Column |
|---|---|
| 1 | ИД |
| 2 | Заказ ИД |
| 3 | Клиент |
| 4 | Агент |
| 5 | Координаты заказа |
| 6 | Координаты клиента |
| 7 | Дистанция |
| 8 | Есть / Нет (label success/danger) |

## Actions

- Фильтр
- Click row — open the underlying order in `/orders/list`

## Backend route

- **Controller file**: `protected/modules/gps/controllers/OrdersGpsController.php`
- **Action**: `actionIndex` (line 5) — renders `index` view with filter context
- **Required permission**: module-level

## See also

- Module reference: [/modules/gps](/docs/modules/gps)
- Orders module: [/modules/orders](/docs/modules/orders)
