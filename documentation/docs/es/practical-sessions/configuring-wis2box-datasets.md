---
title: Configuración de conjuntos de datos en wis2box
---

# Configuración de conjuntos de datos en wis2box

!!! abstract "Objetivos de aprendizaje"
    Al finalizar esta sesión práctica, podrás:

    - crear un nuevo conjunto de datos
    - crear metadatos de descubrimiento para un conjunto de datos
    - configurar mapeos de datos para un conjunto de datos
    - publicar una notificación WIS2 con un registro WCMP2
    - actualizar y volver a publicar tu conjunto de datos

## Introducción

wis2box utiliza conjuntos de datos que están asociados con metadatos de descubrimiento y mapeos de datos.

Los metadatos de descubrimiento se utilizan para crear un registro WCMP2 (WMO Core Metadata Profile 2) que se comparte mediante una notificación WIS2 publicada en tu wis2box-broker.

Los mapeos de datos se utilizan para asociar un complemento de datos a tus datos de entrada, permitiendo que tus datos sean transformados antes de ser publicados mediante la notificación WIS2.

Esta sesión te guiará a través de la creación de un nuevo conjunto de datos, la creación de metadatos de descubrimiento y la configuración de mapeos de datos. Examinarás tu conjunto de datos en el wis2box-api y revisarás la notificación WIS2 para tus metadatos de descubrimiento.

## Preparación

Conéctate a tu broker utilizando MQTT Explorer.

En lugar de usar tus credenciales internas del broker, utiliza las credenciales públicas `everyone/everyone`:

<img alt="MQTT Explorer: Connect to broker" src="../../assets/img/mqtt-explorer-wis2box-broker-everyone-everyone.png" width="800">

!!! Note

    Nunca necesitas compartir las credenciales de tu broker interno con usuarios externos. El usuario 'everyone' es un usuario público para permitir compartir notificaciones WIS2.

    Las credenciales `everyone/everyone` tienen acceso de solo lectura en el tema 'origin/a/wis2/#'. Este es el tema donde se publican las notificaciones WIS2. El Global Broker puede suscribirse con estas credenciales públicas para recibir las notificaciones.
    
    El usuario 'everyone' no verá temas internos ni podrá publicar mensajes.

Abre un navegador y accede a la página `http://YOUR-HOST/wis2box-webapp`. Asegúrate de haber iniciado sesión y poder acceder a la página 'dataset editor'.

Consulta la sección sobre [Inicialización de wis2box](/practical-sessions/initializing-wis2box) si necesitas recordar cómo conectarte al broker o acceder al wis2box-webapp.

## Crear un token de autorización para processes/wis2box

Necesitarás un token de autorización para el endpoint 'processes/wis2box' para publicar tu conjunto de datos.

Para crear un token de autorización, accede a tu VM de entrenamiento por SSH y usa los siguientes comandos para iniciar sesión en el contenedor wis2box-management:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Luego ejecuta el siguiente comando para crear un token de autorización generado aleatoriamente para el endpoint 'processes/wis2box':

```bash
wis2box auth add-token --path processes/wis2box
```

También puedes crear un token con un valor específico proporcionando el token como argumento al comando:

```bash
wis2box auth add-token --path processes/wis2box MyS3cretToken
```

Asegúrate de copiar el valor del token y guardarlo en tu máquina local, ya que lo necesitarás más tarde.

Una vez que tengas tu token, puedes salir del contenedor wis2box-management:

```bash
exit
```

## Creación de un nuevo conjunto de datos en wis2box-webapp

Navega a la página 'dataset editor' en el wis2box-webapp de tu instancia wis2box yendo a `http://YOUR-HOST/wis2box-webapp` y seleccionando 'dataset editor' del menú en el lado izquierdo.

En la página 'dataset editor', bajo la pestaña 'Datasets', haz clic en "Create New ...":

<img alt="Create New Dataset" src="../../assets/img/wis2box-create-new-dataset.png" width="800">

Aparecerá una ventana emergente solicitando que proporciones:

- **Centre ID**: este es el acrónimo de la agencia (en minúsculas y sin espacios), según lo especificado por el Miembro de la OMM, que identifica el centro de datos responsable de publicar los datos.
- **Data Type**: El tipo de datos para los que estás creando metadatos. Puedes elegir entre usar una plantilla predefinida o seleccionar 'other'. Si seleccionas 'other', tendrás que completar más campos manualmente.

!!! Note "Centre ID"

    Tu centre-id debe comenzar con el TLD de tu país, seguido de un guión (`-`) y un nombre abreviado de tu organización (por ejemplo `fr-meteofrance`). El centre-id debe estar en minúsculas y usar solo caracteres alfanuméricos. La lista desplegable muestra todos los centre-ids actualmente registrados en WIS2, así como cualquier centre-id que ya hayas creado en wis2box.

!!! Note "Data Type Templates"

    El campo *Data Type* te permite seleccionar de una lista de plantillas disponibles en el editor de conjuntos de datos de wis2box-webapp. Una plantilla prellenará el formulario con valores predeterminados sugeridos apropiados para el tipo de datos. Esto incluye título y palabras clave sugeridas para los metadatos y complementos de datos preconfigurados. El tema se fijará al tema predeterminado para el tipo de datos.

    Para el propósito del entrenamiento, usaremos el tipo de datos *weather/surface-based-observations/synop* que incluye complementos de datos que aseguran que los datos se transformen al formato BUFR antes de ser publicados.

    Si deseas publicar alertas CAP usando wis2box, usa la plantilla *weather/advisories-warnings*. Esta plantilla incluye un complemento de datos que verifica que los datos de entrada sean una alerta CAP válida antes de publicar. Para crear alertas CAP y publicarlas a través de wis2box puedes usar [CAP Composer](https://github.com/wmo-raf/cap-composer).

Por favor, elige un centre-id apropiado para tu organización.

Para **Data Type**, selecciona **weather/surface-based-observations/synop**:

<img alt="Create New Dataset Form: Initial information" src="../../assets/img/wis2box-create-new-dataset-form-initial.png" width="450">

Haz clic en *continue to form* para continuar, ahora se te presentará el **Dataset Editor Form**.

Ya que seleccionaste el tipo de datos **weather/surface-based-observations/synop**, el formulario estará prellenado con algunos valores iniciales relacionados con este tipo de datos.

## Creación de metadatos de descubrimiento

El Formulario del Editor de Conjuntos de Datos te permite proporcionar los Metadatos de Descubrimiento para tu conjunto de datos que el contenedor wis2box-management utilizará para publicar un registro WCMP2.

Ya que has seleccionado el tipo de datos 'weather/surface-based-observations/synop', el formulario estará prellenado con algunos valores predeterminados.

Por favor, asegúrate de reemplazar el 'Local ID' autogenerado con un nombre descriptivo para tu conjunto de datos, por ejemplo 'synop-dataset-wis2training':

<img alt="Metadata Editor: title, description, keywords" src="../../assets/img/wis2box-metadata-editor-part1.png" width="800">

Revisa el título y las palabras clave, actualízalos según sea necesario, y proporciona una descripción para tu conjunto de datos.

Ten en cuenta que hay opciones para cambiar la 'WMO Data Policy' de 'core' a 'recommended' o para modificar tu Identificador de Metadatos predeterminado, por favor mantén data-policy como 'core' y usa el Identificador de Metadatos predeterminado.

A continuación, revisa la sección que define tus 'Temporal Properties' y 'Spatial Properties'. Puedes ajustar el cuadro delimitador actualizando los campos 'North Latitude', 'South Latitude', 'East Longitude' y 'West Longitude':

<img alt="Metadata Editor: temporal properties, spatial properties" src="../../assets/img/wis2box-metadata-editor-part2.png" width="800">

Luego, completa la sección que define la 'Contact Information of the Data Provider':

<img alt="Metadata Editor: contact information" src="../../assets/img/wis2box-metadata-editor-part3.png" width="800">

Finalmente, completa la sección que define la 'Data Quality Information':

Una vez que hayas completado todas las secciones, haz clic en 'VALIDATE FORM' y verifica si hay errores en el formulario:

<img alt="Metadata Editor: validation" src="../../assets/img/wis2box-metadata-validation-error.png" width="800">

Si hay errores, corrígelos y haz clic en 'VALIDATE FORM' nuevamente.

Asegúrate de no tener errores y de recibir una ventana emergente indicando que tu formulario ha sido validado:

<img alt="Metadata Editor: validation success" src="../../assets/img/wis2box-metadata-validation-success.png" width="800">

A continuación, antes de enviar tu conjunto de datos, revisa los mapeos de datos para tu conjunto de datos.

## Configuración de mapeos de datos

Ya que usaste una plantilla para crear tu conjunto de datos, los mapeos del conjunto de datos han sido prellenados con los complementos predeterminados para el tipo de datos 'weather/surface-based-observations/synop'. Los complementos de datos se utilizan en el wis2box para transformar datos antes de que sean publicados usando la notificación WIS2.

<img alt="Data Mappings: update plugin" src="../../assets/img/wis2box-data-mappings.png" width="800">

Ten en cuenta que puedes hacer clic en el botón "update" para cambiar la configuración del complemento, como la extensión del archivo y el patrón del archivo; puedes dejar la configuración predeterminada por ahora. En una sesión posterior, aprenderás más sobre BUFR y la transformación de datos al formato BUFR.

## Envío de tu conjunto de datos

Finalmente, puedes hacer clic en 'submit' para publicar tu conjunto de datos.

Necesitarás proporcionar el token de autorización para 'processes/wis2box' que creaste anteriormente. Si no lo has hecho, puedes crear un nuevo token siguiendo las instrucciones en la sección de preparación.

Verifica que recibas el siguiente mensaje después de enviar tu conjunto de datos, indicando que el conjunto de datos se envió exitosamente:

<img alt="Submit Dataset Success" src="../../assets/img/wis2box-submit-dataset-success.png" width="400">

Después de hacer clic en 'OK', serás redirigido a la página principal del Editor de Conjuntos de Datos. Ahora, si haces clic en la pestaña 'Dataset', deberías ver tu nuevo conjunto de datos listado:

<img alt="Dataset Editor: new dataset" src="../../assets/img/wis2box-dataset-editor-new-dataset.png" width="800">

## Revisión de la notificación WIS2 para tus metadatos de descubrimiento

Ve a MQTT Explorer, si estabas conectado al broker, deberías ver una nueva notificación WIS2 publicada en el tema `origin/a/wis2/<your-centre-id>/metadata`:

<img alt="MQTT Explorer: WIS2 notification" src="../../assets/img/mqtt-explorer-wis2-notification-metadata.png" width="800">

Inspecciona el contenido de la notificación WIS2 que publicaste. Deberías ver un JSON con una estructura correspondiente al formato de Mensaje de Notificación WIS (WNM).

!!! question

    ¿En qué tema se publica la notificación WIS2?

??? success "Haz clic para revelar la respuesta"

    La notificación WIS2 se publica en el tema `origin/a/wis2/<your-centre-id>/metadata`.

!!! question
    
    Intenta encontrar el título, la descripción y las palabras clave que proporcionaste en los metadatos de descubrimiento en la notificación WIS2. ¿Puedes encontrarlos?

??? success "Haz clic para revelar la respuesta"

    **¡El título, la descripción y las palabras clave que proporcionaste en los metadatos de descubrimiento no están presentes en la carga útil de la notificación WIS2!**
    
    En su lugar, intenta buscar el enlace canónico en la sección "links" en la notificación WIS2:

    <img alt="WIS2 notification for metadata, links sections" src="../../assets/img/wis2-notification-metadata-links.png" width="800">

    **La notificación WIS2 contiene un enlace canónico al registro WCMP2 que fue publicado.**
    
    Copia y pega este enlace canónico en tu navegador para acceder al registro WCMP2, dependiendo de la configuración de tu navegador, es posible que se te solicite descargar el archivo o que se muestre directamente en tu navegador.

    Encontrarás el título, la descripción y las palabras clave que proporcionaste dentro del registro WCMP2.

## Conclusión

!!! success "¡Felicitaciones!"
    En esta sesión práctica, aprendiste cómo:

    - crear un nuevo conjunto de datos
    - definir tus metadatos de descubrimiento
    - revisar tus mapeos de datos
    - publicar metadatos de descubrimiento
    - revisar la notificación WIS2 para tus metadatos de descubrimiento