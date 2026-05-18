---
sidebar_position: 4
title: Add sales agents
---

# Add your sales agents

Sales **agents** are the people who visit clients and take orders. Each agent needs their own login so visits and orders can be attributed correctly.

## Step 1 — Open the agents list

From the menu, choose **Команда → Агенты** (Team → Agents), or open `/agents/agent` directly:

![Agents list — top of page with action buttons](/screens/guide/07-agents-list.webp)

The list shows every agent in your team with their phone, supervisor, and active status.

## Step 2 — Click "Добавить агента"

Look for the **+ Добавить агента** button at the top right of the list. The form opens as a side panel:

![Add agent form with all fields](/screens/guide/29-add-agent-form.webp)

## Step 3 — Fill in the form

| Field | What to enter |
|-------|---------------|
| **Логин** | A short login name (e.g. `agent.askar`) — the agent will use it to sign in to the mobile app |
| **Пароль** | A password you'll share with the agent |
| **ФИО** | The agent's full name as it should appear on documents |
| **Телефон** | Working mobile number — used for SMS and password recovery |
| **Филиал** | Which branch / office this agent belongs to |
| **Супервайзер** | Who oversees this agent (can be changed later) |
| **Активен** | Leave on. Turn off later if the agent leaves the team. |

## Step 4 — Save

Click **Сохранить** (Save). The agent appears in the list immediately and can sign in to the mobile app with their new login and password.

## Step 5 — Set a route or KPI plan (optional)

From the agent's profile you can now:

- **Assign a weekly visit route** — see [Plan visits](../daily-use/plan-visits)
- **Set KPI targets** for the month — sales, AKB, visits — see [Dashboard & KPI](../reports/dashboard-kpi)

## Step 6 — Open an agent's profile

Click any agent's name in the list to open their profile page:

![Agent detail page — profile tabs, KPI, sync log, route](/screens/guide/47-agent-detail.webp)

From here you can:
- Edit phone, login, supervisor assignment
- Open the **KPI** tab to set monthly targets
- Open the **Маршрут** (Route) tab to set the visit plan for this agent
- See their last sync time and device info

## When an agent leaves the team

Don't delete the account — that would erase their visit and order history. Instead:

1. Open the agent's profile.
2. Turn **Активен** off and save.

The agent can no longer sign in, but all their past data remains visible in reports.

:::tip One agent per login
Each agent should have their own login. Two people sharing one login causes orders to be recorded against the wrong person.
:::

---

**Next:** [Add supervisors →](./add-supervisors)
