import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
 
###Nettoyage des données 

"from Fonctions_scrapping import telechargement_DF"

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

def ajout_postes_regroupes_IMC(data):
"""
Ajouter une colonne en regroupant les postes en 4 catégories 
""" 
    postes_regroupes = {"Arrière Droit" : "Arrière",
           "Arrière Gauche" : "Arrière",
           "Ailier Droit" : "Ailier",
           "Ailier Gauche" : "Ailier"}
    
    data["Poste simplifié"]= data["Poste"].replace(postes_regroupes)
    
    data["IMC"] = data["Poids"] / ((data["Taille"]/100) ** 2)


def cleaning(data,nom_fichier):
"""
Fonction finale qui compile tout le nettoyage des données
A MODIFIER Pour choisir entre return ou télécharger les nouvelles données
"""  
    rename_columns(data)
    changement_type_unites(data)
    ajout_postes_regroupes(data)
    new_data = suppression_lignes_vides(data)
    #telechargement_DF(new_data,nom_fichier)
    return new_data

def afficher_regression_par_poste(data):
"""
Afficher les points et les droites de régression linéaire pour chaque poste simplifié.
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


### Exemple d'utilisation du pipeline complet
# Chargement des données brutes
data = pd.read_csv("Donnees_physique_joueurs.csv", index_col=0)

# Nettoyage des données
data_cleaned = cleaning(data, "Donnees_physique_nettoyees.csv")

# Création du graphique final
plt.figure(figsize=(10, 6))
afficher_regression_par_poste(data_cleaned)
plt.show()
plt.show()


### Violin Plot, un genre de boite à moustache améliorée

def afficher_violinplot(data, y, palette="viridis"):
    """
    Affiche un Violin Plot pour une variable donnée en fonction des postes simplifiés.
    
    Paramètres :
    - data : DataFrame contenant les données.
    - y : str, nom de la colonne à afficher sur l'axe des ordonnées.
    - palette : str, palette de couleurs pour le graphique.
    """

    sns.violinplot(x="Poste simplifié", y=y, data=data, palette=palette)
    plt.show()

### Droite de régression basique entre 2 variables
def nuage_droite(data, x, y):
    """
    Affiche un nuage de points avec une droite de régression entre deux variables.
    
    Paramètres :
    - data : DataFrame contenant les données.
    - x : str, nom de la colonne à afficher sur l'axe des abscisses.
    - y : str, nom de la colonne à afficher sur l'axe des ordonnées.
    """
    
    sns.regplot(x=x, y=y, data=data)
    plt.title(f"Nuage de points avec droite de tendance : {x} vs {y}")
    plt.show()

# Exemple : 
# nuage_droite(data, x="Âge", y="IMC")



### Nuage de points interactif

import plotly.express as px

def scatter_plot(data, x, y, hover_data):
    """
    Crée un graphique de dispersion avec Plotly, avec des informations supplémentaires en survol.
    
    Paramètres :
    - data : DataFrame contenant les données à visualiser.
    - x : str, nom de la colonne pour l'axe des abscisses.
    - y : str, nom de la colonne pour l'axe des ordonnées.
    - hover_data : list, colonnes à afficher lors du survol des points.
    """

    data_copy = data.copy()
    # Travail avec une copie pour pas modifier l'index du tableau original
    data_copy = data_copy.reset_index()
    data_copy = data_copy.rename(columns={'index': 'Nom'}) 

    fig = px.scatter(data_copy, x=x, y=y, color="Poste", hover_data=hover_data)
    fig.show()

# Exemple : 
# scatter_plot(data, x="Taille", y="Poids", color="Poste", hover_data=["Nom", "Âge", "IMC"])



