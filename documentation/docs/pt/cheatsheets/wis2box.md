---
title: Guia rápido do WIS2 em uma caixa
---

# Guia rápido do WIS2 em uma caixa

## Visão Geral

O wis2box é executado como um conjunto de comandos do Docker Compose. O comando ``wis2box-ctl.py`` é uma utilidade
(escrita em Python) para executar comandos do Docker Compose facilmente.

## Comandos essenciais do wis2box

### Iniciando e parando

* Iniciar o wis2box:

```bash
python3 wis2box-ctl.py start
```

* Parar o wis2box:

```bash
python3 wis2box-ctl.py stop
```

* Verificar se todos os contêineres do wis2box estão funcionando:

```bash
python3 wis2box-ctl.py status
```

* Fazer login em um contêiner do wis2box (*wis2box-management* por padrão):

```bash
python3 wis2box-ctl.py login
```

* Fazer login em um contêiner específico do wis2box:

```bash
python3 wis2box-ctl.py login wis2box-api
```