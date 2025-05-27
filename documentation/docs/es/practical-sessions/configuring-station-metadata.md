---
title: Configuración de metadatos de estaciones
---

# Configuración de metadatos de estaciones

!!! abstract "Resultados de aprendizaje"

    Al final de esta sesión práctica, podrás:

    - crear un token de autorización para el endpoint `collections/stations`
    - añadir metadatos de estaciones a wis2box
    - actualizar/eliminar metadatos de estaciones usando el **wis2box-webapp**

## Introducción

Para compartir datos internacionalmente entre los Miembros de la OMM, es importante tener un entendimiento común de las estaciones que están produciendo los datos. El Sistema Global Integrado de Observación de la OMM (WIGOS) proporciona un marco para la integración de sistemas de observación y sistemas de gestión de datos. El **Identificador de Estación WIGOS (WSI)** se utiliza como la referencia única de la estación que produjo un conjunto específico de datos de observación.

wis2box tiene una colección de metadatos de estaciones que se utiliza para describir las estaciones que están produciendo los datos de observación y deben ser recuperados de **OSCAR/Surface**. Los metadatos de estaciones en wis2box son utilizados por las herramientas de transformación BUFR para verificar que los datos de entrada contengan un Identificador de Estación WIGOS (WSI) válido y para proporcionar un mapeo entre el WSI y los metadatos de la estación.

## Crear un token de autorización para collections/stations

Para editar estaciones a través del **wis2box-webapp** primero necesitarás crear un token de autorización.

Inicia sesión en tu VM de estudiante y asegúrate de estar en el directorio `wis2box`:

```bash
cd ~/wis2box
```

Luego inicia sesión en el contenedor **wis2box-management** con el siguiente comando:

```bash
python3 wis2box-ctl.py login
```

Dentro del contenedor **wis2box-management** puedes crear un token de autorización para un endpoint específico usando el comando: `wis2box auth add-token --path <my-endpoint>`.

Por ejemplo, para usar un token generado automáticamente al azar para el endpoint `collections/stations`:

```{.copy}
wis2box auth add-token --path collections/stations
```	

La salida se verá así:

```{.copy}
Continue with token: 7ca20386a131f0de384e6ffa288eb1ae385364b3694e47e3b451598c82e899d1 [y/N]? y
Token successfully created
```

O, si deseas definir tu propio token para el endpoint `collections/stations`, puedes usar el siguiente ejemplo:

```{.copy}
wis2box auth add-token --path collections/stations DataIsMagic
```

Salida:
    
```{.copy}
Continue with token: DataIsMagic [y/N]? y
Token successfully created
```

Por favor, crea un token de autorización para el endpoint `collections/stations` usando las instrucciones anteriores.

## añadir metadatos de estaciones usando el **wis2box-webapp**

El **wis2box-webapp** proporciona una interfaz gráfica para editar metadatos de estaciones.

Abre el **wis2box-webapp** en tu navegador navegando a `http://YOUR-HOST/wis2box-webapp`, y selecciona estaciones:

<img alt="wis2box-webapp-select-stations" src="/../assets/img/wis2box-webapp-select-stations.png" width="250">

Cuando hagas clic en 'añadir nueva estación' se te pedirá que proporciones el identificador de estación WIGOS para la estación que deseas añadir:

<img alt="wis2box-webapp-import-station-from-oscar" src="/../assets/img/wis2box-webapp-import-station-from-oscar.png" width="800">

!!! note "Añadir metadatos de estación para 3 o más estaciones"
    Por favor, añade tres o más estaciones a la colección de metadatos de estaciones de tu wis2box. 
      
    Si es posible, utiliza estaciones de tu país, especialmente si trajiste tus propios datos.
      
    Si tu país no tiene ninguna estación en OSCAR/Surface, puedes usar las siguientes estaciones para el propósito de este ejercicio:

      - 0-20000-0-91334
      - 0-20000-0-96323 (nota la elevación de la estación faltante en OSCAR)
      - 0-20000-0-96749 (nota la elevación de la estación faltante en OSCAR)

Cuando hagas clic en buscar, los datos de la estación se recuperarán de OSCAR/Surface, ten en cuenta que esto puede tardar unos segundos.

Revisa los datos devueltos por OSCAR/Surface y añade datos faltantes donde sea necesario. Selecciona un tema para la estación y proporciona tu token de autorización para el endpoint `collections/stations` y haz clic en 'guardar':

<img alt="wis2box-webapp-create-station-save" src="/../assets/img/wis2box-webapp-create-station-save.png" width="800">

<img alt="wis2box-webapp-create-station-success" src="/../assets/img/wis2box-webapp-create-station-success.png" width="500">

Regresa a la lista de estaciones y verás la estación que añadiste:

<img alt="wis2box-webapp-stations-with-one-station" src="/../assets/img/wis2box-webapp-stations-with-one-station.png" width="800">

Repite este proceso hasta que tengas al menos 3 estaciones configuradas.

!!! tip "Derivando información de elevación faltante"

    Si falta la elevación de tu estación, hay servicios en línea que ayudan a buscar la elevación usando datos de elevación abiertos. Un ejemplo es la [API de Datos Topográficos Abiertos](https://www.opentopodata.org).

    Por ejemplo, para obtener la elevación en la latitud -6.15558 y longitud 106.84204, puedes copiar y pegar la siguiente URL en una nueva pestaña del navegador:

    ```{.copy}
    https://api.opentopodata.org/v1/aster30m?locations=-6.15558,106.84204
    ```

    Salida:

    ```{.copy}
    {
      "results": [
        {
          "dataset": "aster30m", 
          "elevation": 7.0, 
          "location": {
            "lat": -6.15558, 
            "lng": 106.84204
          }
        }
      ], 
      "status": "OK"
    }
    ```

## Revisar tus metadatos de estación

Los metadatos de la estación están almacenados en el backend de wis2box y están disponibles a través del **wis2box-api**. 

Si abres un navegador y navegas a `http://YOUR-HOST/oapi/collections/stations/items` verás los metadatos de la estación que añadiste:

<img alt="wis2box-api-stations" src="/../assets/img/wis2box-api-stations.png" width="800">

!!! note "Revisar tus metadatos de estación"

    Verifica que las estaciones que añadiste estén asociadas a tu conjunto de datos visitando `http://YOUR-HOST/oapi/collections/stations/items` en tu navegador.

También tienes la opción de ver/actualizar/eliminar la estación en el **wis2box-webapp**. Ten en cuenta que se requiere proporcionar tu token de autorización para el endpoint `collections/stations` para actualizar/eliminar la estación.

!!! note "Actualizar/eliminar metadatos de estación"

    Intenta ver si puedes actualizar/eliminar los metadatos de la estación para una de las estaciones que añadiste usando el **wis2box-webapp**.

## Carga masiva de metadatos de estación

Ten en cuenta que wis2box también tiene la capacidad de realizar la carga "masiva" de metadatos de estación desde un archivo CSV usando la línea de comandos en el contenedor **wis2box-management**.

```bash
python3 wis2box-ctl.py login
wis2box metadata station publish-collection -p /data/wis2box/metadata/station/station_list.csv -th origin/a/wis2/centre-id/weather/surface-based-observations/synop
```

Esto te permite subir un gran número de estaciones a la vez y asociarlas con un tema específico.

Puedes crear el archivo CSV usando Excel o un editor de texto y luego subirlo al wis2box-host-datadir para hacerlo disponible al contenedor **wis2box-management** en el directorio `/data/wis2box/`.

Después de realizar una carga masiva de estaciones, se recomienda revisar las estaciones en el **wis2box-webapp** para asegurarse de que los datos se subieron correctamente.

Consulta la [documentación oficial de wis2box](https://docs.wis2box.wis.wmo.int) para obtener más información sobre cómo usar esta característica.

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica, aprendiste cómo:

    - crear un token de autorización para el endpoint `collections/stations` para usarlo con el **wis2box-webapp**
    - añadir metadatos de estaciones a wis2box usando el **wis2box-webapp**
    - ver/actualizar/eliminar metadatos de estaciones usando el **wis2box-webapp**