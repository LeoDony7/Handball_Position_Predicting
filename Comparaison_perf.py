## Pour comparer les performances des joueurs prédits à un poste différent

# Créer un indicateur de performance
# Idée : nombre de buts * (1 + efficacité au tir) / temps de jeu ?

# Faire la moyenne de cet indicateur sur chaque poste (possiblement seulement sur les meilleurs joueurs)

# Pour les joueurs prédits à un poste différent, comparer leur indicateur à la moyenne du vrai poste et du poste prédit

# Essayer de comprendre si les différences sont dues à une erreur de prédiction ou au fait qu'un joueur joue au "mauvais" poste

import pandas as pd
import numpy as np

def indicateur_performance(data):
    """
    Ajoute un indicateur de performance basé sur la formule :
    nb de buts * (1 + efficacité) / temps de jeu.
    """

    # Calcul de l'indicateur
    data['Indicateur de performance'] = (data['Total buts'] * (1 + data['%total numerique']/100) / np.maximum(data['Minutes jouées'],1))

    # return data

def moyenne_perf_poste(data):
    """
    Calcul rapide de la moyenne des performances selon le poste.
    Prend pour argument un data frame et un 
    """

    moyennes = data.groupby("Poste")["Indicateur de perfomance"].mean().reset_index()
    moyennes["Perf poste prédit"] = data.groupby("Poste predit")["Indicateur de perfomance"].mean().reset_index()

    moyennes.columns = ['Poste','Perf vrai poste','Perf poste prédit']

    return moyennes


def comparaison_performance(data) :
    """
    Calcule deux ratios pour chaque joueur :
    """
    
    # Joindre les moyennes au DataFrame original
    data = data.join(moyenne_perf_poste(data), on='Poste')

    # Calculer les ratios
    data['Ratio poste réel'] = data['Indicateur de performance'] / data['Perf vrai poste'] * 100
    data['Ratio poste prédit'] = data['Indicateur de performance'] / data['Perf poste prédit'] * 100

    return data


def comparaison(data):
    DF=indicateur_performance(data)
    DF=comparaison_performance(DF)
    
    joueurs_filtrés = DF[DF['Poste'] != DF['Poste prédit']]

    colonnes_a_afficher = ['Poste', 'Poste prédit', 'Perf vrai poste', 'Perf poste prédit']
    joueurs_filtrés = joueurs_filtrés[colonnes_a_afficher]

    print(joueurs_filtrés)






