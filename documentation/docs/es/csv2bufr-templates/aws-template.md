---
title: Plantilla AWS
---

# Plantilla csv2bufr para Estaciones Meteorológicas Automáticas que reportan datos horarios de GBON

La **Plantilla AWS** utiliza un formato CSV estandarizado para ingresar datos de Estaciones Meteorológicas Automáticas en apoyo a los requisitos de reporte de GBON. Esta plantilla de mapeo convierte datos CSV a la secuencia BUFR 301150, 307096.

El formato está destinado para uso con estaciones meteorológicas automáticas que reportan un número mínimo de parámetros, incluyendo presión, temperatura y humedad del aire, velocidad y dirección del viento y precipitación de manera horaria.

## Columnas CSV y descripción

{{ read_csv("docs/assets/tables/aws-minimal.csv") }}

## Ejemplo

Archivo CSV de ejemplo que se ajusta a la plantilla AWS: [aws-example.csv](./../../sample-data/aws-example.csv).