## Traitement et Nettoyage du DataFrame contenant les données de matchs

import pandas as pd
import numpy as np
from Fonctions_scrapping import telechargement_DF


# Fonction qui normalise le nom d'un joueur

def normalisation(nom_joueur):

    '''
    Normalise le nom d'un joueur au format Prénom Nom.

    Paramètres :
        - nom_joueur : chaine de caractère de la forme "NOM Prénom". Le nom et le prénom peuvent éventuellement faire plusieurs mots.
    '''

    mots = nom_joueur.split()

    if len(mots)==2:
        return ' '.join([mots[1].capitalize(),mots[0].capitalize()])
    elif len(mots) >=3 :
        nom=[]
        prenom= []
        for mot in mots:
            if mot.isupper():
                nom.append(mot.capitalize())
            else:
                prenom.append(mot.capitalize())
        return ' '.join(prenom+nom)
    else :
        return nom_joueur


# Fonction qui applique le formatage à un DataFrame

def nom_formate(dataframe):

    '''
    Ajoute à un DataFrame une colonne contenant les noms formatés selon la fonction normalisation.

    Paramètres : 
        - dataframe : Un DataFrame pandas. On utilisera toujours un DataFrame dans lequel l'index est le nom des joueurs.
    '''

    dataframe['Nom formate'] = dataframe.index.map(normalisation)


## Fonctions qui mettent les données du tableau dans le bon format

def traitement_pourcentages(dataframe):

    '''
    Ajoute les colonnes A et B à un DataFrame contenant des colonnes de type A/B.
    Permet également de faire passer les données de ces colonnes de chaine de caractères à nombre réel.

    Paramètres :
        - dataframe : Un DataFrame pandas. On utilisera toujours un DataFrame contenant les données de match.
    '''

    # Colonnes à traiter et leurs nouveaux noms
    colonnes_a_traiter = {'totalbuts': ['Total buts', 'Total tirs'],
                          'butstirs': ['Buts dans le jeu', 'Tirs dans le jeu'],
                          'butspenalty': ['Penalty réussis', 'Tirs de Penalty']
                          }

    # Traiter chaque colonne spécifiée
    for col, nouveaux_noms in colonnes_a_traiter.items():
        if col in dataframe.columns:
            # Trouver l'index de la colonne actuelle
            col_index = dataframe.columns.get_loc(col)
        
            # Spliter la colonne en deux et créer les nouvelles colonnes
            nouvelles_valeurs = dataframe[col].str.split(" / ", expand=True)
        
            # Vérifier si les nouvelles colonnes existent déjà
            for i, nouveau_nom in enumerate(nouveaux_noms):
                if nouveau_nom in dataframe.columns:
                    # Supprimer les colonnes existantes avant d'en insérer de nouvelles
                    dataframe.drop(columns=[nouveau_nom], inplace=True)
            
                # Ajouter la colonne avec les nouvelles valeurs
                dataframe.insert(col_index + i, nouveau_nom, pd.to_numeric(nouvelles_valeurs[i], errors='coerce'))


def traitement_temps_jeu(dataframe):

    '''
    Ajoute à un DataFrame une colonne contenant le temps de jeu, en minutes et sous la forme d'un nombre réel.

    Paramètres :
        - dataframe : Un DataFrame pandas. On utilisera toujours un DataFrame contenant le temps de jeu au format "hh:mm:ss"
    ''' 

    # Récupération du temps de jeu
    temps_jeu = dataframe["Temps jeu"].str.split(":")
    temps_jeu_heures = temps_jeu.str[0].astype(float)
    temps_jeu_min = temps_jeu.str[1].astype(float)
    temps_jeu_sec = temps_jeu.str[2].astype(float)

    # Conversion en minutes
    temps_jeu = temps_jeu_heures*60+temps_jeu_min+temps_jeu_sec/60

    dataframe["Minutes jouées"] = temps_jeu.round(2)
    dataframe["Minutes jouées"] = dataframe["Minutes jouées"].fillna(0)


def traitement_float(dataframe):
    
    '''
    Ajoute à un DataFrame une colonne contenant le pourcentage de tirs réussis sous forme d'un nombre réel.

    Paramètres :
        - dataframe : Un DataFrame pandas. On utilisera toujours un DataFrame traité par la fonction traitement_pourcentages.
    '''

    # Pourcentage de tirs réussis
    dataframe['%total numerique']= (dataframe['Total buts'] *100 / np.maximum(dataframe['Total tirs'],1)).round(2)



# Fonction qui gère toutes les étapes de traitement d'un coup

def traitement(dataframe,nom_fichier= None):

    '''
    Effectue le nettoyage des données d'un DataFrame contenant les données de match.
    Télécharge ou renvoie le DataFrame nettoyé.

    Paramètres :
        - dataframe : Un DataFrame pandas. On utilisera toujours un DataFrame contenant les données de match.
        - nom_fichier (optionnel): chaine de caractères de la forme "nom_fichier.csv". Si renseigné, télécharge le DataFrame traité au format csv sous le nom renseigné.
    '''

    nom_formate(dataframe)
    traitement_pourcentages(dataframe)
    traitement_temps_jeu(dataframe)
    traitement_float(dataframe)

    if nom_fichier:
        telechargement_DF(dataframe,nom_fichier)

    else:
        return dataframe


# Fonction qui permet de faire la jointure entre 2 DataFrames

def jointure_df(dataframe1,dataframe2,nom_fichier = None):

    '''
    Crée un DataFrame en joignant les 2 DataFrames passés en argument.
    La jointure s'effectue sur le nom des joueurs, au format Prénom Nom.
    
    Paramètres :
        - dataframe1 : Un DataFrame pandas ayant pour index le nom des joueurs au format Prénom Nom
        - datafraem2 : Un DataFrame pandas. On l'utilisera toujours sur un DataFrame ayant une colonne 'Nom formate'.
        - nom_fichier (optionnel): chaine de caractères de la forme "nom_fichier.csv". Si renseigné, télécharge le DataFrame crée au format csv sous le nom renseigné.

    '''

    if 'Nom formate' in dataframe2.columns:
        donnees_combinees = pd.merge(dataframe1,dataframe2,left_index= True, right_on='Nom formate', how='inner')
        donnees_combinees.set_index('Nom formate', inplace=True)

        if nom_fichier:
            telechargement_DF(donnees_combinees,nom_fichier)
        
        return donnees_combinees
    else:
        raise ValueError("La colonne 'Nom formate' n'appartient pas au DataFrame, jointure impossible")



## Version Cyrille (la version ci-dessus en est une amélioration)
'''
# Fonctions pour normaliser les noms de manière cohérente (inverser Prénom Nom en NOM PRENOM)
def normaliser_nom(nom):
    # Séparer le nom et le prénom
    parties = nom.split()
    if len(parties) >1 :
        # Par défaut, on considère que le prénom n'est composé que d'un seul mot qui est le premier
        return f"{' '.join(parties[1:]).upper()} {parties[0].upper()}"
    return nom  # Si le format n'est pas correct, on laisse tel quel

# Fonction pour traiter les cas particuliers (prénoms+noms en trois mots dont deux pour le prénom) 
def normaliser_prenom_deux_mots(nom):
    parties = nom.split()
    if len(parties) > 2:  # On vérifie qu'il y a au moins trois mots
        # Les deux premiers mots forment le prénom
        prenom = ' '.join(parties[:2])
        nom_famille = ' '.join(parties[2:])
        return f"{nom_famille.upper()} {prenom.upper()}"
    return nom

# Appliquer la première fonction aux index de donnees_physique
donnees_physique['NOM PRENOM'] = donnees_physique.index.map(normaliser_nom)

# Appliquer la deuxième fonction de normalisation sur les lignes non fusionnées
lignes_non_traitees_donnees_physique = donnees_physique[~donnees_physique['NOM PRENOM'].isin(donnees_combinees.index)].copy()
lignes_non_traitees_donnees_physique['NOM PRENOM'] = lignes_non_traitees_donnees_physique.index.to_series().map(normaliser_prenom_deux_mots)

# Copier les lignes non fusionnées normalisées dans 'donnees_physique'
donnees_physique.update(lignes_non_traitees_donnees_physique)

# Créer une nouvelle colonne de noms normalisés dans donnees_match pour mettre tout en majuscules
donnees_match['NOM PRENOM'] = donnees_match.index.str.upper()

# Afficher les noms normalisés
print("\nIndex normalisés dans 'donnees_match' :")
print(donnees_match['NOM PRENOM'].head())

print("\nIndex normalisés dans 'donnees_physique' :")
print(donnees_physique['NOM PRENOM'].head())

# Fusionner les deux DataFrames en utilisant les noms normalisés comme index final
donnees_combinees = pd.merge(donnees_match, donnees_physique, on='NOM PRENOM', how='inner')
donnees_combinees.set_index('NOM PRENOM', inplace=True)

# Vérifier le nombre total de lignes après fusion
print("\nNombre total de lignes dans le DataFrame fusionné :", len(donnees_combinees))

# Lignes qui ne se sont pas fusionnées dans les DataFrames normalisés
lignes_non_fusionnees_match_normalise = donnees_match[~donnees_match['NOM PRENOM'].isin(donnees_combinees.index)]


############### TRAITEMENT DU NOUVEAU DATAFRAME ############
# Colonnes à traiter et leurs nouveaux noms
colonnes_a_traiter = {
    'totalbuts': ['Total buts', 'Total tirs'],
    'butstirs': ['Buts dans le jeu', 'Tirs dans le jeu'],
    'butspenalty': ['Penalty réussis', 'Tirs de Penalty']
}

# Copier le DataFrame pour préserver les données originales
data = donnees_combinees

# Traiter chaque colonne spécifiée
for col, nouveaux_noms in colonnes_a_traiter.items():
    if col in data.columns:
        # Trouver l'index de la colonne actuelle
        col_index = data.columns.get_loc(col)
        
        # Spliter la colonne en deux et créer les nouvelles colonnes
        nouvelles_valeurs = data[col].str.split(" / ", expand=True)
        
        # Vérifier si les nouvelles colonnes existent déjà
        for i, nouveau_nom in enumerate(nouveaux_noms):
            if nouveau_nom in data.columns:
                # Supprimer les colonnes existantes avant d'en insérer de nouvelles
                data.drop(columns=[nouveau_nom], inplace=True)
            
            # Ajouter la colonne avec les nouvelles valeurs
            data.insert(col_index + i, nouveau_nom, pd.to_numeric(nouvelles_valeurs[i], errors='coerce'))
        
        # Supprimer la colonne originale
        data.drop(columns=[col], inplace=True)

# Afficher les premières lignes du DataFrame modifié
data

'''