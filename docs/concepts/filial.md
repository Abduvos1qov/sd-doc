---
title: Filial (tenant branch)
sidebar_position: 1
audience: All
summary: A branch / sub-company inside one dealer's database — the primary multi-tenant scope on every row.
topics: [concept, multi-tenancy]
---

# Filial — tenant branch

> **TL;DR** — A **Filial** is one branch / regional office of a dealer. Almost every business row in sd-main carries a `FILIAL_ID` foreign key, and the framework filters by it automatically. One dealer can run many filials inside the same database.

## What it is

In Russian-language ERP and CRM tradition, *филиал* (filial) means a **branch office** of a larger company. SalesDoctor borrowed the term directly because the platform was built for distribution dealers in the CIS region.

In sd-main:

- A **Filial** is a single row in `d0_filial` (model `Filial`, `protected/models/Filial.php`). It carries `id`, `domain`, `is_main`, `prefix`, `xml_id`.
- Most business data — clients, agents, orders, payments, stock — extends `BaseFilial` (`protected/models/BaseFilial.php`). `BaseFilial` injects automatic `FILIAL_ID` scoping on every query.
- A user logs in to **one filial at a time**. The active filial id is stored on the session and resolved through `FilialComponent` / `BaseFilial::setFilial()`.

The current filial drives nearly every visible row. Switching to another filial replaces the entire dataset — clients, orders, stock, KPI.

## Why it matters

Filials exist because one **dealer** rarely operates from a single location. A distribution business may run a Tashkent branch, a Samarkand branch, and a Bukhara branch out of the same legal entity, each with its own warehouse, its own field agents, and its own price list.

The filial scope lets each branch:

- See only its own clients and orders.
- Hold a separate stock balance per warehouse.
- Run its own KPI plans and routes.
- Share users only via explicit multi-filial access.

For QA and developers: **forgetting `FILIAL_ID` in a SQL join is the single most common cross-tenant leak**. See [sd-main landmines](../security/sd-main-landmines) for the failure modes.

## How SalesDoctor models it

| Layer | Identifier | Where |
|---|---|---|
| Table | `d0_filial` | Model `Filial` (`protected/models/Filial.php`) |
| Parent class | `BaseFilial` | Every scoped model extends it |
| Foreign key | `FILIAL_ID` | On `d0_client`, `d0_agent`, `d0_order`, `d0_defects`, etc. |
| Session key | active filial id | Set by `FilialComponent` / `BaseFilial::setFilial()` |
| Cache prefix | `t:{db}:f:{id}:` | `ScopedCache` namespacing — see [multi-tenancy](../architecture/multi-tenancy) |

The dealer-level row lives in `Diler` (also `extends BaseFilial`), but Diler represents the **dealer-as-tenant** of the billing system; Filial represents the **operating branch** inside that dealer.

## Example

```sql
-- Get all clients of filial 3 (correct):
SELECT * FROM d0_client WHERE FILIAL_ID = 3;

-- Forget the filter and you leak every branch's data:
SELECT * FROM d0_client;        -- BAD — never run without FILIAL_ID
```

In application code the framework adds the filter automatically:

```php
$clients = Client::model()->findAll();  // BaseFilial silently adds FILIAL_ID = current
```

## Common confusions

| Looks like | But actually |
|---|---|
| Dealer | A **dealer** is the SalesDoctor *customer* (one paid subscription, one database). A filial is a *branch within that dealer*. |
| Tenant | Often a synonym for *dealer* in technical writing. One tenant DB can hold many filials. |
| Warehouse | A warehouse (Store) is a stock location. A filial may own several warehouses; the filial is the legal/admin scope, the warehouse is the inventory scope. |
| Diler model | `Diler` is the *dealer-as-tenant* row used by the billing system. It also extends `BaseFilial` but represents a different abstraction level. |

## Related concepts

- [Outlet](./outlet.md) — clients belong to one filial via `Client.FILIAL_ID`.
- [Period close](./period-close.md) — close dates are per filial.
- [Multi-tenancy architecture](../architecture/multi-tenancy)
- [Data isolation](../security/data-isolation)
- [sd-main landmines](../security/sd-main-landmines)
