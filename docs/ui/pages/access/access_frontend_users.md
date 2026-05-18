---
title: "Users & assignments"
audience: All sd-main developers, QA
summary: Live admin page at /access/frontend/users
topics: [access, rbac, page, ui]
---

# Users & assignments

**URL**: `/access/frontend/users` · **Module**: `access` · **Controller**: `FrontendController::users` · **RBAC**: `operation.rbac.users` · **Role harvested**: `admin`

:::note Screenshot pending — harvester re-run needed:::

## Purpose

The RBAC users board. Pick a user from the left side list, see the union of roles, tasks and operations currently assigned, and bind or unbind privileges using the modal form. Data is loaded from `/access/backend/users`, `/access/backend/users-privileges?userId=…`, and `/access/backend/users-privileges-available?userId=…`.

## Layout

- Left rail: side list of users (`_sideList` partial).
- Top: group selector chips (`_groupList` partial).
- Main pane: assignment table with one row per privilege (`_accessTable` partial).
- Modal: create / update / bind form (`_modalForm` + `_crudBtns` partials).

## Actions

- Bind assignment to selected user
- Unbind selected assignment
- Create / update assignment (modal)
- Remove assignment
- Reload assignments (refetches both lists after a mutation)

## Backend route

- **Controller file**: `protected/modules/access/controllers/FrontendController.php`
- **Action kind**: inline (`actionUsers` calls `$this->render('users')`)
- **View rendered**: `views/frontend/users.php`
- **Required permission**: `operation.rbac.users`
- **JSON endpoints used by this page**:
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

## See also

- Module reference: [/modules/access](/docs/modules/access)
- RBAC concept: [/concepts/rbac](/docs/concepts/rbac)
- RBAC matrix: [/quality/rbac-matrix](/docs/quality/rbac-matrix)
