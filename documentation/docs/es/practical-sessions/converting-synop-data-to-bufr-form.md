---
title: Conversión de datos SYNOP a BUFR
---

# Conversión de datos SYNOP a BUFR usando la aplicación web wis2box-webapp

!!! abstract "Resultados de aprendizaje"
    Al final de esta sesión práctica, serás capaz de:

    - enviar boletines FM-12 SYNOP válidos a través de la aplicación web wis2box para su conversión a BUFR y su intercambio a través del WIS2.0
    - validar, diagnosticar y corregir errores simples de codificación en un boletín FM-12 SYNOP antes de la conversión de formato e intercambio
    - asegurar que los metadatos de la estación requeridos estén disponibles en wis2box
    - confirmar e inspeccionar los boletines convertidos exitosamente

## Introducción

Para permitir a los observadores manuales enviar datos directamente al WIS2.0, la aplicación web wis2box-webapp tiene un formulario para convertir boletines FM-12 SYNOP a BUFR. El formulario también permite a los usuarios diagnosticar y corregir errores simples de codificación en el boletín FM-12 SYNOP antes de la conversión de formato e intercambio e inspeccionar los datos BUFR resultantes.

## Preparación

!!! warning "Prerrequisitos"

    - Asegúrate de que tu wis2box ha sido configurado y está en funcionamiento.
    - Abre una terminal y conéctate a tu VM de estudiante usando SSH.
    - Conéctate al broker MQTT de tu instancia wis2box usando MQTT Explorer.
    - Abre la aplicación web wis2box (``http://<tu-nombre-de-host>/wis2box-webapp``) y asegúrate de estar conectado.

## Uso de la aplicación web wis2box-webapp para convertir FM-12 SYNOP a BUFR

### Ejercicio 1 - usando la aplicación web wis2box-webapp para convertir FM-12 SYNOP a BUFR

Asegúrate de tener el token de autenticación para "procesos/wis2box" que generaste en el ejercicio anterior y que estás conectado a tu broker wis2box en MQTT Explorer.

Copia el siguiente mensaje:
    
``` {.copy}
AAXX 27031
15015 02999 02501 10103 21090 39765 42952 57020 60001=
``` 

Abre la aplicación web wis2box y navega a la página synop2bufr usando el cajón de navegación izquierdo y procede de la siguiente manera:

- Pega el contenido que has copiado en el cuadro de entrada de texto.
- Selecciona el mes y el año usando el selector de fecha, asume el mes actual para este ejercicio.
- Selecciona un tema del menú desplegable (las opciones se basan en los conjuntos de datos configurados en wis2box).
- Ingresa el token de autenticación "procesos/wis2box" que generaste anteriormente
- Asegúrate de que "Publicar en WIS2" esté activado
- Haz clic en "ENVIAR"

<center><img alt="Diálogo mostrando la página synop2bufr, incluyendo el botón de alternancia" src="../../assets/img/synop2bufr-toggle.png"></center>

Haz clic en enviar. Recibirás un mensaje de advertencia ya que la estación no está registrada en wis2box. Ve al editor de estaciones e importa la siguiente estación:

``` {.copy}
0-20000-0-15015
```

Asegúrate de que la estación esté asociada con el tema que seleccionaste en el paso anterior y luego regresa a la página synop2bufr y repite el proceso con los mismos datos que antes.

!!! question
    ¿Cómo puedes ver el resultado de la conversión de FM-12 SYNOP a BUFR?

??? success "Haz clic para revelar la respuesta"
    La sección de resultados de la página muestra Advertencias, Errores y archivos BUFR de salida.

    Haz clic en "Archivos BUFR de salida" para ver una lista de los archivos que se han generado. Deberías ver un archivo listado.

    El botón de descarga permite que los datos BUFR se descarguen directamente a tu computadora.

    El botón de inspección ejecuta un proceso para convertir y extraer los datos de BUFR.

    <center><img alt="Diálogo mostrando el resultado de enviar un mensaje exitosamente"
         src="../../assets/img/synop2bufr-ex2-success.png"></center>

!!! question
    Los datos de entrada FM-12 SYNOP no incluían la ubicación de la estación, la elevación o la altura del barómetro.
    Confirma que estos están en los datos BUFR de salida, ¿de dónde provienen?

??? success "Haz clic para revelar la respuesta"
    Hacer clic en el botón de inspección debería mostrar un diálogo como el que se muestra a continuación.

    <center><img alt="Resultados del botón de inspección mostrando los metadatos básicos de la estación, la ubicación de la estación y las propiedades observadas"
         src="../../assets/img/synop2bufr-ex2.png"></center>

    Esto incluye la ubicación de la estación mostrada en un mapa y metadatos básicos, así como las observaciones en el mensaje.
    
    Como parte de la transformación de FM-12 SYNOP a BUFR, se agregaron metadatos adicionales al archivo BUFR.
    
    El archivo BUFR también puede ser inspeccionado descargando el archivo y validándolo usando una herramienta como el validador BUFR de ECMWF ecCodes.

Ve a MQTT Explorer y verifica el tema de notificaciones WIS2 para ver las notificaciones WIS2 que se han publicado.

### Ejercicio 2 - entendiendo la lista de estaciones

Para este próximo ejercicio convertirás un archivo que contiene múltiples informes, mira los datos a continuación:

``` {.copy}
AAXX 27031
15015 02999 02501 10103 21090 39765 42952 57020 60001=
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
```

!!! question
    Basado en el ejercicio anterior, observa el mensaje FM-12 SYNOP y predice cuántos mensajes BUFR
    serán generados.
    
    Ahora copia y pega este mensaje en el formulario SYNOP y envía los datos.

    ¿El número de mensajes generados coincidió con tu expectativa y si no, por qué no?

??? warning "Haz clic para revelar la respuesta"
    
    Podrías haber esperado que se generaran tres mensajes BUFR, uno para cada informe meteorológico. Sin embargo, en lugar de eso, recibiste 2 advertencias y solo un archivo BUFR.
    
    Para que un informe meteorológico se convierta a BUFR, se requieren los metadatos básicos contenidos en la lista de estaciones. Aunque el ejemplo anterior incluye tres informes meteorológicos, dos de las
    tres estaciones que informaron no estaban registradas en tu wis2box.
    
    Como resultado, solo uno de los tres informes meteorológicos resultó en un archivo BUFR generado y una notificación WIS2 publicada. Los otros dos informes meteorológicos fueron ignorados y se generaron advertencias.

!!! hint
    Toma nota de la relación entre el Identificador WIGOS y el identificador de estación tradicional incluido en la salida BUFR. En muchos casos, para estaciones listadas en el Volumen A del WMO-No. 9 en el momento de migrar a identificadores de estación WIGOS, el identificador de estación WIGOS se da por el identificador de estación tradicional con ``0-20000-0`` antepuesto,
    por ejemplo, ``15015`` se ha convertido en ``0-20000-0-15015``.

Usando la página de lista de estaciones, importa las siguientes estaciones:

``` {.copy}
0-20000-0-15020
0-20000-0-15090
```

Asegúrate de que las estaciones estén asociadas con el tema que seleccionaste en el ejercicio anterior y luego regresa a la página synop2bufr y repite el proceso.

Ahora se deberían generar tres archivos BUFR y no debería haber advertencias ni errores listados en la aplicación web.

Además de la información básica de la estación, se requieren metadatos adicionales como la elevación de la estación sobre el nivel del mar y la altura del barómetro sobre el nivel del mar para la codificación a BUFR. Los campos están incluidos en las páginas de lista de estaciones y editor de estaciones.
    
### Ejercicio 3 - depuración

En este último ejercicio identificarás y corregirás dos de los problemas más comunes encontrados al
usar esta herramienta para convertir FM-12 SYNOP a BUFR.

El ejemplo de datos se muestra en el cuadro a continuación, examina los datos e intenta resolver cualquier problema que pueda haber antes de enviar los datos a través de la aplicación web.

!!! hint
    Puedes editar los datos en el cuadro de entrada en la página de la aplicación web. Si te pierdes algún problema, estos deberían ser detectados y resaltados como una advertencia o error una vez que se haya hecho clic en el botón de enviar.

``` {.copy}
AAXX 27031
15015 02999 02501 10103 21090 39765 42952 57020 60001
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
```

!!! question
    ¿Qué problemas esperabas encontrar al convertir los datos a BUFR y cómo los superaste? ¿Hubo algún problema que no esperabas?

??? success "Haz clic para revelar la respuesta"
    En este primer ejemplo falta el símbolo de "fin de texto" (=), o delimitador de registro, entre el
    primer y segundo informe meteorológico. En consecuencia, las líneas 2 y 3 se tratan como un solo informe,
    lo que lleva a errores en el análisis del mensaje.

El segundo ejemplo a continuación contiene varios problemas comunes encontrados en los informes FM-12 SYNOP. Examina los
datos e intenta identificar los problemas y luego envía los datos corregidos a través de la aplicación web.

```{.copy}
AAXX 27031
15020 02997 23104 10/30 21075 30177 40377 580200 60001 81041=
```

!!! question
    ¿Qué problemas encontraste y cómo los resolviste?

??? success "Haz clic para revelar la respuesta"
    Hay dos problemas en el informe meteorológico.
    
    El primero, en el grupo de temperatura del aire firmada, tiene el carácter de las decenas establecido como ausente (/),
    lo que lleva a un grupo inválido. En este ejemplo sabemos que la temperatura es de 13.0 grados
    Celsius (de los ejemplos anteriores) y por lo tanto este problema puede ser corregido. Operacionalmente, el
    valor correcto necesitaría ser confirmado con el observador.

    El segundo problema ocurre en el grupo 5 donde hay un carácter adicional, con el carácter final duplicado. Este problema puede ser solucionado eliminando el carácter extra.

## Limpieza

Durante los ejercicios en esta sesión habrás importado varios archivos en tu lista de estaciones. Navega a la
página de lista de estaciones y haz clic en los iconos de basura para eliminar las estaciones. Puede que necesites actualizar la página para que las estaciones se eliminen de la lista después de borrar.

<center><img alt="Visor de metadatos de estación"
         src="../../assets/img/synop2bufr-trash.png" width="600"></center>

## Conclusión

!!! success "¡Felicidades!"

    En esta sesión práctica, aprendiste:

    - cómo se puede usar la herramienta synop2bufr para convertir informes FM-12 SYNOP a BUFR;
    - cómo enviar un informe FM-12 SYNOP a través de la aplicación web;
    - cómo diagnosticar y corregir errores simples en un informe FM-12 SYNOP;
    - la importancia de registrar estaciones en wis2box (y OSCAR/Surface);
    - y el uso del botón de inspección para ver el contenido de los datos BUFR.