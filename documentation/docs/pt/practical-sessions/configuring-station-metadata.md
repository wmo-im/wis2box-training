---
title: Configurando metadados da estação
---

# Configurando metadados da estação

!!! abstract "Objetivos de aprendizagem"

    Ao final desta sessão prática, você será capaz de:

    - criar um token de autorização para o endpoint `collections/stations`
    - adicionar metadados de estação ao wis2box
    - atualizar/excluir metadados de estação usando o **wis2box-webapp**

## Introdução

Para compartilhar dados internacionalmente entre os Membros da OMM, é importante ter um entendimento comum das estações que estão produzindo os dados. O Sistema Global Integrado de Observação da OMM (WIGOS) fornece uma estrutura para a integração de sistemas de observação e sistemas de gerenciamento de dados. O **Identificador de Estação WIGOS (WSI)** é usado como a referência única da estação que produziu um conjunto específico de dados de observação.

O wis2box possui uma coleção de metadados de estações que é usada para descrever as estações que estão produzindo os dados de observação e deve ser recuperada do **OSCAR/Surface**. Os metadados da estação no wis2box são usados pelas ferramentas de transformação BUFR para verificar se os dados de entrada contêm um Identificador de Estação WIGOS (WSI) válido e fornecer um mapeamento entre o WSI e os metadados da estação.

## Criar um token de autorização para collections/stations

Para editar estações através do **wis2box-webapp**, você primeiro precisará criar um token de autorização.

Faça login na sua VM de estudante e certifique-se de estar no diretório `wis2box`:

```bash
cd ~/wis2box
```

Em seguida, faça login no container **wis2box-management** com o seguinte comando:

```bash
python3 wis2box-ctl.py login
```

Dentro do container **wis2box-management**, você pode criar um token de autorização para um endpoint específico usando o comando: `wis2box auth add-token --path <my-endpoint>`.

Por exemplo, para usar um token gerado automaticamente aleatório para o endpoint `collections/stations`:

```{.copy}
wis2box auth add-token --path collections/stations
```	

A saída será semelhante a esta:

```{.copy}
Continue with token: 7ca20386a131f0de384e6ffa288eb1ae385364b3694e47e3b451598c82e899d1 [y/N]? y
Token successfully created
```

Ou, se você quiser definir seu próprio token para o endpoint `collections/stations`, pode usar o seguinte exemplo:

```{.copy}
wis2box auth add-token --path collections/stations DataIsMagic
```

Saída:
    
```{.copy}
Continue with token: DataIsMagic [y/N]? y
Token successfully created
```

Por favor, crie um token de autorização para o endpoint `collections/stations` usando as instruções acima.

## Adicionar metadados de estação usando o **wis2box-webapp**

O **wis2box-webapp** fornece uma interface gráfica para editar metadados de estação.

Abra o **wis2box-webapp** no seu navegador navegando até `http://YOUR-HOST/wis2box-webapp`, e selecione estações:

<img alt="wis2box-webapp-select-stations" src="../../assets/img/wis2box-webapp-select-stations.png" width="250">

Quando você clica em 'adicionar nova estação', é solicitado que forneça o identificador de estação WIGOS para a estação que deseja adicionar:

<img alt="wis2box-webapp-import-station-from-oscar" src="../../assets/img/wis2box-webapp-import-station-from-oscar.png" width="800">

!!! note "Adicione metadados de estação para 3 ou mais estações"
    Por favor, adicione três ou mais estações à coleção de metadados de estação do seu wis2box.
      
    Use estações do seu país se possível, especialmente se você trouxe seus próprios dados.
      
    Se seu país não possui estações no OSCAR/Surface, você pode usar as seguintes estações para este exercício:

      - 0-20000-0-91334
      - 0-20000-0-96323 (observe a elevação da estação ausente no OSCAR)
      - 0-20000-0-96749 (observe a elevação da estação ausente no OSCAR)

Quando você clica em pesquisar, os dados da estação são recuperados do OSCAR/Surface, observe que isso pode levar alguns segundos.

Revise os dados retornados pelo OSCAR/Surface e adicione dados ausentes quando necessário. Selecione um tópico para a estação e forneça seu token de autorização para o endpoint `collections/stations` e clique em 'salvar':

<img alt="wis2box-webapp-create-station-save" src="../../assets/img/wis2box-webapp-create-station-save.png" width="800">

<img alt="wis2box-webapp-create-station-success" src="../../assets/img/wis2box-webapp-create-station-success.png" width="500">

Volte para a lista de estações e você verá a estação que adicionou:

<img alt="wis2box-webapp-stations-with-one-station" src="../../assets/img/wis2box-webapp-stations-with-one-station.png" width="800">

Repita este processo até ter pelo menos 3 estações configuradas.

!!! tip "Derivando informações de elevação ausentes"

    Se a elevação da sua estação estiver ausente, existem serviços online para ajudar a procurar a elevação usando dados de elevação abertos. Um exemplo é a [API Open Topo Data](https://www.opentopodata.org).

    Por exemplo, para obter a elevação na latitude -6.15558 e longitude 106.84204, você pode copiar e colar a seguinte URL em uma nova aba do navegador:

    ```{.copy}
    https://api.opentopodata.org/v1/aster30m?locations=-6.15558,106.84204
    ```

    Saída:

    ```{.copy}
    {
      "results": [
        {
          "dataset": "aster30m", 
          "elevation": 7.0, 
          "location": {
            "lat": -6.15558, 
            "lng": 106.84204
          }
        }
      ], 
      "status": "OK"
    }
    ```

## Revisar seus metadados de estação

Os metadados da estação são armazenados no backend do wis2box e disponibilizados através da **wis2box-api**.

Se você abrir um navegador e navegar até `http://YOUR-HOST/oapi/collections/stations/items`, verá os metadados da estação que você adicionou:

<img alt="wis2box-api-stations" src="../../assets/img/wis2box-api-stations.png" width="800">

!!! note "Revise seus metadados de estação"

    Verifique se as estações que você adicionou estão associadas ao seu conjunto de dados visitando `http://YOUR-HOST/oapi/collections/stations/items` no seu navegador.

Você também tem a opção de visualizar/atualizar/excluir a estação no **wis2box-webapp**. Observe que você precisa fornecer seu token de autorização para o endpoint `collections/stations` para atualizar/excluir a estação.

!!! note "Atualizar/excluir metadados de estação"

    Tente ver se você consegue atualizar/excluir os metadados de estação para uma das estações que você adicionou usando o **wis2box-webapp**.

## Upload em massa de metadados de estação

Observe que o wis2box também tem a capacidade de realizar carregamento "em massa" de metadados de estação a partir de um arquivo CSV usando a linha de comando no container **wis2box-management**.

```bash
python3 wis2box-ctl.py login
wis2box metadata station publish-collection -p /data/wis2box/metadata/station/station_list.csv -th origin/a/wis2/centre-id/weather/surface-based-observations/synop
```

Isso permite que você carregue um grande número de estações de uma vez e as associe a um tópico específico.

Você pode criar o arquivo CSV usando Excel ou um editor de texto e depois fazer o upload para wis2box-host-datadir para disponibilizá-lo ao container **wis2box-management** no diretório `/data/wis2box/`.

Após fazer um upload em massa de estações, é recomendado revisar as estações no **wis2box-webapp** para garantir que os dados foram carregados corretamente.

Consulte a [documentação oficial do wis2box](https://docs.wis2box.wis.wmo.int) para mais informações sobre como usar este recurso.

## Conclusão

!!! success "Parabéns!"
    Nesta sessão prática, você aprendeu como:

    - criar um token de autorização para o endpoint `collections/stations` para ser usado com o **wis2box-webapp**
    - adicionar metadados de estação ao wis2box usando o **wis2box-webapp**
    - visualizar/atualizar/excluir metadados de estação usando o **wis2box-webapp**