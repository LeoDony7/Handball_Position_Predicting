import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

 
###Nettoyage des données 

from Fonctions_scrapping import telechargement_DF

def rename_columns(data):
"""
Renommer les colonnes avec les noms choisis
"""  
    noms_colonnes = ["Poste", "Nationalité", "Date de naissance",
                 "Âge", "Taille", "Poids", "Club actuel", "Dernière saison"]
    data.columns = noms_colonnes

def changement_type_unites(data,type='float'):
"""
Enlever les unités et changer le type des données vers un type choisi dans le second argument de la fonction
"""  
    data["Âge"] = data["Âge"].str.replace(r" ans", "", regex=True).astype(type)
    data["Taille"] = data["Taille"].str.replace(r" cm", "", regex=True).astype(type)
    data["Poids"] = data["Poids"].str.replace(r" kgs", "", regex=True).astype(type)

def suppression_lignes_vides(data):
"""
Enlever les lignes pour lesquelles on n'a pas de données sur les variables d'intérêt
"""  
    new_data = data.dropna(subset=['Poste', 'Taille', 'Poids'])
    return new_data

def ajout_postes_regroupes(data):
"""
Ajouter une colonne en regroupant les postes en 4 catégories 
""" 
    postes_regroupes = {"Arrière Droit" : "Arrière",
           "Arrière Gauche" : "Arrière",
           "Ailier Droit" : "Ailier",
           "Ailier Gauche" : "Ailier"}
    
    data["Poste simplifié"]= data["Poste"].replace(postes_regroupes)

def cleaning(data,nom_fichier):
"""
Fonction finale qui compile tout le nettoyage des données
"""  
    rename_columns(data)
    changement_type_unites(data)
    ajout_postes_regroupes(data)
    new_data = suppression_lignes_vides(data)
    telechargement_DF(new_data,nom_fichier)


# Initialiser le modèle de régression linéaire
model = LinearRegression()

# Fonction pour afficher les points et une droite de régression
def afficher_regression_et_points(dataset, color, label):

    X = dataset['Taille'].values.reshape(-1, 1)  # 2D requis pour LinearRegression
    y = dataset['Poids'].values

    model.fit(X, y)
    y_pred = model.predict(X)

    plt.scatter(dataset['Taille'], dataset['Poids'], color=color, label=label)
    plt.plot(dataset['Taille'], y_pred, color=color, linestyle='--', label=f"Régression ({label})")

# Créer le graphique
plt.figure(figsize=(10, 6))

# Ajouter les points et les droites pour chaque groupe
afficher_regression_et_points(data_pivot, 'red', 'Pivot')
afficher_regression_et_points(data_arriere, 'blue', 'Arrière')
afficher_regression_et_points(data_centre, 'green', 'Centre')
afficher_regression_et_points(data_ailier, 'orange', 'Ailier')

# Ajouter des labels et une légende
plt.xlabel("Taille (cm)")
plt.ylabel("Poids (kg)")
plt.title("Relation entre Taille et Poids selon le Poste avec régression")
plt.legend(loc="best", fontsize=10)
plt.grid(True)
plt.show()





