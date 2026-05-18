---
title: "Пользователи"
audience: Разработчики sd-main, QA
summary: Живая страница админки /settings/user/index
topics: [settings, user, page, ui]
---

# Пользователи

**URL**: `/settings/user/index` · **Модуль**: `settings` · **Контроллер**: `UserController::index` · **RBAC**: `operation.settings.user` · **Снятая роль**: `admin`

:::note Скриншот в процессе — нужен повторный запуск харвестера:::

## Назначение

Реестр пользователей тенанта. Каждый логин (админ, менеджер, супервайзер, агент, экспедитор, складовщик, аудитор) регистрируется здесь вместе с креденшелами, локалью, дефолтной ролью, контактами и областями (территория / бренд), которые регулируют доступ во всём приложении. Ротация пароля разделена на самообслуживание (`updateLoginPassword`) и админский путь (`updateLoginPassword2`).

## Колонки таблицы

| № | Колонка |
|---|---|
| 1 | ID |
| 2 | Логин |
| 3 | Полное имя |
| 4 | Роль |
| 5 | Территория |
| 6 | Телефон |
| 7 | Последний вход |
| 8 | Активен |
| 9 | Создан |

## Действия

- Добавить пользователя (модал — `createAjax`)
- Редактировать пользователя (модал — `updateAjax`)
- Удалить пользователя (`deleteUser`)
- Сбросить пароль (сам — `updateLoginPassWord`)
- Сбросить пароль (админ — `updateLoginPassword2`)
- Вернуть ajax-форму (`returnAjaxForm`)
- Переключить активность

## Бэкенд-маршрут

- **Файл контроллера**: `protected/modules/settings/controllers/UserController.php` (строка 24)
- **Тип действия**: inline (`$this->render('admingrid_diler', …)`)
- **Рендерится вьюха**: `views/user/admingrid_diler.php`
- **Требуется доступ**: `operation.settings.user`
- **Соседние эндпоинты**: `getData`, `getUpdatedRow`, `createAjax`, `updateAjax`, `deleteUser`, `updateLoginPassWord`, `updateLoginPassword2`, `returnAjaxForm`

## См. также

- Справочник модуля: [/modules/settings](/docs/modules/settings)
- RBAC-консоль: [`/access/frontend/users`](../access/access_frontend_users)
- Матрица RBAC: [/quality/rbac-matrix](/docs/quality/rbac-matrix)
