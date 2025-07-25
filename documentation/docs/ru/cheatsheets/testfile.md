---
title: WIS2 in a box шпаргалка
---

# WIS2 in a box шпаргалка

## Обзор

wis2box работает как набор команд Docker Compose. Команда ``wis2box-ctl.py`` — это утилита 
(написанная на Python) для упрощённого выполнения команд Docker Compose.

## Основные команды wis2box

### Запуск и остановка

* Запустить wis2box:

```bash
python3 wis2box-ctl.py start
```

* Остановить wis2box:

```bash
python3 wis2box-ctl.py stop
```

* Проверить, что все контейнеры wis2box запущены:

```bash
python3 wis2box-ctl.py status
```

* Войти в контейнер wis2box (*wis2box-management* по умолчанию):

```bash
python3 wis2box-ctl.py login
```

* Войти в конкретный контейнер wis2box:

```bash
python3 wis2box-ctl.py login wis2box-api
```