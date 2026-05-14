---
title: Plantilla CLIMAT
---

# Plantilla csv2bufr para datos climáticos diarios (CLIMAT)

Los mensajes **CLIMAT** informan resúmenes climáticos mensuales compilados a partir de observaciones diarias en estaciones sinópticas y climatológicas, para apoyar el monitoreo climático, la investigación y el archivo.

La plantilla CLIMAT proporciona un formato CSV estandarizado para producir mensajes CLIMAT codificados en formato BUFR para las secuencias 301150,307073.

## Columnas y descripción del CSV

{{ read_csv("docs/assets/tables/climat-table.csv") }}

## Ejemplo

Archivo CSV de ejemplo que cumple con la plantilla CLIMAT: [climat-example.csv](../../sample-data/climat-example.csv).