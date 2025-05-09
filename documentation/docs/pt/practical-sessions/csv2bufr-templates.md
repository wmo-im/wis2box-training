---
title: Modelos de mapeamento de CSV para BUFR
---

# Modelos de mapeamento de CSV para BUFR

!!! abstract "Resultados de aprendizado"
    Ao final desta sessão prática, você será capaz de:

    - criar um novo modelo de mapeamento BUFR para seus dados em CSV
    - editar e depurar seu modelo de mapeamento BUFR personalizado a partir da linha de comando
    - configurar o plugin de dados CSV para BUFR para usar um modelo de mapeamento BUFR personalizado
    - usar os modelos integrados AWS e DAYCLI para converter dados CSV em BUFR

## Introdução

Arquivos de dados em valores separados por vírgula (CSV) são frequentemente usados para registrar dados observacionais e outros em formato tabular.
A maioria dos registradores de dados usados para registrar saídas de sensores pode exportar as observações em arquivos delimitados, incluindo em CSV.
Da mesma forma, quando os dados são ingeridos em um banco de dados, é fácil exportar os dados necessários em arquivos formatados em CSV.

O módulo csv2bufr do wis2box fornece uma ferramenta de linha de comando para converter dados CSV para o formato BUFR. Ao usar csv2bufr, você precisa fornecer um modelo de mapeamento BUFR que mapeie colunas CSV para os elementos BUFR correspondentes. Se você não quiser criar seu próprio modelo de mapeamento, pode usar os modelos integrados AWS e DAYCLI para converter dados CSV em BUFR, mas você precisará garantir que os dados CSV que está usando estão no formato correto para esses modelos. Se você deseja decodificar parâmetros que não estão incluídos nos modelos AWS e DAYCLI, será necessário criar seu próprio modelo de mapeamento.

Nesta sessão, você aprenderá como criar seu próprio modelo de mapeamento para converter dados CSV em BUFR. Você também aprenderá como usar os modelos integrados AWS e DAYCLI para converter dados CSV em BUFR.

## Preparação

Certifique-se de que o wis2box-stack foi iniciado com `python3 wis2box.py start`

Certifique-se de que você tem um navegador web aberto com a UI do MinIO para sua instância acessando `http://YOUR-HOST:9000`
Se você não se lembra das suas credenciais do MinIO, pode encontrá-las no arquivo `wis2box.env` na pasta `wis2box` na sua VM de estudante.

Certifique-se de que você tem o MQTT Explorer aberto e conectado ao seu broker usando as credenciais `everyone/everyone`.

## Criando um modelo de mapeamento

O módulo csv2bufr vem com uma ferramenta de linha de comando para criar seu próprio modelo de mapeamento usando um conjunto de sequências BUFR e/ou elemento BUFR como entrada.

Para encontrar sequências e elementos BUFR específicos, você pode consultar as tabelas BUFR em [https://confluence.ecmwf.int/display/ECC/BUFR+tables](https://confluence.ecmwf.int/display/ECC/BUFR+tables).

### Ferramenta de linha de comando csv2bufr mappings

Para acessar a ferramenta de linha de comando csv2bufr, você precisa fazer login no contêiner wis2box-api:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
```

Para imprimir a página de ajuda para o comando `csv2bufr mapping`:

```bash
csv2bufr mappings --help
```

A página de ajuda mostra 2 subcomandos:

- `csv2bufr mappings create` : Criar um novo modelo de mapeamento
- `csv2bufr mappings list` : Listar os modelos de mapeamento disponíveis no sistema

!!! Note "csv2bufr mapping list"

    O comando `csv2bufr mapping list` mostrará os modelos de mapeamento disponíveis no sistema.
    Modelos padrão são armazenados no diretório `/opt/wis2box/csv2bufr/templates` no contêiner.

    Para compartilhar modelos de mapeamento personalizados com o sistema, você pode armazená-los no diretório definido por `$CSV2BUFR_TEMPLATES`, que é configurado para `/data/wis2box/mappings` por padrão no contêiner. Como o diretório `/data/wis2box/mappings` no contêiner é montado para o diretório `$WIS2BOX_HOST_DATADIR/mappings` no host, você encontrará seus modelos de mapeamento personalizados no diretório `$WIS2BOX_HOST_DATADIR/mappings` no host.

Vamos tentar criar um novo modelo de mapeamento personalizado usando o comando `csv2bufr mapping create` usando como entrada a sequência BUFR 301150 mais o elemento BUFR 012101.

```bash
csv2bufr mappings create 301150 012101 --output /data/wis2box/mappings/my_custom_template.json
```

Você pode verificar o conteúdo do modelo de mapeamento que acabou de criar usando o comando `cat`:

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "Inspeção do modelo de mapeamento"

    Quantas colunas CSV estão sendo mapeadas para elementos BUFR? Qual é o cabeçalho CSV para cada elemento BUFR mapeado?

??? success "Clique para revelar a resposta"
    
    O modelo de mapeamento que você criou mapeia **5** colunas CSV para elementos BUFR, nomeadamente os 4 elementos BUFR na sequência 301150 mais o elemento BUFR 012101. 

    As seguintes colunas CSV estão sendo mapeadas para elementos BUFR:

    - **wigosIdentifierSeries** mapeia para `"eccodes_key": "#1#wigosIdentifierSeries"` (elemento BUFR 001125)
    - **wigosIssuerOfIdentifier** mapeia para `"eccodes_key": "#1#wigosIssuerOfIdentifier` (elemento BUFR 001126)
    - **wigosIssueNumber** mapeia para `"eccodes_key": "#1#wigosIssueNumber"` (elemento BUFR 001127)
    - **wigosLocalIdentifierCharacter** mapeia para `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (elemento BUFR 001128)
    - **airTemperature** mapeia para `"eccodes_key": "#1#airTemperature"` (elemento BUFR 012101)

O modelo de mapeamento que você criou não inclui metadados importantes sobre a observação que foi feita, a data e hora da observação, e a latitude e longitude da estação.

Em seguida, atualizaremos o modelo de mapeamento e adicionaremos as seguintes sequências:
    
- **301011** para Data (Ano, mês, dia)
- **301012** para Hora (Hora, minuto)
- **301023** para Localização (Latitude/longitude (precisão grosseira))

E os seguintes elementos:

- **010004** para Pressão
- **007031** para Altura do barômetro acima do nível médio do mar

Execute o seguinte comando para atualizar o modelo de mapeamento:

```bash
csv2bufr mappings create 301150 301011 301012 301023 007031 012101 010004  --output /data/wis2box/mappings/my_custom_template.json
```

E inspecione o conteúdo do modelo de mapeamento novamente:

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "Inspeção do modelo de mapeamento atualizado"

    Quantas colunas CSV estão agora sendo mapeadas para elementos BUFR? Qual é o cabeçalho CSV para cada elemento BUFR mapeado?

??? success "Clique para revelar a resposta"
    
    O modelo de mapeamento que você criou agora mapeia **18** colunas CSV para elementos BUFR:
    - 4 elementos BUFR da sequência BUFR 301150
    - 3 elementos BUFR da sequência BUFR 301011
    - 2 elementos BUFR da sequência BUFR 301012
    - 2 elementos BUFR da sequência BUFR 301023
    - Elemento BUFR 007031
    - Elemento BUFR 012101

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

Observe que os cabeçalhos deste arquivo CSV são os mesmos que os cabeçalhos CSV no modelo de mapeamento que você criou.

Para testar a conversão de dados, podemos usar a ferramenta de linha de comando `csv2bufr` para converter o arquivo CSV para BUFR usando o modelo de mapeamento que criamos:

```bash
csv2bufr data transform --bufr-template my_custom_template /root/data-conversion-exercises/custom_template_data.csv
```

Você deve ver a seguinte saída:

```bash
CLI:    ... Transformando /root/data-conversion-exercises/custom_template_data.csv para BUFR ...
CLI:    ... Processando subconjuntos:
CLI:    ..... 94 bytes escritos para ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
CLI:    Fim do processamento, saindo.
```

!!! question "Verifique o conteúdo do arquivo BUFR"
    
    Como você pode verificar o conteúdo do arquivo BUFR que acabou de criar e verificar se ele codificou os dados corretamente?

??? success "Clique para revelar a resposta"

    Você pode usar o comando `bufr_dump -p` para verificar o conteúdo do arquivo BUFR que você acabou de criar.
    O comando mostrará o conteúdo do arquivo BUFR em um formato legível por humanos.

    ```bash
    bufr_dump -p ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
    ```

    Na saída, você verá valores para os elementos BUFR que você mapeou no modelo, por exemplo, a "airTemperature" mostrará:
    
    ```bash
    airTemperature=298.15
    ```

Você pode agora sair do contêiner:

```bash
exit
```

### Usando o modelo de mapeamento no wis2box

Para garantir que o novo modelo de mapeamento seja reconhecido pelo contêiner wis2box-api, você precisa reiniciar o contêiner:

```bash
docker restart wis2box-api
```

Você agora pode configurar seu conjunto de dados no wis2box-webapp para usar o modelo de mapeamento personalizado para o plugin de conversão de CSV para BUFR.

O wis2box-webapp detectará automaticamente o modelo de mapeamento que você criou e o disponibilizará na lista de modelos para o plugin de conversão de CSV para BUFR.

Clique no conjunto de dados que você criou na sessão prática anterior e clique em "ATUALIZAR" ao lado do plugin com o nome "Dados CSV convertidos para BUFR":

<img alt="Imagem mostrando o editor de conjunto de dados no wis2box-webapp" src="../../assets/img/wis2box-webapp-data-mapping-update-csv2bufr.png"/>

Você deve ver o novo modelo que você criou na lista de modelos disponíveis:

<img alt="Imagem mostrando os modelos csv2bufr no wis2box-webapp" src="../../assets/img/wis2box-webapp-csv2bufr-templates.png"/>

!!! hint

    Observe que, se você não vir o novo modelo que criou, tente atualizar a página ou abri-la em uma nova janela anônima.

Por enquanto, mantenha a seleção padrão do modelo AWS (clique no canto superior direito para fechar a configuração do plugin).

## Usando o modelo 'AWS'

O modelo 'AWS' fornece um modelo de mapeamento para converter dados CSV para a sequência BUFR 301150, 307096, em apoio aos requisitos mínimos do GBON.

A descrição do modelo AWS pode ser encontrada aqui [aws-template](./../csv2bufr-templates/aws-template.md).

### Revisão dos dados de entrada do exemplo aws

Baixe o exemplo para este exercício no link abaixo:

[aws-example.csv](./../../sample-data/aws-example.csv)

Abra o arquivo que você baixou em um editor e inspecione o conteúdo:

!!! question
    Examinando os campos de data, hora e identificação (identificadores WIGOS e tradicionais), o que você
    percebe? Como a data de hoje seria representada?

??? success "Clique para revelar a resposta"
    Cada coluna contém uma única peça de informação. Por exemplo, a data é dividida em
    ano, mês e dia, espelhando como os dados são armazenados em BUFR. A data de hoje seria 
    dividida nas colunas "ano", "mês" e "dia". Da mesma forma, o tempo precisa ser
    dividido em "hora" e "minuto" e o identificador da estação WIGOS em seus respectivos componentes.

!!! question
    Olhando para o arquivo de dados, como os dados ausentes são codificados?
    
??? success "Clique para revelar a resposta"
    Dados ausentes no arquivo são representados por células vazias. Em um arquivo CSV, isso seria
    codificado por ``,,``. Note que isso é uma célula vazia e não codificada como uma string de comprimento zero, 
    por exemplo, ``,"",``.

!!! hint "Dados ausentes"
    Reconhece-se que os dados podem estar ausentes por uma variedade de razões, seja devido a falha do sensor ou ao parâmetro não ser observado. Nestes casos, os dados ausentes podem ser codificados conforme a resposta acima, os outros dados no relatório permanecem válidos.

### Atualize o arquivo de exemplo

Atualize o arquivo de exemplo que você baixou para usar a data e hora de hoje e altere os identificadores da estação WIGOS para usar estações que você registrou no wis2box-webapp.

### Faça o upload dos dados para o MinIO e verifique o resultado

Navegue até a UI do MinIO e faça login usando as credenciais do arquivo `wis2box.env`.

Navegue até o **wis2box-incoming** e clique no botão "Criar novo caminho":

<img alt="Image showing MinIO UI with the create folder button highlighted" src="../../assets/img/minio-create-new-path.png"/>

Crie uma nova pasta no bucket do MinIO que corresponda ao dataset-id para o conjunto de dados que você criou com o template='weather/surface-weather-observations/synop':

<img alt="Image showing MinIO UI with the create folder button highlighted" src="../../assets/img/minio-create-new-path-metadata_id.png"/>

Faça o upload do arquivo de exemplo que você baixou para a pasta que você criou no bucket do MinIO:

<img alt="Image showing MinIO UI with aws-example uploaded" src="../../assets/img/minio-upload-aws-example.png"/>

Verifique o painel do Grafana em `http://YOUR-HOST:3000` para ver se há algum AVISO ou ERRO. Se você encontrar algum, tente corrigi-lo e repita o exercício.

Verifique o MQTT Explorer para ver se você recebe notificações de dados WIS2.

Se você tiver feito o ingest dos dados com sucesso, você deverá ver 3 notificações no MQTT Explorer no tópico `origin/a/wis2/<centre-id>/data/weather/surface-weather-observations/synop` para as 3 estações para as quais você relatou dados:

<img width="450" alt="Image showing MQTT explorer after uploading AWS" src="../../assets/img/mqtt-explorer-aws-upload.png"/>

## Usando o template 'DayCLI'

O template **DayCLI** fornece um template de mapeamento para converter dados diários de clima em CSV para a sequência BUFR 307075, em apoio ao relato de dados climáticos diários.

A descrição do template DAYCLI pode ser encontrada aqui [daycli-template](./../csv2bufr-templates/daycli-template.md).

Para compartilhar esses dados no WIS2, você precisará criar um novo conjunto de dados no wis2box-webapp que tenha a Hierarquia de Tópicos WIS2 correta e que use o template DAYCLI para converter dados CSV para BUFR.

### Criando um conjunto de dados wis2box para publicar mensagens DAYCLI

Vá para o editor de conjuntos de dados no wis2box-webapp e crie um novo conjunto de dados. Use o mesmo centre-id que nas sessões práticas anteriores e selecione **Data Type='climate/surface-based-observations/daily'**:

<img alt="Create a new dataset in the wis2box-webapp for DAYCLI" src="../../assets/img/wis2box-webapp-create-dataset-daycli.png"/>

Clique em "CONTINUAR PARA O FORMULÁRIO" e adicione uma descrição para seu conjunto de dados, defina a caixa delimitadora e forneça as informações de contato para o conjunto de dados. Uma vez que você tenha preenchido todas as seções, clique em 'VALIDAR FORMULÁRIO' e verifique o formulário.

Revise os plugins de dados para os conjuntos de dados. Clique em "ATUALIZAR" ao lado do plugin com o nome "Dados CSV convertidos para BUFR" e você verá que o template está definido para **DayCLI**:

<img alt="Update the data plugin for the dataset to use the DAYCLI template" src="../../assets/img/wis2box-webapp-update-data-plugin-daycli.png"/>

Feche a configuração do plugin e envie o formulário usando o token de autenticação que você criou na sessão prática anterior.

Você agora deve ter um segundo conjunto de dados no wis2box-webapp que está configurado para usar o template DAYCLI para converter dados CSV para BUFR.

### Revise os dados de entrada do exemplo daycli

Baixe o exemplo para este exercício no link abaixo:

[daycli-example.csv](./../../sample-data/daycli-example.csv)

Abra o arquivo que você baixou em um editor e inspecione o conteúdo:

!!! question
    Quais variáveis adicionais estão incluídas no template daycli?

??? success "Clique para revelar a resposta"
    O template daycli inclui metadados importantes sobre a localização do instrumento e classificações de qualidade da medição para temperatura e umidade, flags de controle de qualidade e informações sobre como a temperatura média diária foi calculada.

### Atualize o arquivo de exemplo

O arquivo de exemplo contém uma linha de dados para cada dia em um mês e relata dados para uma estação. Atualize o arquivo de exemplo que você baixou para usar a data e hora de hoje e altere os identificadores da estação WIGOS para usar uma estação que você registrou no wis2box-webapp.

### Faça o upload dos dados para o MinIO e verifique o resultado

Como antes, você precisará fazer o upload dos dados para o bucket 'wis2box-incoming' no MinIO para serem processados pelo conversor csv2bufr. Desta vez, você precisará criar uma nova pasta no bucket do MinIO que corresponda ao dataset-id para o conjunto de dados que você criou com o template='climate/surface-based-observations/daily', que será diferente do dataset-id que você usou no exercício anterior:

<img alt="Image showing MinIO UI with DAYCLI-example uploaded" src="../../assets/img/minio-upload-daycli-example.png"/>

Após fazer o upload dos dados, verifique se não há AVISOS ou ERROS no painel do Grafana e verifique o MQTT Explorer para ver se você recebe notificações de dados WIS2.

Se você tiver feito o ingest dos dados com sucesso, você deverá ver 30 notificações no MQTT Explorer no tópico `origin/a/wis2/<centre-id>/data/climate/surface-based-observations/daily` para os 30 dias do mês para os quais você relatou dados:

<img width="450" alt="Image showing MQTT explorer after uploading DAYCLI" src="../../assets/img/mqtt-daycli-template-success.png"/>

## Conclusão

!!! success "Parabéns"
    Nesta sessão prática, você aprendeu:

    - como criar um template de mapeamento personalizado para converter dados CSV para BUFR
    - como usar os templates integrados AWS e DAYCLI para converter dados CSV para BUFR