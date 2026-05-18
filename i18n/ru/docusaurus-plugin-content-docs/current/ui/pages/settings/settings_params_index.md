---
title: "Глобальные параметры"
audience: Разработчики sd-main, QA
summary: Живая страница админки /settings/params/index
topics: [settings, params, page, ui]
---

# Глобальные параметры

**URL**: `/settings/params/index` · **Модуль**: `settings` · **Контроллер**: `ParamsController::index` · **RBAC**: `operation.settings.params` · **Снятая роль**: `admin`

:::note Скриншот в процессе — нужен повторный запуск харвестера:::

## Назначение

Сырой key / value-редактор таблицы глобальных параметров. В отличие от главной настроек (где параметры собраны в курированные табы), здесь супер-админ может посмотреть или поправить любую строку — включая серверные тумблеры вроде `showAllRbacFunctions`, `enableOnlineOrder`, `payme.merchantId`. Пользуйтесь только если знаете ключ параметра — для обычной работы безопаснее курированные табы.

## Колонки таблицы

| № | Колонка |
|---|---|
| 1 | Ключ параметра |
| 2 | Значение |
| 3 | Группа |
| 4 | Описание |
| 5 | Обновлено |
| 6 | Кто обновил |

## Действия

- Редактировать значение inline
- Добавить новую строку
- Удалить строку (редко — обычно оставляем строку с пустым значением)

## Бэкенд-маршрут

- **Файл контроллера**: `protected/modules/settings/controllers/ParamsController.php` (строка 5)
- **Тип действия**: inline (`$this->render('index')`)
- **Рендерится вьюха**: `views/params/index.php`
- **Требуется доступ**: `operation.settings.params`

## См. также

- Справочник модуля: [/modules/settings](/docs/modules/settings)
- Каталог настроек: [/quality/settings-catalog](/docs/quality/settings-catalog)
- Главная настроек: [`/settings/settings/index`](./settings_settings_index)
