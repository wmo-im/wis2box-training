---
title: WIS2 in a box cheatsheet
---

# WIS2 in a box cheatsheet

## Visão Geral

wis2box funciona como um conjunto de comandos Docker Compose. O comando ``wis2box-ctl.py`` é uma utilidade
(escrita em Python) para executar comandos Docker Compose facilmente.

## Essenciais do comando wis2box

### Iniciando e parando

* Iniciar wis2box:

```bash
python3 wis2box-ctl.py start
```

* Parar wis2box:

```bash
python3 wis2box-ctl.py stop
```

* Verificar se todos os containers do wis2box estão funcionando:

```bash
python3 wis2box-ctl.py status
```

* Fazer login em um container do wis2box (*wis2box-management* por padrão):

```bash
python3 wis2box-ctl.py login
```

* Fazer login em um container específico do wis2box:

```bash
python3 wis2box-ctl.py login wis2box-api
```