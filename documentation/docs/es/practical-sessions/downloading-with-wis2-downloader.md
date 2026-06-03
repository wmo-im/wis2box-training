---
title: Descargando con WIS2 Downloader
---

# Descargando con WIS2 Downloader

!!! abstract "¡Resultados de aprendizaje!"

    Al final de esta sesión práctica, serás capaz de:

    - explorar y encontrar conjuntos de datos en WIS2 Downloader
    - usar filtros para controlar los archivos descargados
    - utilizar autenticación para descargar conjuntos de datos con acceso controlado
    - cambiar la configuración predeterminada de WIS2 Downloader para casos de uso más avanzados

## Introducción

En WIS2, todos los conjuntos de datos tienen un archivo de metadatos que se puede encontrar en los **Global Discovery Catalogues**. Por lo tanto, se espera que los usuarios consulten siempre estos servicios para encontrar los datos compartidos en WIS2.

WIS2 Downloader utiliza este principio encontrando todos los registros disponibles en estos GDCs y combinándolos internamente para permitir al usuario navegar por los datos disponibles en WIS2. Dado que hay un gran número de registros para mostrar, es esencial proporcionar una forma para que el usuario los filtre y encuentre el registro correcto. Incluso después de encontrar y suscribirse al registro adecuado, puede haber conjuntos de datos donde el número de archivos exceda las necesidades actuales del usuario. Por esta razón, se necesita un segundo nivel de filtrado, uno que opere en el momento de decidir si un archivo debe descargarse.

## Explorando y buscando en la Vista de Catálogo

La **Vista de Catálogo** es una de las dos formas de encontrar y suscribirse a conjuntos de datos en WIS2 Downloader. Agrega registros de los Global Discovery Catalogues y los presenta en una interfaz que permite búsquedas y filtros, similar a navegar directamente en un portal GDC.

Navega a **Catalogue View** en la barra lateral izquierda.

![WIS2 Downloader Catalogue View](../assets/img/wis2-downloader-catalogue-view.png)

En la parte superior de la página encontrarás una barra de búsqueda y un conjunto de filtros. Puedes usarlos para reducir la lista de registros disponibles por palabra clave, Centre ID o política de datos (core vs. recommended).

También puedes filtrar espacialmente definiendo un **bounding box** usando cuatro entradas de coordenadas: **North**, **West**, **South** y **East**, expresadas como valores decimales de latitud y longitud. Cuando se establece un bounding box, puedes elegir entre dos modos de coincidencia:

- **Intersects** — devuelve registros cuya extensión espacial se superpone con el bounding box de cualquier manera.
- **Within** — devuelve solo registros cuya extensión espacial cae completamente dentro del bounding box.

!!! note "Recargando el catálogo"

    El catálogo se carga desde los GDCs cuando se inicia WIS2 Downloader. Si crees que la lista está desactualizada, puedes forzar una recarga desde la sección **Settings** en la barra lateral izquierda.

### Ejercicio: encontrar y suscribirse a un conjunto de datos

!!! question "Encuentra un conjunto de datos de observación de superficie"

    Usa los filtros en la Vista de Catálogo para encontrar un conjunto de datos de observación de superficie **core** relacionado con temperatura y precipitación.

    1. Escribe `surface` en la barra de búsqueda y observa cómo se filtra la lista de registros.
    2. Configura el filtro de política de datos en **core**.
    3. Configura las palabras clave para incluir `temperature, precipitation` y observa cómo cambian los resultados.
    4. Selecciona un registro de los resultados para expandir sus detalles.
    5. Revisa los metadatos mostrados: toma nota del tema, el centro de origen y la política de datos.
    6. Configura la carpeta de destino como `surface-obs`.
    7. Haz clic en **Subscribe** para crear la suscripción.

    Después de suscribirte, navega a **Manage Subscriptions** para confirmar que la nueva suscripción aparece en la lista.

??? success "Haz clic para revelar la respuesta"

    Cualquier registro cuyo tema contenga `surface-based-observations` y cuya política de datos sea `core` es una elección válida. Aplicar el filtro de palabras clave para `temperature, precipitation` reducirá aún más los resultados a conjuntos de datos relevantes para esas variables.

    Una vez suscrito, la vista **Manage Subscriptions** mostrará la suscripción activa con su tema y carpeta de destino. Los archivos comenzarán a descargarse a medida que lleguen nuevas notificaciones al broker.

!!! note "Eliminando archivos descargados"

    Se recomienda limpiar la carpeta de descargas después de completar un ejercicio para liberar espacio en la máquina virtual del estudiante:

    ```bash
    rm -fr wis2downloader/downloads/surface-obs
    ```

## Explorando y buscando en la Vista de Árbol

La **Vista de Árbol** presenta la jerarquía de temas de WIS2 como un árbol colapsable, permitiéndote explorar los temas disponibles nivel por nivel, similar a navegar temas en MQTT Explorer. Está diseñada para una exploración de alto nivel, de arriba hacia abajo, de los datos disponibles en WIS2, comenzando desde la raíz de la jerarquía y profundizando. Esto contrasta con la Vista de Catálogo, que te lleva directamente a registros individuales de conjuntos de datos y es más adecuada cuando ya sabes lo que estás buscando.

Navega a **Tree View** en la barra lateral izquierda.

![WIS2 Downloader Tree View](../assets/img/wis2-downloader-tree-view.png)

El árbol está organizado siguiendo la jerarquía de temas de WIS2. Expande cada nivel haciendo clic en un nodo para revelar sus hijos. En cualquier nivel puedes suscribirte seleccionando un nodo y haciendo clic en **Subscribe**, utilizando un comodín (`#`) para capturar todos los temas debajo de ese nodo.

!!! note "Suscribirse en diferentes niveles"

    Suscribirse en niveles superiores del árbol (por ejemplo, en el nivel de Centre ID) capturará todos los conjuntos de datos publicados por ese centro. Suscribirse en niveles inferiores te da un control más granular. Usa el sufijo comodín `#` que WIS2 Downloader agrega automáticamente al suscribirte desde la Vista de Árbol.

### Ejercicio: encontrar y suscribirse usando la Vista de Árbol

!!! question "Suscríbete a un conjunto de datos mediante la Vista de Árbol"

    Usa la Vista de Árbol para encontrar y suscribirte a datos de observación de superficie de un centro específico.

    1. Expande el árbol comenzando desde el nodo `cache`, luego navega a través de `a` → `wis2`.
    2. Selecciona un Centre ID de tu elección y continúa expandiendo hasta llegar a un tema relacionado con `surface-based-observations`.
    3. Revisa la ruta completa del tema mostrada: confirma que corresponde al conjunto de datos que deseas.
    4. Configura la carpeta de destino como `surface-obs-tree`.
    5. Haz clic en **Subscribe** para crear la suscripción.

    Navega a **Manage Subscriptions** para confirmar que la suscripción está activa.

??? success "Haz clic para revelar la respuesta"

    Cualquier ruta de tema que siga el patrón `cache/a/wis2/<centre-id>/data/core/weather/surface-based-observations/#` es una elección válida. El segmento de Centre ID variará dependiendo del centro que seleccionaste en el árbol.

    La vista **Manage Subscriptions** mostrará la nueva suscripción junto con cualquier otra creada previamente.

!!! note "Eliminando archivos descargados"

    Limpia la carpeta de descargas después de completar el ejercicio:

    ```bash
    rm -fr wis2downloader/downloads/surface-obs-tree
    ```