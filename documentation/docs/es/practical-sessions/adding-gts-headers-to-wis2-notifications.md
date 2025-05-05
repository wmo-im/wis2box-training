---
title: Agregando encabezados GTS a las notificaciones WIS2
---

# Agregando encabezados GTS a las notificaciones WIS2

!!! abstract "Objetivos de aprendizaje"

    Al final de esta sesión práctica, podrás:
    
    - configurar un mapeo entre nombre de archivo y encabezados GTS
    - ingerir datos con un nombre de archivo que coincida con los encabezados GTS
    - ver los encabezados GTS en las notificaciones WIS2

## Introducción

Los Miembros de la OMM que deseen detener su transmisión de datos en GTS durante la fase de transición a WIS2 necesitarán agregar encabezados GTS a sus notificaciones WIS2. Estos encabezados permiten que la pasarela WIS2 a GTS reenvíe los datos a la red GTS.

Esto permite a los Miembros que han migrado a usar un nodo WIS2 para la publicación de datos desactivar su sistema MSS y asegurar que sus datos sigan estando disponibles para los Miembros que aún no han migrado a WIS2.

La propiedad GTS en el Mensaje de Notificación WIS2 debe agregarse como una propiedad adicional al Mensaje de Notificación WIS2. La propiedad GTS es un objeto JSON que contiene los encabezados GTS necesarios para que los datos sean reenviados a la red GTS.

```json
{
  "gts": {
    "ttaaii": "FTAE31",
    "cccc": "VTBB"
  }
}
```

Dentro de wis2box puedes agregar esto a las Notificaciones WIS2 automáticamente proporcionando un archivo adicional llamado `gts_headers_mapping.csv` que contiene la información necesaria para mapear los encabezados GTS a los nombres de archivo entrantes.

Este archivo debe colocarse en el directorio definido por `WIS2BOX_HOST_DATADIR` en tu `wis2box.env` y debe tener las siguientes columnas:

- `string_in_filepath`: una cadena que es parte del nombre del archivo que se usará para hacer coincidir los encabezados GTS
- `TTAAii`: el encabezado TTAAii que se agregará a la notificación WIS2
- `CCCC`: el encabezado CCCC que se agregará a la notificación WIS2

## Preparación

Asegúrate de tener acceso SSH a tu VM de estudiante y que tu instancia de wis2box esté funcionando.

Asegúrate de estar conectado al broker MQTT de tu instancia wis2box usando MQTT Explorer. Puedes usar las credenciales públicas `everyone/everyone` para conectarte al broker.

Asegúrate de tener un navegador web abierto con el panel de Grafana para tu instancia yendo a `http://YOUR-HOST:3000`

## Creando `gts_headers_mapping.csv`

Para agregar encabezados GTS a tus notificaciones WIS2, se requiere un archivo CSV que mapee los encabezados GTS a los nombres de archivo entrantes.

El archivo CSV debe llamarse (exactamente) `gts_headers_mapping.csv` y debe colocarse en el directorio definido por `WIS2BOX_HOST_DATADIR` en tu `wis2box.env`.

## Proporcionando un archivo `gts_headers_mapping.csv`
    
Copia el archivo `exercise-materials/gts-headers-exercises/gts_headers_mapping.csv` a tu instancia wis2box y colócalo en el directorio definido por `WIS2BOX_HOST_DATADIR` en tu `wis2box.env`.

```bash
cp ~/exercise-materials/gts-headers-exercises/gts_headers_mapping.csv ~/wis2box-data
```

Luego reinicia el contenedor wis2box-management para aplicar los cambios:

```bash
docker restart wis2box-management
```

## Ingiriendo datos con encabezados GTS

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

Verifica el panel de Grafana para ver si los datos se ingirieron correctamente. Si ves alguna ADVERTENCIA o ERROR, intenta corregirlos y repite el ejercicio con el comando `wis2box data ingest`.

## Visualizando los encabezados GTS en la Notificación WIS2

Ve a MQTT Explorer y busca el Mensaje de Notificación WIS2 para los datos que acabas de ingerir.

El Mensaje de Notificación WIS2 debe contener los encabezados GTS que proporcionaste en el archivo `gts_headers_mapping.csv`.

## Conclusión

!!! success "¡Felicitaciones!"
    En esta sesión práctica, aprendiste cómo:
      - agregar encabezados GTS a tus notificaciones WIS2
      - verificar que los encabezados GTS estén disponibles a través de tu instalación wis2box