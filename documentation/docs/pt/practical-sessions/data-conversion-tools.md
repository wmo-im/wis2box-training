---
title: Ferramentas de Conversão de Dados
---

# Ferramentas de Conversão de Dados

!!! abstract "Resultados da Aprendizagem"
    Ao final desta sessão prática, você será capaz de:

    - Acessar ferramentas de linha de comando ecCodes dentro do contêiner wis2box-api
    - Usar a ferramenta synop2bufr para converter relatórios FM-12 SYNOP para BUFR pela linha de comando
    - Acionar a conversão synop2bufr através do wis2box-webapp
    - Usar a ferramenta csv2bufr para converter dados CSV para BUFR pela linha de comando

## Introdução

Os dados publicados no WIS2 devem atender aos requisitos e padrões definidos pelas várias comunidades especializadas em disciplinas/domínios do sistema terrestre. Para reduzir a barreira à publicação de dados para observações de superfície terrestres, o wis2box fornece ferramentas para converter dados para o formato BUFR. Essas ferramentas estão disponíveis através do contêiner wis2box-api e podem ser usadas pela linha de comando para testar o processo de conversão de dados.

As principais conversões atualmente suportadas pelo wis2box são relatórios FM-12 SYNOP para BUFR e dados CSV para BUFR. Os dados FM-12 são suportados pois ainda são amplamente utilizados e trocados na comunidade WMO, enquanto os dados CSV são suportados para permitir o mapeamento de dados produzidos por estações meteorológicas automáticas para o formato BUFR.

### Sobre FM-12 SYNOP

Relatórios meteorológicos de superfície de estações terrestres têm sido historicamente reportados por hora ou nos horários sinóticos principais (00, 06, 12 e 18 UTC) e intermediários (03, 09, 15, 21 UTC). Antes da migração para BUFR, esses relatórios eram codificados no formato de texto simples FM-12 SYNOP. Embora a migração para BUFR estivesse programada para ser concluída em 2012, um grande número de relatórios ainda é trocado no formato legado FM-12 SYNOP. Mais informações sobre o formato FM-12 SYNOP podem ser encontradas no Manual da WMO sobre Códigos, Volume I.1 (WMO-No. 306, Volume I.1).

### Sobre ecCodes

A biblioteca ecCodes é um conjunto de bibliotecas de software e utilitários projetados para decodificar e codificar dados meteorológicos nos formatos GRIB e BUFR. É desenvolvida pelo Centro Europeu de Previsões Meteorológicas de Médio Prazo (ECMWF), veja a [documentação ecCodes](https://confluence.ecmwf.int/display/ECC/ecCodes+documentation) para mais informações.

O software wis2box inclui a biblioteca ecCodes na imagem base do contêiner wis2box-api. Isso permite que os usuários acessem as ferramentas de linha de comando e bibliotecas de dentro do contêiner. A biblioteca ecCodes é usada dentro do wis2box-stack para decodificar e codificar mensagens BUFR.

### Sobre csv2bufr e synop2bufr

Além do ecCodes, o wis2box usa os seguintes módulos Python que trabalham com ecCodes para converter dados para o formato BUFR:

- **synop2bufr**: para suportar o formato legado FM-12 SYNOP tradicionalmente usado por observadores manuais. O módulo synop2bufr depende de metadados adicionais da estação para codificar parâmetros adicionais no arquivo BUFR. Veja o [repositório synop2bufr no GitHub](https://github.com/World-Meteorological-Organization/synop2bufr)
- **csv2bufr**: para permitir a conversão de extratos CSV produzidos por estações meteorológicas automáticas para o formato BUFR. O módulo csv2bufr é usado para converter dados CSV para formato BUFR usando um modelo de mapeamento que define como os dados CSV devem ser mapeados para o formato BUFR. Veja o [repositório csv2bufr no GitHub](https://github.com/World-Meteorological-Organization/csv2bufr)

Estes módulos podem ser usados de forma independente ou como parte do stack wis2box.

## Preparação

!!! warning "Pré-requisitos"

    - Certifique-se de que seu wis2box foi configurado e iniciado
    - Certifique-se de ter configurado um conjunto de dados e pelo menos uma estação em seu wis2box
    - Conecte-se ao broker MQTT da sua instância wis2box usando MQTT Explorer
    - Abra o aplicativo web wis2box (`http://YOUR-HOST/wis2box-webapp`) e certifique-se de estar logado
    - Abra o painel Grafana da sua instância acessando `http://YOUR-HOST:3000`

Para usar as ferramentas de linha de comando BUFR, você precisará estar logado no contêiner wis2box-api. A menos que especificado de outra forma, todos os comandos devem ser executados neste contêiner. Você também precisará ter o MQTT Explorer aberto e conectado ao seu broker.

Primeiro, conecte-se à sua VM de estudante via seu cliente SSH e copie os materiais do exercício para o contêiner wis2box-api:

```bash
docker cp ~/exercise-materials/data-conversion-exercises wis2box-api:/root
```

Em seguida, faça login no contêiner wis2box-api e mude para o diretório onde os materiais do exercício estão localizados:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
cd /root/data-conversion-exercises
```

Confirme que as ferramentas estão disponíveis, começando com ecCodes:

```bash
bufr_dump -V
```

Você deve receber a seguinte resposta:

```
ecCodes Version 2.36.0
```

Em seguida, verifique a versão do synop2bufr:

```bash
synop2bufr --version
```

Você deve receber a seguinte resposta:

```
synop2bufr, version 0.7.0
```

Em seguida, verifique o csv2bufr:

```bash
csv2bufr --version
```

Você deve receber a seguinte resposta:

```
csv2bufr, version 0.8.5
```

## Ferramentas de linha de comando ecCodes

A biblioteca ecCodes incluída no contêiner wis2box-api fornece várias ferramentas de linha de comando para trabalhar com arquivos BUFR. 
Os próximos exercícios demonstram como usar `bufr_ls` e `bufr_dump` para verificar o conteúdo de um arquivo BUFR.

### bufr_ls

Neste primeiro exercício, você usará o comando `bufr_ls` para inspecionar os cabeçalhos de um arquivo BUFR e determinar o tipo do conteúdo do arquivo.

Use o seguinte comando para executar `bufr_ls` no arquivo `bufr-cli-ex1.bufr4`:

```bash
bufr_ls bufr-cli-ex1.bufr4
```

Você deve ver a seguinte saída:

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 of 1 messages in bufr-cli-ex1.bufr4

1 of 1 total messages in 1 file
```

Várias opções podem ser passadas para `bufr_ls` para alterar tanto o formato quanto os campos de cabeçalho impressos.

!!! question
     
    Qual seria o comando para listar a saída anterior em formato JSON?

    Você pode executar o comando `bufr_ls` com a flag `-h` para ver as opções disponíveis.

??? success "Clique para revelar a resposta"
    Você pode mudar o formato de saída para JSON usando a flag `-j`, ou seja:
    ```bash
    bufr_ls -j bufr-cli-ex1.bufr4
    ```

    Quando executado, isso deve fornecer a seguinte saída:
    ```
    { "messages" : [
      {
        "centre": "cnmc",
        "masterTablesVersionNumber": 29,
        "localTablesVersionNumber": 0,
        "typicalDate": 20231002,
        "typicalTime": "000000",
        "numberOfSubsets": 1
      }
    ]}
    ```

A saída impressa representa os valores de algumas das chaves de cabeçalho no arquivo BUFR.

Por si só, esta informação não é muito informativa, com apenas informações limitadas sobre o conteúdo do arquivo fornecidas.

Ao examinar um arquivo BUFR, frequentemente queremos determinar o tipo de dados contidos no arquivo e a data/hora típica dos dados no arquivo. Essa informação pode ser listada usando a flag `-p` para selecionar os cabeçalhos a serem exibidos. Múltiplos cabeçalhos podem ser incluídos usando uma lista separada por vírgulas.

Você pode usar o seguinte comando para listar a categoria de dados, subcategoria, data típica e hora:
    
```bash
bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
```

!!! question

    Execute o comando anterior e interprete a saída usando a [Tabela Comum de Códigos C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) para determinar a categoria e subcategoria de dados.

    Que tipo de dados (categoria e subcategoria) está contido no arquivo? Qual é a data e hora típica dos dados?

??? success "Clique para revelar a resposta"
    
    ```
    { "messages" : [
      {
        "dataCategory": 2,
        "internationalDataSubCategory": 4,
        "typicalDate": 20231002,
        "typicalTime": "000000"
      }
    ]}
    ```

    A partir disso, vemos que:

    - A categoria de dados é 2, indicando dados de **"Sondagens verticais (exceto satélite)"**.
    - A subcategoria internacional é 4, indicando **"Relatórios de temperatura/umidade/vento em altitude de estações terrestres fixas (TEMP)"**.
    - A data e hora típicas são 2023-10-02 e 00:00:00z, respectivamente.

### bufr_dump

O comando `bufr_dump` pode ser usado para listar e examinar o conteúdo de um arquivo BUFR, incluindo os próprios dados.

Tente executar o comando `bufr_dump` no segundo arquivo de exemplo `bufr-cli-ex2.bufr4`:

```{.copy}
bufr_dump bufr-cli-ex2.bufr4
```

Isso resulta em um JSON que pode ser difícil de analisar, tente usar a flag `-p` para exibir os dados em texto simples (formato chave=valor):

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

Você verá um grande número de chaves como saída, muitas das quais estão faltando. Isso é típico com dados do mundo real, já que nem todas as chaves eccodes são preenchidas com dados reportados.

Você pode usar o comando `grep` para filtrar a saída e mostrar apenas as chaves que não estão faltando. Por exemplo, para mostrar todas as chaves que não estão faltando, você pode usar o seguinte comando:

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
```

!!! question

    Qual é a pressão reduzida ao nível médio do mar reportada no arquivo BUFR `bufr-cli-ex2.bufr4`?

??? success "Clique para revelar a resposta"

    Usando o seguinte comando:

    ```bash
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i 'pressureReducedToMeanSeaLevel'
    ```

    Você deve ver a seguinte saída:

    ```
    pressureReducedToMeanSeaLevel=105590
    ```
    Isso indica que a pressão reduzida ao nível médio do mar é 105590 Pa (1055,90 hPa).

!!! question

    Qual é o identificador WIGOS da estação que reportou os dados no arquivo BUFR `bufr-cli-ex2.bufr4`?

??? success "Clique para revelar a resposta"

    Usando o seguinte comando:

    ```bash
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i 'wigos'
    ```

    Você deve ver a seguinte saída:

    ```
    wigosIdentifierSeries=0
    wigosIssuerOfIdentifier=20000
    wigosIssueNumber=0
    wigosLocalIdentifierCharacter="99100"
    ```

    Isso indica que o identificador WIGOS da estação é `0-20000-0-99100`.

## Conversão synop2bufr

Agora, vamos ver como converter dados FM-12 SYNOP para formato BUFR usando o módulo `synop2bufr`. O módulo `synop2bufr` é usado para converter dados FM-12 SYNOP para formato BUFR. O módulo está instalado no contêiner wis2box-api e pode ser usado pela linha de comando da seguinte forma:

```{.copy}
synop2bufr data transform \
    --metadata <station-metadata.csv> \
    --output-dir <output-directory-path> \
    --year <year-of-observation> \
    --month <month-of-observation> \
    <input-fm12.txt>
```

O argumento `--metadata` é usado para especificar o arquivo de metadados da estação, que fornece informações adicionais a serem codificadas no arquivo BUFR.
O argumento `--output-dir` é usado para especificar o diretório onde os arquivos BUFR convertidos serão escritos. Os argumentos `--year` e `--month` são usados para especificar o ano e mês da observação.

O módulo `synop2bufr` também é usado no wis2box-webapp para converter dados FM-12 SYNOP para formato BUFR usando um formulário baseado na web.

Os próximos exercícios demonstrarão como o módulo `synop2bufr` funciona e como usá-lo para converter dados FM-12 SYNOP para formato BUFR.

### revisar a mensagem SYNOP de exemplo

Inspecione o arquivo de mensagem SYNOP de exemplo para este exercício `synop_message.txt`:

```bash
cd /root/data-conversion-exercises
more synop_message.txt
```

!!! question

    Quantos relatórios SYNOP estão neste arquivo?

??? success "Clique para revelar a resposta"
    
    A saída mostra o seguinte:

    ```{.copy}
    AAXX 21121
    15015 02999 02501 10103 21090 39765 42952 57020 60001=
    15020 