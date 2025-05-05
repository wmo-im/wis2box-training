---
title: Descobrindo conjuntos de dados do WIS2 Global Discovery Catalogue
---

# Descobrindo conjuntos de dados do WIS2 Global Discovery Catalogue

!!! abstract "Objetivos de aprendizagem!"

    Ao final desta sessão prática, você será capaz de:

    - usar pywiscat para descobrir conjuntos de dados do Global Discovery Catalogue (GDC)

## Introdução

Nesta sessão, você aprenderá como descobrir dados do WIS2 Global Discovery Catalogue (GDC).

No momento, os seguintes GDCs estão disponíveis:

- Environment and Climate Change Canada, Meteorological Service of Canada: <https://wis2-gdc.weather.gc.ca>
- China Meteorological Administration: <https://gdc.wis.cma.cn>
- Deutscher Wetterdienst: <https://wis2.dwd.de/gdc>

Durante as sessões de treinamento local, um GDC local é configurado para permitir que os participantes consultem o GDC para os metadados que publicaram de suas instâncias wis2box. Neste caso, os instrutores fornecerão a URL para o GDC local.

## Preparação

!!! note
    Antes de começar, faça login na sua máquina virtual de estudante.

## Instalando pywiscat

Use o instalador de pacotes Python `pip3` para instalar o pywiscat em sua máquina virtual:
```bash
pip3 install pywiscat
```

!!! note

    Se você encontrar o seguinte erro:

    ```
    WARNING: The script pywiscat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    Então execute o seguinte comando:

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    ...onde `$USER` é seu nome de usuário na sua máquina virtual.

Verifique se a instalação foi bem-sucedida:

```bash
pywiscat --version
```

## Encontrando dados com pywiscat

Por padrão, o pywiscat se conecta ao Global Discovery Catalogue do Canadá. Vamos configurar o pywiscat para consultar o GDC de treinamento definindo a variável de ambiente `PYWISCAT_GDC_URL`:

```bash
export PYWISCAT_GDC_URL=http://gdc.wis2.training:5002
```

Vamos usar o [pywiscat](https://github.com/wmo-im/pywiscat) para consultar o GDC configurado como parte do treinamento.

```bash
pywiscat search --help
```

Agora pesquise no GDC por todos os registros:

```bash
pywiscat search
```

!!! question

    Quantos registros são retornados da pesquisa?

??? success "Clique para revelar a resposta"
    O número de registros depende do GDC que você está consultando. Ao usar o GDC local de treinamento, você deve ver que o número de registros é igual ao número de conjuntos de dados que foram inseridos no GDC durante as outras sessões práticas.

Vamos tentar consultar o GDC com uma palavra-chave:

```bash
pywiscat search -q observations
```

!!! question

    Qual é a política de dados dos resultados?

??? success "Clique para revelar a resposta"
    Todos os dados retornados devem especificar dados "core"

Tente consultas adicionais com `-q`

!!! tip

    O sinalizador `-q` permite a seguinte sintaxe:

    - `-q synop`: encontra todos os registros com a palavra "synop"
    - `-q temp`: encontra todos os registros com a palavra "temp"
    - `-q "observations AND oman"`: encontra todos os registros com as palavras "observations" e "oman"
    - `-q "observations NOT oman"`: encontra todos os registros que contêm a palavra "observations" mas não a palavra "oman"
    - `-q "synop OR temp"`: encontra todos os registros com "synop" ou "temp"
    - `-q "obs*"`: pesquisa aproximada

    Ao pesquisar termos com espaços, coloque entre aspas duplas.

Vamos obter mais detalhes sobre um resultado específico de pesquisa que nos interessa:

```bash
pywiscat get <id>
```

!!! tip

    Use o valor `id` da pesquisa anterior.

## Conclusão

!!! success "Parabéns!"

    Nesta sessão prática, você aprendeu como:

    - usar pywiscat para descobrir conjuntos de dados do WIS2 Global Discovery Catalogue