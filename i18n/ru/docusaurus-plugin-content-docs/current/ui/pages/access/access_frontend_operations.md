---
title: "Операции"
audience: Разработчики sd-main, QA
summary: Живая страница админки /access/frontend/operations
topics: [access, rbac, page, ui]
---

# Операции

**URL**: `/access/frontend/operations` · **Модуль**: `access` · **Контроллер**: `FrontendController::operations` · **RBAC**: `operation.rbac.operations` + глобальный `showAllRbacFunctions` · **Снятая роль**: `admin`

:::note Скриншот в процессе — нужен повторный запуск харвестера:::

## Назначение

Каталог всех RBAC-операций, определённых в системе, только для чтения. Операция — нижний уровень привилегии: каждый вызов `H::access('operation.<module>.<action>')` в контроллерах разрешается в одну из строк отсюда. Список вычисляется методом `Access::AssignmentsAvailable(["type" => 0, "parentType" => 1])`, который перебирает все операции, ещё ни к чему не прикреплённые. Страница скрыта при выключенном `showAllRbacFunctions`.

## Колонки таблицы

| № | Колонка |
|---|---|
| 1 | Имя операции (например, `operation.orders.list`) |
| 2 | Описание (i18n-метка) |
| 3 | Модуль |
| 4 | Группа |

## Действия

- Поиск / фильтр по имени
- Перейти к роли или задаче, чтобы привязать эту операцию

## Бэкенд-маршрут

- **Файл контроллера**: `protected/modules/access/controllers/FrontendController.php`
- **Тип действия**: inline (`actionOperations` вызывает `$this->render('operations')`)
- **Рендерится вьюха**: `views/frontend/operations.php`
- **Требуется доступ**: `operation.rbac.operations`
- **Параметр-фильтр**: `showAllRbacFunctions` должен быть истинным
- **JSON-эндпоинт страницы**: `GET /access/backend/operations`

## См. также

- Справочник модуля: [/modules/access](/docs/modules/access)
- Концепция RBAC: [/concepts/rbac](/docs/concepts/rbac)
- Матрица RBAC: [/quality/rbac-matrix](/docs/quality/rbac-matrix)
