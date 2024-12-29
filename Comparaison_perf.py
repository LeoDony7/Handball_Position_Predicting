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

def moyenne_perf_poste(dataframe):

    '''
    Crée un DataFrame donnant la moyenne de l'indicateur de performance pour chaque poste.
    Ce Dataframe sera utilisé dans la fonction comparaison_performance.

    Paramètres :
        - dataframe : Un DataFrame pandas. On utilisera toujours un DataFrame contenant la colonne 'Poste prédit'.
    '''

    moyennes_vrai_poste = dataframe.groupby("Poste simplifié")["Indicateur de performance"].mean()
    moyennes_poste_predit = dataframe.groupby("Poste prédit")["Indicateur de performance"].mean()

    moyennes = pd.merge(moyennes_vrai_poste,moyennes_poste_predit,left_index= True, right_index=True, how='inner')
    moyennes.reset_index()
    moyennes.columns = ['Perf vrai poste','Perf poste prédit']

    # ma nouvelle idée : (ajouter nouvel argument à la fonction)
    # le nouvel argument prendrait les valeurs : 'Moyenne performances poste actuel' ou 'Moyenne performances des joueurs du poste prédit'
    '''
    moyennes_vrai_poste = dataframe.groupby("Poste simplifié")["Indicateur de performance"].mean()
    moyennes.columns = ['argument_nom_colonne']
    '''

    return moyennes


# Ajoute le rapport entre l'indicateur de performance d'un joueur et la moyenne de cet indicateur pour les joueurs jouant à ce poste
# Ajoute également le rapport entre l'indic et la moyenne des joueurs prédits à ce poste
# (selon mon idée le 2eme indicateur remplacée par moyenne des joueurs jouant au poste prédit)

def comparaison_performance(data):

    '''
    Ajoute à un DataFrame les moyennes de l'indicateur de performance calculé sur les sous-groupes de joueurs pouant au poste actuel et au poste prédit.
    Ajoute à un DataFrame les ratios entre l'indicateur de performance et chacune des moyennes calculées précédemment.

    Paramètres :
        - dataframe : Un DataFrame pandas. On utilisera toujours un DataFrame contenant la colonne 'Indicateur de performances'.
    '''
    
    # Joindre les moyennes au DataFrame original
    data = data.join(moyenne_perf_poste(data), on='Poste simplifié')

    # Calculer les ratios
    data['Ratio poste réel'] = data['Indicateur de performance'] / data['Perf vrai poste'] 
    data['Ratio poste prédit'] = data['Indicateur de performance'] / data['Perf poste prédit'] 

    # ma nouvelle idée :
    '''
    data = data.join(moyenne_perf_poste(data,'Moyenne perf joueurs au poste actuel'), on='Poste simplifié')
    data = data.join(moyenne_perf_poste(data,'Moyenne perf joueurs au poste prédit'), on='Poste prédit')
    
    data['Ratio poste réel'] = data['Indicateur de performance'] / data['Moyenne perf joueurs au poste actuel'] 
    data['Ratio poste prédit'] = data['Indicateur de performance'] / data['Moyenne perf joueurs au poste prédit'] 
    '''


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

def comparaison(dataframe,nom_fichier):

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





