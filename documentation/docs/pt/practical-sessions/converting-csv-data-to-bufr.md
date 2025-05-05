---
title: Convertendo dados CSV para BUFR
---

# Convertendo dados CSV para BUFR

!!! abstract "Resultados de aprendizagem"
    Ao final desta sessão prática, você será capaz de:

    - usar a **MinIO UI** para fazer upload de arquivos de dados CSV de entrada e monitorar o resultado
    - conhecer o formato dos dados CSV para uso com o modelo padrão automático de estação meteorológica BUFR
    - usar o editor de conjuntos de dados no **wis2box webapp** para criar um conjunto de dados para publicar mensagens DAYCLI
    - conhecer o formato dos dados CSV para uso com o modelo DAYCLI BUFR
    - usar **wis2box webapp** para validar e converter dados de amostra para estações AWS para BUFR (opcional)

## Introdução

Arquivos de dados em valores separados por vírgulas (CSV) são frequentemente usados para registrar observações e outros dados em um formato tabular.
A maioria dos registradores de dados usados para gravar saídas de sensores é capaz de exportar as observações em arquivos delimitados, incluindo em CSV.
Da mesma forma, quando os dados são inseridos em um banco de dados, é fácil exportar os dados necessários em arquivos formatados em CSV.
Para auxiliar na troca de dados originalmente armazenados em formatos de dados tabulares, um conversor de CSV para BUFR foi implementado no
wis2box usando o mesmo software que para SYNOP para BUFR.

Nesta sessão, você aprenderá sobre o uso do conversor csv2bufr no wis2box para os seguintes modelos integrados:

- **AWS** (aws-template.json) : Modelo de mapeamento para converter dados CSV de arquivo de estação meteorológica automática simplificada para sequência BUFR 301150, 307096
- **DayCLI** (daycli-template.json) : Modelo de mapeamento para converter dados CSV climáticos diários para sequência BUFR 307075

## Preparação

Certifique-se de que o wis2box-stack foi iniciado com `python3 wis2box.py start`

Certifique-se de que você tem um navegador web aberto com a MinIO UI para sua instância acessando `http://<seu-host>:9000`
Se você não se lembrar de suas credenciais MinIO, você pode encontrá-las no arquivo `wis2box.env` na pasta `wis2box-1.0.0rc1` no seu VM de estudante.

Certifique-se de que você tem o MQTT Explorer aberto e conectado ao seu corretor usando as credenciais `everyone/everyone`.

## Exercício 1: Usando csv2bufr com o modelo 'AWS'

O modelo 'AWS' fornece um modelo de mapeamento predefinido para converter dados CSV de estações AWS em apoio aos requisitos de relatório do GBON.

A descrição do modelo AWS pode ser encontrada [aqui](/csv2bufr-templates/aws-template).

### Revisar os dados de entrada do exemplo aws

Baixe o exemplo para este exercício no link abaixo:

[aws-example.csv](/sample-data/aws-example.csv)

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
    codificado por ``,,``. Observe que esta é uma célula vazia e não codificada como uma string de comprimento zero, 
    por exemplo, ``,"",``.

!!! hint "Dados ausentes"
    Reconhece-se que os dados podem estar ausentes por uma variedade de razões, seja devido a falha do sensor 
    ou o parâmetro não ser observado. Nestes casos, os dados ausentes podem ser codificados
    conforme a resposta acima, os outros dados no relatório permanecem válidos.

!!! question
    Quais são os identificadores da estação WIGOS para as estações que reportam dados no arquivo de exemplo? Como ele é definido no arquivo de entrada?

??? success "Clique para revelar a resposta"

    O identificador da estação WIGOS é definido por 4 colunas separadas no arquivo:

    - **wsi_series**: série do identificador WIGOS
    - **wsi_issuer**: emissor do identificador WIGOS
    - **wsi_issue_number**: número da emissão WIGOS
    - **wsi_local**: identificador local WIGOS

    Os identificadores das estações WIGOS usados no arquivo de exemplo são `0-20000-0-60351`, `0-20000-0-60355` e `0-20000-0-60360`.	

### Atualizar o arquivo de exemplo

Atualize o arquivo de exemplo que você baixou para usar a data e hora de hoje e altere os identificadores das estações WIGOS para usar estações que você registrou no wis2box-webapp.

### Fazer upload dos dados para MinIO e verificar o resultado

Navegue até a MinIO UI e faça login usando as credenciais do arquivo `wis2box.env`.

Navegue até o **wis2box-incoming** e clique no botão "Criar novo caminho":

<img alt="Imagem mostrando a MinIO UI com o botão de criar pasta destacado" src="../../assets/img/minio-create-new-path.png"/>

Crie uma nova pasta no bucket MinIO que corresponda ao dataset-id para o conjunto de dados que você criou com o template='weather/surface-weather-observations/synop':

<img alt="Imagem mostrando a MinIO UI com o botão de criar pasta destacado" src="../../assets/img/minio-create-new-path-metadata_id.png"/>

Faça o upload do arquivo de exemplo que você baixou para a pasta que você criou no bucket MinIO:

<img alt="Imagem mostrando a MinIO UI com aws-example carregado" src="../../assets/img/minio-upload-aws-example.png"/></center>

Verifique o painel do Grafana em `http://<seu-host>:3000` para ver se há algum AVISO ou ERRO. Se você vir algum, tente corrigi-los e repita o exercício.

Verifique o MQTT Explorer para ver se você recebe notificações de dados WIS2.

Se você tiver feito o ingestão dos dados com sucesso, você deverá ver 3 notificações no MQTT explorer no tópico `origin/a/wis2/<centre-id>/data/weather/surface-weather-observations/synop` para as 3 estações para as quais você relatou dados:

<img width="450" alt="Imagem mostrando MQTT explorer após o upload de AWS" src="../../assets/img/mqtt-explorer-aws-upload.png"/>

## Exercício 2 - Usando o modelo 'DayCLI'

No exercício anterior, usamos o conjunto de dados que você criou com Data-type='weather/surface-weather-observations/synop', que tem predefinido o modelo de conversão de CSV para BUFR para o modelo AWS.

No próximo exercício, usaremos o modelo 'DayCLI' para converter dados climáticos diários para BUFR.

A descrição do modelo DAYCLI pode ser encontrada [aqui](/csv2bufr-templates/daycli-template).

!!! Note "Sobre o modelo DAYCLI"
    Observe que a sequência BUFR DAYCLI será atualizada durante 2025 para incluir informações adicionais e bandeiras de QC revisadas. O modelo DAYCLI incluído no wis2box será atualizado para refletir essas mudanças. A OMM comunicará quando o software wis2box for atualizado para incluir o novo modelo DAYCLI, para permitir que os usuários atualizem seus sistemas de acordo.

### Criando um conjunto de dados wis2box para publicar mensagens DAYCLI

Vá para o editor de conjuntos de dados no wis2box-webapp e crie um novo conjunto de dados. Use o mesmo centre-id que nas sessões práticas anteriores e selecione **Data Type='climate/surface-based-observations/daily'**:

<img alt="Criar um novo conjunto de dados no wis2box-webapp para DAYCLI" src="../../assets/img/wis2box-webapp-create-dataset-daycli.png"/>

Clique em "CONTINUAR PARA O FORMULÁRIO" e adicione uma descrição para o seu conjunto de dados, defina a caixa delimitadora e forneça as informações de contato para o conjunto de dados. Uma vez que você terminar de preencher todas as seções, clique em 'VALIDAR FORMULÁRIO' e verifique o formulário.

Revise os plugins de dados para os conjuntos de dados. Clique em "ATUALIZAR" ao lado do plugin com o nome "Dados CSV convertidos para BUFR" e você verá que o modelo está definido para **DayCLI**:

<img alt="Atualizar o plugin de dados para o conjunto de dados para usar o modelo DAYCLI" src="../../assets/img/wis2box-webapp-update-data-plugin-daycli.png"/>

Feche a configuração do plugin e envie o formulário usando o token de autenticação que você criou na sessão prática anterior.

Você agora deve ter um segundo conjunto de dados no wis2box-webapp que está configurado para usar o modelo DAYCLI para converter dados CSV para BUFR.

### Revisar os dados de entrada do exemplo daycli

Baixe o exemplo para este exercício no link abaixo:

[daycli-example.csv](/sample-data/daycli-example.csv)

Abra o arquivo que você baixou em um editor e inspecione o conteúdo:

!!! question
    Quais variáveis adicionais estão incluídas no modelo daycli?

??? success "Clique para revelar a resposta"
    O modelo daycli inclui metadados importantes sobre o posicionamento do instrumento e classificações de qualidade da medição para temperatura e umidade, bandeiras de controle de qualidade e informações sobre como a temperatura média diária foi calculada.

### Atualizar o arquivo de exemplo

O arquivo de exemplo contém uma linha de dados para cada dia de um mês e relata dados para uma estação. Atualize o arquivo de exemplo que você baixou para usar a data e hora de hoje e altere os identificadores das estações WIGOS para usar uma estação que você registrou no wis2box-webapp.

### Fazer upload dos dados para MinIO e verificar o resultado

Como antes, você precisará fazer o upload dos dados para o bucket 'wis2box-incoming' no MinIO para ser processado pelo conversor csv2bufr. Desta vez, você precisará criar uma nova pasta no bucket MinIO que corresponda ao dataset-id para o conjunto de dados que você criou com o template='climate/surface-based-observations/daily', que será diferente do dataset-id que você usou no exercício anterior:

<img alt="Imagem mostrando a MinIO UI com DAYCLI-example carregado" src="../../assets/img/minio-upload-daycli-example.png"/></center>

Após fazer o upload dos dados, verifique se não há AVISOS ou ERROS no painel do Grafana e verifique o MQTT Explorer para ver se você recebe notificações de dados WIS2.

Se você tiver feito o ingestão dos dados com sucesso, você deverá ver 30 notificações no MQTT explorer no tópico `origin/a/wis2/<centre-id>/data/climate/surface-based-observations/daily` para os 30 dias do mês para os quais você relatou dados:

<img width="450" alt="Imagem mostrando MQTT explorer após o upload de DAYCLI" src="../../assets/img/mqtt-daycli-template-success.png"/>

## Exercício 3 - usando o formulário CSV no wis2box-webapp (opcional)

O aplicativo web wis2box fornece uma interface para fazer upload de dados CSV e convertê-los para BUFR antes de publicá-los no WIS2, usando o modelo AWS.

O uso deste formulário é destinado a fins de depuração e validação, o método de envio recomendado para publicar dados de Estações Meteorológicas Automatizadas é configurar um processo que faça o upload automático dos dados para o bucket MinIO.

### Usando o Formulário CSV no aplicativo web wis2box

Navegue até o Formulário CSV no aplicativo web wis2box
(``http://<seu-nome-de-host>/wis2box-webapp/csv2bufr_form``).
Use o arquivo [aws-example.csv](/sample-data/aws-example.csv) para este exercício.
Você agora deve ser capaz de clicar em próximo para visualizar e validar o arquivo.

<center><img alt="Imagem mostrando a tela de upload de CSV para BUFR" src="../../assets/img/csv2bufr-ex1.png"/></center>

Clicar no botão próximo carrega o arquivo no navegador e valida o conteúdo contra um esquema predefinido.
Ainda não foram convertidos ou publicados dados. Na aba de visualização/validação, você deve ser apresentado com uma lista de avisos
sobre dados ausentes, mas neste exercício, esses podem ser ignorados.

<center><img alt="Imagem mostrando a página de validação de exemplo de CSV para BUFR com avisos" src="../../assets/img/csv2bufr-warnings.png"/></center>

Clique em *próximo* para prosseguir e você será solicitado a fornecer um dataset-id para os dados a serem publicados. Selecione o dataset-id que você criou anteriormente e clique em *próximo*.

Você agora deve estar em uma página de autorização onde será solicitado a inserir o token ``processes/wis2box``
que você criou anteriormente. Insira este token e clique no botão "Publicar no WIS2" para garantir
que "Publicar para WIS2" esteja selecionado (veja a captura de tela abaixo).

<center><img alt="tela de autenticação e publicação csv2bufr" src="../../assets/img/csv2bufr-toggle-publish.png"/></center>

Clique em próximo para transformar em BUFR e publicar, você então deverá ver a seguinte tela:

<center><img alt="Imagem mostrando a tela de sucesso de exemplo de CSV para BUFR" src="../../assets/img/csv2bufr-success.png"/></center>

Clicar na seta para baixo à direita de ``Arquivos BUFR de saída`` deve revelar os botões ``Download`` e ``Inspecionar``.
Clique em inspecionar para visualizar os dados e confirmar que os valores estão conforme o esperado.

<center><img alt="Imagem mostrando a inspeção de saída de CSV para BUFR" src="../../assets/img/csv2bufr-inspect.png"/></center>

### Depurando dados de entrada inválidos

Neste exercício, examinaremos o que acontece com dados de entrada inválidos. Baixe o próximo arquivo de exemplo clicando no
link abaixo. Este contém os mesmos dados que o primeiro arquivo, mas com as colunas vazias removidas.
Examine o arquivo e confirme quais colunas foram removidas e, em seguida, siga o mesmo processo para converter os dados para BUFR.

[csv2bufr-ex3a.csv](/sample-data/csv2bufr-ex3a.csv)

!!! question
    Com as colunas ausentes do arquivo, você conseguiu converter os dados para BUFR?
    Você notou alguma mudança nos avisos na página de validação?

??? success "Clique para revelar a resposta"
    Você ainda deveria ter sido capaz de converter os dados para BUFR, mas as mensagens de aviso teriam sido atualizadas
    para indicar que as colunas estavam completamente ausentes, em vez de conter um valor ausente.

No próximo exemplo, uma coluna adicional foi adicionada ao arquivo CSV.

[csv2bufr-ex3b.csv](/sample-data/csv2bufr-ex3b.csv)

!!! question
    Sem fazer o upload ou enviar o arquivo, você pode prever o que acontecerá quando fizer?

Agora faça o upload e confirme se sua previsão estava correta.

??? success "Clique para revelar a resposta"
    Quando o arquivo for validado, você agora receberá um aviso de que a coluna ``index``
    não é encontrada no esquema e que os dados serão ignorados. Você deve ser capaz de clicar
    através e converter para BUFR como no exemplo anterior.

No exemplo final deste exercício, os dados foram modificados. Examine o conteúdo do arquivo CSV.

[csv2bufr-ex3c.csv](/sample-data/csv2bufr-ex3c.csv)

!!! question
    O que mudou no arquivo e o que você acha que acontecerá?

Agora faça o upload do arquivo e confirme se você estava correto.

??? warning "Clique para revelar a resposta"
    Os campos de pressão foram convertidos de Pa para hPa nos dados de entrada. No entanto, o conversor de CSV para BUFR
    espera as mesmas unidades que BUFR (Pa) e, como resultado, esses campos falham na validação por estarem
    fora do intervalo. Você deve ser capaz de editar o CSV para corrigir o problema e reenviar os dados retornando
    à primeira tela e fazendo o upload novamente.

!!! hint
    O aplicativo web wis2box