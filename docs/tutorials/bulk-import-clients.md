---
title: Bulk-import clients from Excel
sidebar_position: 7
audience: End users (admin | data-entry)
summary: Download the template, fill three rows, upload, review row-level errors, and commit.
topics: [tutorial, how-to, clients]
---

# Bulk-import clients from Excel

**You will**: Download the import template, fill in three test rows, upload the file, fix any per-row validation errors, and commit the import so the new clients appear on the clients grid. By the end you will know the standard onboarding-from-spreadsheet flow.
**You need**: A user with role 1 or 9 with `operation.clients.create`; Excel (or LibreOffice Calc); knowledge of which **Категория клиента** and **Территория** each new client belongs to.
**Time**: ~10 minutes
**Hard parts**:
- The importer is a **two-step** flow: upload → review → commit. If you close the tab between steps, the upload is discarded.
- Duplicate detection runs by (`NAME`, `INN`) — if you forget INN, you can create real duplicates.

## Step 1 — Open the clients page and grab the template

Navigate to **Clients → Clients** (URL: `/clients/client`).

![Annotated screenshot of the clients list](/screens/annotated/clients_client.annotated.png)

1. The toolbar shows action chips: **Неподтвержденные клиенты** (①), **История изменения визитов** (②), and **QR-kod** (③). Above them is the **Экспорт / Импорт** menu — open it.
2. Click **Скачать шаблон**. The browser downloads `clients_template.xlsx`. The file has one header row with all expected columns.

The data grid below (④) is where your imported rows will appear after commit.

## Step 2 — Fill three test rows

Open the template. Fill exactly three rows with realistic data:

| Column | Required | Example |
|---|---|---|
| `NAME` | yes | OOO "Test Outlet 1" |
| `INN` | recommended | 304012345 |
| `ADDRESS` | yes | Tashkent, Yunusabad, M.Ulugbek 12 |
| `PHONE` | recommended | +998901234567 |
| `CATEGORY` | yes | A |
| `TERRITORY` | yes | Yunusabad |
| `PRICE_TYPE` | no — defaults | retail |
| `LAT`, `LON` | no | 41.32, 69.27 |

Save the file as `clients_test.xlsx`.

## Step 3 — Upload and review

1. Back on `/clients/client`, open **Экспорт / Импорт → Импорт**.
2. Pick your `clients_test.xlsx` file. The page submits to `POST /clients/import/preview`.
3. A preview screen opens showing each row with a status badge:
   - **OK**: will be inserted on commit.
   - **Duplicate**: an existing client matches by `NAME`+`INN`; row will be skipped.
   - **Error**: a required column is empty or a referenced category does not exist; row needs editing before commit.
4. Hover any error to see the exact column and reason.

## Step 4 — Fix errors

If any row shows **Error**:

1. Click **Скачать ошибки**. This downloads a copy of the file with an extra `ERROR` column.
2. Fix the rows in Excel.
3. Re-upload through the same dialog. The previous preview is discarded.

Iterate until all three rows are **OK**.

## Step 5 — Commit

1. Click **Импортировать** at the bottom of the preview. The page calls `POST /clients/import/commit`.
2. Inside one DB transaction, the controller inserts the **OK** rows into `d0_client`, skips **Duplicate** rows, and writes a row to `d0_client_import_log` so you have an audit trail of who imported what when.
3. You are redirected back to `/clients/client` with a green flash showing how many rows were inserted.

## Step 6 — Verify

1. On the clients grid (④), filter by **Название** for "Test Outlet". All three new rows should appear.
2. Click one — the detail page should show the address, INN, phone, category and territory you uploaded.
3. Cross-check in the audit log at **Settings → Журнал импорта**: the import you just ran is at the top with your username and a count of 3.

## What just happened (under the hood)

The flow is split across `ClientImportController::actionPreview` (validates and returns a preview without writing) and `ClientImportController::actionCommit` (writes inside a transaction). Duplicate detection compares trimmed `LOWER(NAME)` + `INN`. Category and territory are resolved to FK by exact name match; if your spreadsheet column says "A-Class" but the DB has "A", the row errors out. See the [clients module](/docs/modules/clients) for the full column reference and the [data model](/docs/data/schema-reference) for `d0_client`.

## Common mistakes

- **Closing the tab between preview and commit**: the preview is held server-side per session. Close the tab and you have to re-upload.
- **Missing INN on real businesses**: duplicate detection then falls back to name only. With slightly different spellings ("OOO Test" vs "OOO 'Test'") you create real duplicates.
- **Category/territory typos**: rows error out silently if you do not look at the preview — the badge is small.
- **No GPS**: clients without `LAT`/`LON` cannot be visited by agents from mobile (GPS check-in fails). Either set coordinates in the spreadsheet or have a supervisor capture them on first visit.

## Next steps

- Onboard a freshly-imported B2B customer to self-service: [Onboard a B2B customer to the online portal](./set-up-online-portal.md).
- Have an agent visit them tomorrow: [Create an order from the mobile agent app](./create-order-mobile.md).
- Full clients reference: [clients module](/docs/modules/clients).
