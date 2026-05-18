---
title: Onboard a B2B customer to the online portal
sidebar_position: 9
audience: End users (admin | sales manager)
summary: Issue portal credentials, flip the online-order flag, and walk through the customer's first cart.
topics: [tutorial, how-to, onlineOrder, clients]
---

# Onboard a B2B customer to the online portal

**You will**: Take an existing wholesale customer, generate a portal login for them, enable self-service ordering, and confirm a first cart-to-order conversion on the dashboard. By the end you will know the standard B2B portal onboarding flow.
**You need**: A user with role 1 or 9 with `operation.clients.update` and `operation.settings.update`; an existing client record (see [Bulk-import clients](./bulk-import-clients.md) if you need one); the tenant's portal URL (typically `https://<tenant>.salesdoctor.io/portal`).
**Time**: ~5 minutes
**Hard parts**:
- The `enableOnlineOrder` flag is a **per-client** setting, not tenant-wide. Many people get tripped up trying to find it in tenant settings.
- The portal uses api4 (a different controller stack from api3 mobile). Permissions errors here will not be in the mobile log.

## Step 1 — Find the client

Open the clients grid (`/clients/client`) and search for the customer by name or INN. Click their row to open the detail page.

## Step 2 — Issue a portal login

On the client detail page, look for the **Онлайн-заказ** or **Портал** tab.

1. Click **Сгенерировать логин**. The system creates a `d0_client_login` row with a random password.
2. The form shows the new login and a one-time password — copy them now, the password is not stored in clear text after the dialog closes.
3. Tick **Активен**.
4. Save. This writes the login row and stamps `d0_client.PORTAL_LOGIN_ID`.

If your build uses a different layout (some tenants embed login under **Контакты**), the underlying flag is the same — look for **enableOnlineOrder** as a per-client toggle.

## Step 3 — Enable online ordering for this client

Still on the client page:

1. Find the **enableOnlineOrder** checkbox (sometimes labelled **Онлайн-заказы разрешены**).
2. Tick it. This writes `d0_client.ENABLE_ONLINE_ORDER=1`.
3. Save.

The client can now sign in to the portal. Their assigned price type (`d0_client.PRICE_TYPE_ID`) is what they will see in the catalog — if it's the wrong one, change it here before they log in.

## Step 4 — Walk the customer through their first cart

Either send the credentials to the customer or shadow them through the first cart.

1. Open the portal URL in a private browser window and sign in.
2. Browse the catalog. Products visible here come from `r_product` filtered by `ACTIVE='Y'` and joined to the customer's price type.
3. Add 1-2 products to the cart and click **Оформить заказ**.
4. The portal calls `POST /api4/order/post`. This writes a row to `d0_order` with `TYPE=3` (online) and `STATUS=0` (pending review by your operator).

## Step 5 — Verify on the web admin

Back in the admin, navigate to **Online orders** (URL: `/onlineOrder/order`).

![Annotated screenshot of the online orders grid](/screens/annotated/onlineOrder_order.annotated.png)

The grid shows the new submission:

1. **Статус** (①) = "Новый". Filter on this if many orders are queued.
2. **Контакт** (②) = the customer's portal login.
3. Use **Поиск** (③) to search by client name or order number.
4. The grid (④) lists every online order with date, amount, line count, and status.

Click the row to review and either **Принять** (convert into a regular `d0_order` for fulfilment) or **Отклонить**.

## What just happened (under the hood)

Two writes turn a regular client into a portal customer: `d0_client_login` (the credentials, password is hashed) and `d0_client.ENABLE_ONLINE_ORDER=1` (the toggle that lets the customer see the catalog and post orders). The portal itself is served by api4 — `OrderController::actionPost` in `protected/modules/api4/controllers/` writes `d0_order` with `TYPE=3`. The admin grid `/onlineOrder/order` is the operator-facing inbox for these. See the [onlineOrder module](/docs/modules/onlineOrder) for the full operator-side workflow and the [integration module](/docs/modules/integration) for the third-party API surface.

## Common mistakes

- **Forgetting the per-client flag**: portal login works but the customer sees an empty catalog. Always pair the login with `ENABLE_ONLINE_ORDER=1`.
- **Wrong price type**: customer logs in and complains the prices are too high. Usually you assigned them the retail price type instead of their negotiated wholesale tier.
- **Letting online orders auto-confirm**: by default they queue for operator review. Tenants that auto-confirm via `enableAutoApproveOnline=1` skip the operator step — which is fine until a customer puts in a 10x quantity by accident.

## Next steps

- Take the portal order and convert it to a real one: [Create your first order from the web admin](./create-order-web.md) (the "Online" tab uses the same form).
- Onboard more customers at once: [Bulk-import clients from Excel](./bulk-import-clients.md).
- Full portal reference: [onlineOrder module](/docs/modules/onlineOrder).
