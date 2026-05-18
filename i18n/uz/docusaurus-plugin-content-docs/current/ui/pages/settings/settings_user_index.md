---
title: "Foydalanuvchilar"
audience: sd-main dasturchilari, QA
summary: Admin paneldagi jonli sahifa /settings/user/index
topics: [settings, user, page, ui]
---

# Foydalanuvchilar

**URL**: `/settings/user/index` · **Modul**: `settings` · **Kontroller**: `UserController::index` · **RBAC**: `operation.settings.user` · **Yigʻilgan rol**: `admin`

:::note Skrinshot tayyorlanmoqda — harvester'ni qayta ishga tushirish kerak:::

## Vazifasi

Tenant'ning foydalanuvchilar roʻyxati. Har bir login (admin, menejer, supervayzer, agent, ekspeditor, omborchi, auditor) bu yerda kirish maʼlumotlari, til, standart rol, kontakt va qolgan ilovani cheklaydigan hudud / brend qamrovlari bilan birga roʻyxatdan oʻtkaziladi. Parolni almashtirish ikkita yoʻlga boʻlingan: oʻz-oʻzini xizmat koʻrsatish (`updateLoginPassword`) va super-admin yoʻli (`updateLoginPassword2`).

## Jadval ustunlari

| № | Ustun |
|---|---|
| 1 | ID |
| 2 | Login |
| 3 | Toʻliq ism |
| 4 | Rol |
| 5 | Hudud |
| 6 | Telefon |
| 7 | Oxirgi kirish |
| 8 | Faol |
| 9 | Yaratilgan |

## Amallar

- Foydalanuvchi qoʻshish (modal — `createAjax`)
- Foydalanuvchini tahrirlash (modal — `updateAjax`)
- Foydalanuvchini oʻchirish (`deleteUser`)
- Parolni tiklash (oʻzi — `updateLoginPassWord`)
- Parolni tiklash (admin — `updateLoginPassword2`)
- Ajax formani qaytarish (`returnAjaxForm`)
- Faollikni oʻzgartirish

## Backend marshrut

- **Kontroller fayli**: `protected/modules/settings/controllers/UserController.php` (24-qator)
- **Action turi**: inline (`$this->render('admingrid_diler', …)`)
- **Render qilinadigan view**: `views/user/admingrid_diler.php`
- **Talab qilinadigan ruxsat**: `operation.settings.user`
- **Qoʻshni endpoint'lar**: `getData`, `getUpdatedRow`, `createAjax`, `updateAjax`, `deleteUser`, `updateLoginPassWord`, `updateLoginPassword2`, `returnAjaxForm`

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/settings](/docs/modules/settings)
- RBAC konsoli: [`/access/frontend/users`](../access/access_frontend_users)
- RBAC matritsasi: [/quality/rbac-matrix](/docs/quality/rbac-matrix)
