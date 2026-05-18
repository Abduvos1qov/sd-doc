---
title: "Города"
audience: Разработчики sd-main, QA
summary: Живая страница админки /settings/city/index
topics: [settings, geo, page, ui]
---

# Города

**URL**: `/settings/city/index` · **Модуль**: `settings` · **Контроллер**: `CityController::index` · **RBAC**: `operation.settings.city` · **Снятая роль**: `admin`

:::note Скриншот в процессе — нужен повторный запуск харвестера:::

## Назначение

Справочник городов. Используется как уровень адреса для клиентов, агентов и складов и как географический фильтр в KPI- и отчётах продаж. Каждый город привязан к `Region`. Есть Excel-импорт, чтобы новый тенант наполнялся из мастер-таблицы, а не вручную.

## Колонки таблицы

| № | Колонка |
|---|---|
| 1 | ID |
| 2 | Название |
| 3 | Регион |
| 4 | Почтовый индекс |
| 5 | Порядок |
| 6 | Активен |

## Действия

- Добавить город (модал — `createAjax`)
- Редактировать город (модал — `updateAjax`)
- Импорт из Excel (`importXls`)
- Переключить активность

## Бэкенд-маршрут

- **Файл контроллера**: `protected/modules/settings/controllers/CityController.php` (строка 46)
- **Тип действия**: inline (`$this->render('admingrid_diler', …)`)
- **Рендерится вьюха**: `views/city/admingrid_diler.php`
- **Требуется доступ**: `operation.settings.city`
- **Соседние эндпоинты**: `getData`, `getUpdatedRow`, `createAjax`, `updateAjax`, `importXls`

## См. также

- Справочник модуля: [/modules/settings](/docs/modules/settings)
- Регионы: [`/settings/region/index`](./settings_region_index)
