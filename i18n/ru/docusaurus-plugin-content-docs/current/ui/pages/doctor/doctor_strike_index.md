---
title: "Strike rate plan"
audience: All sd-main developers, QA
summary: Admin page at /doctor/strike — set strike-rate targets (orders / visits) per agent
topics: [doctor, strike-rate, page, ui]
---

# Strike rate plan

**URL**: `/doctor/strike` · **Module**: `doctor` · **Controller**: `StrikeController::index` · **RBAC**: `operation.doctor.strikePlan` · **Role harvested**: `admin`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Defines strike-rate targets — what fraction of visits should convert to an order. Same flow shape as АКБ / SKU: filter, set plan per agent, push to mobile.

## Fields

| Label | Name | Type | Required |
|---|---|---|---|
| Период | filter | select | yes |
| Регион | filter | select | no |
| Супервайзер | filter | select | no |
| Категория продуктов | filter | select | no |
| План Strike Rate | `PLAN` | numeric (percent) | yes |

## Grid columns

| # | Column |
|---|---|
| 1 | Агент |
| 2 | Территория |
| 3 | Визиты |
| 4 | Заявки |
| 5 | Strike Rate (факт) |
| 6 | План |
| 7 | Расхождение |
| 8 | Действия |

## Actions

- Применить фильтр
- Просмотр (`actionView`)
- Поделиться с агентами (`actionShareToAgents`)
- Сохранить
- Сбросить

## Backend route

- **Controller file**: `protected/modules/doctor/controllers/StrikeController.php`
- **Actions**: `actionIndex` (line 49), `actionView` (line 142), `actionReturnAjax`, `actionReturnAjaxPageLoad`, `actionReturnAjaxView`
- **Required permission**: `H::access('operation.doctor.strikePlan')`

## See also

- Module reference: [/modules/doctor](/docs/modules/doctor)
- Pages index: [/ui/pages/doctor](./index.md)
