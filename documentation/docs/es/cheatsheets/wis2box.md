---
title: Hoja de referencia rápida de WIS2 en una caja
---

# Hoja de referencia rápida de WIS2 en una caja

## Visión general

wis2box se ejecuta como un conjunto de comandos de Docker Compose. El comando ``wis2box-ctl.py`` es una utilidad
(escrita en Python) para ejecutar comandos de Docker Compose fácilmente.

## Esenciales del comando wis2box

### Iniciar y detener

* Iniciar wis2box:

```bash
python3 wis2box-ctl.py start
```

* Detener wis2box:

```bash
python3 wis2box-ctl.py stop
```

* Verificar que todos los contenedores de wis2box estén funcionando:

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