---
title: Feuille de triche WIS2 en boîte
---

# Feuille de triche WIS2 en boîte

## Vue d'ensemble

wis2box fonctionne comme une suite de commandes Docker Compose. La commande ``wis2box-ctl.py`` est un utilitaire
(écrit en Python) pour exécuter facilement des commandes Docker Compose.

## Essentiels des commandes wis2box

### Démarrage et arrêt

* Démarrer wis2box :

```bash
python3 wis2box-ctl.py start
```

* Arrêter wis2box :

```bash
python3 wis2box-ctl.py stop
```

* Vérifier que tous les conteneurs wis2box sont en fonctionnement :

```bash
python3 wis2box-ctl.py status
```

* Se connecter à un conteneur wis2box (*wis2box-management* par défaut) :

```bash
python3 wis2box-ctl.py login
```

* Se connecter à un conteneur wis2box spécifique :

```bash
python3 wis2box-ctl.py login wis2box-api
```