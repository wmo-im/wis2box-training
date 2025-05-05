---
title: Consultando dados usando a API do wis2box
---

# Consultando dados usando a API do wis2box

!!! abstract "Objetivos de aprendizagem"
    Ao final desta sessão prática, você será capaz de:

    - usar a API do wis2box para consultar e filtrar suas estações
    - usar a API do wis2box para consultar e filtrar seus dados

## Introdução

A API do wis2box fornece acesso de descoberta e consulta de forma legível por máquina aos dados que foram inseridos no wis2box. A API é baseada no padrão OGC API - Features e é implementada usando [pygeoapi](https://pygeoapi.io).

A API do wis2box fornece acesso às seguintes coleções:

- Estações
- Metadados de descoberta
- Notificações de dados
- mais uma coleção por conjunto de dados configurado, que armazena a saída do bufr2geojson (o plugin `bufr2geojson` precisa estar habilitado na configuração dos mapeamentos de dados para preencher os itens na coleção do conjunto de dados).

Nesta sessão prática, você aprenderá como usar a API de dados para navegar e consultar dados que foram inseridos no wis2box.

## Preparação

!!! note
    Navegue até a página inicial da API do wis2box em seu navegador:

    `http://YOUR-HOST/oapi`

<img alt="wis2box-api-landing-page" src="../../assets/img/wis2box-api-landing-page.png" width="600">

## Inspecionando coleções

Na página inicial, clique no link 'Collections'.

!!! question
    Quantas coleções de dados você vê na página resultante? O que você acha que cada coleção representa?

??? success "Clique para revelar a resposta"
    Devem ser exibidas 4 coleções, incluindo "Stations", "Discovery metadata" e "Data notifications"

## Inspecionando estações

Na página inicial, clique no link 'Collections' e depois no link 'Stations'.

<img alt="wis2box-api-collections-stations" src="../../assets/img/wis2box-api-collections-stations.png" width="600">

Clique no link 'Browse' e depois no link 'json'.

!!! question
    Quantas estações são retornadas? Compare este número com a lista de estações em `http://YOUR-HOST/wis2box-webapp/station`

??? success "Clique para revelar a resposta"
    O número de estações da API deve ser igual ao número de estações que você vê no webapp do wis2box.

!!! question
    Como podemos consultar uma única estação (por exemplo, `Balaka`)?

??? success "Clique para revelar a resposta"
    Consulte a API com `http://YOUR-HOST/oapi/collections/stations/items?q=Balaka`.

!!! note
    O exemplo acima é baseado nos dados de teste do Malawi. Tente testar com as estações que você inseriu como parte dos exercícios anteriores.

## Inspecionando observações

!!! note
    O exemplo acima é baseado nos dados de teste do Malawi. Tente testar com as observações que você inseriu como parte dos exercícios.

Na página inicial, clique no link 'Collections' e depois no link 'Surface weather observations from Malawi'.

<img alt="wis2box-api-collections-malawi-obs" src="../../assets/img/wis2box-api-collections-malawi-obs.png" width="600">

Clique no link 'Queryables'.

<img alt="wis2box-api-collections-malawi-obs-queryables" src="../../assets/img/wis2box-api-collections-malawi-obs-queryables.png" width="600">

!!! question
    Qual queryable seria usado para filtrar por identificador de estação?

??? success "Clique para revelar a resposta"
    O `wigos_station_identifer` é o queryable correto.

Navegue até a página anterior (ou seja, `http://YOUR-HOST/oapi/collections/urn:wmo:md:mwi:mwi_met_centre:surface-weather-observations`)

Clique no link 'Browse'.

!!! question
    Como podemos visualizar a resposta JSON?

??? success "Clique para revelar a resposta"
    Clicando no link 'JSON' no canto superior direito da página, ou adicionando `f=json` à solicitação da API no navegador.

Inspecione a resposta JSON das observações.

!!! question
    Quantos registros são retornados?

!!! question
    Como podemos limitar a resposta a 3 observações?

??? success "Clique para revelar a resposta"
    Adicione `limit=3` à solicitação da API.

!!! question
    Como podemos ordenar a resposta pelas observações mais recentes?

??? success "Clique para revelar a resposta"
    Adicione `sortby=-resultTime` à solicitação da API (observe o sinal `-` para indicar ordem decrescente). Para ordenar pelas observações mais antigas, atualize a solicitação para incluir `sortby=resultTime`.

!!! question
    Como podemos filtrar as observações por uma única estação?

??? success "Clique para revelar a resposta"
    Adicione `wigos_station_identifier=<WSI>` à solicitação da API.

!!! question
    Como podemos receber as observações como CSV?

??? success "Clique para revelar a resposta"
    Adicione `f=csv` à solicitação da API.

!!! question
    Como podemos mostrar uma única observação (id)?

??? success "Clique para revelar a resposta"
    Usando o identificador de recurso de uma solicitação da API contra as observações, consulte a API em `http://YOUR-HOST/oapi/collections/{collectionId}/items/{featureId}`, onde `{collectionId}` é o nome da sua coleção de observações e `{itemId}` é o identificador da observação única de interesse.

## Conclusão

!!! success "Parabéns!"
    Nesta sessão prática, você aprendeu como:

    - usar a API do wis2box para consultar e filtrar suas estações
    - usar a API do wis2box para consultar e filtrar seus dados