---
title: Поиск наборов данных в Глобальном каталоге обнаружения WIS2
---

# Поиск наборов данных в Глобальном каталоге обнаружения WIS2

!!! abstract "Результаты обучения!"

    По окончании этого практического занятия вы сможете:

    - использовать pywiscat для поиска наборов данных в Global Discovery Catalogue (GDC)

## Введение

В этом занятии вы научитесь искать данные в WIS2 Global Discovery Catalogue (GDC).

На данный момент доступны следующие GDC:

- Environment and Climate Change Canada, Meteorological Service of Canada: <https://wis2-gdc.weather.gc.ca>
- China Meteorological Administration: <https://gdc.wis.cma.cn>
- Deutscher Wetterdienst: <https://wis2.dwd.de/gdc>

Во время локальных учебных сессий настраивается локальный GDC, чтобы участники могли запрашивать метаданные, опубликованные из их экземпляров wis2box. В этом случае тренеры предоставят URL локального GDC.

## Подготовка

!!! note
    Перед началом войдите в свою учебную виртуальную машину.

## Установка pywiscat

Используйте установщик пакетов Python `pip3` для установки pywiscat на вашу виртуальную машину:
```bash
pip3 install pywiscat
```

!!! note

    Если вы столкнулись со следующей ошибкой:

    ```
    WARNING: The script pywiscat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    Выполните следующую команду:

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    ...где `$USER` - это ваше имя пользователя на виртуальной машине.

Проверьте успешность установки:

```bash
pywiscat --version
```

## Поиск данных с помощью pywiscat

По умолчанию pywiscat подключается к Global Discovery Catalogue Канады. Давайте настроим pywiscat для запросов к учебному GDC, установив переменную окружения `PYWISCAT_GDC_URL`:

```bash
export PYWISCAT_GDC_URL=http://gdc.wis2.training:5002
```

Давайте используем [pywiscat](https://github.com/wmo-im/pywiscat) для запросов к GDC, настроенному в рамках обучения.

```bash
pywiscat search --help
```

Теперь выполним поиск всех записей в GDC:

```bash
pywiscat search
```

!!! question

    Сколько записей возвращается при поиске?

??? success "Нажмите, чтобы увидеть ответ"
    Количество записей зависит от GDC, к которому вы обращаетесь. При использовании локального учебного GDC вы должны увидеть, что количество записей равно количеству наборов данных, загруженных в GDC во время других практических занятий.

Давайте попробуем выполнить поиск в GDC по ключевому слову:

```bash
pywiscat search -q observations
```

!!! question

    Какова политика доступа к данным в результатах?

??? success "Нажмите, чтобы увидеть ответ"
    Все возвращаемые данные должны иметь пометку "core"

Попробуйте дополнительные запросы с `-q`

!!! tip

    Флаг `-q` поддерживает следующий синтаксис:

    - `-q synop`: найти все записи со словом "synop"
    - `-q temp`: найти все записи со словом "temp"
    - `-q "observations AND oman"`: найти все записи со словами "observations" и "oman"
    - `-q "observations NOT oman"`: найти все записи, содержащие слово "observations", но не содержащие слово "oman"
    - `-q "synop OR temp"`: найти все записи со словами "synop" или "temp"
    - `-q "obs*"`: нечеткий поиск

    При поиске терминов с пробелами заключайте их в двойные кавычки.

Давайте получим более подробную информацию о конкретном результате поиска, который нас интересует:

```bash
pywiscat get <id>
```

!!! tip

    Используйте значение `id` из предыдущего поиска.


## Заключение

!!! success "Поздравляем!"

    В этом практическом занятии вы научились:

    - использовать pywiscat для поиска наборов данных в WIS2 Global Discovery Catalogue