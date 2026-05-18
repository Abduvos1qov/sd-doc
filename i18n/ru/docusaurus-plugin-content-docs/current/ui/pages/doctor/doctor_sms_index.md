---
title: "SMS broadcast"
audience: All sd-main developers, QA
summary: Admin page at /doctor/sms — compose and send SMS to client/agent groups
topics: [doctor, sms, page, ui]
---

# SMS broadcast

**URL**: `/doctor/sms` · **Module**: `doctor` · **Controller**: `SmsController::index` · **RBAC**: module-level (SMS permission gate) · **Role harvested**: `admin`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Compose and dispatch SMS campaigns to client / agent recipient groups. Includes balance / package purchase (`actionBuy`, `actionBoughtPackages`), template save (`actionSaveTemplate`), do-not-call-list housekeeping (`actionClearDontPhone`), scheduled send (`actionSendSmsLater`), and an archive view (`actionArchive`).

## Fields (compose form)

| Label | Name | Type | Required |
|---|---|---|---|
| Получатели | recipient selector | multi-select | yes |
| Сообщение | `MESSAGE` | textarea | yes |
| Шаблон | template picker | select | no |
| Отправить позже | `SEND_AT` | datetime | no |

The page also renders the `_form.php` partial for the template editor.

## Grid columns (campaign / send log)

| # | Column |
|---|---|
| 1 | Дата отправки |
| 2 | Получатель |
| 3 | Текст |
| 4 | Статус |
| 5 | Стоимость |

## Actions

- Отправить (`actionSendSms`)
- Отправить позже (`actionSendSmsLater`)
- Купить пакет (`actionBuy`) / Купленные пакеты (`actionBoughtPackages`)
- Сохранить шаблон (`actionSaveTemplate`)
- Очистить чёрный список (`actionClearDontPhone`)
- Архив (`actionArchive` → `archive.php`)
- Удалить выбранные (`actionDeleteSelected`)

## Backend route

- **Controller file**: `protected/modules/doctor/controllers/SmsController.php`
- **Actions**: `actionIndex` (line 62), `actionSendingSms`, `actionSendSms`, `actionSendSmsLater`, `actionBuy`, `actionBoughtPackages`, `actionSaveTemplate`, `actionClearDontPhone`, `actionDeleteSelected`, `actionArchive`, `actionReturnAjaxForm`, `actionUpdateAjax`, `actionDeleteAjax`
- **Required permission**: module-level (some actions reference `operation.doctor.volumePlan`-style gates inline; check controller comments for current matrix)

## See also

- Module reference: [/modules/doctor](/docs/modules/doctor)
- SMS settings (server-toggles): [/settings/server-toggles](/docs/settings/server-toggles)
- Pages index: [/ui/pages/doctor](./index.md)
