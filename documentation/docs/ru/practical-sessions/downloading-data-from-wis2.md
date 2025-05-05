---
title: Загрузка и декодирование данных из WIS2
---

# Загрузка и декодирование данных из WIS2

!!! abstract "Результаты обучения!"

    По завершении этого практического занятия вы сможете:

    - использовать "wis2downloader" для подписки на уведомления о данных WIS2 и загрузки данных в вашу локальную систему
    - просматривать статус загрузок в панели мониторинга Grafana
    - декодировать загруженные данные с помощью контейнера "decode-bufr-jupyter"

## Введение

В этом занятии вы научитесь настраивать подписку на WIS2 Broker и автоматически загружать данные в вашу локальную систему с помощью сервиса "wis2downloader", включенного в wis2box.

!!! note "О wis2downloader"
     
     Wis2downloader также доступен как отдельный сервис, который можно запустить на системе, отличной от той, которая публикует уведомления WIS2. Смотрите [wis2downloader](https://pypi.org/project/wis2downloader/) для получения дополнительной информации об использовании wis2downloader как отдельного сервиса.

     Если вы хотите разработать собственный сервис для подписки на уведомления WIS2 и загрузки данных, вы можете использовать [исходный код wis2downloader](https://github.com/World-Meteorological-Organization/wis2downloader) в качестве примера.

!!! Другие инструменты для доступа к данным WIS2

    Следующие инструменты также могут использоваться для поиска и доступа к данным из WIS2:

    - [pywiscat](https://github.com/wmo-im/pywiscat) предоставляет возможности поиска в WIS2 Global Discovery Catalogue для поддержки отчетности и анализа каталога WIS2 и связанных с ним метаданных
    - [pywis-pubsub](https://github.com/World-Meteorological-Organization/pywis-pubsub) предоставляет возможности подписки и загрузки данных ВМО из инфраструктурных сервисов WIS2

## Подготовка

Перед началом войдите в вашу учебную виртуальную машину и убедитесь, что ваш экземпляр wis2box запущен и работает.

## Просмотр панели мониторинга wis2downloader в Grafana

Откройте веб-браузер и перейдите к панели мониторинга Grafana вашего экземпляра wis2box по адресу `http://YOUR-HOST:3000`.

Нажмите на "панели мониторинга" в левом меню, затем выберите **панель мониторинга wis2downloader**.

Вы должны увидеть следующую панель:

![панель мониторинга wis2downloader](../assets/img/wis2downloader-dashboard.png)

Эта панель основана на метриках, публикуемых сервисом wis2downloader, и покажет вам статус текущих загрузок.

В верхнем левом углу вы можете видеть активные в данный момент подписки.

Оставьте эту панель открытой, так как вы будете использовать её для мониторинга прогресса загрузки в следующем упражнении.

## Проверка конфигурации wis2downloader

Сервис wis2downloader, запускаемый стеком wis2box, можно настроить с помощью переменных окружения, определенных в вашем файле wis2box.env.

Следующие переменные окружения используются wis2downloader:

    - DOWNLOAD_BROKER_HOST: Имя хоста MQTT брокера для подключения. По умолчанию globalbroker.meteo.fr
    - DOWNLOAD_BROKER_PORT: Порт MQTT брокера для подключения. По умолчанию 443 (HTTPS для websockets)
    - DOWNLOAD_BROKER_USERNAME: Имя пользователя для подключения к MQTT брокеру. По умолчанию everyone
    - DOWNLOAD_BROKER_PASSWORD: Пароль для подключения к MQTT брокеру. По умолчанию everyone
    - DOWNLOAD_BROKER_TRANSPORT: websockets или tcp, механизм транспорта для подключения к MQTT брокеру. По умолчанию websockets
    - DOWNLOAD_RETENTION_PERIOD_HOURS: Период хранения загруженных данных в часах. По умолчанию 24
    - DOWNLOAD_WORKERS: Количество рабочих процессов загрузки. По умолчанию 8. Определяет количество параллельных загрузок
    - DOWNLOAD_MIN_FREE_SPACE_GB: Минимальное свободное пространство в ГБ для хранения загрузок. По умолчанию 1

Чтобы просмотреть текущую конфигурацию wis2downloader, используйте следующую команду:

```bash
cat ~/wis2box/wis2box.env | grep DOWNLOAD
```

!!! question "Проверка конфигурации wis2downloader"
    
    Какой MQTT брокер используется по умолчанию для подключения wis2downloader?

    Какой период хранения данных установлен по умолчанию?

??? success "Нажмите, чтобы увидеть ответ"

    MQTT брокер по умолчанию для подключения wis2downloader - `globalbroker.meteo.fr`.

    Период хранения данных по умолчанию - 24 часа.

!!! note "Обновление конфигурации wis2downloader"

    Для обновления конфигурации wis2downloader вы можете отредактировать файл wis2box.env. Чтобы применить изменения, повторно запустите команду запуска стека wis2box:

    ```bash
    python3 wis2box-ctl.py start
    ```

    И вы увидите, как сервис wis2downloader перезапустится с новой конфигурацией.

Для целей этого упражнения вы можете оставить конфигурацию по умолчанию.

## Добавление подписок в wis2downloader

Внутри контейнера **wis2downloader** вы можете использовать командную строку для просмотра, добавления и удаления подписок.

Чтобы войти в контейнер **wis2downloader**, используйте следующую команду:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Затем используйте следующую команду для просмотра активных подписок:

```bash
wis2downloader list-subscriptions
```

Эта команда вернет пустой список, так как в данный момент нет активных подписок.

Для целей этого упражнения мы подпишемся на тему `cache/a/wis2/de-dwd-gts-to-wis2/#`, чтобы подписаться на данные, публикуемые шлюзом GTS-to-WIS2 DWD, и загружать уведомления из Global Cache.

Чтобы добавить эту подписку, используйте следующую команду:

```bash
wis2downloader add-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Затем выйдите из контейнера **wis2downloader**, набрав `exit`:

```bash
exit
```

Проверьте панель мониторинга wis2downloader в Grafana, чтобы увидеть новую добавленную подписку. Подождите несколько минут, и вы должны увидеть начало первых загрузок. Переходите к следующему упражнению, когда убедитесь, что загрузки начались.

## Просмотр загруженных данных

Сервис wis2downloader в стеке wis2box загружает данные в директорию 'downloads' в каталоге, который вы определили как WIS2BOX_HOST_DATADIR в вашем файле wis2box.env. Чтобы просмотреть содержимое директории downloads, используйте следующую команду:

```bash
ls -R ~/wis2box-data/downloads
```

Обратите внимание, что загруженные данные хранятся в директориях, названных в соответствии с темой, по которой было опубликовано уведомление WIS2.

## Удаление подписок из wis2downloader

Теперь снова войдите в контейнер wis2downloader:

```bash
python3 wis2box-ctl.py login wis2downloader
```

и удалите созданную вами подписку из wis2downloader, используя следующую команду:

```bash
wis2downloader remove-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

И выйдите из контейнера wis2downloader, набрав `exit`:
    
```bash
exit
```

Проверьте панель мониторинга wis2downloader в Grafana, чтобы увидеть удаление подписки. Вы должны увидеть, что загрузки прекратились.

## Загрузка и декодирование данных для траектории тропического циклона

В этом упражнении вы подпишетесь на учебный брокер WIS2, который публикует примеры данных для обучения. Вы настроите подписку для загрузки данных о траектории тропического циклона. Затем вы декодируете загруженные данные с помощью контейнера "decode-bufr-jupyter".

### Подписка на wis2training-broker и настройка новой подписки

Это демонстрирует, как подписаться на брокер, отличный от брокера по умолчанию, и позволит вам загружать данные, публикуемые учебным брокером WIS2.

Отредактируйте файл wis2box.env и измените DOWNLOAD_BROKER_HOST на `wis2training-broker.wis2dev.io`, DOWNLOAD_BROKER_PORT на `1883` и DOWNLOAD_BROKER_TRANSPORT на `tcp`:

```copy
# downloader settings
DOWNLOAD_BROKER_HOST=wis2training-broker.wis2dev.io
DOWNLOAD_BROKER_PORT=1883
DOWNLOAD_BROKER_USERNAME=everyone
DOWNLOAD_BROKER_PASSWORD=everyone
# download transport mechanism (tcp or websockets)
DOWNLOAD_BROKER_TRANSPORT=tcp
```

Затем снова запустите команду 'start' для применения изменений:

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

Теперь мы настроим новую подписку на тему для загрузки данных о траектории циклона из учебного брокера WIS2.

Войдите в контейнер **wis2downloader**:

```bash
python3 wis2box-ctl.py login wis2downloader
```

И выполните следующую команду (скопируйте и вставьте, чтобы избежать опечаток):

```bash
wis2downloader add-subscription --topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
```

Выйдите из контейнера **wis2downloader**, набрав `exit`.

Подождите, пока не увидите начало загрузок на панели мониторинга wis2downloader в Grafana.

!!! note "Загрузка данных из учебного брокера WIS2"

    Учебный брокер WIS2 - это тестовый брокер, который используется для обучения и может не публиковать данные постоянно.

    Во время очных учебных сессий местный инструктор обеспечит публикацию данных учебным брокером WIS2 для загрузки.

    Если вы выполняете это упражнение вне учебной сессии, вы можете не увидеть загружаемых данных.

Проверьте, что данные были загружены, снова просмотрев логи wis2downloader:

```bash
docker logs wis2downloader
```

Вы должны увидеть сообщение в логах, похожее на следующее:

```copy
[...] INFO - Message received under topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
[...] INFO - Downloaded A_JSXX05ECEP020000_C_ECMP_...
```

### Декодирование загруженных данных

Чтобы продемонстрировать, как вы можете декодировать загруженные данные, мы запустим новый контейнер, используя образ 'decode-bufr-jupyter'.

Этот контейнер запустит сервер Jupyter notebook на вашем экземпляре, который включает библиотеку "ecCodes", которую вы можете использовать для декодирования данных BUFR.

Мы будем использовать примеры блокнотов, включенные в `~/exercise-materials/notebook-examples`, для декодирования загруженных данных о траекториях циклонов.

Чтобы запустить контейнер, используйте следующую команду:

```bash
docker run -d --name decode-bufr-jupyter \
    -v ~/wis2box-data/downloads:/root/downloads \
    -p 8888:8888 \
    -e JUPYTER_TOKEN=dataismagic! \
    mlimper/decode-bufr-jupyter
```

!!! note "О контейнере decode-bufr-jupyter