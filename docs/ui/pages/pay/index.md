---
title: "Pay — UI pages"
sidebar_position: 1
---

# Pay — UI pages

The **Pay** module is a webhook-only subsystem; it has **no user-facing admin views**.

It exposes three external-callback endpoints used by Uzbek payment providers to settle online orders created via the bot/storefront flow:

| Route | Controller | Purpose |
|---|---|---|
| `/pay/payme/index` | `PaymeController::index` | Payme (Paycom) merchant API receiver — CheckPerformTransaction / CreateTransaction / PerformTransaction / CancelTransaction / CheckTransaction / GetStatement |
| `/pay/click/index` | `ClickController::index` | Click prepare / complete callback (signature-verified) |
| `/pay/apelsin/index` | `ApelsinController::index` | Apelsin notify callback |

Each action reads the raw POST body, persists it to a per-call log file via `Distr::saveFile`, dispatches to the corresponding helper class (`PaymeHelper`, `ClickTransaction`, `ApelsinHelper`), updates the linked `OnlineOrder` (sets `PAY` field, calls `createTransaction()`), and replies with the provider-specific JSON envelope.

There are no GET-served HTML pages, no forms, and no grids to document. Configuration (merchant IDs, secret keys, login credentials) lives in the global params table — see the [Settings module reference](/docs/modules/settings) and the [Params page](../settings/settings_params_index).

## See also

- Module reference: [/modules/pay](/docs/modules/pay)
- Online-order flow: [`OnlineOrder` model](/docs/schema/online-order)
- Routes inventory: [`static/data/routes.json`](/data/routes.json)
