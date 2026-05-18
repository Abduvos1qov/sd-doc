---
title: "Users"
audience: All sd-main developers, QA
summary: Live admin page at /settings/user/index
topics: [settings, user, page, ui]
---

# Users

**URL**: `/settings/user/index` · **Module**: `settings` · **Controller**: `UserController::index` · **RBAC**: `operation.settings.user` · **Role harvested**: `admin`

:::note Screenshot pending — harvester re-run needed:::

## Purpose

The tenant's user roster. Every login (admin, manager, supervisor, agent, expeditor, warehouse, audit) is registered here together with login credentials, locale, default role, contact info and the territory / brand scopes that gate the rest of the app. Password rotation is split into a self-service path (`updateLoginPassword`) and a super-admin path (`updateLoginPassword2`).

## Grid columns

| # | Column |
|---|---|
| 1 | ID |
| 2 | Login |
| 3 | Full name |
| 4 | Role |
| 5 | Territory |
| 6 | Phone |
| 7 | Last login |
| 8 | Active |
| 9 | Created at |

## Actions

- Add user (modal — `createAjax`)
- Edit user (modal — `updateAjax`)
- Delete user (`deleteUser`)
- Reset password (self — `updateLoginPassWord`)
- Reset password (admin — `updateLoginPassword2`)
- Return ajax form (`returnAjaxForm`)
- Toggle active

## Backend route

- **Controller file**: `protected/modules/settings/controllers/UserController.php` (line 24)
- **Action kind**: inline (`$this->render('admingrid_diler', …)`)
- **View rendered**: `views/user/admingrid_diler.php`
- **Required permission**: `operation.settings.user`
- **Sibling endpoints**: `getData`, `getUpdatedRow`, `createAjax`, `updateAjax`, `deleteUser`, `updateLoginPassWord`, `updateLoginPassword2`, `returnAjaxForm`

## See also

- Module reference: [/modules/settings](/docs/modules/settings)
- RBAC console: [`/access/frontend/users`](../access/access_frontend_users)
- RBAC matrix: [/quality/rbac-matrix](/docs/quality/rbac-matrix)
