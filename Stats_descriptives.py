import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
 
###Nettoyage des données 

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
Enlever les lignes pour lesquelles on n'a pas de données sur les variables d'intérêt.
Cela ne concerne presque aucune ligne de notre DataFrame mais la précaution s'impose. 
"""  
    new_data = data.dropna(subset=['Poste', 'Taille', 'Poids'])
    return new_data

def ajout_postes_regroupes_IMC(data):
"""
Ajouter une colonne en regroupant les postes en 4 catégories.
Ajout d'une colonne pour une nouvelle variable IMC.
""" 
    postes_regroupes = {"Arrière Droit" : "Arrière",
           "Arrière Gauche" : "Arrière",
           "Ailier Droit" : "Ailier",
           "Ailier Gauche" : "Ailier"}
    
    data["Poste simplifié"]= data["Poste"].replace(postes_regroupes)
    
    data["IMC"] = data["Poids"] / ((data["Taille"]/100) ** 2)


def cleaning(data):
"""
Fonction qui compile tout le nettoyage des données
Elle retourne un nouveau DataFrame netoyé.
"""  
    rename_columns(data)
    changement_type_unites(data)
    ajout_postes_regroupes(data)
    new_data = suppression_lignes_vides(data)
    return new_data



def afficher_regression_par_poste(data):
"""
Afficher les points et les droites de régression linéaire pour chaque poste simplifié.
La fonction prend pour argument le DataFrame. Il faut donc s'assurer que les variables sont dans un format exploitable.
"""
    model = LinearRegression()  
    couleurs = sns.color_palette("husl", len(data["Poste simplifié"].unique()))

    for i, poste in enumerate(data["Poste simplifié"].unique()):
        subset = data[data["Poste simplifié"] == poste]

        X = subset['Taille'].values.reshape(-1, 1)  # Format requis pour LinearRegression
        y = subset['Poids'].values
     
        model.fit(X, y)
        y_pred = model.predict(X)

        plt.scatter(subset['Taille'], subset['Poids'], color=couleurs[i], label=poste)
        plt.plot(subset['Taille'], y_pred, color=couleurs[i], linestyle='--')

    plt.xlabel("Taille (cm)")
    plt.ylabel("Poids (kg)")
    plt.title("Relation entre Taille et Poids selon le Poste avec régression")
    plt.legend(loc="best")
    plt.grid(True)

"""
Exemple d'utilisation du pipeline complet

# Chargement des données brutes
data = pd.read_csv("Donnees_physique_joueurs.csv", index_col=0)

# Nettoyage des données
data_cleaned = cleaning(data, "Donnees_physique_nettoyees.csv")

# Création du graphique final
plt.figure(figsize=(10, 6))
afficher_regression_par_poste(data_cleaned)
plt.show()
plt.show()
"""

### Violin Plot, un genre de boite à moustache améliorée

def afficher_violinplot(data, y, palette="viridis"):
    """
    Affiche un Violin Plot pour une variable donnée en fonction des postes simplifiés.
    Elle prend pour paramètres un DataFrame, une variable d'intérêt (str) à choisit entre le poids, la taille ou l'IMC par exemple. 
    La palette initiale est "viridis" et nous conseillons la palette "plasma" qui est dans le même style. 
    """

    sns.violinplot(x="Poste simplifié", y=y, data=data, palette=palette)
    plt.show()

### Droite de régression basique entre 2 variables
def nuage_droite(data, x, y):
    """
    Affiche un nuage de points avec une droite de régression entre deux variables.
    Elle prend pour paramètres un DataFrame et deux variables d'intérêt (str).
    
    Exemple d'usage :
    nuage_droite(data, "Âge", "IMC")
    """
    
    sns.regplot(x=x, y=y, data=data)
    plt.title(f"Nuage de points avec droite de tendance : {x} vs {y}")
    plt.show()


### Nuage de points interactif

import plotly.express as px

def scatter_plot(data, x, y, hover_data):
    """
    Crée un graphique de dispersion avec Plotly, avec des informations supplémentaires en survol.
    La partie hover_data doit être une liste de noms de colonnes que l'on souhaite afficher en survolant les poids du nuage. 
    
    Exemple d'usage : 
    scatter_plot(data, "Taille","Poids", ["Nom", "Âge", "IMC"])    
    """

    data_copy = data.copy()
    # Travail avec une copie pour pas modifier l'index du tableau original
    data_copy = data_copy.reset_index()
    data_copy = data_copy.rename(columns={'index': 'Nom'}) 

    fig = px.scatter(data_copy, x=x, y=y, color="Poste", hover_data=hover_data)
    fig.show()



