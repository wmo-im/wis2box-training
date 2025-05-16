---
title: Подключение к WIS2 через MQTT
---

# Подключение к WIS2 через MQTT

!!! abstract "Учебные результаты"

    К концу этой практической сессии вы сможете:

    - подключиться к Global Broker WIS2 с использованием MQTT Explorer
    - изучить структуру тем WIS2
    - изучить структуру сообщений уведомлений WIS2

## Введение

WIS2 использует протокол MQTT для объявления о доступности данных о погоде/климате/воде. Global Broker WIS2 подписывается на все узлы WIS2 в сети и перепубликует полученные сообщения. Global Cache подписывается на Global Broker, загружает данные из сообщения, а затем перепубликует сообщение в теме `cache` с новым URL. Global Discovery Catalogue публикует метаданные обнаружения от Broker и предоставляет API поиска.

Вот пример структуры сообщения уведомления WIS2 для сообщения, полученного по теме `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`:	

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

На этой практической сессии вы научитесь использовать инструмент MQTT Explorer для настройки подключения клиента MQTT к Global Broker WIS2 и сможете отображать сообщения уведомлений WIS2.

MQTT Explorer — полезный инструмент для просмотра и изучения структуры тем для данного MQTT брокера для просмотра публикуемых данных.

Обратите внимание, что MQTT в основном используется для коммуникации "машина-машина"; это означает, что обычно клиент автоматически анализирует сообщения по мере их получения. Для программной работы с MQTT (например, на Python) вы можете использовать библиотеки клиента MQTT, такие как [paho-mqtt](https://pypi.org/project/paho-mqtt), чтобы подключаться к MQTT брокеру и обрабатывать входящие сообщения. Существует множество программного обеспечения для клиентов и серверов MQTT в зависимости от ваших требований и технической среды.

## Использование MQTT Explorer для подключения к Global Broker

Для просмотра сообщений, публикуемых Global Broker WIS2, вы можете использовать "MQTT Explorer", который можно загрузить с [сайта MQTT Explorer](https://mqtt-explorer.com).

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

    - **Одноуровневый (+)**: одноуровневый подстановочный знак заменяет один уровень темы
    - **Многоуровневый (#)**: многоуровневый подстановочный знак заменяет несколько уровней темы

    В данном случае `origin/a/wis2/#` подпишется на все темы под `origin/a/wis2`.

Нажмите 'BACK', затем 'SAVE', чтобы сохранить данные вашего подключения и подписки. Затем нажмите 'CONNECT':

Сообщения должны начать появляться в вашей сессии MQTT Explorer следующим образом:

<img alt="mqtt-explorer-global-broker-topics" src="/../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

Теперь вы готовы начать изучение структуры тем и сообщений WIS2.

## Упражнение 1: Изучение структуры тем WIS2

Используйте MQTT для просмотра структуры тем под `origin`.

!!! question
    
    Как мы можем определить центр WIS, который опубликовал данные?

??? success "Нажмите, чтобы увидеть ответ"

    Вы можете щелкнуть в окне слева в MQTT Explorer, чтобы развернуть структуру тем.
    
    Мы можем определить центр WIS, который опубликовал данные, посмотрев на четвертый уровень структуры тем. Например, следующая тема:

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    говорит нам, что данные были опубликованы центром WIS с идентификатором центра `br-inmet`, который является идентификатором центра для Instituto Nacional de Meteorologia - INMET, Бразилия.

!!! question

    Как мы можем отличить сообщения, опубликованные центрами WIS, которые размещают шлюз GTS-to-WIS2, от сообщений, опубликованных центрами WIS, которые размещают узел WIS2?

??? success "Нажмите, чтобы увидеть ответ"

    Мы можем отличить сообщения, исходящие от шлюза GTS-to-WIS2, посмотрев на идентификатор центра в структуре тем. Например, следующая тема:

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    говорит нам, что данные были опубликованы шлюзом GTS-to-WIS2, размещенным Deutscher Wetterdienst (DWD), Германия. Шлюз GTS-to-WIS2 - это специальный тип публикатора данных, который публикует данные из Глобальной телекоммуникационной системы (GTS) в WIS2. Структура темы составлена из заголовков TTAAii CCCC для сообщений GTS.

## Упражнение 2: Изучение структуры сообщений WIS2

Отключитесь от MQTT Explorer и обновите раздел 'Advanced', чтобы изменить подписку на следующие:

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="/../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    Подстановочный знак `+` используется для подписки на все центры WIS.

Подключитесь снова к Global Broker и дождитесь появления сообщений.

Вы можете просмотреть содержимое сообщения WIS2 в разделе "Value" справа. Попробуйте развернуть структуру темы, чтобы увидеть разные уровни сообщения, пока не дойдете до последнего уровня, и изучите содержимое одного из сообщений.

!!! question

    Как мы можем определить временную метку, когда данные были опубликованы? И как мы можем определить временную метку, когда данные были собраны?

??? success "Нажмите, чтобы увидеть ответ"

    Временная метка, когда данные были опубликованы, содержится в разделе `properties` сообщения с ключом `pubtime`.

    Временная метка, когда данные были собраны, содержится в разделе `properties` сообщения с ключом `datetime`.

    <img alt="mqtt-explorer-global-broker-msg-properties" src="/../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    Как мы можем загрузить данные по предоставленному URL в сообщении?

??? success "Нажмите, чтобы увидеть ответ"

    URL содержится в разделе `links` с `rel="canonical"` и определен ключом `href`.

    Вы можете скопировать URL и вставить его в веб-браузер, чтобы загрузить данные.

## Упражнение 3: Изучение различий между темами 'origin' и 'cache'

Убедитесь, что вы все еще подключены к Global Broker с подписками на темы `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` и `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`, как описано в Упражнении 2.

Попробуйте идентифицировать сообщение для того же идентификатора центра, опубликованное как в темах `origin`, так и в темах `cache`.


!!! question

    В чем разница между сообщениями, опубликованными в темах `origin` и `cache`?

??? success "Нажмите, чтобы увидеть ответ"

    Сообщения, опубликованные в темах `origin`, являются оригинальными сообщениями, которые Global Broker перепубликует от узлов WIS2 в сети. 

    Сообщения, опубликованные в темах `cache`, являются сообщениями для данных, которые были загружены Global Cache. Если вы проверите содержимое сообщения из темы, начинающейся с `cache`, вы увидите, что ссылка 'canonical' была обновлена на новый URL.
    
    В сети WIS2 существует несколько Global Cache, поэтому вы получите одно сообщение от каждого Global Cache, который загрузил сообщение.

    Global Cache будет загружать и перепубликовать только сообщения, которые были опубликованы в иерархии тем `../data/core/...`.

## Заключение

!!! success "Поздравляем!"
    На этой практической сессии вы научились:

    - подписываться на услуги Global Broker WIS2 с использованием MQTT Explorer
    - структуре тем WIS2
    - структуре сообщений уведомлений WIS2
    - различиях между основными и рекомендуемыми данными
    - структуре тем, используемой шлюзом GTS-to-WIS2
    - различиях между сообщениями Global Broker, опубликованными в темах `origin` и `cache`