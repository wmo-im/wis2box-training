---
title: Monitoramento de Notificações WIS2
---

# Monitoramento de Notificações WIS2

!!! abstract "Resultados de aprendizagem"

    Ao final desta sessão prática, você será capaz de:
    
    - acionar o fluxo de trabalho do wis2box ao fazer upload de dados no MinIO usando o comando `wis2box data ingest`
    - visualizar avisos e erros exibidos no painel do Grafana
    - verificar o conteúdo dos dados que estão sendo publicados

## Introdução

O **painel do Grafana** utiliza dados do Prometheus e do Loki para exibir o status do seu wis2box. O Prometheus armazena dados de séries temporais das métricas coletadas, enquanto o Loki armazena os logs dos contêineres em execução na sua instância do wis2box. Esses dados permitem que você verifique quanto dados são recebidos no MinIO e quantas notificações WIS2 são publicadas, e se há erros detectados nos logs.

Para ver o conteúdo das notificações WIS2 que estão sendo publicadas em diferentes tópicos do seu wis2box, você pode usar a aba 'Monitorar' no **wis2box-webapp**.

## Preparação

Esta seção utilizará o conjunto de dados "surface-based-observations/synop" criado anteriormente na sessão prática [Configurando conjuntos de dados no wis2box](/practical-sessions/configuring-wis2box-datasets).

Faça login na sua VM de estudante usando seu cliente SSH (PuTTY ou outro).

Certifique-se de que o wis2box está funcionando:

```bash
cd ~/wis2box-1.0.0rc1/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Certifique-se de que você tem o MQTT Explorer em execução e conectado à sua instância usando as credenciais públicas `everyone/everyone` com uma assinatura no tópico `origin/a/wis2/#`.

Certifique-se de que você tem acesso à interface web do MinIO indo para `http://<seu-host>:9000` e que você está logado (usando `WIS2BOX_STORAGE_USERNAME` e `WIS2BOX_STORAGE_PASSWORD` do seu arquivo `wis2box.env`).

Certifique-se de que você tem um navegador aberto com o painel do Grafana para sua instância indo para `http://<seu-host>:3000`.

## Ingestão de alguns dados

Por favor, execute os seguintes comandos a partir da sua sessão de cliente SSH:

Copie o arquivo de dados de exemplo `aws-example.csv` para o diretório que você definiu como `WI2BOX_HOST_DATADIR` no seu arquivo `wis2box.env`.

```bash
cp ~/exercise-materials/monitoring-exercises/aws-example.csv ~/wis2box-data/
```

Certifique-se de que você está no diretório `wis2box-1.0.0rc1` e faça login no contêiner **wis2box-management**:

```bash
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login
```

Verifique se os dados de exemplo estão disponíveis no diretório `/data/wis2box/` dentro do contêiner **wis2box-management**:

```bash
ls -lh /data/wis2box/aws-example.csv
```

!!! note
    O `WIS2BOX_HOST_DATADIR` é montado como `/data/wis2box/` dentro do contêiner de gerenciamento do wis2box pelo arquivo `docker-compose.yml` incluído no diretório `wis2box-1.0.0rc1`.
    
    Isso permite que você compartilhe dados entre o host e o contêiner.

!!! question "Exercício 1: ingestão de dados usando `wis2box data ingest`"

    Execute o seguinte comando para ingerir o arquivo de dados de exemplo `aws-example.csv` na sua instância do wis2box:

    ```bash
    wis2box data ingest -p /data/wis2box/aws-example.csv --metadata-id urn:wmo:md:not-my-centre:core.surface-based-observations.synop
    ```

    Os dados foram ingeridos com sucesso? Se não, qual foi a mensagem de erro e como você pode corrigi-la?

??? success "Clique para revelar a resposta"

    Você verá a seguinte saída:

    ```bash
    Error: metadata_id=urn:wmo:md:not-my-centre:core.surface-based-observations.synop not found in data mappings
    ```

    A mensagem de erro indica que o identificador de metadados que você forneceu não corresponde a nenhum dos conjuntos de dados que você configurou na sua instância do wis2box.

    Forneça o metadata-id correto que corresponde ao conjunto de dados que você criou na sessão prática anterior e repita o comando de ingestão de dados até que você veja a seguinte saída:

    ```bash 
    Processing /data/wis2box/aws-example.csv
    Done
    ```

Vá para o console do MinIO no seu navegador e verifique se o arquivo `aws-example.csv` foi carregado no bucket `wis2box-incoming`. Você deve ver que há um novo diretório com o nome do conjunto de dados que você forneceu na opção `--metadata-id`:

<img alt="minio-wis2box-incoming-dataset-folder" src="../../assets/img/minio-wis2box-incoming-dataset-folder.png" width="800">

!!! note
    O comando `wis2box data ingest` carregou o arquivo no bucket `wis2box-incoming` no MinIO em um diretório nomeado após o identificador de metadados que você forneceu.

Vá para o painel do Grafana no seu navegador e verifique o status da ingestão de dados.

!!! question "Exercício 2: verifique o status da ingestão de dados"
    
    Vá para o painel do Grafana no seu navegador e verifique o status da ingestão de dados.
    
    Os dados foram ingeridos com sucesso?

??? success "Clique para revelar a resposta"
    O painel na parte inferior do painel inicial do Grafana relata os seguintes avisos:    
    
    `WARNING - input=aws-example.csv warning=Station 0-20000-0-60355 not in station list; skipping`
    `WARNING - input=aws-example.csv warning=Station 0-20000-0-60360 not in station list; skipping`

    Este aviso indica que as estações não estão definidas na lista de estações do seu wis2box. Nenhuma notificação WIS2 será publicada para esta estação até que você a adicione à lista de estações e a associe ao tópico para o seu conjunto de dados.

!!! question "Exercício 3: adicione as estações de teste e repita a ingestão de dados"

    Adicione as estações ao seu wis2box usando o editor de estações no **wis2box-webapp**, e associe as estações ao tópico para o seu conjunto de dados.

    Agora, reenvie o arquivo de dados de exemplo `aws-example.csv` para o mesmo caminho no MinIO que você usou no exercício anterior.

    Verifique o painel do Grafana, há novos erros ou avisos? Como você pode ver que os dados de teste foram ingeridos e publicados com sucesso?

??? success "Clique para revelar a resposta"

    Você pode verificar os gráficos no painel inicial do Grafana para ver se os dados de teste foram ingeridos e publicados com sucesso.
    
    Se bem-sucedido, você deve ver o seguinte:

    <img alt="grafana_success" src="../../assets/img/grafana_success.png" width="800">

!!! question "Exercício 4: verifique o broker MQTT para notificações WIS2"
    
    Vá para o MQTT Explorer e verifique se você pode ver a Mensagem de Notificação WIS2 para os dados que você acabou de ingerir.
    
    Quantas notificações de dados WIS2 foram publicadas pelo seu wis2box?
    
    Como você acessa o conteúdo dos dados que estão sendo publicados?

??? success "Clique para revelar a resposta"

    Você deve ver 6 notificações de dados WIS2 publicadas pelo seu wis2box.

    Para acessar o conteúdo dos dados que estão sendo publicados, você pode expandir a estrutura do tópico para ver os diferentes níveis da mensagem até chegar ao último nível e revisar o conteúdo da mensagem de uma das mensagens.

    O conteúdo da mensagem tem uma seção "links" com uma chave "rel" de "canonical" e uma chave "href" com a URL para baixar os dados. A URL estará no formato `http://<seu-host>/data/...`. 
    
    Observe que o formato dos dados é BUFR e você precisará de um analisador BUFR para visualizar o conteúdo dos dados. O formato BUFR é um formato binário usado pelos serviços meteorológicos para troca de dados. Os plugins de dados dentro do wis2box transformaram os dados de CSV para BUFR antes de publicá-los.

## Visualizando o conteúdo dos dados que você publicou

Você pode usar o **wis2box-webapp** para visualizar o conteúdo das notificações de dados WIS2 que foram publicadas pelo seu wis2box.

Abra o **wis2box-webapp** no seu navegador navegando até `http://<seu-host>/wis2box-webapp` e selecione a aba **Monitoramento**:

<img alt="wis2box-webapp-monitor" src="../../assets/img/wis2box-webapp-monitor.png" width="220">

Na aba de monitoramento, selecione seu dataset-id e clique em "ATUALIZAR"

??? question "Exercício 5: visualize as notificações WIS2 no wis2box-webapp"
    
    Quantas notificações de dados WIS2 foram publicadas pelo seu wis2box? 

    Qual é a temperatura do ar relatada na última notificação na estação com o identificador WIGOS=0-20000-0-60355?

??? success "Clique para revelar a resposta"

    Se você ingeriu os dados de teste com sucesso, você deve ver 6 notificações de dados WIS2 publicadas pelo seu wis2box.

    Para ver a temperatura do ar medida para a estação com identificador WIGOS=0-20000-0-60355, clique no botão "INSPECIONAR" ao lado do arquivo para essa estação para abrir uma janela pop-up exibindo o conteúdo analisado do arquivo de dados. A temperatura do ar medida nesta estação foi de 25,0 graus Celsius.

!!! Note
    O contêiner wis2box-api inclui ferramentas para analisar arquivos BUFR e exibir o conteúdo em um formato legível por humanos. Isso não é um requisito central para a implementação do WIS2.0, mas foi incluído no wis2box para ajudar os publicadores de dados a verificar o conteúdo dos dados que estão publicando.

## Conclusão

!!! success "Parabéns!"
    Nesta sessão prática, você aprendeu como:

    - acionar o fluxo de trabalho do wis2box fazendo upload de dados no MinIO usando o comando `wis2box data ingest`
    - visualizar as notificações WIS2 publicadas pelo seu wis2box no painel do Grafana e no MQTT Explorer
    - verificar o conteúdo dos dados sendo publicados usando o **wis2box-webapp**