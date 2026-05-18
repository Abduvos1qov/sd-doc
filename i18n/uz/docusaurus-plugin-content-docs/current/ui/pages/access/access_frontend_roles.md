---
title: "Rollar"
audience: sd-main dasturchilari, QA
summary: Admin paneldagi jonli sahifa /access/frontend/roles
topics: [access, rbac, page, ui]
---

# Rollar

**URL**: `/access/frontend/roles` · **Modul**: `access` · **Kontroller**: `FrontendController::roles` · **RBAC**: `operation.rbac.roles` + global `showAllRbacFunctions` · **Yigʻilgan rol**: `admin`

:::note Skrinshot tayyorlanmoqda — harvester'ni qayta ishga tushirish kerak:::

## Vazifasi

RBAC rollar katalogi. Rol bir nechta operatsiyani (va ixtiyoriy ravishda boshqa rollarni) birlashtiradi. Ushbu sahifada `manager` yoki `audit-lite` kabi rollarni yaratiladi va tayinlovlar jadvali orqali ularga operatsiyalar biriktiriladi. Server parametri `showAllRbacFunctions` oʻchirilgan boʻlsa sahifa berkitiladi — `operation.rbac.roles` bor foydalanuvchi ham `H::err403()` oladi.

## Joylashuv

- Chap panel: rollar yon roʻyxati.
- Markaz: tayinlovlar jadvali (tanlangan rolga biriktirilgan operatsiyalar).
- Modal: create / update / bind forma.

## Amallar

- Yangi rol yaratish
- Rolni qayta nomlash / oʻchirish
- Rolga operatsiyani biriktirish
- Rolga operatsiyani uzish
- Oʻzgartirishdan keyin qayta yuklash

## Backend marshrut

- **Kontroller fayli**: `protected/modules/access/controllers/FrontendController.php`
- **Action turi**: inline (`actionRoles` `$this->render('roles')` ni chaqiradi)
- **Render qilinadigan view**: `views/frontend/roles.php`
- **Talab qilinadigan ruxsat**: `operation.rbac.roles`
- **Yashirish parametri**: `showAllRbacFunctions` true boʻlishi kerak
- **Sahifa ishlatadigan JSON endpoint'lar**:
  - `GET /access/backend/roles`
  - `GET /access/backend/roles-privileges?roleId=…`
  - `GET /access/backend/roles-privileges-available?roleId=…`
  - `POST /access/backend/create-update-assignment`
  - `POST /access/backend/remove-assignments`
  - `POST /access/backend/bind-assignments`
  - `POST /access/backend/un-bind-assignments`

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/access](/docs/modules/access)
- RBAC kontsepsiyasi: [/concepts/rbac](/docs/concepts/rbac)
- RBAC matritsasi: [/quality/rbac-matrix](/docs/quality/rbac-matrix)
