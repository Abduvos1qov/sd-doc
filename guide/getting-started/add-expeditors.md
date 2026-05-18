---
sidebar_position: 6
title: Add expeditors
---

# Add expeditors

An **expeditor** delivers orders to clients — usually a driver with a van. Each morning they load up, drive a route, drop off orders, and bring back unsold stock or money collected.

## Step 1 — Open the expeditors list

From the menu choose **Команда → Экспедиторы** (Team → Expeditors), or open `/staff/view/expeditor` directly:

![Expeditors list](/screens/guide/19-expeditors-list.png)

You see every expeditor with their phone, assigned vehicle, and today's trip status.

## Step 2 — Click "Добавить"

Click **+ Добавить** at the top right. The expeditor creation form opens at `/staff/create/expeditor`:

![Add expeditor form](/screens/guide/31-add-expeditor-form.png)

## Step 3 — Fill in the form

| Field | What to enter |
|-------|---------------|
| **Логин** | A short login name (e.g. `exp.rustam`) |
| **Пароль** | A password to share |
| **ФИО** | Full name |
| **Телефон** | Working mobile number |
| **Филиал** | Branch |
| **Машина** | Vehicle assigned to them (optional, can be changed daily) |

## Step 4 — Save

Click **Сохранить**. The expeditor can sign in to the mobile app immediately.

## A typical expeditor day

| Time | What happens |
|------|--------------|
| **Morning** | Pick up load at the warehouse — the app shows today's orders, the expeditor confirms quantities |
| **On the route** | Each stop: hand goods, record delivery, collect payment, record returns |
| **End of day** | Return unsold goods, hand cash to the cashier — trip closes |

You'll see all of this happening live on your dashboard while they work.

## Step 5 — Watch the trip live

From **Заявки → Рейсы** (Orders → Trips):

![Trips view — today's deliveries](/screens/guide/20-trips-view.png)

Each row is one expeditor's trip with:

- Stops completed vs planned
- Money currently on the van
- Last GPS ping
- Any anomalies (long stop, off-route, missed)

## Tips

- **One van per expeditor per day** is the cleanest setup. Two expeditors sharing a vehicle confuses load tracking.
- **Don't reuse logins** between agents and expeditors. The mobile app shows different screens for each role.
- **Inactive expeditors** — turn off **Активен** in the profile when an expeditor is off (illness, holiday, leaves the team). The login stops working but history stays.

---

**Next:** [Add clients →](./add-clients)
