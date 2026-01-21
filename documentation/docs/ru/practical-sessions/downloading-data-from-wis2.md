---
title: Загрузка данных из WIS2 с использованием wis2downloader
---

# Загрузка данных из WIS2 с использованием wis2downloader

!!! abstract "Результаты обучения!"

    К концу этой практической сессии вы сможете:

    - использовать "wis2downloader" для подписки на уведомления о данных WIS2 и загрузки данных на вашу локальную систему
    - просматривать статус загрузок на панели мониторинга Grafana
    - научиться настраивать wis2downloader для подписки на брокер, отличный от стандартного

## Введение

В этой сессии вы научитесь настраивать подписку на брокер WIS2 и автоматически загружать данные на вашу локальную систему с использованием сервиса "wis2downloader", включенного в wis2box.

!!! note "О wis2downloader"
     
     Сервис wis2downloader также доступен как отдельный сервис, который можно запускать на другой системе, отличной от той, которая публикует уведомления WIS2. Подробнее о использовании wis2downloader как отдельного сервиса смотрите на [wis2downloader](https://pypi.org/project/wis2downloader/).

     Если вы хотите разработать собственный сервис для подписки на уведомления WIS2 и загрузки данных, вы можете использовать [исходный код wis2downloader](https://github.com/World-Meteorological-Organization/wis2downloader) в качестве примера.

## Подготовка

Перед началом работы войдите в вашу виртуальную машину (VM) для студентов и убедитесь, что ваш экземпляр wis2box запущен и работает.

## Основы wis2downloader

Сервис wis2downloader включен в качестве отдельного контейнера в wis2box, как это определено в файлах Docker Compose. Контейнер Prometheus в wis2box настроен на сбор метрик из контейнера wis2downloader, и эти метрики можно визуализировать на панели мониторинга Grafana.

### Просмотр панели мониторинга wis2downloader в Grafana

Откройте веб-браузер и перейдите на панель мониторинга Grafana для вашего экземпляра wis2box, используя адрес `http://YOUR-HOST:3000`.

Нажмите на "dashboards" в левом меню:

![grafana dashboard selection](../assets/img/grafana-dashboard-selection.png)

и выберите **wis2downloader dashboard**:

![grafana dashboard options, select wis2downloader](../assets/img/grafana-select-wis2downloader-dashboard.png)

Вы должны увидеть следующую панель мониторинга:

![wis2downloader dashboard](../assets/img/wis2downloader-dashboard.png)

Эта панель мониторинга основана на метриках, публикуемых сервисом wis2downloader, и показывает статус загрузок, которые в данный момент выполняются.

В левом верхнем углу вы можете увидеть активные подписки.

Оставьте эту панель мониторинга открытой, так как вы будете использовать её для мониторинга прогресса загрузки в следующем упражнении.

### Обзор конфигурации wis2downloader

Сервис wis2downloader в wis2box можно настроить с использованием переменных окружения, определенных в вашем файле `wis2box.env`.

Следующие переменные окружения используются сервисом wis2downloader:

    - DOWNLOAD_BROKER_HOST: Имя хоста MQTT брокера для подключения. По умолчанию: globalbroker.meteo.fr
    - DOWNLOAD_BROKER_PORT: Порт MQTT брокера для подключения. По умолчанию: 443 (HTTPS для веб-сокетов)
    - DOWNLOAD_BROKER_USERNAME: Имя пользователя для подключения к MQTT брокеру. По умолчанию: everyone
    - DOWNLOAD_BROKER_PASSWORD: Пароль для подключения к MQTT брокеру. По умолчанию: everyone
    - DOWNLOAD_BROKER_TRANSPORT: websockets или tcp, механизм транспорта для подключения к MQTT брокеру. По умолчанию: websockets
    - DOWNLOAD_RETENTION_PERIOD_HOURS: Период хранения загруженных данных в часах. По умолчанию: 24
    - DOWNLOAD_WORKERS: Количество рабочих процессов для загрузки. По умолчанию: 8. Определяет количество параллельных загрузок.
    - DOWNLOAD_MIN_FREE_SPACE_GB: Минимальный свободный объем памяти в ГБ, который нужно сохранить на томе, где хранятся загрузки. По умолчанию: 1.

Чтобы просмотреть текущую конфигурацию wis2downloader, используйте следующую команду:

```bash
cat ~/wis2box/wis2box.env | grep DOWNLOAD
```

!!! question "Просмотр конфигурации wis2downloader"
    
    Какой MQTT брокер используется по умолчанию для подключения wis2downloader?

    Каков период хранения загруженных данных по умолчанию?

??? success "Нажмите, чтобы увидеть ответ"

    MQTT брокер по умолчанию для подключения wis2downloader — это `globalbroker.meteo.fr`.

    Период хранения загруженных данных по умолчанию составляет 24 часа.

!!! note "Обновление конфигурации wis2downloader"

    Чтобы обновить конфигурацию wis2downloader, вы можете отредактировать файл wis2box.env. Для применения изменений перезапустите стек wis2box с помощью команды:

    ```bash
    python3 wis2box-ctl.py start
    ```

    После этого сервис wis2downloader перезапустится с новой конфигурацией.

Вы можете оставить стандартную конфигурацию для следующего упражнения.

### Интерфейс командной строки wis2downloader

Чтобы получить доступ к интерфейсу командной строки wis2downloader в рамках wis2box, войдите в контейнер **wis2downloader** с помощью следующей команды:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Используйте следующую команду, чтобы просмотреть список активных подписок:

```bash
wis2downloader list-subscriptions
```

Эта команда вернет пустой список, так как подписки еще не настроены.

## Загрузка данных GTS с использованием WIS2 Global Broker

Если вы оставили стандартную конфигурацию wis2downloader, он в данный момент подключен к WIS2 Global Broker, размещенному Météo-France.

### Настройка подписки

Используйте следующую команду `cache/a/wis2/de-dwd-gts-to-wis2/#`, чтобы подписаться на данные, публикуемые шлюзом GTS-to-WIS2, размещенным DWD, и доступные через Global Caches:

```bash
wis2downloader add-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Затем выйдите из контейнера **wis2downloader**, введя `exit`:

```bash
exit
```

### Проверка загруженных данных

Проверьте панель мониторинга wis2downloader в Grafana, чтобы увидеть добавленную подписку. Подождите несколько минут, и вы должны увидеть начало загрузок. Перейдите к следующему упражнению, как только убедитесь, что загрузки начались.

Сервис wis2downloader в wis2box загружает данные в директорию 'downloads', которая находится в каталоге, определенном как `WIS2BOX_HOST_DATADIR` в вашем файле `wis2box.env`. Чтобы просмотреть содержимое директории загрузок, используйте следующую команду:

```bash
ls -R ~/wis2box-data/downloads
```

Обратите внимание, что загруженные данные хранятся в директориях, названных в соответствии с темой, на которой было опубликовано уведомление WIS2.

!!! question "Просмотр загруженных данных"

    Какие директории вы видите в директории загрузок?

    Видите ли вы какие-либо загруженные файлы в этих директориях?

??? success "Нажмите, чтобы увидеть ответ"
    Вы должны увидеть структуру директорий, начинающуюся с `cache/a/wis2/de-dwd-gts-to-wis2/`, под которой будут находиться дополнительные директории, названные в соответствии с заголовками бюллетеней GTS загруженных данных.

    В зависимости от времени начала подписки, вы можете увидеть или не увидеть загруженные файлы в этой директории. Если файлов пока нет, подождите еще несколько минут и проверьте снова.

Проверьте панель мониторинга wis2downloader в Grafana, чтобы увидеть прогресс загрузки. Вы увидите добавленную подписку в левом верхнем углу панели, а также увеличение количества загрузок по мере их выполнения:

![wis2downloader dashboard with active subscription](../assets/img/wis2downloader-dashboard-with-subscription.png)

### Удаление подписки и загруженных данных

Давайте очистим подписку и загруженные данные перед переходом к следующему упражнению.

Снова войдите в контейнер wis2downloader:

```bash
python3 wis2box-ctl.py login wis2downloader
```

и удалите подписку, используя следующую команду:

```bash
wis2downloader remove-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Посетите панель мониторинга Grafana, чтобы убедиться, что подписка была удалена и загрузки остановлены. Вы должны увидеть, что подписка исчезла из верхнего левого угла панели.

**Подождите несколько минут, пока панель не покажет, что загрузки остановлены.**

Наконец, вы можете удалить загруженные данные с помощью следующей команды в контейнере wis2downloader:

```bash
rm -rf app/data/downloads/*
```

!!! note
    
    Директория `app/data/downloads` в контейнере wis2downloader сопоставлена с директорией `downloads` в `WIS2BOX_HOST_DATADIR`, как это определено в вашем файле `wis2box.env`. Команда выше удаляет все загруженные данные.

Выйдите из контейнера wis2downloader, введя `exit`:
    
```bash
exit
```

Проверьте, что директория загрузок на вашем хосте снова пуста:

```bash
ls -R ~/wis2box-data/downloads
```

!!! note "О шлюзах GTS-to-WIS2"
    В настоящее время существуют два шлюза GTS-to-WIS2, которые публикуют данные через WIS2 Global Broker и Global Caches:

- DWD (Германия): centre-id=*de-dwd-gts-to-wis2*  
- JMA (Япония): centre-id=*jp-jma-gts-to-wis2*  

Если в предыдущем упражнении вы замените `de-dwd-gts-to-wis2` на `jp-jma-gts-to-wis2`, вы получите уведомления и данные, публикуемые шлюзом JMA GTS-to-WIS2.

!!! note "Темы origin vs cache"

    При подписке на тему, начинающуюся с `origin/`, вы будете получать уведомления с каноническим URL, который указывает на сервер данных, предоставляемый WIS-центром, публикующим данные.

    При подписке на тему, начинающуюся с `cache/`, вы будете получать несколько уведомлений для одних и тех же данных, по одному для каждого Global Cache. Каждое уведомление будет содержать канонический URL, указывающий на сервер данных соответствующего Global Cache. Программа wis2downloader загрузит данные с первого канонического URL, к которому сможет подключиться.

## Загрузка примерных данных из WIS2 Training Broker

В этом упражнении вы подпишетесь на WIS2 Training Broker, который публикует примерные данные для учебных целей.

### Изменение конфигурации wis2downloader

Это демонстрирует, как подписаться на брокера, который не является брокером по умолчанию, и позволит вам загрузить данные, публикуемые через WIS2 Training Broker.

Отредактируйте файл `wis2box.env` и измените `DOWNLOAD_BROKER_HOST` на `wis2training-broker.wis2dev.io`, `DOWNLOAD_BROKER_PORT` на `1883` и `DOWNLOAD_BROKER_TRANSPORT` на `tcp`:

```copy
# настройки загрузчика
DOWNLOAD_BROKER_HOST=wis2training-broker.wis2dev.io
DOWNLOAD_BROKER_PORT=1883
DOWNLOAD_BROKER_USERNAME=everyone
DOWNLOAD_BROKER_PASSWORD=everyone
# механизм передачи данных (tcp или websockets)
DOWNLOAD_BROKER_TRANSPORT=tcp
```

Дважды проверьте, что внесенные изменения соответствуют указанным выше, выполнив команду:

```bash
cat ~/wis2box/wis2box.env | grep DOWNLOAD
```

Затем выполните команду 'restart', чтобы применить изменения:

```bash
python3 wis2box-ctl.py restart
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

Теперь мы настроим новую подписку на тему для загрузки данных о траекториях циклонов из WIS2 Training Broker.

Войдите в контейнер **wis2downloader**:

```bash
python3 wis2box-ctl.py login wis2downloader
```

И выполните следующую команду (скопируйте и вставьте, чтобы избежать ошибок):

```bash
wis2downloader add-subscription --topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
```

Выйдите из контейнера **wis2downloader**, введя `exit`.

### Проверка загруженных данных

Подождите, пока в панели управления wis2downloader в Grafana не начнется загрузка данных.

Убедитесь, что данные были загружены, снова проверив логи wis2downloader:

```bash
docker logs wis2downloader
```

Вы должны увидеть сообщение в логах, похожее на следующее:

```copy
[...] INFO - Message received under topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
[...] INFO - Downloaded A_JSXX05ECEP020000_C_ECMP_...
```

Проверьте содержимое каталога загрузок снова:

```bash
ls -R ~/wis2box-data/downloads
```

Вы должны увидеть новый каталог с именем `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory`, содержащий загруженные данные.

!!! question "Просмотр загруженных данных"
    
    Какой формат файла у загруженных данных?

??? success "Нажмите, чтобы увидеть ответ"

    Загруженные данные находятся в формате BUFR, что указано расширением файла `.bufr`.

Теперь попробуйте добавить еще две подписки для загрузки данных о месячных аномалиях температуры поверхности и глобальных прогнозах ансамблей из следующих тем:

- `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/global`
- `origin/a/wis2/int-wis2-training/data/core/climate/experimental/anomalies/monthly/surface-temperature`

Подождите, пока в панели управления wis2downloader в Grafana не начнется загрузка данных.

Снова проверьте содержимое каталога загрузок:

```bash
ls -R ~/wis2box-data/downloads
```

Вы должны увидеть новые каталоги, соответствующие темам, на которые вы подписались, содержащие загруженные данные.

## Заключение

!!! success "Поздравляем!"

    В этом практическом занятии вы научились:

    - использовать 'wis2downloader' для подписки на WIS2 Broker и загрузки данных на локальную систему
    - просматривать статус загрузок в панели управления Grafana
    - изменять конфигурацию wis2downloader для подписки на другого брокера
    - просматривать загруженные данные на локальной системе