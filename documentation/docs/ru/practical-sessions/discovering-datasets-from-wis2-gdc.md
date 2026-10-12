---
title: Обнаружение наборов данных в WIS2 Global Discovery Catalogue
---

# Обнаружение наборов данных в WIS2 Global Discovery Catalogue

!!! abstract "Результаты обучения!"

    По завершении этой практической сессии вы сможете:

    - использовать pywmocat для обнаружения наборов данных в Global Discovery Catalogue (GDC)

## Введение

В этой сессии вы научитесь находить данные в WIS2 Global Discovery Catalogue (GDC) с помощью [pywmocat](https://github.com/wmo-im/pywmocat), инструмента командной строки для поиска и извлечения метаданных из WIS2 GDC.

На данный момент доступны следующие GDC:

- Environment and Climate Change Canada, Meteorological Service of Canada: <https://wis2-gdc.weather.gc.ca/collections/wis2-discovery-metadata>
- China Meteorological Administration: <https://gdc.wis.cma.cn/collections/wis2-discovery-metadata>
- Deutscher Wetterdienst: <https://wis2.dwd.de/gdc/collections/wis2-discovery-metadata>

Во время локальных тренировочных сессий настраивается локальный GDC, чтобы участники могли запрашивать метаданные, опубликованные из их экземпляров wis2box. В этом случае тренеры предоставят URL для локального GDC.

## Подготовка

!!! note
    Перед началом работы войдите в свою виртуальную машину (VM) для обучения.

## Установка pywmocat

Используйте установщик пакетов Python `pip3` для установки pywmocat на вашу виртуальную машину:

```bash
pip3 install pywmocat
```

!!! note

    Если вы столкнулись с ошибкой:

    ```
    WARNING: The script pywmocat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    Тогда выполните следующую команду:

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    ...где `$USER` — это ваше имя пользователя на виртуальной машине.

Проверьте, что установка прошла успешно:

```bash
pywmocat --version
```

## Поиск данных с помощью pywmocat

По умолчанию pywmocat подключается к Global Discovery Catalogue (GDC), размещенному Environment and Climate Change Canada (ECCC).

!!! note "Изменение URL GDC"
    Если вы выполняете это упражнение во время локальной тренировочной сессии, вы можете настроить pywmocat для запроса локального GDC, установив переменную окружения `PYWISCAT_GDC_URL`:

    ```bash
    export PYWMOCAT_WIS2_GDC_URL=http://gdc.training.wis2dev.io/collections/wis2-discovery-metadata
    ```

Чтобы увидеть доступные параметры, выполните:

```bash
pywmocat wis2-gdc search --help
```

Вы можете выполнить поиск всех записей в GDC:

```bash
pywmocat wis2-gdc search
```

!!! question

    Сколько записей возвращается в результате поиска?

??? success "Нажмите, чтобы увидеть ответ"
    Количество записей зависит от GDC, который вы запрашиваете. При использовании локального тренировочного GDC вы должны увидеть, что количество записей равно количеству наборов данных, загруженных в GDC во время других практических сессий.

Попробуем выполнить запрос в GDC с использованием ключевого слова:

```bash
pywmocat wis2-gdc search -q observations
```

!!! question

    Какова политика данных для результатов?

??? success "Нажмите, чтобы увидеть ответ"
    Все возвращенные данные должны быть указаны как "core" (основные данные).

Попробуйте выполнить дополнительные запросы с помощью `-q`.

!!! tip

    Флаг `-q` поддерживает следующий синтаксис:

    - `-q synop`: найти все записи с ключевым словом "synop"
    - `-q temp`: найти все записи с ключевым словом "temp"
    - `-q "observations AND oman"`: найти все записи с ключевыми словами "observations" и "oman"
    - `-q "observations NOT oman"`: найти все записи, содержащие слово "observations", но не слово "oman"
    - `-q "synop OR temp"`: найти все записи с ключевыми словами "synop" или "temp"
    - `-q "obs*"`: нечеткий поиск

    При поиске терминов с пробелами заключайте их в двойные кавычки.

Получим больше информации о конкретном результате поиска, который нас интересует:

```bash
pywmocat wis2-gdc get <id>
```

!!! tip

    Используйте значение `id` из предыдущего поиска.

## Заключение

!!! success "Поздравляем!"

    В этой практической сессии вы научились:

    - использовать pywmocat для обнаружения наборов данных в WIS2 Global Discovery Catalogue