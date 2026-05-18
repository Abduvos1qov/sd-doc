---
title: "Регионы"
audience: Разработчики sd-main, QA
summary: Живая страница админки /settings/region/index
topics: [settings, geo, page, ui]
---

# Регионы

**URL**: `/settings/region/index` · **Модуль**: `settings` · **Контроллер**: `RegionController::index` · **RBAC**: `operation.settings.region` · **Снятая роль**: `admin`

:::note Скриншот в процессе — нужен повторный запуск харвестера:::

## Назначение

Справочник регионов — более крупный географический уровень над `City`. Задаёт территориальную размерность в KPI / отчётах продаж и обычно совпадает со скоупом супервайзера. У большинства тенантов сюда зашиты 14 узбекских вилоятов плюс Ташкент.

## Колонки таблицы

| № | Колонка |
|---|---|
| 1 | ID |
| 2 | Название |
| 3 | Код |
| 4 | Порядок |
| 5 | Активен |

## Действия

- Добавить регион
- Редактировать регион (`updateAjax`)
- Массовое удаление (`ajaxMassDelete`)
- Переключить активность

## Бэкенд-маршрут

- **Файл контроллера**: `protected/modules/settings/controllers/RegionController.php` (строка 38)
- **Тип действия**: inline (`$this->render('admin', …)` шелл + `_ajaxmassdelete`)
- **Рендерится вьюха**: `views/region/admin.php`
- **Требуется доступ**: `operation.settings.region`
- **Соседние эндпоинты**: `updateAjax`, `ajaxMassDelete`

## См. также

- Справочник модуля: [/modules/settings](/docs/modules/settings)
- Города: [`/settings/city/index`](./settings_city_index)
