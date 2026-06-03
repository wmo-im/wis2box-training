---
title: Инициализация wis2box
---

# Инициализация wis2box

!!! abstract "Результаты обучения"

    К концу этого практического занятия вы сможете:

    - запустить скрипт `wis2box-create-config.py` для создания начальной конфигурации
    - запустить wis2box и проверить статус его компонентов
    - просмотреть содержимое **wis2box-api**
    - получить доступ к **wis2box-webapp**
    - подключиться к локальному **wis2box-broker** с помощью MQTT Explorer

!!! note

    Текущие учебные материалы основаны на версии wis2box-release 1.3.0. 
    
    См. [accessing-your-student-vm](./accessing-your-student-vm.md) для инструкций по загрузке и установке программного обеспечения wis2box, если вы проходите обучение вне локальной учебной сессии.

## Подготовка

Войдите в свою виртуальную машину (VM) с использованием имени пользователя и пароля и убедитесь, что вы находитесь в каталоге `wis2box`:

```bash
cd ~/wis2box
```

## Создание начальной конфигурации

Для начальной конфигурации wis2box требуется:

- файл окружения `wis2box.env`, содержащий параметры конфигурации
- каталог на хост-машине, который будет использоваться совместно между хост-машиной и контейнерами wis2box, определяемый переменной окружения `WIS2BOX_HOST_DATADIR`

Скрипт `wis2box-create-config.py` может быть использован для создания начальной конфигурации вашего wis2box. 

Он задаст вам ряд вопросов для настройки конфигурации.

После завершения работы скрипта вы сможете просмотреть и обновить файлы конфигурации.

Запустите скрипт следующим образом:

```bash
python3 wis2box-create-config.py
```

### Каталог wis2box-host-data

Скрипт попросит вас указать каталог, который будет использоваться для переменной окружения `WIS2BOX_HOST_DATADIR`.

Обратите внимание, что необходимо указать полный путь к этому каталогу.

Например, если ваше имя пользователя — `username`, полный путь к каталогу будет `/home/username/wis2box-data`:

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

### URL wis2box

Далее вас попросят указать URL для вашего wis2box. Это URL, который будет использоваться для доступа к веб-приложению, API и пользовательскому интерфейсу wis2box.

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

### Пароли WEBAPP, STORAGE и BROKER

Вы можете использовать опцию случайной генерации паролей, когда вас попросят указать `WIS2BOX_WEBAPP_PASSWORD`, `WIS2BOX_STORAGE_PASSWORD`, `WIS2BOX_BROKER_PASSWORD`, или задать свои собственные.

Не беспокойтесь о запоминании этих паролей, они будут сохранены в файле `wis2box.env` в вашем каталоге wis2box.

### Проверка `wis2box.env`

После завершения работы скрипта проверьте содержимое файла `wis2box.env` в текущем каталоге:

```bash
cat ~/wis2box/wis2box.env
```

Или проверьте содержимое файла через WinSCP.

!!! question

    Какое значение имеет WISBOX_BASEMAP_URL в файле wis2box.env?

??? success "Нажмите, чтобы увидеть ответ"

    Значение по умолчанию для WIS2BOX_BASEMAP_URL — `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`.

    Этот URL относится к серверу тайлов OpenStreetMap. Если вы хотите использовать другого поставщика карт, вы можете изменить этот URL, указав другой сервер тайлов.

!!! question 

    Какое значение имеет переменная окружения WIS2BOX_STORAGE_DATA_RETENTION_DAYS в файле wis2box.env?

??? success "Нажмите, чтобы увидеть ответ"

    Значение по умолчанию для WIS2BOX_STORAGE_DATA_RETENTION_DAYS — 30 дней. Вы можете изменить это значение на другое количество дней, если хотите.
    
    Контейнер wis2box-management ежедневно выполняет cron-задачу для удаления данных, старше указанного количества дней, из корзины `wis2box-public` и API-бэкенда:
    
    ```{.copy}
    0 0 * * * su wis2box -c "wis2box data clean --days=$WIS2BOX_STORAGE_DATA_RETENTION_DAYS"
    ```

!!! note

    Файл `wis2box.env` содержит переменные окружения, определяющие конфигурацию вашего wis2box. Для получения дополнительной информации обратитесь к [wis2box-documentation](https://docs.wis2box.wis.wmo.int/en/latest/reference/configuration.html).

    Не редактируйте файл `wis2box.env`, если вы не уверены в изменениях, которые собираетесь внести. Неправильные изменения могут привести к прекращению работы wis2box.

    Не делитесь содержимым файла `wis2box.env` с кем-либо, так как он содержит конфиденциальную информацию, такую как пароли.

## Запуск wis2box

Убедитесь, что вы находитесь в каталоге, содержащем файлы определения программного стека wis2box:

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
Current version=Undefined, latest version=1.3.0
Would you like to update ? (y/n/exit)
```

Выберите ``y``, и скрипт создаст файл ``docker-compose.images-1.3.0.yml``, загрузит необходимые Docker-образы и запустит сервисы.

Загрузка образов может занять некоторое время в зависимости от скорости вашего интернет-соединения. Этот шаг требуется только при первом запуске wis2box.

Проверьте статус с помощью следующей команды:

```{.copy}
python3 wis2box-ctl.py status
```

Повторяйте эту команду, пока все сервисы не будут запущены.

!!! note "wis2box и Docker"
    wis2box работает как набор контейнеров Docker, управляемых с помощью docker-compose.
    
    Сервисы определены в различных файлах `docker-compose*.yml`, которые можно найти в каталоге `~/wis2box/`.
    
    Python-скрипт `wis2box-ctl.py` используется для выполнения команд Docker Compose, управляющих сервисами wis2box.

    Вам не нужно знать детали контейнеров Docker для работы с программным стеком wis2box, но вы можете изучить файлы `docker-compose*.yml`, чтобы увидеть, как определены сервисы. Если вы хотите узнать больше о Docker, вы можете найти дополнительную информацию в [документации Docker](https://docs.docker.com/).

Чтобы войти в контейнер wis2box-management, используйте следующую команду:

```{.copy}
python3 wis2box-ctl.py login
```

Обратите внимание, что после входа ваш приглашение изменится, указывая, что вы теперь находитесь внутри контейнера wis2box-management:

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

Запустите следующую команду, чтобы увидеть запущенные контейнеры Docker на вашей хост-машине:

```{.copy}
docker ps --format "table {{.Names}} \t{{.Status}} \t{{.Image}}"
```

Вы должны увидеть следующие запущенные контейнеры:

```{bash}
NAMES                     STATUS                         IMAGE
nginx                     Up 56 seconds                  nginx:1.30.1-alpine
mqtt_metrics_collector    Up 58 seconds                  ghcr.io/world-meteorological-organization/wis2box-mqtt-metrics-collector:1.3.0
wis2box-auth              Up 59 seconds                  ghcr.io/world-meteorological-organization/wis2box-auth:1.3.0
wis2box-ui                Up About a minute              ghcr.io/world-meteorological-organization/wis2box-ui:1.3.0
wis2box-management        Up About a minute              ghcr.io/world-meteorological-organization/wis2box-management:1.3.0
wis2box-minio             Up 2 minutes (healthy)         ghcr.io/world-meteorological-organization/wis2box-minio:latest
wis2box-api               Up About a minute (healthy)    ghcr.io/world-meteorological-organization/wis2box-api:1.3.0
elasticsearch             Up 2 minutes (healthy)         docker.elastic.co/elasticsearch/elasticsearch:8.6.2
grafana                   Up 2 minutes                   grafana/grafana-oss:12.4.2
loki                      Up 2 minutes                   grafana/loki:2.4.1
elasticsearch-exporter    Up 2 minutes                   quay.io/prometheuscommunity/elasticsearch-exporter:latest
prometheus                Up 2 minutes                   prom/prometheus:v2.37.0
mosquitto                 Up 2 minutes                   ghcr.io/world-meteorological-organization/wis2box-broker:1.3.0
wis2box-webapp            Up 2 minutes (healthy)         ghcr.io/world-meteorological-organization/wis2box-webapp:1.3.0
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

Wis2box содержит API (интерфейс прикладного программирования), который предоставляет доступ к данным и процессы для интерактивной визуализации, преобразования данных и их публикации.

Откройте новую вкладку и перейдите на страницу `http://YOUR-HOST/oapi`.

<img alt="wis2box-api.png" src="/../assets/img/wis2box-api.png" width="800">

Это главная страница API wis2box (работает через контейнер **wis2box-api**).

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
    
    Вы увидите, что на странице указано "No items", так как уведомления о данных еще не были опубликованы.

## wis2box webapp

Откройте веб-браузер и перейдите на страницу `http://YOUR-HOST/wis2box-webapp`.

Вы увидите всплывающее окно с запросом имени пользователя и пароля. Используйте имя пользователя по умолчанию `wis2box-user` и пароль `WIS2BOX_WEBAPP_PASSWORD`, указанный в файле `wis2box.env`, и нажмите "Sign in":

!!! note 

    Проверьте ваш файл wis2box.env для значения переменной WIS2BOX_WEBAPP_PASSWORD. Вы можете использовать следующую команду, чтобы проверить значение этой переменной окружения:

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_WEBAPP_PASSWORD
    ```

После входа в систему наведите курсор на меню слева, чтобы увидеть доступные опции в веб-приложении wis2box:

<img alt="wis2box-webapp-menu.png" src="/../assets/img/wis2box-webapp-menu.png" width="400">

Это веб-приложение wis2box, которое позволяет вам взаимодействовать с вашим wis2box:

- создавать и управлять наборами данных
- обновлять/просматривать метаданные станций
- загружать ручные наблюдения с использованием формы FM-12 synop
- отслеживать уведомления, опубликованные на вашем wis2box-broker

Мы будем использовать это веб-приложение в следующем занятии.

## wis2box-broker

Откройте MQTT Explorer на вашем компьютере и подготовьте новое подключение для подключения к вашему брокеру (работает через контейнер **wis2box-broker**).

Нажмите `+`, чтобы добавить новое подключение:

<img alt="mqtt-explorer-new-connection.png" src="/../assets/img/mqtt-explorer-new-connection.png" width="300">

Вы можете нажать кнопку 'ADVANCED' и убедиться, что у вас есть подписки на следующие темы:

- `#`
- `$SYS/#`

<img alt="mqtt-explorer-topics.png" src="/../assets/img/mqtt-explorer-topics.png" width="550">

!!! note

    Тема `#` является подпиской с подстановочным знаком, которая подписывается на все темы, опубликованные на брокере.

    Сообщения, опубликованные в теме `$SYS`, являются системными сообщениями, опубликованными самим сервисом mosquitto.

Используйте следующие данные для подключения, убедившись, что вы заменили значение `<your-host>` на имя вашего хоста, а `<WIS2BOX_BROKER_PASSWORD>` на значение из вашего файла `wis2box.env`:

- **Protocol: mqtt://**
- **Host: `<your-host>`**
- **Port: 1883**
- **Username: wis2box**
- **Password: `<WIS2BOX_BROKER_PASSWORD>`**

!!! note 

    Вы можете проверить ваш файл wis2box.env для значения переменной WIS2BOX_BROKER_PASSWORD. Вы можете использовать следующую команду, чтобы проверить значение этой переменной окружения:

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_BROKER_PASSWORD
    ```

    Обратите внимание, что это ваш **внутренний** пароль брокера, Global Broker будет использовать другие (только для чтения) учетные данные для подписки на ваш брокер. Никогда не делитесь этим паролем с кем-либо.

Убедитесь, что вы нажали "SAVE", чтобы сохранить данные подключения.

Затем нажмите "CONNECT", чтобы подключиться к вашему **wis2box-broker**.

<img alt="mqtt-explorer-wis2box-broker-port1883.png" src="/../assets/img/mqtt-explorer-wis2box-broker-port1883.png" width="700">

После подключения вы увидите внутреннюю статистику mosquitto, опубликованную вашим брокером в теме `$SYS`:

<img alt="mqtt-explorer-sys-topic.png" src="/../assets/img/mqtt-explorer-sys-topic.png" width="400">

То же самое подключение также может быть выполнено с использованием MQTT через WebSockets на порту 80, используя следующие данные подключения:

<img alt="mqtt-explorer-wis2box-broker-websockets.png" src="/../assets/img/mqtt-explorer-wis2box-broker-websockets.png" width="700">

## Заключение

!!! success "Поздравляем!"
    В этом практическом занятии вы узнали, как:

    - запустить скрипт `wis2box-create-config.py` для создания начальной конфигурации
    - запустить wis2box и проверить статус его компонентов
    - получить доступ к wis2box-webapp и wis2box-API через браузер
    - подключиться к MQTT брокеру на вашей виртуальной машине с помощью MQTT Explorer
```