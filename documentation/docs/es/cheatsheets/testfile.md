---
title: WIS2 in a box cheatsheet
---

# WIS2 in a box cheatsheet

## Resumen

wis2box se ejecuta como un conjunto de comandos de Docker Compose. El comando ``wis2box-ctl.py`` es una utilidad 
(escrita en Python) para ejecutar comandos de Docker Compose de manera sencilla.

## Comandos esenciales de wis2box

### Iniciar y detener

* Iniciar wis2box:

```bash
python3 wis2box-ctl.py start
```

* Detener wis2box:

```bash
python3 wis2box-ctl.py stop
```

* Verificar que todos los contenedores de wis2box estén en ejecución:

```bash
python3 wis2box-ctl.py status
```

* Iniciar sesión en un contenedor de wis2box (*wis2box-management* por defecto):

```bash
python3 wis2box-ctl.py login
```

* Iniciar sesión en un contenedor específico de wis2box:

```bash
python3 wis2box-ctl.py login wis2box-api
```