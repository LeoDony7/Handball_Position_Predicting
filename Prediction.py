import pandas as pd
from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Modèles retenus
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

def Prediction(data):

    '''
    Cette fonction ajoute une colonne au dataframe avec le poste prédit pour chaque joueur.
    '''

    # Choix variables explicatives et variable cible
    X = data[['Taille','Poids']] 
    y = data['Poste simplifié']

    # Choix du modèle avec les meilleurs paramètres (à modifier si besoin)
    model = SVC(kernel='rbf', C=1, gamma=10 , random_state=42)

    # Pipeline pour standardiser les données plus facilement
    pipeline = Pipeline([('Standardisation', StandardScaler()),('modèle', model)])


    # Prédiction
    data['Poste prédit'] = cross_val_predict(pipeline, X, y, cv=5)



