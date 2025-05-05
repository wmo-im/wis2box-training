---
title: Automatizando a ingestão de dados
---

# Automatizando a ingestão de dados

!!! abstract "Resultados de aprendizado"

    Ao final desta sessão prática, você será capaz de:
    
    - entender como os plugins de dados do seu conjunto de dados determinam o fluxo de trabalho de ingestão de dados
    - inserir dados no wis2box usando um script com o cliente Python MinIO
    - inserir dados no wis2box acessando o MinIO via SFTP

## Introdução

O contêiner **wis2box-management** escuta eventos do serviço de armazenamento MinIO para disparar a ingestão de dados baseada nos plugins de dados configurados para o seu conjunto de dados. Isso permite que você faça upload de dados no bucket do MinIO e acione o fluxo de trabalho do wis2box para publicar dados no corretor WIS2.

Os plugins de dados definem os módulos Python que são carregados pelo contêiner **wis2box-management** e determinam como os dados são transformados e publicados.

No exercício anterior, você deveria ter criado um conjunto de dados usando o modelo `surface-based-observations/synop` que incluía os seguintes plugins de dados:

<img alt="mapeamentos de dados" src="../../assets/img/wis2box-data-mappings.png" width="800">

Quando um arquivo é carregado no MinIO, o wis2box corresponderá o arquivo a um conjunto de dados quando o caminho do arquivo contiver o id do conjunto de dados (`metadata_id`) e determinará os plugins de dados a serem usados com base na extensão do arquivo e no padrão de arquivo definido nos mapeamentos do conjunto de dados.

Nas sessões anteriores, acionamos o fluxo de trabalho de ingestão de dados usando a funcionalidade de linha de comando do wis2box, que faz upload de dados para o armazenamento MinIO no caminho correto.

Os mesmos passos podem ser feitos programaticamente usando qualquer software cliente MinIO ou S3, permitindo que você automatize sua ingestão de dados como parte de seus fluxos de trabalho operacionais.

Alternativamente, você também pode acessar o MinIO usando o protocolo SFTP para fazer upload de dados e acionar o fluxo de trabalho de ingestão de dados.

## Preparação

Faça login na sua VM de estudante usando seu cliente SSH (PuTTY ou outro).

Certifique-se de que o wis2box está funcionando:

```bash
cd ~/wis2box-1.0.0rc1/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Certifique-se de que o MQTT Explorer está em execução e conectado à sua instância. Se você ainda estiver conectado da sessão anterior, limpe quaisquer mensagens anteriores que você possa ter recebido da fila.
Isso pode ser feito desconectando e reconectando ou clicando no ícone da lixeira para o tópico dado.

Certifique-se de que você tem um navegador web aberto com o painel do Grafana para sua instância acessando `http://<seu-host>:3000`

E certifique-se de que você tem uma segunda aba aberta com a interface do usuário do MinIO em `http://<seu-host>:9001`. Lembre-se de que você precisa fazer login com o `WIS2BOX_STORAGE_USER` e `WIS2BOX_STORAGE_PASSWORD` definidos no seu arquivo `wis2box.env`.

## Exercício 1: configurar um script Python para inserir dados no MinIO

Neste exercício, usaremos o cliente Python MinIO para copiar dados para o MinIO.

O MinIO fornece um cliente Python que pode ser instalado da seguinte forma:

```bash
pip3 install minio
```

Na sua VM de estudante, o pacote 'minio' para Python já estará instalado.

Vá para o diretório `exercise-materials/data-ingest-exercises`; este diretório contém um script de exemplo `copy_file_to_incoming.py` que usa o cliente Python MinIO para copiar um arquivo para o MinIO.

Tente executar o script para copiar o arquivo de dados de exemplo `csv-aws-example.csv` para o bucket `wis2box-incoming` no MinIO da seguinte forma:

```bash
cd ~/exercise-materials/data-ingest-exercises
python3 copy_file_to_incoming.py csv-aws-example.csv
```

!!! note

    Você receberá um erro, pois o script ainda não está configurado para acessar o endpoint MinIO no seu wis2box.

O script precisa conhecer o endpoint correto para acessar o MinIO no seu wis2box. Se o wis2box estiver rodando no seu host, o endpoint do MinIO estará disponível em `http://<seu-host>:9000`. O script também precisa ser atualizado com sua senha de armazenamento e o caminho no bucket do MinIO para armazenar os dados.

!!! question "Atualize o script e ingira os dados CSV"
    
    Edite o script `copy_file_to_incoming.py` para corrigir os erros, usando um dos seguintes métodos:
    - Da linha de comando: use o editor de texto `nano` ou `vim` para editar o script
    - Usando o WinSCP: inicie uma nova conexão usando o Protocolo de Arquivo `SCP` e as mesmas credenciais que seu cliente SSH. Navegue até o diretório `exercise-materials/data-ingest-exercises` e edite `copy_file_to_incoming.py` usando o editor de texto integrado
    
    Certifique-se de que você:

    - defina o endpoint MinIO correto para o seu host
    - forneça a senha de armazenamento correta para sua instância MinIO
    - forneça o caminho correto no bucket MinIO para armazenar os dados

    Re-execute o script para inserir o arquivo de dados de exemplo `csv-aws-example.csv` no MinIO:

    ```bash
    python3 copy_file_to_incoming.py csv-aws-example.csv
    ```

    E certifique-se de que os erros foram resolvidos.

Você pode verificar se os dados foram carregados corretamente verificando a interface do usuário do MinIO e vendo se os dados de exemplo estão disponíveis no diretório correto no bucket `wis2box-incoming`.

Você pode usar o painel do Grafana para verificar o status do fluxo de trabalho de ingestão de dados.

Finalmente, você pode usar o MQTT Explorer para verificar se as notificações foram publicadas para os dados que você inseriu. Você deve ver que os dados CSV foram transformados para o formato BUFR e que uma notificação de dados WIS2 foi publicada com uma URL "canônica" para permitir o download dos dados BUFR.

## Exercício 2: Ingestão de dados binários

A seguir, tentaremos inserir dados binários no formato BUFR usando o cliente Python MinIO.

O wis2box pode inserir dados binários no formato BUFR usando o plugin `wis2box.data.bufr4.ObservationDataBUFR` incluído no wis2box.

Este plugin dividirá o arquivo BUFR em mensagens BUFR individuais e publicará cada mensagem no corretor MQTT. Se a estação para a mensagem BUFR correspondente não estiver definida nos metadados da estação wis2box, a mensagem não será publicada.

Como você usou o modelo `surface-based-observations/synop` na sessão anterior, seus mapeamentos de dados incluem o plugin `FM-12 data converted to BUFR` para os mapeamentos do conjunto de dados. Este plugin carrega o módulo `wis2box.data.synop2bufr.ObservationDataSYNOP2BUFR` para inserir os dados.

!!! question "Ingestão de dados binários no formato BUFR"

    Execute o seguinte comando para copiar o arquivo de dados binários `bufr-example.bin` para o bucket `wis2box-incoming` no MinIO:

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

Verifique o painel do Grafana e o MQTT Explorer para ver se os dados de teste foram inseridos e publicados com sucesso e, se você vir algum erro, tente resolvê-los.

!!! question "Verifique a ingestão de dados"

    Quantas mensagens foram publicadas no corretor MQTT para esta amostra de dados?

??? success "Clique para revelar a resposta"

    Se você inseriu e publicou com sucesso a última amostra de dados, você deve ter recebido 10 novas notificações no corretor MQTT wis2box. Cada notificação corresponde a dados para uma estação para um carimbo de data/hora de observação.

    O plugin `wis2box.data.bufr4.ObservationDataBUFR` divide o arquivo BUFR em mensagens BUFR individuais e publica uma mensagem para cada estação e carimbo de data/hora de observação.

## Exercício 3: Ingestão de dados SYNOP no formato ASCII

Na sessão anterior, usamos o formulário SYNOP no **wis2box-webapp** para inserir dados SYNOP no formato ASCII. Você também pode inserir dados SYNOP no formato ASCII fazendo upload dos dados no MinIO.

Na sessão anterior, você deveria ter criado um conjunto de dados que incluía o plugin 'FM-12 data converted to BUFR' para os mapeamentos do conjunto de dados:

<img alt="mapeamentos de conjunto de dados" src="../../assets/img/wis2box-data-mappings.png" width="800">

Este plugin carrega o módulo `wis2box.data.synop2bufr.ObservationDataSYNOP2BUFR` para inserir os dados.

Tente usar o cliente Python MinIO para inserir os dados de teste `synop-202307.txt` e `synop-202308.txt` na sua instância wis2box.

Observe que os 2 arquivos contêm o mesmo conteúdo, mas o nome do arquivo é diferente. O nome do arquivo é usado para determinar a data da amostra de dados.

O plugin synop2bufr depende de um padrão de arquivo para extrair a data do nome do arquivo. O primeiro grupo na expressão regular é usado para extrair o ano e o segundo grupo é usado para extrair o mês.

!!! question "Ingestão de dados SYNOP FM-12 no formato ASCII"

    Volte à interface MinIO no seu navegador e navegue até o bucket `wis2box-incoming` e até o caminho onde você fez o upload dos dados de teste no exercício anterior.
    
    Faça o upload dos novos arquivos no caminho correto no bucket `wis2box-incoming` no MinIO para acionar o fluxo de trabalho de ingestão de dados.

    Verifique o painel do Grafana e o MQTT Explorer para ver se os dados de teste foram inseridos e publicados com sucesso.

    Qual é a diferença no `properties.datetime` entre as duas mensagens publicadas no corretor MQTT?

??? success "Clique para revelar a resposta"

    Verifique as propriedades das últimas 2 notificações no MQTT Explorer e você notará que uma notificação tem:

    ```{.copy}
    "properties": {
        "data_id": "wis2/urn:wmo:md:nl-knmi-test:surface-based-observations.synop/WIGOS_0-20000-0-60355_20230703T090000",
        "datetime": "2023-07-03T09:00:00Z",
        ...
    ```

    e a outra notificação tem:

    ```{.copy}
    "properties": {
        "data_id": "wis2/urn:wmo:md:nl-knmi-test:surface-based-observations.synop/WIGOS_0-20000-0-60355_20230803T09:00:00Z",
        "datetime": "2023-08-03T09:00:00Z",
        ...
    ```

    O nome do arquivo foi usado para determinar o ano e o mês da amostra de dados.

## Exercício 4: Ingestão de dados no MinIO usando SFTP

Dados também podem ser inseridos no MinIO via SFTP.

O serviço MinIO habilitado na pilha wis2box tem SFTP habilitado na porta 8022. Você pode acessar o MinIO via SFTP usando as mesmas credenciais da interface do usuário do MinIO. Neste exercício, usaremos as credenciais de administrador para o serviço MinIO conforme definido em `wis2box.env`, mas você também pode criar usuários adicionais na interface do usuário do MinIO.

Para acessar o MinIO via SFTP, você pode usar qualquer software cliente SFTP. Neste exercício, usaremos o WinSCP, que é um cliente SFTP gratuito para Windows.

Usando o WinSCP, sua conexão seria assim:

<img alt="conexão sftp-winscp" src="../../assets/img/winscp-sftp-connection.png" width="400">

Para nome de usuário e senha, use os valores das variáveis de ambiente `WIS2BOX_STORAGE_USERNAME` e `WIS2BOX_STORAGE_PASSWORD` do seu arquivo `wis2box.env`. Clique em 'salvar' para salvar a sessão e depois em 'login' para conectar.

Quando você fizer login, você verá o bucket MinIO `wis2box-incoming` e `wis2box-public` no diretório raiz. Você pode fazer upload de dados para o bucket `wis2box-incoming` para acionar o fluxo de trabalho de ingestão de dados.

Clique no bucket `wis2box-incoming` para navegar até este bucket, clique com o botão direito e selecione *Novo*->*Diretório* para criar um novo diretório no bucket `wis2box-incoming`.

Crie o diretório *not-a-valid-path* e faça o upload do arquivo *randomfile.txt* neste diretório (você pode usar qualquer arquivo que desejar).

Verifique o painel do Grafana na porta 3000 para ver se o fluxo de trabalho de ingestão de dados foi acionado. Você deve ver:

*ERRO - Erro de validação de caminho: Não foi possível corresponder http://minio:9000/wis2box-incoming/not-a-valid-path/randomfile.txt ao conjunto de dados, o caminho deve incluir um dos seguintes: ...*

O erro indica que o arquivo foi carregado no MinIO e o fluxo de trabalho de ingestão de dados foi acionado, mas como o caminho não corresponde a nenhum conjunto de dados na instância wis2box, o mapeamento de dados falhou.

Você também pode usar `sftp` a partir da linha de comando:

```bash
sftp -P 8022 -oBatchMode=no -o StrictHostKeyChecking=no <meu-nome-de-host-ou-ip>
```
Faça login usando as credenciais definidas em `wis2box.env` para as variáveis de ambiente `WIS2BOX_STORAGE_USERNAME` e `WIS2BOX_STORAGE_PASSWORD`, navegue até o bucket `wis2box-incoming` e então crie um diretório e faça upload de um arquivo da seguinte forma:

```bash
cd wis2box-incoming
mkdir not-a-valid-path
cd not-a-valid-path
put ~/exercise-materials/data-ingest-exercises/synop.txt .
```

Isso resultará em um "Erro de validação de caminho" no painel do Grafana, indicando que o arquivo foi carregado no MinIO.

Para sair do cliente sftp, digite `exit`. 

!!! Question "Inserir dados no MinIO usando SFTP"

    Tente inserir o arquivo `synop.txt` na sua instância wis2box usando SFTP para acionar o fluxo de trabalho de ingestão de dados.

    Verifique a interface do usuário do MinIO para ver se o arquivo foi carregado no caminho correto no bucket `wis2box-incoming`.
    
    Verifique o painel do Grafana para ver se o fluxo de trabalho de ingestão de dados foi acionado ou se houve algum erro.

 Para garantir que seus dados sejam inseridos corretamente, certifique-se de que o arquivo seja carregado no bucket `wis2box-incoming` em um diretório que corresponda ao id do conjunto de dados ou ao tópico do seu conjunto de dados.

## Conclusão

!!! success "Parabéns!"
    Nesta sessão prática, você aprendeu a:

    - acionar o fluxo de trabalho do wis2box usando um script Python e o cliente Python MinIO
    - usar diferentes plugins de dados para inserir diferentes formatos de dados
    - fazer upload de dados no MinIO usando SFTP