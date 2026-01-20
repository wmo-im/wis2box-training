---
title: Подключение к WIS2 через MQTT
---

# Подключение к WIS2 через MQTT

!!! abstract "Результаты обучения"

    По завершении этой практической сессии вы сможете:

    - подключиться к WIS2 Global Broker с использованием MQTT Explorer
    - изучить структуру тем WIS2
    - изучить структуру уведомлений WIS2

## Введение

WIS2 использует протокол MQTT для уведомления о доступности данных о погоде, климате и водных ресурсах. WIS2 Global Broker подписывается на все WIS2 Nodes в сети и повторно публикует полученные сообщения. Global Cache подписывается на Global Broker, загружает данные из сообщения и затем повторно публикует сообщение в теме `cache` с новым URL. Global Discovery Catalogue публикует метаданные для поиска из Broker и предоставляет API для поиска.

Пример структуры уведомления WIS2 для сообщения, полученного по теме `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`:

```json
{
   "id":"3c14d7bf-e6b9-4f59-b4ea-f2fc52a33cd3",
   "type":"Feature",
   "conformsTo":[
      "http://wis.wmo.int/spec/wnm/1/conf/core"
   ],
   "geometry":{
      "coordinates":[
         -99.1964,
         19.404,
         2314
      ],
      "type":"Point"
   },
   "properties":{
      "data_id":"br-inmet:data:core:weather:surface-based-observations:synop/WIGOS_0-20000-0-76679_20250206T231600",
      "datetime":"2025-02-06T23:16:00Z",
      "pubtime":"2026-01-20T13:14:52Z",
      "integrity":{
         "method":"sha512",
         "value":"qtlI3Noay2I4zcdA1XCpn8vzVLIt0RKrR398VGFgTttc1XRUVb4dHWNCDKPXUo4mNkiFKx5TTHBvrxlzqWmMnQ=="
      },
      "metadata_id":"urn:wmo:md:br-inmet:data:core:weather:surface-based-observations:synop",
      "wigos_station_identifier":"0-20000-0-76679"
   },
   "links":[
      {
         "rel":"canonical",
         "type":"application/bufr",
         "href":"http://localhost/data/2025-02-06/wis/urn:wmo:md:br-inmet:data:core:weather:surface-based-observations:synop/WIGOS_0-20000-0-76679_20250206T231600.bufr4",
         "length":125117
      },
      {
         "rel":"via",
         "type":"text/html",
         "href":"https://oscar.wmo.int/surface/#/search/station/stationReportDetails/0-20000-0-76679"
      }
   ],
   "generated_by":"wis2box 1.2.0"
}
```

В этой практической сессии вы научитесь использовать инструмент MQTT Explorer для настройки подключения MQTT клиента к WIS2 Global Broker и сможете отображать уведомления WIS2.

MQTT Explorer — это полезный инструмент для просмотра и анализа структуры тем для заданного MQTT брокера, чтобы изучить публикуемые данные.

!!! note "О MQTT"
    MQTT Explorer предоставляет удобный интерфейс для подключения к MQTT брокеру и изучения используемых тем и структуры сообщений.
    
    На практике MQTT предназначен для машинного взаимодействия, где приложение или сервис подписывается на темы и обрабатывает сообщения программно в реальном времени.
    
    Для работы с MQTT программно (например, на Python) можно использовать библиотеки клиентов MQTT, такие как [paho-mqtt](https://pypi.org/project/paho-mqtt), чтобы подключиться к MQTT брокеру и обрабатывать входящие сообщения. Существует множество программных решений для клиентов и серверов MQTT, в зависимости от ваших требований и технической среды.

## Использование MQTT Explorer для подключения к Global Broker

Чтобы просмотреть сообщения, публикуемые WIS2 Global Broker, вы можете использовать "MQTT Explorer", который можно скачать с [веб-сайта MQTT Explorer](https://mqtt-explorer.com).

Откройте MQTT Explorer и добавьте новое подключение к Global Broker, размещенному MeteoFrance, используя следующие данные:

- host: globalbroker.meteo.fr
- port: 8883
- username: everyone
- password: everyone

<img alt="mqtt-explorer-global-broker-connection" src="/../assets/img/mqtt-explorer-global-broker-connection.png" width="800">

Нажмите кнопку 'ADVANCED', удалите предварительно настроенные темы и добавьте следующие темы для подписки:

- `origin/a/wis2/#`

<img alt="mqtt-explorer-global-broker-advanced" src="/../assets/img/mqtt-explorer-global-broker-sub-origin.png" width="800">

!!! note
    При настройке подписок MQTT вы можете использовать следующие подстановочные знаки:

    - **Одноуровневый (+)**: подстановочный знак для одного уровня темы
    - **Многоуровневый (#)**: подстановочный знак для нескольких уровней темы

    В данном случае `origin/a/wis2/#` подпишется на все темы под `origin/a/wis2`.

Нажмите 'BACK', затем 'SAVE', чтобы сохранить данные подключения и подписки. Затем нажмите 'CONNECT':

Сообщения должны начать появляться в вашей сессии MQTT Explorer следующим образом:

<img alt="mqtt-explorer-global-broker-topics" src="/../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

Теперь вы готовы начать изучение тем WIS2 и структуры сообщений.

## Упражнение 1: Изучение структуры тем WIS2

Используйте MQTT для просмотра структуры тем под темами `origin`.

!!! question
    
    Как мы можем определить WIS центр, который опубликовал данные?

??? success "Нажмите, чтобы увидеть ответ"

    Вы можете нажать на левую часть окна в MQTT Explorer, чтобы развернуть структуру тем.
    
    Мы можем определить WIS центр, который опубликовал данные, посмотрев на четвертый уровень структуры тем. Например, следующая тема:

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    указывает, что данные были опубликованы WIS центром с идентификатором центра `br-inmet`, который соответствует Instituto Nacional de Meteorologia - INMET, Бразилия.

!!! question

    Как мы можем различить сообщения, опубликованные WIS-центрами, которые размещают шлюз GTS-to-WIS2, и сообщения, опубликованные WIS-центрами, которые размещают WIS2 Node?

??? success "Нажмите, чтобы увидеть ответ"

    Мы можем различить сообщения, поступающие от шлюза GTS-to-WIS2, посмотрев на идентификатор центра в структуре тем. Например, следующая тема:

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    указывает, что данные были опубликованы шлюзом GTS-to-WIS2, размещенным Deutscher Wetterdienst (DWD), Германия. Шлюз GTS-to-WIS2 — это особый тип издателя данных, который публикует данные из Global Telecommunication System (GTS) в WIS2. Структура тем состоит из заголовков TTAAii CCCC для сообщений GTS.

## Упражнение 2: Изучение структуры сообщений WIS2

Отключитесь от MQTT Explorer и обновите раздел 'Advanced', чтобы изменить подписку на следующие темы:

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="/../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    Подстановочный знак `+` используется для подписки на все WIS-центры.

Переподключитесь к Global Broker и дождитесь появления сообщений.

Вы можете просмотреть содержимое сообщения WIS2 в разделе "Value" справа. Попробуйте развернуть структуру тем, чтобы увидеть различные уровни сообщения, пока не достигнете последнего уровня, и изучите содержимое одного из сообщений.

!!! question

    Как мы можем определить временную метку, когда данные были опубликованы? И как мы можем определить временную метку, когда данные были собраны?

??? success "Нажмите, чтобы увидеть ответ"

    Временная метка, когда данные были опубликованы, содержится в разделе `properties` сообщения с ключом `pubtime`.

    Временная метка, когда данные были собраны, содержится в разделе `properties` сообщения с ключом `datetime`.

    <img alt="mqtt-explorer-global-broker-msg-properties" src="/../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    Как мы можем скачать данные по URL, указанному в сообщении?

??? success "Нажмите, чтобы увидеть ответ"

    URL содержится в разделе `links` с `rel="canonical"` и определяется ключом `href`.

    Вы можете скопировать URL и вставить его в веб-браузер, чтобы скачать данные.

## Упражнение 3: Изучение различий между темами 'origin' и 'cache'

Убедитесь, что вы все еще подключены к Global Broker, используя подписки на темы `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` и `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`, как описано в Упражнении 2.

Попробуйте найти сообщение для одного и того же идентификатора центра, опубликованное как в темах `origin`, так и в темах `cache`.

!!! question

    В чем разница между сообщениями, опубликованными в темах `origin` и `cache`?

??? success "Нажмите, чтобы увидеть ответ"

    Сообщения, опубликованные в темах `origin`, являются оригинальными сообщениями, которые Global Broker повторно публикует из WIS2 Nodes в сети.

    Сообщения, опубликованные в темах `cache`, — это сообщения для данных, которые были загружены Global Cache. Если вы проверите содержимое сообщения из темы, начинающейся с `cache`, вы увидите, что ссылка 'canonical' была обновлена на новый URL.
    
    В сети WIS2 существует несколько Global Cache, поэтому вы получите одно сообщение от каждого Global Cache, который загрузил сообщение.

    Global Cache загружает и повторно публикует только сообщения, которые были опубликованы в иерархии тем `../data/core/...`.

## Заключение

!!! success "Поздравляем!"
    В этой практической сессии вы узнали:

    - как подписываться на сервисы WIS2 Global Broker с использованием MQTT Explorer
    - структуру тем WIS2
    - структуру уведомлений WIS2
    - разницу между основными и рекомендованными данными
    - структуру тем, используемую шлюзом GTS-to-WIS2
    - разницу между сообщениями Global Broker, опубликованными в темах `origin` и `cache`