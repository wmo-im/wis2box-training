---
title: Connexion à WIS2 via MQTT
---

# Connexion à WIS2 via MQTT

!!! abstract "Résultats d'apprentissage"

    À la fin de cette session pratique, vous serez capable de :

    - vous connecter au Courtier Global WIS2 en utilisant MQTT Explorer
    - examiner la structure des sujets WIS2
    - examiner la structure des messages de notification WIS2

## Introduction

WIS2 utilise le protocole MQTT pour annoncer la disponibilité des données météorologiques/climatiques/hydrologiques. Le Courtier Global WIS2 s'abonne à tous les Nœuds WIS2 du réseau et republie les messages qu'il reçoit. Le Cache Global s'abonne au Courtier Global, télécharge les données dans le message puis republie le message sur le sujet `cache` avec une nouvelle URL. Le Catalogue de Découverte Global publie les métadonnées de découverte du Courtier et fournit une API de recherche.

Voici un exemple de la structure de message de notification WIS2 pour un message reçu sur le sujet `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop` :

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

Dans cette session pratique, vous apprendrez à utiliser l'outil MQTT Explorer pour configurer une connexion client MQTT au Courtier Global WIS2 et à afficher les messages de notification WIS2.

MQTT Explorer est un outil utile pour parcourir et examiner la structure des sujets pour un courtier MQTT donné afin de réviser les données publiées.

Notez que MQTT est principalement utilisé pour la communication "machine à machine"; cela signifie qu'en général, un client analyserait automatiquement les messages à mesure qu'ils sont reçus. Pour travailler avec MQTT de manière programmatique (par exemple, en Python), vous pouvez utiliser des bibliothèques clientes MQTT telles que [paho-mqtt](https://pypi.org/project/paho-mqtt) pour vous connecter à un courtier MQTT et traiter les messages entrants. Il existe de nombreux logiciels clients et serveurs MQTT, en fonction de vos besoins et de votre environnement technique.

## Utilisation de MQTT Explorer pour se connecter au Courtier Global

Pour voir les messages publiés par un Courtier Global WIS2, vous pouvez utiliser "MQTT Explorer" qui peut être téléchargé depuis le [site web de MQTT Explorer](https://mqtt-explorer.com).

Ouvrez MQTT Explorer et ajoutez une nouvelle connexion au Courtier Global hébergé par MeteoFrance en utilisant les détails suivants :

- hôte : globalbroker.meteo.fr
- port : 8883
- nom d'utilisateur : everyone
- mot de passe : everyone

<img alt="connexion-courtier-global-mqtt-explorer" src="../../assets/img/mqtt-explorer-global-broker-connection.png" width="800">

Cliquez sur le bouton 'AVANCÉ', retirez les sujets pré-configurés et ajoutez les sujets suivants auxquels vous abonner :

- `origin/a/wis2/#`

<img alt="mqtt-explorer-courtier-global-avancé" src="../../assets/img/mqtt-explorer-global-broker-sub-origin.png" width="800">

!!! note
    Lors de la configuration des abonnements MQTT, vous pouvez utiliser les jokers suivants :

    - **Niveau unique (+)** : un joker de niveau unique remplace un niveau de sujet
    - **Niveau multiple (#)** : un joker de niveau multiple remplace plusieurs niveaux de sujet

    Dans ce cas, `origin/a/wis2/#` vous abonnera à tous les sujets sous le sujet `origin/a/wis2`.

Cliquez sur 'RETOUR', puis 'ENREGISTRER' pour sauvegarder vos détails de connexion et d'abonnement. Ensuite, cliquez sur 'CONNECTER' :

Les messages devraient commencer à apparaître dans votre session MQTT Explorer comme suit :

<img alt="sujets-courtier-global-mqtt-explorer" src="../../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

Vous êtes maintenant prêt à commencer à explorer les sujets et la structure des messages WIS2.

## Exercice 1 : Examiner la structure des sujets WIS2

Utilisez MQTT pour parcourir la structure des sujets sous les sujets `origin`.

!!! question
    
    Comment pouvons-nous distinguer le centre WIS qui a publié les données ?

??? success "Cliquez pour révéler la réponse"

    Vous pouvez cliquer sur la fenêtre de gauche dans MQTT Explorer pour développer la structure des sujets.
    
    Nous pouvons distinguer le centre WIS qui a publié les données en regardant le quatrième niveau de la structure des sujets. Par exemple, le sujet suivant :

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    nous indique que les données ont été publiées par un centre WIS avec l'identifiant de centre `br-inmet`, qui est l'identifiant de centre pour l'Instituto Nacional de Meteorologia - INMET, Brésil.

!!! question

    Comment pouvons-nous distinguer entre les messages publiés par les centres WIS hébergeant une passerelle GTS-to-WIS2 et les messages publiés par les centres WIS hébergeant un nœud WIS2 ?

??? success "Cliquez pour révéler la réponse"

    Nous pouvons distinguer les messages provenant de la passerelle GTS-to-WIS2 en regardant l'identifiant de centre dans la structure des sujets. Par exemple, le sujet suivant :

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    nous indique que les données ont été publiées par la passerelle GTS-to-WIS2 hébergée par Deutscher Wetterdienst (DWD), Allemagne. La passerelle GTS-to-WIS2 est un type spécial de publieur de données qui publie des données du Système Mondial de Télécommunication (GTS) à WIS2. La structure des sujets est composée par les en-têtes TTAAii CCCC pour les messages GTS.

## Exercice 2 : Examiner la structure des messages WIS2

Déconnectez-vous de MQTT Explorer et mettez à jour les sections 'Avancé' pour changer l'abonnement aux sujets suivants :

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="sujets-courtier-global-mqtt-explorer-exercice2" src="../../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    Le joker `+` est utilisé pour s'abonner à tous les centres WIS.

Reconnectez-vous au Courtier Global et attendez que les messages apparaissent.

Vous pouvez voir le contenu du message WIS2 dans la section "Valeur" sur le côté droit. Essayez de développer la structure des sujets pour voir les différents niveaux du message jusqu'à atteindre le dernier niveau et examinez le contenu du message d'un des messages.

!!! question

    Comment pouvons-nous identifier l'horodatage de la publication des données ? Et comment pouvons-nous identifier l'horodatage de la collecte des données ?

??? success "Cliquez pour révéler la réponse"

    L'horodatage de la publication des données est contenu dans la section `properties` du message avec une clé de `pubtime`.

    L'horodatage de la collecte des données est contenu dans la section `properties` du message avec une clé de `datetime`.

    <img alt="propriétés-message-courtier-global-mqtt-explorer" src="../../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    Comment pouvons-nous télécharger les données à partir de l'URL fournie dans le message ?

??? success "Cliquez pour révéler la réponse"

    L'URL est contenue dans la section `links` avec `rel="canonical"` et définie par la clé `href`.

    Vous pouvez copier l'URL et la coller dans un navigateur web pour télécharger les données.

## Exercice 3 : Examiner la différence entre les sujets 'origin' et 'cache'

Assurez-vous que vous êtes toujours connecté au Courtier Global en utilisant les abonnements aux sujets `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` et `cache/a/wis2/+/data/core/weather/surface-based-observations/synop` comme décrit dans l'Exercice 2.

Essayez d'identifier un message pour le même identifiant de centre publié à la fois sur les sujets `origin` et `cache`.


!!! question

    Quelle est la différence entre les messages publiés sur les sujets `origin` et `cache` ?

??? success "Cliquez pour révéler la réponse"

    Les messages publiés sur les sujets `origin` sont les messages originaux que le Courtier Global republie à partir des Nœuds WIS2 du réseau.

    Les messages publiés sur les sujets `cache` sont les messages pour lesquels les données ont été téléchargées par le Cache Global. Si vous vérifiez le contenu du message du sujet commençant par `cache`, vous verrez que le lien 'canonical' a été mis à jour avec une nouvelle URL.
    
    Il existe plusieurs Caches Globaux dans le réseau WIS2, donc vous recevrez un message de chaque Cache Global qui a téléchargé le message.

    Le Cache Global ne télécharge et ne republie que les messages qui ont été publiés sur la hiérarchie des sujets `../data/core/...`.

## Conclusion

!!! success "Félicitations !"
    Dans cette session pratique, vous avez appris :

    - comment vous abonner aux services du Courtier Global WIS2 en utilisant MQTT Explorer
    - la structure des sujets WIS2
    - la structure des messages de notification WIS2
    - la différence entre les données de base et les données recommandées
    - la structure des sujets utilisée par la passerelle GTS-to-WIS2
    - la différence entre les messages du Courtier Global publiés sur les sujets `origin` et `cache`