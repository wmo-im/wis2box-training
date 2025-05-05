---
title: Conversão de dados SYNOP para BUFR
---

# Conversão de dados SYNOP para BUFR usando o wis2box-webapp

!!! abstract "Resultados de aprendizado"
    Ao final desta sessão prática, você será capaz de:

    - enviar boletins FM-12 SYNOP válidos por meio do aplicativo web wis2box para conversão para BUFR e troca através do WIS2.0
    - validar, diagnosticar e corrigir erros simples de codificação em um boletim FM-12 SYNOP antes da conversão de formato e troca
    - garantir que os metadados da estação necessários estejam disponíveis no wis2box
    - confirmar e inspecionar boletins convertidos com sucesso

## Introdução

Para permitir que observadores manuais enviem dados diretamente para o WIS2.0, o wis2box-webapp possui um formulário para converter boletins FM-12 SYNOP para BUFR. O formulário também permite que os usuários diagnostiquem e corrijam erros simples de codificação no boletim FM-12 SYNOP antes da conversão de formato e troca e inspecionem os dados BUFR resultantes.

## Preparação

!!! warning "Pré-requisitos"

    - Certifique-se de que seu wis2box foi configurado e iniciado.
    - Abra um terminal e conecte-se à sua VM de estudante usando SSH.
    - Conecte-se ao corretor MQTT da sua instância wis2box usando o MQTT Explorer.
    - Abra o aplicativo web wis2box (``http://<seu-nome-de-host>/wis2box-webapp``) e certifique-se de que você está logado.

## Usando o wis2box-webapp para converter FM-12 SYNOP para BUFR

### Exercício 1 - usando o wis2box-webapp para converter FM-12 SYNOP para BUFR

Certifique-se de que você tem o token de autenticação para "processes/wis2box" que você gerou no exercício anterior e que você está conectado ao corretor wis2box no MQTT Explorer.

Copie a seguinte mensagem:
    
``` {.copy}
AAXX 27031
15015 02999 02501 10103 21090 39765 42952 57020 60001=
``` 

Abra o aplicativo web wis2box e navegue até a página synop2bufr usando o menu de navegação à esquerda e proceda da seguinte forma:

- Cole o conteúdo que você copiou na caixa de entrada de texto.
- Selecione o mês e o ano usando o seletor de data, assuma o mês atual para este exercício.
- Selecione um tópico no menu suspenso (as opções são baseadas nos conjuntos de dados configurados no wis2box).
- Insira o token de autenticação "processes/wis2box" que você gerou anteriormente
- Certifique-se de que "Publicar no WIS2" está ativado
- Clique em "ENVIAR"

<center><img alt="Diálogo mostrando a página synop2bufr, incluindo botão de alternância" src="../../assets/img/synop2bufr-toggle.png"></center>

Clique em enviar. Você receberá uma mensagem de aviso, pois a estação não está registrada no wis2box. Vá para o editor de estações e importe a seguinte estação:

``` {.copy}
0-20000-0-15015
```

Certifique-se de que a estação está associada ao tópico que você selecionou na etapa anterior e, em seguida, retorne à página synop2bufr e repita o processo com os mesmos dados de antes.

!!! question
    Como você pode ver o resultado da conversão de FM-12 SYNOP para BUFR?

??? success "Clique para revelar a resposta"
    A seção de resultados da página mostra Avisos, Erros e arquivos BUFR de Saída.

    Clique em "Arquivos BUFR de Saída" para ver uma lista dos arquivos que foram gerados. Você deve ver um arquivo listado.

    O botão de download permite que os dados BUFR sejam baixados diretamente para o seu computador.

    O botão de inspeção executa um processo para converter e extrair os dados de BUFR.

    <center><img alt="Diálogo mostrando o resultado de enviar uma mensagem com sucesso"
         src="../../assets/img/synop2bufr-ex2-success.png"></center>

!!! question
    Os dados de entrada FM-12 SYNOP não incluíam a localização da estação, elevação ou altura do barômetro.
    Confirme que esses estão nos dados BUFR de saída, de onde eles vêm?

??? success "Clique para revelar a resposta"
    Clicar no botão de inspeção deve abrir um diálogo como o mostrado abaixo.

    <center><img alt="Resultados do botão de inspeção mostrando os metadados básicos da estação, a localização da estação e as propriedades observadas"
         src="../../assets/img/synop2bufr-ex2.png"></center>

    Isso inclui a localização da estação mostrada em um mapa e metadados básicos, bem como as observações na mensagem.
    
    Como parte da transformação de FM-12 SYNOP para BUFR, metadados adicionais foram adicionados ao arquivo BUFR.
    
    O arquivo BUFR também pode ser inspecionado baixando o arquivo e validando usando uma ferramenta como o validador BUFR da ECMWF ecCodes.

Vá para o MQTT Explorer e verifique o tópico de notificações WIS2 para ver as notificações WIS2 que foram publicadas.

### Exercício 2 - entendendo a lista de estações

Neste próximo exercício, você converterá um arquivo contendo vários relatórios, veja os dados abaixo:

``` {.copy}
AAXX 27031
15015 02999 02501 10103 21090 39765 42952 57020 60001=
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
```

!!! question
    Baseado no exercício anterior, olhe para a mensagem FM-12 SYNOP e preveja quantas mensagens BUFR
    serão geradas.
    
    Agora copie e cole essa mensagem no formulário SYNOP e envie os dados.

    O número de mensagens geradas correspondeu à sua expectativa e, se não, por quê?

??? warning "Clique para revelar a resposta"
    
    Você poderia esperar que três mensagens BUFR fossem geradas, uma para cada relatório meteorológico. No entanto, em vez disso, você recebeu 2 avisos e apenas um arquivo BUFR.
    
    Para que um relatório meteorológico seja convertido para BUFR, os metadados básicos contidos na lista de estações são necessários. Embora o exemplo acima inclua três relatórios meteorológicos, duas das três estações que relataram não estavam registradas no seu wis2box.
    
    Como resultado, apenas um dos três relatórios meteorológicos resultou em um arquivo BUFR sendo gerado e uma notificação WIS2 sendo publicada. Os outros dois relatórios meteorológicos foram ignorados e avisos foram gerados.

!!! hint
    Observe a relação entre o Identificador WIGOS e o identificador tradicional da estação incluído na saída BUFR. Em muitos casos, para estações listadas no WMO-No. 9 Volume A no momento da migração para identificadores de estação WIGOS, o identificador de estação WIGOS é dado pelo identificador de estação tradicional com ``0-20000-0`` prefixado,
    por exemplo, ``15015`` se tornou ``0-20000-0-15015``.

Usando a página da lista de estações, importe as seguintes estações:

``` {.copy}
0-20000-0-15020
0-20000-0-15090
```

Certifique-se de que as estações estão associadas ao tópico que você selecionou no exercício anterior e, em seguida, retorne à página synop2bufr e repita o processo.

Três arquivos BUFR agora devem ser gerados e não deve haver avisos ou erros listados no aplicativo web.

Além das informações básicas da estação, metadados adicionais, como a elevação da estação acima do nível do mar e a altura do barômetro acima do nível do mar, são necessários para a codificação para BUFR. Os campos estão incluídos nas páginas da lista de estações e do editor de estações.
    
### Exercício 3 - depuração

Neste último exercício, você identificará e corrigirá dois dos problemas mais comuns encontrados ao
usar essa ferramenta para converter FM-12 SYNOP para BUFR.

Os dados de exemplo são mostrados na caixa abaixo, examine os dados e tente resolver quaisquer problemas que possam existir antes de enviar os dados pelo aplicativo web.

!!! hint
    Você pode editar os dados na caixa de entrada na página do aplicativo web. Se você perder algum problema,
    eles devem ser detectados e destacados como um aviso ou erro assim que o botão enviar for clicado.

``` {.copy}
AAXX 27031
15015 02999 02501 10103 21090 39765 42952 57020 60001
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
```

!!! question
    Quais problemas você esperava encontrar ao converter os dados para BUFR e como você
    os superou? Houve algum problema que você não estava esperando?

??? success "Clique para revelar a resposta"
    No primeiro exemplo, o símbolo de "fim de texto" (=), ou delimitador de registro, está faltando entre o
    primeiro e o segundo relatórios meteorológicos. Consequentemente, as linhas 2 e 3 são tratadas como um único relatório,
    levando a erros na análise da mensagem.

O segundo exemplo abaixo contém vários problemas comuns encontrados em relatórios FM-12 SYNOP. Examine os
dados e tente identificar os problemas e, em seguida, envie os dados corrigidos pelo aplicativo web.

```{.copy}
AAXX 27031
15020 02997 23104 10/30 21075 30177 40377 580200 60001 81041=
```

!!! question
    Quais problemas você encontrou e como os resolveu?

??? success "Clique para revelar a resposta"
    Há dois problemas no relatório meteorológico.
    
    O primeiro, no grupo de temperatura do ar assinada, tem o caractere das dezenas definido como ausente (/),
    levando a um grupo inválido. Neste exemplo, sabemos que a temperatura é de 13,0 graus Celsius (dos exemplos acima) e, portanto, esse problema pode ser corrigido. Operacionalmente, o valor correto precisaria ser confirmado com o observador.

    O segundo problema ocorre no grupo 5, onde há um caractere adicional, com o caractere final duplicado. Este problema pode ser corrigido removendo o caractere extra.

## Limpeza

Durante os exercícios desta sessão, você importou vários arquivos para sua lista de estações. Navegue até a 
página da lista de estações e clique nos ícones de lixeira para deletar as estações. Você pode precisar atualizar a página para ter
as estações removidas da lista após a exclusão.

<center><img alt="Visualizador de metadados da estação"
         src="../../assets/img/synop2bufr-trash.png" width="600"></center>

## Conclusão

!!! success "Parabéns!"

    Nesta sessão prática, você aprendeu:

    - como a ferramenta synop2bufr pode ser usada para converter relatórios FM-12 SYNOP para BUFR;
    - como enviar um relatório FM-12 SYNOP através do aplicativo web;
    - como diagnosticar e corrigir erros simples em um relatório FM-12 SYNOP;
    - a importância de registrar estações no wis2box (e OSCAR/Surface);
    - e o uso do botão de inspeção para visualizar o conteúdo dos dados BUFR.