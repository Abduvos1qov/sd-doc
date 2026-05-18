---
title: "Tasks"
audience: All sd-main developers, QA
summary: Live admin page at /access/frontend/tasks
topics: [access, rbac, page, ui]
---

# Tasks

**URL**: `/access/frontend/tasks` · **Module**: `access` · **Controller**: `FrontendController::tasks` · **RBAC**: `operation.rbac.tasks` + global `showAllRbacFunctions` · **Role harvested**: `admin`

:::note Screenshot pending — harvester re-run needed:::

## Purpose

Catalog of RBAC tasks. A *task* groups one or more operations into a reusable bundle that can be granted directly to a user or attached to a role — Yii calls this the **task** layer, sitting between operations and roles. Hidden when `showAllRbacFunctions` is off.

## Layout

- Left rail: side list of tasks.
- Main pane: operations attached to the selected task.
- Modal: create / update / bind form.

## Actions

- Create new task
- Rename / delete task
- Attach operation to task
- Detach operation from task
- Reload after change

## Backend route

- **Controller file**: `protected/modules/access/controllers/FrontendController.php`
- **Action kind**: inline (`actionTasks` calls `$this->render('tasks')`)
- **View rendered**: `views/frontend/tasks.php`
- **Required permission**: `operation.rbac.tasks`
- **Gating param**: `showAllRbacFunctions` must be truthy
- **JSON endpoints used by this page**:
  - `GET /access/backend/tasks`
  - `GET /access/backend/tasks-privileges?taskId=…`
  - `GET /access/backend/tasks-privileges-available?taskId=…`
  - `POST /access/backend/create-update-assignment`
  - `POST /access/backend/remove-assignments`

## See also

- Module reference: [/modules/access](/docs/modules/access)
- RBAC concept: [/concepts/rbac](/docs/concepts/rbac)
- RBAC matrix: [/quality/rbac-matrix](/docs/quality/rbac-matrix)
