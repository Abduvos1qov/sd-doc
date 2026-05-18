---
title: "Единицы измерения"
audience: Разработчики sd-main, QA
summary: Живая страница админки /settings/unit/index
topics: [settings, product, page, ui]
---

# Единицы измерения

**URL**: `/settings/unit/index` · **Модуль**: `settings` · **Контроллер**: `UnitController::index` · **RBAC**: `operation.settings.unit` · **Снятая роль**: `admin`

:::note Скриншот в процессе — нужен повторный запуск харвестера:::

## Назначение

Справочник единиц измерения. У каждого товара есть базовая единица (штука, кг, литр) и может быть продаваемый паком размер (10 штук = 1 коробка). Единицы используются стоком, финансом и отчётами для отображения количеств. Коэффициенты пересчёта между единицами хранятся на самой строке `Product`, а не здесь — этот экран только каталогизирует названия и короткие лейблы.

## Колонки таблицы

| № | Колонка |
|---|---|
| 1 | ID |
| 2 | Название |
| 3 | Короткий лейбл |
| 4 | Порядок |
| 5 | Активна |

## Действия

- Добавить единицу
- Редактировать единицу (`updateAjax`)
- Переключить активность

## Бэкенд-маршрут

- **Файл контроллера**: `protected/modules/settings/controllers/UnitController.php` (строка 46)
- **Тип действия**: inline (`$this->render('admingrid_diler', …)`)
- **Рендерится вьюха**: `views/unit/admingrid_diler.php`
- **Требуется доступ**: `operation.settings.unit`
- **Соседние эндпоинты**: `getData`, `getUpdatedRow`, `updateAjax`

## См. также

- Справочник модуля: [/modules/settings](/docs/modules/settings)
- Мастер товаров: [`/settings/product/index`](./settings_product_index)
- Тара / упаковка: [/concepts/tara-packaging](/docs/concepts/tara-packaging)
