---
title: Admin (super-admin) — start here
sidebar_position: 1
audience: Admin
summary: The dealer's super-admin. Configures the platform, manages users and RBAC, runs period close, and operates integrations.
topics: [role-landing]
---

# Welcome, Admin

You are role **1** in this dealer's database — the highest-privilege user. You don't take orders or visit clients. You configure how the system behaves: who can log in, what they can see, when the books close, which external systems get pinged, and which mobile-app toggles are flipped on.

You are the only role that can edit global server parameters and run a period close. With that privilege comes the responsibility to keep a clean audit trail of any change you make outside the normal day's flow.

## In your first 5 minutes

- [Authentication & roles](../security/auth-and-roles) — what each of roles 1–11 can do.
- [RBAC](../security/rbac) — how operations map to permissions.
- [sd-main landmines](../security/sd-main-landmines) — every silent failure mode you must know about.

## Daily tasks

| Task | Where in the admin | Tutorial |
|------|-------------------|----------|
| Create or edit a user / change role | `/settings/access-staff` | [Set up an agent](../tutorials/setup-agent) |
| Set or rotate the period close date | `/settings/closed` | [Server toggles and period close](../quality/settings/server-toggles-and-period-close) |
| Edit global server parameters | `/settings/params` | [Server toggles](../quality/settings/server-toggles-and-period-close) |
| Configure RBAC permissions | `/settings/rbac` | [RBAC and users](../quality/settings/rbac-and-users) |
| Manage cashboxes | `/settings/cashbox` | [Cashbox management](../quality/settings/cashbox-management) |
| Configure price types | `/settings/price-type` | [Price types](../quality/settings/price-types) |
| Wire an integration (1C / Faktura.uz / Telegram) | `/integration` | [Integrations overview](../integrations/overview) |
| Onboard a new filial | `/settings/filial` | [Multi-tenancy](../architecture/multi-tenancy) |

## Reference

- [Settings module](../modules/settings-access-staff) — the admin surface
- [Auth and roles](../security/auth-and-roles)
- [Data isolation](../security/data-isolation)
- [Multi-tenancy](../architecture/multi-tenancy)
- [RBAC](../security/rbac) — the permission matrix
- [Integration module](../modules/integration)

## Common gotchas

- **`FILIAL_ID` is the cross-tenant boundary.** A raw SQL or a stored proc without `FILIAL_ID` leaks data across branches — see [sd-main landmines](../security/sd-main-landmines).
- **Period close is per-dealer-setting, per-filial-enforcement.** Each filial closes against its own calendar; don't assume one global cut-off.
- **Agent packet edits are read-modify-write.** Two admins editing different keys of the same agent's `SETTINGS` blob can silently clobber each other. See [agents-packet](../quality/team/agents-packet#conflict-landmine--the-read-modify-write-hazard).
- **All-zero KPI deletes the row.** Clearing every target value on a KPI deletes the `Kpi` + `KpiTask` rows for that month — easy to do by accident.
- **Subscription cap is enforced at agent-create time.** A dealer over its licence cap silently refuses new active agents.

## Glossary terms you'll meet

- [Filial](../concepts/filial)
- [Period close](../concepts/period-close)
- [Price type](../concepts/price-type)
- [KPI](../concepts/kpi)
- [Outlet](../concepts/outlet)
- [Bonus vs discount](../concepts/bonus-vs-discount)
- [Defect vs reject](../concepts/defect-vs-reject)
