---
title: "Главная настроек"
audience: Разработчики sd-main, QA
summary: Живая страница админки /settings/settings/index
topics: [settings, page, ui]
---

# Главная настроек

**URL**: `/settings/settings/index` · **Модуль**: `settings` · **Контроллер**: `SettingsController::index` · **RBAC**: `operation.settings.access` · **Снятая роль**: `admin`

:::note Скриншот в процессе — нужен повторный запуск харвестера:::

## Назначение

Главная панель конфигурации sd-main. Каждая рантайм-настройка тенанта (правила прайс-листов, флаги потока заказов, поведение баланса и финанса, GPS-пороги, аудит-параметры, переключатели интеграций) сгруппирована тут в табы. Сохранения POST'ятся через `SettingsController::saveSettings`; кэш сбрасывается через `actionTruncateCache`.

## Расположение

- Сверху: переключатель табов — General · Orders · Prices · Stock · Finans · GPS · Audit · Integrations · UI · Telegram.
- Каждая вкладка: форма с группами полей (число, селект, булево, многострочный текст).
- Низ: «Сохранить», «Сбросить раздел», «Очистить кэш».

## Действия

- Сохранить настройки (пишет в `sd_params` / per-tenant таблицу)
- Очистить кэш (`/settings/settings/truncateCache`)
- Очистить настройки datatable (`/settings/settings/deleteDatatableSettings`)
- Сохранить шапку заявок (`/settings/settings/saveHeaderOrders`)
- Очистить одну запись table-control (`/settings/settings/truncateTableControl`)

## Бэкенд-маршрут

- **Файл контроллера**: `protected/modules/settings/controllers/SettingsController.php` (строка 38)
- **Тип действия**: inline
- **Рендерится вьюха**: `views/settings/index.php`
- **Требуется доступ**: `operation.settings.access`
- **Соседние write-эндпоинты**: `saveSettings`, `saveHeaderOrders`, `truncateCache`, `truncateTableControl`, `deleteDatatableSettings`

## См. также

- Справочник модуля: [/modules/settings](/docs/modules/settings)
- Каталог настроек: [/quality/settings-catalog](/docs/quality/settings-catalog)
- Редактор параметров: [`/settings/params/index`](./settings_params_index)
