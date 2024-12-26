import pandas as pd
from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from Fonctions_scrapping import telechargement_DF

# Modèles retenus
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

def Prediction(data,type_modele,telechargement=None):

    '''
    Cette fonction ajoute une colonne au dataframe avec le poste prédit pour chaque joueur.
    '''

    # Choix variables explicatives et variable cible
    X = data[['Taille','Poids']] 
    y = data['Poste simplifié']

    # Choix du modèle avec les meilleurs paramètres (à modifier si besoin)
    model_SVC = SVC(kernel='rbf', C=1, gamma=10 , random_state=42)
    model_RF = RandomForestClassifier(max_depth=10,min_samples_leaf=2, min_samples_split=10,n_estimators=50,random_state=42)

    dict_modele = {'SVC': model_SVC, 'RF' : model_RF}
    model = dict_modele[type_modele]
    
    # Pipeline pour standardiser les données plus facilement
    pipeline = Pipeline([('Standardisation', StandardScaler()),('modèle', model)])


    # Prédiction
    data['Poste prédit'] = cross_val_predict(pipeline, X, y, cv=5)

    # Téléchargement du DataFrame si voulu
    if telechargement:
        telechargement_DF(data,telechargement)


'''
### test de la fonction

from Nettoyage import cleaning

donnees_brutes = pd.read_csv("Donnees_physique_joueurs.csv",index_col=0)

donnees_nettoyees = cleaning(donnees_brutes)

Prediction(donnees_nettoyees)

print(donnees_nettoyees.head())
'''