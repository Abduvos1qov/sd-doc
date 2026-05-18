---
title: Outlet (a.k.a. client / customer)
sidebar_position: 2
audience: All
summary: The retail store an agent visits. The Client row in sd-main covers both the legal customer and the physical outlet — they're conflated by design.
topics: [concept, clients]
---

# Outlet — the place an agent visits

> **TL;DR** — An **Outlet** is a retail point of sale that a field agent calls on: one shop, one address, one geocoded pin. In sd-main the database row is called `Client` (`d0_client`). The same row also stores the legal customer identity, so "outlet" and "customer" are conflated in the schema.

## What it is

In distribution terminology:

- **Outlet** = the *physical* shop the agent walks into (one storefront, one set of GPS coordinates).
- **Customer** = the *legal entity* that owns the outlet — often a multi-store retailer.

SalesDoctor's schema does not separate the two. Each row in `d0_client` carries both the shop attributes (`ADRESS`, `LAT`, `LON`, `ORIENT`) and the customer attributes (`FIRM_NAME`, `CLIENT_CAT`, `PRICE_TYPE_ID`, `BALANS`). If one customer owns three physical stores, the convention is **three Client rows**, distinguished by name suffix or `XML_ID` linkage to the source system.

The Russian UI labels these screens *Клиенты* (Clients). Internally and in this documentation we use **outlet** when emphasising the visit / geolocation aspect, and **client** when emphasising the financial / contractual aspect.

## Why it matters

The outlet is the *atomic unit of the route*: every visit, every order, every defect, every audit attaches to one outlet. KPI metrics like [AKB](./akb.md) and OKB count distinct outlet ids, not legal entities.

For business:
- Sales reports are sliced by outlet.
- GPS geofencing checks the agent stood within range of the outlet's `LAT`/`LON`.
- The outlet's `PRICE_TYPE_ID` decides which price list applies to its orders.
- The outlet's `BALANS` is the running customer debt.

## How SalesDoctor models it

| Layer | Identifier | Where |
|---|---|---|
| Table | `d0_client` | Model `Client` (`protected/models/Client.php`) |
| Parent class | `BaseFilial` | Auto-scoped by `FILIAL_ID` |
| Primary key | `CLIENT_ID` | Used by every order / visit / defect row |
| Geolocation | `LAT`, `LON`, `ORIENT` | Used for geofence and map views |
| Pricing | `PRICE_TYPE_ID`, `BONUS_ID`, `DISCOUNT_ID` | Defaults applied to new orders |
| Categorisation | `CLIENT_CAT`, `CLIENT_CHANNEL`, `CLIENT_CLASS` | Drives report grouping and KPI eligibility |
| Balance | `BALANS`, `ALLOW_CONSIG` | Running debt + consignment flag |

The full 52-column row is documented in [the Clients module reference](../modules/clients).

## Example

```sql
-- One outlet in Tashkent, owned by firm "Korzinka", category 2:
SELECT CLIENT_ID, FIRM_NAME, NAME, ADRESS, LAT, LON, CLIENT_CAT, PRICE_TYPE_ID, BALANS
FROM d0_client
WHERE FILIAL_ID = 1 AND CITY = 'Tashkent' AND CLIENT_CAT = 2
ORDER BY FIRM_NAME LIMIT 5;
```

A typical row:

| CLIENT_ID | FIRM_NAME | NAME | LAT | LON | BALANS |
|---|---|---|---|---|---|
| 14823 | Korzinka | Korzinka Yunusabad-3 | 41.3625 | 69.2871 | -1 250 000 |

(Negative `BALANS` = the outlet owes the dealer.)

## Common confusions

| Looks like | But actually |
|---|---|
| Customer = Outlet | Conflated by schema; in real life one customer may own several outlets, each a separate Client row. |
| Legal entity record | `d0_client` is *not* normalised; legal-entity data (TIN, registration) lives on the same row, not a separate table. |
| `d0_filial_client` | A linking table that maps outlets to *other* filials, used for cross-filial visibility — not the primary outlet row. |
| `Contragent` | A separate legal counterparty record used by some accounting integrations; not the same as Client. |

## Related concepts

- [Filial](./filial.md) — outlets are scoped to one filial via `FILIAL_ID`.
- [Visit](./visit.md) — every agent-outlet interaction.
- [AKB](./akb.md) — active outlet count.
- [Price type](./price-type.md) — pinned to the outlet.
- [Clients module reference](../modules/clients)
