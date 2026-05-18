---
title: Price type
sidebar_position: 7
audience: All
summary: A named price list (retail, wholesale, special) chosen per order — decides which product price each line uses.
topics: [concept, orders, pricing]
---

# Price type

> **TL;DR** — A **Price type** is a named price list (e.g. *"Retail UZS"*, *"Wholesale USD"*, *"VIP special"*) that an order is built against. Every order has exactly one price type; every product line takes its unit price from that list. Each outlet has a default price type, and the operator can switch it at order-creation time if rules allow.

## What it is

In distribution, the same product is sold at different prices to different customer classes — supermarket chains pay wholesale, end consumers pay retail, VIP partners get a special list. Rather than store a separate price column per channel on the product, SalesDoctor stores a **collection of price lists** (one per price type) and lets the order pick which list to use.

Each price type carries:

- A **name** and a **currency**.
- A **parent** price type, supporting list hierarchies (e.g. *"Wholesale USD"* extending *"Wholesale base"*).
- A **hand-edit** flag (`HAND_EDIT`) — does this list allow the operator to override a unit price manually?
- A **for client** flag — is this list assignable to outlets, or only used internally?
- A `FILIAL` / `DILER` scope — some lists are filial-specific.

## Why it matters

The price type drives:

- **Order totals** — picking the wrong list silently changes revenue.
- **Discount eligibility** — automatic discount rules can match by price type.
- **Bonus eligibility** — bonus rules likewise.
- **Currency** — `Order.PRICE_TYPE` carries the currency through to the ledger.
- **Reports** — sales reports pivot by price type to compare channels.

For QA: when a price seems "wrong" on an order, the first question is *which price type is on the order*, not *what's the product price*.

## How SalesDoctor models it

| Layer | Identifier | Where |
|---|---|---|
| Model | `PriceType` | `protected/models/PriceType.php` |
| Table | `d0_price_type` | 24 columns |
| FK on outlet | `Client.PRICE_TYPE_ID` | Outlet's *default* price type |
| FK on order | `Order.PRICE_TYPE`, `Order.OLD_PRICE_TYPE` | Active list + override history |
| FK on KPI | `KpiTaskTemplate.PRICE_TYPE` | KPI filter |
| Hand-edit | `PriceType.HAND_EDIT` | Allows manual price overrides on lines |
| QA workflow | [Price types](../quality/settings/price-types) | Operator-side guide |

Key columns on `d0_price_type`: `PRICE_TYPE_ID, NAME, CURRENCY, PARENT, TYPE, FOR_CLIENT, OLD_PRICE_TYPE, FILIAL, DILER, DESCRIPTION, SORT, ACTIVE, HAND_EDIT`.

The actual unit prices live in a **separate** product-price table — the `PriceType` row is just the list's identity.

## Example

A dealer might run these price types in one filial:

| PRICE_TYPE_ID | NAME | CURRENCY | HAND_EDIT |
|---|---|---|---|
| 1 | Retail UZS | UZS | 0 |
| 2 | Wholesale UZS | UZS | 0 |
| 3 | VIP — Hand-edit | UZS | 1 |
| 7 | Wholesale USD | USD | 0 |

An outlet with `PRICE_TYPE_ID = 2` defaults to *Wholesale UZS* on new orders. The operator may switch to *VIP* (3) if their role permits; *VIP* allows the operator to type unit prices directly per line because `HAND_EDIT = 1`.

## Common confusions

| Looks like | But actually |
|---|---|
| Just a currency | Currency is one *property* of the price type — but two lists in the same currency may have totally different prices. |
| The product price | Product price = (price-type, product) cell. The PriceType row is only the list header. |
| Discount rule | A discount **modifies** a chosen price-type price; the price type itself doesn't carry discount logic. |
| Price type is static | Operators can switch the price type on an order at creation time (if RBAC allows), and the change is logged in `OLD_PRICE_TYPE`. |

## Related concepts

- [Outlet](./outlet.md) — carries the default `PRICE_TYPE_ID`.
- [Bonus vs discount](./bonus-vs-discount.md)
- [Price types — QA workflow](../quality/settings/price-types)
- [Server toggles](../quality/settings/server-toggles-and-period-close) — `appAllowPriceTypes`, `allowManualPriceForAgent`.
- [Orders module reference](../modules/orders)
