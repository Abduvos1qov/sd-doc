---
sidebar_position: 10
title: Discounts, bonuses & catalog
---

# Configure discounts, bonuses & catalog

Pricing logic lives in three places: **discount rules** (Скидки), **bonus rules** (Бонусы), and the **product catalog** itself (which carries unit prices and brand/category info).

## Step 1 — Set up discount rules

Open **Настройки → Скидки** (Settings → Discounts), or `/settings/skidka`:

![Discount rules list](/screens/guide/54-settings-discounts.webp)

Each rule defines: who gets the discount (client category, channel, agent), on what (product / category), and how much (% or fixed amount).

Click **+ Добавить** to create a rule. Common patterns:
- "5% off for all Supermarket-channel clients on Beverages"
- "Fixed 10,000 UZS off when Client Category = A"
- "Agent-specific quota — agent X has 50,000 UZS discount budget this month"

## Step 2 — Set up bonus rules (buy-X-get-Y)

Open **Настройки → Бонусы** (Settings → Bonuses), or `/settings/bonus`:

![Bonus rules list](/screens/guide/55-settings-bonus.webp)

Bonus rules are "buy N of product X, get M of product Y free." Examples:
- "Buy 10 Coca-Cola 0.5L, get 1 free"
- "Buy 100,000 UZS worth of Brand X, get a free poster"
- "Buy 5 units across category Beverages, get 1 unit of category Snacks free"

Both rules apply automatically during order capture — agents don't have to remember which promo is running today.

## Step 3 — Sales channels

Open **Настройки → Канал сбыта** (Settings → Sales channel), or `/settings/channel`:

![Sales channels](/screens/guide/56-settings-channel.webp)

Channels classify your clients: small shop / supermarket / restaurant / kiosk / cafe / etc. The channel:
- Drives discount and bonus eligibility (above)
- Filters reports
- Determines visit-plan frequency (some channels are visited weekly, others bi-weekly)

Add the channels your business needs — usually 4–8 is enough.

## Step 4 — Brands

Open **Настройки → Бренд** (Settings → Brand), or `/settings/brand`:

![Brands](/screens/guide/58-settings-brand.webp)

A **brand** is a product family with a single logo / marketing identity (e.g. "Coca-Cola", "Nestlé Nesquik"). The brand:
- Groups products in the catalog
- Slices reports ("by brand")
- Drives MML rules ("must-match list" — every shop must carry at least 3 SKUs of Brand X)

## Step 5 — Products catalog

Open **Настройки → Товары** (Settings → Products), or `/settings/product`:

![Products catalog](/screens/guide/57-settings-products.webp)

Every product needs:
- Name (Russian, Uzbek if relevant)
- Brand
- Category (food / drinks / hygiene / etc.)
- Unit of measure (piece, box, kg, litre)
- Barcode (for scanning on mobile)
- Default price (per price type)

Bulk-import from Excel is supported — your administrator does this once during setup.

## Tips

- **Start simple** — define 5–10 discount rules, not 50. Complex pricing confuses everyone.
- **One bonus per category** — overlapping bonuses on the same product cause math arguments.
- **Brand naming consistency** — "Coca-Cola" vs "Coca Cola" vs "CocaCola" will be three different brands in reports.

---

**Next:** [Create your first order →](../daily-use/first-order)
