---
sidebar_position: 5
title: Add supervisors
---

# Add supervisors

A **supervisor** oversees a group of agents. They see live progress on the dashboard, approve special prices, and review the team's daily reports.

## Step 1 — Open the supervisors list

From the menu choose **Команда → Супервайзеры** (Team → Supervisors), or open `/team/supervisor` directly:

![Supervisors list](/screens/guide/17-supervisors-list.webp)

The list shows every supervisor with their phone, branch, and the agents who report to them.

## Step 2 — Click "Добавить"

Click **+ Добавить** at the top right. You'll land on the supervisor form at `/team/supervisor/create`:

![Add supervisor form](/screens/guide/30-add-supervisor-form.webp)

## Step 3 — Fill in the form

| Field | What to enter |
|-------|---------------|
| **Логин** | A short login name (e.g. `sup.olim`) |
| **Пароль** | A password to share with them |
| **ФИО** | Full name |
| **Телефон** | Working mobile number |
| **Филиал** | Branch they belong to |
| **Агенты** | Tick the agents who will report to this supervisor |

## Step 4 — Save

Click **Сохранить**. The supervisor can sign in immediately to the same web app.

## What a supervisor can do

| Action | Where |
|--------|-------|
| Watch live team progress | Dashboard |
| Approve special prices | Pending orders alert |
| Review daily reports | Reports → By agent |
| See visit photos | Audit → Photo report |
| Track agent KPI progress | Dashboard / KPI report |

## Step 5 — Reassign an agent

To move an agent to a different supervisor:

1. Open the **new** supervisor's profile
2. Find the agent in the **Агенты** picker
3. Tick them and save

The agent immediately reports to the new supervisor. Past history stays with whoever had the agent at the time.

:::tip One supervisor per agent
An agent reports to exactly one supervisor at a time. If you need two people to oversee a team, give them the **Manager** role instead — managers see all agents at once.
:::

---

**Next:** [Add expeditors →](./add-expeditors)
