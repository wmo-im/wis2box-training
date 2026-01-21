---
title: Инициализация wis2box
---

# Инициализация wis2box

!!! abstract "Результаты обучения"

    К концу этой практической сессии вы сможете:

    - запустить скрипт `wis2box-create-config.py` для создания начальной конфигурации
    - запустить wis2box и проверить статус его компонентов
    - просмотреть содержимое **wis2box-api**
    - получить доступ к **wis2box-webapp**
    - подключиться к локальному **wis2box-broker** с использованием MQTT Explorer

!!! note

    Текущие учебные материалы основаны на версии wis2box-release 1.2.0. 
    
    См. [accessing-your-student-vm](./accessing-your-student-vm.md) для инструкций по загрузке и установке программного стека wis2box, если вы проходите это обучение вне локальной учебной сессии.

## Подготовка

Войдите в свою выделенную виртуальную машину (VM) с использованием имени пользователя и пароля и убедитесь, что вы находитесь в директории `wis2box`:

```bash
cd ~/wis2box
```

## Создание начальной конфигурации

Для начальной конфигурации wis2box требуется:

- файл окружения `wis2box.env`, содержащий параметры конфигурации
- директория на хост-машине для совместного использования между хост-машиной и контейнерами wis2box, определяемая переменной окружения `WIS2BOX_HOST_DATADIR`

Скрипт `wis2box-create-config.py` может быть использован для создания начальной конфигурации вашего wis2box. 

Он задаст вам ряд вопросов для настройки конфигурации.

После завершения работы скрипта вы сможете просмотреть и обновить файлы конфигурации.

Запустите скрипт следующим образом:

```bash
python3 wis2box-create-config.py
```

### Директория wis2box-host-data

Скрипт попросит вас указать директорию, которая будет использоваться для переменной окружения `WIS2BOX_HOST_DATADIR`.

Обратите внимание, что необходимо указать полный путь к этой директории.

Например, если ваше имя пользователя — `username`, полный путь к директории будет `/home/username/wis2box-data`:

```{.copy}
username@student-vm-username:~/wis2box$ python3 wis2box-create-config.py
Please enter the directory to be used for WIS2BOX_HOST_DATADIR:
/home/username/wis2box-data
The directory to be used for WIS2BOX_HOST_DATADIR will be set to:
    /home/username/wis2box-data
Is this correct? (y/n/exit)
y
The directory /home/username/wis2box-data has been created.
```

### URL для wis2box

Далее вам будет предложено ввести URL для вашего wis2box. Это URL, который будет использоваться для доступа к веб-приложению, API и интерфейсу wis2box.

Используйте `http://<your-hostname-or-ip>` в качестве URL.

```{.copy}
Please enter the URL of the wis2box:
 For local testing the URL is http://localhost
 To enable remote access, the URL should point to the public IP address or domain name of the server hosting the wis2box.
http://username.training.wis2dev.io
The URL of the wis2box will be set to:
  http://username.training.wis2dev.io
Is this correct? (y/n/exit)
```

### Пароли для WEBAPP, STORAGE и BROKER

Вы можете использовать опцию генерации случайных паролей при вводе `WIS2BOX_WEBAPP_PASSWORD`, `WIS2BOX_STORAGE_PASSWORD`, `WIS2BOX_BROKER_PASSWORD` или задать свои собственные.

Не беспокойтесь о запоминании этих паролей, они будут сохранены в файле `wis2box.env` в вашей директории wis2box.

### Проверка `wis2box.env`

После завершения работы скрипта проверьте содержимое файла `wis2box.env` в текущей директории:

```bash
cat ~/wis2box/wis2box.env
```

Или проверьте содержимое файла через WinSCP.

!!! question

    Какое значение имеет WISBOX_BASEMAP_URL в файле wis2box.env?

??? success "Нажмите, чтобы увидеть ответ"

    Значение по умолчанию для WIS2BOX_BASEMAP_URL — `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`.

    Этот URL ссылается на сервер тайлов OpenStreetMap. Если вы хотите использовать другого поставщика карт, вы можете изменить этот URL, чтобы он указывал на другой сервер тайлов.

!!! question 

    Какое значение имеет переменная окружения WIS2BOX_STORAGE_DATA_RETENTION_DAYS в файле wis2box.env?

??? success "Нажмите, чтобы увидеть ответ"

    Значение по умолчанию для WIS2BOX_STORAGE_DATA_RETENTION_DAYS — 30 дней. Вы можете изменить это значение на другое количество дней, если хотите.
    
    Контейнер wis2box-management выполняет ежедневное задание cron для удаления данных, старше указанного количества дней, из корзины `wis2box-public` и API-бэкенда:
    
    ```{.copy}
    0 0 * * * su wis2box -c "wis2box data clean --days=$WIS2BOX_STORAGE_DATA_RETENTION_DAYS"
    ```

!!! note

    Файл `wis2box.env` содержит переменные окружения, определяющие конфигурацию вашего wis2box. Для получения дополнительной информации обратитесь к [wis2box-documentation](https://docs.wis2box.wis.wmo.int/en/latest/reference/configuration.html).

    Не редактируйте файл `wis2box.env`, если вы не уверены в вносимых изменениях. Неправильные изменения могут привести к сбою работы wis2box.

    Не делитесь содержимым файла `wis2box.env` с кем-либо, так как он содержит конфиденциальную информацию, такую как пароли.

## Запуск wis2box

Убедитесь, что вы находитесь в директории, содержащей файлы определения программного стека wis2box:

```{.copy}
cd ~/wis2box
```

Запустите wis2box с помощью следующей команды:

```{.copy}
python3 wis2box-ctl.py start
```

При первом запуске этой команды вы увидите следующий вывод:

```
No docker-compose.images-*.yml files found, creating one
Current version=Undefined, latest version=1.2.0
Would you like to update ? (y/n/exit)
```

Выберите ``y``, и скрипт создаст файл ``docker-compose.images-1.2.0.yml``, загрузит необходимые образы Docker и запустит сервисы.

Загрузка образов может занять некоторое время в зависимости от скорости вашего интернет-соединения. Этот шаг требуется только при первом запуске wis2box.

Проверьте статус с помощью следующей команды:

```{.copy}
python3 wis2box-ctl.py status
```

Повторяйте эту команду, пока все сервисы не будут запущены.

!!! note "wis2box и Docker"
    wis2box работает как набор контейнеров Docker, управляемых с помощью docker-compose.
    
    Сервисы определены в различных файлах `docker-compose*.yml`, которые можно найти в директории `~/wis2box/`.
    
    Python-скрипт `wis2box-ctl.py` используется для выполнения базовых команд Docker Compose, управляющих сервисами wis2box.

    Вам не нужно знать детали контейнеров Docker для работы с программным стеком wis2box, но вы можете изучить файлы `docker-compose*.yml`, чтобы увидеть, как определены сервисы. Если вы хотите узнать больше о Docker, вы можете найти дополнительную информацию в [документации Docker](https://docs.docker.com/).

Чтобы войти в контейнер wis2box-management, используйте следующую команду:

```{.copy}
python3 wis2box-ctl.py login
```

Обратите внимание, что после входа ваш приглашение изменится, указывая, что вы находитесь внутри контейнера wis2box-management:

```{bash}
root@025381da3c40:/home/wis2box#
```

Внутри контейнера wis2box-management вы можете выполнять различные команды для управления вашим wis2box, такие как:

- `wis2box auth add-token --path processes/wis2box` : для создания токена авторизации для конечной точки *processes/wis2box*
- `wis2box data clean --days=<number-of-days>` : для очистки данных, старше определенного количества дней, из корзины *wis2box-public*

Чтобы выйти из контейнера и вернуться на хост-машину, используйте следующую команду:

```{.copy}
exit
```

Выполните следующую команду, чтобы увидеть запущенные контейнеры Docker на вашей хост-машине:

```{.copy}
docker ps --format "table {{.Names}} \t{{.Status}} \t{{.Image}}"
```

Вы должны увидеть следующие запущенные контейнеры:

```{bash}
NAMES                     STATUS                   IMAGE
elasticsearch            docker.elastic.co/elasticsearch/elasticsearch:8.6.2                              "/bin/tini -- /usr/l…"   elasticsearch            Около минуты назад   Работает около минуты (healthy)     9200/tcp, 9300/tcp
elasticsearch-exporter   quay.io/prometheuscommunity/elasticsearch-exporter:latest                        "/bin/elasticsearch_…"   elasticsearch-exporter   Около минуты назад   Работает около минуты               7979/tcp
grafana                  grafana/grafana-oss:9.0.3                                                        "/run.sh"                grafana                  Около минуты назад   Работает около минуты               0.0.0.0:3000->3000/tcp
loki                     grafana/loki:2.4.1                                                               "/usr/bin/loki -conf…"   loki                     Около минуты назад   Работает около минуты               3100/tcp
mosquitto                ghcr.io/world-meteorological-organization/wis2box-broker:1.2.0                   "/docker-entrypoint.…"   mosquitto                Около минуты назад   Работает около минуты               0.0.0.0:1883->1883/tcp, 0.0.0.0:8884->8884/tcp
mqtt_metrics_collector   ghcr.io/world-meteorological-organization/wis2box-mqtt-metrics-collector:1.2.0   "python3 -u mqtt_met…"   mqtt_metrics_collector   Около минуты назад   Работает 10 секунд                   8000/tcp, 0.0.0.0:8001->8001/tcp
nginx                    nginx:alpine                                                                     "/docker-entrypoint.…"   web-proxy                Около минуты назад   Работает 9 секунд                    0.0.0.0:80->80/tcp
prometheus               prom/prometheus:v2.37.0                                                          "/bin/prometheus --c…"   prometheus               Около минуты назад   Работает около минуты               9090/tcp
wis2box-api              ghcr.io/world-meteorological-organization/wis2box-api:1.2.0                      "/app/docker/es-entr…"   wis2box-api              Около минуты назад   Работает 36 секунд (healthy)         
wis2box-auth             ghcr.io/world-meteorological-organization/wis2box-auth:1.2.0                     "/entrypoint.sh"         wis2box-auth             Около минуты назад   Работает 10 секунд                   
wis2box-management       ghcr.io/world-meteorological-organization/wis2box-management:1.2.0               "/home/wis2box/entry…"   wis2box-management       Около минуты назад   Работает 12 секунд                   
wis2box-minio            minio/minio:RELEASE.2024-08-03T04-33-23Z-cpuv1                                   "/usr/bin/docker-ent…"   minio                    Около минуты назад   Работает около минуты (healthy)     0.0.0.0:8022->8022/tcp, 0.0.0.0:9000-9001->9000-9001/tcp
wis2box-ui               ghcr.io/world-meteorological-organization/wis2box-ui:1.2.0                       "/docker-entrypoint.…"   wis2box-ui               Около минуты назад   Работает 35 секунд                   0.0.0.0:9999->80/tcp
wis2box-webapp           ghcr.io/world-meteorological-organization/wis2box-webapp:1.2.0                   "sh /wis2box-webapp/…"   wis2box-webapp           Около минуты назад   Работает около минуты (unhealthy)   4173/tcp
wis2downloader           ghcr.io/wmo-im/wis2downloader:v0.3.2                                             "/home/wis2downloade…"   wis2downloader           Около минуты назад   Работает около минуты (healthy)

```

Эти контейнеры являются частью программного стека wis2box и предоставляют различные сервисы, необходимые для работы wis2box.

Выполните следующую команду, чтобы увидеть тома Docker, работающие на вашем хосте:

```{.copy}
docker volume ls
```

Вы должны увидеть следующие тома:

- wis2box_project_auth-data
- wis2box_project_es-data
- wis2box_project_minio-data
- wis2box_project_prometheus-data
- wis2box_project_loki-data
- wis2box_project_mosquitto-config

А также некоторые анонимные тома, используемые различными контейнерами.

Тома, начинающиеся с `wis2box_project_`, используются для хранения постоянных данных для различных сервисов в программном стеке wis2box.

## wis2box API

wis2box содержит API (интерфейс прикладного программирования), который предоставляет доступ к данным и процессы для интерактивной визуализации, преобразования данных и их публикации.

Откройте новую вкладку и перейдите на страницу `http://YOUR-HOST/oapi`.

<img alt="wis2box-api.png" src="/../assets/img/wis2box-api.png" width="800">

Это главная страница API wis2box (работающего через контейнер **wis2box-api**).

!!! question
     
     Какие коллекции доступны в данный момент?

??? success "Нажмите, чтобы увидеть ответ"
    
    Чтобы увидеть коллекции, доступные через API, нажмите `View the collections in this service`:

    <img alt="wis2box-api-collections.png" src="/../assets/img/wis2box-api-collections.png" width="600">

    В настоящее время доступны следующие коллекции:

    - Станции
    - Уведомления о данных
    - Метаданные для обнаружения


!!! question

    Сколько уведомлений о данных было опубликовано?

??? success "Нажмите, чтобы увидеть ответ"

    Нажмите на "Data notifications", затем нажмите на `Browse through the items of "Data Notifications"`. 
    
    Вы увидите, что на странице написано "No items", так как уведомления о данных еще не были опубликованы.

## wis2box webapp

Откройте веб-браузер и перейдите на страницу `http://YOUR-HOST/wis2box-webapp`.

Вы увидите всплывающее окно с запросом имени пользователя и пароля. Используйте имя пользователя по умолчанию `wis2box-user` и пароль `WIS2BOX_WEBAPP_PASSWORD`, указанный в файле `wis2box.env`, затем нажмите "Sign in":

!!! note 

    Проверьте ваш файл wis2box.env, чтобы узнать значение переменной WIS2BOX_WEBAPP_PASSWORD. Вы можете использовать следующую команду, чтобы проверить значение этой переменной окружения:

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_WEBAPP_PASSWORD
    ```

После входа переместите мышь к меню слева, чтобы увидеть доступные опции в веб-приложении wis2box:

<img alt="wis2box-webapp-menu.png" src="/../assets/img/wis2box-webapp-menu.png" width="400">

Это веб-приложение wis2box, которое позволяет вам взаимодействовать с вашим wis2box:

- создавать и управлять наборами данных
- обновлять/просматривать метаданные станций
- загружать ручные наблюдения с использованием формы FM-12 synop
- отслеживать уведомления, опубликованные на вашем wis2box-broker

Мы будем использовать это веб-приложение в следующем занятии.

## wis2box-broker

Откройте MQTT Explorer на вашем компьютере и подготовьте новое подключение для соединения с вашим брокером (работающим через контейнер **wis2box-broker**).

Нажмите `+`, чтобы добавить новое подключение:

<img alt="mqtt-explorer-new-connection.png" src="/../assets/img/mqtt-explorer-new-connection.png" width="300">

Вы можете нажать кнопку 'ADVANCED' и убедиться, что у вас есть подписки на следующие темы:

- `#`
- `$SYS/#`

<img alt="mqtt-explorer-topics.png" src="/../assets/img/mqtt-explorer-topics.png" width="550">

!!! note

    Тема `#` — это подписка с подстановочным знаком, которая подписывается на все темы, опубликованные на брокере.

    Сообщения, опубликованные под темой `$SYS`, являются системными сообщениями, публикуемыми самим сервисом mosquitto.

Используйте следующие данные для подключения, убедившись, что вы заменили значение `<your-host>` на имя вашего хоста, а `<WIS2BOX_BROKER_PASSWORD>` на значение из вашего файла `wis2box.env`:

- **Протокол: mqtt://**
- **Хост: `<your-host>`**
- **Порт: 1883**
- **Имя пользователя: wis2box**
- **Пароль: `<WIS2BOX_BROKER_PASSWORD>`**

!!! note 

    Вы можете проверить ваш файл wis2box.env, чтобы узнать значение переменной WIS2BOX_BROKER_PASSWORD. Вы можете использовать следующую команду, чтобы проверить значение этой переменной окружения:

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_BROKER_PASSWORD
    ```

    Обратите внимание, что это ваш **внутренний** пароль брокера, Global Broker будет использовать другие (только для чтения) учетные данные для подписки на ваш брокер. Никогда не делитесь этим паролем с кем-либо.

Убедитесь, что вы нажали "SAVE", чтобы сохранить данные подключения.

Затем нажмите "CONNECT", чтобы подключиться к вашему **wis2box-broker**.

<img alt="mqtt-explorer-wis2box-broker.png" src="/../assets/img/mqtt-explorer-wis2box-broker.png" width="600">

После подключения проверьте, что внутренние статистические данные mosquitto публикуются вашим брокером в теме `$SYS`:

<img alt="mqtt-explorer-sys-topic.png" src="/../assets/img/mqtt-explorer-sys-topic.png" width="400">

Оставьте MQTT Explorer открытым, так как мы будем использовать его для мониторинга сообщений, публикуемых на брокере.

## Заключение

!!! success "Поздравляем!"
    В этом практическом занятии вы узнали, как:

    - запустить скрипт `wis2box-create-config.py` для создания начальной конфигурации
    - запустить wis2box и проверить статус его компонентов
    - получить доступ к wis2box-webapp и wis2box-API в браузере
    - подключиться к MQTT брокеру на вашей учебной виртуальной машине с использованием MQTT Explorer