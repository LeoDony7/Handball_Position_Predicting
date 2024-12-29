## Evaluation des performances des différents modèles selon les paramètres choisis

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, f1_score

# Modèles testés : KNN, SVM et Random Forest
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

from Choix_modele import preparation_donnees


# Evaluation du modèle KNN

def Eval_modele_KNN(dataframe,k):

    '''
    Renvoie la matrice de confusion et le F1-score (macro) liés à la prédiction faite par le modèle KNN paramétré selon le k passé en argument.

    Paramètres :
        - dataframe : Un DataFrame pandas contenant les données morphologiques des joueurs et leur poste.
        - k : un entier. Il s'agit du nombre de voisins utilisé comme paramètre pour le modèle KNN utilisé.
    '''
    
    # Préparation des données
    X_train, X_test, y_train, y_test = preparation_donnees(dataframe)

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



# Evaluation du modèle SVM

def Eval_modele_SVM(dataframe,parametres : dict):

    '''
    Renvoie la matrice de confusion et le F1-score (macro) liés à la prédiction faite par le modèle SVM paramétré selon le dictionnaire de paramètres passé en argument.
    
    Paramètres:
        - dataframe : Un DataFrame pandas contenant les données morphologiques des joueurs et leur poste.
        - parametres : Un Dictionnaire python contenant à minima les clés suivantes : 'kernel', 'C' et 'gamma'.
    '''

    # Préparation des données
    X_train, X_test, y_train, y_test = preparation_donnees(dataframe)

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



# Evaluation du modèle Random Forest

def Eval_modele_Random_Forest(data,parametres : dict):
    
    '''
    Renvoie la matrice de confusion et le F1-score (macro) liés à la prédiction faite par le modèle Random Forest paramétré selon le dictionnaire de paramètres passé en argument.
    
    Paramètres:
        - dataframe : Un DataFrame pandas contenant les données morphologiques des joueurs et leur poste.
        - parametres : Un Dictionnaire python contenant à minima les clés suivantes : 'max_depth', 'min_samples_leaf', 'min_samples_split' et 'n_estimators'.
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
