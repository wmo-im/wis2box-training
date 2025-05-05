---
title: Шпаргалка WIS2 в коробке
---

# Шпаргалка WIS2 в коробке

## Обзор

wis2box работает как набор команд Docker Compose. Команда ``wis2box-ctl.py`` — это утилита
(написанная на Python), которая позволяет легко выполнять команды Docker Compose.

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

* Проверить, что все контейнеры wis2box работают:

```bash
python3 wis2box-ctl.py status
```

* Войти в контейнер wis2box (по умолчанию *wis2box-management*):

```bash
python3 wis2box-ctl.py login
```

* Войти в конкретный контейнер wis2box:

```bash
python3 wis2box-ctl.py login wis2box-api
```