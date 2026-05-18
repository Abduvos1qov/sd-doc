---
sidebar_position: 11
title: Stock write-off
---

# Writing off stock

Sometimes stock has to leave inventory without being sold — it's expired, broken, lost in transit, or you're correcting a miscount. The **write-off** ("Списание" / Excretion) is the formal way to remove it.

## Step 1 — Open the write-off list

From the menu choose **Склад → Списания** (Warehouse → Write-offs), or open `/stock/excretion` directly:

![Stock write-off list](/screens/guide/63-stock-write-off.webp)

You see every write-off ever done — who, when, from which warehouse, what was written off, why.

## Step 2 — Click "Add write-off"

Click **+ Добавить** at the top right. The form opens with three sections:

- **Header** — Warehouse, date, reason category (expired / damaged / lost / inventory correction)
- **Product table** — what's being written off
- **Comment** — free-text explanation (recommended)

## Step 3 — Fill the header

| Field | What to enter |
|-------|---------------|
| **Склад** (Warehouse) | Where the stock currently is (defect / main / van) |
| **Дата** (Date) | When the write-off happened |
| **Причина** (Reason) | Pick from: expired, damaged, lost, inventory correction, theft |
| **Ответственный** (Responsible) | Person signing for the write-off |

## Step 4 — Add the products

For each item:
- Pick the product (or scan barcode)
- Enter the **quantity** to remove
- The **value** auto-calculates from the product's cost price

The form shows a running total of value being written off — useful for finance reporting.

## Step 5 — Save

Click **Сохранить**. The stock balance updates immediately:
- The quantity disappears from the source warehouse
- A write-off ledger row appears in finance reports
- The cost value hits your P&L as a loss

## Common reasons and what they mean

| Reason | When to use it |
|--------|---------------|
| **Просрочка** (Expired) | Past the use-by date. Most common reason. |
| **Поломка** (Damaged) | Physical damage — bottle broken, packaging crushed |
| **Утеря** (Lost) | Missing during inventory count, no recovery expected |
| **Корректировка** (Inventory correction) | The system showed N units but the shelf had N−2; this aligns the count |
| **Кража** (Theft) | Confirmed theft — usually paired with a police report |

## Step 6 — Review the impact in reports

After saving, the write-off shows up in:
- **Stock balance** — quantities now reflect the post-write-off totals
- **P&L report** — the cost of written-off goods appears under "losses"
- **Stock report by reason** — category breakdown ("how much do we lose to expiration per month?")

## Tips

- **Always add a comment** — when finance asks "why was 500,000 UZS of beer written off last month?", the comment saves you.
- **Run monthly write-offs** as a routine — not when you notice something. Catching expired stock the day before it expires is too late.
- **A separate "defect" warehouse** (covered in [Set up warehouses](./set-up-warehouses)) makes write-offs cleaner — defective stock lives there from the moment it comes back from a client, then gets written off in a single weekly action.

---

**Next:** [Create your first order →](../daily-use/first-order)
