---
title: "Foydalanuvchilar va tayinlovlar"
audience: sd-main dasturchilari, QA
summary: Admin paneldagi jonli sahifa /access/frontend/users
topics: [access, rbac, page, ui]
---

# Foydalanuvchilar va tayinlovlar

**URL**: `/access/frontend/users` · **Modul**: `access` · **Kontroller**: `FrontendController::users` · **RBAC**: `operation.rbac.users` · **Yigʻilgan rol**: `admin`

:::note Skrinshot tayyorlanmoqda — harvester'ni qayta ishga tushirish kerak:::

## Vazifasi

RBAC foydalanuvchilar paneli. Chap roʻyxatdan foydalanuvchini tanlang, unga biriktirilgan rollar, vazifalar va operatsiyalar birlashmasini koʻring va modal forma orqali imtiyozlarni biriktiring yoki uzing. Maʼlumotlar `/access/backend/users`, `/access/backend/users-privileges?userId=…` va `/access/backend/users-privileges-available?userId=…` dan yuklanadi.

## Joylashuv

- Chap panel: foydalanuvchilar yon roʻyxati (`_sideList` partial).
- Yuqori: guruh selektori (`_groupList` partial).
- Markaz: tayinlovlar jadvali, har bir imtiyoz uchun bir qator (`_accessTable` partial).
- Modal: create / update / bind forma (`_modalForm` + `_crudBtns` partial'lar).

## Amallar

- Tanlangan foydalanuvchiga imtiyozni biriktirish
- Tanlangan tayinlovni uzish
- Tayinlovni yaratish / yangilash (modal)
- Tayinlovni oʻchirish
- Tayinlovlarni qayta yuklash (har bir mutatsiyadan keyin)

## Backend marshrut

- **Kontroller fayli**: `protected/modules/access/controllers/FrontendController.php`
- **Action turi**: inline (`actionUsers` `$this->render('users')` ni chaqiradi)
- **Render qilinadigan view**: `views/frontend/users.php`
- **Talab qilinadigan ruxsat**: `operation.rbac.users`
- **Sahifa ishlatadigan JSON endpoint'lar**:
  - `GET /access/backend/users`
  - `GET /access/backend/users-privileges?userId=…`
  - `GET /access/backend/users-privileges-available?userId=…`
  - `POST /access/backend/create-update-assignment`
  - `POST /access/backend/remove-assignments`
  - `POST /access/backend/bind-assignments`
  - `POST /access/backend/un-bind-assignments`
  - `POST /access/backend/bind-user`
  - `POST /access/backend/un-bind-user`
  - `POST /access/backend/reload-assignments`

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/access](/docs/modules/access)
- RBAC kontsepsiyasi: [/concepts/rbac](/docs/concepts/rbac)
- RBAC matritsasi: [/quality/rbac-matrix](/docs/quality/rbac-matrix)
