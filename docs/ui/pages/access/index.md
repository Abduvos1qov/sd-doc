---
title: "Access — UI pages"
sidebar_position: 1
---

# Access — UI pages

The **Access** module is the in-app RBAC console. The user-facing surface is rendered by `FrontendController` and consumes the JSON API exposed by `BackendController`; both live under `protected/modules/access/controllers/`.

| URL | Page | Controller | RBAC |
|---|---|---|---|
| `/access/frontend/users` | [Users & assignments](./access_frontend_users) | `FrontendController::users` | `operation.rbac.users` |
| `/access/frontend/roles` | [Roles](./access_frontend_roles) | `FrontendController::roles` | `operation.rbac.roles` |
| `/access/frontend/tasks` | [Tasks](./access_frontend_tasks) | `FrontendController::tasks` | `operation.rbac.tasks` |
| `/access/frontend/operations` | [Operations](./access_frontend_operations) | `FrontendController::operations` | `operation.rbac.operations` |

The Roles / Tasks / Operations pages are additionally gated by the global server flag `showAllRbacFunctions` — when off they return 403 even for users with the operation permission. See the [RBAC concept page](/docs/concepts/rbac) and the [Access module reference](/docs/modules/access).

## See also

- Module reference: [/modules/access](/docs/modules/access)
- Routes inventory: [`static/data/routes.json`](/data/routes.json)
