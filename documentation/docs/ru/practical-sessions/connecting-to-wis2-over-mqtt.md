---
title: Подключение к WIS2 через MQTT
---

# Подключение к WIS2 через MQTT

!!! abstract "Результаты обучения"

    К концу этой практической сессии вы сможете:

    - подключиться к WIS2 Global Broker с использованием MQTT Explorer
    - изучить структуру тем WIS2
    - изучить структуру уведомлений WIS2

## Введение

WIS2 использует протокол MQTT для уведомления о доступности данных о погоде, климате и воде. WIS2 Global Broker подписывается на все WIS2 Nodes в сети и перепубликовывает полученные сообщения. Global Cache подписывается на Global Broker, загружает данные из сообщения и затем перепубликовывает сообщение в теме `cache` с новым URL. Global Discovery Catalogue публикует метаданные для поиска из Broker и предоставляет API для поиска.

Пример структуры уведомления WIS2 для сообщения, полученного по теме `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`:

```json
{
  "id": "59f9b013-c4b3-410a-a52d-fff18f3f1b47",
  "type": "Feature",
  "version": "v04",
  "geometry": {
    "coordinates": [
      -38.69389,
      -17.96472,
      60
    ],
    "type": "Point"
  },
  "properties": {
    "data_id": "br-inmet/data/core/weather/surface-based-observations/synop/WIGOS_0-76-2-2900801000W83499_20240815T060000",
    "datetime": "2024-08-15T06:00:00Z",
    "pubtime": "2024-08-15T09:52:02Z",
    "integrity": {
      "method": "sha512",
      "value": "TBuWycx/G0lIiTo47eFPBViGutxcIyk7eikppAKPc4aHgOmTIS5Wb9+0v3awMOyCgwpFhTruRRCVReMQMp5kYw=="
    },
    "content": {
      "encoding": "base64",
      "value": "QlVGUgAA+gQAABYAACsAAAAAAAIAHAAH6AgPBgAAAAALAAABgMGWx1AAAM0ABOIAAAODM0OTkAAAAAAAAAAAAAAKb5oKEpJ6YkJ6mAAAAAAAAAAAAAAAAv0QeYA29WQa87ZhH4CQP//z+P//BD////+ASznXuUb///8MgAS3/////8X///e+AP////AB/+R/yf////////////////////6/1/79H/3///gEt////////4BLP6QAf/+/pAB//4H0YJ/YeAh/f2///7TH/////9+j//f///////////////////v0f//////////////////////wNzc3Nw==",
      "size": 250
    },
    "wigos_station_identifier": "0-76-2-2900801000W83499"
  },
  "links": [
    {
      "rel": "canonical",
      "type": "application/bufr",
      "href": "http://wis2bra.inmet.gov.br/data/2024-08-15/wis/br-inmet/data/core/weather/surface-based-observations/synop/WIGOS_0-76-2-2900801000W83499_20240815T060000.bufr4",
      "length": 250
    }
  ]
}
```

В этой практической сессии вы узнаете, как использовать инструмент MQTT Explorer для настройки подключения клиента MQTT к WIS2 Global Broker и отображения уведомлений WIS2.

MQTT Explorer — это полезный инструмент для просмотра и анализа структуры тем для заданного брокера MQTT и анализа публикуемых данных.

!!! note "О MQTT"
    MQTT Explorer предоставляет удобный интерфейс для подключения к брокеру MQTT и изучения тем и структуры сообщений, используемых в WIS2.
    
    На практике MQTT предназначен для машинного взаимодействия, где приложение или сервис подписывается на темы и обрабатывает сообщения программно в режиме реального времени.
    
    Для работы с MQTT программно (например, на Python) можно использовать клиентские библиотеки MQTT, такие как [paho-mqtt](https://pypi.org/project/paho-mqtt), чтобы подключаться к брокеру MQTT и обрабатывать входящие сообщения. Существует множество программных решений для клиентов и серверов MQTT, в зависимости от ваших требований и технической среды.

## Использование MQTT Explorer для подключения к Global Broker

Чтобы просмотреть сообщения, публикуемые WIS2 Global Broker, можно использовать "MQTT Explorer", который можно скачать с [веб-сайта MQTT Explorer](https://mqtt-explorer.com).

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
    При настройке подписок MQTT можно использовать следующие подстановочные символы:

    - **Одноуровневый (+)**: подстановочный символ для одного уровня темы
    - **Многоуровневый (#)**: подстановочный символ для нескольких уровней темы

    В данном случае `origin/a/wis2/#` подпишется на все темы под `origin/a/wis2`.

Нажмите 'BACK', затем 'SAVE', чтобы сохранить данные подключения и подписки. Затем нажмите 'CONNECT':

Сообщения начнут появляться в вашей сессии MQTT Explorer следующим образом:

<img alt="mqtt-explorer-global-broker-topics" src="/../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

Теперь вы готовы начать изучение тем WIS2 и структуры сообщений.

## Упражнение 1: Изучение структуры тем WIS2

Используйте MQTT для просмотра структуры тем под темами `origin`.

!!! question
    
    Как можно определить WIS-центр, который опубликовал данные?

??? success "Нажмите, чтобы увидеть ответ"

    Вы можете нажать на окно слева в MQTT Explorer, чтобы развернуть структуру тем.
    
    Мы можем определить WIS-центр, который опубликовал данные, посмотрев на четвертый уровень структуры темы. Например, следующая тема:

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    говорит нам, что данные были опубликованы WIS-центром с идентификатором центра `br-inmet`, который соответствует Instituto Nacional de Meteorologia - INMET, Бразилия.

!!! question

    Как можно отличить сообщения, опубликованные WIS-центрами, размещающими шлюз GTS-to-WIS2, от сообщений, опубликованных WIS-центрами, размещающими WIS2 Node?

??? success "Нажмите, чтобы увидеть ответ"

    Мы можем отличить сообщения, поступающие от шлюза GTS-to-WIS2, посмотрев на идентификатор центра в структуре темы. Например, следующая тема:

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    говорит нам, что данные были опубликованы шлюзом GTS-to-WIS2, размещенным Deutscher Wetterdienst (DWD), Германия. Шлюз GTS-to-WIS2 — это особый тип издателя данных, который публикует данные из Global Telecommunication System (GTS) в WIS2. Структура темы состоит из заголовков TTAAii CCCC для сообщений GTS.

## Упражнение 2: Изучение структуры сообщений WIS2

Отключитесь от MQTT Explorer и обновите раздел 'Advanced', чтобы изменить подписку на следующие темы:

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="/../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    Подстановочный символ `+` используется для подписки на все WIS-центры.

Переподключитесь к Global Broker и дождитесь появления сообщений. 

Вы можете просмотреть содержимое сообщения WIS2 в разделе "Value" справа. Попробуйте развернуть структуру темы, чтобы увидеть различные уровни сообщения, пока не дойдете до последнего уровня, и изучите содержимое одного из сообщений.

!!! question

    Как можно определить временную метку публикации данных? А как можно определить временную метку сбора данных?

??? success "Нажмите, чтобы увидеть ответ"

    Временная метка публикации данных содержится в разделе `properties` сообщения с ключом `pubtime`.

    Временная метка сбора данных содержится в разделе `properties` сообщения с ключом `datetime`.

    <img alt="mqtt-explorer-global-broker-msg-properties" src="/../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    Как можно скачать данные по URL, указанному в сообщении?

??? success "Нажмите, чтобы увидеть ответ"

    URL содержится в разделе `links` с `rel="canonical"` и определяется ключом `href`.

    Вы можете скопировать URL и вставить его в веб-браузер, чтобы скачать данные.

## Упражнение 3: Изучение разницы между темами 'origin' и 'cache'

Убедитесь, что вы все еще подключены к Global Broker, используя подписки на темы `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` и `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`, как описано в Упражнении 2.

Попробуйте найти сообщение для одного и того же идентификатора центра, опубликованное как в темах `origin`, так и в темах `cache`.

!!! question

    В чем разница между сообщениями, опубликованными в темах `origin` и `cache`?

??? success "Нажмите, чтобы увидеть ответ"

    Сообщения, опубликованные в темах `origin`, являются оригинальными сообщениями, которые Global Broker перепубликовывает из WIS2 Nodes в сети. 

    Сообщения, опубликованные в темах `cache`, — это сообщения, для которых данные были загружены Global Cache. Если вы проверите содержимое сообщения из темы, начинающейся с `cache`, вы увидите, что ссылка 'canonical' была обновлена на новый URL.
    
    В сети WIS2 существует несколько Global Cache, поэтому вы получите одно сообщение от каждого Global Cache, который загрузил сообщение.

    Global Cache загружает и перепубликовывает только сообщения, опубликованные в иерархии тем `../data/core/...`.

## Заключение

!!! success "Поздравляем!"
    В этой практической сессии вы узнали:

    - как подписываться на сервисы WIS2 Global Broker с использованием MQTT Explorer
    - структуру тем WIS2
    - структуру уведомлений WIS2
    - разницу между основными и рекомендованными данными
    - структуру тем, используемую шлюзом GTS-to-WIS2
    - разницу между сообщениями Global Broker, опубликованными в темах `origin` и `cache`