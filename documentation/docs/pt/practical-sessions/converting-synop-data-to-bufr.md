---
title: Conversão de dados SYNOP para BUFR
---

# Conversão de dados SYNOP para BUFR a partir da linha de comando

!!! abstract "Resultados de aprendizagem"
    Ao final desta sessão prática, você será capaz de:

    - usar a ferramenta synop2bufr para converter relatórios FM-12 SYNOP para BUFR;
    - diagnosticar e corrigir erros simples de codificação em relatórios FM-12 SYNOP antes da conversão de formato;

## Introdução

Relatórios meteorológicos de superfície de estações terrestres têm sido historicamente relatados a cada hora ou nas principais
(00, 06, 12 e 18 UTC) e horas sinóticas intermediárias (03, 09, 15, 21 UTC). Antes da migração
para BUFR, esses relatórios eram codificados no formato de código SYNOP FM-12 em texto simples. Embora a migração para BUFR
estivesse programada para ser concluída até 2012, um grande número de relatórios ainda é trocado no legado
formato FM-12 SYNOP. Mais informações sobre o formato FM-12 SYNOP podem ser encontradas no Manual da OMM sobre Códigos,
Volume I.1 (OMM-No. 306, Volume I.1).

[Manual da OMM sobre Códigos, Volume I.1](https://library.wmo.int/records/item/35713-manual-on-codes-international-codes-volume-i-1)

Para auxiliar na conclusão da migração para BUFR, algumas ferramentas foram desenvolvidas para
codificar relatórios FM-12 SYNOP para BUFR, nesta sessão você aprenderá como usar essas ferramentas, bem
como a relação entre as informações contidas nos relatórios FM-12 SYNOP e as mensagens BUFR.

## Preparação

!!! warning "Pré-requisitos"

    - Certifique-se de que seu wis2box foi configurado e iniciado.
    - Confirme o status visitando a API wis2box (`http://<seu-nome-de-host>/oapi`) e verificando se a API está funcionando.
    - Certifique-se de ler as seções **synop2bufr primer** e **ecCodes primer** antes de iniciar os exercícios.

## synop2bufr primer

Abaixo estão comandos e configurações essenciais do `synop2bufr`:

### transform
A função `transform` converte uma mensagem SYNOP para BUFR:

```bash
synop2bufr data transform --metadata my_file.csv --output-dir ./my_directory --year message_year --month message_month my_SYNOP.txt
```

Observe que, se as opções de metadados, diretório de saída, ano e mês não forem especificadas, elas assumirão seus valores padrão:

| Opção        | Padrão |
| ------------ | ------- |
| --metadata   | station_list.csv |
| --output-dir | O diretório de trabalho atual. |
| --year       | O ano atual. |
| --month      | O mês atual. |

!!! note
    Deve-se ter cautela ao usar o ano e o mês padrão, pois o dia do mês especificado no relatório pode não corresponder (por exemplo, junho não tem 31 dias).

Nos exemplos, o ano e o mês não são dados, então sinta-se à vontade para especificar uma data você mesmo ou usar os valores padrão.

## ecCodes primer

ecCodes fornece tanto ferramentas de linha de comando quanto pode ser incorporado em suas próprias aplicações. Abaixo estão algumas utilidades de linha de comando úteis para trabalhar com dados BUFR.

### bufr_dump

O comando `bufr_dump` é uma ferramenta genérica de informações BUFR. Ele possui muitas opções, mas as seguintes serão as mais aplicáveis aos exercícios:

```bash
bufr_dump -p my_bufr.bufr4
```

Isso exibirá o conteúdo BUFR na sua tela. Se você estiver interessado nos valores assumidos por uma variável em particular, use o comando `egrep`:

```bash
bufr_dump -p my_bufr.bufr4 | egrep -i temperature
```

Isso exibirá variáveis relacionadas à temperatura em seus dados BUFR. Se você quiser fazer isso para vários tipos de variáveis, filtre a saída usando um pipe (`|`):

```bash
bufr_dump -p my_bufr.bufr4 | egrep -i 'temperature|wind'
```

## Convertendo FM-12 SYNOP para BUFR usando synop2bufr a partir da linha de comando

A biblioteca eccodes e o módulo synop2bufr estão instalados no contêiner wis2box-api. Para fazer os próximos exercícios, copiaremos o diretório synop2bufr-exercises para o contêiner wis2box-api e executaremos os exercícios a partir daí.

```bash
docker cp ~/exercise-materials/synop2bufr-exercises wis2box-api:/root
```

Agora podemos entrar no contêiner e executar os exercícios:

```bash
docker exec -it wis2box-api /bin/bash
```

### Exercício 1
Navegue até o diretório `/root/synop2bufr-exercises/ex_1` e inspecione o arquivo de mensagem SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_1
more message.txt
```

!!! question

    Quantos relatórios SYNOP estão neste arquivo?

??? success "Clique para revelar a resposta"
    
    Há 1 relatório SYNOP, pois há apenas 1 delimitador (=) no final da mensagem.

Inspecione a lista de estações:

```bash
more station_list.csv
```

!!! question

    Quantas estações estão listadas na lista de estações?

??? success "Clique para revelar a resposta"

    Há 1 estação, o arquivo station_list.csv contém uma linha de metadados da estação.

!!! question
    Tente converter `message.txt` para o formato BUFR.

??? success "Clique para revelar a resposta"

    Para converter a mensagem SYNOP para o formato BUFR, use o seguinte comando:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

!!! tip

    Veja a seção [synop2bufr primer](#synop2bufr-primer).

Inspecione os dados BUFR resultantes usando `bufr_dump`.

!!! question
     Descubra como comparar os valores de latitude e longitude com aqueles na lista de estações.

??? success "Clique para revelar a resposta"

    Para comparar os valores de latitude e longitude nos dados BUFR com aqueles na lista de estações, use o seguinte comando:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | egrep -i 'latitude|longitude'
    ```

    Isso exibirá os valores de latitude e longitude nos dados BUFR.

!!! tip

    Veja a seção [ecCodes primer](#eccodes-primer).

### Exercício 2
Navegue até o diretório `exercise-materials/synop2bufr-exercises/ex_2` e inspecione o arquivo de mensagem SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_2
more message.txt
```

!!! question

    Quantos relatórios SYNOP estão neste arquivo?

??? success "Clique para revelar a resposta"

    Há 3 relatórios SYNOP, pois há 3 delimitadores (=) no final da mensagem.

Inspecione a lista de estações:

```bash
more station_list.csv
```

!!! question

    Quantas estações estão listadas na lista de estações?

??? success "Clique para revelar a resposta"

    Há 3 estações, o arquivo station_list.csv contém três linhas de metadados da estação.

!!! question
    Converta `message.txt` para o formato BUFR.

??? success "Clique para revelar a resposta"

    Para converter a mensagem SYNOP para o formato BUFR, use o seguinte comando:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

!!! question

    Com base nos resultados dos exercícios nesta e na sessão anterior, como você preveria o número de
    arquivos BUFR resultantes com base no número de relatórios SYNOP e estações listadas no arquivo de metadados da estação?

??? success "Clique para revelar a resposta"

    Para ver os arquivos BUFR produzidos, execute o seguinte comando:

    ```bash
    ls -l *.bufr4
    ```

    O número de arquivos BUFR produzidos será igual ao número de relatórios SYNOP no arquivo de mensagem.

Inspecione os dados BUFR resultantes usando `bufr_dump`.

!!! question
    Como você pode verificar o ID da Estação WIGOS codificado dentro dos dados BUFR de cada arquivo produzido?

??? success "Clique para revelar a resposta"

    Isso pode ser feito usando os seguintes comandos:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15020_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15090_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    Observe que, se você tiver um diretório com apenas esses 3 arquivos BUFR, você pode usar curingas do Linux da seguinte forma:

    ```bash
    bufr_dump -p *.bufr4 | egrep -i 'wigos'
    ```

### Exercício 3
Navegue até o diretório `exercise-materials/synop2bufr-exercises/ex_3` e inspecione o arquivo de mensagem SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_3
more message.txt
```

Esta mensagem SYNOP contém apenas um relatório mais longo com mais seções.

Inspecione a lista de estações:

```bash
more station_list.csv
```

!!! question

    É problemático que este arquivo contenha mais estações do que há relatórios na mensagem SYNOP?

??? success "Clique para revelar a resposta"

    Não, isso não é um problema desde que exista uma linha no arquivo da lista de estações com um TSI da estação que corresponda ao do relatório SYNOP que estamos tentando converter.

!!! note

    O arquivo da lista de estações é uma fonte de metadados para o `synop2bufr` fornecer as informações ausentes no relatório SYNOP alfanumérico e necessárias no SYNOP BUFR.

!!! question
    Converta `message.txt` para o formato BUFR.

??? success "Clique para revelar a resposta"

    Isso é feito usando o comando `transform`, por exemplo:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

Inspecione os dados BUFR resultantes usando `bufr_dump`.

!!! question

    Encontre as seguintes variáveis:

    - Temperatura do ar (K) do relatório
    - Cobertura total de nuvens (%) do relatório
    - Período total de sol (minutos) do relatório
    - Velocidade do vento (m/s) do relatório

??? success "Clique para revelar a resposta"

    Para encontrar as variáveis por palavra-chave nos dados BUFR, você pode usar os seguintes comandos:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15260_20240921T115500.bufr4 | egrep -i 'temperature'
    ```

    Você pode usar o seguinte comando para pesquisar várias palavras-chave:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15260_20240921T115500.bufr4 | egrep -i 'temperature|cover|sunshine|wind'
    ```

!!! tip

    Você pode achar o último comando da seção [ecCodes primer](#eccodes-primer) útil.


### Exercício 4
Navegue até o diretório `exercise-materials/synop2bufr-exercises/ex_4` e inspecione o arquivo de mensagem SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_4
more message_incorrect.txt
```

!!! question

    O que está incorreto neste arquivo SYNOP?

??? success "Clique para revelar a resposta"

    O relatório SYNOP para 15015 está faltando o delimitador (`=`) que permite ao `synop2bufr` distinguir este relatório do próximo.

Tente converter `message_incorrect.txt` usando `station_list.csv`

!!! question

    Quais problemas você encontrou com essa conversão?

??? success "Clique para revelar a resposta"

    Para converter a mensagem SYNOP para o formato BUFR, use o seguinte comando:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message_incorrect.txt
    ```

    Tentar converter deve levantar os seguintes erros:
    
    - `[ERROR] Não foi possível decodificar a mensagem SYNOP`
    - `[ERROR] Erro ao analisar o relatório SYNOP: AAXX 21121 15015 02999 02501 10103 21090 39765 42952 57020 60001 15020 02997 23104 10130 21075 30177 40377 58020 60001 81041. 10130 não é um grupo válido!`

### Exercício 5
Navegue até o diretório `exercise-materials/synop2bufr-exercises/ex_5` e inspecione o arquivo de mensagem SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_5
more message.txt
```

Tente converter `message.txt` para o formato BUFR usando `station_list_incorrect.csv` 

!!! question

    Quais problemas você encontrou com essa conversão?  
    Considerando o erro apresentado, justifique o número de arquivos BUFR produzidos.

??? success "Clique para revelar a resposta"

    Para converter a mensagem SYNOP para o formato BUFR, use o seguinte comando:

    ```bash
    synop2bufr data transform --metadata station_list_incorrect.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

    Um dos TSIs da estação (`15015`) não tem metadados correspondentes na lista de estações, o que impedirá o synop2bufr de acessar metadados adicionais necessários para converter o primeiro relatório SYNOP para BUFR.

    Você verá o seguinte aviso:

    - `[WARNING] Estação 15015 não encontrada no arquivo de estação`

    Você pode ver o número de arquivos BUFR produzidos executando o seguinte comando:

    ```bash
    ls -l *.bufr4
    ```

    Há 3 relatórios SYNOP em message.txt, mas apenas 2 arquivos BUFR foram produzidos. Isso ocorre porque um dos relatórios SYNOP não tinha os metadados necessários, conforme mencionado acima.

## Conclusão

!!! success "Parabéns!"

    Nesta sessão prática, você aprendeu:

    - como a ferramenta synop2bufr pode ser usada para converter relatórios FM-12 SYNOP para BUFR;
    - como diagnosticar e corrigir erros simples de codificação em relatórios FM-12 SYNOP antes da conversão de formato;