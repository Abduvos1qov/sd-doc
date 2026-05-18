---
title: Approve a payment as the cashier
sidebar_position: 8
audience: End users (cashier)
summary: Open the pending-payments queue, review evidence, approve, and watch the cashbox and client debt change.
topics: [tutorial, how-to, payment, finans]
---

# Approve a payment as the cashier

**You will**: Open the queue of payments registered by agents, verify each one against the receipt/photo evidence, approve them so the cashbox balance moves and the client debt shrinks. By the end you will know the cashier-side half of the agent → cashier hand-off.
**You need**: A user with role 5 (cashier) or 1/9 (admin) with `operation.payment.approve`; one or more payments queued by agents — see [Register a payment from an agent](./register-payment.md).
**Time**: ~30 seconds per payment
**Hard parts**:
- Approving puts the row into the ledger **immediately** — there is no "undo". A wrong approval needs a manual correction in finans, which is messy.
- The cashbox the payment was registered against must be one you have access to; otherwise the row is invisible to you.

## Step 1 — Open the pending queue

Navigate to **Finance → Платежи на утверждении** (URL: `/payment/payment/pending` or similar, depending on tenant build).

The grid lists every payment row with `STATUS=0`. Columns:

| Column | What |
|---|---|
| **Дата** | When the agent registered the payment |
| **Агент** | Who registered it |
| **Клиент** | Who paid |
| **Заказ №** | Linked order |
| **Сумма** | Amount in the order's currency |
| **Способ** | Cash / card / transfer |
| **Касса** | Target cashbox |
| **Фото** | Receipt photo if attached |

Filter by **Агент** or **Касса** to scope the queue if it is long.

## Step 2 — Review evidence

For each pending payment, before clicking approve:

1. Click the row to open the detail panel.
2. Match **Сумма** against the order's outstanding amount. If the agent over-collected (paid more than due), this is fine — it creates a credit on the client.
3. Look at the **Фото** — does it match the printed receipt for that amount?
4. Read the **Комментарий**. If it is empty or unclear, do not approve — message the agent.

## Step 3 — Approve

1. With the row open, click **Утвердить**.
2. The page posts to `POST /payment/payment/approve`. Inside one DB transaction the controller:
   - Sets `d0_payment.STATUS=1` (approved) and stamps `APPROVED_BY` + `APPROVED_DATE`.
   - Inserts a row into `d0_client_transaction` reducing the client's `BALANCE` by the payment amount.
   - Inserts a row into `d0_cashbox_transaction` increasing the cashbox balance.
   - If the payment fully closes the order's outstanding, updates `d0_order.STATUS` to **Оплачен** (`STATUS=5` or as configured).
3. The row leaves your queue and is now visible (with green tick) on the client's transaction history and the cashbox ledger.

For ambiguous rows, use **Отклонить** instead. This sets `STATUS=2` (rejected) and notifies the agent — they can register again with a corrected amount.

## Step 4 — Verify the side-effects

1. Open the client (URL: `/clients/client/view?id=<clientId>`) and look at **Остаток** (balance). It should now be lower by the payment amount.
2. Open the cashbox (URL: `/settings/cashbox` → click the target cashbox). The balance should be higher by the same amount.
3. Open the source order — if the payment fully closed it, status should now be **Оплачен**.

## What just happened (under the hood)

`PaymentController::actionApprove` (RBAC `operation.payment.approve`) writes three things inside one transaction:

| Write | Table | Effect |
|---|---|---|
| Update | `d0_payment` | `STATUS=1`, stamp `APPROVED_BY`/`APPROVED_DATE` |
| Insert | `d0_client_transaction` | Reduce client debt (`AMOUNT` negative) |
| Insert | `d0_cashbox_transaction` | Increase cashbox balance (`AMOUNT` positive) |

If any of these fail, the whole transaction rolls back — you will not get a "half-approved" payment. See [payment module](/docs/modules/payment) for the full state machine and [finans module](/docs/modules/finans) for the ledger model.

## Common mistakes

- **Approving without looking at the photo**: agents make typos. A 1,000,000 vs 100,000 mistake is a quick way to corrupt your monthly close.
- **Approving across cashboxes**: if the agent registered to "Касса А" but their cash was deposited into "Касса Б", you cannot fix that here — reject and have them re-register.
- **Wrong currency hiding under the row**: USD payments to UZS orders appear identical at a glance. The currency badge is in small grey next to the amount.

## Next steps

- The agent side of this flow: [Register a payment from an agent](./register-payment.md).
- Daily cash close: [finans module — settlement](/docs/modules/finans).
- Full payment reference: [payment module](/docs/modules/payment).
