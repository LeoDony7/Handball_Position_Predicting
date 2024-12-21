## Stats descriptives 

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


data = pd.read_csv("Donnees\Donnees_physiques_nettoyees.csv",index_col=0)


## Visualisation de la repartition de la taille et du poids des joueurs

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
        plt.axhline(y=data['Poids'].mean(), color='black', linestyle="--",label='Poids moyen',linewidth=2)
        plt.axvline(x=data['Taille'].mean(), color='black', linestyle="--",label='Taille moyenne',linewidth=2)
    
    plt.title("Visualisation de la distribution de la taille et du poids des joueurs", fontsize=14)
    plt.xlabel("Taille (cm)", fontsize=12)
    plt.ylabel("Poids (kg)", fontsize=12)
    plt.legend(title="Poste")
    plt.grid(True)

    if telechargement:
        plt.savefig(telechargement, dpi=300, bbox_inches="tight")
    
    plt.show()

# Appel de la fonction
Visualisation_Taille_Poids(data,moyenne=True,telechargement="Graph_taille_poste_moyenne_1.png")


## Récupération de la moyenne et de la variance de la taille et du poids selon le poste

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
