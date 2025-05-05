---
title: Scoprire i dataset dal WIS2 Global Discovery Catalogue
---

# Scoprire i dataset dal WIS2 Global Discovery Catalogue

!!! abstract "Obiettivi di apprendimento!"

    Al termine di questa sessione pratica, sarai in grado di:

    - utilizzare pywiscat per scoprire dataset dal Global Discovery Catalogue (GDC)

## Introduzione

In questa sessione imparerai come scoprire i dati dal WIS2 Global Discovery Catalogue (GDC).

Al momento, sono disponibili i seguenti GDC:

- Environment and Climate Change Canada, Meteorological Service of Canada: <https://wis2-gdc.weather.gc.ca>
- China Meteorological Administration: <https://gdc.wis.cma.cn>
- Deutscher Wetterdienst: <https://wis2.dwd.de/gdc>

Durante le sessioni di formazione locali, viene configurato un GDC locale per consentire ai partecipanti di interrogare il GDC per i metadati pubblicati dalle loro istanze wis2box. In questo caso, i formatori forniranno l'URL del GDC locale.

## Preparazione

!!! note
    Prima di iniziare, effettua l'accesso alla tua VM studente.

## Installazione di pywiscat

Usa il gestore di pacchetti Python `pip3` per installare pywiscat sulla tua VM:
```bash
pip3 install pywiscat
```

!!! note

    Se riscontri il seguente errore:

    ```
    WARNING: The script pywiscat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    Esegui il seguente comando:

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    ...dove `$USER` è il tuo nome utente sulla VM.

Verifica che l'installazione sia avvenuta con successo:

```bash
pywiscat --version
```

## Trovare dati con pywiscat

Per impostazione predefinita, pywiscat si connette al Global Discovery Catalogue del Canada. Configuriamo pywiscat per interrogare il GDC di formazione impostando la variabile d'ambiente `PYWISCAT_GDC_URL`:

```bash
export PYWISCAT_GDC_URL=http://gdc.wis2.training:5002
```

Utilizziamo [pywiscat](https://github.com/wmo-im/pywiscat) per interrogare il GDC configurato per la formazione.

```bash
pywiscat search --help
```

Ora cerca nel GDC tutti i record:

```bash
pywiscat search
```

!!! question

    Quanti record vengono restituiti dalla ricerca?

??? success "Clicca per vedere la risposta"
    Il numero di record dipende dal GDC che stai interrogando. Quando usi il GDC locale di formazione, dovresti vedere che il numero di record è uguale al numero di dataset che sono stati inseriti nel GDC durante le altre sessioni pratiche.

Proviamo a interrogare il GDC con una parola chiave:

```bash
pywiscat search -q observations
```

!!! question

    Qual è la politica dei dati dei risultati?

??? success "Clicca per vedere la risposta"
    Tutti i dati restituiti dovrebbero specificare dati "core"

Prova ulteriori ricerche con `-q`

!!! tip

    Il flag `-q` permette la seguente sintassi:

    - `-q synop`: trova tutti i record con la parola "synop"
    - `-q temp`: trova tutti i record con la parola "temp"
    - `-q "observations AND oman"`: trova tutti i record con le parole "observations" e "oman"
    - `-q "observations NOT oman"`: trova tutti i record che contengono la parola "observations" ma non la parola "oman"
    - `-q "synop OR temp"`: trova tutti i record con "synop" o "temp"
    - `-q "obs*"`: ricerca fuzzy

    Quando cerchi termini con spazi, racchiudili tra virgolette doppie.

Otteniamo maggiori dettagli su un risultato specifico della ricerca che ci interessa:

```bash
pywiscat get <id>
```

!!! tip

    Usa il valore `id` dalla ricerca precedente.

## Conclusione

!!! success "Congratulazioni!"

    In questa sessione pratica, hai imparato a:

    - utilizzare pywiscat per scoprire dataset dal WIS2 Global Discovery Catalogue