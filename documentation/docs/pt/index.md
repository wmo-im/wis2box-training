---
title: Início
---

<img alt="WMO logo" src="../assets/img/wmo-logo.png" width="200">
# Treinamento WIS2 in a box

WIS2 in a box ([wis2box](https://docs.wis2box.wis.wmo.int)) é uma Implementação de Referência Livre e de Código Aberto (FOSS) de um WMO WIS2 Node. O projeto fornece um conjunto de ferramentas plug and play para ingerir, processar e publicar dados meteorológicos/climáticos/hídricos usando abordagens baseadas em padrões alinhados com os princípios do WIS2. O wis2box também fornece acesso a todos os dados na rede WIS2. O wis2box foi projetado para ter uma baixa barreira de entrada para provedores de dados, fornecendo infraestrutura e serviços habilitadores para descoberta, acesso e visualização de dados.

Este treinamento fornece explicações passo a passo de vários aspectos do projeto wis2box, bem como diversos exercícios para ajudá-lo a publicar e baixar dados do WIS2. O treinamento é fornecido na forma de apresentações gerais e exercícios práticos.

Os participantes poderão trabalhar com dados e metadados de teste de exemplo, além de integrar seus próprios dados e metadados.

Este treinamento abrange uma ampla gama de tópicos (instalação/configuração/configuração, publicação/download de dados, etc.).

## Objetivos e resultados de aprendizagem

Os objetivos deste treinamento são familiarizar-se com o seguinte:

- Conceitos e componentes fundamentais da arquitetura WIS2
- Formatos de dados e metadados utilizados no WIS2 para descoberta e acesso
- Arquitetura e ambiente wis2box
- Funções principais do wis2box:
    - Gerenciamento de metadados
    - Ingestão de dados e transformação para formato BUFR
    - Broker MQTT para publicação de mensagens WIS2
    - Endpoint HTTP para download de dados
    - Endpoint API para acesso programático aos dados

## Navegação

A navegação à esquerda fornece um sumário para todo o treinamento.

A navegação à direita fornece um sumário para uma página específica.

## Pré-requisitos

### Conhecimento

- Comandos básicos de Linux (veja o [guia de referência](cheatsheets/linux.md))
- Conhecimento básico de redes e protocolos de Internet

### Software

Este treinamento requer as seguintes ferramentas:

- Uma instância executando sistema operacional Ubuntu (fornecida pelos instrutores da WMO durante sessões de treinamento locais) veja [Acessando sua VM de estudante](practical-sessions/accessing-your-student-vm.md#introduction)
- Cliente SSH para acessar sua instância
- MQTT Explorer em sua máquina local
- Cliente SCP e SFTP para copiar arquivos de sua máquina local

## Convenções

!!! question

    Uma seção marcada desta forma convida você a responder uma pergunta.

Você também notará seções de dicas e notas no texto:

!!! tip

    As dicas compartilham ajuda sobre como melhor realizar as tarefas.

!!! note

    As notas fornecem informações adicionais sobre o tópico abordado pela sessão prática, bem como sobre como melhor realizar as tarefas.

Os exemplos são indicados da seguinte forma:

Configuration
``` {.yaml linenums="1"}
my-collection-defined-in-yaml:
    type: collection
    title: my title defined as a yaml attribute named title
    description: my description as a yaml attribute named description
```

Trechos que precisam ser digitados em um terminal/console são indicados como:

```bash
echo 'Hello world'
```

Os nomes dos contêineres (imagens em execução) são indicados em **negrito**.

## Local e materiais do treinamento

O conteúdo do treinamento, wiki e rastreador de problemas são gerenciados no GitHub em [https://github.com/World-Meteorological-Organization/wis2box-training](https://github.com/World-Meteorological-Organization/wis2box-training).

## Imprimindo o material

Este treinamento pode ser exportado para PDF. Para salvar ou imprimir este material de treinamento, vá para a [página de impressão](print_page) e selecione Arquivo > Imprimir > Salvar como PDF.

## Materiais de exercício

Os materiais de exercício podem ser baixados do arquivo [exercise-materials.zip](/exercise-materials.zip).

## Suporte

Para problemas/bugs/sugestões ou melhorias/contribuições para este treinamento, utilize o [rastreador de problemas do GitHub](https://github.com/World-Meteorological-Organization/wis2box-training/issues).

Todos os bugs, melhorias e problemas do wis2box podem ser relatados no [GitHub](https://github.com/World-Meteorological-Organization/wis2box/issues).

Para suporte adicional ou dúvidas, entre em contato com wis2-support@wmo.int.

Como sempre, a documentação principal do wis2box pode ser encontrada em [https://docs.wis2box.wis.wmo.int](https://docs.wis2box.wis.wmo.int).

Contribuições são sempre incentivadas e bem-vindas!