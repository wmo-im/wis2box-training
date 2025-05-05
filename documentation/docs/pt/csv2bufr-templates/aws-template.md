---
title: Modelo AWS
---

# Modelo csv2bufr para Estações Meteorológicas Automáticas reportando dados horários GBON

O **Modelo AWS** utiliza um formato CSV padronizado para ingestão de dados de Estações Meteorológicas Automáticas em apoio aos requisitos de relatório GBON. Este modelo de mapeamento converte dados CSV para a sequência BUFR 301150, 307096.

O formato é destinado ao uso com estações meteorológicas automáticas que reportam um número mínimo de parâmetros, incluindo pressão, temperatura e umidade do ar, velocidade e direção do vento e precipitação em uma base horária.

## Colunas e descrição do CSV

{{ read_csv("docs/assets/tables/aws-minimal.csv") }}

## Exemplo

Arquivo CSV de exemplo que está em conformidade com o modelo AWS: [aws-example.csv](/sample-data/aws-example.csv).