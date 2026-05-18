---
title: "Роли"
audience: Разработчики sd-main, QA
summary: Живая страница админки /access/frontend/roles
topics: [access, rbac, page, ui]
---

# Роли

**URL**: `/access/frontend/roles` · **Модуль**: `access` · **Контроллер**: `FrontendController::roles` · **RBAC**: `operation.rbac.roles` + глобальный `showAllRbacFunctions` · **Снятая роль**: `admin`

:::note Скриншот в процессе — нужен повторный запуск харвестера:::

## Назначение

Каталог ролей RBAC. Роль собирает набор операций (и опционально другие роли). На этой странице создают роль вроде `manager` или `audit-lite` и привязывают к ней операции через таблицу назначений. Страница скрыта, если серверный параметр `showAllRbacFunctions` выключен — даже при наличии `operation.rbac.roles` поднимается `H::err403()`.

## Расположение

- Левая колонка: список ролей.
- Центр: таблица назначений (операции, привязанные к выбранной роли).
- Модал: форма create / update / bind.

## Действия

- Создать роль
- Переименовать / удалить роль
- Привязать операцию к роли
- Отвязать операцию от роли
- Перечитать после изменения

## Бэкенд-маршрут

- **Файл контроллера**: `protected/modules/access/controllers/FrontendController.php`
- **Тип действия**: inline (`actionRoles` вызывает `$this->render('roles')`)
- **Рендерится вьюха**: `views/frontend/roles.php`
- **Требуется доступ**: `operation.rbac.roles`
- **Параметр-фильтр**: `showAllRbacFunctions` должен быть истинным
- **JSON-эндпоинты, которые использует страница**:
  - `GET /access/backend/roles`
  - `GET /access/backend/roles-privileges?roleId=…`
  - `GET /access/backend/roles-privileges-available?roleId=…`
  - `POST /access/backend/create-update-assignment`
  - `POST /access/backend/remove-assignments`
  - `POST /access/backend/bind-assignments`
  - `POST /access/backend/un-bind-assignments`

## См. также

- Справочник модуля: [/modules/access](/docs/modules/access)
- Концепция RBAC: [/concepts/rbac](/docs/concepts/rbac)
- Матрица RBAC: [/quality/rbac-matrix](/docs/quality/rbac-matrix)
