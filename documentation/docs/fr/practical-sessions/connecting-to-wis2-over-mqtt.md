---
title: Connexion à WIS2 via MQTT
---

# Connexion à WIS2 via MQTT

!!! abstract "Objectifs d'apprentissage"

    À la fin de cette session pratique, vous serez capable de :

    - vous connecter au WIS2 Global Broker en utilisant MQTT Explorer
    - examiner la structure des sujets WIS2
    - examiner la structure des messages de notification WIS2

## Introduction

WIS2 utilise le protocole MQTT pour annoncer la disponibilité des données météorologiques/climatiques/hydrologiques. Le WIS2 Global Broker s'abonne à tous les WIS2 Nodes du réseau et republie les messages qu'il reçoit. Le Global Cache s'abonne au Global Broker, télécharge les données contenues dans le message, puis republie le message sur le sujet `cache` avec une nouvelle URL. Le Global Discovery Catalogue publie les métadonnées de découverte à partir du Broker et fournit une API de recherche.

Voici un exemple de structure de message de notification WIS2 pour un message reçu sur le sujet `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop` :

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

Dans cette session pratique, vous apprendrez à utiliser l'outil MQTT Explorer pour configurer une connexion client MQTT à un WIS2 Global Broker et afficher les messages de notification WIS2.

MQTT Explorer est un outil utile pour parcourir et examiner la structure des topics d’un broker MQTT donné afin de consulter les données publiées.

!!! note "À propos de MQTT"
    MQTT Explorer fournit une interface conviviale pour se connecter à un broker MQTT et explorer les topics et la structure des messages utilisés par WIS2.
    
    En pratique, MQTT est conçu pour une communication machine-à-machine, où une application ou un service s'abonne à des topics et traite les messages de manière programmatique en temps réel.
    
    Pour travailler avec MQTT de manière programmatique (par exemple, en Python), vous pouvez utiliser des bibliothèques clients MQTT telles que [paho-mqtt](https://pypi.org/project/paho-mqtt) pour vous connecter à un broker MQTT et traiter les messages entrants. Il existe de nombreux logiciels clients et serveurs MQTT, selon vos besoins et votre environnement technique.

## Utiliser MQTT Explorer pour se connecter au Global Broker

Pour afficher les messages publiés par un WIS2 Global Broker, vous pouvez utiliser "MQTT Explorer", téléchargeable depuis le [site web de MQTT Explorer](https://mqtt-explorer.com).

Ouvrez MQTT Explorer et ajoutez une nouvelle connexion au Global Broker hébergé par MeteoFrance en utilisant les détails suivants :

- host : globalbroker.meteo.fr
- port : 8883
- username : everyone
- password : everyone

<img alt="mqtt-explorer-global-broker-connection" src="/../assets/img/mqtt-explorer-global-broker-connection.png" width="800">

Cliquez sur le bouton 'ADVANCED', supprimez les topics préconfigurés et ajoutez les topics suivants pour vous y abonner :

- `origin/a/wis2/#`

<img alt="mqtt-explorer-global-broker-advanced" src="/../assets/img/mqtt-explorer-global-broker-sub-origin.png" width="800">

!!! note
    Lors de la configuration des abonnements MQTT, vous pouvez utiliser les jokers suivants :

    - **Niveau unique (+)** : un joker de niveau unique remplace un seul niveau de topic.
    - **Niveaux multiples (#)** : un joker de niveaux multiples remplace plusieurs niveaux de topics.

    Dans ce cas, `origin/a/wis2/#` s'abonnera à tous les topics sous le topic `origin/a/wis2`.

Cliquez sur 'BACK', puis sur 'SAVE' pour enregistrer les détails de votre connexion et de votre abonnement. Ensuite, cliquez sur 'CONNECT' :

Les messages devraient commencer à apparaître dans votre session MQTT Explorer comme suit :

<img alt="mqtt-explorer-global-broker-topics" src="/../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

Vous êtes maintenant prêt à explorer les topics et la structure des messages WIS2.

## Exercice 1 : Examiner la structure des topics WIS2

Utilisez MQTT pour parcourir la structure des topics sous les topics `origin`.

!!! question
    
    Comment pouvons-nous distinguer le centre WIS qui a publié les données ?

??? success "Cliquez pour révéler la réponse"

    Vous pouvez cliquer sur la fenêtre de gauche dans MQTT Explorer pour développer la structure des topics.
    
    Nous pouvons distinguer le centre WIS qui a publié les données en regardant le quatrième niveau de la structure des topics. Par exemple, le topic suivant :

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    nous indique que les données ont été publiées par un centre WIS avec le centre-id `br-inmet`, qui correspond au centre-id de l'Instituto Nacional de Meteorologia - INMET, Brésil.

!!! question

    Comment pouvons-nous distinguer les messages publiés par les centres WIS hébergeant une passerelle GTS-to-WIS2 et ceux publiés par les centres WIS hébergeant un WIS2 Node ?

??? success "Cliquez pour révéler la réponse"

    Nous pouvons distinguer les messages provenant d'une passerelle GTS-to-WIS2 en regardant le centre-id dans la structure des topics. Par exemple, le topic suivant :

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    nous indique que les données ont été publiées par la passerelle GTS-to-WIS2 hébergée par Deutscher Wetterdienst (DWD), Allemagne. La passerelle GTS-to-WIS2 est un type spécial de producteur de données qui publie des données du Global Telecommunication System (GTS) vers WIS2. La structure des topics est composée des en-têtes TTAAii CCCC pour les messages GTS.

## Exercice 2 : Examiner la structure des messages WIS2

Déconnectez-vous de MQTT Explorer et mettez à jour les sections 'Advanced' pour modifier l'abonnement comme suit :

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="/../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    Le joker `+` est utilisé pour s'abonner à tous les centres WIS.

Reconnectez-vous au Global Broker et attendez que les messages apparaissent. 

Vous pouvez consulter le contenu du message WIS2 dans la section "Value" sur le côté droit. Essayez de développer la structure des topics pour voir les différents niveaux du message jusqu'à atteindre le dernier niveau et examinez le contenu d'un des messages.

!!! question

    Comment pouvons-nous identifier l'horodatage auquel les données ont été publiées ? Et comment pouvons-nous identifier l'horodatage auquel les données ont été collectées ?

??? success "Cliquez pour révéler la réponse"

    L'horodatage auquel les données ont été publiées est contenu dans la section `properties` du message avec une clé `pubtime`.

    L'horodatage auquel les données ont été collectées est contenu dans la section `properties` du message avec une clé `datetime`.

    <img alt="mqtt-explorer-global-broker-msg-properties" src="/../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    Comment pouvons-nous télécharger les données à partir de l'URL fournie dans le message ?

??? success "Cliquez pour révéler la réponse"

    L'URL est contenue dans la section `links` avec `rel="canonical"` et définie par la clé `href`.

    Vous pouvez copier l'URL et la coller dans un navigateur web pour télécharger les données.

## Exercice 3 : Examiner la différence entre les topics 'origin' et 'cache'

Assurez-vous d'être toujours connecté au Global Broker en utilisant les abonnements aux topics `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` et `cache/a/wis2/+/data/core/weather/surface-based-observations/synop` comme décrit dans l'Exercice 2.

Essayez d'identifier un message pour le même centre-id publié à la fois sur les topics `origin` et `cache`.

!!! question

    Quelle est la différence entre les messages publiés sur les topics `origin` et `cache` ?

??? success "Cliquez pour révéler la réponse"

    Les messages publiés sur les topics `origin` sont les messages originaux que le Global Broker republie à partir des WIS2 Nodes du réseau. 

    Les messages publiés sur les topics `cache` sont les messages pour lesquels les données ont été téléchargées par le Global Cache. Si vous examinez le contenu du message provenant d'un topic commençant par `cache`, vous verrez que le lien 'canonical' a été mis à jour avec une nouvelle URL.
    
    Il existe plusieurs Global Caches dans le réseau WIS2, vous recevrez donc un message de chaque Global Cache ayant téléchargé le message.

    Le Global Cache ne télécharge et ne republie que les messages publiés dans la hiérarchie de topics `../data/core/...`.

## Conclusion

!!! success "Félicitations !"
    Dans cette session pratique, vous avez appris :

    - comment s'abonner aux services WIS2 Global Broker en utilisant MQTT Explorer
    - la structure des topics WIS2
    - la structure des messages de notification WIS2
    - la différence entre les données core et recommandées
    - la structure des topics utilisée par la passerelle GTS-to-WIS2
    - la différence entre les messages Global Broker publiés sur les topics `origin` et `cache`