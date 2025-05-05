---
title: Plantilla AWS
---

# Plantilla csv2bufr para Estaciones Meteorológicas Automáticas que reportan datos GBON por hora

La **Plantilla AWS** utiliza un formato CSV estandarizado para ingerir datos de Estaciones Meteorológicas Automáticas en apoyo a los requisitos de informes GBON. Esta plantilla de mapeo convierte datos CSV a secuencia BUFR 301150, 307096.

El formato está destinado a ser utilizado con estaciones meteorológicas automáticas que reportan un número mínimo de parámetros, incluyendo presión, temperatura del aire y humedad, velocidad y dirección del viento y precipitación en una base horaria.

## Columnas CSV y descripción

{{ read_csv("docs/assets/tables/aws-minimal.csv") }}

## Ejemplo

Archivo CSV de ejemplo que cumple con la plantilla AWS: [aws-example.csv](/sample-data/aws-example.csv).