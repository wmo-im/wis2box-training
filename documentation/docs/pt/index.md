---
title: Início
---

<img alt="Logotipo da WMO" src="assets/img/wmo-logo.png" width="200">
# Treinamento WIS2 in a box

WIS2 in a box ([wis2box](https://docs.wis2box.wis.wmo.int)) é uma Implementação de Referência Livre e de Código Aberto (FOSS) de um WIS2 Node da WMO. O projeto fornece um conjunto de ferramentas plug and play para ingestão, processamento e publicação de dados meteorológicos/climáticos/hídricos usando abordagens baseadas em padrões alinhadas aos princípios do WIS2. wis2box também oferece acesso a todos os dados na rede WIS2. wis2box é projetado para ter uma barreira baixa de entrada para provedores de dados, fornecendo infraestrutura e serviços habilitadores para descoberta, acesso e visualização de dados.

Este treinamento fornece explicações passo a passo sobre vários aspectos do projeto wis2box, bem como uma série de exercícios
para ajudá-lo a publicar e baixar dados do WIS2. O treinamento é fornecido na forma de apresentações gerais, bem como
exercícios práticos.

Os participantes poderão trabalhar com dados e metadados de teste de amostra, bem como integrar seus próprios dados e metadados.

Este treinamento abrange uma ampla gama de tópicos (instalação/configuração/configuração, publicação/download de dados, etc.).

## Objetivos e resultados de aprendizagem

Os objetivos deste treinamento são se familiarizar com o seguinte:

- Conceitos e componentes centrais da arquitetura WIS2
- Formatos de dados e metadados usados no WIS2 para descoberta e acesso
- Arquitetura e ambiente do wis2box
- Funções principais do wis2box:
    - gestão de metadados
    - ingestão de dados e transformação para o formato BUFR
    - broker MQTT para publicação de mensagens WIS2
    - ponto de extremidade HTTP para download de dados
    - ponto de extremidade da API para acesso programático aos dados

## Navegação

A navegação à esquerda fornece um índice para todo o treinamento.

A navegação à direita fornece um índice para uma página específica.

## Pré-requisitos

### Conhecimento

- Comandos básicos de Linux (veja o [cheatsheet](cheatsheets/linux.md))
- Conhecimento básico de redes e protocolos da Internet

### Software

Este treinamento requer as seguintes ferramentas:

- Uma instância rodando o sistema operacional Ubuntu (fornecida pelos instrutores da WMO durante sessões de treinamento locais) veja [Acessando sua VM de estudante](practical-sessions/accessing-your-student-vm.md#introduction)
- Cliente SSH para acessar sua instância
- MQTT Explorer em sua máquina local
- Cliente SCP e SFTP para copiar arquivos de sua máquina local

## Convenções

!!! question

    Uma seção marcada assim convida você a responder uma pergunta.

Você também notará seções de dicas e notas dentro do texto:

!!! tip

    Dicas compartilham ajuda sobre como realizar tarefas da melhor forma.

!!! note

    Notas fornecem informações adicionais sobre o tópico coberto pela sessão prática, bem como sobre como realizar tarefas da melhor forma.

Exemplos são indicados da seguinte forma:

Configuração
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

Nomes de contêineres (imagens em execução) são denotados em **negrito**.

## Local e materiais do treinamento

Os conteúdos do treinamento, wiki e rastreador de problemas são gerenciados no GitHub em [https://github.com/World-Meteorological-Organization/wis2box-training](https://github.com/World-Meteorological-Organization/wis2box-training).

## Imprimindo o material

Este treinamento pode ser exportado para PDF. Para salvar ou imprimir este material de treinamento, vá para a [página de impressão](print_page) e selecione
Arquivo > Imprimir > Salvar como PDF.

## Materiais do exercício

Os materiais do exercício podem ser baixados do arquivo zip [exercise-materials.zip](/exercise-materials.zip).

## Suporte

Para problemas/bugs/sugestões ou melhorias/contribuições para este treinamento, por favor, use o [rastreador de problemas do GitHub](https://github.com/World-Meteorological-Organization/wis2box-training/issues).

Todos os bugs, melhorias e problemas do wis2box podem ser relatados no [GitHub](https://github.com/World-Meteorological-Organization/wis2box/issues).

Para suporte adicional ou perguntas, por favor, entre em contato com wis2-support@wmo.int.

Como sempre, a documentação principal do wis2box pode ser encontrada em [https://docs.wis2box.wis.wmo.int](https://docs.wis2box.wis.wmo.int).

Contribuições são sempre incentivadas e bem-vindas!