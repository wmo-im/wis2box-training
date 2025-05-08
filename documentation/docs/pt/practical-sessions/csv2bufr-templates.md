---
title: Templates de mapeamento CSV-para-BUFR
---

# Templates de mapeamento CSV-para-BUFR

!!! abstract "Objetivos de aprendizagem"
    Ao final desta sessão prática, você será capaz de:

    - criar um novo template de mapeamento BUFR para seus dados CSV
    - editar e depurar seu template personalizado de mapeamento BUFR pela linha de comando
    - configurar o plugin de dados CSV-para-BUFR para usar um template personalizado de mapeamento BUFR
    - usar os templates integrados AWS e DAYCLI para converter dados CSV para BUFR

## Introdução

Arquivos de valores separados por vírgula (CSV) são frequentemente utilizados para registrar dados observacionais e outros dados em formato tabular.
A maioria dos registradores de dados usados para gravar saídas de sensores podem exportar as observações em arquivos delimitados, incluindo CSV.
Da mesma forma, quando os dados são inseridos em um banco de dados, é fácil exportar os dados necessários em arquivos formatados em CSV.

O módulo wis2box csv2bufr fornece uma ferramenta de linha de comando para converter dados CSV para o formato BUFR. Ao usar o csv2bufr, você precisa fornecer um template de mapeamento BUFR que mapeia colunas CSV para elementos BUFR correspondentes. Se você não quiser criar seu próprio template de mapeamento, pode usar os templates integrados AWS e DAYCLI para converter dados CSV para BUFR, mas precisará garantir que os dados CSV que está usando estejam no formato correto para esses templates. Se você quiser decodificar parâmetros que não estão incluídos nos templates AWS e DAYCLI, precisará criar seu próprio template de mapeamento.

Nesta sessão, você aprenderá como criar seu próprio template de mapeamento para converter dados CSV para BUFR. Você também aprenderá como usar os templates integrados AWS e DAYCLI para converter dados CSV para BUFR.

## Preparação

Certifique-se de que o wis2box-stack foi iniciado com `python3 wis2box.py start`

Certifique-se de ter um navegador web aberto com a interface MinIO para sua instância acessando `http://YOUR-HOST:9000`
Se você não se lembra de suas credenciais MinIO, pode encontrá-las no arquivo `wis2box.env` no diretório `wis2box` em sua VM de estudante.

Certifique-se de que você tem o MQTT Explorer aberto e conectado ao seu broker usando as credenciais `everyone/everyone`.

## Criando um template de mapeamento

O módulo csv2bufr vem com uma ferramenta de linha de comando para criar seu próprio template de mapeamento usando um conjunto de sequências BUFR e/ou elementos BUFR como entrada.

Para encontrar sequências e elementos BUFR específicos, você pode consultar as tabelas BUFR em [https://confluence.ecmwf.int/display/ECC/BUFR+tables](https://confluence.ecmwf.int/display/ECC/BUFR+tables).

### Ferramenta de linha de comando csv2bufr mappings

Para acessar a ferramenta de linha de comando csv2bufr, você precisa fazer login no container wis2box-api:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
```

Para imprimir a página de ajuda para o comando `csv2bufr mapping`:

```bash
csv2bufr mappings --help
```

A página de ajuda mostra 2 subcomandos:

- `csv2bufr mappings create` : Criar um novo template de mapeamento
- `csv2bufr mappings list` : Listar os templates de mapeamento disponíveis no sistema

!!! Note "csv2bufr mapping list"

    O comando `csv2bufr mapping list` mostrará os templates de mapeamento disponíveis no sistema.
    Os templates padrão são armazenados no diretório `/opt/wis2box/csv2bufr/templates` no container.

    Para compartilhar templates de mapeamento personalizados com o sistema, você pode armazená-los no diretório definido por `$CSV2BUFR_TEMPLATES`, que é definido como `/data/wis2box/mappings` por padrão no container. Como o diretório `/data/wis2box/mappings` no container está montado no diretório `$WIS2BOX_HOST_DATADIR/mappings` no host, você encontrará seus templates de mapeamento personalizados no diretório `$WIS2BOX_HOST_DATADIR/mappings` no host.

Vamos tentar criar um novo template de mapeamento personalizado usando o comando `csv2bufr mapping create` usando como entrada a sequência BUFR 301150 mais o elemento BUFR 012101.

```bash
csv2bufr mappings create 301150 012101 --output /data/wis2box/mappings/my_custom_template.json
```

Você pode verificar o conteúdo do template de mapeamento que acabou de criar usando o comando `cat`:

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "Inspeção do template de mapeamento"

    Quantas colunas CSV estão sendo mapeadas para elementos BUFR? Qual é o cabeçalho CSV para cada elemento BUFR sendo mapeado?

??? success "Clique para revelar a resposta"
    
    O template de mapeamento que você criou mapeia **5** colunas CSV para elementos BUFR, especificamente os 4 elementos BUFR na sequência 301150 mais o elemento BUFR 012101.

    As seguintes colunas CSV estão sendo mapeadas para elementos BUFR:

    - **wigosIdentifierSeries** mapeia para `"eccodes_key": "#1#wigosIdentifierSeries"` (elemento BUFR 001125)
    - **wigosIssuerOfIdentifier** mapeia para `"eccodes_key": "#1#wigosIssuerOfIdentifier` (elemento BUFR 001126)
    - **wigosIssueNumber** mapeia para `"eccodes_key": "#1#wigosIssueNumber"` (elemento BUFR 001127)
    - **wigosLocalIdentifierCharacter** mapeia para `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (elemento BUFR 001128)
    - **airTemperature** mapeia para `"eccodes_key": "#1#airTemperature"` (elemento BUFR 012101)

O template de mapeamento que você criou não inclui metadados importantes sobre a observação que foi feita, a data e hora da observação, e a latitude e longitude da estação.

Em seguida, vamos atualizar o template de mapeamento e adicionar as seguintes sequências:
    
- **301011** para Data (Ano, mês, dia)
- **301012** para Hora (Hora, minuto)
- **301023** para Localização (Latitude/longitude (precisão aproximada))

E os seguintes elementos:

- **010004** para Pressão
- **007031** para Altura do barômetro acima do nível médio do mar

Execute o seguinte comando para atualizar o template de mapeamento:

```bash
csv2bufr mappings create 301150 301011 301012 301023 007031 012101 010004  --output /data/wis2box/mappings/my_custom_template.json
```

E inspecione o conteúdo do template de mapeamento novamente:

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "Inspeção do template de mapeamento atualizado"

    Quantas colunas CSV estão agora sendo mapeadas para elementos BUFR? Qual é o cabeçalho CSV para cada elemento BUFR sendo mapeado?

??? success "Clique para revelar a resposta"
    
    O template de mapeamento que você criou agora mapeia **18** colunas CSV para elementos BUFR:
    - 4 elementos BUFR da sequência BUFR 301150
    - 3 elementos BUFR da sequência BUFR 301011
    - 2 elementos BUFR da sequência BUFR 301012
    - 2 elementos BUFR da sequência BUFR 301023
    - elemento BUFR 007031
    - elemento BUFR 012101

    As seguintes colunas CSV estão sendo mapeadas para elementos BUFR:

    - **wigosIdentifierSeries** mapeia para `"eccodes_key": "#1#wigosIdentifierSeries"` (elemento BUFR 001125)
    - **wigosIssuerOfIdentifier** mapeia para `"eccodes_key": "#1#wigosIssuerOfIdentifier` (elemento BUFR 001126)
    - **wigosIssueNumber** mapeia para `"eccodes_key": "#1#wigosIssueNumber"` (elemento BUFR 001127)
    - **wigosLocalIdentifierCharacter** mapeia para `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (elemento BUFR 001128)
    - **year** mapeia para `"eccodes_key": "#1#year"` (elemento BUFR 004001)
    - **month** mapeia para `"eccodes_key": "#1#month"` (elemento BUFR 004002)
    - **day** mapeia para `"eccodes_key": "#1#day"` (elemento BUFR 004003)
    - **hour** mapeia para `"eccodes_key": "#1#hour"` (elemento BUFR 004004)
    - **minute** mapeia para `"eccodes_key": "#1#minute"` (elemento BUFR 004005)
    - **latitude** mapeia para `"eccodes_key": "#1#latitude"` (elemento BUFR 005002)
    - **longitude** mapeia para `"eccodes_key": "#1#longitude"` (elemento BUFR 006002)
    - **heightOfBarometerAboveMeanSeaLevel"** mapeia para `"eccodes_key": "#1#heightOfBarometerAboveMeanSeaLevel"` (elemento BUFR 007031)
    - **airTemperature** mapeia para `"eccodes_key": "#1#airTemperature"` (elemento BUFR 012101)
    - **nonCoordinatePressure** mapeia para `"eccodes_key": "#1#nonCoordinatePressure"` (elemento BUFR 010004)

Verifique o conteúdo do arquivo `custom_template_data.csv` no diretório `/root/data-conversion-exercises`:

```bash
cat /root/data-conversion-exercises/custom_template_data.csv
```

Observe que os cabeçalhos deste arquivo CSV são os mesmos que os cabeçalhos CSV no template de mapeamento que você criou.

Para testar a conversão de dados, podemos usar a ferramenta de linha de comando `csv2bufr` para converter o arquivo CSV para BUFR usando o template de mapeamento que criamos:

```bash
csv2bufr data transform --bufr-template my_custom_template /root/data-conversion-exercises/custom_template_data.csv
```

Você deverá ver a seguinte saída:

```bash
CLI:    ... Transforming /root/data-conversion-exercises/custom_template_data.csv to BUFR ...
CLI:    ... Processing subsets:
CLI:    ..... 94 bytes written to ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
CLI:    End of processing, exiting.
```

!!! question "Verificar o conteúdo do arquivo BUFR"
    
    Como você pode verificar o conteúdo do arquivo BUFR que acabou de criar e verificar se ele codificou os dados corretamente?

??? success "Clique para revelar a resposta"

    Você pode usar o comando `bufr_dump -p` para verificar o conteúdo do arquivo BUFR que acabou de criar.
    O comando mostrará o conteúdo do arquivo BUFR em um formato legível por humanos.

    ```bash
    bufr_dump -p ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
    ```

    Na saída, você verá valores para os elementos BUFR que você mapeou no template, por exemplo, a "airTemperature" mostrará:
    
    ```bash
    airTemperature=298.15
    ```

Agora você pode sair do container:

```bash
exit
```

### Usando o template de mapeamento no wis2box

Para garantir que o novo template de mapeamento seja reconhecido pelo container wis2box-api, você precisa reiniciar o container:

```bash
docker restart wis2box-api
```

Agora você pode configurar seu conjunto de dados no wis2box-webapp para usar o template de mapeamento personalizado para o plugin de conversão CSV para BUFR.

O wis2box-webapp detectará automaticamente o template de mapeamento que você criou e o disponibilizará na lista de templates para o plugin de conversão CSV para BUFR.

Clique no conjunto de dados que você criou na sessão prática anterior e clique em "UPDATE" ao lado do plugin com nome "CSV data converted to BUFR":

<img alt="Imagem mostrando o editor de conjunto de dados no wis2box-webapp" src="../../assets/img/wis2box-webapp-data-mapping-update-csv2bufr.png"/>

Você deverá ver o novo template que criou na lista de templates disponíveis:

<img alt="Imagem mostrando os templates csv2bufr no wis2box-webapp" src="../../assets/img/wis2box-webapp-csv2bufr-templates.png"/>

!!! hint

    Note que se você não vir o novo template que criou, tente atualizar a página ou abri-la em uma nova janela anônima.

Por enquanto, mantenha a seleção padrão do template AWS (clique no canto superior direito para fechar a configuração do plugin).

## Usando o template 'AWS'

O template 'AWS' fornece um template de mapeamento para converter dados CSV para a sequência BUFR 301150, 307096, em suporte aos requisitos mínimos do GBON.

A descrição do template AWS pode ser encontrada aqui [aws-template](./../csv2bufr-templates/aws-template.md).

### Revisar os dados de entrada do exemplo aws

Baixe o exemplo para este exercício do link abaixo:

[aws-example.csv](./../sample-data/aws-example.csv)

Abra o arquivo que você baixou em um editor e inspecione o conteúdo:

!!! question
    Examinando os campos de data, hora e identificação (identificadores WIGOS e tradicionais), o que
    você nota? Como a data de hoje seria representada?

??? success "Clique para revelar a resposta"
    Cada coluna contém uma única informação. Por exemplo, a data é dividida em
    ano, mês e dia, espelhando como os dados são armazenados em BUFR. A data de hoje seria
    dividida nas colunas "year", "month" e "day". Da mesma forma, o horário precisa ser
    dividido em "hour" e "minute" e o identificador da estação WIGOS em seus respectivos componentes.

!!! question
    Olhando para o arquivo de dados, como os dados ausentes são codificados?
    
??? success "Clique para revelar a