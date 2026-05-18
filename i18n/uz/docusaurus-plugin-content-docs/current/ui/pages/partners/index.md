---
title: "Partners UI pages"
audience: All sd-main developers, QA
summary: Index of UI page reference docs for the partners module
topics: [partners, ui, page-index]
---

# Partners UI pages

The `partners` module manages the distributor's partner-merchant accounts (role 7). Each partner is a `User` row paired with a `Partner` row that maps the partner to one or more product categories. The module also exposes per-partner debt/payment ("долг" / "оплата") transaction tracking against `ClientTransaction` and `ClientFinans`.

## Pages

| Page | Route | Audience |
|---|---|---|
| [Partners list](./partners_list_index.md) | `/partners/list` | admin / settings manager |
| [Partner transactions overview](./partners_list_transaction.md) | `/partners/list/transaction` | admin / settings manager |
| [Partner transaction detail](./partners_list_detail.md) | `/partners/list/detail/client/<USER_ID>` | admin / settings manager |

## See also

- Module reference: [/modules/partners](/docs/modules/partners)
- Page-to-module map: [/quality/page-to-module-map](/docs/quality/page-to-module-map)
