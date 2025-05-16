---
title: Baixando e decodificando dados do WIS2
---

# Baixando e decodificando dados do WIS2

!!! abstract "Resultados de aprendizagem!"

    Ao final desta sessão prática, você será capaz de:

    - usar o "wis2downloader" para se inscrever em notificações de dados do WIS2 e baixar dados para seu sistema local
    - visualizar o status dos downloads no painel do Grafana
    - decodificar alguns dados baixados usando o container "decode-bufr-jupyter"

## Introdução

Nesta sessão, você aprenderá como configurar uma inscrição em um Broker do WIS2 e baixar automaticamente dados para seu sistema local usando o serviço "wis2downloader" incluído no wis2box.

!!! note "Sobre o wis2downloader"
     
     O wis2downloader também está disponível como um serviço autônomo que pode ser executado em um sistema diferente daquele que está publicando as notificações do WIS2. Veja [wis2downloader](https://pypi.org/project/wis2downloader/) para mais informações sobre o uso do wis2downloader como um serviço autônomo.

     Se você deseja desenvolver seu próprio serviço para se inscrever em notificações do WIS2 e baixar dados, você pode usar o [código fonte do wis2downloader](https://github.com/World-Meteorological-Organization/wis2downloader) como referência.

!!! Other tools for accessing WIS2 data

    As seguintes ferramentas também podem ser usadas para descobrir e acessar dados do WIS2:

    - [pywiscat](https://github.com/wmo-im/pywiscat) oferece capacidade de busca sobre o Catálogo Global de Descoberta do WIS2 em apoio ao relatório e análise do Catálogo do WIS2 e seus metadados de descoberta associados
    - [pywis-pubsub](https://github.com/World-Meteorological-Organization/pywis-pubsub) oferece capacidade de inscrição e download de dados da WMO a partir dos serviços de infraestrutura do WIS2

## Preparação

Antes de começar, faça login na sua VM de estudante e certifique-se de que sua instância do wis2box está funcionando.

## Visualizando o painel do wis2downloader no Grafana

Abra um navegador web e navegue até o painel do Grafana para sua instância do wis2box acessando `http://YOUR-HOST:3000`.

Clique em painéis no menu à esquerda e, em seguida, selecione o **painel do wis2downloader**.

Você deverá ver o seguinte painel:

![painel do wis2downloader](../assets/img/wis2downloader-dashboard.png)

Este painel é baseado nas métricas publicadas pelo serviço wis2downloader e mostrará o status dos downloads que estão em andamento.

No canto superior esquerdo, você pode ver as inscrições que estão atualmente ativas.

Mantenha este painel aberto, pois você o usará para monitorar o progresso do download no próximo exercício.

## Revisando a configuração do wis2downloader

O serviço wis2downloader iniciado pela pilha do wis2box pode ser configurado usando as variáveis de ambiente definidas no seu arquivo wis2box.env.

As seguintes variáveis de ambiente são usadas pelo wis2downloader:

    - DOWNLOAD_BROKER_HOST: O nome do host do broker MQTT ao qual conectar. Padrão é globalbroker.meteo.fr
    - DOWNLOAD_BROKER_PORT: A porta do broker MQTT ao qual conectar. Padrão é 443 (HTTPS para websockets)
    - DOWNLOAD_BROKER_USERNAME: O nome de usuário para usar ao conectar ao broker MQTT. Padrão é everyone
    - DOWNLOAD_BROKER_PASSWORD: A senha para usar ao conectar ao broker MQTT. Padrão é everyone
    - DOWNLOAD_BROKER_TRANSPORT: websockets ou tcp, o mecanismo de transporte para usar ao conectar ao broker MQTT. Padrão é websockets,
    - DOWNLOAD_RETENTION_PERIOD_HOURS: O período de retenção em horas para os dados baixados. Padrão é 24
    - DOWNLOAD_WORKERS: O número de trabalhadores de download para usar. Padrão é 8. Determina o número de downloads paralelos.
    - DOWNLOAD_MIN_FREE_SPACE_GB: O espaço livre mínimo em GB para manter no volume que hospeda os downloads. Padrão é 1.

Para revisar a configuração atual do wis2downloader, você pode usar o seguinte comando:

```bash
cat ~/wis2box/wis2box.env | grep DOWNLOAD
```

!!! question "Revise a configuração do wis2downloader"
    
    Qual é o broker MQTT padrão ao qual o wis2downloader se conecta?

    Qual é o período de retenção padrão para os dados baixados?

??? success "Clique para revelar a resposta"

    O broker MQTT padrão ao qual o wis2downloader se conecta é `globalbroker.meteo.fr`.

    O período de retenção padrão para os dados baixados é de 24 horas.

!!! note "Atualizando a configuração do wis2downloader"

    Para atualizar a configuração do wis2downloader, você pode editar o arquivo wis2box.env. Para aplicar as alterações, você pode executar novamente o comando de início para a pilha do wis2box:

    ```bash
    python3 wis2box-ctl.py start
    ```

    E você verá o serviço wis2downloader reiniciar com a nova configuração.

Você pode manter a configuração padrão para o propósito deste exercício.

## Adicionando inscrições ao wis2downloader

Dentro do container **wis2downloader**, você pode usar a linha de comando para listar, adicionar e deletar inscrições.

Para fazer login no container **wis2downloader**, use o seguinte comando:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Em seguida, use o seguinte comando para listar as inscrições que estão atualmente ativas:

```bash
wis2downloader list-subscriptions
```

Este comando retorna uma lista vazia, pois não há inscrições atualmente ativas.

Para o propósito deste exercício, vamos nos inscrever no seguinte tópico `cache/a/wis2/de-dwd-gts-to-wis2/#`, para se inscrever em dados publicados pelo gateway GTS-to-WIS2 hospedado pela DWD e notificações de download do Global Cache.

Para adicionar essa inscrição, use o seguinte comando:

```bash
wis2downloader add-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Em seguida, saia do container **wis2downloader** digitando `exit`:

```bash
exit
```

Verifique o painel do wis2downloader no Grafana para ver a nova inscrição adicionada. Espere alguns minutos e você deverá ver os primeiros downloads começando. Vá para o próximo exercício assim que confirmar que os downloads estão começando.

## Visualizando os dados baixados

O serviço wis2downloader na pilha do wis2box baixa os dados no diretório 'downloads' no diretório que você definiu como WIS2BOX_HOST_DATADIR no seu arquivo wis2box.env. Para visualizar o conteúdo do diretório de downloads, você pode usar o seguinte comando:

```bash
ls -R ~/wis2box-data/downloads
```

Observe que os dados baixados são armazenados em diretórios nomeados após o tópico em que a Notificação WIS2 foi publicada.

## Removendo inscrições do wis2downloader

Em seguida, faça login novamente no container wis2downloader:

```bash
python3 wis2box-ctl.py login wis2downloader
```

e remova a inscrição que você fez do wis2downloader, usando o seguinte comando:

```bash
wis2downloader remove-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

E saia do container wis2downloader digitando `exit`:
    
```bash
exit
```

Verifique o painel do wis2downloader no Grafana para ver a inscrição removida. Você deverá ver os downloads parando.

## Baixar e decodificar dados para uma trajetória de ciclone tropical

Neste exercício, você se inscreverá no WIS2 Training Broker que está publicando dados de exemplo para fins de treinamento. Você configurará uma inscrição para baixar dados para uma trajetória de ciclone tropical. Em seguida, você decodificará os dados baixados usando o container "decode-bufr-jupyter".

### Inscreva-se no wis2training-broker e configure uma nova inscrição

Isso demonstra como se inscrever em um broker que não é o broker padrão e permitirá que você baixe alguns dados publicados pelo WIS2 Training Broker.

Edite o arquivo wis2box.env e altere o DOWNLOAD_BROKER_HOST para `wis2training-broker.wis2dev.io`, altere DOWNLOAD_BROKER_PORT para `1883` e altere DOWNLOAD_BROKER_TRANSPORT para `tcp`:

```copy
# configurações do downloader
DOWNLOAD_BROKER_HOST=wis2training-broker.wis2dev.io
DOWNLOAD_BROKER_PORT=1883
DOWNLOAD_BROKER_USERNAME=everyone
DOWNLOAD_BROKER_PASSWORD=everyone
# mecanismo de transporte de download (tcp ou websockets)
DOWNLOAD_BROKER_TRANSPORT=tcp
```

Em seguida, execute o comando 'start' novamente para aplicar as alterações:

```bash
python3 wis2box-ctl.py start
```

Verifique os logs do wis2downloader para ver se a conexão com o novo broker foi bem-sucedida:

```bash
docker logs wis2downloader
```

Você deverá ver a seguinte mensagem de log:

```copy
...
INFO - Conectando...
INFO - Host: wis2training-broker.wis2dev.io, port: 1883
INFO - Conectado com sucesso
```

Agora vamos configurar uma nova inscrição no tópico para baixar dados de trajetória de ciclone do WIS2 Training Broker.

Faça login no container **wis2downloader**:

```bash
python3 wis2box-ctl.py login wis2downloader
```

E execute o seguinte comando (copie e cole isso para evitar erros de digitação):

```bash
wis2downloader add-subscription --topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
```

Saia do container **wis2downloader** digitando `exit`.

Espere até ver os downloads começando no painel do wis2downloader no Grafana.

!!! note "Baixando dados do WIS2 Training Broker"

    O WIS2 Training Broker é um broker de teste que é usado para fins de treinamento e pode não publicar dados o tempo todo.

    Durante as sessões de treinamento presenciais, o instrutor local garantirá que o WIS2 Training Broker publique dados para você baixar.

    Se você estiver fazendo este exercício fora de uma sessão de treinamento, pode não ver nenhum dado sendo baixado.

Verifique se os dados foram baixados verificando os logs do wis2downloader novamente com:

```bash
docker logs wis2downloader
```

Você deverá ver uma mensagem de log semelhante à seguinte:

```copy
[...] INFO - Mensagem recebida sob o tópico origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
[...] INFO - Baixado A_JSXX05ECEP020000_C_ECMP_...
```

### Decodificando dados baixados

Para demonstrar como você pode decodificar os dados baixados, iniciaremos um novo container usando a imagem 'decode-bufr-jupyter'.

Este container iniciará um servidor de notebook Jupyter na sua instância, que inclui a biblioteca "ecCodes" que você pode usar para decodificar dados BUFR.

Usaremos os notebooks de exemplo incluídos em `~/exercise-materials/notebook-examples` para decodificar os dados baixados para as trajetórias de ciclones.

Para iniciar o container, use o seguinte comando:

```bash
docker run -d --name decode-bufr-jupyter \
    -v ~/wis2box-data/downloads:/root/downloads \
    -p 8888:8888 \
    -e JUPYTER_TOKEN=dataismagic! \
    mlimper/decode-bufr-jupyter
```

!!! note "Sobre o container decode-bufr-jupyter"

    O container `decode-bufr-jupyter` é um container personalizado que inclui a biblioteca ecCodes e executa um servidor de notebook Jupyter. O container é baseado em uma imagem que inclui a biblioteca `ecCodes` para decodificar dados BUFR, junto com bibliotecas para plotagem e análise de dados.

    O comando acima inicia o container no modo desanexado, com o nome `decode-bufr-jupyter`, a porta 8888 é mapeada para o sistema host e a variável de ambiente `JUPYTER_TOKEN` é definida como `dataismagic!`.
    
    O comando acima também monta o diretório `~/wis2box-data/downloads` para `/root/downloads` no container. Isso garante que os dados baixados estejam disponíveis para o servidor de notebook Jupyter.
    
Uma vez que o container esteja iniciado, você pode acessar o servidor de notebook Jupyter navegando até `http://YOUR-HOST:8888` no seu navegador web.

Você verá uma tela solicitando que você insira uma "Senha ou token".

Forneça o token `dataismagic!` para fazer login no servidor de notebook Jupyter.

Após fazer login, você deverá ver a seguinte tela listando os diretórios no container:

![Tela inicial do Jupyter notebook](../assets/img/jupyter-files-screen1.png)

Dê um duplo clique no diretório `example-notebooks` para abri-lo.

Você deverá ver a seguinte tela listando os notebooks de exemplo, dê um duplo clique no notebook `tropical_cyclone_track.ipynb` para abri-lo:

![Notebooks de exemplo do Jupyter](../assets/img/jupyter-files-screen2.png)

Você agora está no notebook Jupyter para decodificar os dados da trajetória do ciclone tropical:

![Notebook Jupyter de trajetória de ciclone tropical](../assets/img/jupyter-tropical-cyclone-track.png)

Leia as instruções no caderno e execute as células para decodificar os dados baixados das trajetórias de ciclones tropicais. Execute cada célula clicando nela e depois no botão de execução na barra de ferramentas ou pressionando `Shift+Enter`.

No final, você deve ver um gráfico da probabilidade de ocorrência das trajetórias de ciclones tropicais:

![Tropical cyclone tracks](../assets/img/tropical-cyclone-track-map.png)

!!! question 

    O resultado exibe a probabilidade prevista de trajetória de tempestade tropical dentro de 200 km. Como você atualizaria o caderno para exibir a probabilidade prevista de trajetória de tempestade tropical dentro de 300 km?

??? success "Clique para revelar a resposta"

    Para atualizar o caderno para exibir a probabilidade prevista de trajetória de tempestade tropical dentro de uma distância diferente, você pode atualizar a variável `distance_threshold` no bloco de código que calcula a probabilidade de ocorrência.

    Para exibir a probabilidade prevista de trajetória de tempestade tropical dentro de 300 km,

    ```python
    # set distance threshold (meters)
    distance_threshold = 300000  # 300 km em metros
    ```

    Em seguida, re-execute as células no caderno para ver o gráfico atualizado.

!!! note "Decodificando dados BUFR"

    O exercício que você acabou de fazer forneceu um exemplo específico de como você pode decodificar dados BUFR usando a biblioteca ecCodes. Diferentes tipos de dados podem requerer diferentes etapas de decodificação e você pode precisar consultar a documentação para o tipo de dado com o qual está trabalhando.
    
    Para mais informações, consulte a [documentação do ecCodes](https://confluence.ecmwf.int/display/ECC).



## Conclusão

!!! success "Parabéns!"

    Nesta sessão prática, você aprendeu como:

    - usar o 'wis2downloader' para se inscrever em um WIS2 Broker e baixar dados para o seu sistema local
    - visualizar o status dos downloads no painel do Grafana
    - decodificar alguns dados baixados usando o contêiner 'decode-bufr-jupyter'