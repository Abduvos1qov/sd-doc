---
title: "Roles"
audience: All sd-main developers, QA
summary: Live admin page at /access/frontend/roles
topics: [access, rbac, page, ui]
---

# Roles

**URL**: `/access/frontend/roles` · **Module**: `access` · **Controller**: `FrontendController::roles` · **RBAC**: `operation.rbac.roles` + global `showAllRbacFunctions` · **Role harvested**: `admin`

:::note Screenshot pending — harvester re-run needed:::

## Purpose

Catalog of RBAC roles. Each role aggregates a set of operations (and optionally other roles). Use this page to define a role like `manager` or `audit-lite`, then attach operations to it via the assignment table. The page is hidden when the server param `showAllRbacFunctions` is off, even if the user otherwise has `operation.rbac.roles` — `H::err403()` is raised.

## Layout

- Left rail: side list of roles.
- Main pane: assignments table (operations attached to the selected role).
- Modal: create / update / bind form.

## Actions

- Create new role
- Rename / delete role
- Attach operation to role
- Detach operation from role
- Reload after change

## Backend route

- **Controller file**: `protected/modules/access/controllers/FrontendController.php`
- **Action kind**: inline (`actionRoles` calls `$this->render('roles')`)
- **View rendered**: `views/frontend/roles.php`
- **Required permission**: `operation.rbac.roles`
- **Gating param**: `showAllRbacFunctions` must be truthy
- **JSON endpoints used by this page**:
  - `GET /access/backend/roles`
  - `GET /access/backend/roles-privileges?roleId=…`
  - `GET /access/backend/roles-privileges-available?roleId=…`
  - `POST /access/backend/create-update-assignment`
  - `POST /access/backend/remove-assignments`
  - `POST /access/backend/bind-assignments`
  - `POST /access/backend/un-bind-assignments`

## See also

- Module reference: [/modules/access](/docs/modules/access)
- RBAC concept: [/concepts/rbac](/docs/concepts/rbac)
- RBAC matrix: [/quality/rbac-matrix](/docs/quality/rbac-matrix)
