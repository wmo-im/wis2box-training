---
title: Инициализация wis2box
---

# Инициализация wis2box

!!! abstract "Учебные результаты"

    К концу этой практической сессии вы сможете:

    - запустить скрипт `wis2box-create-config.py` для создания начальной конфигурации
    - запустить wis2box и проверить статус его компонентов
    - просмотреть содержимое **wis2box-api**
    - получить доступ к **wis2box-webapp**
    - подключиться к локальному **wis2box-broker** с использованием MQTT Explorer

!!! note

    Текущие учебные материалы основаны на версии wis2box-release 1.0.0.
    
    См. [accessing-your-student-vm](./accessing-your-student-vm.md) для инструкций по загрузке и установке программного стека wis2box, если вы проводите эту тренировку вне локальной учебной сессии.

## Подготовка

Войдите в вашу назначенную виртуальную машину с вашим именем пользователя и паролем и убедитесь, что вы находитесь в директории `wis2box`:

```bash
cd ~/wis2box
```

## Создание начальной конфигурации

Для начальной конфигурации wis2box требуется:

- файл окружения `wis2box.env`, содержащий параметры конфигурации
- директория на хост-машине для обмена между хост-машиной и контейнерами wis2box, определенная переменной окружения `WIS2BOX_HOST_DATADIR`

Скрипт `wis2box-create-config.py` можно использовать для создания начальной конфигурации вашего wis2box.

Он задаст вам ряд вопросов для настройки вашей конфигурации.

Вы сможете просмотреть и обновить файлы конфигурации после завершения работы скрипта.

Запустите скрипт следующим образом:

```bash
python3 wis2box-create-config.py
```

### Директория wis2box-host-data

Скрипт попросит вас ввести директорию для переменной окружения `WIS2BOX_HOST_DATADIR`.

Обратите внимание, что вам нужно определить полный путь к этой директории.

Например, если ваше имя пользователя `username`, полный путь к директории будет `/home/username/wis2box-data`:

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

Далее вас попросят ввести URL для вашего wis2box. Это URL, который будет использоваться для доступа к веб-приложению, API и UI wis2box.

Пожалуйста, используйте `http://<your-hostname-or-ip>` в качестве URL.

```{.copy}
Please enter the URL of the wis2box:
 For local testing the URL is http://localhost
 To enable remote access, the URL should point to the public IP address or domain name of the server hosting the wis2box.
http://username.wis2.training
The URL of the wis2box will be set to:
  http://username.wis2.training
Is this correct? (y/n/exit)
```

### Пароли WEBAPP, STORAGE и BROKER

Вы можете использовать опцию генерации случайного пароля, когда будете запрашивать `WIS2BOX_WEBAPP_PASSWORD`, `WIS2BOX_STORAGE_PASSWORD`, `WIS2BOX_BROKER_PASSWORD` и определить свой собственный.

Не беспокойтесь о запоминании этих паролей, они будут сохранены в файле `wis2box.env` в вашей директории wis2box.

### Просмотр `wis2box.env`

После завершения работы скриптов проверьте содержимое файла `wis2box.env` в вашей текущей директории:

```bash
cat ~/wis2box/wis2box.env
```

Или проверьте содержимое файла через WinSCP.

!!! question

    Каково значение WISBOX_BASEMAP_URL в файле wis2box.env?

??? success "Нажмите, чтобы увидеть ответ"

    Значение по умолчанию для WIS2BOX_BASEMAP_URL — `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`.

    Этот URL ссылается на сервер тайлов OpenStreetMap. Если вы хотите использовать другого поставщика карт, вы можете изменить этот URL, чтобы он указывал на другой сервер тайлов.

!!! question

    Каково значение переменной окружения WIS2BOX_STORAGE_DATA_RETENTION_DAYS в файле wis2box.env?

??? success "Нажмите, чтобы увидеть ответ"

    Значение по умолчанию для WIS2BOX_STORAGE_DATA_RETENTION_DAYS составляет 30 дней. Вы можете изменить это значение на другое количество дней, если хотите.
    
    Контейнер wis2box-management ежедневно запускает cronjob для удаления данных, старше определенного количества дней, определенного переменной WIS2BOX_STORAGE_DATA_RETENTION_DAYS, из корзины `wis2box-public` и бэкенда API:
    
    ```{.copy}
    0 0 * * * su wis2box -c "wis2box data clean --days=$WIS2BOX_STORAGE_DATA_RETENTION_DAYS"
    ```

!!! note

    Файл `wis2box.env` содержит переменные окружения, определяющие конфигурацию вашего wis2box. Для получения дополнительной информации см. [wis2box-documentation](https://docs.wis2box.wis.wmo.int/en/latest/reference/configuration.html).

    Не редактируйте файл `wis2box.env`, если вы не уверены в вносимых изменениях. Неправильные изменения могут привести к тому, что ваш wis2box перестанет работать.

    Не делитесь содержимым вашего файла `wis2box.env` с кем-либо, так как он содержит конфиденциальную информацию, такую как пароли.

## Запуск wis2box

Убедитесь, что вы находитесь в директории, содержащей файлы определения программного стека wis2box:

```{.copy}
cd ~/wis2box
```

Запустите wis2box следующей командой:

```{.copy}
python3 wis2box-ctl.py start
```

При первом запуске этой команды вы увидите следующий вывод:

```
No docker-compose.images-*.yml files found, creating one
Current version=Undefined, latest version=1.0.0
Would you like to update ? (y/n/exit)
```

Выберите ``y`` и скрипт создаст файл ``docker-compose.images-1.0.0.yml``, загрузит необходимые образы Docker и запустит сервисы.

Загрузка образов может занять некоторое время в зависимости от скорости вашего интернет-соединения. Этот шаг требуется только при первом запуске wis2box.

Проверьте статус следующей командой:

```{.copy}
python3 wis2box-ctl.py status
```

Повторяйте эту команду, пока все сервисы не будут запущены и работают.

!!! note "wis2box и Docker"
    wis2box работает как набор контейнеров Docker, управляемых docker-compose.
    
    Сервисы определены в различных `docker-compose*.yml`, которые можно найти в директории `~/wis2box/`.
    
    Python-скрипт `wis2box-ctl.py` используется для выполнения команд Docker Compose, которые управляют сервисами wis2box.

    Вам не нужно знать детали контейнеров Docker для работы с программным стеком wis2box, но вы можете изучить файлы `docker-compose*.yml`, чтобы увидеть, как определены сервисы. Если вы заинтересованы в изучении Docker, вы можете найти дополнительную информацию в [Docker documentation](https://docs.docker.com/).

Для входа в контейнер wis2box-management используйте следующую команду:

```{.copy}
python3 wis2box-ctl.py login
```

Внутри контейнера wis2box-management вы можете выполнить различные команды для управления вашим wis2box, такие как:

- `wis2box auth add-token --path processes/wis2box` : для создания токена авторизации для конечной точки `processes/wis2box`
- `wis2box data clean --days=<number-of-days>` : для очистки данных, старше определенного количества дней, из корзины `wis2box-public`

Для выхода из контейнера и возврата на хост-машину используйте следующую команду:

```{.copy}
exit
```

Выполните следующую команду, чтобы увидеть запущенные на вашей хост-машине контейнеры Docker:

```{.copy}
docker ps
```

Вы должны увидеть следующие запущенные контейнеры:

- wis2box-management
- wis2box-api
- wis2box-minio
- wis2box-webapp
- wis2box-auth
- wis2box-ui
- wis2downloader
- elasticsearch
- elasticsearch-exporter
- nginx
- mosquitto
- prometheus
- grafana
- loki

Эти контейнеры являются частью программного стека wis2box и обеспечивают различные сервисы, необходимые для работы wis2box.

Выполните следующую команду, чтобы увидеть запущенные на вашей хост-машине тома Docker:

```{.copy}
docker volume ls
```

Вы должны увидеть следующие тома:

- wis2box_project_auth-data
- wis2box_project_es-data
- wis2box_project_htpasswd
- wis2box_project_minio-data
- wis2box_project_prometheus-data
- wis2box_project_loki-data
- wis2box_project_mosquitto-config

А также некоторые анонимные тома, используемые различными контейнерами.

Тома, начинающиеся с `wis2box_project_`, используются для хранения постоянных данных для различных сервисов в программном стеке wis2box.

## wis2box API

wis2box содержит API (интерфейс программирования приложений), который предоставляет доступ к данным и процессы для интерактивной визуализации, трансформации данных и публикации.

Откройте новую вкладку и перейдите на страницу `http://YOUR-HOST/oapi`.

<img alt="wis2box-api.png" src="/../assets/img/wis2box-api.png" width="800">

Это главная страница API wis2box (работает через контейнер **wis2box-api**).

!!! question

     Какие коллекции в настоящее время доступны?

??? success "Нажмите, чтобы увидеть ответ"
    
    Чтобы просмотреть коллекции, в настоящее время доступные через API, нажмите `View the collections in this service`:

    <img alt="wis2box-api-collections.png" src="/../assets/img/wis2box-api-collections.png" width="600">

    В настоящее время доступны следующие коллекции:

    - Станции
    - Уведомления о данных
    - Метаданные обнаружения


!!! question

    Сколько уведомлений о данных было опубликовано?

??? success "Нажмите, чтобы увидеть ответ"

    Нажмите на "Уведомления о данных", затем нажмите `Browse through the items of "Data Notifications"`.
    
    Вы заметите, что на странице написано "Нет элементов", так как уведомления о данных еще не были опубликованы.

## wis2box webapp

Откройте веб-браузер и посетите страницу `http://YOUR-HOST/wis2box-webapp`.

Вы увидите всплывающее окно с запросом вашего имени пользователя и пароля. Используйте имя пользователя по умолчанию `wis2box-user` и `WIS2BOX_WEBAPP_PASSWORD`, определенный в файле `wis2box.env`, и нажмите "Войти":

!!! note

    Проверьте ваш wis2box.env на предмет значения вашего WIS2BOX_WEBAPP_PASSWORD. Вы можете использовать следующую команду, чтобы проверить значение этой переменной окружения:

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_WEBAPP_PASSWORD
    ```

После входа в систему переместите курсор мыши в меню слева, чтобы увидеть доступные опции в веб-приложении wis2box:

<img alt="wis2box-webapp-menu.png" src="/../assets/img/wis2box-webapp-menu.png" width="400">

Это веб-приложение wis2box позволяет вам взаимодействовать с вашим wis2box:

- создавать и управлять наборами данных
- обновлять/просматривать метаданные вашей станции
- загружать ручные наблюдения с использованием формы FM-12 synop
- мониторить уведомления, опубликованные на вашем wis2box-broker

Мы будем использовать это веб-приложение в последующих сессиях.

## wis2box-broker

Откройте MQTT Explorer на вашем компьютере и подготовьте новое подключение для подключения к вашему брокеру (работает через контейнер **wis2box-broker**).

Нажмите `+`, чтобы добавить новое подключение:

<img alt="mqtt-explorer-new-connection.png" src="/../assets/img/mqtt-explorer-new-connection.png" width="300">

Вы можете нажать кнопку 'ADVANCED' и убедиться, что у вас есть подписки на следующие темы:

- `#`
- `$SYS/#`

<img alt="mqtt-explorer-topics.png" src="/../assets/img/mqtt-explorer-topics.png" width="550">

!!! note

    Тема `#` является подпиской с шаблоном, которая подписывается на все темы, публикуемые на брокере.

    Сообщения, публикуемые под темой `$SYS`, являются системными сообщениями, публикуемыми самой службой mosquitto.

Используйте следующие данные для подключения, убедившись, что вы заменили значение `<your-host>` на ваше имя хоста и `<WIS2BOX_BROKER_PASSWORD>` на значение из вашего файла `wis2box.env`:

- **Протокол: mqtt://**
- **Хост: `<your-host>`**
- **Порт: 1883**
- **Имя пользователя: wis2box**
- **Пароль: `<WIS2

Как только вы подключитесь, убедитесь, что статистика внутреннего mosquitto публикуется вашим брокером в теме `$SYS`:

<img alt="mqtt-explorer-sys-topic.png" src="/../assets/img/mqtt-explorer-sys-topic.png" width="400">

Оставьте MQTT Explorer открытым, так как мы будем использовать его для мониторинга сообщений, публикуемых на брокере.

## Заключение

!!! success "Поздравляем!"
    В этом практическом занятии вы научились:

    - запускать скрипт `wis2box-create-config.py` для создания начальной конфигурации
    - запускать wis2box и проверять статус его компонентов
    - получать доступ к wis2box-webapp и wis2box-API в браузере
    - подключаться к MQTT брокеру на вашей учебной VM с использованием MQTT Explorer