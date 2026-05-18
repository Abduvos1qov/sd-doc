---
title: "Operations"
audience: All sd-main developers, QA
summary: Live admin page at /access/frontend/operations
topics: [access, rbac, page, ui]
---

# Operations

**URL**: `/access/frontend/operations` · **Module**: `access` · **Controller**: `FrontendController::operations` · **RBAC**: `operation.rbac.operations` + global `showAllRbacFunctions` · **Role harvested**: `admin`

:::note Screenshot pending — harvester re-run needed:::

## Purpose

Read-only catalog of every RBAC operation defined in the system. Operations are the lowest-level privilege; every controller `H::access('operation.<module>.<action>')` call resolves to a row here. The list is computed by `Access::AssignmentsAvailable(["type" => 0, "parentType" => 1])`, which enumerates all operations not yet attached to anything. Hidden when `showAllRbacFunctions` is off.

## Grid columns

| # | Column |
|---|---|
| 1 | Operation name (e.g. `operation.orders.list`) |
| 2 | Description (i18n label) |
| 3 | Module |
| 4 | Group |

## Actions

- Filter / search by name
- Open a related role or task to attach this operation

## Backend route

- **Controller file**: `protected/modules/access/controllers/FrontendController.php`
- **Action kind**: inline (`actionOperations` calls `$this->render('operations')`)
- **View rendered**: `views/frontend/operations.php`
- **Required permission**: `operation.rbac.operations`
- **Gating param**: `showAllRbacFunctions` must be truthy
- **JSON endpoint used by this page**: `GET /access/backend/operations`

## See also

- Module reference: [/modules/access](/docs/modules/access)
- RBAC concept: [/concepts/rbac](/docs/concepts/rbac)
- RBAC matrix: [/quality/rbac-matrix](/docs/quality/rbac-matrix)
