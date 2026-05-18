---
title: "Operatsiyalar"
audience: sd-main dasturchilari, QA
summary: Admin paneldagi jonli sahifa /access/frontend/operations
topics: [access, rbac, page, ui]
---

# Operatsiyalar

**URL**: `/access/frontend/operations` · **Modul**: `access` · **Kontroller**: `FrontendController::operations` · **RBAC**: `operation.rbac.operations` + global `showAllRbacFunctions` · **Yigʻilgan rol**: `admin`

:::note Skrinshot tayyorlanmoqda — harvester'ni qayta ishga tushirish kerak:::

## Vazifasi

Tizimda aniqlangan barcha RBAC operatsiyalarining faqat oʻqish uchun katalogi. Operatsiya — imtiyozning eng past darajasi: kontrollerlardagi har bir `H::access('operation.<module>.<action>')` chaqiruv shu yerdagi qatorga mos keladi. Roʻyxat `Access::AssignmentsAvailable(["type" => 0, "parentType" => 1])` metodi orqali hisoblanadi va u hali hech narsaga biriktirilmagan barcha operatsiyalarni qaytaradi. `showAllRbacFunctions` oʻchirilgan boʻlsa sahifa yashiriladi.

## Jadval ustunlari

| № | Ustun |
|---|---|
| 1 | Operatsiya nomi (masalan, `operation.orders.list`) |
| 2 | Tavsif (i18n yorlig'i) |
| 3 | Modul |
| 4 | Guruh |

## Amallar

- Nomi boʻyicha filtr / qidiruv
- Operatsiyani biriktirish uchun mos rol yoki vazifani ochish

## Backend marshrut

- **Kontroller fayli**: `protected/modules/access/controllers/FrontendController.php`
- **Action turi**: inline (`actionOperations` `$this->render('operations')` ni chaqiradi)
- **Render qilinadigan view**: `views/frontend/operations.php`
- **Talab qilinadigan ruxsat**: `operation.rbac.operations`
- **Yashirish parametri**: `showAllRbacFunctions` true boʻlishi kerak
- **Sahifa ishlatadigan JSON endpoint**: `GET /access/backend/operations`

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/access](/docs/modules/access)
- RBAC kontsepsiyasi: [/concepts/rbac](/docs/concepts/rbac)
- RBAC matritsasi: [/quality/rbac-matrix](/docs/quality/rbac-matrix)
