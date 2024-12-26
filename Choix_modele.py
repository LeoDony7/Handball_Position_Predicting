## Choix du modèle pour prédire le poste des joueurs

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

# Modèles testés : KNN, SVM et Random Forest
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

def preparation_donnees(data,taille_test=0.2):
    
    '''
    Cette fonction permet de préparer l'entrainement d'un modèle en séparant les données entre échantillon d'entrainement et de test, puis standardise les données.
    Elle prend en argument la taille de l'échantillon de test par rapport à la taille des données. La valeur par défaut est 20%, qui est une valeur usuelle.
    Le choix a été fait de fixer l'aléa de la séparation des données, tout en stratifiant pour garder les proportions des postes dans chaque échantillon.
    '''

    # Choix variables explicatives et variable cible
    X = data[['Taille','Poids']] 
    y = data['Poste simplifié']

    # Séparation données entre entrainement et test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=taille_test, random_state=42, stratify=y)

    # Standardisation des données
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test

def parametre_KNN(data):

    '''
    Cette fonction permet d'évaluer les performances de KNN en fonction du k choisi, afin de déterminer le k optimal.
    Elle renvoie une représentation graphique des métriques "Balanced Accuracy" et "F1_macro" en fonction de k.
    Du fait de la taille du dataset, une validation croisée à 5 plis est effectuée pour des résultats plus robustes.
    '''

    X_train, X_test, y_train, y_test = preparation_donnees(data)

    k_values = range(1, 20)
    scores_acc = []
    scores_f1 = []

    for k in k_values:
        knn = KNeighborsClassifier(n_neighbors=k)
        score_accuracy = cross_val_score(knn, X_train, y_train, cv=5, scoring='balanced_accuracy')
        score_f1 = cross_val_score(knn, X_train, y_train, cv=5, scoring='f1_macro')
        scores_acc.append(score_accuracy.mean())
        scores_f1.append(score_f1.mean())

    # Visualisation des résultats
    plt.figure(figsize=(8, 6))
    plt.plot(k_values, scores_acc, marker='o', color= 'blue', label=' Balanced accuracy (validation croisée)')
    plt.plot(k_values, scores_f1, marker='o', color='red', label='F1_macro (validation croisée)')
    plt.title("Choix du meilleur k")
    plt.xlabel("Valeur de k")
    plt.xticks(k_values)
    plt.legend()
    plt.grid()
    plt.show()


def parametres_SVM(data,metrique='accuracy'):

    '''
    Cette fonction renvoie, en fonction de la métrique en argument, le couple de paramètre (C, gamma) donnant le meilleur score à la classification via SVM.
    Le choix a été fait de fixer kernel = 'rb' du fait de la distribution des données.
    '''

    X_train, X_test, y_train, y_test = preparation_donnees(data)

    # Optimisation des hyperparamètres avec GridSearchCV
    param_grid = {'C': [0.1, 1, 10, 100],
                  'gamma': ['scale', 0.01, 0.1, 1, 10]
                  }
    grid = GridSearchCV(SVC(kernel='rbf'), param_grid, scoring=metrique, refit=False, verbose=2, cv=5)
    grid.fit(X_train, y_train)

    # Afficher les meilleurs paramètres
    return grid.best_params_

'''
data = pd.read_csv("Donnees\Donnees_physiques_nettoyees.csv")
'''

'''
print(parametres_SVM(data,metrique='f1_macro')) # resultat {'C': 1, 'gamma': 10}
print(parametres_SVM(data,metrique='balanced_accuracy')) # resultat : {'C': 100, 'gamma': 0.01}
'''

def parametres_Random_Forest(data, metrique='accuracy'):

    '''
    
    '''

    X_train, X_test, y_train, y_test = preparation_donnees(data)

    param_grid = {'n_estimators': [50, 100, 200],   # Nombre d'arbres
                  'max_depth': [None, 10, 20, 30], # Profondeur maximale des arbres
                  'min_samples_split': [2, 5, 10], # Minimum d'échantillons pour diviser un nœud
                  'min_samples_leaf': [1, 2, 4] # Minimum d'échantillons par feuille
                  }

    # Recherche avec GridSearchCV
    grid = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, scoring=metrique, cv=5, verbose=2, n_jobs=-1)
    grid.fit(X_train, y_train)

    # Affichage des meilleurs paramètres
    return grid.best_params_

'''
print(parametres_Random_Forest(data,'f1_macro'))
# resultat {'max_depth': 10, 'min_samples_leaf': 2, 'min_samples_split': 10, 'n_estimators': 50}
print(parametres_Random_Forest(data,'balanced_accuracy'))
# resultat {'max_depth': None, 'min_samples_leaf': 2, 'min_samples_split': 10, 'n_estimators': 50}
'''
