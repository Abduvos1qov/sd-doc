---
title: "Vazifalar"
audience: sd-main dasturchilari, QA
summary: Admin paneldagi jonli sahifa /access/frontend/tasks
topics: [access, rbac, page, ui]
---

# Vazifalar

**URL**: `/access/frontend/tasks` · **Modul**: `access` · **Kontroller**: `FrontendController::tasks` · **RBAC**: `operation.rbac.tasks` + global `showAllRbacFunctions` · **Yigʻilgan rol**: `admin`

:::note Skrinshot tayyorlanmoqda — harvester'ni qayta ishga tushirish kerak:::

## Vazifasi

RBAC vazifalar katalogi. *Vazifa* — bir yoki bir nechta operatsiyani qayta foydalanish mumkin boʻlgan bog'lamga birlashtiruvchi qatlam: uni toʻgʻridan-toʻgʻri foydalanuvchiga berish yoki rolga biriktirish mumkin. Yii bunga **task** qatlami deydi, u operatsiyalar va rollar oraligʻida turadi. `showAllRbacFunctions` oʻchirilgan boʻlsa sahifa yashiriladi.

## Joylashuv

- Chap panel: vazifalar yon roʻyxati.
- Markaz: tanlangan vazifaga biriktirilgan operatsiyalar.
- Modal: create / update / bind forma.

## Amallar

- Yangi vazifa yaratish
- Vazifani qayta nomlash / oʻchirish
- Vazifaga operatsiyani biriktirish
- Vazifadan operatsiyani uzish
- Oʻzgartirishdan keyin qayta yuklash

## Backend marshrut

- **Kontroller fayli**: `protected/modules/access/controllers/FrontendController.php`
- **Action turi**: inline (`actionTasks` `$this->render('tasks')` ni chaqiradi)
- **Render qilinadigan view**: `views/frontend/tasks.php`
- **Talab qilinadigan ruxsat**: `operation.rbac.tasks`
- **Yashirish parametri**: `showAllRbacFunctions` true boʻlishi kerak
- **Sahifa ishlatadigan JSON endpoint'lar**:
  - `GET /access/backend/tasks`
  - `GET /access/backend/tasks-privileges?taskId=…`
  - `GET /access/backend/tasks-privileges-available?taskId=…`
  - `POST /access/backend/create-update-assignment`
  - `POST /access/backend/remove-assignments`

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/access](/docs/modules/access)
- RBAC kontsepsiyasi: [/concepts/rbac](/docs/concepts/rbac)
- RBAC matritsasi: [/quality/rbac-matrix](/docs/quality/rbac-matrix)
