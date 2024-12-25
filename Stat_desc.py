import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

## Stats descriptives 

## /!\ Enlever les appels des fonctions pour les mettre dans un autre fichier

# Visualisation de la répartition de la taille et du poids des joueurs

def Visualisation_Taille_Poids(data_set,moyenne=False,telechargement=None):

    '''
    Cette fonction renvoie le nuage de points des joueurs selon leur taille et leur poids, avec une couleur différente pour chaque poste.
    La fonction prend en argument le DataFrame contenant les données.
    On peut aussi préciser si on veut afficher les moyennes de Taille et Poids sur le graphique.
    On peut également préciser si on veut télécharger le fichier en renseignant telechargement ="nom_fichier.png"
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
        data = data_set, 
        palette = palette_dictionnaire,
        s=85,           # Taille des points
        alpha=0.8        # Transparence
        )

    if moyenne:
        # Ajout de lignes verticales et horizontales pour visualiser la moyenne du poids et de la taille dans les données
        plt.axhline(y=data_set['Poids'].mean(), color='black', linestyle="--",label='Poids moyen',linewidth=2)
        plt.axvline(x=data_set['Taille'].mean(), color='black', linestyle="--",label='Taille moyenne',linewidth=2)
    
    plt.title("Visualisation de la distribution de la taille et du poids des joueurs", fontsize=14)
    plt.xlabel("Taille (cm)", fontsize=12)
    plt.ylabel("Poids (kg)", fontsize=12)
    plt.legend(title="Poste")
    plt.grid(True)

    if telechargement:
        plt.savefig(telechargement, dpi=300, bbox_inches="tight")
    
    plt.show()


# Appel de la fonction
data = pd.read_csv("Donnees\Donnees_physiques_nettoyees.csv",index_col=0)
Visualisation_Taille_Poids(data,moyenne=True,telechargement="Graph_taille_poste_moyenne_1.png")



# Récupération de la moyenne et de la variance de la taille et du poids selon le poste

def Moyenne_et_Std(data_set):
    
    '''
    Cette fonction prend en argument le DataFrame contenant les données.
    Elle renvoie un nouveau dataframe donnant la moyenne et l'écart-type de la taille et du poids des joueurs selon leur poste.
    '''

    dictionnaire_moyenne_std={}
    for poste in data_set['Poste simplifié'].unique():
        dictionnaire_moyenne_std[poste]=[data[data['Poste simplifié']==poste]['Taille'].mean(),
                                         data[data['Poste simplifié']==poste]['Taille'].std(),
                                         data[data['Poste simplifié']==poste]['Poids'].mean(),
                                         data[data['Poste simplifié']==poste]['Poids'].std()]
        
    df_moyenne_std = pd.DataFrame.from_dict(dictionnaire_moyenne_std,orient='index')
    df_moyenne_std.columns=['Taille Moyenne','Taille Std','Poids Moyenne','Poids Std']
    return df_moyenne_std

# Appel de la fonction
print(Moyenne_et_Std(data))


## Graphique boite à moustache de la taille et du poids selon le poste

def Boxplot_taille(data,telechargement=None):

    '''
    Cette fonction prend en argument le DataFrame avec les données et renvoie un boxplot de la taille selon le poste.
    On peut également télécharger le fichier en précisant telechargement="nom_fichier.png".
    '''

    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Poste simplifié", y="Taille", data=data)
    plt.title("Répartition de la taille selon le poste")
    plt.ylabel("Taille (cm)")

    if telechargement:
        plt.savefig(telechargement, dpi=300, bbox_inches="tight")

    plt.show()

def Boxplot_poids(data,telechargement=None):

    '''
    Cette fonction prend en argument le DataFrame avec les données et renvoie un boxplot du poids selon le poste.
    On peut également télécharger le fichier en précisant telechargement="nom_fichier.png".
    '''

    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Poste simplifié", y="Poids", data=data)
    plt.title("Répartition du poids selon le poste")
    plt.ylabel("Poids (kg)")

    if telechargement:
        plt.savefig(telechargement, dpi=300, bbox_inches="tight")

    plt.show()

# Appel des fonctions
Boxplot_taille(data)
Boxplot_poids(data)


## Ajout des fonctions faites par Jame dans le fichier du nettoyage

from sklearn.linear_model import LinearRegression


# /!\ J'ai rajouté une option de téléchargement du graphique et j'ai mis plt.figure et plt.show direct dans la fonction
def afficher_regression_par_poste(data,telechargement=None):

    '''
    Cette fonction prend en argument un DataFrame, et optionnellement un nom pour télécharger le fichier.
    Elle renvoie le nuage de points des joueurs selon leur taille et leur poids, avec une régression entre taille et poids pour chaque poste.
    Si l'argument téléchargement (format nom_fichier.csv) est renseigné, le graphique est téléchargé sous ce nom dans le repertoire actuel.
    '''    
    
    model = LinearRegression()  
    couleurs = sns.color_palette("husl", len(data["Poste simplifié"].unique()))

    plt.figure(figsize=(10, 6))

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

    if telechargement:
        plt.savefig(telechargement, dpi=300, bbox_inches="tight")

    plt.show()



### Violin Plot, un genre de boite à moustache améliorée

def afficher_violinplot(data, y, palette="viridis"):
    
    '''
    Affiche un Violin Plot pour une variable donnée en fonction des postes simplifiés.
    
    Paramètres :
    - data : DataFrame contenant les données.
    - y : str, nom de la colonne à afficher sur l'axe des ordonnées.
    - palette : str, palette de couleurs pour le graphique.
    '''

    sns.violinplot(x="Poste simplifié", y=y, data=data, palette=palette)
    plt.show()


# Droite de régression basique entre 2 variables

def nuage_droite(data, x, y):
    
    '''
    Affiche un nuage de points avec une droite de régression entre deux variables.
    
    Paramètres :
    - data : DataFrame contenant les données.
    - x : str, nom de la colonne à afficher sur l'axe des abscisses.
    - y : str, nom de la colonne à afficher sur l'axe des ordonnées.
    '''
    
    sns.regplot(x=x, y=y, data=data)
    plt.title(f"Nuage de points avec droite de tendance : {x} vs {y}")
    plt.show()


# Nuage de points interactif

import plotly.express as px

def scatter_plot(data, x, y, hover_data):

    '''
    Crée un graphique de dispersion avec Plotly, avec des informations supplémentaires en survol.
    
    Paramètres :
    - data : DataFrame contenant les données à visualiser.
    - x : str, nom de la colonne pour l'axe des abscisses.
    - y : str, nom de la colonne pour l'axe des ordonnées.
    - hover_data : list, colonnes à afficher lors du survol des points.
    '''

    data_copy = data.copy()
    # Travail avec une copie pour pas modifier l'index du tableau original
    data_copy = data_copy.reset_index()
    data_copy = data_copy.rename(columns={'index': 'Nom'}) 

    fig = px.scatter(data_copy, x=x, y=y, color="Poste", hover_data=hover_data)
    fig.show()