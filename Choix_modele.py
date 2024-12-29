## Choix du modèle et des paramètres pour prédire le poste des joueurs

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

# Modèles testés : KNN, SVM et Random Forest
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier


# Préparation des données pour l'entrainement et le test d'un modèle 

def preparation_donnees(dataframe,taille_test=0.2):
    
    '''
    Renvoie les données séparées et standardisées en vue de l'entrainement et le test d'un modèle.
    80% des données servent à l'entrainement, les 20% restantes servent au test.
    Nous avons décidé d'effectuer une stratification afin d'avoir chacune des modalités de la variable cible dans la même proportion dans chaque échantillon.

    Paramètres :
        - dataframe : Un DataFrame pandas contenant les données morphologiques des joueurs et leur poste.
        - taille_test : Un nombre entre 0 et 1. Il définit la proportion de données à envoyer dans l'échantillon de test. Par défaut, fixé à 0,2.
    '''

    # Choix variables explicatives et variable cible
    X = dataframe[['Taille','Poids']] 
    y = dataframe['Poste simplifié']

    # Séparation données entre entrainement et test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=taille_test, random_state=42, stratify=y)

    # Standardisation des données
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test


# Choix paramètres pour KNN

def parametre_KNN(dataframe):

    '''
    Renvoie un graphique représentant des métriques balanced accuracy et f1-score (macro) en fonction du nombres de voisins k du modèle KNN.
    Du fait de la taille du dataset, une validation croisée à 5 plis est effectuée pour des résultats plus robustes.

    Paramètres :
        - dataframe : Un DataFrame pandas contenant les données morphologiques des joueurs et leur poste.
    '''


    X_train, X_test, y_train, y_test = preparation_donnees(dataframe)

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


# Choix paramètres pour SVM

def parametres_SVM(dataframe,metrique='accuracy'):

    '''
    Renvoie le couple de paramètres (C,gamma) donnant le meilleur score selon la métrique passée en argument.
    Le choix a été fait de fixer kernel = 'rbf' du fait de la distribution des données.
    Les couples possibles sont dans un ensemble discret.

    Paramètres : 
        - dataframe : Un DataFrame contenant les données morphologiques des joueurs et leur poste.
        - metrique : une chaine de caractère. Elle correspond à la métrique selon laquelle optimiser.
    '''

    X_train, X_test, y_train, y_test = preparation_donnees(dataframe)

    # Optimisation des hyperparamètres avec GridSearchCV
    param_grid = {'C': [0.1, 1, 10, 100],
                  'gamma': ['scale', 0.01, 0.1, 1, 10]
                  }
    grid = GridSearchCV(SVC(kernel='rbf'), param_grid, scoring=metrique, refit=False, verbose=1, cv=5)
    grid.fit(X_train, y_train)

    # Afficher les meilleurs paramètres
    return grid.best_params_


# Choix paramètres pour Random Forest

def parametres_Random_Forest(data, metrique='accuracy'):

    '''
    Renvoie la combinaison de paramètres donnant le meilleur score selon la métrique passée en argument.
    Les combinaisons possibles sont dans un ensemble discret.

    Paramètres : 
        - dataframe : Un DataFrame contenant les données morphologiques des joueurs et leur poste.
        - metrique : une chaine de caractère. Elle correspond à la métrique selon laquelle optimiser.
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

