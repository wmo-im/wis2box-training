---
title: Adicionando cabeçalhos GTS às notificações WIS2
---

# Adicionando cabeçalhos GTS às notificações WIS2

!!! abstract "Objetivos de aprendizagem"

    Ao final desta sessão prática, você será capaz de:
    
    - configurar um mapeamento entre nome do arquivo e cabeçalhos GTS
    - ingerir dados com um nome de arquivo que corresponda aos cabeçalhos GTS
    - visualizar os cabeçalhos GTS nas notificações WIS2

## Introdução

Os Membros da WMO que desejam interromper sua transmissão de dados no GTS durante a fase de transição para o WIS2 precisarão adicionar cabeçalhos GTS às suas notificações WIS2. Esses cabeçalhos permitem que o gateway WIS2 para GTS encaminhe os dados para a rede GTS.

Isso permite que os Membros que migraram para usar um WIS2 Node para publicação de dados desativem seu sistema MSS e garantam que seus dados ainda estejam disponíveis para os Membros que ainda não migraram para o WIS2.

A propriedade GTS na Mensagem de Notificação WIS2 precisa ser adicionada como uma propriedade adicional à Mensagem de Notificação WIS2. A propriedade GTS é um objeto JSON que contém os cabeçalhos GTS necessários para que os dados sejam encaminhados para a rede GTS.

```json
{
  "gts": {
    "ttaaii": "FTAE31",
    "cccc": "VTBB"
  }
}
```

No wis2box, você pode adicionar isso automaticamente às Notificações WIS2 fornecendo um arquivo adicional chamado `gts_headers_mapping.csv` que contém as informações necessárias para mapear os cabeçalhos GTS para os nomes dos arquivos recebidos.

Este arquivo deve ser colocado no diretório definido por `WIS2BOX_HOST_DATADIR` no seu `wis2box.env` e deve ter as seguintes colunas:

- `string_in_filepath`: uma string que faz parte do nome do arquivo que será usada para corresponder aos cabeçalhos GTS
- `TTAAii`: o cabeçalho TTAAii a ser adicionado à notificação WIS2
- `CCCC`: o cabeçalho CCCC a ser adicionado à notificação WIS2

## Preparação

Certifique-se de ter acesso SSH à sua VM de estudante e que sua instância wis2box esteja em execução.

Certifique-se de estar conectado ao broker MQTT da sua instância wis2box usando o MQTT Explorer. Você pode usar as credenciais públicas `everyone/everyone` para se conectar ao broker.

Certifique-se de ter um navegador web aberto com o painel Grafana para sua instância acessando `http://YOUR-HOST:3000`

## Criando `gts_headers_mapping.csv`

Para adicionar cabeçalhos GTS às suas notificações WIS2, é necessário um arquivo CSV que mapeie os cabeçalhos GTS para os nomes dos arquivos recebidos.

O arquivo CSV deve ser nomeado (exatamente) `gts_headers_mapping.csv` e deve ser colocado no diretório definido por `WIS2BOX_HOST_DATADIR` no seu `wis2box.env`.

## Fornecendo um arquivo `gts_headers_mapping.csv`
    
Copie o arquivo `exercise-materials/gts-headers-exercises/gts_headers_mapping.csv` para sua instância wis2box e coloque-o no diretório definido por `WIS2BOX_HOST_DATADIR` no seu `wis2box.env`.

```bash
cp ~/exercise-materials/gts-headers-exercises/gts_headers_mapping.csv ~/wis2box-data
```

Em seguida, reinicie o contêiner wis2box-management para aplicar as alterações:

```bash
docker restart wis2box-management
```

## Ingerindo dados com cabeçalhos GTS

Copie o arquivo `exercise-materials/gts-headers-exercises/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt` para o diretório definido por `WIS2BOX_HOST_DATADIR` no seu `wis2box.env`:

```bash
cp ~/exercise-materials/gts-headers-exercises/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt ~/wis2box-data
```

Em seguida, faça login no contêiner **wis2box-management**:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Na linha de comando do wis2box, podemos ingerir o arquivo de dados de exemplo `A_SMRO01YRBK171200_C_EDZW_20240717120502.txt` em um conjunto de dados específico da seguinte forma:

```bash
wis2box data ingest -p /data/wis2box/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt --metadata-id urn:wmo:md:not-my-centre:core.surface-based-observations.synop
```

Certifique-se de substituir a opção `metadata-id` pelo identificador correto do seu conjunto de dados.

Verifique o painel Grafana para ver se os dados foram ingeridos corretamente. Se você vir algum AVISO ou ERRO, tente corrigi-los e repita o exercício com o comando `wis2box data ingest`.

## Visualizando os cabeçalhos GTS na Notificação WIS2

Vá para o MQTT Explorer e verifique a Mensagem de Notificação WIS2 para os dados que você acabou de ingerir.

A Mensagem de Notificação WIS2 deve conter os cabeçalhos GTS que você forneceu no arquivo `gts_headers_mapping.csv`.

## Conclusão

!!! success "Parabéns!"
    Nesta sessão prática, você aprendeu como:
      - adicionar cabeçalhos GTS às suas notificações WIS2
      - verificar se os cabeçalhos GTS estão disponíveis através da sua instalação wis2box