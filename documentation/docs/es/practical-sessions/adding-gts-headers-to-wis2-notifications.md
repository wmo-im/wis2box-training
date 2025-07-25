---
title: Añadiendo encabezados GTS a las notificaciones WIS2
---

# Añadiendo encabezados GTS a las notificaciones WIS2

!!! abstract "Resultados de aprendizaje"

    Al final de esta sesión práctica, podrás:
    
    - configurar un mapeo entre el nombre del archivo y los encabezados GTS
    - ingerir datos con un nombre de archivo que coincida con los encabezados GTS
    - ver los encabezados GTS en las notificaciones WIS2

## Introducción

Los miembros de la OMM que deseen detener su transmisión de datos en GTS durante la fase de transición a WIS2 necesitarán añadir encabezados GTS a sus notificaciones WIS2. Estos encabezados permiten que la puerta de enlace de WIS2 a GTS reenvíe los datos a la red GTS.

Esto permite a los miembros que han migrado a usar un nodo WIS2 para la publicación de datos desactivar su sistema MSS y asegurar que sus datos sigan estando disponibles para los miembros que aún no han migrado a WIS2.

La propiedad GTS en el Mensaje de Notificación WIS2 necesita ser añadida como una propiedad adicional al Mensaje de Notificación WIS2. La propiedad GTS es un objeto JSON que contiene los encabezados GTS que son necesarios para que los datos sean reenviados a la red GTS.

```json
{
  "gts": {
    "ttaaii": "FTAE31",
    "cccc": "VTBB"
  }
}
```

Dentro de wis2box puedes añadir esto a las Notificaciones WIS2 automáticamente proporcionando un archivo adicional llamado `gts_headers_mapping.csv` que contiene la información requerida para mapear los encabezados GTS a los nombres de archivos entrantes.

Este archivo debe ser colocado en el directorio definido por `WIS2BOX_HOST_DATADIR` en tu `wis2box.env` y debe tener las siguientes columnas:

- `string_in_filepath`: una cadena que es parte del nombre del archivo que se utilizará para coincidir con los encabezados GTS
- `TTAAii`: el encabezado TTAAii que se añadirá a la notificación WIS2
- `CCCC`: el encabezado CCCC que se añadirá a la notificación WIS2

## Preparación

Asegúrate de tener acceso SSH a tu VM de estudiante y que tu instancia de wis2box esté funcionando.

Asegúrate de estar conectado al broker MQTT de tu instancia de wis2box usando MQTT Explorer. Puedes usar las credenciales públicas `everyone/everyone` para conectarte al broker.

Asegúrate de tener un navegador web abierto con el tablero de Grafana para tu instancia yendo a `http://YOUR-HOST:3000`

## creando `gts_headers_mapping.csv`

Para añadir encabezados GTS a tus notificaciones WIS2, se requiere un archivo CSV que mapee los encabezados GTS a los nombres de archivos entrantes.

El archivo CSV debe ser nombrado (exactamente) `gts_headers_mapping.csv` y debe ser colocado en el directorio definido por `WIS2BOX_HOST_DATADIR` en tu `wis2box.env`. 

## Proporcionando un archivo `gts_headers_mapping.csv`
    
Copia el archivo `exercise-materials/gts-headers-exercises/gts_headers_mapping.csv` a tu instancia de wis2box y colócalo en el directorio definido por `WIS2BOX_HOST_DATADIR` en tu `wis2box.env`.

```bash
cp ~/exercise-materials/gts-headers-exercises/gts_headers_mapping.csv ~/wis2box-data
```

Luego reinicia el contenedor de wis2box-management para aplicar los cambios:

```bash
docker restart wis2box-management
```

## Ingeriendo datos con encabezados GTS

Copia el archivo `exercise-materials/gts-headers-exercises/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt` al directorio definido por `WIS2BOX_HOST_DATADIR` en tu `wis2box.env`:

```bash
cp ~/exercise-materials/gts-headers-exercises/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt ~/wis2box-data
```

Luego inicia sesión en el contenedor **wis2box-management**:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Desde la línea de comandos de wis2box podemos ingerir el archivo de datos de muestra `A_SMRO01YRBK171200_C_EDZW_20240717120502.txt` en un conjunto de datos específico de la siguiente manera:

```bash
wis2box data ingest -p /data/wis2box/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt --metadata-id urn:wmo:md:not-my-centre:core.surface-based-observations.synop
```

Asegúrate de reemplazar la opción `metadata-id` con el identificador correcto para tu conjunto de datos.

Revisa el tablero de Grafana para ver si los datos fueron ingeridos correctamente. Si ves alguna ADVERTENCIA o ERROR, intenta solucionarlo y repite el comando `wis2box data ingest`.

## Viendo los encabezados GTS en la Notificación WIS2

Ve al MQTT Explorer y verifica el Mensaje de Notificación WIS2 para los datos que acabas de ingerir.

El Mensaje de Notificación WIS2 debería contener los encabezados GTS que proporcionaste en el archivo `gts_headers_mapping.csv`.

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica, aprendiste cómo:
      - añadir encabezados GTS a tus notificaciones WIS2
      - verificar que los encabezados GTS estén disponibles a través de tu instalación de wis2box