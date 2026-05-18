---
title: Cashier — start here
sidebar_position: 5
audience: Cashier
summary: Approves and rejects incoming payments. Reconciles cashboxes against the ledger.
topics: [role-landing]
---

# Welcome, Cashier

You are role **6**. Your job is the money in: every payment an expeditor or agent reports lands in your queue, and your approval is what turns it into a `TRANS_TYPE = 3` (payment receipt) row in the client's ledger. You also reconcile cashboxes — the named tills that the dealer uses (cash, card, bank account) — and flag mismatches.

You see all payment events for your filial. You do not approve orders themselves, you do not edit prices, and you do not touch period close.

## In your first 5 minutes

- [Payment module reference](../modules/payment) — the data layer.
- [Payment approval (QA)](../quality/payment/payment-approval) — the day-to-day flow.
- [Cashbox management](../quality/settings/cashbox-management) — the till definitions.

## Daily tasks

| Task | Where in the admin | Tutorial |
|------|-------------------|----------|
| Approve an incoming payment | `/finans/payment` | [Approve a payment as cashier](../tutorials/approve-payment-as-cashier) |
| Reject a suspect payment | `/finans/payment` → row | [Payment approval](../quality/payment/payment-approval) |
| Reconcile a cashbox balance against expected | `/finans/cashbox` | [Cashbox balance](../quality/finans/cashbox-balance) |
| Apply a manual ledger correction | `/finans/correction` | [Manual correction](../quality/finans/manual-correction) |
| Register a one-off payment from the web | `/finans/payment/new` | [Register a payment](../tutorials/register-payment) |
| Watch a client's running debt | `/finans/client` | [Client debt view](../quality/finans/client-debt-view) |
| Settle a closed order vs payment | `/finans/settlement` | [Settlement](../quality/finans/settlement) |
| Inspect expense / P&L rows | `/finans/expenses` | [Expenses and PnL](../quality/payment/expenses-and-pnl) |

## Reference

- [Payment module](../modules/payment)
- [Finans module (ledger)](../modules/finans)
- [Transaction types](../quality/finans/transaction-types) — TRANS_TYPE codes.
- [Multi-currency](../quality/finans/multi-currency)
- [RBAC permission matrix](../security/rbac)

## Common gotchas

- **Every paid order has *two* ledger rows.** `TRANS_TYPE = 1` (invoice — created when the order is placed) plus `TRANS_TYPE = 3` (payment receipt — created when you approve). Missing either is a bug.
- **Period close locks corrections.** A manual correction to a closed period requires admin override; you can't apply it directly.
- **Cashbox is per-expeditor.** Each expeditor has their own cashbox assignment — a payment recorded against the wrong cashbox reconciles wrong.
- **Currency on the cashbox is fixed.** Don't accept multi-currency payments into a single-currency cashbox — they'll convert at the wrong rate.
- **Approving a payment does not affect order status.** The order moves on its own status flow; payment is just a ledger event.

## Glossary terms you'll meet

- [Outlet](../concepts/outlet)
- [Period close](../concepts/period-close)
- [Price type](../concepts/price-type) — affects the currency on the invoice.
- [Defect vs reject](../concepts/defect-vs-reject) — both affect the debt you reconcile.
- [Bonus vs discount](../concepts/bonus-vs-discount) — bonuses don't generate revenue rows; discounts shrink them.
- [Filial](../concepts/filial)
