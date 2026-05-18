---
title: "Пользователи и назначения"
audience: Разработчики sd-main, QA
summary: Живая страница админки /access/frontend/users
topics: [access, rbac, page, ui]
---

# Пользователи и назначения

**URL**: `/access/frontend/users` · **Модуль**: `access` · **Контроллер**: `FrontendController::users` · **RBAC**: `operation.rbac.users` · **Снятая роль**: `admin`

:::note Скриншот в процессе — нужен повторный запуск харвестера:::

## Назначение

Доска RBAC по пользователям. Выберите пользователя в боковом списке, увидите объединение всех его ролей, задач и операций и используйте модальную форму, чтобы привязать или отвязать привилегии. Данные подгружаются из `/access/backend/users`, `/access/backend/users-privileges?userId=…` и `/access/backend/users-privileges-available?userId=…`.

## Расположение

- Левая колонка: список пользователей (партиал `_sideList`).
- Верх: переключатель групп (партиал `_groupList`).
- Центр: таблица назначений, по строке на привилегию (партиал `_accessTable`).
- Модал: форма create / update / bind (партиалы `_modalForm` + `_crudBtns`).

## Действия

- Привязать привилегию к выбранному пользователю
- Отвязать выбранное назначение
- Создать / изменить назначение (модал)
- Удалить назначение
- Перечитать назначения (после любой мутации)

## Бэкенд-маршрут

- **Файл контроллера**: `protected/modules/access/controllers/FrontendController.php`
- **Тип действия**: inline (`actionUsers` вызывает `$this->render('users')`)
- **Рендерится вьюха**: `views/frontend/users.php`
- **Требуется доступ**: `operation.rbac.users`
- **JSON-эндпоинты, которые использует страница**:
  - `GET /access/backend/users`
  - `GET /access/backend/users-privileges?userId=…`
  - `GET /access/backend/users-privileges-available?userId=…`
  - `POST /access/backend/create-update-assignment`
  - `POST /access/backend/remove-assignments`
  - `POST /access/backend/bind-assignments`
  - `POST /access/backend/un-bind-assignments`
  - `POST /access/backend/bind-user`
  - `POST /access/backend/un-bind-user`
  - `POST /access/backend/reload-assignments`

## См. также

- Справочник модуля: [/modules/access](/docs/modules/access)
- Концепция RBAC: [/concepts/rbac](/docs/concepts/rbac)
- Матрица RBAC: [/quality/rbac-matrix](/docs/quality/rbac-matrix)
