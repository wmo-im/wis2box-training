---
title: Подключение к WIS2 через MQTT
---

# Подключение к WIS2 через MQTT

!!! abstract "Результаты обучения"

    К концу этой практической сессии вы сможете:

    - подключиться к WIS2 Global Broker с помощью MQTT Explorer
    - изучить структуру тем WIS2
    - изучить структуру уведомлений WIS2

## Введение

WIS2 использует протокол MQTT для уведомления о доступности данных о погоде/климате/водных ресурсах. WIS2 Global Broker подписывается на все WIS2 Nodes в сети и повторно публикует полученные сообщения. Global Cache подписывается на Global Broker, загружает данные из сообщения и затем повторно публикует сообщение в теме `cache` с новым URL. Global Discovery Catalogue публикует метаданные для поиска из Broker и предоставляет API для поиска.

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

В этой практической сессии вы научитесь использовать инструмент MQTT Explorer для настройки подключения MQTT клиента к WIS2 Global Broker и отображения уведомлений WIS2.

MQTT Explorer — это полезный инструмент для просмотра и анализа структуры тем для заданного MQTT брокера и данных, которые публикуются.

!!! note "О MQTT"
    MQTT Explorer предоставляет удобный интерфейс для подключения к MQTT брокеру и изучения тем и структуры сообщений, используемых в WIS2.
    
    На практике MQTT предназначен для машинного взаимодействия, где приложение или сервис подписывается на темы и обрабатывает сообщения программно в реальном времени.
    
    Для работы с MQTT программно (например, на Python) вы можете использовать библиотеки MQTT клиента, такие как [paho-mqtt](https://pypi.org/project/paho-mqtt), чтобы подключиться к MQTT брокеру и обрабатывать входящие сообщения. Существует множество программных решений для клиентов и серверов MQTT, в зависимости от ваших требований и технической среды.

## Использование MQTT Explorer для подключения к Global Broker

Чтобы просмотреть сообщения, публикуемые WIS2 Global Broker, вы можете использовать "MQTT Explorer", который можно скачать с [веб-сайта MQTT Explorer](https://mqtt-explorer.com).

Откройте MQTT Explorer и добавьте новое подключение к Global Broker, размещенному MeteoFrance, используя следующие данные:

- host: globalbroker.meteo.fr
- port: 8883
- username: everyone
- password: everyone

<img alt="mqtt-explorer-global-broker-connection" src="/../assets/img/mqtt-explorer-global-broker-connection.png" width="800">

Нажмите кнопку 'ADVANCED', удалите предустановленные темы и добавьте следующие темы для подписки:

- `origin/a/wis2/#`

<img alt="mqtt-explorer-global-broker-advanced" src="/../assets/img/mqtt-explorer-global-broker-sub-origin.png" width="800">

!!! note
    При настройке подписок MQTT вы можете использовать следующие подстановочные символы:

    - **Одноуровневый (+)**: подстановочный символ для одного уровня темы
    - **Многоуровневый (#)**: подстановочный символ для нескольких уровней темы

    В данном случае `origin/a/wis2/#` подпишется на все темы под `origin/a/wis2`.

Нажмите 'BACK', затем 'SAVE', чтобы сохранить детали подключения и подписки. Затем нажмите 'CONNECT':

Сообщения должны начать появляться в вашей сессии MQTT Explorer следующим образом:

<img alt="mqtt-explorer-global-broker-topics" src="/../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

Теперь вы готовы начать изучение тем и структуры сообщений WIS2.

## Упражнение 1: Изучение структуры тем WIS2

Используйте MQTT для просмотра структуры тем под темами `origin`.

!!! question
    
    Как можно определить WIS центр, который опубликовал данные?

??? success "Нажмите, чтобы увидеть ответ"

    Вы можете нажать на окно слева в MQTT Explorer, чтобы развернуть структуру тем.
    
    Мы можем определить WIS центр, который опубликовал данные, посмотрев на четвертый уровень структуры темы. Например, следующая тема:

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    говорит нам, что данные были опубликованы WIS центром с centre-id `br-inmet`, который соответствует Instituto Nacional de Meteorologia - INMET, Бразилия.

!!! question

    Как можно отличить сообщения, опубликованные WIS центрами, которые хостят шлюз GTS-to-WIS2, от сообщений, опубликованных WIS центрами, которые хостят WIS2 Node?

??? success "Нажмите, чтобы увидеть ответ"

    Мы можем отличить сообщения, поступающие от шлюза GTS-to-WIS2, посмотрев на centre-id в структуре темы. Например, следующая тема:

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    говорит нам, что данные были опубликованы шлюзом GTS-to-WIS2, хостящимся Deutscher Wetterdienst (DWD), Германия. Шлюз GTS-to-WIS2 — это особый тип издателя данных, который публикует данные из Global Telecommunication System (GTS) в WIS2. Структура темы состоит из заголовков TTAAii CCCC для сообщений GTS.

## Упражнение 2: Изучение структуры сообщений WIS2

Отключитесь от MQTT Explorer и обновите раздел 'Advanced', чтобы изменить подписку на следующие темы:

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="/../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    Подстановочный символ `+` используется для подписки на все WIS центры.

Подключитесь снова к Global Broker и дождитесь появления сообщений. 

Вы можете просмотреть содержимое сообщения WIS2 в разделе "Value" справа. Попробуйте развернуть структуру темы, чтобы увидеть разные уровни сообщения, пока не достигнете последнего уровня, и изучите содержимое одного из сообщений.

!!! question

    Как можно определить временную метку, когда данные были опубликованы? А как можно определить временную метку, когда данные были собраны?

??? success "Нажмите, чтобы увидеть ответ"

    Временная метка, когда данные были опубликованы, содержится в разделе `properties` сообщения с ключом `pubtime`.

    Временная метка, когда данные были собраны, содержится в разделе `properties` сообщения с ключом `datetime`.

    <img alt="mqtt-explorer-global-broker-msg-properties" src="/../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    Как можно скачать данные по URL, указанному в сообщении?

??? success "Нажмите, чтобы увидеть ответ"

    URL содержится в разделе `links` с `rel="canonical"` и определяется ключом `href`.

    Вы можете скопировать URL и вставить его в веб-браузер, чтобы скачать данные.

## Упражнение 3: Изучение различий между темами 'origin' и 'cache'

Убедитесь, что вы все еще подключены к Global Broker, используя подписки на темы `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` и `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`, как описано в Упражнении 2.

Попробуйте найти сообщение для одного и того же centre-id, опубликованное как в темах `origin`, так и в темах `cache`.

!!! question

    В чем разница между сообщениями, опубликованными в темах `origin` и `cache`?

??? success "Нажмите, чтобы увидеть ответ"

    Сообщения, опубликованные в темах `origin`, — это оригинальные сообщения, которые Global Broker повторно публикует из WIS2 Nodes в сети. 

    Сообщения, опубликованные в темах `cache`, — это сообщения, для которых данные были загружены Global Cache. Если вы проверите содержимое сообщения из темы, начинающейся с `cache`, вы увидите, что ссылка 'canonical' была обновлена на новый URL.
    
    В сети WIS2 существует несколько Global Cache, поэтому вы получите одно сообщение от каждого Global Cache, который загрузил сообщение.

    Global Cache загружает и повторно публикует только те сообщения, которые были опубликованы в иерархии тем `../data/core/...`.

## Заключение

!!! success "Поздравляем!"
    В этой практической сессии вы узнали:

    - как подписываться на сервисы WIS2 Global Broker с помощью MQTT Explorer
    - структуру тем WIS2
    - структуру уведомлений WIS2
    - различие между основными и рекомендованными данными
    - структуру тем, используемую шлюзом GTS-to-WIS2
    - различие между сообщениями Global Broker, опубликованными в темах `origin` и `cache`