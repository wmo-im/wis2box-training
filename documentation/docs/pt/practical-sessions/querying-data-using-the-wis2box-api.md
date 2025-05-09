---
title: Consultando dados usando a API wis2box
---

# Consultando dados usando a API wis2box

!!! abstract "Resultados de aprendizado"
    Ao final desta sessão prática, você será capaz de:

    - usar a API wis2box para consultar e filtrar suas estações
    - usar a API wis2box para consultar e filtrar seus dados

## Introdução

A API wis2box fornece acesso de descoberta e consulta de maneira legível por máquina aos dados que foram ingeridos no wis2box. A API é baseada no padrão OGC API - Features e é implementada usando [pygeoapi](https://pygeoapi.io).

A API wis2box oferece acesso às seguintes coleções:

- Estações
- Metadados de descoberta
- Notificações de dados
- mais uma coleção por conjunto de dados configurado, que armazena a saída de bufr2geojson (o plugin `bufr2geojson` precisa ser ativado na configuração de mapeamento de dados para preencher os itens na coleção de conjunto de dados).

Nesta sessão prática, você aprenderá a usar a API de dados para navegar e consultar dados que foram ingeridos no wis2box.

## Preparação

!!! note
    Navegue até a página inicial da API wis2box no seu navegador web:

    `http://YOUR-HOST/oapi`

<img alt="wis2box-api-landing-page" src="../../assets/img/wis2box-api-landing-page.png" width="600">

## Inspeção de coleções

Da página inicial, clique no link 'Coleções'.

!!! question
    Quantas coleções de conjuntos de dados você vê na página resultante? O que você acha que cada coleção representa?

??? success "Clique para revelar a resposta"
    Deveriam ser exibidas 4 coleções, incluindo "Estações", "Metadados de descoberta" e "Notificações de dados"

## Inspeção de estações

Da página inicial, clique no link 'Coleções', depois clique no link 'Estações'.

<img alt="wis2box-api-collections-stations" src="../../assets/img/wis2box-api-collections-stations.png" width="600">

Clique no link 'Navegar', depois clique no link 'json'.

!!! question
    Quantas estações são retornadas? Compare esse número com a lista de estações em `http://YOUR-HOST/wis2box-webapp/station`

??? success "Clique para revelar a resposta"
    O número de estações da API deve ser igual ao número de estações que você vê no wis2box-webapp.

!!! question
    Como podemos consultar por uma única estação (por exemplo, `Balaka`)?

??? success "Clique para revelar a resposta"
    Consulte a API com `http://YOUR-HOST/oapi/collections/stations/items?q=Balaka`.

!!! note
    O exemplo acima é baseado nos dados de teste do Malawi. Tente testar contra as estações que você ingeriu como parte dos exercícios anteriores.

## Inspeção de observações

!!! note
    O exemplo acima é baseado nos dados de teste do Malawi. Tente testar contra a observação que você ingeriu como parte dos exercícios.

Da página inicial, clique no link 'Coleções', depois clique no link 'Observações meteorológicas de superfície do Malawi'.

<img alt="wis2box-api-collections-malawi-obs" src="../../assets/img/wis2box-api-collections-malawi-obs.png" width="600">

Clique no link 'Consultáveis'.

<img alt="wis2box-api-collections-malawi-obs-queryables" src="../../assets/img/wis2box-api-collections-malawi-obs-queryables.png" width="600">

!!! question
    Qual consultável seria usado para filtrar pelo identificador da estação?

??? success "Clique para revelar a resposta"
    O `wigos_station_identifer` é o consultável correto.

Navegue para a página anterior (ou seja, `http://YOUR-HOST/oapi/collections/urn:wmo:md:mwi:mwi_met_centre:surface-weather-observations`)

Clique no link 'Navegar'.

!!! question
    Como podemos visualizar a resposta JSON?

??? success "Clique para revelar a resposta"
    Clicando no link 'JSON' no canto superior direito da página, ou adicionando `f=json` à solicitação da API no navegador web.

Inspeccione a resposta JSON das observações.

!!! question
    Quantos registros são retornados?

!!! question
    Como podemos limitar a resposta a 3 observações?

??? success "Clique para revelar a resposta"
    Adicione `limit=3` à solicitação da API.

!!! question
    Como podemos ordenar a resposta pelas observações mais recentes?

??? success "Clique para revelar a resposta"
    Adicione `sortby=-resultTime` à solicitação da API (observe o sinal `-` para denotar ordem decrescente). Para ordenar pelas observações mais antigas, atualize a solicitação para incluir `sortby=resultTime`.

!!! question
    Como podemos filtrar as observações por uma única estação?

??? success "Clique para revelar a resposta"
    Adicione `wigos_station_identifier=<WSI>` à solicitação da API.

!!! question
    Como podemos receber as observações como um CSV?

??? success "Clique para revelar a resposta"
    Adicione `f=csv` à solicitação da API.

!!! question
    Como podemos mostrar uma única observação (id)?

??? success "Clique para revelar a resposta"
    Usando o identificador de recurso de uma solicitação da API contra as observações, consulte a API para `http://YOUR-HOST/oapi/collections/{collectionId}/items/{featureId}`, onde `{collectionId}` é o nome da sua coleção de observações e `{itemId}` é o identificador da observação única de interesse.

## Conclusão

!!! success "Parabéns!"
    Nesta sessão prática, você aprendeu a:

    - usar a API wis2box para consultar e filtrar suas estações
    - usar a API wis2box para consultar e filtrar seus dados