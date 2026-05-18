---
title: "Access — interfeys sahifalari"
sidebar_position: 1
---

# Access — interfeys sahifalari

**Access** moduli — ilova ichidagi RBAC konsoli. Foydalanuvchi koʻradigan qism `FrontendController` tomonidan render qilinadi va `BackendController` chiqaradigan JSON API'dan maʼlumot oladi. Ikkala kontroller ham `protected/modules/access/controllers/` ichida joylashgan.

| URL | Sahifa | Kontroller | RBAC |
|---|---|---|---|
| `/access/frontend/users` | [Foydalanuvchilar va tayinlovlar](./access_frontend_users) | `FrontendController::users` | `operation.rbac.users` |
| `/access/frontend/roles` | [Rollar](./access_frontend_roles) | `FrontendController::roles` | `operation.rbac.roles` |
| `/access/frontend/tasks` | [Vazifalar](./access_frontend_tasks) | `FrontendController::tasks` | `operation.rbac.tasks` |
| `/access/frontend/operations` | [Operatsiyalar](./access_frontend_operations) | `FrontendController::operations` | `operation.rbac.operations` |

Roles / Tasks / Operations sahifalari qoʻshimcha ravishda global `showAllRbacFunctions` server bayrog'i bilan yashiriladi — bayroq oʻchirilgan boʻlsa, mos operatsiya bor foydalanuvchilar ham 403 oladi. [RBAC kontsepsiyasi](/docs/concepts/rbac) va [Access moduli maʼlumotnomasi](/docs/modules/access) ga qarang.

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/access](/docs/modules/access)
- Marshrutlar reestri: [`static/data/routes.json`](/data/routes.json)
