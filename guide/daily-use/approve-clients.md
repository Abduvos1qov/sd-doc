---
sidebar_position: 4
title: Approve new clients
---

# Approve newly-added clients

When an agent adds a new client from their mobile app during a visit, the client lands in an **approval queue** instead of going straight to your active client list. This guard catches duplicates, typos, and made-up clients before they pollute your reports.

## Step 1 — Open the approval queue

From the clients list, click **Неподтвержденные клиенты** (Unconfirmed clients), or open `/clients/approval` directly:

![Unconfirmed clients approval queue](/screens/guide/62-clients-approval.png)

Each row is a client an agent created in the field but you haven't reviewed yet.

## Step 2 — Read each pending row

Columns typically shown:
- **Дата создания** (Created on) — when the agent submitted it
- **Агент** (Agent) — who created it
- **Название** (Name) — what they typed
- **Телефон** (Phone)
- **Адрес** (Address)
- **Координаты** (GPS coordinates) — captured automatically
- **Действия** (Actions) — approve / reject / merge

## Step 3 — Look for problems

Before approving, scan for:
- **Duplicates** — does a client with the same phone or address already exist?
- **Typos** — "Магазин Юлдуз" vs "Магазин Юлдус"
- **Made-up clients** — GPS coordinates in the middle of a field, no phone, generic name
- **Wrong channel/territory** — the agent picked the wrong category

The search box at the top lets you check for existing clients with the same phone or name in seconds.

## Step 4 — Approve, reject, or merge

| Action | When to use |
|--------|-------------|
| **Подтвердить** (Approve) | Looks correct, no duplicate found. Client becomes active. |
| **Отклонить** (Reject) | Made-up or unverifiable. Returns to the agent with a reason. |
| **Объединить** (Merge) | Same shop as an existing client. Combines them; the existing client absorbs the new GPS + any extra fields. |

Approval is one click — the row disappears from the queue.

## Step 5 — Bulk approve

If a trusted agent submits 20 well-formed clients, you can multi-select and approve all at once:
1. Tick the checkbox column for each row
2. Click **Групповая обработка → Подтвердить** at the top

## When to approve and when to wait

| Situation | What to do |
|-----------|-----------|
| Agent has good track record, normal-looking row | Approve |
| GPS shows the shop is on a major street with similar name nearby | Search first; merge if duplicate |
| GPS coordinates show a residential building or empty field | Reject and ask the agent why |
| Same name appears 3+ times from different agents | Merge or reject — only one is real |

## Tips

- **Daily review** is the right cadence — too long and the queue grows; too often and you spend time on partially-filled rows.
- **Train agents to use the GPS feature** — coordinates make verification much faster.
- **Pre-define your channels and categories** before agents start creating clients — otherwise they'll guess.

---

**Next:** [Mobile agent app →](../mobile/agent-app)
