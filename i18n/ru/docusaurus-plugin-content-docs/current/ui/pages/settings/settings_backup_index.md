---
title: "Бэкап / экспорт"
audience: Разработчики sd-main, QA
summary: Живая страница админки /settings/backup/index
topics: [settings, backup, export, page, ui]
---

# Бэкап / экспорт

**URL**: `/settings/backup/index` · **Модуль**: `settings` · **Контроллер**: `BackupController::index` · **RBAC**: `operation.settings.backup` · **Снятая роль**: `admin`

:::note Скриншот в процессе — нужен повторный запуск харвестера:::

## Назначение

Центральный хаб экспорта. Каждая плитка запускает экспорт одного справочника — стримит CSV / JSON текущего состояния тенанта; полезно для оффсайт-бэкапа, передачи аудитору и разовой миграции на новую установку. Эндпоинты приходят из `BackupController::endpoints` и покрывают весь набор справочников (товары, цены, клиенты и т. д.).

## Плитки

- Каталог эндпоинтов (`endpoints`)
- Товар (`product`)
- Категория товара (`productCategory`)
- Тип кейса товара (`productCaseType`)
- Группа категорий товара (`productCatGroup`)
- Группа товаров (`productGroup`)
- Подкатегория товара (`productSubCategory`)
- Тип цены (`priceType`)
- Цена (`price`)
- (и остальные плитки справочников — полный список в исходнике контроллера)

## Действия

- Запустить экспорт по выбранной плитке
- Скачать получившийся файл

## Бэкенд-маршрут

- **Файл контроллера**: `protected/modules/settings/controllers/BackupController.php` (строка 41)
- **Тип действия**: inline (`$this->render('index', …)`)
- **Рендерится вьюха**: `views/backup/index.php`
- **Требуется доступ**: `operation.settings.backup`

## См. также

- Справочник модуля: [/modules/settings](/docs/modules/settings)
- Каталог настроек: [/quality/settings-catalog](/docs/quality/settings-catalog)
