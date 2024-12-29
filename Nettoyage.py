## Nettoyage des données

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from Fonctions_scrapping import telechargement_DF



# Renommer les colonnes

def rename_columns(dataframe):
    
    '''
    Renomme les colonnes du DataFrame passé en argument.
    Le choix a été fait d'intérioriser la liste des noms, on applique donc cette fonction avant toute autre modification du DataFrame.

    Paramètres : 
        - dataframe : Le DataFrame pandas contenant les données brutes sur les joueurs.
    '''  
    
    noms_colonnes = ["Poste", "Nationalité", "Date de naissance",
                     "Âge", "Taille", "Poids", "Club actuel", "Dernière saison"]
    dataframe.columns = noms_colonnes



# Gestion des unités des grandeurs

def changement_type_unites(dataframe,type='float'):

    '''
    Fait passer les données d'un DataFrame au format numérique (float par défaut).
    On applique cette fonction seulement sur les colonnes que l'on manipulera par la suite.
    
    Paramètres : 
        - dataframe : Un DataFrame pandas déjà transformé via la fonction rename_columns.
        -type (optionnel) : une chaine de caractère définissant vers quel type transformer les valeurs. Par défaut, float.
    '''

    dataframe["Âge"] = dataframe["Âge"].str.replace(r" ans", "", regex=True).astype(type)
    dataframe["Taille"] = dataframe["Taille"].str.replace(r" cm", "", regex=True).astype(type)
    dataframe["Poids"] = dataframe["Poids"].str.replace(r" kgs", "", regex=True).astype(type)



# Suppression des lignes vides

def suppression_lignes_vides(dataframe):
    
    '''
    Renvoie un nouveau DataFrame dans lequel les lignes pour lesquelles il manque des valeurs pour les variables d'intérêts ont été supprimées.
    
    Paramètres :
        - dataframe : Un DataFrame pandas déjà transformé via la fonction rename_columns.
    '''
 
    new_dataframe = dataframe.dropna(subset=['Poste', 'Taille', 'Poids'])
    return new_dataframe



# Ajout d'une colonne avec les postes par catégorie

def ajout_postes_regroupes(dataframe):

    '''
    Ajoute à un DataFrame une colonne codant les postes de manière simplifiée.
    Les arrières gauches et droits seront seulement des arrières et idem pour les ailiers gauches et droits.

    Paramètres :
        - dataframe : Un DataFrame pandas déjà transformé via la fonction rename_columns.
    '''

    postes_regroupes = {"Arrière Droit" : "Arrière",
           "Arrière Gauche" : "Arrière",
           "Ailier Droit" : "Ailier",
           "Ailier Gauche" : "Ailier"}
    
    dataframe["Poste simplifié"]= dataframe["Poste"].replace(postes_regroupes)



# Ajout d'une colonnne avec l'IMC des joueurs

def ajout_IMC(dataframe):

    '''
    Ajoute à un DataFrame une colonne contenant l'IMC des joueurs.

    Paramètres :
        - dataframe : Un DataFrame pandas déjà transformé via rename_columns.
    '''

    dataframe["IMC"] = dataframe["Poids"] / ((dataframe["Taille"]/100) ** 2).round(1)



# Nettoyage de la base de données

def cleaning(dataframe,nom_fichier=None):

    '''
    Réalise toutes les étapes du nettoyage d'un DataFrame contenant les données des joueurs.
    Télécharge ou renvoie le DataFrame nettoyé.

    Paramètres :
        - dataframe : Un DataFrame pandas contenant les données des joueurs.
        - nom_fichier (optionnel): chaine de caractères de la forme "nom_fichier.csv". Si renseigné, télécharge le DataFrame traité au format csv sous le nom renseigné.

    Etapes réalisées :
        - Renommer les colonnes
        - Passer les données au format numérique (float)
        - Ajouter la colonne avec les postes simplifiés
        - Ajouter une colonne avec l'IMC des joueurs 
        - Suppression des lignes vides
        - Téléchargement ou renvoi du DataFrame nettoyé
    '''

    rename_columns(dataframe)
    changement_type_unites(dataframe)
    ajout_postes_regroupes(dataframe)
    ajout_IMC(dataframe)
    new_data = suppression_lignes_vides(dataframe)

    if nom_fichier is None :
        return new_data
    else:
        telechargement_DF(new_data,nom_fichier)


