## Comparaisons des performances des joueurs mal prédits

import pandas as pd
import numpy as np
from Fonctions_scrapping import telechargement_DF

## Modif que j'ai envie de faire : ne faire que le DF moyennes_vrai_poste, mais le join sur 2 trucs différents
## On le join sur post simplifé pour avoir la moyenne du poste auquel un joueur joue
## et on le join sur post prédit pour avoir la moyenne des joueurs jouant rééllement au poste prédit pour le joueur
## Actuellement on compare la moyenne du joueur à la moyenne des joueurs prédit à ce poste
## Avec ma modif on aurait la moyenne des joueurs jouant effectivement à ce poste
## Il faudrait alors rajouter un argument de nom de colonne dans moyenne_perf_poste pour pas se mélanger quand on join



# Ajout d'un indicateur de performances

def indicateur_performance(dataframe):

    '''
    Ajoute à un DataFrame un indicateur de performance calculé via la formule suivante :
    nombre de buts * (1 + efficacité au tir) / temps de jeu en minutes

    Paramètres :
        - dataframe : Un DataFrame pandas. On utilisera toujours un DataFrame contenant les données de match nettoyées.
    '''

    # Calcul de l'indicateur
    dataframe['Indicateur de performance'] = (dataframe['Total buts'] * (1 + dataframe['%total numerique']/100) / np.maximum(dataframe['Minutes jouées'],1)).round(3)

    # Remarque : ajout de np.maximum(colonne,1) pour ne pas diviser par 0 et donc pour ne pas avoir de cases NaN à l'arrivée


# Création d'un DF avec la moyenne de l'indicateur de performance pour les joueurs jouant à ce poste et ceux prédits à ce poste
# (selon mon idée seulement pour les joueurs jouant à ce poste)

def moyenne_perf_poste(dataframe, nom_colonne):

    '''
    Crée un DataFrame donnant la moyenne de l'indicateur de performance pour chaque poste.
    Ce Dataframe sera utilisé dans la fonction comparaison_performance.

    Paramètres :
        - dataframe : Un DataFrame pandas. On utilisera toujours un DataFrame contenant la colonne 'Poste prédit' et 'Poste simplifié'.
        - nom_colonne : Une chaine de caractères. Nom à donner à la colonne du DataFrame crée.
    '''

    moyennes_vrai_poste = dataframe.groupby("Poste simplifié")["Indicateur de performance"].mean()
    moyennes_vrai_poste.name = nom_colonne


    return moyennes_vrai_poste
    




# Ajoute le rapport entre l'indicateur de performance d'un joueur et la moyenne de cet indicateur pour les joueurs jouant à ce poste
# Ajoute également le rapport entre l'indic et la moyenne des joueurs prédits à ce poste
# (selon mon idée le 2eme indicateur remplacée par moyenne des joueurs jouant au poste prédit)

def comparaison_performance(dataframe):

    '''
    Renvoie un DataFrame étant une copie du Dataframe en entreé, avec 4 nouvelles colonnes:
    -Les moyennes de l'indicateur de performance calculé sur les sous-groupes de joueurs jouant au poste actuel et au poste prédit.
    -Les ratios entre l'indicateur de performance et chacune des moyennes calculées précédemment.

    Paramètres :
        - dataframe : Un DataFrame pandas. On utilisera toujours un DataFrame contenant la colonne 'Indicateur de performances'.
    '''
    
    # Joindre les moyennes au DataFrame original
    dataframe_1 = dataframe.join(moyenne_perf_poste(dataframe,'Moyenne perf joueurs au poste actuel'), on='Poste simplifié')
    dataframe_2 = dataframe_1.join(moyenne_perf_poste(dataframe,'Moyenne perf joueurs au poste prédit'), on='Poste prédit')
    
    # Calculer les ratios
    dataframe_2['Ratio poste réel'] = dataframe_2['Indicateur de performance'] / dataframe_2['Moyenne perf joueurs au poste actuel'] 
    dataframe_2['Ratio poste prédit'] = dataframe_2['Indicateur de performance'] / dataframe_2['Moyenne perf joueurs au poste prédit'] 
    
    return dataframe_2


## Préparation du DataFrame pour la comparaison 

def traitement_comparaison(dataframe,nom_fichier=None):

    '''
    Effectue le traitement des données en vue de la comparaison des performances.
    Télécharge ou renvoie le DataFrame traité.
    
    Paramètres : 
        - dataframe : Un DataFrame pandas. On utilisera toujours le Dataframe joint issu des 2 DataFrames nettoyés.
        - nom_fichier (optionnel): chaine de caractères de la forme "nom_fichier.csv". Si renseigné, télécharge le DataFrame traité au format csv sous le nom renseigné.
    
    Traitements effectués :
        - Calcul de l'indicateur de performances
        - Calcul de la moyenne de cet indicateur par poste
        - Calcul du ratio entre l'indicateur individuel et la moyenne pour le poste actuel
        - Calcul du ratio entre l'indicateur individuel et la moyenne pour le poste prédit
    '''

    indicateur_performance(dataframe)
    comparaison_performance(dataframe)

    # téléchargement (optionnel)
    if nom_fichier:
        telechargement_DF(dataframe,nom_fichier)
    else:
        return dataframe



# Renvoie un DF avec les joueurs prédits à un poste différent du leur et les différentes infos de performances

def comparaison(dataframe,nom_fichier=None):

    '''
    Crée un DataFrame contenant les joueurs dont le poste prédit est différent du poste actuel.
    Les colonnes de ce DataFrame contiennent des informations autour des performances des joueurs.

    Paramètres : 
        - dataframe : Un DataFrame pandas. On utilisera toujours un DataFrame traité par la fonction traitement_comparaison.
        - nom_fichier (optionnel): chaine de caractères de la forme "nom_fichier.csv". Si renseigné, télécharge le DataFrame traité au format csv sous le nom renseigné.
    '''
    
    joueurs_filtrés = dataframe[dataframe['Poste simplifié'] != dataframe['Poste prédit']]

    colonnes_a_afficher = ['Poste simplifié', 'Poste prédit', 'Perf vrai poste', 'Perf poste prédit','Ratio poste réel', 'Ratio poste prédit']
    joueurs_filtrés = joueurs_filtrés[colonnes_a_afficher]

    # téléchargement (optionnel)
    if nom_fichier:
        telechargement_DF(joueurs_filtrés,nom_fichier)

    return joueurs_filtrés





