## Pour comparer les performances des joueurs prédits à un poste différent

# Créer un indicateur de performance
# Idée : nombre de buts * (1 + efficacité au tir) / temps de jeu ?

# Faire la moyenne de cet indicateur sur chaque poste (possiblement seulement sur les meilleurs joueurs)

# Pour les joueurs prédits à un poste différent, comparer leur indicateur à la moyenne du vrai poste et du poste prédit

# Essayer de comprendre si les différences sont dues à une erreur de prédiction ou au fait qu'un joueur joue au "mauvais" poste



## Modif que j'ai envie de faire : ne faire que le DF moyennes_vrai_poste, mais le join sur 2 trucs différents
## On le join sur post simplifé pour avoir la moyenne du poste auquel un joueur joue
## et on le join sur post prédit pour avoir la moyenne des joueurs jouant rééllement au poste prédit pour le joueur
## Actuellement on compare la moyenne du joueur à la moyenne des joueurs prédit à ce poste
## Avec ma modif on aurait la moyenne des joueurs jouant effectivement à ce poste
## Il faudrait alors rajouter un argument de nom de colonne dans moyenne_perf_poste pour pas se mélanger quand on join

import pandas as pd
import numpy as np
from Fonctions_scrapping import telechargement_DF


# Ajout d'un indicateur de performances

def indicateur_performance(data):

    """
    Ajoute un indicateur de performance basé sur la formule :
    nb de buts * (1 + efficacité) / temps de jeu.
    """

    # Calcul de l'indicateur
    data['Indicateur de performance'] = (data['Total buts'] * (1 + data['%total numerique']/100) / np.maximum(data['Minutes jouées'],1)).round(3)



# Création d'un DF avec la moyenne de l'indicateur de performance pour les joueurs jouant à ce poste et ceux prédits à ce poste
# (selon mon idée seulement pour les joueurs jouant à ce poste)

def moyenne_perf_poste(data):

    """
    Calcul rapide de la moyenne des performances selon le poste.
    Prend pour argument un data frame et un 
    """

    moyennes_vrai_poste = data.groupby("Poste simplifié")["Indicateur de performance"].mean()
    moyennes_poste_predit = data.groupby("Poste prédit")["Indicateur de performance"].mean()

    moyennes = pd.merge(moyennes_vrai_poste,moyennes_poste_predit,left_index= True, right_index=True, how='inner')
    moyennes.reset_index()
    moyennes.columns = ['Perf vrai poste','Perf poste prédit']

    # ma nouvelle idée : (ajouter nouvel argument à la fonction)
    # le nouvel argument prendrait les valeurs : 'Moyenne performances poste actuel' ou 'Moyenne performances des joueurs du poste prédit'
    '''
    moyennes_vrai_poste = data.groupby("Poste simplifié")["Indicateur de performance"].mean()
    moyennes.columns = ['argument_nom_colonne']
    '''

    return moyennes


# Ajoute le rapport entre l'indicateur de performance d'un joueur et la moyenne de cet indicateur pour les joueurs jouant à ce poste
# Ajoute également le rapport entre l'indic et la moyenne des joueurs prédits à ce poste
# (selon mon idée le 2eme indicateur remplacée par moyenne des joueurs jouant au poste prédit)

def comparaison_performance(data) :
    """
    Calcule deux ratios pour chaque joueur :
    """
    
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

    return data

# Renvoie un DF avec les joueurs prédits à un poste différent du leur et les différentes infos de performances

def comparaison(data):

    '''
    Description.
    '''

    DF=comparaison_performance(data)
    
    joueurs_filtrés = DF[DF['Poste simplifié'] != DF['Poste prédit']]

    colonnes_a_afficher = ['Poste simplifié', 'Poste prédit', 'Perf vrai poste', 'Perf poste prédit','Ratio poste réel', 'Ratio poste prédit']
    joueurs_filtrés = joueurs_filtrés[colonnes_a_afficher]

    telechargement_DF(joueurs_filtrés,nom_fichier='DF_filtre_test.csv')
    return joueurs_filtrés






