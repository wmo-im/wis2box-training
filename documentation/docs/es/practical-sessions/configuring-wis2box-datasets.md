---
title: Configuración de conjuntos de datos en wis2box
---

# Configuración de conjuntos de datos en wis2box

!!! abstract "Resultados de aprendizaje"
    Al final de esta sesión práctica, podrás:

    - usar el editor de conjuntos de datos de wis2box-webapp
    - crear nuevos conjuntos de datos utilizando las plantillas *weather/surface-based-observations/synop* y *other*
    - definir tus metadatos de descubrimiento
    - revisar tus mapeos de datos
    - publicar una notificación WIS2 para tus metadatos de descubrimiento

## Introducción

wis2box utiliza conjuntos de datos que están asociados con metadatos de descubrimiento y mapeos de datos.

Los metadatos de descubrimiento se utilizan para crear un registro WCMP2 (WMO Core Metadata Profile 2) que se comparte mediante una notificación WIS2 publicada en tu wis2box-broker.

Los mapeos de datos se utilizan para asociar un complemento de datos con tus datos de entrada, permitiendo que tus datos se transformen antes de ser publicados mediante la notificación WIS2.

Esta sesión te guiará en la creación de nuevos conjuntos de datos utilizando la plantilla predeterminada y tu plantilla personalizada, en la creación de metadatos de descubrimiento y en la configuración de mapeos de datos. Inspeccionarás tus conjuntos de datos en wis2box-api y revisarás la notificación WIS2 para tus metadatos de descubrimiento.

## Preparación

Conéctate a tu broker utilizando MQTT Explorer.

En lugar de usar las credenciales internas de tu broker, utiliza las credenciales públicas `everyone/everyone`:

<img alt="MQTT Explorer: Conectar al broker" src="/../assets/img/mqtt-explorer-wis2box-broker-everyone-everyone.png" width="800">

!!! Note

    Nunca necesitas compartir las credenciales de tu broker interno con usuarios externos. El usuario 'everyone' es un usuario público que permite compartir notificaciones WIS2.

    Las credenciales `everyone/everyone` tienen acceso de solo lectura al tema 'origin/a/wis2/#'. Este es el tema donde se publican las notificaciones WIS2. El Global Broker puede suscribirse con estas credenciales públicas para recibir las notificaciones.
    
    El usuario 'everyone' no podrá ver temas internos ni publicar mensajes.
    
Abre un navegador y ve a `http://YOUR-HOST/wis2box-webapp`. Asegúrate de haber iniciado sesión y de poder acceder a la página 'dataset editor'.

Consulta la sección sobre [Inicialización de wis2box](./initializing-wis2box.md) si necesitas recordar cómo conectarte al broker o acceder a wis2box-webapp.

## Crear un token de autorización para processes/wis2box

Necesitarás un token de autorización para el endpoint 'processes/wis2box' para publicar tu conjunto de datos.

Para crear un token de autorización, accede a tu máquina virtual de entrenamiento mediante SSH y utiliza los siguientes comandos:

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

## El editor de conjuntos de datos de wis2box-webapp

Navega a la página 'dataset editor' en wis2box-webapp de tu instancia de wis2box accediendo a `http://YOUR-HOST/wis2box-webapp` y seleccionando 'dataset editor' en el menú de la izquierda.

En la página 'dataset editor', bajo la pestaña 'Datasets', haz clic en "Create New ...":

<img alt="Crear nuevo conjunto de datos" src="/../assets/img/wis2box-create-new-dataset.png" width="800">

Aparecerá una ventana emergente que te pedirá proporcionar:

- **Centre ID**: este es el acrónimo de la agencia (en minúsculas y sin espacios), según lo especificado por el Miembro de la OMM, que identifica el centro de datos responsable de publicar los datos.
- **Template**: El tipo de datos para el que estás creando metadatos. Puedes elegir entre usar una plantilla predefinida o seleccionar *other*.

<img alt="Ventana emergente para crear un nuevo conjunto de datos" src="/../assets/img/wis2box-create-new-dataset-pop-up.png" width="600">

!!! Note "Centre ID"

    Tu Centre ID debe comenzar con el TLD de tu país, seguido de un guion (`-`) y un nombre abreviado de tu organización (por ejemplo, `fr-meteofrance`). El Centre ID debe estar en minúsculas y usar solo caracteres alfanuméricos. La lista desplegable muestra todos los Centre IDs actualmente registrados en WIS2, así como cualquier Centre ID que ya hayas creado en wis2box. Por favor, elige un Centre ID apropiado para tu organización.

!!! Note "Template"

    El campo *Template* te permite seleccionar de una lista de plantillas disponibles en el editor de conjuntos de datos de wis2box-webapp. Una plantilla pre-poblará el formulario con valores predeterminados sugeridos apropiados para el tipo de datos. Esto incluye un título y palabras clave sugeridas para los metadatos y complementos de datos preconfigurados.
    
    El tema se establece automáticamente en el tema predeterminado vinculado a la plantilla seleccionada, a menos que selecciones *other*. Si seleccionas *other*, el tema puede definirse desde una lista desplegable basada en la [Jerarquía de Temas de WIS2](https://codes.wmo.int/wis/topic-hierarchy/_earth-system-discipline).

Para el propósito del entrenamiento, crearás dos conjuntos de datos:
    
- Un conjunto de datos utilizando la plantilla *weather/surface-based-observations/synop*, que incluye complementos de datos que transforman los datos al formato BUFR antes de la publicación.
- Un conjunto de datos utilizando la plantilla *other*, donde serás responsable de definir el Tema WIS2 y usarás el complemento "Universal" para publicar los datos sin transformación.

## Template=weather/surface-based-observations/synop

Para **Template**, selecciona **weather/surface-based-observations/synop**:

<img alt="Formulario para crear un nuevo conjunto de datos: Información inicial" src="/../assets/img/wis2box-create-new-dataset-form-initial.png" width="450">

Haz clic en *continue to form* para continuar. Ahora se te presentará el **Formulario del Editor de Conjuntos de Datos**.

Dado que seleccionaste la plantilla **weather/surface-based-observations/synop**, el formulario estará pre-poblado con algunos valores iniciales relacionados con este tipo de datos.

### Creación de metadatos de descubrimiento

El Formulario del Editor de Conjuntos de Datos te permite proporcionar los Metadatos de Descubrimiento para tu conjunto de datos que el contenedor wis2box-management utilizará para publicar un registro WCMP2.

Dado que seleccionaste la plantilla 'weather/surface-based-observations/synop', el formulario estará pre-poblado con algunos valores predeterminados.

Asegúrate de reemplazar el 'Local ID' generado automáticamente con un nombre descriptivo para tu conjunto de datos, por ejemplo, 'synop-dataset-wis2training':

<img alt="Editor de Metadatos: título, descripción, palabras clave" src="/../assets/img/wis2box-metadata-editor-part1.png" width="800">

Revisa el título y las palabras clave, actualízalos según sea necesario y proporciona una descripción para tu conjunto de datos.

Nota que hay opciones para cambiar la 'Política de Datos de la OMM' de 'core' a 'recommended' o para modificar tu Identificador de Metadatos predeterminado. Por favor, mantén la política de datos como 'core' y utiliza el Identificador de Metadatos predeterminado.

A continuación, revisa la sección que define tus 'Propiedades Temporales' y 'Propiedades Espaciales'. Puedes ajustar el cuadro delimitador actualizando los campos 'North Latitude', 'South Latitude', 'East Longitude' y 'West Longitude':

<img alt="Editor de Metadatos: propiedades temporales, propiedades espaciales" src="/../assets/img/wis2box-metadata-editor-part2.png" width="800">

Luego, completa la sección que define la 'Información de Contacto del Proveedor de Datos':

<img alt="Editor de Metadatos: información de contacto" src="/../assets/img/wis2box-metadata-editor-part3.png" width="800">

Finalmente, completa la sección que define la 'Información de Calidad de los Datos':

Una vez que hayas completado todas las secciones, haz clic en 'VALIDATE FORM' y verifica el formulario para detectar errores:

<img alt="Editor de Metadatos: validación" src="/../assets/img/wis2box-metadata-validation-error.png" width="800">

Si hay errores, corrígelos y haz clic en 'VALIDATE FORM' nuevamente.

Asegúrate de que no haya errores y de que recibas una ventana emergente indicando que tu formulario ha sido validado:

<img alt="Editor de Metadatos: validación exitosa" src="/../assets/img/wis2box-metadata-validation-success.png" width="800">

A continuación, antes de enviar tu conjunto de datos, revisa los mapeos de datos para tu conjunto de datos.

### Configuración de mapeos de datos

Dado que utilizaste una plantilla para crear tu conjunto de datos, los mapeos de datos se han pre-poblado con los complementos predeterminados para la plantilla 'weather/surface-based-observations/synop'. Los complementos de datos se utilizan en wis2box para transformar los datos antes de que se publiquen mediante la notificación WIS2.

<img alt="Mapeos de Datos: actualizar complemento" src="/../assets/img/wis2box-data-mappings.png" width="800">

Ten en cuenta que puedes hacer clic en el botón "Update" para cambiar la configuración del complemento, como la extensión de archivo y el patrón de archivo. Por ahora, puedes dejar la configuración predeterminada.

### Envío de tu conjunto de datos

Finalmente, puedes hacer clic en 'submit' para publicar tu conjunto de datos.

Necesitarás proporcionar el token de autorización para 'processes/wis2box' que creaste anteriormente. Si no lo has hecho, puedes crear un nuevo token siguiendo las instrucciones en la sección de preparación.

Verifique que reciba el siguiente mensaje después de enviar su conjunto de datos, indicando que el conjunto de datos se envió correctamente:

<img alt="Submit Dataset Success" src="/../assets/img/wis2box-submit-dataset-success.png" width="400">

Después de hacer clic en 'OK', será redirigido a la página principal del Editor de Conjuntos de Datos. Ahora, si hace clic en la pestaña 'Dataset', debería ver su nuevo conjunto de datos listado:

<img alt="Dataset Editor: new dataset" src="/../assets/img/wis2box-dataset-editor-new-dataset.png" width="800">

### Revisando la notificación WIS2 para sus metadatos de descubrimiento

Vaya a MQTT Explorer. Si estaba conectado al broker, debería ver una nueva notificación WIS2 publicada en el tema `origin/a/wis2/<your-centre-id>/metadata`:

<img alt="MQTT Explorer: WIS2 notification" src="/../assets/img/mqtt-explorer-wis2-notification-metadata.png" width="800">

Inspeccione el contenido de la notificación WIS2 que publicó. Debería ver un JSON con una estructura correspondiente al formato del Mensaje de Notificación WIS (WNM).

!!! question

    ¿En qué tema se publica la notificación WIS2?

??? success "Haga clic para revelar la respuesta"

    La notificación WIS2 se publica en el tema `origin/a/wis2/<your-centre-id>/metadata`.

!!! question
    
    Intente encontrar el título, la descripción y las palabras clave que proporcionó en los metadatos de descubrimiento dentro de la notificación WIS2. ¿Puede encontrarlos?

??? success "Haga clic para revelar la respuesta"

    **¡El título, la descripción y las palabras clave que proporcionó en los metadatos de descubrimiento no están presentes en el contenido de la notificación WIS2!** 
    
    En su lugar, intente buscar el enlace canónico en la sección "links" de la notificación WIS2:

    <img alt="WIS2 notification for metadata, links sections" src="/../assets/img/wis2-notification-metadata-links.png" width="800">

    **La notificación WIS2 contiene un enlace canónico al registro WCMP2 que fue publicado.** 
    
    Copie y pegue este enlace canónico en su navegador para acceder al registro WCMP2. Dependiendo de la configuración de su navegador, es posible que se le solicite descargar el archivo o que se muestre directamente en su navegador.

    Encontrará el título, la descripción y las palabras clave que proporcionó dentro del registro WCMP2.

wis2box proporciona solo un número limitado de plantillas predefinidas. Estas plantillas están diseñadas para tipos comunes de conjuntos de datos, pero es posible que no siempre coincidan con datos especializados. Para todos los demás tipos de conjuntos de datos, puede crear su conjunto de datos seleccionando Template=*other*.

## Template=other

A continuación, crearemos un segundo conjunto de datos utilizando Template=*other*.

Haga clic en "Create New ..." nuevamente para crear un nuevo conjunto de datos. Use el mismo centre-id que utilizó antes, debería estar disponible en la lista desplegable. Para **Template**, seleccione **other**:

<img alt="Create New Dataset Form: Initial information" src="/../assets/img/wis2box-create-new-dataset-form-initial-other.png" width="450">

Haga clic en *continue to form* para continuar, ahora se le presentará nuevamente el **Dataset Editor Form**.

### Creando metadatos de descubrimiento

Proporcione sus propios valores para los campos 'Title' y 'Description' y asegúrese de reemplazar el 'Local ID' generado automáticamente con un nombre descriptivo para su conjunto de datos:

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other.png" width="800">

Tenga en cuenta que, dado que seleccionó Template=*other*, depende de usted definir la Jerarquía de Temas WIS2 utilizando las listas desplegables para 'Discipline' y 'Sub-Discipline'.

Para este ejercicio, seleccione el Tema de Subdisciplina "prediction/analysis/medium-range/deterministic/global":

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other-topic.png" width="800">

Dado que utilizó Template=*other*, no se definieron palabras clave previamente. Asegúrese de agregar al menos 3 palabras clave de su elección:

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other-2.png" width="800">

Después de completar los campos obligatorios, complete las secciones restantes del formulario, incluyendo 'Temporal Properties', 'Spatial Properties' y 'Contact Information of the Data Provider', y asegúrese de validar el formulario.

### Configurando mapeos de datos

Cuando se utiliza una plantilla personalizada, no se proporcionan mapeos de datos predeterminados. Como resultado, el Editor de Mapeos de Conjuntos de Datos estará vacío y los usuarios deben configurar los mapeos según sus requisitos específicos.

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other1.png" width="800">

Haga clic en "ADD A PLUGIN +" para agregar un complemento de datos a su conjunto de datos.

Seleccione el complemento con el nombre **"Universal data without conversion"**. Este complemento está diseñado para publicar datos sin aplicar ninguna transformación.

Al agregar este complemento, deberá especificar la **File Extension** y un **File Pattern** (definido por una expresión regular) que coincida con el patrón de nombres de sus archivos de datos. En el caso del complemento "Universal", el File Pattern también se utiliza para determinar la propiedad "datetime" de los datos.

!!! Note "Parsing datetime from filename"

    El complemento "Universal" asume que el primer grupo en la expresión regular corresponde a la fecha y hora de los datos. 

    El File Pattern predeterminado es `^.*?_(\d{8}).*?\..*$`, que coincide con 8 dígitos precedidos por un guion bajo y seguidos por cualquier carácter y un punto antes de la extensión del archivo. Por ejemplo:

    - `mydata_20250101.txt` coincidirá y extraerá el 25 de enero de 2025 como la propiedad datetime de los datos.
    - `mydata_2025010112.txt` no coincidirá, ya que hay 10 dígitos en lugar de 8.
    - `mydata-20250101.txt` no coincidirá, ya que hay un guion en lugar de un guion bajo antes de la fecha.

    Al ingerir datos utilizando el complemento "Universal", renombre sus archivos para que coincidan con el valor predeterminado o actualice el File Pattern asegurándose de que el primer grupo en la expresión regular corresponda a la fecha y hora.

Mantenga los valores predeterminados para "File Name" por ahora, ya que coinciden con los datos que ingerirá en la próxima sesión práctica:

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other2.png" width="800">

Haga clic en "SAVE" para guardar la configuración del complemento y verifique que ahora vea el complemento listado en el Editor de Mapeos de Conjuntos de Datos:

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other3.png" width="800">

Tenga en cuenta que, cuando ingiera datos, la extensión del archivo y el patrón del nombre del archivo deben coincidir con la configuración que haya proporcionado aquí; de lo contrario, los datos no se procesarán y el contenedor wis2box-management registrará mensajes de ERROR.

### Enviar y revisar el resultado

Finalmente, proporcione el token de autorización para 'processes/wis2box' que creó anteriormente y haga clic en 'submit' para publicar su conjunto de datos.

Después de un envío exitoso, su nuevo conjunto de datos aparecerá en la pestaña Dataset:

<img alt="Dataset Editor: new dataset" src="/../assets/img/wis2box-dataset-editor-new-dataset-other.png" width="800">

Vaya a MQTT Explorer, si estaba conectado a su broker, debería ver otra nueva notificación WIS2 publicada en el tema `origin/a/wis2/<your-centre-id>/metadata`.

!!! question
    
    Visite la interfaz de usuario de wis2box en `http://YOUR-HOST`.
    
    ¿Cuántos conjuntos de datos ve listados? ¿Cómo puede ver la Jerarquía de Temas WIS2 utilizada para cada conjunto de datos y cómo puede ver la descripción de cada conjunto de datos?

??? success "Haga clic para revelar la respuesta"

    Al abrir la interfaz de usuario de wis2box en `http://YOUR-HOST`, debería ver 2 conjuntos de datos listados junto con su Jerarquía de Temas WIS2. Para ver la descripción de cada conjunto de datos, puede hacer clic en "metadata", lo que lo redirigirá al elemento 'discovery-metadata' correspondiente, tal como lo sirve la wis2box-api.

!!! question

    Intente actualizar la descripción del último conjunto de datos que creó. Después de actualizar la descripción, ¿ve una nueva notificación WIS2 publicada en el tema `origin/a/wis2/<your-centre-id>/metadata`? ¿Cuál es la diferencia entre la nueva notificación y la anterior?

??? success "Haga clic para revelar la respuesta"

    Debería ver un nuevo mensaje de notificación de datos enviado después de actualizar su conjunto de datos en el tema `origin/a/wis2/<your-centre-id>/metadata`.
    
    En el mensaje, el valor de *"rel": "canonical"* cambiará a *"rel": "update"*, indicando que los datos publicados anteriormente han sido modificados. Para ver la descripción actualizada, copie y pegue la URL en su navegador y debería ver la descripción actualizada.

!!! question

    Intente actualizar la Jerarquía de Temas del último conjunto de datos que creó cambiando la selección en "Sub-Discipline Topics". ¿Ve una nueva notificación WIS2 publicada en el tema `origin/a/wis2/<your-centre-id>/metadata`?

??? success "Haga clic para revelar la respuesta"

    **No** puede actualizar la Jerarquía de Temas de un conjunto de datos existente. El campo de Jerarquía de Temas está deshabilitado en el Editor de Conjuntos de Datos después de que se haya creado el conjunto de datos. Si desea utilizar una Jerarquía de Temas diferente, primero elimine el conjunto de datos existente y luego cree un nuevo conjunto de datos con la Jerarquía de Temas deseada.

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica, aprendiste a:

    - usar el editor de conjuntos de datos de wis2box-webapp
    - crear nuevos conjuntos de datos utilizando las plantillas Template=*weather/surface-based-observations/synop* y Template=*other*
    - definir tus metadatos de descubrimiento
    - revisar tus asignaciones de datos
    - publicar los metadatos de descubrimiento y revisar la notificación de WIS2