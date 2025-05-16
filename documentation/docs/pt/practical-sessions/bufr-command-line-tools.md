---
title: Trabalhando com dados BUFR
---

# Trabalhando com dados BUFR

!!! abstract "Resultados de aprendizagem"
    Nesta sessão prática, você será apresentado a algumas das ferramentas BUFR incluídas no contêiner **wis2box-api** que são usadas para transformar dados para o formato BUFR e para ler o conteúdo codificado em BUFR.
    
    Você aprenderá:

    - como inspecionar os cabeçalhos no arquivo BUFR usando o comando `bufr_ls`
    - como extrair e inspecionar os dados dentro de um arquivo bufr usando `bufr_dump`
    - a estrutura básica dos modelos bufr usados em csv2bufr e como usar a ferramenta de linha de comando
    - e como fazer alterações básicas nos modelos bufr e como atualizar o wis2box para usar a versão revisada

## Introdução

Os plugins que produzem notificações com dados BUFR usam processos no wis2box-api para trabalhar com dados BUFR, por exemplo, para transformar os dados de CSV para BUFR ou de BUFR para geojson.

O contêiner wis2box-api inclui várias ferramentas para trabalhar com dados BUFR.

Estas incluem as ferramentas desenvolvidas pelo ECMWF e incluídas no software ecCodes, mais informações sobre estas podem ser encontradas no [site do ecCodes](https://confluence.ecmwf.int/display/ECC/BUFR+tools).

Nesta sessão, você será apresentado ao `bufr_ls` e `bufr_dump` do pacote de software ecCodes e à configuração avançada da ferramenta csv2bufr.

## Preparação

Para usar as ferramentas de linha de comando BUFR, você precisará estar logado no contêiner wis2box-api e, a menos que especificado de outra forma, todos os comandos devem ser executados neste contêiner. Você também precisará ter o MQTT Explorer aberto e conectado ao seu corretor.

Primeiro, conecte-se à sua VM de estudante via seu cliente ssh e depois faça login no contêiner wis2box-api:

```{.copy}
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login wis2box-api
```

Confirme que as ferramentas estão disponíveis, começando com ecCodes:

``` {.copy}
bufr_dump -V
```
Você deve obter a seguinte resposta:

```
ecCodes Version 2.28.0
```

Em seguida, verifique o csv2bufr:

```{.copy}
csv2bufr --version
```

Você deve obter a seguinte resposta:

```
csv2bufr, version 0.7.4
```

Finalmente, crie um diretório de trabalho para trabalhar:

```{.copy}
cd /data/wis2box
mkdir -p working/bufr-cli
cd working/bufr-cli
```

Agora você está pronto para começar a usar as ferramentas BUFR.

## Usando as ferramentas de linha de comando BUFR

### Exercício 1 - bufr_ls
Neste primeiro exercício, você usará o comando `bufr_ls` para inspecionar os cabeçalhos de um arquivo BUFR e determinar o conteúdo do arquivo. Os seguintes cabeçalhos estão incluídos em um arquivo BUFR:

| cabeçalho                            | chave ecCodes                  | descrição                                                                                                                                           |
|--------------------------------------|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| centro originador/gerador            | centre                         | O centro originador / gerador dos dados                                                                                                             |
| sub-centro originador/gerador        | bufrHeaderSubCentre            | O sub-centro originador / gerador dos dados                                                                                                         | 
| Número de sequência de atualização   | updateSequenceNumber           | Se esta é a primeira versão dos dados (0) ou uma atualização (>0)                                                                                   |               
| Categoria de dados                   | dataCategory                   | O tipo de dados contidos na mensagem BUFR, por exemplo, dados de superfície. Veja [Tabela A do BUFR](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)  |
| Subcategoria de dados internacionais | internationalDataSubCategory   | O subtipo de dados contidos na mensagem BUFR, por exemplo, dados de superfície. Veja [Tabela de Códigos Comuns C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) |
| Ano                                  | typicalYear (typicalDate)      | Tempo mais típico para o conteúdo da mensagem BUFR                                                                                                  |
| Mês                                  | typicalMonth (typicalDate)     | Tempo mais típico para o conteúdo da mensagem BUFR                                                                                                  |
| Dia                                  | typicalDay (typicalDate)       | Tempo mais típico para o conteúdo da mensagem BUFR                                                                                                  |
| Hora                                 | typicalHour (typicalTime)      | Tempo mais típico para o conteúdo da mensagem BUFR                                                                                                  |
| Minuto                               | typicalMinute (typicalTime)    | Tempo mais típico para o conteúdo da mensagem BUFR                                                                                                  |
| Descritores BUFR                     | unexpandedDescriptors          | Lista de um ou mais descritores BUFR definindo os dados contidos no arquivo                                                                         |

Baixe o arquivo de exemplo diretamente no contêiner de gerenciamento do wis2box usando o seguinte comando:

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex1.bufr4 --output bufr-cli-ex1.bufr4
```

Agora use o seguinte comando para executar `bufr_ls` neste arquivo:

```bash
bufr_ls bufr-cli-ex1.bufr4
```

Você deve ver a seguinte saída:

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 of 1 messages in bufr-cli-ex1.bufr4

1 of 1 total messages in 1 files
```

Por si só, essa informação não é muito informativa, com apenas informações limitadas sobre o conteúdo do arquivo fornecidas.

A saída padrão não fornece informações sobre o tipo de observação ou dados e está em um formato que não é muito fácil de ler. No entanto, várias opções podem ser passadas para `bufr_ls` para alterar tanto o formato quanto os campos de cabeçalho impressos.

Use `bufr_ls` sem argumentos para visualizar as opções:

```{.copy}
bufr_ls
```

Você deve ver a seguinte saída:

```
NAME    bufr_ls

DESCRIPTION
        List content of BUFR files printing values of some header keys.
        Only scalar keys can be printed.
        It does not fail when a key is not found.

USAGE
        bufr_ls [options] bufr_file bufr_file ...

OPTIONS
        -p key[:{s|d|i}],key[:{s|d|i}],...
                Declaration of keys to print.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be requested. Default type is string.
        -F format
                C style format for floating-point values.
        -P key[:{s|d|i}],key[:{s|d|i}],...
                As -p adding the declared keys to the default list.
        -w key[:{s|d|i}]{=|!=}value,key[:{s|d|i}]{=|!=}value,...
                Where clause.
                Messages are processed only if they match all the key/value constraints.
                A valid constraint is of type key=value or key!=value.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be specified. Default type is string.
                In the value you can also use the forward-slash character '/' to specify an OR condition (i.e. a logical disjunction)
                Note: only one -w clause is allowed.
        -j      JSON output
        -s key[:{s|d|i}]=value,key[:{s|d|i}]=value,...
                Key/values to set.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be defined. By default the native type is set.
        -n namespace
                All the keys belonging to the given namespace are printed.
        -m      Mars keys are printed.
        -V      Version.
        -W width
                Minimum width of each column in output. Default is 10.
        -g      Copy GTS header.
        -7      Does not fail when the message has wrong length

SEE ALSO
        Full documentation and examples at:
        <https://confluence.ecmwf.int/display/ECC/bufr_ls>
```

Agora execute o mesmo comando no arquivo de exemplo, mas saída as informações em JSON.

!!! question
    Que sinal você passa para o comando `bufr_ls` para visualizar a saída em formato JSON?

??? success "Clique para revelar a resposta"
    Você pode alterar o formato de saída para json usando o sinal `-j`, ou seja,
    `bufr_ls -j <arquivo-de-entrada>`. Isso pode ser mais legível do que o formato de saída padrão. Veja o exemplo de saída abaixo:

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

Ao examinar um arquivo BUFR, muitas vezes queremos determinar o tipo de dados contidos no arquivo e a data/hora típica dos dados. Essas informações podem ser listadas usando o sinal `-p` para selecionar os cabeçalhos a serem saídos. Vários cabeçalhos podem ser incluídos usando uma lista separada por vírgulas.

Usando o comando `bufr_ls`, inspecione o arquivo de teste e identifique o tipo de dados contidos no arquivo e a data e hora típicas para esses dados.

??? hint
    As chaves ecCodes estão dadas na tabela acima. Podemos usar o seguinte para listar a dataCategory e
    internationalDataSubCategory dos dados BUFR:

    ```
    bufr_ls -p dataCategory,internationalDataSubCategory bufr-cli-ex1.bufr4
    ```

    Chaves adicionais podem ser adicionadas conforme necessário.

!!! question
    Que tipo de dados (categoria de data e subcategoria) estão contidos no arquivo? Qual é a data e hora típicas
    para os dados?

??? success "Clique para revelar a resposta"
    O comando que você precisa executar deve ter sido semelhante a:
    
    ```
    bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
    ```

    Você pode ter chaves adicionais, ou listado o ano, mês, dia etc individualmente. A saída deve
    ser semelhante a abaixo, dependendo de você ter selecionado a saída JSON ou padrão.

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

    - A categoria de dados é 2, da [Tabela A do BUFR](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)
      podemos ver que este arquivo contém dados de "Sondagens verticais (exceto por satélite)".
    - A subcategoria internacional é 4, indicando
      "Relatórios de temperatura/umidade/vento de nível superior de estações terrestres fixas (TEMP)" dados. Esta informação pode ser consultada na [Tabela de Códigos Comuns C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) (linha 33). Note a combinação
      de categoria e subcategoria.
    - A data e hora típicas são 2023/10/02 e 00:00:00z, respectivamente.

    

### Exercício 2 - bufr_dump

O comando `bufr_dump` pode ser usado para listar e examinar o conteúdo de um arquivo BUFR, incluindo os próprios dados.

Neste exercício, usaremos um arquivo BUFR que é o mesmo que você criou durante a sessão prática inicial de csv2bufr usando o wis2box-webapp.

Baixe o arquivo de amostra para o contêiner de gerenciamento do wis2box diretamente com o seguinte comando:

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex2.bufr4 --output bufr-cli-ex2.bufr4
```

Agora execute o comando `bufr_dump` no arquivo, usando o sinal `-p` para saída dos dados em texto simples (formato chave=valor):

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

Você deve ver cerca de 240 chaves na saída, muitas das quais estão faltando. Isso é típico com dados do mundo real, pois nem todas as chaves eccodes são preenchidas com dados relatados.

!!! hint
    Os valores ausentes podem ser filtrados usando ferramentas como `grep`:
    ```{.copy}
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
    ```

O arquivo BUFR de exemplo para este exercício vem da sessão prática de csv2bufr. Por favor, baixe o arquivo CSV original para o seu local atual da seguinte forma:

```{.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/csv2bufr-ex1.csv --output csv2bufr-ex1.csv
```

E exiba o conteúdo do arquivo com:

```{.copy}
more csv2bufr-ex1.csv
```

!!! question
    Use o seguinte comando para exibir a coluna 18 no arquivo CSV e você encontrará a pressão média do nível do mar relatada (msl_pressure):

    ```{.copy}
    more csv2bufr-ex1.csv | cut -d ',' -f 18
    ```
    
    Qual chave na saída BUFR corresponde à pressão média do nível do mar?

??? hint
    Ferramentas como `grep` podem ser usadas em combinação com `bufr_dump`. Por exemplo:
    
    ```{.copy}
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i "pressure"
    ```
    
    filtraria o conteúdo de `bufr_dump` para apenas aquelas linhas contendo a palavra pressão. Alternativamente,
    a saída poderia ser filtrada em um valor.

??? success "Clique para revelar a resposta"
    A chave "pressureReducedToMeanSeaLevel" corresponde à coluna msl_pressure no arquivo CSV de entrada.

Passe alguns minutos examinando o resto da saída, comparando com o arquivo CSV de entrada antes de passar para o próximo
exercício. Por exemplo, você pode tentar encontrar as chaves na saída BUFR que correspondem à umidade relativa (coluna 23 no arquivo CSV) e à temperatura do ar (coluna 21 no arquivo CSV).

### Exercício 3 - arquivos de mapeamento csv2bufr

A ferramenta csv2bufr pode ser configurada para processar dados tabulares com diferentes colunas e sequências BUFR.

Isso é feito por meio de um arquivo de configuração escrito no formato JSON.

Como os próprios dados BUFR, o arquivo JSON contém uma seção de cabeçalho e uma seção de dados, com essas correspondendo amplamente às mesmas seções em BUFR.

Além disso, algumas opções de formatação são especificadas dentro do arquivo JSON.

O arquivo JSON para o mapeamento padrão pode ser visualizado através do link abaixo (clique com o botão direito e abra em uma nova aba):

[aws-template.json](https://raw.githubusercontent.com/wmo-im/csv2bufr/main/csv2bufr/templates/resources/aws-template.json)

Examine a seção `header` do arquivo de mapeamento (mostrado abaixo) e compare com a tabela do exercício 1 (coluna chave ecCodes):

```
"header":[
    {"eccodes_key": "edition", "value": "const:4"},
    {"eccodes_key": "masterTableNumber", "value": "const:0"},
    {"eccodes_key": "bufrHeaderCentre", "value": "const:0"},
    {"eccodes_key": "bufrHeaderSubCentre", "value": "const:0"},
    {"eccodes_key": "updateSequenceNumber", "value": "const:0"},
    {"eccodes_key": "dataCategory", "value": "const:0"},
    {"eccodes_key": "internationalDataSubCategory", "value": "const:2"},
    {"eccodes_key": "masterTablesVersionNumber", "value": "const:30"},
    {"eccodes_key": "numberOfSubsets", "value": "const:1"},
    {"eccodes_key": "observedData", "value": "const:1"},
    {"eccodes_key": "compressedData", "value": "const:0"},
    {"eccodes_key": "typicalYear", "value": "data:year"},
    {"eccodes_key": "typicalMonth", "value": "data:month"},
    {"eccodes_key": "typicalDay", "value": "data:day"},
    {"eccodes_key": "typicalHour", "value": "data:hour"},
   