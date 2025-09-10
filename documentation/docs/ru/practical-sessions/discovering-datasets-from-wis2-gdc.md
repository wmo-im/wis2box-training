---
title: Обнаружение наборов данных из WIS2 Global Discovery Catalogue
---

# Обнаружение наборов данных из WIS2 Global Discovery Catalogue

!!! abstract "Результаты обучения!"

    К концу этой практической сессии вы сможете:

    - использовать pywiscat для поиска наборов данных в Global Discovery Catalogue (GDC)

## Введение

В этой сессии вы научитесь находить данные в WIS2 Global Discovery Catalogue (GDC) с помощью [pywiscat](https://github.com/wmo-im/pywiscat), инструмента командной строки для поиска и извлечения метаданных из WIS2 GDC.

На данный момент доступны следующие GDC:

- Environment and Climate Change Canada, Meteorological Service of Canada: <https://wis2-gdc.weather.gc.ca>
- China Meteorological Administration: <https://gdc.wis.cma.cn>
- Deutscher Wetterdienst: <https://wis2.dwd.de/gdc>

Во время локальных тренировочных сессий настраивается локальный GDC, чтобы участники могли запрашивать метаданные, опубликованные из их экземпляров wis2box. В этом случае тренеры предоставят URL для локального GDC.

## Подготовка

!!! note
    Перед началом, пожалуйста, войдите в вашу виртуальную машину (VM) студента.

## Установка pywiscat

Используйте установщик пакетов Python `pip3` для установки pywiscat на вашу виртуальную машину (VM):
```bash
pip3 install pywiscat
```

!!! note

    Если вы столкнулись с следующей ошибкой:

    ```
    WARNING: The script pywiscat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    Тогда выполните следующую команду:

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    ...где `$USER` — это ваше имя пользователя на вашей виртуальной машине.

Убедитесь, что установка прошла успешно:

```bash
pywiscat --version
```

## Поиск данных с помощью pywiscat

По умолчанию pywiscat подключается к Global Discovery Catalogue (GDC), размещенному Environment and Climate Change Canada (ECCC).

!!! note "Изменение URL GDC"
    Если вы выполняете это упражнение во время локальной тренировочной сессии, вы можете настроить pywiscat для запроса локального GDC, установив переменную окружения `PYWISCAT_GDC_URL`:

    ```bash
    export PYWISCAT_GDC_URL=http://gdc.wis2.training:5002
    ```

Чтобы увидеть доступные опции, выполните:

```bash
pywiscat search --help
```

Вы можете выполнить поиск всех записей в GDC:

```bash
pywiscat search
```

!!! question

    Сколько записей возвращается в результате поиска?

??? success "Нажмите, чтобы увидеть ответ"
    Количество записей зависит от GDC, который вы запрашиваете. При использовании локального тренировочного GDC вы должны увидеть, что количество записей равно количеству наборов данных, которые были загружены в GDC во время других практических сессий.

Попробуем выполнить запрос в GDC с использованием ключевого слова:

```bash
pywiscat search -q observations
```

!!! question

    Какова политика данных для результатов?

??? success "Нажмите, чтобы увидеть ответ"
    Все возвращенные данные должны указывать на "core" данные.

Попробуйте дополнительные запросы с использованием `-q`.

!!! tip

    Флаг `-q` поддерживает следующий синтаксис:

    - `-q synop`: найти все записи с словом "synop"
    - `-q temp`: найти все записи с словом "temp"
    - `-q "observations AND oman"`: найти все записи с словами "observations" и "oman"
    - `-q "observations NOT oman"`: найти все записи, содержащие слово "observations", но не содержащее слово "oman"
    - `-q "synop OR temp"`: найти все записи с "synop" или "temp"
    - `-q "obs*"`: нечеткий поиск

    При поиске терминов с пробелами заключайте их в двойные кавычки.

Давайте получим больше информации о конкретном результате поиска, который нас интересует:

```bash
pywiscat get <id>
```

!!! tip

    Используйте значение `id` из предыдущего поиска.

## Заключение

!!! success "Поздравляем!"

    В этой практической сессии вы научились:

    - использовать pywiscat для поиска наборов данных в WIS2 Global Discovery Catalogue