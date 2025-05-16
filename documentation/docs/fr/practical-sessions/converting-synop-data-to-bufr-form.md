---
title: Conversion des données SYNOP en BUFR
---

# Conversion des données SYNOP en BUFR à l'aide de l'application web wis2box

!!! abstract "Objectifs d'apprentissage"
    À la fin de cette session pratique, vous serez capable de :

    - soumettre des bulletins FM-12 SYNOP valides via l'application web wis2box pour conversion en BUFR et échange via le WIS2.0
    - valider, diagnostiquer et corriger des erreurs de codage simples dans un bulletin FM-12 SYNOP avant la conversion de format et l'échange
    - s'assurer que les métadonnées de station requises sont disponibles dans le wis2box
    - confirmer et inspecter les bulletins convertis avec succès

## Introduction

Pour permettre aux observateurs manuels de soumettre des données directement au WIS2.0, l'application web wis2box-webapp dispose d'un formulaire pour convertir les bulletins FM-12 SYNOP en BUFR. Le formulaire permet également aux utilisateurs de diagnostiquer et de corriger des erreurs de codage simples dans le bulletin FM-12 SYNOP avant la conversion de format et l'échange et d'inspecter les données BUFR résultantes.

## Préparation

!!! warning "Prérequis"

    - Assurez-vous que votre wis2box a été configuré et démarré.
    - Ouvrez un terminal et connectez-vous à votre VM étudiante via SSH.
    - Connectez-vous au broker MQTT de votre instance wis2box à l'aide de MQTT Explorer.
    - Ouvrez l'application web wis2box (``http://<votre-nom-d'hôte>/wis2box-webapp``) et assurez-vous que vous êtes connecté.

## Utilisation de l'application web wis2box pour convertir FM-12 SYNOP en BUFR

### Exercice 1 - Utilisation de l'application web wis2box pour convertir FM-12 SYNOP en BUFR

Assurez-vous que vous avez le jeton d'authentification pour "processes/wis2box" que vous avez généré lors de l'exercice précédent et que vous êtes connecté à votre broker wis2box dans MQTT Explorer.

Copiez le message suivant :
    
``` {.copy}
AAXX 27031
15015 02999 02501 10103 21090 39765 42952 57020 60001=
``` 

Ouvrez l'application web wis2box et naviguez jusqu'à la page synop2bufr en utilisant le tiroir de navigation gauche et procédez comme suit :

- Collez le contenu que vous avez copié dans la zone de texte.
- Sélectionnez le mois et l'année à l'aide du sélecteur de date, en supposant le mois en cours pour cet exercice.
- Sélectionnez un sujet dans le menu déroulant (les options sont basées sur les ensembles de données configurés dans le wis2box).
- Entrez le jeton d'authentification "processes/wis2box" que vous avez généré précédemment
- Assurez-vous que "Publier sur WIS2" est activé
- Cliquez sur "SOUMETTRE"

<center><img alt="Dialogue montrant la page synop2bufr, incluant le bouton bascule" src="/../assets/img/synop2bufr-toggle.png"></center>

Cliquez sur soumettre. Vous recevrez un message d'avertissement car la station n'est pas enregistrée dans le wis2box. Allez à l'éditeur de station et importez la station suivante :

``` {.copy}
0-20000-0-15015
```

Assurez-vous que la station est associée au sujet que vous avez sélectionné à l'étape précédente, puis revenez à la page synop2bufr et répétez le processus avec les mêmes données qu'auparavant.

!!! question
    Comment pouvez-vous voir le résultat de la conversion de FM-12 SYNOP en BUFR ?

??? success "Cliquez pour révéler la réponse"
    La section des résultats de la page affiche des avertissements, des erreurs et des fichiers BUFR de sortie.

    Cliquez sur "Fichiers BUFR de sortie" pour voir une liste des fichiers qui ont été générés. Vous devriez voir un fichier listé.

    Le bouton de téléchargement permet de télécharger les données BUFR directement sur votre ordinateur.

    Le bouton d'inspection lance un processus pour convertir et extraire les données du BUFR.

    <center><img alt="Dialogue montrant le résultat de la soumission réussie d'un message"
         src="/../assets/img/synop2bufr-ex2-success.png"></center>

!!! question
    Les données d'entrée FM-12 SYNOP n'incluaient pas la localisation de la station, l'élévation ou la hauteur du baromètre.
    Confirmez que ces éléments sont dans les données BUFR de sortie, d'où viennent-ils ?

??? success "Cliquez pour révéler la réponse"
    Cliquer sur le bouton d'inspection devrait afficher un dialogue comme celui montré ci-dessous.

    <center><img alt="Résultats du bouton d'inspection montrant les métadonnées de base de la station, la localisation de la station et les propriétés observées"
         src="/../assets/img/synop2bufr-ex2.png"></center>

    Cela inclut la localisation de la station affichée sur une carte et les métadonnées de base, ainsi que les observations dans le message.
    
    Dans le cadre de la transformation de FM-12 SYNOP en BUFR, des métadonnées supplémentaires ont été ajoutées au fichier BUFR.
    
    Le fichier BUFR peut également être inspecté en téléchargeant le fichier et en le validant à l'aide d'un outil tel que le validateur BUFR ecCodes de l'ECMWF.

Allez à MQTT Explorer et vérifiez le sujet des notifications WIS2 pour voir les notifications WIS2 qui ont été publiées.

### Exercice 2 - comprendre la liste des stations

Pour cet exercice suivant, vous convertirez un fichier contenant plusieurs rapports, voir les données ci-dessous :

``` {.copy}
AAXX 27031
15015 02999 02501 10103 21090 39765 42952 57020 60001=
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
```

!!! question
    Sur la base de l'exercice précédent, examinez le message FM-12 SYNOP et prédisez combien de messages BUFR
    seront générés.
    
    Copiez maintenant ce message dans le formulaire SYNOP et soumettez les données.

    Le nombre de messages générés correspond-il à votre attente et sinon, pourquoi pas ?

??? warning "Cliquez pour révéler la réponse"
    
    Vous auriez pu vous attendre à ce que trois messages BUFR soient générés, un pour chaque rapport météorologique. Cependant, à la place, vous avez obtenu 2 avertissements et seulement un fichier BUFR.
    
    Pour qu'un rapport météorologique soit converti en BUFR, les métadonnées de base contenues dans la 
    liste des stations sont requises. Bien que l'exemple ci-dessus inclue trois rapports météorologiques, deux des
    trois stations rapportant n'étaient pas enregistrées dans votre wis2box.
    
    En conséquence, seul l'un des trois rapports météorologiques a résulté en un fichier BUFR généré et une notification WIS2 publiée. Les deux autres rapports météorologiques ont été ignorés et des avertissements ont été générés.

!!! hint
    Notez la relation entre l'identifiant WIGOS et l'identifiant de station traditionnel inclus dans la sortie BUFR. Dans de nombreux cas, pour les stations répertoriées dans le WMO-No. 9
    Volume A au moment de la migration vers les identifiants de station WIGOS, l'identifiant de station WIGOS est donné par l'identifiant de station traditionnel avec ``0-20000-0`` préfixé,
    par exemple ``15015`` est devenu ``0-20000-0-15015``.

Utilisant la page de la liste des stations, importez les stations suivantes :

``` {.copy}
0-20000-0-15020
0-20000-0-15090
```

Assurez-vous que les stations sont associées au sujet que vous avez sélectionné lors de l'exercice précédent, puis revenez à la page synop2bufr et répétez le processus.

Trois fichiers BUFR devraient maintenant être générés et aucune erreur ou avertissement ne devrait être listé dans l'application web.

En plus des informations de base sur la station, des métadonnées supplémentaires telles que l'élévation de la station au-dessus du niveau de la mer et la hauteur du baromètre au-dessus du niveau de la mer sont nécessaires pour l'encodage en BUFR. Les champs sont inclus dans les pages de la liste des stations et de l'éditeur de stations.
    
### Exercice 3 - débogage

Dans cet exercice final, vous identifierez et corrigerez deux des problèmes les plus courants rencontrés lors de
l'utilisation de cet outil pour convertir FM-12 SYNOP en BUFR.

Les données d'exemple sont montrées dans la boîte ci-dessous, examinez les données et essayez de résoudre les problèmes qui pourraient
exister avant de soumettre les données via l'application web.

!!! hint
    Vous pouvez éditer les données dans la zone de saisie sur la page de l'application web. Si vous manquez des problèmes,
    ceux-ci devraient être détectés et mis en évidence comme un avertissement ou une erreur une fois le bouton de soumission
    cliqué.

``` {.copy}
AAXX 27031
15015 02999 02501 10103 21090 39765 42952 57020 60001
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
```

!!! question
    Quels problèmes vous attendiez-vous à rencontrer lors de la conversion des données en BUFR et comment les avez-vous
    surmontés ? Y avait-il des problèmes auxquels vous ne vous attendiez pas ?

??? success "Cliquez pour révéler la réponse"
    Dans ce premier exemple, le symbole "fin de texte" (=), ou délimiteur d'enregistrement, manque entre le
    premier et le deuxième rapport météorologique. Par conséquent, les lignes 2 et 3 sont traitées comme un seul rapport,
    entraînant des erreurs dans l'analyse du message.

Le deuxième exemple ci-dessous contient plusieurs problèmes courants trouvés dans les rapports FM-12 SYNOP. Examinez les
données et essayez d'identifier les problèmes, puis soumettez les données corrigées via l'application web.

```{.copy}
AAXX 27031
15020 02997 23104 10/30 21075 30177 40377 580200 60001 81041=
```

!!! question
    Quels problèmes avez-vous trouvés et comment les avez-vous résolus ?

??? success "Cliquez pour révéler la réponse"
    Il y a deux problèmes dans le rapport météorologique.
    
    Le premier, dans le groupe de température de l'air signé, a le caractère des dizaines défini comme manquant (/),
    entraînant un groupe invalide. Dans cet exemple, nous savons que la température est de 13,0 degrés
    Celsius (d'après les exemples ci-dessus) et donc ce problème peut être corrigé. Opérationnellement, la
    valeur correcte devrait être confirmée avec l'observateur.

    Le deuxième problème se produit dans le groupe 5 où il y a un caractère supplémentaire, avec le dernier
    caractère dupliqué. Ce problème peut être résolu en supprimant le caractère supplémentaire.

## Ménage

Pendant les exercices de cette session, vous aurez importé plusieurs fichiers dans votre liste de stations. Naviguez vers la
page de la liste des stations et cliquez sur les icônes de poubelle pour supprimer les stations. Vous devrez peut-être actualiser la page pour que
les stations soient retirées de la liste après leur suppression.

<center><img alt="Visualisateur de métadonnées de station"
         src="/../assets/img/synop2bufr-trash.png" width="600"></center>

## Conclusion

!!! success "Félicitations !"

    Dans cette session pratique, vous avez appris :

    - comment l'outil synop2bufr peut être utilisé pour convertir des rapports FM-12 SYNOP en BUFR ;
    - comment soumettre un rapport FM-12 SYNOP via l'application web ;
    - comment diagnostiquer et corriger des erreurs simples dans un rapport FM-12 SYNOP ;
    - l'importance d'enregistrer les stations dans le wis2box (et OSCAR/Surface) ;
    - et l'utilisation du bouton d'inspection pour visualiser le contenu des données BUFR.