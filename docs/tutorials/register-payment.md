---
title: Register a payment from an agent
sidebar_position: 3
audience: End users (sales rep | manager)
summary: Open a delivered order, enter the cash collected, and queue the payment for the cashier to approve.
topics: [tutorial, how-to, payment, orders]
---

# Register a payment from an agent

**You will**: Find an order the agent has just collected cash for, attach a payment to it, and put the payment in front of the cashier for approval. By the end you will know how the agent → cashier hand-off works.
**You need**: A user with role 4 (agent) or 3/9 (operator/manager); the order must already be in status `Delivered` or later; cashbox must be active in **Settings → Cashbox**.
**Time**: ~2 minutes
**Hard parts**:
- Payments are **two-step**: the agent registers, the cashier approves. Until the cashier acts, the cashbox balance does not move and the client debt does not change.
- The currency of the payment must match the order's currency, otherwise the form refuses to save.

## Step 1 — Find the order

Open the orders list (URL: `/orders/list`).

![Annotated screenshot of orders list](/screens/annotated/orders_list.annotated.png)

1. Filter **Статус заявки** (①) by **Доставлен** to narrow to deliverable orders.
2. Optionally filter **Тип заявки** (②), **Категория клиента** (③), **Территория** (④) or **Супервайзер** (⑤) to find the right row faster.
3. Click the order row in the grid (⑥).

## Step 2 — Open the payment dialog

On the order detail page, scroll to the **Платежи** (Payments) panel and click **+ Добавить платёж**.

A modal opens with:

| Field | What to enter |
|---|---|
| **Сумма** | Amount actually collected (in the order's currency) |
| **Способ оплаты** | Cash / card / transfer — pick what the customer paid with |
| **Касса** | Which cashbox to credit (defaults to your filial's primary cash) |
| **Комментарий** | Optional, but cashiers reject vague entries — write the receipt number |
| **Фото** | Receipt photo if `enablePaymentPhoto=1` for the tenant |

## Step 3 — Save and check the badge

1. Click **Сохранить**.
2. The form posts to `POST /payment/payment/create` — the row is written to `d0_payment` with `STATUS=0` (pending) and **does not** yet update the client debt.
3. The order page now shows the payment in the **Платежи** panel with a yellow "На утверждении" badge.

## Step 4 — Verify

1. Have the cashier open **Finance → Платежи на утверждении**. The new row should appear in the queue.
2. The client's debt panel on `/clients/client` still shows the **old** balance — it changes only after the cashier approves.

## What just happened (under the hood)

`POST /payment/payment/create` (RBAC `operation.payment.create`) inserts one row into `d0_payment` with `STATUS=0`. No ledger entry is written to `d0_client_transaction` yet — that happens in step two, when the cashier flips `STATUS=1` via [Approve a payment as the cashier](./approve-payment-as-cashier.md). See the [payment module](/docs/modules/payment) for the full state machine and the [finans module](/docs/modules/finans) for the ledger model.

## Common mistakes

- **Wrong currency**: the form lets you type any number, but on save it rejects with "Валюта не совпадает с заказом". The order's currency is locked at creation — pick a cashbox in the same currency.
- **Forgetting the photo**: if `enablePaymentPhoto` is on for the tenant, the cashier auto-rejects payments without one and you have to redo the work.
- **Approving your own payment**: agents do not have `operation.payment.approve`. Even if a role is mis-configured to allow this, don't — the audit log flags it and supervisors get a Telegram alert.

## Next steps

- Cashier flow that completes this loop: [Approve a payment as the cashier](./approve-payment-as-cashier.md).
- Adjusting a wrong-amount payment after approval: [finans module — manual correction](/docs/modules/finans).
- Full payment reference: [payment module](/docs/modules/payment).
