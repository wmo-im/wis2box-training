---
title: Trabajando con datos BUFR
---

# Trabajando con datos BUFR

!!! abstract "Resultados de aprendizaje"
    En esta sesión práctica se te introducirá a algunas de las herramientas BUFR incluidas en el contenedor **wis2box-api** que se utilizan para transformar datos al formato BUFR y para leer el contenido codificado en BUFR.
    
    Aprenderás:

    - cómo inspeccionar los encabezados en el archivo BUFR usando el comando `bufr_ls`
    - cómo extraer e inspeccionar los datos dentro de un archivo bufr usando `bufr_dump`
    - la estructura básica de las plantillas bufr utilizadas en csv2bufr y cómo usar la herramienta de línea de comandos
    - y cómo hacer cambios básicos a las plantillas bufr y cómo actualizar el wis2box para usar la versión revisada

## Introducción

Los complementos que producen notificaciones con datos BUFR utilizan procesos en el wis2box-api para trabajar con datos BUFR, por ejemplo para transformar los datos de CSV a BUFR o de BUFR a geojson.

El contenedor wis2box-api incluye varias herramientas para trabajar con datos BUFR.

Estas incluyen las herramientas desarrolladas por ECMWF e incluidas en el software ecCodes, más información sobre estas se puede encontrar en el [sitio web de ecCodes](https://confluence.ecmwf.int/display/ECC/BUFR+tools).

En esta sesión se te introducirá a los comandos `bufr_ls` y `bufr_dump` del paquete de software ecCodes y a la configuración avanzada de la herramienta csv2bufr.

## Preparación

Para usar las herramientas de línea de comandos BUFR necesitarás estar conectado al contenedor wis2box-api y a menos que se especifique lo contrario todos los comandos deben ejecutarse en este contenedor. También necesitarás tener MQTT Explorer abierto y conectado a tu broker.

Primero conéctate a tu VM de estudiante a través de tu cliente ssh y luego inicia sesión en el contenedor wis2box-api:

```{.copy}
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login wis2box-api
```

Confirma que las herramientas están disponibles, comenzando con ecCodes:

``` {.copy}
bufr_dump -V
```
Deberías obtener la siguiente respuesta:

```
ecCodes Version 2.28.0
```

Luego verifica csv2bufr:

```{.copy}
csv2bufr --version
```

Deberías obtener la siguiente respuesta:

```
csv2bufr, versión 0.7.4
```

Finalmente, crea un directorio de trabajo para trabajar en él:

```{.copy}
cd /data/wis2box
mkdir -p working/bufr-cli
cd working/bufr-cli
```

Ahora estás listo para comenzar a usar las herramientas BUFR.

## Uso de las herramientas de línea de comandos BUFR

### Ejercicio 1 - bufr_ls
En este primer ejercicio usarás el comando `bufr_ls` para inspeccionar los encabezados de un archivo BUFR y determinar el contenido del archivo. Los siguientes encabezados están incluidos en un archivo BUFR:

| encabezado                            | clave de ecCodes                  | descripción                                                                                                                                           |
|-----------------------------------|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| centro originador/generador     | centre                       | El centro originador / generador de los datos                                                                                                      |
| subcentro originador/generador | bufrHeaderSubCentre          | El subcentro originador / generador de los datos                                                                                                  | 
| Número de secuencia de actualización            | updateSequenceNumber         | Si esta es la primera versión de los datos (0) o una actualización (>0)                                                                                   |               
| Categoría de datos                     | dataCategory                 | El tipo de datos contenidos en el mensaje BUFR, por ejemplo, datos de superficie. Ver [Tabla A de BUFR](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)  |
| Subcategoría de datos internacionales   | internationalDataSubCategory | El subtipo de datos contenidos en el mensaje BUFR, por ejemplo, datos de superficie. Ver [Tabla de Códigos Comunes C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) |
| Año                              | typicalYear (typicalDate)    | El tiempo más típico para los contenidos del mensaje BUFR                                                                                                       |
| Mes                             | typicalMonth (typicalDate)   | El tiempo más típico para los contenidos del mensaje BUFR                                                                                                       |
| Día                               | typicalDay (typicalDate)     | El tiempo más típico para los contenidos del mensaje BUFR                                                                                                       |
| Hora                              | typicalHour (typicalTime)    | El tiempo más típico para los contenidos del mensaje BUFR                                                                                                       |
| Minuto                            | typicalMinute (typicalTime)  | El tiempo más típico para los contenidos del mensaje BUFR                                                                                                       |
| Descriptores BUFR                  | unexpandedDescriptors        | Lista de uno o más descriptores BUFR que definen los datos contenidos en el archivo                                                                        |

Descarga el archivo de ejemplo directamente en el contenedor de gestión de wis2box usando el siguiente comando:

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex1.bufr4 --output bufr-cli-ex1.bufr4
```

Ahora usa el siguiente comando para ejecutar `bufr_ls` en este archivo:

```bash
bufr_ls bufr-cli-ex1.bufr4
```

Deberías ver la siguiente salida:

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 of 1 messages in bufr-cli-ex1.bufr4

1 of 1 total messages in 1 files
```

Por sí sola, esta información no es muy informativa, ya que solo proporciona información limitada sobre el contenido del archivo.

La salida predeterminada no proporciona información sobre el tipo de observación o datos y está en un formato que no es muy fácil de leer. Sin embargo, se pueden pasar varias opciones a `bufr_ls` para cambiar tanto el formato como los campos de encabezado impresos.

Usa `bufr_ls` sin ningún argumento para ver las opciones:

```{.copy}
bufr_ls
```

Deberías ver la siguiente salida:

```
NAME    bufr_ls

DESCRIPTION
        List content of BUFR files printing values of some header keys.
        Only scalar keys can be printed.
        It does not fail when a key is not found.

USAGE
        bufr_ls [options] bufr_file bufr_file ...

OPTIONS
        -p key[:{s|d|i}],key[:{s|d|i}],...
                Declaration of keys to print.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be requested. Default type is string.
        -F format
                C style format for floating-point values.
        -P key[:{s|d|i}],key[:{s|d|i}],...
                As -p adding the declared keys to the default list.
        -w key[:{s|d|i}]{=|!=}value,key[:{s|d|i}]{=|!=}value,...
                Where clause.
                Messages are processed only if they match all the key/value constraints.
                A valid constraint is of type key=value or key!=value.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be specified. Default type is string.
                In the value you can also use the forward-slash character '/' to specify an OR condition (i.e. a logical disjunction)
                Note: only one -w clause is allowed.
        -j      JSON output
        -s key[:{s|d|i}]=value,key[:{s|d|i}]=value,...
                Key/values to set.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be defined. By default the native type is set.
        -n namespace
                All the keys belonging to the given namespace are printed.
        -m      Mars keys are printed.
        -V      Version.
        -W width
                Minimum width of each column in output. Default is 10.
        -g      Copy GTS header.
        -7      Does not fail when the message has wrong length

SEE ALSO
        Full documentation and examples at:
        <https://confluence.ecmwf.int/display/ECC/bufr_ls>
```

Ahora ejecuta el mismo comando en el archivo de ejemplo pero muestra la información en formato JSON.

!!! question
    ¿Qué bandera pasas al comando `bufr_ls` para ver la salida en formato JSON?

??? success "Haz clic para revelar la respuesta"
    Puedes cambiar el formato de salida a json usando la bandera `-j`, es decir,
    `bufr_ls -j <archivo-de-entrada>`. Esto puede ser más legible que el formato de salida predeterminado. Vea el ejemplo de salida a continuación:

    ```
    { "messages" : [
      {
        "centre": "cnmc",
        "masterTablesVersionNumber": 29,
        "localTablesVersionNumber": 0,
        "typicalDate": 20231002,
        "typicalTime": "000000",
        "numberOfSubsets": 1
      }
    ]}
    ```

Al examinar un archivo BUFR, a menudo queremos determinar el tipo de datos contenidos en el archivo y la fecha/hora típica de los datos en el archivo. Esta información se puede listar usando la bandera `-p` para seleccionar los encabezados a mostrar. Se pueden incluir múltiples encabezados usando una lista separada por comas.

Usando el comando `bufr_ls`, inspecciona el archivo de prueba e identifica el tipo de datos contenidos en el archivo y la fecha y hora típicas para esos datos.

??? hint
    Las claves ecCodes están dadas en la tabla anterior. Podemos usar lo siguiente para listar la dataCategory y
    internationalDataSubCategory de los datos BUFR:

    ```
    bufr_ls -p dataCategory,internationalDataSubCategory bufr-cli-ex1.bufr4
    ```

    Se pueden agregar claves adicionales según sea necesario.

!!! question
    ¿Qué tipo de datos (categoría de datos y subcategoría) están contenidos en el archivo? ¿Cuál es la fecha y hora típicas para los datos?

??? success "Haz clic para revelar la respuesta"
    El comando que necesitabas ejecutar debería haber sido similar a:
    
    ```
    bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
    ```

    Es posible que hayas agregado claves adicionales o listado el año, mes, día, etc. individualmente. La salida debería
    ser similar a la siguiente, dependiendo de si seleccionaste la salida JSON o la predeterminada.

    ```
    { "messages" : [
      {
        "dataCategory": 2,
        "internationalDataSubCategory": 4,
        "typicalDate": 20231002,
        "typicalTime": "000000"
      }
    ]}
    ```

    De esto vemos que:

    - La categoría de datos es 2, de [Tabla A de BUFR](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)
      podemos ver que este archivo contiene datos de "sondeos verticales (otros que no son de satélite)".
    - La subcategoría internacional es 4, indicando
      "informes de temperatura/humedad/viento de nivel superior de estaciones terrestres fijas (TEMP)" datos. Esta información se puede buscar
      en [Tabla de Códigos Comunes C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) (fila 33). Nota la combinación
      de categoría y subcategoría.
    - La fecha y hora típicas son 2023/10/02 y 00:00:00z respectivamente.

    

### Ejercicio 2 - bufr_dump

El comando `bufr_dump` se puede usar para listar y examinar los contenidos de un archivo BUFR, incluidos los datos en sí.

En este ejercicio usaremos un archivo BUFR que es el mismo que creaste durante la sesión práctica inicial de csv2bufr usando el wis2box-webapp.

Descarga el archivo de muestra al contenedor de gestión de wis2box directamente con el siguiente comando:

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex2.bufr4 --output bufr-cli-ex2.bufr4
```

Ahora ejecuta el comando `bufr_dump` en el archivo, usando la bandera `-p` para mostrar los datos en texto plano (formato clave=valor):

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

Deberías ver alrededor de 240 claves en la salida, muchas de las cuales están ausentes. Esto es típico con datos del mundo real ya que no todas las claves de eccodes están pobladas con datos reportados.

!!! hint
    Los valores faltantes se pueden filtrar usando herramientas como `grep`:
    ```{.copy}
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
    ```

El archivo BUFR de ejemplo para este ejercicio proviene de la sesión práctica de csv2bufr. Por favor, descarga el archivo CSV original en tu ubicación actual de la siguiente manera:

```{.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/csv2bufr-ex1.csv --output csv2bufr-ex1.csv
```

Y muestra el contenido del archivo con:

```{.copy}
more csv2bufr-ex1.csv
```

!!! question
    Usa el siguiente comando para mostrar la columna 18 en el archivo CSV y encontrarás la presión media del nivel del mar reportada (msl_pressure):

    ```{.copy}
    more csv2bufr-ex1.csv | cut -d ',' -f 18
    ```
    
    ¿Qué clave en la salida BUFR corresponde a la presión media del nivel del mar?

??? hint
    Herramientas como `grep` se pueden usar en combinación con `bufr_dump`. Por ejemplo:
    
    ```{.copy}
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i "pressure"
    ```
    
    filtraría los contenidos de `bufr_dump` solo a esas líneas que contienen la palabra presión. Alternativamente,
    la salida podría filtrarse en un valor.

??? success "Haz clic para revelar la respuesta"
    La clave "pressureReducedToMeanSeaLevel" corresponde a la columna msl_pressure en el archivo CSV de entrada.

Pasa unos minutos examinando el resto de la salida, comparándola con el archivo CSV de entrada antes de pasar al siguiente
ejercicio. Por ejemplo, puedes intentar encontrar las claves en la salida BUFR que corresponden a la humedad relativa (columna 23 en el archivo CSV) y la temperatura del aire (columna 21 en el archivo CSV).

### Ejercicio 3 - archivos de mapeo csv2bufr

La herramienta csv2bufr se puede configurar para procesar datos tabulares con diferentes columnas y secuencias BUFR.

Esto se hace mediante un archivo de configuración escrito en formato JSON.

Al igual que los datos BUFR en sí, el archivo JSON contiene una sección de encabezado y una sección de datos, que corresponden ampliamente a las mismas secciones en BUFR.

Además, algunas opciones de formato se especifican dentro del archivo JSON.

El archivo JSON para el mapeo predeterminado se puede ver a través del enlace a continuación (haz clic derecho y abre en una nueva pestaña):

[aws-template.json](https://raw.githubusercontent.com/wmo-im/csv2bufr/main/csv2bufr/templates/resources/aws-template.json)

Examina la sección `header` del archivo de mapeo (mostrada a continuación) y compárala con la tabla del ejercicio 1 (columna de clave ecCodes):

```
"header":[
    {"eccodes_key": "edition", "value": "const:4"},
    {"eccodes_key": "masterTableNumber", "value": "const:0"},
    {"eccodes_key": "bufrHeaderCentre", "value": "const:0"},
    {"eccodes_key": "bufrHeaderSubCentre", "value": "const:0"},
    {"eccodes_key": "updateSequenceNumber", "value": "const:0"},
    {"eccodes_key": "dataCategory", "value": "const:0"},
    {"eccodes_key": "internationalDataSubCategory", "value": "const:2"},
    {"eccodes_key": "masterTablesVersionNumber", "value": "const:30"},
    {"eccodes_key": "numberOfSubsets", "value": "const:1"},
    {"eccodes_key": "observedData", "value": "const:1"},
    {"eccodes_key": "compressedData", "value": "const:0"},
    {"eccodes_key": "typicalYear", "value": "data:year"},
    {"eccodes_key": "typicalMonth", "value": "data:month"},
    {"eccodes_key": "typicalDay", "value": "data:day"},
    {"eccodes_key": "typicalHour", "value": "data:hour"},
    {"eccodes_key": "typicalMinute", "value": "data:minute"},
    {"eccodes_key": "unexpandedDescriptors", "value":"array:301150, 307096"}
],
```

Aquí puedes ver los mismos encabezados que están disponibles en la salida del