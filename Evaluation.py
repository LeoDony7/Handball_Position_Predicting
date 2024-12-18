import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, f1_score

# Modèles testés : KNN, SVM et Random Forest
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

from Choix_modele import preparation_donnees


## On va faire des fonctions qui servent directement à évaluer les performances en utilisant seulement le .predict

## Ensuite on fera une fonction qui prédit effectivement sur l'ensemble du dataset en utilisant .cros_val_predict

def Eval_modele_KNN(data,k):

    '''
    Cette fonction prend en argument un DataFrame et un k.

    '''
    
    # Préparation des données
    X_train, X_test, y_train, y_test = preparation_donnees(data)

    # Entrainement du modèle KNN sur les données d'entrainement
    knn_model = KNeighborsClassifier(n_neighbors=k)
    knn_model.fit(X_train, y_train)

    # Prédiction sur les données de test
    y_pred = knn_model.predict(X_test)

    # Évaluation du modèle
    conf_matrix = confusion_matrix(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average='macro')
    plt.figure(figsize=(10, 8))
    sns.heatmap(conf_matrix,
                annot=True,
                cmap='Blues',
                fmt='d',
                xticklabels=knn_model.classes_,
                yticklabels=knn_model.classes_)
    plt.title(f'Matrice de confusion KNN avec k={k}\n F1 (macro): {f1_macro:.2f}', fontsize=12)

    plt.xlabel("Prédictions")
    plt.ylabel("Vérités")
    plt.show()

    #return classification_report(y_test, y_pred)

data = pd.read_csv("Donnees\Donnees_physiques_nettoyees.csv")
Eval_modele_KNN(data,5)


def Eval_modele_SVM(data,parametres : dict):

    '''
    Cette fonction prend en argument un DataFrame et les paramètres du modèle SVM.
    '''

    # Préparation des données
    X_train, X_test, y_train, y_test = preparation_donnees(data)

    # Entrainement du modèle SVM sur les données d'entrainement 
    svm_model = SVC(kernel=parametres['kernel'], C= parametres['C'], gamma= parametres['gamma'], random_state=42)
    svm_model.fit(X_train, y_train)

    # Prédiction sur l'ensemble de test
    y_pred = svm_model.predict(X_test)

    # Évaluation du modèle
    conf_matrix = confusion_matrix(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average='macro')
    plt.figure(figsize=(10, 8))
    sns.heatmap(conf_matrix,
                annot=True,
                cmap='Blues',
                fmt='d',
                xticklabels=svm_model.classes_,
                yticklabels=svm_model.classes_)
    plt.title(f'Matrice de confusion SVM avec {parametres}\n F1 (macro): {f1_macro:.2f}', fontsize=12)
    plt.xlabel("Prédictions")
    plt.ylabel("Vérités")
    plt.show()

best_param_SVM={'kernel': 'rbf','C': 1, 'gamma': 10}
Eval_modele_SVM(data,best_param_SVM)


def Eval_modele_Random_Forest(data,parametres : dict):
    
    '''
    
    '''

    # Préparation des données
    X_train, X_test, y_train, y_test = preparation_donnees(data)

    rf_model = RandomForestClassifier(random_state=42,max_depth=parametres['max_depth'], min_samples_leaf=parametres['min_samples_leaf'],min_samples_split=parametres['min_samples_split'],n_estimators=parametres['n_estimators'])
    rf_model.fit(X_train, y_train)

    # Prédiction sur l'ensemble de test
    y_pred = rf_model.predict(X_test)

    # Évaluation du modèle
    conf_matrix = confusion_matrix(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average='macro')
    plt.figure(figsize=(10, 8))
    sns.heatmap(conf_matrix,
                annot=True,
                cmap='Blues',
                fmt='d',
                xticklabels=rf_model.classes_,
                yticklabels=rf_model.classes_)
    plt.title(f'Matrice de confusion Random Forest avec : \n{parametres}\n F1 (macro): {f1_macro:.2f}', fontsize=12)
    plt.xlabel("Prédictions")
    plt.ylabel("Vérités")
    plt.show()

best_param_RF = {'max_depth': 10, 'min_samples_leaf': 2, 'min_samples_split': 10, 'n_estimators': 50}

Eval_modele_Random_Forest(data,best_param_RF)