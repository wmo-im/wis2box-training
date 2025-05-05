---
title: Modelo DAYCLI
---

# Modelo csv2bufr para dados climáticos diários (DAYCLI)

O modelo **DAYCLI** fornece um formato CSV padronizado para converter dados climáticos diários para a sequência BUFR 307075.

O formato é destinado ao uso com Sistemas de Gestão de Dados Climáticos para publicar dados no WIS2, em apoio aos requisitos de relatórios para observações climáticas diárias.

Este modelo mapeia observações diárias de:

 - Temperatura mínima, máxima e média durante o período de 24 horas
 - Precipitação total acumulada durante o período de 24 horas
 - Profundidade total da neve no momento da observação
 - Profundidade de neve fresca durante o período de 24 horas

Este modelo requer metadados adicionais em relação ao modelo simplificado AWS: método de cálculo da temperatura média; alturas do sensor e da estação; classificação de exposição e qualidade da medição.

!!! Nota "Sobre o modelo DAYCLI"
    Por favor, note que a sequência BUFR DAYCLI será atualizada durante 2025 para incluir informações adicionais e bandeiras de QC revisadas. O modelo DAYCLI incluído no wis2box será atualizado para refletir essas mudanças. A OMM comunicará quando o software wis2box for atualizado para incluir o novo modelo DAYCLI, permitindo que os usuários atualizem seus sistemas de acordo.

## Colunas CSV e descrição

{{ read_csv("docs/assets/tables/daycli-table.csv") }}

## Método de média

{{ read_csv("docs/assets/tables/averaging-method-table.csv") }}

## Bandeira de qualidade

{{ read_csv("docs/assets/tables/quality_flag.csv") }}

## Referências para classificação de localização

[Referência para "classificação de localização de temperatura"](https://library.wmo.int/idviewer/35625/839).

[Referência para "classificação de localização de precipitação"](https://library.wmo.int/idviewer/35625/840).

## Exemplo

Arquivo CSV de exemplo que está em conformidade com o modelo DAYCLI: [daycli-example.csv](/sample-data/daycli-example.csv).