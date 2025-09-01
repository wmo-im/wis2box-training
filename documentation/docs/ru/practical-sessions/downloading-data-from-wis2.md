---
title: Загрузка данных из WIS2 с использованием wis2downloader
---

# Загрузка данных из WIS2 с использованием wis2downloader

!!! abstract "Результаты обучения!"

    По окончании этой практической сессии вы сможете:

    - использовать "wis2downloader" для подписки на уведомления о данных WIS2 и загрузки данных на вашу локальную систему
    - просматривать статус загрузок на панели мониторинга Grafana
    - научиться настраивать wis2downloader для подписки на брокер, отличный от брокера по умолчанию

## Введение

В этой сессии вы научитесь настраивать подписку на WIS2 Broker и автоматически загружать данные на вашу локальную систему с использованием сервиса "wis2downloader", включенного в wis2box.

!!! note "О wis2downloader"
     
     Сервис wis2downloader также доступен как отдельный сервис, который может быть запущен на другой системе, отличной от той, которая публикует уведомления WIS2. Подробнее о его использовании в качестве отдельного сервиса можно узнать на [wis2downloader](https://pypi.org/project/wis2downloader/).

     Если вы хотите разработать собственный сервис для подписки на уведомления WIS2 и загрузки данных, вы можете использовать [исходный код wis2downloader](https://github.com/World-Meteorological-Organization/wis2downloader) в качестве примера.

## Подготовка

Перед началом работы войдите в вашу виртуальную машину (VM) для студентов и убедитесь, что ваш экземпляр wis2box запущен и работает.

## Основы wis2downloader

Сервис wis2downloader включен в качестве отдельного контейнера в wis2box, как это определено в файлах Docker Compose. Контейнер Prometheus в wis2box настроен на сбор метрик из контейнера wis2downloader, и эти метрики можно визуализировать на панели мониторинга Grafana.

### Просмотр панели мониторинга wis2downloader в Grafana

Откройте веб-браузер и перейдите на панель мониторинга Grafana для вашего экземпляра wis2box, используя адрес `http://YOUR-HOST:3000`.

Нажмите на "dashboards" в левом меню, а затем выберите **wis2downloader dashboard**.

Вы должны увидеть следующую панель мониторинга:

![wis2downloader dashboard](../assets/img/wis2downloader-dashboard.png)

Эта панель основана на метриках, публикуемых сервисом wis2downloader, и отображает статус загрузок, которые выполняются в данный момент.

В левом верхнем углу вы можете увидеть активные подписки.

Оставьте эту панель открытой, так как вы будете использовать ее для мониторинга процесса загрузки в следующем упражнении.

### Проверка конфигурации wis2downloader

Сервис wis2downloader в wis2box можно настроить с использованием переменных окружения, определенных в вашем файле `wis2box.env`.

Следующие переменные окружения используются для настройки wis2downloader:

    - DOWNLOAD_BROKER_HOST: Имя хоста MQTT брокера для подключения. По умолчанию: globalbroker.meteo.fr
    - DOWNLOAD_BROKER_PORT: Порт MQTT брокера для подключения. По умолчанию: 443 (HTTPS для веб-сокетов)
    - DOWNLOAD_BROKER_USERNAME: Имя пользователя для подключения к MQTT брокеру. По умолчанию: everyone
    - DOWNLOAD_BROKER_PASSWORD: Пароль для подключения к MQTT брокеру. По умолчанию: everyone
    - DOWNLOAD_BROKER_TRANSPORT: websockets или tcp, механизм транспорта для подключения к MQTT брокеру. По умолчанию: websockets
    - DOWNLOAD_RETENTION_PERIOD_HOURS: Период хранения загруженных данных в часах. По умолчанию: 24
    - DOWNLOAD_WORKERS: Количество рабочих потоков для загрузки. По умолчанию: 8. Определяет количество параллельных загрузок.
    - DOWNLOAD_MIN_FREE_SPACE_GB: Минимальное свободное пространство в гигабайтах на томе, где хранятся загрузки. По умолчанию: 1.

Чтобы проверить текущую конфигурацию wis2downloader, выполните следующую команду:

```bash
cat ~/wis2box/wis2box.env | grep DOWNLOAD
```

!!! question "Проверьте конфигурацию wis2downloader"
    
    Какой MQTT брокер используется по умолчанию для подключения wis2downloader?

    Какой период хранения загруженных данных установлен по умолчанию?

??? success "Нажмите, чтобы увидеть ответ"

    MQTT брокер по умолчанию для подключения wis2downloader — это `globalbroker.meteo.fr`.

    Период хранения загруженных данных по умолчанию составляет 24 часа.

!!! note "Обновление конфигурации wis2downloader"

    Чтобы обновить конфигурацию wis2downloader, вы можете отредактировать файл wis2box.env. Для применения изменений перезапустите стек wis2box с помощью команды:

    ```bash
    python3 wis2box-ctl.py start
    ```

    После этого сервис wis2downloader перезапустится с новой конфигурацией.

Вы можете оставить конфигурацию по умолчанию для следующего упражнения.

### Интерфейс командной строки wis2downloader

Чтобы получить доступ к интерфейсу командной строки wis2downloader в рамках wis2box, войдите в контейнер **wis2downloader**, используя следующую команду:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Используйте следующую команду, чтобы отобразить список активных подписок:

```bash
wis2downloader list-subscriptions
```

Эта команда вернет пустой список, так как подписки еще не настроены.

## Загрузка данных GTS с использованием WIS2 Global Broker

Если вы оставили конфигурацию wis2downloader по умолчанию, он в настоящее время подключен к WIS2 Global Broker, размещенному Météo-France.

### Настройка подписки

Используйте следующую команду `cache/a/wis2/de-dwd-gts-to-wis2/#`, чтобы подписаться на данные, публикуемые шлюзом GTS-to-WIS2, размещенным DWD, и доступные через Global Caches:

```bash
wis2downloader add-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Затем выйдите из контейнера **wis2downloader**, набрав `exit`:

```bash
exit
```

### Проверка загруженных данных

Проверьте панель мониторинга wis2downloader в Grafana, чтобы увидеть добавленную подписку. Подождите несколько минут, и вы должны увидеть начало загрузок. Перейдите к следующему упражнению, как только убедитесь, что загрузки начались.

Сервис wis2downloader в wis2box загружает данные в каталог 'downloads', расположенный в каталоге, который вы указали как `WIS2BOX_HOST_DATADIR` в вашем файле `wis2box.env`. Чтобы просмотреть содержимое каталога загрузок, выполните следующую команду:

```bash
ls -R ~/wis2box-data/downloads
```

Обратите внимание, что загруженные данные хранятся в каталогах, названных в соответствии с темой, на которой было опубликовано уведомление WIS2.

!!! question "Просмотр загруженных данных"

    Какие каталоги вы видите в каталоге загрузок?

    Видите ли вы какие-либо загруженные файлы в этих каталогах?

??? success "Нажмите, чтобы увидеть ответ"
    Вы должны увидеть структуру каталогов, начинающуюся с `cache/a/wis2/de-dwd-gts-to-wis2/`, под которой будут находиться дополнительные каталоги, названные в соответствии с заголовками бюллетеней GTS для загруженных данных.

    В зависимости от времени начала подписки вы можете или не можете увидеть загруженные файлы в этом каталоге. Если файлов пока нет, подождите еще несколько минут и проверьте снова.

Давайте очистим подписку и загруженные данные перед переходом к следующему упражнению.

Войдите обратно в контейнер wis2downloader:

```bash
python3 wis2box-ctl.py login wis2downloader
```

и удалите подписку, используя следующую команду:

```bash
wis2downloader remove-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Удалите загруженные данные с помощью следующей команды:

```bash
rm -rf /wis2box-data/downloads/cache/*
```

И выйдите из контейнера wis2downloader, набрав `exit`:
    
```bash
exit
```

Проверьте панель мониторинга wis2downloader в Grafana, чтобы убедиться, что подписка удалена. Вы должны увидеть, что загрузки остановились.

!!! note "О шлюзах GTS-to-WIS2"
    В настоящее время два шлюза GTS-to-WIS2 публикуют данные через WIS2 Global Broker и Global Caches:

    - DWD (Германия): centre-id=*de-dwd-gts-to-wis2*
    - JMA (Япония): centre-id=*jp-jma-gts-to-wis2*
    
    Если в предыдущем упражнении вы замените `de-dwd-gts-to-wis2` на `jp-jma-gts-to-wis2`, вы получите уведомления и данные, публикуемые шлюзом JMA GTS-to-WIS2.

!!! note "Темы origin vs cache"

    При подписке на тему, начинающуюся с `origin/`, вы получите уведомления с каноническим URL, указывающим на сервер данных, предоставленный WIS-центром, публикующим данные.

    При подписке на тему, начинающуюся с `cache/`, вы получите несколько уведомлений для одних и тех же данных, по одному для каждого Global Cache. Каждое уведомление будет содержать канонический URL, указывающий на сервер данных соответствующего Global Cache. Сервис wis2downloader загрузит данные с первого доступного канонического URL.

## Загрузка примерных данных с WIS2 Training Broker

В этом упражнении вы подпишетесь на WIS2 Training Broker, который публикует примерные данные для учебных целей.

### Изменение конфигурации wis2downloader

Это демонстрирует, как подписаться на брокера, который не является брокером по умолчанию, и позволит вам загрузить данные, опубликованные с WIS2 Training Broker.

Отредактируйте файл `wis2box.env` и измените `DOWNLOAD_BROKER_HOST` на `wis2training-broker.wis2dev.io`, `DOWNLOAD_BROKER_PORT` на `1883` и `DOWNLOAD_BROKER_TRANSPORT` на `tcp`:

```copy
# настройки загрузчика
DOWNLOAD_BROKER_HOST=wis2training-broker.wis2dev.io
DOWNLOAD_BROKER_PORT=1883
DOWNLOAD_BROKER_USERNAME=everyone
DOWNLOAD_BROKER_PASSWORD=everyone
# механизм транспортировки загрузки (tcp или websockets)
DOWNLOAD_BROKER_TRANSPORT=tcp
```

Затем снова выполните команду 'start', чтобы применить изменения:

```bash
python3 wis2box-ctl.py start
```

Проверьте логи wis2downloader, чтобы убедиться, что подключение к новому брокеру прошло успешно:

```bash
docker logs wis2downloader
```

Вы должны увидеть следующее сообщение в логах:

```copy
...
INFO - Connecting...
INFO - Host: wis2training-broker.wis2dev.io, port: 1883
INFO - Connected successfully
```

### Настройка новых подписок

Теперь мы настроим новую подписку на топик для загрузки данных о треках циклонов с WIS2 Training Broker.

Войдите в контейнер **wis2downloader**:

```bash
python3 wis2box-ctl.py login wis2downloader
```

И выполните следующую команду (скопируйте и вставьте, чтобы избежать ошибок):

```bash
wis2downloader add-subscription --topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
```

Выйдите из контейнера **wis2downloader**, набрав `exit`.

### Проверка загруженных данных

Дождитесь начала загрузок, которые будут отображаться на панели мониторинга wis2downloader в Grafana.

Убедитесь, что данные были загружены, снова проверив логи wis2downloader:

```bash
docker logs wis2downloader
```

Вы должны увидеть сообщение в логах, похожее на следующее:

```copy
[...] INFO - Message received under topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
[...] INFO - Downloaded A_JSXX05ECEP020000_C_ECMP_...
```

Проверьте содержимое каталога загрузок:

```bash
ls -R ~/wis2box-data/downloads
```

Вы должны увидеть новый каталог с именем `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory`, содержащий загруженные данные.

!!! question "Просмотрите загруженные данные"
    
    Каков формат файла загруженных данных?

??? success "Нажмите, чтобы увидеть ответ"

    Загруженные данные находятся в формате BUFR, что указано расширением файла `.bufr`.

Теперь попробуйте добавить еще две подписки для загрузки данных о месячных аномалиях температуры поверхности и глобальных прогнозах ансамбля из следующих топиков:

- `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/global`
- `origin/a/wis2/int-wis2-training/data/core/climate/experimental/anomalies/monthly/surface-temperature`

Дождитесь начала загрузок, которые будут отображаться на панели мониторинга wis2downloader в Grafana.

Снова проверьте содержимое каталога загрузок:

```bash
ls -R ~/wis2box-data/downloads
```

Вы должны увидеть два новых каталога с именами `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/global` и `origin/a/wis2/int-wis2-training/data/core/climate/experimental/anomalies/monthly/surface-temperature`, содержащие загруженные данные.

!!! question "Просмотрите загруженные данные для двух новых топиков"
    
    Каков формат файла загруженных данных для топика `../prediction/forecast/medium-range/probabilistic/global`?

    Каков формат файла загруженных данных для топика `../climate/experimental/anomalies/monthly/surface-temperature`?

??? success "Нажмите, чтобы увидеть ответ"

    Загруженные данные для топика `../prediction/forecast/medium-range/probabilistic/global` находятся в формате GRIB2, что указано расширением файла `.grib2`.

    Загруженные данные для топика `../climate/experimental/anomalies/monthly/surface-temperature` находятся в формате NetCDF, что указано расширением файла `.nc`.

## Заключение

!!! success "Поздравляем!"

    В ходе этой практической сессии вы научились:

    - использовать 'wis2downloader' для подписки на WIS2 Broker и загрузки данных на локальную систему
    - просматривать статус загрузок на панели мониторинга Grafana
    - изменять конфигурацию по умолчанию wis2downloader для подписки на другого брокера
    - просматривать загруженные данные на локальной системе