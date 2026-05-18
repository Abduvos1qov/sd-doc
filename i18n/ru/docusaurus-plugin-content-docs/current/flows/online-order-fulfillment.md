---
sidebar_position: 2
title: Online order fulfillment (portal / Telegram bot)
audience: All
summary: B2B portal and Telegram-bot orders, from catalog browse through optional online prepayment to delivery. Crosses onlineOrder, pay (Payme/Click/Apelsin webhooks), api4 (B2B API), orders, vs, finans, integration (Telegram), and notification.
topics: [flow, onlineOrder, pay, gateway, integration, telegram, api4, orders, finans, payment]
---

# Online order fulfillment (portal / Telegram bot)

> **TL;DR** — A client signs in to the **online portal** or opens the **Telegram WebApp bot**, browses the catalog, builds a cart, and submits. Optionally they prepay through **Payme**, **Click**, or **Apelsin**. Each gateway hits a webhook in `protected/modules/pay/controllers/`, which verifies the signature, applies idempotency on the transaction id, and credits the order. The order is mirrored to a regular `Order` row, joins the same delivery flow as a mobile order, and the Telegram bot streams status updates back to the client. The trunk delivery, finans, and payment phases reuse the canonical [order end-to-end](/docs/flows/order-end-to-end) flow — this page covers only the **online-only** segments.

## Purpose

A retail client (a supermarket buyer, a pharmacy purchasing manager, a HoReCa procurement officer) doesn't want to wait for a sales agent's next visit. They open a browser bookmark or a Telegram bot, log in with their phone number, browse the same catalog the agents see, and place an order themselves. The order might be paid up-front via a Uzbek payment gateway, or marked for cash-on-delivery. Either way it lands in the same office *Orders* list as any agent-placed order, joins a delivery trip, and is fulfilled by the same expeditor.

This flow exists for three reasons: it cuts the agent's call/visit cost, it lets clients order outside business hours, and it gives the distributor a B2B portal that competes with marketplace apps. The Telegram WebApp variant is dominant in markets where the client base lives inside Telegram rather than browsers.

## Modules involved

| Module | What it does in this flow | Key file path |
| --- | --- | --- |
| `onlineOrder` | Portal frontend; catalog, cart, checkout, order history, Telegram bot bridge | `protected/modules/onlineOrder/controllers/` |
| `api4` | B2B API used by both the portal frontend and the bot — read catalog, post order, query status | `protected/modules/api4/controllers/` |
| `pay` | Gateway-specific webhook controllers (Payme, Click, Apelsin) with signature verification and idempotency | `protected/modules/pay/controllers/` and `protected/modules/pay/components/` |
| `api4/OnlinePaymentController` | Aggregator endpoint for Payme-Go, OptimaQR, OdEngi, Kaspi — used by the bot WebApp | `protected/modules/api4/controllers/OnlinePaymentController.php` |
| `orders` | Receives the mirrored `Order` row once payment is authorized (or COD selected); same state machine as offline orders | `protected/modules/orders/` |
| `stock` / `vs` | Validates availability at cart-build time and reserves on order confirm | `protected/modules/stock/`, `protected/modules/vs/` |
| `finans` | Posts the order debit on delivery (same path as offline) and the gateway credit on webhook | `protected/modules/finans/` |
| `integration` (Telegram) | Bot worker; receives webapp callbacks, sends status push messages | `protected/modules/integration/` and `onlineOrder/controllers/Telegram*` |
| `payment` | Cashier-side approval queue if cash is involved (COD or partial cash) | `protected/modules/payment/controllers/ApprovalController.php` |
| `sms` / notification | Confirmation SMS / Telegram message when the order is accepted, dispatched, delivered | `protected/modules/sms/`, `Order::notifyInoutReporter()` |

Cross-references — modules: [onlineOrder](/docs/modules/onlineOrder), [pay](/docs/modules/pay), [integration](/docs/modules/integration). API: [api v4 — online-payment](/docs/api/api-v4-online/online-payment). Trunk flow: [order end-to-end](/docs/flows/order-end-to-end).

## End-to-end sequence

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant Web as Portal / Telegram WebApp
    participant API4 as api4<br/>Catalog + Order
    participant Online as onlineOrder<br/>OrderController
    participant Gateway as Gateway<br/>Payme / Click / Apelsin
    participant Pay as pay<br/>webhook
    participant Orders as orders<br/>Order::save
    participant Hook as Order::afterSave
    participant Stock as stock + vs
    participant Finans as finans<br/>ClientTransaction
    participant Bot as Telegram bot<br/>(integration)
    participant Office as Office UI
    actor Expeditor

    Client->>Web: Sign in (phone + OTP / Telegram auth)
    Web->>API4: GET catalog, prices, stock
    Client->>Web: Build cart, pick delivery slot
    Web->>API4: POST /api4/order (intent=draft)
    API4->>Online: Create OnlineOrder (STATUS pending)

    alt Prepay via gateway
        Web->>Gateway: Redirect / open invoice
        Client->>Gateway: Enter card / scan QR / pay
        Gateway-->>Pay: Webhook (CheckPerform / Create / Perform)
        Pay->>Pay: Verify signature, dedupe by tx_id
        Pay->>Online: Mark OnlineOrder paid
        Pay->>Finans: Credit gateway-side payment
    else Cash-on-delivery
        Online->>Online: Mark COD; no gateway round-trip
    end

    Online->>Orders: Create Order row (STATUS=1, SOURCE=online)
    Orders->>Stock: Reserve lines
    Orders->>Hook: afterSave (new)
    Hook->>Bot: Push "order accepted" to client
    Hook->>Online: onOrderChange (rerender state)

    Note over Office,Expeditor: Same trunk flow from here on
    Office->>Orders: Assign trip, expeditor
    Expeditor->>Orders: Deliver (STATUS 1/2 → 3)
    Orders->>Hook: afterSave (status change)
    Hook->>Finans: Debit on delivery
    Hook->>Bot: Push "delivered" to client
    Hook->>Online: onOrderChange

    alt Refund / cancel
        Office->>Online: Cancel + refund flag
        Online->>Pay: Initiate refund (gateway API)
        Pay->>Gateway: Refund call
        Gateway-->>Pay: Webhook (refund confirmed)
        Pay->>Finans: Reversing entries
    end
```

## Phase-by-phase narrative

### Phase 1 — Client sign-in and catalog browse

**Who triggers:** the client, in a web browser, in the Telegram WebApp (button inside a chat), or via direct bot commands.

**What happens:** the portal uses the same backend as the mobile agent app — `api4` exposes catalog, prices, current stock, must-buy rules, recommended sales, and the per-client price-type override. Auth is by phone-number OTP (`api4/login`) or, in the Telegram path, by the Telegram `initData` signed payload that the bot worker validates against `BOT_TOKEN`. A successful auth resolves a `{{client}}` row and caches a session token.

The client sees only their own price type, their own credit limit (if enforced), and the subset of products their distributor has marked visible-online (`Product.SHOW_ONLINE` or similar flag).

**Where the state lives:** session token in client storage; no order row yet.

See also: [onlineOrder module](/docs/modules/onlineOrder), [tutorial — set up the online portal](/docs/tutorials/set-up-online-portal).

### Phase 2 — Cart build and draft submission

**Who triggers:** the client, by tapping *Add to cart* / *Checkout*.

**What happens:** the client adds items, picks quantities, optionally applies a promo code, picks a delivery slot. When they submit, the client receives an `OnlineOrder` row with `STATUS = pending` (or similar draft state) — this is the **portal-side** record. It is **not** the same as the offline `Order` row yet. The split lets the portal hold the cart through a gateway round-trip without polluting the operational `orders` lists with half-paid intents.

`onlineOrder/OrderController::actionUpdate` and the corresponding api4 endpoint validate cart math, re-check stock availability, and apply price-type / discount rules before persisting the `OnlineOrder` row.

**Where the state lives:** `{{online_order}}` row with `CONTACT_ID`, line array, total, payment-method choice, optional gateway-tx placeholder.

### Phase 3 — Online prepayment via gateway (optional branch)

**Who triggers:** the client picking *Pay online* and a specific gateway.

**What happens:** the portal redirects to (or opens an in-WebApp invoice for) the chosen provider:

- **Payme** — invoice URL with `m=<merchant_id>` and `ac.order_id=<online_order_id>`. The Payme JSON-RPC merchant API then calls back into `pay/payme/index` with `CheckPerformTransaction`, `CreateTransaction`, `PerformTransaction`, `CancelTransaction`, `CheckTransaction`, `GetStatement` methods. `PaymeHelper::run()` dispatches each method, **verifies the Basic-Auth merchant token**, looks up the corresponding `OnlineOrder` by `order_id`, refuses requests for unknown / wrong-amount orders, and is idempotent on `tx_id`.
- **Click** — Click Pass / Click Up flow. Webhook hits `pay/click/index`. Signature is the MD5 of `(click_trans_id, service_id, secret_key, merchant_trans_id, amount, action, sign_time)` — `ClickHelper` recomputes and compares.
- **Apelsin** — `pay/apelsin/index` with `ApelsinHelper`. Validates HMAC over the JSON body.

Each helper writes a **gateway-side log** (`Distr::saveFile`) before processing, so a disputed callback can be replayed offline. On a successful `PerformTransaction` (or equivalent), the helper:

1. Marks the `OnlineOrder.PAID` flag / sets a `GATEWAY_TX_ID`.
2. Posts a credit row to finans tagged with the gateway (`ClientTransaction` with `SOURCE = payme|click|apelsin`).
3. Triggers the order materialization step (Phase 4).

The **api4-aggregator** path (`api4/online-payment/payme-pay`, `api4/online-payment/optima-qr`, etc.) is used by the Telegram WebApp — it consolidates pay-intent creation across multiple gateways behind one API surface. The webhook side still goes to the per-gateway module.

**Where the state lives:** `{{online_order}}.PAID = 1`, `{{online_order}}.GATEWAY_TX_ID` set, `{{client_transaction}}` credit row for the prepayment.

API reference: [api v4 — online-payment](/docs/api/api-v4-online/online-payment).

### Phase 4 — Materialization as a real Order

**Who triggers:** either the successful gateway webhook (prepaid path) or the immediate confirm step (COD path).

**What happens:** `onlineOrder` creates a new `Order` row keyed to the `OnlineOrder` via the `ORDER_ID` join column. The `Order` is born at `STATUS = 1` (New) with `SOURCE = online` (so reports can split portal-originated from agent-originated). `OnlineOrder.ORDER_ID` is back-filled.

From this moment on the order is **identical** to any agent-captured order:

- `Order::afterSave()` runs (new-record branch): stock is reserved (or vs-deducted for van-flow online orders, which is rare but supported), a finans debit is created if `debtNewOrder` is on, `OrderHistory` rows are appended.
- The deferred `AfterResponse::run` block fires `OnlineOrderController::onOrderChange` so the portal/bot sees the new state, fires `notifyInoutReporter` so supervisor channels see it, and pushes to SD-integration for ERP.

**Where the state lives:** a `{{order}}` row with `SOURCE = online`, linked to the originating `{{online_order}}` row, plus the usual `{{order_detail}}` lines and `{{order_history}}` audit row.

See also: [order end-to-end](/docs/flows/order-end-to-end) — Phases 2 and 3 of the trunk flow.

### Phase 5 — Office assignment, dispatch, delivery

**Who triggers:** the operator (same as the trunk flow), then the expeditor.

**What happens:** identical to Phases 4 and 5 of the [order end-to-end](/docs/flows/order-end-to-end) flow. The operator slots the order onto a trip, the trip dispatches, the expeditor delivers, `STATUS` walks 1 → 2 → 3, `Order::afterSave()` updates finans on the 2 → 3 transition.

The only online-specific behavior is in `Order::afterSave()`'s `AfterResponse::run` block — when it detects `$onlineOrder` is non-null, it calls `OnlineOrderController::onOrderChange($onlineOrder)`, which:

1. Re-renders the client-facing status card.
2. Pushes a Telegram update via the bot worker (*Your order is on the way*, *Your order has been delivered*).
3. Awards loyalty bonus points via `OnlineOrder::loyaltyBonus()` if the order completed.

**Where the state lives:** `{{order}}.STATUS = 3`, `{{order}}.DATE_DELIVERED` set, `{{order_history}}` updated; `{{online_order}}` mirror gets `BONUS` columns populated.

### Phase 6 — Settlement (mixed prepay / cash / credit)

**Who triggers:** depends on payment mode chosen at checkout.

**What happens:**

- **Fully prepaid online.** Phase 3 already credited finans. On delivery, the order's debit (Phase 5) exactly cancels the earlier credit; `Order.DEBT` lands at 0. No cashier action needed.
- **Cash on delivery.** The expeditor collects cash at the door. The expeditor app records the payment row (same approval flow as an agent-collected payment), which lands in the cashier's *Approval* queue. Cashier confirms; finans gets the credit; `Order.DEBT` reduces.
- **B2B credit (no payment at delivery).** The order rides as an open AR debit. The client clears it in a later session — either an online payment (which then takes the gateway path again), a bank wire imported into the approval queue, or a cash visit to the kassa.
- **Partial prepay.** The remaining balance behaves like one of the above three.

**Where the state lives:** `{{client_transaction}}` debits and credits, `{{order}}.DEBT` recomputed.

See also: [payment lifecycle](/docs/concepts/payment-lifecycle), [order end-to-end — Phase 8](/docs/flows/order-end-to-end).

### Phase 7 — Telegram bot status push

**Who triggers:** `Order::afterSave()` → `AfterResponse::run` block, on every status change of an online-sourced order.

**What happens:** the integration module's bot worker holds the persistent connection to Telegram. `onOrderChange` formats a localized status message (Uzbek/Russian) from the order summary and the new status, looks up the linked `{{contact}}` row's `CHAT_ID`, and sends the message. The bot also handles inbound: when the client replies with a quick command (*track*, *cancel*, *repeat*), the bot worker routes to `onlineOrder/Telegram*` handlers which read the current order and either respond inline or open the WebApp at the right screen.

The webapp-bot variant (`WebappBotController`, `onlineOrder/controllers/WebAppController`) exposes the same catalog inside a Telegram WebApp panel — same backend, no separate frontend.

**Where the state lives:** outbound only; the inbound side may modify the `{{online_order}}` row (e.g. cancel).

See also: [integration module](/docs/modules/integration).

## State changes

| Phase | Order.STATUS | OnlineOrder state | Gateway state | Finans state |
| --- | --- | --- | --- | --- |
| 1. Sign-in / browse | n/a | n/a | n/a | unchanged |
| 2. Cart submit (draft) | n/a | pending | n/a | unchanged |
| 3a. Gateway started | n/a | pending | tx created | unchanged |
| 3b. Gateway succeeded | n/a | paid | tx perform-confirmed | credit posted (prepay) |
| 3c. Gateway failed | n/a | pending or cancelled | tx cancelled | unchanged |
| 4. Materialized | 1 (New) | paid or COD | tx settled (if any) | unchanged or debit posted (if `debtNewOrder`) |
| 5a. Loaded | 2 (Shipped) | paid or COD | settled | unchanged |
| 5b. Delivered | 3 (Delivered) | paid or COD | settled | debit posted (delivery), netted vs Phase 3 credit |
| 6a. COD cash approved | 3 (Delivered) | settled | n/a | credit posted, Order.DEBT reduced |
| 6b. Refund | 5 (Cancelled) or partial | refund pending then refunded | refund call confirmed | reversing entries |

## Failure modes and recovery

**Gateway signature fails.** The webhook handler returns the gateway-defined error code (Payme: `-32504`, Click: error `-1`). The gateway retries on its own schedule. No DB write happens, no order is materialized — the client's bank shows *transaction pending* and either auto-cancels or the operator resolves manually.

**Gateway succeeds but our webhook handler crashes mid-flight.** Idempotency by `GATEWAY_TX_ID` makes the next retry safe — the helper sees the existing `OnlineOrder.GATEWAY_TX_ID` and either skips or completes the materialization step. The `Distr::saveFile` log preserves the raw payload for replay if needed.

**Gateway timeout (network).** The portal shows *Payment pending* and polls `CheckTransaction` (Payme) or the equivalent on Click/Apelsin to learn the truth. If the gateway has accepted the money but the webhook hasn't fired in 5 minutes, the operator can manually trigger the materialization step from the back office — same idempotency guards apply.

**Client cancels mid-checkout (browser closed before gateway).** The `OnlineOrder` row sits in `pending` indefinitely; a sweeper job auto-cancels rows older than N hours (configurable per tenant). No stock is reserved at this phase, so nothing leaks.

**Stock-out between cart-build and confirm.** Phase 2 re-checks availability; if a line is no longer satisfiable, the portal surfaces the per-line `left = $available` warning and asks the client to adjust. If discovered at Phase 4 materialization, the order is held in `pending` and an operator splits or partially fulfills it.

**Prepaid order cancelled by the operator before dispatch.** Operator marks the underlying `Order` as cancelled (`STATUS = 5`). The `onlineOrder` post-process fires a refund via the gateway helper (`PaymeHelper::cancelTransaction` / Click `cancel` / Apelsin refund). On success, finans posts reversing entries; on failure, the row stays *refund pending* and accounting follows up manually.

**Telegram push failure.** The bot worker retries with exponential backoff; the message is dropped after N attempts and reported via `ErrorReporter::sendMessage`. The order itself is unaffected — the status DB write has already happened.

**Duplicate gateway callback (the gateway is buggy).** All three helpers gate on `tx_id` — a duplicate `PerformTransaction` returns the original receipt without re-crediting finans. The dedupe is enforced by a unique index on `(SOURCE, GATEWAY_TX_ID)` in the client-transaction table.

**B2B credit limit exceeded.** Cart-build validation blocks submit when the projected open balance would exceed the client's `CREDIT_LIMIT` (if enforced for online orders by tenant setting). The client sees an inline error and must reduce the cart or prepay.

**Refund where the gateway only supports same-day reversal.** If the cancel window has passed, the operator records a manual *refund-to-bank-wire* row in finans and works the refund offline; the gateway-side tx stays settled, the client-side balance is squared via a manual credit.

## See also

- Modules: [onlineOrder](/docs/modules/onlineOrder), [pay](/docs/modules/pay), [integration](/docs/modules/integration), [orders](/docs/modules/orders), [stock](/docs/modules/stock), [vs](/docs/modules/vs), [finans](/docs/modules/finans), [payment](/docs/modules/payment), [sms](/docs/modules/sms)
- API: [api v4 — online-payment](/docs/api/api-v4-online/online-payment)
- Concepts: [payment lifecycle](/docs/concepts/payment-lifecycle), [trip lifecycle](/docs/concepts/trip-lifecycle), [bonus vs discount](/docs/concepts/bonus-vs-discount)
- Tutorials: [set up the online portal](/docs/tutorials/set-up-online-portal), [approve payment as cashier](/docs/tutorials/approve-payment-as-cashier), [register payment](/docs/tutorials/register-payment)
- Trunk flow: [order end-to-end](/docs/flows/order-end-to-end)
