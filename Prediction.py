## Prédiction sur l'ensemble des données

from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, f1_score
import seaborn as sns
import matplotlib.pyplot as plt

from Fonctions_scrapping import telechargement_DF

# Modèles retenus
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier


# Prédiction

def Prediction(dataframe,type_modele,nom_fichier=None):

    '''
    Ajoute à un DataFrame une colonne contenant le poste des joueurs, prédit selon le modèle passé en argument.
    Possibilité de télécharger le DataFrame modifié.

    Paramètres :
        - dataframe : Un DataFrame pandas contenant les informations morphologiques des joueurs.
        - modele : une chaine de caractère à choisir parmi 'SVC' et 'RF'. Elle définit le modèle à utiliser pour la prédiction.
        - nom_fichier (optionnel): chaine de caractères de la forme "nom_fichier.csv". Si renseigné, télécharge le DataFrame traité au format csv sous le nom renseigné.   
    '''

    # Choix variables explicatives et variable cible
    X = dataframe[['Taille','Poids']] 
    y = dataframe['Poste simplifié']

    # Choix du modèle avec les meilleurs paramètres (à modifier si besoin)
    model_SVC = SVC(kernel='rbf', C=1, gamma=10 , random_state=42)
    model_RF = RandomForestClassifier(max_depth=10,min_samples_leaf=2, min_samples_split=10,n_estimators=50,random_state=42)

    dict_modele = {'SVC': model_SVC, 'RF' : model_RF}
    model = dict_modele[type_modele]
    
    # Pipeline pour standardiser les données plus facilement
    pipeline = Pipeline([('Standardisation', StandardScaler()),('modèle', model)])


    # Prédiction
    dataframe['Poste prédit'] = cross_val_predict(pipeline, X, y, cv=5)

    # Téléchargement du DataFrame si voulu
    if nom_fichier:
        telechargement_DF(dataframe,nom_fichier)


# Rapport de classification sur l'ensemble des données 

def Rapport_prediction(dataframe):

    '''
    Renvoie la matrice de confusion de la prédiction contenue dans le DataFrame passé en argument.
    Affiche également le F1-score (macro).

    Paramètres :
        - dataframe : Un DataFrame pandas contenant les postes prédits des joueurs.
    '''

    conf_matrix = confusion_matrix(dataframe['Poste simplifié'], dataframe['Poste prédit'])
    f1_macro = f1_score(dataframe['Poste simplifié'], dataframe['Poste prédit'], average='macro')
    plt.figure(figsize=(10, 8))
    sns.heatmap(conf_matrix,
                annot=True,
                cmap='Blues',
                fmt='d',
                xticklabels=True,
                yticklabels=True)
    plt.title(f'Matrice de confusion après la prédiction \n F1 (macro): {f1_macro:.2f}', fontsize=12)
    plt.xlabel("Prédictions")
    plt.ylabel("Vérités")
    plt.show()