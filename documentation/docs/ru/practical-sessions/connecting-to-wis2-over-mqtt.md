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

WIS2 использует протокол MQTT для уведомления о доступности данных о погоде, климате и воде. WIS2 Global Broker подписывается на все WIS2 Nodes в сети и перепубликует полученные сообщения. Global Cache подписывается на Global Broker, загружает данные из сообщения и затем перепубликует сообщение в теме `cache` с новым URL. Global Discovery Catalogue публикует метаданные для поиска из Broker и предоставляет API для поиска.

Пример структуры уведомления WIS2 для сообщения, полученного по теме `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`:

```json
{
   "id":"7a34051b-aa92-40f3-bbab-439143657c8c",
   "type":"Feature",
   "conformsTo":[
      "http://wis.wmo.int/spec/wnm/1/conf/core"
   ],
   "geometry":{
      "type":"Polygon",
      "coordinates":[
         [
            [
               -73.98723548042966,
               5.244486395687602
            ],
            [
               -34.729993455533034,
               5.244486395687602
            ],
            [
               -34.729993455533034,
               -33.768377780900764
            ],
            [
               -73.98723548042966,
               -33.768377780900764
            ],
            [
               -73.98723548042966,
               5.244486395687602
            ]
         ]
      ]
   },
   "properties":{
      "data_id":"br-inmet/metadata/urn:wmo:md:br-inmet:rr1ieq",
      "datetime":"2026-01-20T08:30:21Z",
      "pubtime":"2026-01-20T08:30:22Z",
      "integrity":{
         "method":"sha512",
         "value":"RN+GzqgONURtkzOCo5vQJ5t7SzlAvaGONywEnTXHrHew9RQmUhrHbASvmDlCeRTb8vhE+1/h/7/20f2XJFHCcA=="
      },
      "content":{
         "encoding":"base64",
         "value":"eyJpZCI6ICJ1cm46d21vOm1kOmJyLWlubWV0OnJyMWllcSIsICJjb25mb3Jtc1RvIjogWyJodHRwOi8vd2lzLndtby5pbnQvc3BlYy93Y21wLzIvY29uZi9jb3JlIl0sICJ0eXBlIjogIkZlYXR1cmUiLCAidGltZSI6IHsiaW50ZXJ2YWwiOiBbIjIwMjYtMDEtMjAiLCAiLi4iXSwgInJlc29sdXRpb24iOiAiUFQxSCJ9LCAiZ2VvbWV0cnkiOiB7InR5cGUiOiAiUG9seWdvbiIsICJjb29yZGluYXRlcyI6IFtbWy03My45ODcyMzU0ODA0Mjk2NiwgNS4yNDQ0ODYzOTU2ODc2MDJdLCBbLTM0LjcyOTk5MzQ1NTUzMzAzNCwgNS4yNDQ0ODYzOTU2ODc2MDJdLCBbLTM0LjcyOTk5MzQ1NTUzMzAzNCwgLTMzLjc2ODM3Nzc4MDkwMDc2NF0sIFstNzMuOTg3MjM1NDgwNDI5NjYsIC0zMy43NjgzNzc3ODA5MDA3NjRdLCBbLTczLjk4NzIzNTQ4MDQyOTY2LCA1LjI0NDQ4NjM5NTY4NzYwMl1dXX0sICJwcm9wZXJ0aWVzIjogeyJ0eXBlIjogImRhdGFzZXQiLCAiaWRlbnRpZmllciI6ICJ1cm46d21vOm1kOmJyLWlubWV0OnJyMWllcSIsICJ0aXRsZSI6ICJIb3VybHkgc3lub3B0aWMgb2JzZXJ2YXRpb25zIGZyb20gZml4ZWQtbGFuZCBzdGF0aW9ucyAoU1lOT1ApIChici1pbm1ldCkiLCAiZGVzY3JpcHRpb24iOiAidGVzdCIsICJrZXl3b3JkcyI6IFsib2JzZXJ2YXRpb25zIiwgInRlbXBlcmF0dXJlIiwgInZpc2liaWxpdHkiLCAicHJlY2lwaXRhdGlvbiIsICJwcmVzc3VyZSIsICJjbG91ZHMiLCAic25vdyBkZXB0aCIsICJldmFwb3JhdGlvbiIsICJyYWRpYXRpb24iLCAid2luZCIsICJ0b3RhbCBzdW5zaGluZSIsICJodW1pZGl0eSJdLCAidGhlbWVzIjogW3siY29uY2VwdHMiOiBbeyJpZCI6ICJ3ZWF0aGVyIiwgInRpdGxlIjogIldlYXRoZXIifV0sICJzY2hlbWUiOiAiaHR0cDovL2NvZGVzLndtby5pbnQvd2lzL3RvcGljLWhpZXJhcmNoeS9lYXJ0aC1zeXN0ZW0tZGlzY2lwbGluZSJ9XSwgImNvbnRhY3RzIjogW3sib3JnYW5pemF0aW9uIjogIndtbyIsICJlbWFpbHMiOiBbeyJ2YWx1ZSI6ICJ0ZXN0QGNuLmNvbSJ9XSwgImFkZHJlc3NlcyI6IFt7ImNvdW50cnkiOiAiQlJBIn1dLCAibGlua3MiOiBbeyJyZWwiOiAiYWJvdXQiLCAiaHJlZiI6ICJodHRwOi8vdGVzdC5jb20iLCAidHlwZSI6ICJ0ZXh0L2h0bWwifV0sICJyb2xlcyI6IFsiaG9zdCJdfV0sICJjcmVhdGVkIjogIjIwMjYtMDEtMjBUMDg6MzA6MjFaIiwgInVwZGF0ZWQiOiAiMjAyNi0wMS0yMFQwODozMDoyMVoiLCAid21vOmRhdGFQb2xpY3kiOiAiY29yZSIsICJpZCI6ICJ1cm46d21vOm1kOmJyLWlubWV0OnJyMWllcSJ9LCAibGlua3MiOiBbeyJocmVmIjogIm1xdHQ6Ly9ldmVyeW9uZTpldmVyeW9uZUBsb2NhbGhvc3Q6MTg4MyIsICJ0eXBlIjogImFwcGxpY2F0aW9uL2pzb24iLCAibmFtZSI6ICJvcmlnaW4vYS93aXMyL2JyLWlubWV0L2RhdGEvY29yZS93ZWF0aGVyL3N1cmZhY2UtYmFzZWQtb2JzZXJ2YXRpb25zL3N5bm9wIiwgInJlbCI6ICJpdGVtcyIsICJjaGFubmVsIjogIm9yaWdpbi9hL3dpczIvYnItaW5tZXQvZGF0YS9jb3JlL3dlYXRoZXIvc3VyZmFjZS1iYXNlZC1vYnNlcnZhdGlvbnMvc3lub3AiLCAiZmlsdGVycyI6IHsid2lnb3Nfc3RhdGlvbl9pZGVudGlmaWVyIjogeyJ0eXBlIjogInN0cmluZyIsICJ0aXRsZSI6ICJXSUdPUyBTdGF0aW9uIElkZW50aWZpZXIiLCAiZGVzY3JpcHRpb24iOiAiRmlsdGVyIGJ5IFdJR09TIFN0YXRpb24gSWRlbnRpZmllciJ9fSwgInRpdGxlIjogIk5vdGlmaWNhdGlvbnMifSwgeyJocmVmIjogImh0dHA6Ly9sb2NhbGhvc3QvbWV0YWRhdGEvZGF0YS91cm46d21vOm1kOmJyLWlubWV0OnJyMWllcS5qc29uIiwgInR5cGUiOiAiYXBwbGljYXRpb24vZ2VvK2pzb24iLCAibmFtZSI6ICJ1cm46d21vOm1kOmJyLWlubWV0OnJyMWllcSIsICJyZWwiOiAiY2Fub25pY2FsIiwgInRpdGxlIjogInVybjp3bW86bWQ6YnItaW5tZXQ6cnIxaWVxIn1dfQ==",
         "size":1957
      }
   },
   "links":[
      {
         "rel":"canonical",
         "type":"application/geo+json",
         "href":"http://localhost/data/metadata/urn:wmo:md:br-inmet:rr1ieq.json",
         "length":1957
      }
   ],
   "generated_by":"wis2box 1.2.0"
}
```

В этом практическом занятии вы научитесь использовать инструмент MQTT Explorer для настройки подключения MQTT-клиента к WIS2 Global Broker и отображения уведомлений WIS2.

MQTT Explorer — это полезный инструмент для просмотра и анализа структуры тем для заданного MQTT-брокера, чтобы изучить публикуемые данные.

!!! note "О MQTT"
    MQTT Explorer предоставляет удобный интерфейс для подключения к MQTT-брокеру и изучения структуры тем и сообщений, используемых в WIS2.
    
    На практике MQTT предназначен для связи между машинами, где приложение или сервис подписывается на темы и обрабатывает сообщения программно в реальном времени.
    
    Для работы с MQTT программно (например, на Python) вы можете использовать библиотеки MQTT-клиентов, такие как [paho-mqtt](https://pypi.org/project/paho-mqtt), чтобы подключиться к MQTT-брокеру и обрабатывать входящие сообщения. Существует множество программных решений для MQTT-клиентов и серверов, в зависимости от ваших требований и технической среды.

## Использование MQTT Explorer для подключения к Global Broker

Чтобы просматривать сообщения, публикуемые WIS2 Global Broker, вы можете использовать "MQTT Explorer", который можно скачать с [веб-сайта MQTT Explorer](https://mqtt-explorer.com).

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
    При настройке подписок MQTT вы можете использовать следующие подстановочные знаки:

    - **Одноуровневый (+)**: подстановочный знак для одного уровня заменяет один уровень темы.
    - **Многоуровневый (#)**: подстановочный знак для нескольких уровней заменяет несколько уровней темы.

    В данном случае `origin/a/wis2/#` подпишется на все темы под `origin/a/wis2`.

Нажмите 'BACK', затем 'SAVE', чтобы сохранить данные подключения и подписки. Затем нажмите 'CONNECT':

Сообщения должны начать появляться в вашей сессии MQTT Explorer следующим образом:

<img alt="mqtt-explorer-global-broker-topics" src="/../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

Теперь вы готовы начать изучение тем и структуры сообщений WIS2.

## Упражнение 1: Изучение структуры тем WIS2

Используйте MQTT для просмотра структуры тем под темами `origin`.

!!! question
    
    Как мы можем определить WIS-центр, который опубликовал данные?

??? success "Нажмите, чтобы увидеть ответ"

    Вы можете нажать на окно слева в MQTT Explorer, чтобы развернуть структуру тем.
    
    Мы можем определить WIS-центр, который опубликовал данные, посмотрев на четвертый уровень структуры темы. Например, следующая тема:

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    говорит нам, что данные были опубликованы WIS-центром с идентификатором `br-inmet`, который является идентификатором для Instituto Nacional de Meteorologia - INMET, Бразилия.

!!! question

    Как мы можем отличить сообщения, опубликованные WIS-центрами, которые размещают шлюз GTS-to-WIS2, от сообщений, опубликованных WIS-центрами, которые размещают WIS2 Node?

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
    Подстановочный знак `+` используется для подписки на все WIS-центры.

Подключитесь снова к Global Broker и дождитесь появления сообщений. 

Вы можете просмотреть содержимое сообщения WIS2 в разделе "Value" справа. Попробуйте развернуть структуру темы, чтобы увидеть различные уровни сообщения, пока не дойдете до последнего уровня, и изучите содержимое одного из сообщений.

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

    Сообщения, опубликованные в темах `origin`, — это оригинальные сообщения, которые Global Broker перепубликовывает из WIS2 Nodes в сети. 

    Сообщения, опубликованные в темах `cache`, — это сообщения для данных, которые были загружены Global Cache. Если вы проверите содержимое сообщения из темы, начинающейся с `cache`, вы увидите, что ссылка 'canonical' была обновлена на новый URL.
    
    В сети WIS2 существует несколько Global Cache, поэтому вы получите одно сообщение от каждого Global Cache, который загрузил сообщение.

    Global Cache будет загружать и перепубликовывать только сообщения, которые были опубликованы в иерархии тем `../data/core/...`.

## Заключение

!!! success "Поздравляем!"
    В этом практическом занятии вы узнали:

    - как подписываться на сервисы WIS2 Global Broker с использованием MQTT Explorer
    - структуру тем WIS2
    - структуру уведомлений WIS2
    - разницу между основными и рекомендованными данными
    - структуру тем, используемую шлюзом GTS-to-WIS2
    - разницу между сообщениями Global Broker, опубликованными в темах `origin` и `cache`