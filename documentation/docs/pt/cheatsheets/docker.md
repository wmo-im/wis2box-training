---
title: Guia de Consulta Rápida do Docker
---

# Guia de Consulta Rápida do Docker

## Visão Geral

O Docker permite a criação de ambientes virtuais de maneira isolada, apoiando a virtualização de recursos computacionais. O conceito básico por trás do Docker é a contêinerização,
onde softwares podem ser executados como serviços, interagindo com outros contêineres de software, por exemplo.

O fluxo de trabalho típico do Docker envolve a criação e construção de **imagens**, que são então executadas como **contêineres** ativos.

O Docker é usado para executar o conjunto de serviços que compõem o wis2box usando imagens pré-construídas.

### Gerenciamento de Imagens

* Listar imagens disponíveis

```bash
docker image ls
```

* Atualizar uma imagem:

```bash
docker pull my-image:latest
```

* Remover uma imagem:

```bash
docker rmi my-image:local
```

### Gerenciamento de Volumes

* Listar todos os volumes criados:

```bash
docker volume ls
```

* Exibir informações detalhadas sobre um volume:

```bash
docker volume inspect my-volume
```

* Remover um volume:

```bash
docker volume rm my-volume
```

* Remover todos os volumes não utilizados:

```bash
docker volume prune
```

### Gerenciamento de Contêineres

* Exibir uma lista de contêineres atualmente em execução:

```bash
docker ps
```

* Lista de todos os contêineres:

```bash
docker ps -a
```

* Entrar no terminal interativo de um contêiner em execução:


!!! dica

    use `docker ps` para usar o ID do contêiner no comando abaixo

```bash
docker exec -it my-container /bin/bash
```

* Remover um contêiner

```bash
docker rm my-container
```

* Remover um contêiner em execução:

```bash
docker rm -f my-container
```
