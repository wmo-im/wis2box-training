---
title: Configuración de conjuntos de datos en wis2box
---

# Configuración de conjuntos de datos en wis2box

!!! abstract "Resultados de aprendizaje"
    Al final de esta sesión práctica, serás capaz de:

    - Crear nuevos conjuntos de datos utilizando la plantilla predeterminada y tu plantilla personalizada
    - Crear metadatos de descubrimiento para tu conjunto de datos
    - Configurar mapeos de datos para tu conjunto de datos
    - Publicar una notificación WIS2 con un registro WCMP2
    - Actualizar y volver a publicar tu conjunto de datos

## Introducción

wis2box utiliza conjuntos de datos que están asociados con metadatos de descubrimiento y mapeos de datos.

Los metadatos de descubrimiento se utilizan para crear un registro WCMP2 (WMO Core Metadata Profile 2) que se comparte mediante una notificación WIS2 publicada en tu wis2box-broker.

Los mapeos de datos se utilizan para asociar un complemento de datos a tus datos de entrada, permitiendo que tus datos se transformen antes de ser publicados mediante la notificación WIS2.

Esta sesión te guiará a través de la creación de nuevos conjuntos de datos utilizando la plantilla predeterminada y tu plantilla personalizada, la creación de metadatos de descubrimiento y la configuración de mapeos de datos. Inspeccionarás tus conjuntos de datos en el wis2box-api y revisarás la notificación WIS2 para tus metadatos de descubrimiento.

## Preparación

Conéctate a tu broker utilizando MQTT Explorer.

En lugar de usar las credenciales internas de tu broker, utiliza las credenciales públicas `everyone/everyone`:

<img alt="MQTT Explorer: Conectar al broker" src="/../assets/img/mqtt-explorer-wis2box-broker-everyone-everyone.png" width="800">

!!! Nota

    Nunca necesitas compartir las credenciales de tu broker interno con usuarios externos. El usuario 'everyone' es un usuario público para habilitar el intercambio de notificaciones WIS2.

    Las credenciales `everyone/everyone` tienen acceso de solo lectura al tema 'origin/a/wis2/#'. Este es el tema donde se publican las notificaciones WIS2. El Global Broker puede suscribirse con estas credenciales públicas para recibir las notificaciones.
    
    El usuario 'everyone' no verá temas internos ni podrá publicar mensajes.
    
Abre un navegador y accede a la página `http://YOUR-HOST/wis2box-webapp`. Asegúrate de haber iniciado sesión y de poder acceder a la página 'dataset editor'.

Consulta la sección sobre [Inicialización de wis2box](./initializing-wis2box.md) si necesitas recordar cómo conectarte al broker o acceder a wis2box-webapp.

## Crear un token de autorización para processes/wis2box

Necesitarás un token de autorización para el endpoint 'processes/wis2box' para publicar tu conjunto de datos.

Para crear un token de autorización, accede a tu máquina virtual de entrenamiento mediante SSH y utiliza los siguientes comandos para iniciar sesión en el contenedor wis2box-management:

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

Asegúrate de copiar el valor del token y almacenarlo en tu máquina local, ya que lo necesitarás más adelante.

Una vez que tengas tu token, puedes salir del contenedor wis2box-management:

```bash
exit
```

## Creación de nuevos conjuntos de datos en wis2box-webapp

Navega a la página 'dataset editor' en el wis2box-webapp de tu instancia de wis2box accediendo a `http://YOUR-HOST/wis2box-webapp` y seleccionando 'dataset editor' desde el menú en el lado izquierdo.

En la página 'dataset editor', bajo la pestaña 'Datasets', haz clic en "Create New ...":

<img alt="Crear nuevo conjunto de datos" src="/../assets/img/wis2box-create-new-dataset.png" width="800">

Aparecerá una ventana emergente que te pedirá proporcionar:

- **Centre ID**: este es el acrónimo de la agencia (en minúsculas y sin espacios), según lo especificado por el Miembro de la OMM, que identifica el centro de datos responsable de publicar los datos.
- **Template**: La plantilla correspondiente al tipo de datos para los que estás creando metadatos. Puedes elegir entre usar una plantilla predefinida o seleccionar 'other'. Si se selecciona 'other', significa que deseas definir una plantilla personalizada y, por lo tanto, se deben completar manualmente campos adicionales.

<img alt="Ventana emergente para crear nuevo conjunto de datos" src="/../assets/img/wis2box-create-new-dataset-pop-up.png" width="600">

!!! Nota "Centre ID"

    Tu centre-id debe comenzar con el TLD de tu país, seguido de un guion (`-`) y un nombre abreviado de tu organización (por ejemplo, `fr-meteofrance`). El centre-id debe estar en minúsculas y usar solo caracteres alfanuméricos. La lista desplegable muestra todos los centre-ids actualmente registrados en WIS2, así como cualquier centre-id que ya hayas creado en wis2box. Por favor, elige un centre-id apropiado para tu organización.

!!! Nota "Template"

    El campo *Template* te permite seleccionar de una lista de plantillas disponibles en el editor de conjuntos de datos de wis2box-webapp. Una plantilla pre-poblará el formulario con valores predeterminados sugeridos apropiados para el tipo de datos. Esto incluye un título y palabras clave sugeridas para los metadatos y complementos de datos preconfigurados. El tema se establece automáticamente en el tema predeterminado vinculado a la plantilla seleccionada.

    Para el propósito del entrenamiento, trabajaremos con dos opciones al crear nuevos conjuntos de datos:
    
    1. La plantilla predefinida *weather/surface-based-observations/synop*, que incluye complementos de datos que transforman los datos al formato BUFR antes de la publicación;
    2. La plantilla *other*, que te permite definir tu propia plantilla personalizada completando manualmente los campos requeridos.

    Si deseas publicar alertas CAP utilizando wis2box, utiliza la plantilla *weather/advisories-warnings*. Esta plantilla incluye un complemento de datos que verifica que los datos de entrada sean una alerta CAP válida antes de publicarlos. Para crear alertas CAP y publicarlas a través de wis2box, puedes usar el [WMO CAP Composer](https://github.com/World-Meteorological-Organization/cap-composer) o reenviar el XML CAP desde tu propio sistema al bucket wis2box-incoming.

Ahora, vamos a crear un nuevo conjunto de datos utilizando una plantilla predefinida.

## Crear un nuevo conjunto de datos utilizando una plantilla predefinida

Para **Template**, selecciona **weather/surface-based-observations/synop**:

<img alt="Formulario para crear nuevo conjunto de datos: Información inicial" src="/../assets/img/wis2box-create-new-dataset-form-initial.png" width="450">

Haz clic en *continue to form* para continuar, ahora se te presentará el **Formulario del Editor de Conjuntos de Datos**.

Dado que seleccionaste la plantilla **weather/surface-based-observations/synop**, el formulario estará pre-poblado con algunos valores iniciales relacionados con este tipo de datos.

### Creación de metadatos de descubrimiento

El Formulario del Editor de Conjuntos de Datos te permite proporcionar los Metadatos de Descubrimiento para tu conjunto de datos que el contenedor wis2box-management utilizará para publicar un registro WCMP2.

Dado que seleccionaste la plantilla 'weather/surface-based-observations/synop', el formulario estará pre-poblado con algunos valores predeterminados.

Asegúrate de reemplazar el 'Local ID' generado automáticamente con un nombre descriptivo para tu conjunto de datos, por ejemplo, 'synop-dataset-wis2training':

<img alt="Editor de Metadatos: título, descripción, palabras clave" src="/../assets/img/wis2box-metadata-editor-part1.png" width="800">

Revisa el título y las palabras clave, actualízalos según sea necesario y proporciona una descripción para tu conjunto de datos.

Ten en cuenta que hay opciones para cambiar la 'Política de Datos de la OMM' de 'core' a 'recommended' o para modificar tu Identificador de Metadatos predeterminado. Por favor, mantén la política de datos como 'core' y utiliza el Identificador de Metadatos predeterminado.

A continuación, revisa la sección que define tus 'Propiedades Temporales' y 'Propiedades Espaciales'. Puedes ajustar el cuadro delimitador actualizando los campos 'North Latitude', 'South Latitude', 'East Longitude' y 'West Longitude':

<img alt="Editor de Metadatos: propiedades temporales, propiedades espaciales" src="/../assets/img/wis2box-metadata-editor-part2.png" width="800">

Luego, completa la sección que define la 'Información de Contacto del Proveedor de Datos':

<img alt="Editor de Metadatos: información de contacto" src="/../assets/img/wis2box-metadata-editor-part3.png" width="800">

Finalmente, completa la sección que define la 'Información de Calidad de los Datos':

Una vez que hayas completado todas las secciones, haz clic en 'VALIDATE FORM' y verifica el formulario en busca de errores:

<img alt="Editor de Metadatos: validación" src="/../assets/img/wis2box-metadata-validation-error.png" width="800">

Si hay errores, corrígelos y haz clic en 'VALIDATE FORM' nuevamente.

Asegúrate de no tener errores y de recibir una indicación emergente de que tu formulario ha sido validado:

<img alt="Editor de Metadatos: validación exitosa" src="/../assets/img/wis2box-metadata-validation-success.png" width="800">

A continuación, antes de enviar tu conjunto de datos, revisa los mapeos de datos para tu conjunto de datos.

### Configuración de mapeos de datos

Dado que utilizaste una plantilla para crear tu conjunto de datos, los mapeos de datos del conjunto han sido pre-poblados con los complementos predeterminados para la plantilla 'weather/surface-based-observations/synop'. Los complementos de datos se utilizan en wis2box para transformar los datos antes de que se publiquen mediante la notificación WIS2.

<img alt="Mapeos de Datos: actualizar complemento" src="/../assets/img/wis2box-data-mappings.png" width="800">

Nota que puedes hacer clic en el botón "update" para cambiar la configuración del plugin, como la extensión de archivo y el patrón de archivo. Por ahora, puedes dejar la configuración predeterminada. Esto se explicará con más detalle más adelante al crear un conjunto de datos personalizado.

### Enviar tu conjunto de datos

Finalmente, puedes hacer clic en 'submit' para publicar tu conjunto de datos.

Deberás proporcionar el token de autorización para 'processes/wis2box' que creaste anteriormente. Si no lo has hecho, puedes crear un nuevo token siguiendo las instrucciones en la sección de preparación.

Verifica que recibas el siguiente mensaje después de enviar tu conjunto de datos, indicando que el conjunto de datos se envió correctamente:

<img alt="Submit Dataset Success" src="/../assets/img/wis2box-submit-dataset-success.png" width="400">

Después de hacer clic en 'OK', serás redirigido a la página principal del Editor de Conjuntos de Datos. Ahora, si haces clic en la pestaña 'Dataset', deberías ver tu nuevo conjunto de datos listado:

<img alt="Dataset Editor: new dataset" src="/../assets/img/wis2box-dataset-editor-new-dataset.png" width="800">

### Revisar la notificación WIS2 para tus metadatos de descubrimiento

Ve a MQTT Explorer, si estabas conectado al broker, deberías ver una nueva notificación WIS2 publicada en el tema `origin/a/wis2/<your-centre-id>/metadata`:

<img alt="MQTT Explorer: WIS2 notification" src="/../assets/img/mqtt-explorer-wis2-notification-metadata.png" width="800">

Inspecciona el contenido de la notificación WIS2 que publicaste. Deberías ver un JSON con una estructura correspondiente al formato del Mensaje de Notificación WIS (WNM).

!!! question

    ¿En qué tema se publica la notificación WIS2?

??? success "Haz clic para revelar la respuesta"

    La notificación WIS2 se publica en el tema `origin/a/wis2/<your-centre-id>/metadata`.

!!! question
    
    Intenta encontrar el título, la descripción y las palabras clave que proporcionaste en los metadatos de descubrimiento en la notificación WIS2. ¿Puedes encontrarlos?

??? success "Haz clic para revelar la respuesta"

    **¡El título, la descripción y las palabras clave que proporcionaste en los metadatos de descubrimiento no están presentes en el payload de la notificación WIS2!** 
    
    En su lugar, intenta buscar el enlace canónico en la sección "links" de la notificación WIS2:

    <img alt="WIS2 notification for metadata, links sections" src="/../assets/img/wis2-notification-metadata-links.png" width="800">

    **La notificación WIS2 contiene un enlace canónico al registro WCMP2 que se publicó.** 
    
    Copia y pega este enlace canónico en tu navegador para acceder al registro WCMP2. Dependiendo de la configuración de tu navegador, es posible que se te solicite descargar el archivo o que se muestre directamente en tu navegador.

    Encontrarás el título, la descripción y las palabras clave que proporcionaste dentro del registro WCMP2.

wis2box proporciona solo un número limitado de plantillas predefinidas. Estas plantillas están diseñadas para tipos comunes de conjuntos de datos, pero pueden no coincidir siempre con datos especializados. Cuando las plantillas predefinidas no son adecuadas, se puede crear una plantilla personalizada. Esto permite a los usuarios definir los campos de metadatos requeridos según su conjunto de datos.

En la siguiente sección, crearemos un nuevo conjunto de datos y mostraremos cómo configurarlo utilizando una plantilla personalizada.

## Crear un nuevo conjunto de datos configurando tu plantilla personalizada

Para **Template**, selecciona **other**:

<img alt="Create New Dataset Form: Initial information" src="/../assets/img/wis2box-create-new-dataset-form-initial-other.png" width="450">

Haz clic en *continue to form* para continuar, ahora se te presentará el **Formulario del Editor de Conjuntos de Datos**.

Dado que se seleccionó la plantilla *other*, el siguiente paso es hacer clic en *Continue* para proceder. Ahora se te presentará el Formulario del Editor de Conjuntos de Datos. Dentro de este formulario, los campos clave como Título, Descripción, Temas de subdisciplina y Palabras clave deben ser completados o revisados por el usuario. La opción Experimental (tema de texto libre) controla cómo se definen los Temas de subdisciplina: si esta opción está seleccionada, los Temas de subdisciplina pueden ingresarse como texto libre, permitiendo al usuario definir un tema personalizado. Si la opción no está seleccionada, los Temas de subdisciplina se presentan como una lista desplegable, y se debe elegir una de las opciones predefinidas.

### Crear metadatos de descubrimiento personalizados

En esta etapa, deberás completar los campos requeridos en el Formulario del Editor de Conjuntos de Datos, incluyendo Título, Descripción, ID Local, Temas de subdisciplina y Palabras clave.

Para el propósito de este entrenamiento, completaremos estos campos utilizando una plantilla personalizada del conjunto de datos del Sistema Global de Predicción por Conjuntos (GEPS) como ejemplo. Este ejemplo sirve solo como referencia; en operaciones reales de WIS2, los usuarios deben personalizar los campos de metadatos según los requisitos de sus propios conjuntos de datos.

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other.png" width="800">

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other-2.png" width="800">

Los pasos posteriores son los mismos que al crear un conjunto de datos con la plantilla predefinida synop. Para instrucciones detalladas, consulta la sección *Creating discovery metadata* bajo *Create a new dataset by using a predefined template*.

### Configurar mapeos de datos personalizados

Cuando se utiliza una plantilla personalizada, no se proporcionan mapeos de datos predeterminados. Como resultado, el Editor de Mapeos de Conjuntos de Datos estará vacío y los usuarios deberán configurar los mapeos según sus requisitos específicos.

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other1.png" width="800">

En este entrenamiento, personalizaremos un conjunto de datos GEPS y utilizaremos el plugin universal de datos sin conversión como ejemplo. Este plugin está diseñado para publicar datos sin aplicar ninguna transformación. Dado que los datos GEPS se entregan en formato GRIB2, la extensión de archivo debe configurarse como .grib2; de lo contrario, los datos no podrán publicarse correctamente.

Se debe prestar especial atención al campo Regex, ya que afecta directamente la ingesta de datos. Si la expresión regular no coincide con el patrón de nombres de los archivos de datos, se producirán errores de publicación. Para evitar esto, actualiza el regex para que coincida con la convención de nombres de tu conjunto de datos, o deja el regex predeterminado sin cambios y asegúrate de que tus archivos de datos sean renombrados en consecuencia.

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other2.png" width="800">

En operaciones reales de WIS2, los usuarios pueden elegir diferentes plugins dependiendo de sus requisitos; aquí utilizamos el plugin universal de datos sin conversión solo como ejemplo.

Si deseas publicar otros tipos y formatos de datos, puedes hacer clic en el botón "update" para cambiar configuraciones como la extensión de archivo y el patrón de archivo.

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other3.png" width="800">

### Enviar tu conjunto de datos personalizado

El proceso de envío es el mismo que se describe en la sección *Submitting your dataset* bajo *Create a new dataset by using a predefined template*. Consulta esa sección para obtener instrucciones detalladas.

Después de un envío exitoso, tu nuevo conjunto de datos aparecerá en la pestaña Dataset:

<img alt="Dataset Editor: new dataset" src="/../assets/img/wis2box-dataset-editor-new-dataset-other.png" width="800">

### Revisar la notificación WIS2 para tus metadatos de descubrimiento

Ve a MQTT Explorer, si estabas conectado al broker, deberías ver una nueva notificación WIS2 publicada en el tema `origin/a/wis2/<your-centre-id>/metadata`:

<img alt="MQTT Explorer: WIS2 notification" src="/../assets/img/mqtt-explorer-wis2-notification-metadata-other.png" width="800">

!!! question
    
    ¿Cuál es el Identificador de Metadatos del conjunto de datos GEPS personalizado que creaste?

??? success "Haz clic para revelar la respuesta"

    Al abrir la interfaz de usuario de wis2box, puedes ver el conjunto de datos GEPS personalizado. El Identificador de Metadatos es:

    *urn:wmo:md:nl-knmi-test:customized-geps-dataset-wis2-training*

!!! question

    Si modificamos un conjunto de datos, ¿se enviará un nuevo mensaje de notificación de datos? ¿Qué cambios pueden esperarse?

??? success "Haz clic para revelar la respuesta"

    Sí. Se enviará un nuevo mensaje de notificación de datos. En el mensaje, el valor de "rel": "canonical" dentro del elemento "links" cambiará a "rel": "update", indicando que el conjunto de datos ha sido modificado.

!!! question
    
    Si eliminamos un conjunto de datos, ¿se enviará un nuevo mensaje de notificación de datos? ¿Qué cambios pueden esperarse?

??? success "Haz clic para revelar la respuesta"

    Sí. Se enviará un nuevo mensaje de notificación de datos. En el mensaje, el valor de "rel": "canonical" dentro del elemento "links" cambiará a "rel": "deletion", indicando que el conjunto de datos ha sido eliminado.

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica, aprendiste a:

    - Crear nuevos conjuntos de datos utilizando la plantilla predeterminada y tu plantilla personalizada
    - definir tus metadatos de descubrimiento
    - revisar tus mapeos de datos
    - publicar metadatos de descubrimiento
    - revisar la notificación WIS2 para tus metadatos de descubrimiento