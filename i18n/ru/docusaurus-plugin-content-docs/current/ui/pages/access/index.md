---
title: "Access — страницы интерфейса"
sidebar_position: 1
---

# Access — страницы интерфейса

Модуль **Access** — встроенная RBAC-консоль. Видимая пользователю часть рендерится `FrontendController`, данные она получает по JSON API из `BackendController`. Оба контроллера лежат в `protected/modules/access/controllers/`.

| URL | Страница | Контроллер | RBAC |
|---|---|---|---|
| `/access/frontend/users` | [Пользователи и назначения](./access_frontend_users) | `FrontendController::users` | `operation.rbac.users` |
| `/access/frontend/roles` | [Роли](./access_frontend_roles) | `FrontendController::roles` | `operation.rbac.roles` |
| `/access/frontend/tasks` | [Задачи](./access_frontend_tasks) | `FrontendController::tasks` | `operation.rbac.tasks` |
| `/access/frontend/operations` | [Операции](./access_frontend_operations) | `FrontendController::operations` | `operation.rbac.operations` |

Страницы Roles / Tasks / Operations дополнительно скрыты глобальным флагом `showAllRbacFunctions` — при выключенном флаге даже владельцы соответствующих операций получают 403. См. [концепцию RBAC](/docs/concepts/rbac) и [справочник модуля Access](/docs/modules/access).

## См. также

- Справочник модуля: [/modules/access](/docs/modules/access)
- Реестр маршрутов: [`static/data/routes.json`](/data/routes.json)
