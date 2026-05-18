---
title: Create and activate an agent account
sidebar_position: 5
audience: End users (admin | HR | supervisor)
summary: Create a user, assign role 4, assign a route, and verify the agent can sign in on mobile.
topics: [tutorial, how-to, team, settings]
---

# Create and activate an agent account

**You will**: Create a brand-new user, assign them role `4` (field agent), attach a route so they have outlets to visit tomorrow, and activate the record so they can log in on mobile. By the end you will know the standard onboarding flow that HR runs every time a new sales rep is hired.
**You need**: A user with role 1 or 9 (admin) with `operation.users.create`; the agent's full name, phone, and login; the route ID (or you can create one inline).
**Time**: ~6 minutes
**Hard parts**:
- Setting `ACTIVE='N'` keeps the record but blocks login — useful for terminations, but easy to confuse with "deleted".
- Roles are numeric (`1=admin`, `2=manager`, `3=operator`, `4=agent`, `5=cashier`, `9=super`, `10=expeditor`). Pick the wrong number and the user gets a different home page.

## Step 1 — Open the agents list

Navigate to **Staff → Agents** (URL: `/staff/view/agent`).

![Annotated screenshot of the agents list](/screens/annotated/staff_view_agent.annotated.png)

The data grid (①) lists every user with role `4` in the current filial. Each row shows login, name, status (`ACTIVE`), assigned route, and last-sync timestamp. Use the column filters at the top of the grid to find existing agents — but for this tutorial we are creating a new one.

## Step 2 — Create the user

1. Click **+ Добавить агента** in the toolbar above the grid (URL: `/staff/staff/create?role=4`).
2. Fill the form:

| Field | What to enter |
|---|---|
| **ФИО** | Full name as it appears on payroll |
| **Логин** | Lowercase Latin letters + digits, no spaces |
| **Пароль** | Initial password — the agent must change it on first login |
| **Телефон** | Required; used for SMS notifications |
| **Филиал** | Pre-filled to your current filial; only admins can pick a different one |
| **Касса** | Default cashbox for cash payments collected on the route |

3. Click **Сохранить**. The form posts to `POST /staff/staff/create`.

## Step 3 — Assign role 4

If the form had a **Роль** dropdown, set it to **Агент**. Otherwise:

1. Open the user's detail page after save.
2. Find the **Роль** field — set it to `4` (Агент).
3. Save. This writes `d0_user.ROLE_ID=4`. The user's home page is now the agent dashboard.

For finer-grained permissions on top of the role, see [RBAC reference](/docs/security/rbac).

## Step 4 — Assign a route

A new agent with no route cannot do anything on mobile — the route tab is empty and check-ins are blocked.

1. Go to **Team → Маршруты** (Routes).
2. Find or create the route this agent will work.
3. In the route's **Агент** field, pick the new user. This writes `d0_route.AGENT_ID = <new userId>`.
4. Make sure the route has outlets attached — visit `d0_route_client` (or use the **Клиенты маршрута** tab).

Alternatively assign the route from the user's own detail page if the **Маршрут** tab is present there.

## Step 5 — Activate and test login

1. Back on `/staff/view/agent`, find the new row. The **ACTIVE** column should read `Y`. If it says `N`, click the row and toggle the **Активен** flag. This writes `d0_user.ACTIVE='Y'`.
2. Have the agent install the SalesDoctor mobile app and sign in with the login/password from step 2.
3. On first login the app calls `POST /api3/login`, receives a token, then `GET /api3/sync/start` downloads their assigned route, products, and price types.
4. Confirm the route tab shows tomorrow's outlets.

## Step 6 — Verify on the web

Refresh `/staff/view/agent`. The new row should show:

- **ACTIVE**: `Y`
- **Маршрут**: the route you assigned
- **Последний sync**: a recent timestamp (after the agent's first login)

## What just happened (under the hood)

`POST /staff/staff/create` writes one row to `d0_user` with `ROLE_ID=4`. The route assignment is a separate write on `d0_route.AGENT_ID`. The mobile app's first sync (`/api3/sync/start`) reads these joined together to seed the local SQLite database. See the [team module](/docs/modules/team) and [agents module](/docs/modules/agents) for the data model, and [auth and roles](/docs/security/auth-and-roles) for how `ROLE_ID` maps to RBAC permissions.

## Common mistakes

- **Forgetting to assign a route**: the agent can log in but their route tab is empty and check-ins fail with "нет маршрута на сегодня".
- **Setting ROLE_ID=2 or 3 by accident**: the user gets the operator/manager home page instead of the agent dashboard, and the mobile app will refuse to log them in (it gates by role 4 only).
- **Leaving `ACTIVE='N'`**: login fails with a generic "неверный логин" — agents waste 20 minutes assuming the password is wrong before someone checks the active flag.

## Next steps

- Set up a KPI plan so this new agent shows up on the dashboard: [Run an agent KPI report](./run-kpi-report.md).
- Walk them through their first mobile order: [Create an order from the mobile agent app](./create-order-mobile.md).
- Full reference on roles and permissions: [agents module](/docs/modules/agents), [team module](/docs/modules/team).
