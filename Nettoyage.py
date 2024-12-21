import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from Fonctions_scrapping import telechargement_DF

## Nettoyage des données

# Renommer les colonnes

def rename_columns(data):
    
    '''
    Cette fonction prend en argument un DataFrame.
    Elle modifie le nom des colonnes du DataFrame en utilisant la liste à l'intérieur de la fonction.
    Le choix a été fait d'intérioriser la liste des noms, on applique donc cette fonction avant toute autre modification du DataFrame.
    '''  
    
    noms_colonnes = ["Poste", "Nationalité", "Date de naissance",
                     "Âge", "Taille", "Poids", "Club actuel", "Dernière saison"]
    data.columns = noms_colonnes


# Gestion des unités des grandeurs

def changement_type_unites(data,type='float'):

    '''
    Cette fonction prend en argument un DataFrame et le type vers lequel transformer les données (par défaut float).
    La fonction permet de supprimer les unités dans les cases du DataFrame et de transformer les chaines de nombres en un format adapté aux calculs.
    '''

    data["Âge"] = data["Âge"].str.replace(r" ans", "", regex=True).astype(type)
    data["Taille"] = data["Taille"].str.replace(r" cm", "", regex=True).astype(type)
    data["Poids"] = data["Poids"].str.replace(r" kgs", "", regex=True).astype(type)


# Suppression des lignes vides

def suppression_lignes_vides(data):
    
    '''
    Cette fonction prend en argument un DataFrame.
    Elle renvoie un nouveau DataFrame qui correspond au DataFrame d'origine vidé des lignes
    pour lesquelles il nous manque des valeurs pour les variables d'intérêt.
    '''
 
    new_data = data.dropna(subset=['Poste', 'Taille', 'Poids'])
    return new_data


# Ajout d'une colonne avec les postes par catégorie

def ajout_postes_regroupes(data):

    '''
    Cette fonction prend en argument un DataFrame.
    Elle ajoute à ce DataFrame une colonne dans laquelle certains postes sont regroupés.
    Les arrières gauches et droits seront des arrières et idem pour les ailiers gauches et droits.
    '''

    postes_regroupes = {"Arrière Droit" : "Arrière",
           "Arrière Gauche" : "Arrière",
           "Ailier Droit" : "Ailier",
           "Ailier Gauche" : "Ailier"}
    
    data["Poste simplifié"]= data["Poste"].replace(postes_regroupes)
    

# Ajout d'une colonnne avec l'IMC des joueurs

def ajout_IMC(data):

    '''
    Cette fonction prend en argument un DataFrame.
    Elle rajoute à ce DataFrame une colonne contenant l'IMC.
    '''

    data["IMC"] = data["Poids"] / ((data["Taille"]/100) ** 2)


# Nettoyage de la base de données

def cleaning(data,nom_fichier=None):

    '''
    Cette fonction prend en argument un DataFrame et un argument optionnel, le nom du fichier.
    Cette fonction effectue toutes les opérations de nettoyage sur le DataFrame passé en argument.
    Si le nom du fichier est précisé, la fonction télécharge la base de données au format csv.
    Sinon, la fonction renvoie le DataFrame nettoyé.
    '''

    rename_columns(data)
    changement_type_unites(data)
    ajout_postes_regroupes(data)
    ajout_IMC(data)
    new_data = suppression_lignes_vides(data)

    if nom_fichier is None :
        return new_data
    else:
        telechargement_DF(new_data,nom_fichier)


