---
title: Configurando um conjunto de dados recomendado com controle de acesso
---

# Configurando um conjunto de dados recomendado com controle de acesso

!!! abstract "Resultados de aprendizado"
    Ao final desta sessão prática, você será capaz de:

    - criar um novo conjunto de dados com política de dados 'recomendada'
    - adicionar um token de acesso ao conjunto de dados
    - validar que o conjunto de dados não pode ser acessado sem o token de acesso
    - adicionar o token de acesso aos cabeçalhos HTTP para acessar o conjunto de dados

## Introdução

Conjuntos de dados que não são considerados 'núcleo' na WMO podem opcionalmente ser configurados com uma política de controle de acesso. wis2box fornece um mecanismo para adicionar um token de acesso a um conjunto de dados que impedirá os usuários de baixar dados a menos que forneçam o token de acesso nos cabeçalhos HTTP.

## Preparação

Certifique-se de ter acesso SSH à sua VM de estudante e que sua instância de wis2box esteja funcionando.

Certifique-se de estar conectado ao broker MQTT de sua instância wis2box usando MQTT Explorer. Você pode usar as credenciais públicas `everyone/everyone` para se conectar ao broker.

Certifique-se de ter um navegador web aberto com o wis2box-webapp para sua instância acessando `http://YOUR-HOST/wis2box-webapp`.

## Criar um novo conjunto de dados com política de dados 'recomendada'

Vá para a página 'editor de conjunto de dados' no wis2box-webapp e crie um novo conjunto de dados. Selecione o Tipo de Dados = 'weather/surface-weather-observations/synop'.

<img alt="create-dataset-recommended" src="../../assets/img/create-dataset-template.png" width="800">

Para "Centre ID", use o mesmo que você usou nas sessões práticas anteriores.

Clique em 'CONTINUE To FORM' para prosseguir.

No editor de conjunto de dados, defina a política de dados para 'recomendada' (observe que alterar a política de dados atualizará a 'Hierarquia de Tópicos').
Substitua o 'Local ID' gerado automaticamente por um nome descritivo para o conjunto de dados, por exemplo, 'dados-recomendados-com-controle-de-acesso':

<img alt="create-dataset-recommended" src="../../assets/img/create-dataset-recommended.png" width="800">

Continue preenchendo os campos necessários para Propriedades Espaciais e Informações de Contato, e 'Validar formulário' para verificar se há erros.

Finalmente, envie o conjunto de dados, usando o token de autenticação criado anteriormente, e verifique se o novo conjunto de dados foi criado no wis2box-webapp.

Verifique o MQTT-explorer para ver se você recebe a Mensagem de Notificação WIS2 anunciando o novo registro de Metadados de Descoberta no tópico `origin/a/wis2/<your-centre-id>/metadata`.

## Adicionar um token de acesso ao conjunto de dados

Faça login no contêiner wis2box-management,

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Do comando de linha dentro do contêiner, você pode proteger um conjunto de dados usando o comando `wis2box auth add-token`, usando a flag `--metadata-id` para especificar o identificador de metadados do conjunto de dados e o token de acesso como argumento.

Por exemplo, para adicionar o token de acesso `S3cr3tT0k3n` ao conjunto de dados com identificador de metadados `urn:wmo:md:not-my-centre:core.surface-based-observations.synop`:

```bash
wis2box auth add-token --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop S3cr3tT0k3n
```

Saia do contêiner wis2box-management:

```bash
exit
```

## Publicar alguns dados no conjunto de dados

Copie o arquivo `exercise-materials/access-control-exercises/aws-example.csv` para o diretório definido por `WIS2BOX_HOST_DATADIR` no seu `wis2box.env`:

```bash
cp ~/exercise-materials/access-control-exercises/aws-example.csv ~/wis2box-data
```

Em seguida, use WinSCP ou um editor de linha de comando para editar o arquivo `aws-example.csv` e atualizar os identificadores de estação WIGOS nos dados de entrada para corresponder às estações que você tem em sua instância wis2box.

Em seguida, vá para o editor de estação no wis2box-webapp. Para cada estação que você usou em `aws-example.csv`, atualize o campo 'tópico' para corresponder ao 'tópico' do conjunto de dados que você criou no exercício anterior.

Esta estação agora estará associada a 2 tópicos, um para o conjunto de dados 'núcleo' e outro para o conjunto de dados 'recomendado':

<img alt="edit-stations-add-topics" src="../../assets/img/edit-stations-add-topics.png" width="600">

Você precisará usar seu token para `collections/stations` para salvar os dados da estação atualizada.

Em seguida, faça login no contêiner wis2box-management:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

A partir da linha de comando do wis2box, podemos ingerir o arquivo de dados de exemplo `aws-example.csv` em um conjunto de dados específico da seguinte forma:

```bash
wis2box data ingest -p /data/wis2box/aws-example.csv --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop
```

Certifique-se de fornecer o identificador de metadados correto para seu conjunto de dados e **verifique se você recebe notificações de dados WIS2 no MQTT Explorer**, no tópico `origin/a/wis2/<your-centre-id>/data/recommended/surface-based-observations/synop`.

Verifique o link canônico na Mensagem de Notificação WIS2 e copie/cole o link no navegador para tentar baixar os dados.

Você deverá ver um erro 403 Proibido.

## Adicionar o token de acesso aos cabeçalhos HTTP para acessar o conjunto de dados

Para demonstrar que o token de acesso é necessário para acessar o conjunto de dados, reproduziremos o erro que você viu no navegador usando a função de linha de comando `wget`.

Da linha de comando na sua VM de estudante, use o comando `wget` com o link canônico que você copiou da Mensagem de Notificação WIS2.

```bash
wget <canonical-link>
```

Você verá que a solicitação HTTP retorna com *401 Não autorizado* e os dados não são baixados.

Agora adicione o token de acesso aos cabeçalhos HTTP para acessar o conjunto de dados.

```bash
wget --header="Authorization: Bearer S3cr3tT0k3n" <canonical-link>
```

Agora os dados devem ser baixados com sucesso.

## Conclusão

!!! success "Parabéns!"
    Nesta sessão prática, você aprendeu como:

    - criar um novo conjunto de dados com política de dados 'recomendada'
    - adicionar um token de acesso ao conjunto de dados
    - validar que o conjunto de dados não pode ser acessado sem o token de acesso
    - adicionar o token de acesso aos cabeçalhos HTTP para acessar o conjunto de dados