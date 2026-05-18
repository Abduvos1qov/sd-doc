---
title: "Rating UI pages"
audience: All sd-main developers, QA
summary: Index of UI page reference docs for the rating module
topics: [rating, ui, page-index]
---

# Rating UI pages

The `rating` module powers client satisfaction polls. Admins create poll templates with weighted questions, generate per-client share links, and review aggregated star ratings and comments. End clients open a hashed link to submit a star rating plus optional comment without logging in.

## Pages

| Page | Route | Audience |
|---|---|---|
| [Polls list (admin)](./rating_index_index.md) | `/rating/index` | admin / supervisor |
| [Client rating list](./rating_client_index.md) | `/rating/client` | admin / supervisor |
| [Public poll page](./rating_poll_index.md) | `/rating/poll?hash=…` | external clients (no auth) |

## See also

- Module reference: [/modules/rating](/docs/modules/rating)
- Page-to-module map: [/quality/page-to-module-map](/docs/quality/page-to-module-map)
