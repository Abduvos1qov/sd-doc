---
title: "Задачи"
audience: Разработчики sd-main, QA
summary: Живая страница админки /access/frontend/tasks
topics: [access, rbac, page, ui]
---

# Задачи

**URL**: `/access/frontend/tasks` · **Модуль**: `access` · **Контроллер**: `FrontendController::tasks` · **RBAC**: `operation.rbac.tasks` + глобальный `showAllRbacFunctions` · **Снятая роль**: `admin`

:::note Скриншот в процессе — нужен повторный запуск харвестера:::

## Назначение

Каталог задач RBAC. *Задача* — это переиспользуемая связка из одной или нескольких операций, которую можно выдать пользователю напрямую или прицепить к роли. В терминах Yii это слой **task**, расположенный между операциями и ролями. Страница скрыта при выключенном `showAllRbacFunctions`.

## Расположение

- Левая колонка: список задач.
- Центр: операции, привязанные к выбранной задаче.
- Модал: форма create / update / bind.

## Действия

- Создать задачу
- Переименовать / удалить задачу
- Привязать операцию к задаче
- Отвязать операцию от задачи
- Перечитать после изменения

## Бэкенд-маршрут

- **Файл контроллера**: `protected/modules/access/controllers/FrontendController.php`
- **Тип действия**: inline (`actionTasks` вызывает `$this->render('tasks')`)
- **Рендерится вьюха**: `views/frontend/tasks.php`
- **Требуется доступ**: `operation.rbac.tasks`
- **Параметр-фильтр**: `showAllRbacFunctions` должен быть истинным
- **JSON-эндпоинты, которые использует страница**:
  - `GET /access/backend/tasks`
  - `GET /access/backend/tasks-privileges?taskId=…`
  - `GET /access/backend/tasks-privileges-available?taskId=…`
  - `POST /access/backend/create-update-assignment`
  - `POST /access/backend/remove-assignments`

## См. также

- Справочник модуля: [/modules/access](/docs/modules/access)
- Концепция RBAC: [/concepts/rbac](/docs/concepts/rbac)
- Матрица RBAC: [/quality/rbac-matrix](/docs/quality/rbac-matrix)
