import pandas as pd
from sklearn.linear_model import LinearRegression
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



