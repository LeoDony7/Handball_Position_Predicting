## Stats descriptives

import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression



# Visualisation de la répartition de la taille et du poids des joueurs

def Visualisation_Taille_Poids(dataframe,moyenne=False,nom_fichier=None):

    '''
    Renvoie le nuage de points des joueurs selon leur taille et leur poids, avec une couleur différente pour chaque poste.
    On a la possibilité d'afficher les moyennes de Taille et Poids sur le graphique.
    On a également la possibilité de télécharger le graphique en renseignant nom_fichier.

    Paramètres :
        - dataframe : Un DataFrame pandas contenant les données joueurs et ayant été nettoyé.
        - moyenne (optionnel) : Un Booléen permettant d'afficher ou non les moyennes de Taille et Poids sur le graphique. Par défaut, False.
        - nom_fichier : Une chaine de caractère de la forme "nom_fichier.csv". Nom qu'on souhaite donner au fichier.
    '''

    # Couleurs pour l'affichage
    palette_dictionnaire = {"Demi Centre": "green",
                            "Ailier": "orange",
                            "Pivot": "red",
                            "Arrière": "blue"}

    # Création de la figure
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x = 'Taille', 
        y = 'Poids', 
        hue = 'Poste simplifié', 
        data = dataframe, 
        palette = palette_dictionnaire,
        s=85,           # Taille des points
        alpha=0.8        # Transparence
        )

    if moyenne:
        # Ajout de lignes verticales et horizontales pour visualiser la moyenne du poids et de la taille dans les données
        plt.axhline(y=dataframe['Poids'].mean(), color='black', linestyle="--",label='Poids moyen',linewidth=2)
        plt.axvline(x=dataframe['Taille'].mean(), color='black', linestyle="--",label='Taille moyenne',linewidth=2)
    
    plt.title("Visualisation de la distribution de la taille et du poids des joueurs", fontsize=14)
    plt.xlabel("Taille (cm)", fontsize=12)
    plt.ylabel("Poids (kg)", fontsize=12)
    plt.legend(title="Poste")
    plt.grid(True)

    if nom_fichier:
        plt.savefig(nom_fichier, dpi=300, bbox_inches="tight")
    
    plt.show()



# Récupération de la moyenne et de la variance de la taille et du poids selon le poste

def Moyenne_et_Std(dataframe):
    
    '''
    Crée un dictionnaire résumant la moyenne et l'écart type du poids et de la taille des joueurs selon leur poste.
    
    Paramètres :
        - dataframe : Un DataFrame pandas contenant les données joueurs et ayant été nettoyé. 
    '''

    dictionnaire_moyenne_std={}
    for poste in dataframe['Poste simplifié'].unique():
        dictionnaire_moyenne_std[poste]=[dataframe[dataframe['Poste simplifié']==poste]['Taille'].mean(),
                                         dataframe[dataframe['Poste simplifié']==poste]['Taille'].std(),
                                         dataframe[dataframe['Poste simplifié']==poste]['Poids'].mean(),
                                         dataframe[dataframe['Poste simplifié']==poste]['Poids'].std()]
        
    df_moyenne_std = pd.DataFrame.from_dict(dictionnaire_moyenne_std,orient='index')
    df_moyenne_std.columns=['Taille Moyenne','Taille Std','Poids Moyenne','Poids Std']
    return df_moyenne_std



## Graphique boite à moustache de la taille et du poids selon le poste

def Boxplot_taille(dataframe,nom_fichier=None):

    '''
    Renvoie un boxplot de la taille selon le poste.
    On a la possibilité de télécharger le graphique en renseignant nom_fichier.

    Paramètres :
        - dataframe : Un DataFrame pandas contenant les données joueurs et ayant été nettoyé.
        - nom_fichier : Une chaine de caractère de la forme "nom_fichier.csv". Nom qu'on souhaite donner au fichier.
    '''

    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Poste simplifié", y="Taille", data=dataframe)
    plt.title("Répartition de la taille selon le poste")
    plt.ylabel("Taille (cm)")

    if nom_fichier:
        plt.savefig(nom_fichier, dpi=300, bbox_inches="tight")

    plt.show()

def Boxplot_poids(data,telechargement=None):

    '''
    Renvoie un boxplot du poids selon le poste.
    On a la possibilité de télécharger le graphique en renseignant nom_fichier.

    Paramètres :
        - dataframe : Un DataFrame pandas contenant les données joueurs et ayant été nettoyé.
        - nom_fichier : Une chaine de caractère de la forme "nom_fichier.csv". Nom qu'on souhaite donner au fichier.
    '''

    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Poste simplifié", y="Poids", data=data)
    plt.title("Répartition du poids selon le poste")
    plt.ylabel("Poids (kg)")

    if telechargement:
        plt.savefig(telechargement, dpi=300, bbox_inches="tight")

    plt.show()






def afficher_regression_par_poste(dataframe,nom_fichier=None):

    '''
    Renvoie le nuage de points des joueurs selon leur taille et leur poids, avec une régression entre taille et poids pour chaque poste.
    On a la possibilité de télécharger le graphique en renseignant nom_fichier.
    
     Paramètres :
        - dataframe : Un DataFrame pandas contenant les données joueurs et ayant été nettoyé.
        - nom_fichier : Une chaine de caractère de la forme "nom_fichier.csv". Nom qu'on souhaite donner au fichier.
    '''    
    
    model = LinearRegression()  
    couleurs = sns.color_palette("husl", len(dataframe["Poste simplifié"].unique()))

    plt.figure(figsize=(10, 6))

    for i, poste in enumerate(dataframe["Poste simplifié"].unique()):
        subset = dataframe[dataframe["Poste simplifié"] == poste]

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

    if nom_fichier:
        plt.savefig(nom_fichier, dpi=300, bbox_inches="tight")

    plt.show()



### Violin Plot, un genre de boite à moustache améliorée

def afficher_violinplot(dataframe, y, palette="viridis"):
    
    '''
    Affiche un Violin Plot pour une variable donnée en fonction des postes simplifiés.
    
    Paramètres :
        - dataframe : Un DataFrame  pandas contenant les données joueurs et ayant été nettoyé.
        - y : str, nom de la colonne à afficher sur l'axe des ordonnées.
        - palette : str, palette de couleurs pour le graphique.
    '''

    sns.violinplot(x="Poste simplifié", y=y, data=dataframe, palette=palette)
    plt.show()


# Droite de régression basique entre 2 variables

def nuage_droite(dataframe, x, y):
    
    '''
    Affiche un nuage de points avec une droite de régression entre deux variables.
    
    Paramètres :
        - dataframe : Un DataFrame  pandas contenant les données joueurs et ayant été nettoyé.
        - x : str, nom de la colonne à afficher sur l'axe des abscisses.
        - y : str, nom de la colonne à afficher sur l'axe des ordonnées.
    '''
    
    sns.regplot(x=x, y=y, data=dataframe)
    plt.title(f"Nuage de points avec droite de tendance : {x} vs {y}")
    plt.show()


# Nuage de points interactif


def scatter_plot(dataframe, x, y, hover_data):

    '''
    Crée un graphique de dispersion avec Plotly, avec des informations supplémentaires en survol.
    
    Paramètres :
        - dataframe : Un DataFrame  pandas contenant les données joueurs et ayant été nettoyé.
        - x : str, nom de la colonne pour l'axe des abscisses.
        - y : str, nom de la colonne pour l'axe des ordonnées.
        - hover_data : list, colonnes à afficher lors du survol des points.
    '''

    data_copy = dataframe.copy()
    # Travail avec une copie pour pas modifier l'index du tableau original
    data_copy = data_copy.reset_index()
    data_copy = data_copy.rename(columns={'index': 'Nom'}) 

    fig = px.scatter(data_copy, x=x, y=y, color="Poste", hover_data=hover_data)
    fig.show()