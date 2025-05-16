---
title: Inicializando o wis2box
---

# Inicializando o wis2box

!!! abstract "Resultados de aprendizado"

    Ao final desta sessão prática, você será capaz de:

    - executar o script `wis2box-create-config.py` para criar a configuração inicial
    - iniciar o wis2box e verificar o status de seus componentes
    - visualizar o conteúdo do **wis2box-api**
    - acessar o **wis2box-webapp**
    - conectar ao **wis2box-broker** local usando o MQTT Explorer

!!! note

    Os materiais de treinamento atuais são baseados no wis2box-release 1.0.0.
    
    Veja [accessing-your-student-vm](./accessing-your-student-vm.md) para instruções sobre como baixar e instalar o pacote de software do wis2box se você estiver realizando este treinamento fora de uma sessão de treinamento local.

## Preparação

Faça login na sua VM designada com seu nome de usuário e senha e certifique-se de que você está no diretório `wis2box`:

```bash
cd ~/wis2box
```

## Criando a configuração inicial

A configuração inicial para o wis2box requer:

- um arquivo de ambiente `wis2box.env` contendo os parâmetros de configuração
- um diretório na máquina hospedeira para compartilhar entre a máquina hospedeira e os contêineres do wis2box definidos pela variável de ambiente `WIS2BOX_HOST_DATADIR`

O script `wis2box-create-config.py` pode ser usado para criar a configuração inicial do seu wis2box.

Ele fará uma série de perguntas para ajudar a configurar sua configuração.

Você poderá revisar e atualizar os arquivos de configuração após a conclusão do script.

Execute o script da seguinte forma:

```bash
python3 wis2box-create-config.py
```

### Diretório wis2box-host-data

O script pedirá que você insira o diretório a ser usado para a variável de ambiente `WIS2BOX_HOST_DATADIR`.

Observe que você precisa definir o caminho completo para este diretório.

Por exemplo, se seu nome de usuário é `username`, o caminho completo para o diretório é `/home/username/wis2box-data`:

```{.copy}
username@student-vm-username:~/wis2box$ python3 wis2box-create-config.py
Por favor, insira o diretório a ser usado para WIS2BOX_HOST_DATADIR:
/home/username/wis2box-data
O diretório a ser usado para WIS2BOX_HOST_DATADIR será definido como:
    /home/username/wis2box-data
Está correto? (s/n/sair)
s
O diretório /home/username/wis2box-data foi criado.
```

### URL do wis2box

Em seguida, será solicitado que você insira a URL para seu wis2box. Esta é a URL que será usada para acessar a aplicação web, API e UI do wis2box.

Por favor, use `http://<seu-nome-de-host-ou-ip>` como a URL.

```{.copy}
Por favor, insira a URL do wis2box:
 Para testes locais a URL é http://localhost
 Para habilitar o acesso remoto, a URL deve apontar para o endereço IP público ou nome de domínio do servidor que hospeda o wis2box.
http://username.wis2.training
A URL do wis2box será definida como:
  http://username.wis2.training
Está correto? (s/n/sair)
```

### Senhas do WEBAPP, STORAGE e BROKER

Você pode usar a opção de geração de senha aleatória quando solicitado e definir `WIS2BOX_WEBAPP_PASSWORD`, `WIS2BOX_STORAGE_PASSWORD`, `WIS2BOX_BROKER_PASSWORD` por conta própria.

Não se preocupe em lembrar essas senhas, elas serão armazenadas no arquivo `wis2box.env` no seu diretório wis2box.

### Revisar `wis2box.env`

Uma vez que o script estiver concluído, verifique o conteúdo do arquivo `wis2box.env` no seu diretório atual:

```bash
cat ~/wis2box/wis2box.env
```

Ou verifique o conteúdo do arquivo via WinSCP.

!!! question

    Qual é o valor de WISBOX_BASEMAP_URL no arquivo wis2box.env?

??? success "Clique para revelar a resposta"

    O valor padrão para WIS2BOX_BASEMAP_URL é `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`.

    Esta URL refere-se ao servidor de tiles do OpenStreetMap. Se você deseja usar um provedor de mapas diferente, você pode alterar essa URL para apontar para um servidor de tiles diferente.

!!! question 

    Qual é o valor da variável de ambiente WIS2BOX_STORAGE_DATA_RETENTION_DAYS no arquivo wis2box.env?

??? success "Clique para revelar a resposta"

    O valor padrão para WIS2BOX_STORAGE_DATA_RETENTION_DAYS é 30 dias. Você pode alterar esse valor para um número diferente de dias, se desejar.
    
    O contêiner wis2box-management executa um cronjob diariamente para remover dados mais antigos que o número de dias definido por WIS2BOX_STORAGE_DATA_RETENTION_DAYS do bucket `wis2box-public` e do backend da API:
    
    ```{.copy}
    0 0 * * * su wis2box -c "wis2box data clean --days=$WIS2BOX_STORAGE_DATA_RETENTION_DAYS"
    ```

!!! note

    O arquivo `wis2box.env` contém variáveis de ambiente que definem a configuração do seu wis2box. Para mais informações, consulte a [wis2box-documentation](https://docs.wis2box.wis.wmo.int/en/latest/reference/configuration.html).

    Não edite o arquivo `wis2box.env` a menos que você tenha certeza das alterações que está fazendo. Alterações incorretas podem fazer com que seu wis2box pare de funcionar.

    Não compartilhe o conteúdo do seu arquivo `wis2box.env` com ninguém, pois ele contém informações sensíveis, como senhas.

## Iniciar o wis2box

Certifique-se de que você está no diretório que contém os arquivos de definição do pacote de software do wis2box:

```{.copy}
cd ~/wis2box
```

Inicie o wis2box com o seguinte comando:

```{.copy}
python3 wis2box-ctl.py start
```

Ao executar este comando pela primeira vez, você verá a seguinte saída:

```
Nenhum arquivo docker-compose.images-*.yml encontrado, criando um
Versão atual=Indefinida, última versão=1.0.0
Gostaria de atualizar? (s/n/sair)
```

Selecione ``s`` e o script criará o arquivo ``docker-compose.images-1.0.0.yml``, baixará as imagens Docker necessárias e iniciará os serviços.

Baixar as imagens pode levar algum tempo, dependendo da velocidade da sua conexão com a internet. Esta etapa é necessária apenas na primeira vez que você iniciar o wis2box.

Inspeccione o status com o seguinte comando:

```{.copy}
python3 wis2box-ctl.py status
```

Repita este comando até que todos os serviços estejam funcionando.

!!! note "wis2box e Docker"
    O wis2box funciona como um conjunto de contêineres Docker gerenciados pelo docker-compose.
    
    Os serviços são definidos nos diversos `docker-compose*.yml` que podem ser encontrados no diretório `~/wis2box/`.
    
    O script Python `wis2box-ctl.py` é usado para executar os comandos subjacentes do Docker Compose que controlam os serviços do wis2box.

    Você não precisa conhecer os detalhes dos contêineres Docker para executar o pacote de software do wis2box, mas pode inspecionar os arquivos `docker-compose*.yml` para ver como os serviços são definidos. Se você estiver interessado em aprender mais sobre Docker, pode encontrar mais informações na [Docker documentation](https://docs.docker.com/).

Para fazer login no contêiner wis2box-management, use o seguinte comando:

```{.copy}
python3 wis2box-ctl.py login
```

Dentro do contêiner wis2box-management, você pode executar vários comandos para gerenciar seu wis2box, como:

- `wis2box auth add-token --path processes/wis2box` : para criar um token de autorização para o endpoint `processes/wis2box`
- `wis2box data clean --days=<number-of-days>` : para limpar dados mais antigos que um certo número de dias do bucket `wis2box-public`

Para sair do contêiner e voltar para a máquina hospedeira, use o seguinte comando:

```{.copy}
exit
```

Execute o seguinte comando para ver os contêineres docker em execução na sua máquina hospedeira:

```{.copy}
docker ps
```

Você deve ver os seguintes contêineres em execução:

- wis2box-management
- wis2box-api
- wis2box-minio
- wis2box-webapp
- wis2box-auth
- wis2box-ui
- wis2downloader
- elasticsearch
- elasticsearch-exporter
- nginx
- mosquitto
- prometheus
- grafana
- loki

Esses contêineres fazem parte do pacote de software do wis2box e fornecem os vários serviços necessários para executar o wis2box.

Execute o seguinte comando para ver os volumes docker em execução na sua máquina hospedeira:

```{.copy}
docker volume ls
```

Você deve ver os seguintes volumes:

- wis2box_project_auth-data
- wis2box_project_es-data
- wis2box_project_htpasswd
- wis2box_project_minio-data
- wis2box_project_prometheus-data
- wis2box_project_loki-data
- wis2box_project_mosquitto-config

Bem como alguns volumes anônimos usados pelos vários contêineres.

Os volumes que começam com `wis2box_project_` são usados para armazenar dados persistentes para os vários serviços no pacote de software do wis2box.

## API do wis2box

O wis2box contém uma API (Interface de Programação de Aplicações) que fornece acesso a dados e processos para visualização interativa, transformação de dados e publicação.

Abra uma nova aba e navegue até a página `http://YOUR-HOST/oapi`.

<img alt="wis2box-api.png" src="/../assets/img/wis2box-api.png" width="800">

Esta é a página inicial da API do wis2box (executada via contêiner **wis2box-api**).

!!! question
     
     Quais coleções estão disponíveis atualmente?

??? success "Clique para revelar a resposta"
    
    Para visualizar as coleções atualmente disponíveis através da API, clique em `Ver as coleções neste serviço`:

    <img alt="wis2box-api-collections.png" src="/../assets/img/wis2box-api-collections.png" width="600">

    As seguintes coleções estão atualmente disponíveis:

    - Estações
    - Notificações de dados
    - Metadados de descoberta


!!! question

    Quantas notificações de dados foram publicadas?

??? success "Clique para revelar a resposta"

    Clique em "Notificações de dados", depois clique em `Navegar pelos itens de "Notificações de Dados"`. 
    
    Você notará que a página diz "Nenhum item" pois ainda não foram publicadas notificações de dados.

## Aplicativo web do wis2box

Abra um navegador da web e visite a página `http://YOUR-HOST/wis2box-webapp`.

Você verá um pop-up pedindo seu nome de usuário e senha. Use o nome de usuário padrão `wis2box-user` e o `WIS2BOX_WEBAPP_PASSWORD` definido no arquivo `wis2box.env` e clique em "Entrar":

!!! note 

    Verifique seu wis2box.env para o valor do seu WIS2BOX_WEBAPP_PASSWORD. Você pode usar o seguinte comando para verificar o valor dessa variável de ambiente:

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_WEBAPP_PASSWORD
    ```

Uma vez logado, mova o mouse para o menu à esquerda para ver as opções disponíveis no aplicativo web do wis2box:

<img alt="wis2box-webapp-menu.png" src="/../assets/img/wis2box-webapp-menu.png" width="400">

Este é o aplicativo web do wis2box que permite interagir com seu wis2box:

- criar e gerenciar conjuntos de dados
- atualizar/revisar seus metadados de estação
- fazer upload de observações manuais usando o formulário FM-12 synop 
- monitorar notificações publicadas no seu wis2box-broker

Usaremos este aplicativo web em uma sessão posterior.

## wis2box-broker

Abra o MQTT Explorer no seu computador e prepare uma nova conexão para se conectar ao seu broker (executado via contêiner **wis2box-broker**).

Clique em `+` para adicionar uma nova conexão:

<img alt="mqtt-explorer-new-connection.png" src="/../assets/img/mqtt-explorer-new-connection.png" width="300">

Você pode clicar no botão 'AVANÇADO' e verificar se você tem inscrições nos seguintes tópicos:

- `#`
- `$SYS/#`

<img alt="mqtt-explorer-topics.png" src="/../assets/img/mqtt-explorer-topics.png" width="550">

!!! note

    O tópico `#` é uma inscrição curinga que se inscreverá em todos os tópicos publicados no broker.

    As mensagens publicadas sob o tópico `$SYS` são mensagens do sistema publicadas pelo próprio serviço mosquitto.

Use os seguintes detalhes de conexão, certificando-se de substituir o valor de `<your-host>` pelo seu nome de host e `<WIS2BOX_BROKER_PASSWORD>` pelo valor do seu arquivo `wis2box.env`:

- **Protocolo: mqtt://**
- **Host: `<your-host>`**
- **Porta: 1883**
- **Nome de usuário: wis2box**
- **Senha: `<WIS2BOX_BROKER_PASSWORD>`**

!!! note 

    Você pode verificar seu wis2box.env para o valor do seu WIS2BOX_BROKER_PASSWORD. Você pode usar o seguinte comando para verificar o valor dessa variável de ambiente:

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_BROKER_PASSWORD
    ```

    Observe que esta é a sua senha **interna** do broker, o Global Broker usará credenciais diferentes (somente leitura) para se inscrever no seu broker. Nunca compartilhe essa senha com ninguém.

Certifique-se de clicar em "SALVAR" para armazenar os detalhes da sua conexão.

Em seguida, clique em "CONECTAR" para se conectar ao seu **wis2box-broker**.

<img alt="mqtt-explorer-wis2box-broker.png" src="/../assets/img/mqtt-explorer-wis2box-broker.png" width="600">

Uma vez conectado, verifique se as estatísticas internas do mosquitto estão sendo publicadas pelo seu broker sob o tópico `$SYS`:

<img alt="mqtt-explorer-sys-topic.png" src="/../assets/img/mqtt-explorer-sys-topic.png" width="400">

Mantenha o MQTT Explorer aberto, pois usaremos para monitorar as mensagens publicadas no broker.

## Conclusão

!!! success "Parabéns!"
    Nesta sessão prática, você aprendeu a:

    - executar o script `wis2box-create-config.py` para criar a configuração inicial
    - iniciar o wis2box e verificar o status de seus componentes
    - acessar o wis2box-webapp e wis2box-API em um navegador
    - conectar ao broker MQTT na sua VM de estudante usando o MQTT Explorer