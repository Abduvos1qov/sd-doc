---
title: "Список партнёров"
audience: All sd-main developers, QA
summary: Admin page at /partners/list — manage partner users (role 7) and their categories
topics: [partners, page, ui]
---

# Список партнёров

**URL**: `/partners/list` · **Module**: `partners` · **Controller**: `ListController::index` · **RBAC**: `operation.settings.partners` · **Role harvested**: `admin`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Lists every partner user (User.ROLE = 7) attached to the current diler, grouped into Активные / Неактивные tabs. Used to create new partners, edit existing ones (name, login, password, product categories) and toggle their active status. Backed by Yii's `AjaxCrudBehavior` so add/edit/delete all happen inline via modal forms.

## Fields (form fields rendered by `_form.php`)

| Label | Name | Type | Required |
|---|---|---|---|
| Категории продуктов | `PRODUCT_CAT_ID[]` | multi-select | yes |
| Ф.И.О. | `User[NAME]` | text | yes |
| Активный | `Partner[ACTIVE]` | checkbox | no |
| Email | `User[EMAIL]` | email | no |
| Телефон | `User[TEL]` | text | no |
| Внешний ID | `User[XML_ID]` | text | no |
| Логин | `User[LOGIN]` | text | yes |
| Пароль | `User[PASSWORD]` | password | yes (new), optional (edit) |

## Grid columns

The page has two DataTables (one per tab); both share these columns:

| # | Column | Source |
|---|---|---|
| 1 | Ф.И.О. | `User.NAME` (joined via `Spravochnik[user][USER_ID]`) |
| 2 | Категория товара | `Partner::returnAllProductCategoryForPartner(USER_ID)` |
| 3 | (edit button) | per-row `<a class="btn btn-info update">` |

## Actions

- Добавить нового партнера — opens `_form.php` modal in create mode
- Транзакция — navigates to `/partners/list/transaction`
- Активные / Неактивные tabs — filter by `Partner.ACTIVE = 'Y' | 'N'`
- (per row) edit — opens `_form.php` modal in update mode
- (per row) delete — calls `actionDeleteAjax`
- DataTable buttons: pageLength, colvis, Excel export

## Backend route

- **Controller file**: `protected/modules/partners/controllers/ListController.php`
- **Action**: `actionIndex` (line 45) — renders `admingrid_diler` view
- **Required permission**: `operation.settings.partners`
- **Sibling AJAX actions**: `actionReturnAjaxForm`, `actionCreateAjax`, `actionUpdateAjax`, `actionDeleteAjax`
- **Behavior**: `AjaxCrudBehavior` (model `Partner`, form alias `_form`, paginate 10)

## See also

- Module reference: [/modules/partners](/docs/modules/partners)
- Pages index: [/ui/pages/partners](./index.md)
