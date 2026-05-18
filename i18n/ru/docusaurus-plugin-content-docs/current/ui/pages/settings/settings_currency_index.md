---
title: "Валюты"
audience: Разработчики sd-main, QA
summary: Живая страница админки /settings/currency/index
topics: [settings, currency, page, ui]
---

# Валюты

**URL**: `/settings/currency/index` · **Модуль**: `settings` · **Контроллер**: `CurrencyController::index` · **RBAC**: `operation.settings.currency` · **Снятая роль**: `admin`

:::note Скриншот в процессе — нужен повторный запуск харвестера:::

## Назначение

CRUD-таблица валют и их дневных курсов. Используется финансом и заказами для конвертации между базовой валютой (обычно `UZS`) и котируемыми (`USD`, `RUB`). Курс автоматически подтягивается с фида ЦБ Узбекистана, если интеграция включена; ручные правки перекрывают фид.

## Колонки таблицы

| № | Колонка |
|---|---|
| 1 | ISO-код |
| 2 | Название |
| 3 | Символ |
| 4 | Курс к базовой |
| 5 | Дата действия |
| 6 | Источник (фид / руками) |
| 7 | Активна |

## Действия

- Добавить валюту
- Редактировать валюту
- Редактировать курс на дату (модал — `updateAjax`)
- Переключить активность
- Обновить из фида

## Бэкенд-маршрут

- **Файл контроллера**: `protected/modules/settings/controllers/CurrencyController.php` (строка 41)
- **Тип действия**: inline (`$this->render('admingrid_diler', …)`)
- **Рендерится вьюха**: `views/currency/admingrid_diler.php`
- **Требуется доступ**: `operation.settings.currency`
- **Соседние эндпоинты**: `getData`, `getUpdatedRow`, `updateAjax`

## См. также

- Справочник модуля: [/modules/settings](/docs/modules/settings)
- Мультивалютное округление: [/concepts/multi-currency-rounding](/docs/concepts/multi-currency-rounding)
