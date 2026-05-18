---
title: Plantilla DAYCLI
---

# Plantilla csv2bufr para datos climáticos diarios (DAYCLI)

La plantilla **DAYCLI** proporciona un formato CSV estandarizado para convertir datos climáticos diarios a la secuencia BUFR 307075.

El formato está diseñado para su uso con Sistemas de Gestión de Datos Climáticos para publicar datos en WIS2, en apoyo a los requisitos de reporte para observaciones climáticas diarias.

Esta plantilla mapea observaciones diarias de:

 - Temperatura mínima, máxima y promedio durante un período de 24 horas
 - Precipitación total acumulada durante un período de 24 horas
 - Profundidad total de nieve al momento de la observación
 - Profundidad de nieve fresca durante un período de 24 horas

Esta plantilla requiere metadatos adicionales con respecto a la plantilla simplificada de AWS: método de cálculo de la temperatura promedio; alturas del sensor y de la estación; clasificación de exposición y calidad de medición.

!!! Note "Acerca de la plantilla DAYCLI"
    Tenga en cuenta que la secuencia BUFR de DAYCLI se actualizará durante 2026 para incluir información adicional y banderas de control de calidad revisadas. La plantilla DAYCLI incluida en el wis2box se actualizará para reflejar estos cambios. La OMM comunicará cuando el software de wis2box se actualice para incluir la nueva plantilla DAYCLI, permitiendo a los usuarios actualizar sus sistemas en consecuencia.

## Columnas y descripción del CSV

{{ read_csv("docs/assets/tables/daycli-table.csv") }}

## Método de promediado

{{ read_csv("docs/assets/tables/averaging-method-table.csv") }}

## Banderas de calidad

{{ read_csv("docs/assets/tables/quality_flag.csv") }}

## Referencias para la clasificación de ubicación

[Referencia para "temperature_siting_classification"](https://library.wmo.int/idviewer/35625/839).

[Referencia para "precipitation_siting_classification"](https://library.wmo.int/idviewer/35625/840).

## Ejemplo

Archivo CSV de ejemplo que cumple con la plantilla DAYCLI: [daycli-example.csv](../../sample-data/daycli-example.csv).