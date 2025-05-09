---
title: Scoperta di dataset dal Catalogo Globale di Scoperta WIS2
---

# Scoperta di dataset dal Catalogo Globale di Scoperta WIS2

!!! abstract "Risultati di apprendimento!"

    Al termine di questa sessione pratica, sarai in grado di:

    - utilizzare pywiscat per scoprire dataset dal Catalogo Globale di Scoperta (GDC)

## Introduzione

In questa sessione imparerai come scoprire dati dal Catalogo Globale di Scoperta WIS2 (GDC).

Al momento, i seguenti GDC sono disponibili:

- Environment and Climate Change Canada, Meteorological Service of Canada: <https://wis2-gdc.weather.gc.ca>
- China Meteorological Administration: <https://gdc.wis.cma.cn>
- Deutscher Wetterdienst: <https://wis2.dwd.de/gdc>


Durante le sessioni di formazione locali, viene configurato un GDC locale per permettere ai partecipanti di interrogare il GDC per i metadati che hanno pubblicato dalle loro istanze di wis2box. In questo caso i formatori forniranno l'URL del GDC locale.

## Preparazione

!!! note
    Prima di iniziare, effettua il login alla tua VM studente.

## Installazione di pywiscat

Usa l'installer di pacchetti Python `pip3` per installare pywiscat sulla tua VM:
```bash
pip3 install pywiscat
```

!!! note

    Se incontri il seguente errore:

    ```
    WARNING: The script pywiscat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    Allora esegui il seguente comando:

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    ...dove `$USER` è il tuo nome utente sulla tua VM.

Verifica che l'installazione sia stata completata con successo:

```bash
pywiscat --version
```

## Ricerca di dati con pywiscat

Per impostazione predefinita, pywiscat si connette al Catalogo Globale di Scoperta del Canada. Configuriamo pywiscat per interrogare il GDC di formazione impostando la variabile d'ambiente `PYWISCAT_GDC_URL`:

```bash
export PYWISCAT_GDC_URL=http://gdc.wis2.training:5002
```

Usiamo [pywiscat](https://github.com/wmo-im/pywiscat) per interrogare il GDC configurato come parte della formazione.

```bash
pywiscat search --help
```

Ora cerca nel GDC tutti i record:

```bash
pywiscat search
```

!!! question

    Quanti record vengono restituiti dalla ricerca?

??? success "Clicca per rivelare la risposta"
    Il numero di record dipende dal GDC che stai interrogando. Utilizzando il GDC di formazione locale, dovresti vedere che il numero di record è uguale al numero di dataset che sono stati inseriti nel GDC durante le altre sessioni pratiche.

Proviamo a interrogare il GDC con una parola chiave:

```bash
pywiscat search -q observations
```

!!! question

    Qual è la politica dei dati dei risultati?

??? success "Clicca per rivelare la risposta"
    Tutti i dati restituiti dovrebbero specificare "core" data

Prova ulteriori query con `-q`

!!! tip

    Il flag `-q` permette la seguente sintassi:

    - `-q synop`: trova tutti i record con la parola "synop"
    - `-q temp`: trova tutti i record con la parola "temp"
    - `-q "observations AND oman"`: trova tutti i record con le parole "observations" e "oman"
    - `-q "observations NOT oman"`: trova tutti i record che contengono la parola "observations" ma non la parola "oman"
    - `-q "synop OR temp"`: trova tutti i record con entrambe le parole "synop" o "temp"
    - `-q "obs*"`: ricerca fuzzy

    Quando cerchi termini con spazi, racchiudili tra virgolette doppie.

Otteniamo più dettagli su un risultato di ricerca specifico che ci interessa:

```bash
pywiscat get <id>
```

!!! tip

    Usa il valore `id` dalla ricerca precedente.


## Conclusione

!!! success "Congratulazioni!"

    In questa sessione pratica, hai imparato come:

    - utilizzare pywiscat per scoprire dataset dal Catalogo Globale di Scoperta WIS2