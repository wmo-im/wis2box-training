---
title: Añadiendo encabezados GTS a las notificaciones WIS2
---

# Añadiendo encabezados GTS a las notificaciones WIS2

!!! abstract "Resultados de aprendizaje"

    Al final de esta sesión práctica, serás capaz de:
    
    - configurar un mapeo entre nombres de archivo y encabezados GTS
    - ingerir datos con un nombre de archivo que coincida con los encabezados GTS
    - visualizar los encabezados GTS en las notificaciones WIS2
    - usar el formulario FM-12 SYNOP para añadir manualmente encabezados GTS a una notificación WIS2

## Introducción

Los Miembros de la OMM que deseen detener la transmisión de sus datos en GTS durante la fase de transición a WIS2 necesitarán añadir encabezados GTS a sus notificaciones WIS2. Estos encabezados permiten que el gateway de WIS2 a GTS reenvíe los datos a la red GTS.

Esto permite a los Miembros que han migrado a usar un nodo WIS2 para la publicación de datos deshabilitar su sistema MSS y garantizar que sus datos sigan estando disponibles para los Miembros que aún no han migrado a WIS2.

La propiedad GTS en el Mensaje de Notificación WIS2 debe añadirse como una propiedad adicional al Mensaje de Notificación WIS2. La propiedad GTS es un objeto JSON que contiene los encabezados GTS necesarios para que los datos sean reenviados a la red GTS.

```json
{
  "gts": {
    "ttaaii": "FTAE31",
    "cccc": "VTBB"
  }
}
```

Dentro de wis2box, puedes añadir esto a las Notificaciones WIS2 automáticamente proporcionando un archivo adicional llamado `gts_headers_mapping.csv` que contiene la información requerida para mapear los encabezados GTS a los nombres de archivo entrantes.

Este archivo debe colocarse en el directorio definido por `WIS2BOX_HOST_DATADIR` en tu archivo `wis2box.env` y debe tener las siguientes columnas:

- `string_in_filepath`: una cadena que forma parte del nombre del archivo que se utilizará para coincidir con los encabezados GTS
- `TTAAii`: el encabezado TTAAii que se añadirá a la notificación WIS2
- `CCCC`: el encabezado CCCC que se añadirá a la notificación WIS2

A partir de wis2box-1.3.0, los publicadores de datos tienen dos opciones para (opcionalmente) añadir propiedades GTS a sus notificaciones:

1. Para archivos subidos a MinIO, preparar el archivo de mapeo `gts_headers_mappings.csv` con las propiedades requeridas.

2. Para entrada de datos usando el formulario FM-12 SYNOP en wis2box-webapp, seleccionar `Add GTS headers` y proporcionar la información manualmente.

## Preparación

Asegúrate de tener acceso SSH a tu VM de estudiante y que tu instancia de wis2box esté funcionando.

Asegúrate de estar conectado al broker MQTT de tu instancia de wis2box usando MQTT Explorer. Puedes usar las credenciales públicas `everyone/everyone` para conectarte al broker.

Asegúrate de tener un navegador web abierto con el tablero de Grafana para tu instancia accediendo a `http://YOUR-HOST:3000`.

## Ejercicio 1: Usar un archivo de mapeo para datos subidos a MinIO

El primer ejercicio demostrará cómo añadir encabezados GTS para datos que se suben a MinIO, usando un archivo de mapeo llamado `gts_headers_mapping.csv`.

### Crear `gts_headers_mapping.csv`

Para añadir encabezados GTS a tus notificaciones WIS2, se requiere un archivo CSV que mapee los encabezados GTS a los nombres de archivo entrantes.

El archivo CSV debe llamarse (exactamente) `gts_headers_mapping.csv` y debe colocarse en el directorio definido por `WIS2BOX_HOST_DATADIR` en tu archivo `wis2box.env`.

Copia el archivo `exercise-materials/gts-headers-exercises/gts_headers_mapping.csv` a tu instancia de wis2box y colócalo en el directorio definido por `WIS2BOX_HOST_DATADIR` en tu archivo `wis2box.env`.

```bash
cp ~/exercise-materials/gts-headers-exercises/gts_headers_mapping.csv ~/wis2box-data
```

### Aplicar los mapeos
    
Después de crear el archivo `gts_headers_mapping.csv`, necesitas reiniciar el contenedor wis2box-management para aplicar los cambios. Puedes hacerlo ejecutando el siguiente comando en tu VM de estudiante:

```bash
docker restart wis2box-management
```

### Ingerir datos con encabezados GTS

Copia el archivo `exercise-materials/gts-headers-exercises/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt` al directorio definido por `WIS2BOX_HOST_DATADIR` en tu archivo `wis2box.env`:

```bash
cp ~/exercise-materials/gts-headers-exercises/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt ~/wis2box-data
```

Luego inicia sesión en el contenedor **wis2box-management**:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Desde la línea de comandos de wis2box, podemos ingerir el archivo de datos de ejemplo `A_SMRO01YRBK171200_C_EDZW_20240717120502.txt` en un conjunto de datos específico de la siguiente manera:

```bash
wis2box data ingest -p /data/wis2box/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt --metadata-id urn:wmo:md:not-my-centre:core.surface-based-observations.synop
```

Asegúrate de reemplazar la opción `metadata-id` con el identificador correcto para tu conjunto de datos.

Revisa el tablero de Grafana para verificar si los datos fueron ingeridos correctamente. Si ves algún WARNING o ERROR, intenta solucionarlos y repite el ejercicio con el comando `wis2box data ingest`.

### Visualizar los encabezados GTS en la Notificación WIS2

Ve a MQTT Explorer y verifica el Mensaje de Notificación WIS2 para los datos que acabas de ingerir.

El Mensaje de Notificación WIS2 debería contener los encabezados GTS que proporcionaste en el archivo `gts_headers_mapping.csv`.

## Ejercicio 2: Usar el formulario FM-12 SYNOP

Cuando uses el formulario FM-12 SYNOP en wis2box-webapp, puedes añadir manualmente encabezados GTS a tus notificaciones WIS2 seleccionando la opción "Add GTS headers" y proporcionando la información requerida.

Para este ejercicio, puedes usar los datos de ejemplo a continuación o proporcionar los tuyos propios:

Mensaje FM-12 SYNOP:

```{copy}
AAXX 03094
64400 42460 71004 10285 20245 30113 40133 8493/
    333 59005 83813 81930 87363 94966 95836=
```

Encabezados GTS: TTAAii=`ISIH01` y CCCC=`FCBB`

!!! note
    El plugin synop2bufr en wis2box convierte mensajes FM-12 SYNOP en BUFR, por lo que el TTAAii debería comenzar con `IS`:

    - I = Datos observacionales (codificados en binario) – BUFR
    - S = Superficie/nivel del mar

### Enviar manualmente el formulario FM-12 SYNOP con encabezados GTS

Ve al formulario FM-12 SYNOP en wis2box-webapp y completa el formulario con los datos de ejemplo anteriores o usa los tuyos propios.

Asegúrate de seleccionar la opción "Add GTS headers" y proporcionar la información requerida de los encabezados GTS:

<img alt="fm-12-synop-form-gts-headers.png" src="/../assets/img/fm-12-synop-form-gts-headers.png" width="800">

Proporciona el token de autenticación requerido y envía el formulario.

Es probable que veas un mensaje de error porque esta estación no está en tu lista de estaciones. Necesitarás añadir la estación "0-20000-0-64400" a tu lista de estaciones para que los datos se conviertan y publiquen correctamente.

### Visualizar los encabezados GTS en la Notificación WIS2

Ve a MQTT Explorer y verifica el Mensaje de Notificación WIS2 para los datos que acabas de ingerir para ver si los encabezados GTS están incluidos en la notificación.

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica, aprendiste cómo:
      - añadir encabezados GTS a tus notificaciones WIS2
      - verificar que los encabezados GTS están disponibles a través de tu instalación de wis2box